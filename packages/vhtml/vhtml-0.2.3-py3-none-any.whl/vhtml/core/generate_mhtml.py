import os
import json
import base64
import logging
from datetime import datetime
from pathlib import Path
from typing import Optional, List, Dict, Any

# Configure logging
logger = logging.getLogger('vhtml.mhtml_generator')

def generate_mhtml(document_folder: str, output_file: str) -> bool:
    """
    Generate standards-compliant MHTML file with proper MIME parts for HTML, images, JS, and JSON.
    HTML is NOT base64-encoded; resources are embedded as base64.
    """
    try:
        logger.info(f"Generating MHTML from folder: {document_folder}")
        folder = Path(document_folder)
        name = folder.name
        boundary = "----=_NextPart_000_0000"
        crlf = "\r\n"

        # Find files
        html_files = list(folder.glob("*.html"))
        js_files = list(folder.glob("*.js"))
        json_files = list(folder.glob("*.json"))
        img_files = list(folder.glob("*.png")) + list(folder.glob("*.jpg")) + list(folder.glob("*.jpeg")) + list(folder.glob("*.gif"))

        if not html_files or not json_files:
            logger.error("Missing required HTML or JSON files in the document folder")
            return False

        html_file = html_files[0]
        json_file = json_files[0]

        # JS file is optional
        js_file = js_files[0] if js_files else None

        # Read HTML
        html_content = html_file.read_text(encoding='utf-8')

        # Embed JSON as a <script> tag
        try:
            json_data = json.loads(json_file.read_text(encoding='utf-8'))
            embedded_json = f"<script>window.data = {json.dumps(json_data, ensure_ascii=False, indent=2)};</script>"
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {json_file}: {e}")
            return False

        # Embed JS if present
        js_content = ""
        if js_file:
            js_content = js_file.read_text(encoding='utf-8')
            js_content = f"<script>\n{js_content}\n</script>"

        # Place embedded JSON and JS
        final_html = html_content
        if "<!--DATA-->" in html_content:
            final_html = final_html.replace("<!--DATA-->", embedded_json)
        else:
            final_html = final_html.replace("</body>", f"{embedded_json}{crlf}</body>")
        if js_content:
            if "<!--SCRIPT-->" in html_content:
                final_html = final_html.replace("<!--SCRIPT-->", js_content)
            else:
                final_html = final_html.replace("</body>", f"{js_content}{crlf}</body>")

        # Don't embed images as base64 in HTML; let MHTML handle them as separate parts

        # Prepare MHTML parts
        parts = []

        # HTML part (plain text)
        parts.append(
            f"--{boundary}{crlf}"
            f"Content-Type: text/html; charset=\"utf-8\"{crlf}"
            f"Content-Transfer-Encoding: 8bit{crlf}"
            f"Content-Location: {html_file.name}{crlf}{crlf}"
            f"{final_html}{crlf}"
        )

        # JS part
        if js_file:
            js_data = js_file.read_bytes()
            js_b64 = base64.b64encode(js_data).decode('ascii')
            parts.append(
                f"--{boundary}{crlf}"
                f"Content-Type: application/javascript{crlf}"
                f"Content-Transfer-Encoding: base64{crlf}"
                f"Content-Location: {js_file.name}{crlf}{crlf}"
                f"{js_b64}{crlf}"
            )

        # JSON part
        json_data_bytes = json_file.read_bytes()
        json_b64 = base64.b64encode(json_data_bytes).decode('ascii')
        parts.append(
            f"--{boundary}{crlf}"
            f"Content-Type: application/json{crlf}"
            f"Content-Transfer-Encoding: base64{crlf}"
            f"Content-Location: {json_file.name}{crlf}{crlf}"
            f"{json_b64}{crlf}"
        )

        # Image parts
        for img in img_files:
            img_bytes = img.read_bytes()
            img_b64 = base64.b64encode(img_bytes).decode('ascii')
            # Determine MIME type
            ext = img.suffix.lower()
            if ext == '.png':
                mime = 'image/png'
            elif ext in ('.jpg', '.jpeg'):
                mime = 'image/jpeg'
            elif ext == '.gif':
                mime = 'image/gif'
            else:
                mime = 'application/octet-stream'
            parts.append(
                f"--{boundary}{crlf}"
                f"Content-Type: {mime}{crlf}"
                f"Content-Transfer-Encoding: base64{crlf}"
                f"Content-Location: {img.name}{crlf}{crlf}"
                f"{img_b64}{crlf}"
            )

        # End boundary
        parts.append(f"--{boundary}--{crlf}")

        # Compose full MHTML
        now = datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')
        mhtml_header = (
            f"From: <Saved by vHTML>{crlf}"
            f"Subject: {name}{crlf}"
            f"Date: {now}{crlf}"
            f"MIME-Version: 1.0{crlf}"
            f"Content-Type: multipart/related; boundary=\"{boundary}\"; type=\"text/html\"{crlf}{crlf}"
        )
        mhtml = mhtml_header + ''.join(parts)

        # Write file
        output_path = Path(output_file)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with output_path.open('w', encoding='utf-8', newline='') as f:
            f.write(mhtml)
        logger.info(f"Successfully generated MHTML: {output_file}")
        print(f"✅ Generated MHTML: {output_file}")
        return True

    except Exception as e:
        logger.error(f"Error generating MHTML: {str(e)}", exc_info=True)
        print(f"❌ Error generating MHTML: {str(e)}")
        return False


def main():
    """Command line interface for MHTML generation"""
    import argparse
    import sys

    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate MHTML file from document folder")
    parser.add_argument(
        "input_folder",
        help="Path to the folder containing document files (HTML, JSON, JS)"
    )
    parser.add_argument(
        "-o", "--output",
        help="Output MHTML file path (default: <input_folder>.mhtml)",
        default=None
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )

    # Parse arguments
    args = parser.parse_args()

    # Set up logging
    log_level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

    # Determine output file path
    input_path = Path(args.input_folder)
    output_file = args.output
    if not output_file:
        output_file = input_path.with_suffix('.mhtml')

    # Generate MHTML
    success = generate_mhtml(args.input_folder, output_file)

    # Exit with appropriate status code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

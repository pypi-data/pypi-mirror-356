import os
import json
import base64
from pathlib import Path
from bs4 import BeautifulSoup

def embed_images_in_html(html: str, folder: Path) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    for img in soup.find_all('img'):
        src = img.get('src')
        if not src or src.startswith('data:') or src.startswith(('http://', 'https://')):
            continue

        img_path = folder / src
        if img_path.exists():
            mime = "image/png"
            if img_path.suffix.lower() in ['.jpg', '.jpeg']:
                mime = "image/jpeg"
            elif img_path.suffix.lower() == '.gif':
                mime = "image/gif"

            with open(img_path, 'rb') as f:
                b64 = base64.b64encode(f.read()).decode('utf-8')
                img['src'] = f"data:{mime};base64,{b64}"

    return str(soup)

def create_standalone_html(folder_path: str, output_file: str):
    folder = Path(folder_path)
    html_file = next(folder.glob("*.html"))
    json_file = next(folder.glob("*.json"))
    js_files = list(folder.glob("*.js"))

    html_content = html_file.read_text(encoding='utf-8')
    json_data = json.loads(json_file.read_text(encoding='utf-8'))
    json_script = f"<script>window.data = {json.dumps(json_data, indent=2, ensure_ascii=False)};</script>"

    js_script = ""
    if js_files:
        js = js_files[0].read_text(encoding='utf-8')
        js_script = f"<script>\n{js}\n</script>"

    # Wstaw dane i skrypt
    final_html = html_content
    if "<!--DATA-->" in final_html:
        final_html = final_html.replace("<!--DATA-->", json_script)
    else:
        final_html = final_html.replace("</body>", f"{json_script}</body>")

    if "<!--SCRIPT-->" in final_html:
        final_html = final_html.replace("<!--SCRIPT-->", js_script)
    else:
        final_html = final_html.replace("</body>", f"{js_script}</body>")

    # Osadź obrazki
    final_html = embed_images_in_html(final_html, folder)

    # Zapisz wynik
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"✅ Wygenerowano plik HTML: {output_file}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generuje samodzielny plik HTML z folderu dokumentu")
    parser.add_argument("folder", help="Ścieżka do folderu z dokumentem")
    parser.add_argument("-o", "--output", default="output.html", help="Plik wynikowy (HTML)")

    args = parser.parse_args()
    create_standalone_html(args.folder, args.output)

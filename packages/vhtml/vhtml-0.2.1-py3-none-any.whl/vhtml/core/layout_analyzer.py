#!/usr/bin/env python3
"""
PDF to HTML Analyzer with OpenCV and OCR
Modularny system do analizy dokumentów PDF i konwersji do HTML z metadanymi
"""

import cv2
import numpy as np
import pytesseract
from pdf2image import convert_from_path
from PIL import Image, ImageDraw
import json
import os
import logging
from dataclasses import dataclass, asdict
from typing import List, Dict, Tuple, Optional
from langdetect import detect
import re
from jinja2 import Template
import base64
from io import BytesIO

# Configure logging
logger = logging.getLogger('vhtml.layout_analyzer')


@dataclass
class Block:
    """Reprezentacja bloku tekstu w dokumencie"""
    id: str
    type: str  # header, content, table, footer
    position: Dict[str, int]  # x, y, width, height
    content: str
    language: str
    confidence: float
    formatting: Dict
    image_data: str = ""  # base64 encoded image
    
    def to_dict(self) -> Dict:
        """Konwertuje obiekt Block do słownika do serializacji JSON"""
        return {
            'id': self.id,
            'type': self.type,
            'position': self.position,
            'content': self.content,
            'language': self.language,
            'confidence': self.confidence,
            'formatting': self.formatting,
            'image_data': self.image_data if self.image_data else ""
        }


@dataclass
class DocumentMetadata:
    """Metadane całego dokumentu"""
    doc_type: str  # invoice, form, letter, other
    language: str
    layout: str  # 4-block, 6-block, custom
    confidence: float
    blocks: List[Block]


class PDFProcessor:
    """Procesor PDF do konwersji na obrazy"""

    def __init__(self, dpi=300):
        self.dpi = dpi

    def pdf_to_images(self, pdf_path: str) -> List[Image.Image]:
        """Konwertuje PDF do listy obrazów"""
        logger.info(f"Rozpoczynanie konwersji pliku PDF: {pdf_path}")
        try:
            images = convert_from_path(pdf_path, dpi=self.dpi)
            logger.info(f"Pomyślnie przekonwertowano {len(images)} stron z pliku {os.path.basename(pdf_path)}")
            return images
        except Exception as e:
            logger.error(f"Błąd podczas konwersji pliku PDF {pdf_path}: {str(e)}", exc_info=True)
            return []


class LayoutAnalyzer:
    """Analizator układu dokumentu wykorzystujący OpenCV"""

    def __init__(self):
        self.logger = logging.getLogger('vhtml.layout_analyzer')
        self.min_contour_area = 1000
        self.block_templates = {
            'invoice': self._get_invoice_template(),
            '6-column': self._get_6_column_template(),
            'universal': self._get_universal_template()
        }
        self.logger.debug("Zainicjalizowano LayoutAnalyzer z szablonami: %s", 
                         list(self.block_templates.keys()))

    def analyze_layout(self, image: Image.Image) -> Tuple[str, List[Dict]]:
        """Analizuje układ dokumentu i zwraca typ oraz bloki"""
        self.logger.info("Rozpoczynanie analizy układu dokumentu")
        try:
            cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
            self.logger.debug("Przekonwertowano obraz do formatu OpenCV")

            # Preprocessing
            self.logger.debug("Przetwarzanie wstępne obrazu")
            gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
            denoised = cv2.fastNlMeansDenoising(gray)
            self.logger.debug("Zakończono przetwarzanie wstępne obrazu")

            # Wykrywanie bloków tekstu
            self.logger.debug("Wykrywanie bloków tekstu")
            blocks = self._detect_text_blocks(denoised)
            self.logger.info(f"Wykryto {len(blocks)} bloków tekstu")

            # Klasyfikacja układu
            self.logger.debug("Klasyfikacja układu dokumentu")
            layout_type = self._classify_layout(blocks, image.size)
            self.logger.info(f"Zidentyfikowano typ układu: {layout_type}")

            return layout_type, blocks
            
        except Exception as e:
            self.logger.error(f"Błąd podczas analizy układu dokumentu: {str(e)}", exc_info=True)
            raise

    def _detect_text_blocks(self, gray_image) -> List[Dict]:
        """Wykrywa bloki tekstu używając OpenCV"""
        # Morfologia do łączenia bliskich elementów tekstu
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 10))
        dilated = cv2.dilate(gray_image, kernel, iterations=2)

        # Threshold i inwersja
        _, thresh = cv2.threshold(dilated, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        # Znajdź kontury
        contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        blocks = []
        for i, contour in enumerate(contours):
            area = cv2.contourArea(contour)
            if area > self.min_contour_area:
                x, y, w, h = cv2.boundingRect(contour)
                blocks.append({
                    'id': f'block_{i}',
                    'position': {'x': x, 'y': y, 'width': w, 'height': h},
                    'area': area
                })

        # Sortuj bloki według pozycji (góra-dół, lewo-prawo)
        blocks.sort(key=lambda b: (b['position']['y'], b['position']['x']))

        return blocks

    def _classify_layout(self, blocks: List[Dict], image_size: Tuple[int, int]) -> str:
        """Klasyfikuje typ układu dokumentu"""
        num_blocks = len(blocks)
        width, height = image_size

        if num_blocks == 4:
            # Sprawdź czy to układ faktury
            top_blocks = [b for b in blocks if b['position']['y'] < height * 0.3]
            if len(top_blocks) == 2:
                return 'invoice'

        elif num_blocks == 6:
            # Sprawdź czy to układ 6-kolumnowy
            rows = self._group_blocks_by_rows(blocks, height)
            if len(rows) == 3 and all(len(row) == 2 for row in rows):
                return '6-column'

        return 'universal'

    def _group_blocks_by_rows(self, blocks: List[Dict], image_height: int) -> List[List[Dict]]:
        """Grupuje bloki w rzędy"""
        rows = []
        current_row = []
        current_y = None
        tolerance = image_height * 0.05  # 5% tolerancji

        for block in blocks:
            y = block['position']['y']

            if current_y is None or abs(y - current_y) <= tolerance:
                current_row.append(block)
                current_y = y if current_y is None else current_y
            else:
                if current_row:
                    rows.append(current_row)
                current_row = [block]
                current_y = y

        if current_row:
            rows.append(current_row)

        return rows

    def _get_invoice_template(self) -> Dict:
        return {
            'name': 'invoice',
            'blocks': ['sender', 'recipient', 'items_table', 'payment_summary']
        }

    def _get_6_column_template(self) -> Dict:
        return {
            'name': '6-column',
            'blocks': ['A', 'B', 'C', 'D', 'E', 'F']
        }

    def _get_universal_template(self) -> Dict:
        return {
            'name': 'universal',
            'blocks': 'dynamic'
        }


class OCREngine:
    """Silnik OCR z rozpoznawaniem języka"""

    def __init__(self):
        self.languages = {
            'pl': 'pol',
            'en': 'eng',
            'de': 'deu'
        }

    def extract_text_from_block(self, image: Image.Image, block_position: Dict) -> Tuple[str, str, float]:
        """Wyciąga tekst z bloku obrazu"""
        # Wytnij blok z obrazu
        x, y, w, h = block_position['x'], block_position['y'], block_position['width'], block_position['height']
        block_image = image.crop((x, y, x + w, y + h))

        # OCR z kilkoma językami
        custom_config = r'--oem 3 --psm 6 -l pol+eng+deu'
        text = pytesseract.image_to_string(block_image, config=custom_config)

        # Rozpoznaj język
        language = self._detect_language(text)

        # Oblicz pewność OCR
        confidence = self._calculate_ocr_confidence(block_image, text)

        return text.strip(), language, confidence

    def _detect_language(self, text: str) -> str:
        """Rozpoznaje język tekstu"""
        try:
            if len(text.strip()) < 10:
                return 'unknown'
            detected = detect(text)
            return detected if detected in self.languages else 'en'
        except:
            return 'en'

    def _calculate_ocr_confidence(self, image: Image.Image, text: str) -> float:
        """Oblicza pewność OCR"""
        try:
            # Użyj pytesseract do obliczenia pewności
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            confidences = [int(conf) for conf in data['conf'] if int(conf) > 0]
            return np.mean(confidences) / 100.0 if confidences else 0.5
        except:
            return 0.5


class HTMLGenerator:
    """Generator HTML z metadanymi JSON"""

    def __init__(self):
        self.base_template = self._get_base_template()

    def generate_html(self, metadata: DocumentMetadata, images: List[Image.Image]) -> str:
        """Generuje HTML z metadanymi"""

        # Przygotuj dane dla szablonu
        template_data = {
            'document': asdict(metadata),
            'blocks': []
        }

        # Przygotuj bloki z obrazami
        for i, block in enumerate(metadata.blocks):
            # Konwertuj obraz bloku do base64
            if i < len(images):
                block_image = self._extract_block_image(images[0], block.position)
                block.image_data = self._image_to_base64(block_image)

            template_data['blocks'].append(asdict(block))

        # Renderuj template
        template = Template(self.base_template)
        html_content = template.render(**template_data)

        return html_content

    def _extract_block_image(self, full_image: Image.Image, position: Dict) -> Image.Image:
        """Wycina obraz bloku z pełnego obrazu"""
        x, y, w, h = position['x'], position['y'], position['width'], position['height']
        return full_image.crop((x, y, x + w, y + h))

    def _image_to_base64(self, image: Image.Image) -> str:
        """Konwertuje obraz do base64"""
        buffer = BytesIO()
        image.save(buffer, format='PNG')
        img_str = base64.b64encode(buffer.getvalue()).decode()
        return f"data:image/png;base64,{img_str}"

    def _get_base_template(self) -> str:
        """Zwraca szablon HTML"""
        return '''
<!DOCTYPE html>
<html lang="{{ document.language }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document Analysis - {{ document.doc_type }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f5f5f5;
        }
        .document-container {
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
            overflow: hidden;
        }
        .document-header {
            background: #2c3e50;
            color: white;
            padding: 20px;
        }
        .document-info {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-top: 10px;
        }
        .info-item {
            background: rgba(255,255,255,0.1);
            padding: 10px;
            border-radius: 4px;
        }
        .blocks-container {
            padding: 20px;
        }
        .block {
            margin-bottom: 30px;
            border: 1px solid #ddd;
            border-radius: 8px;
            overflow: hidden;
            background: white;
        }
        .block-header {
            background: #34495e;
            color: white;
            padding: 15px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .block-meta {
            font-size: 0.9em;
            opacity: 0.8;
        }
        .block-content {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            padding: 20px;
        }
        .block-image {
            text-align: center;
        }
        .block-image img {
            max-width: 100%;
            border: 1px solid #ddd;
            border-radius: 4px;
        }
        .block-text {
            background: #f8f9fa;
            padding: 15px;
            border-radius: 4px;
            border-left: 4px solid #3498db;
        }
        .confidence-bar {
            height: 4px;
            background: #ecf0f1;
            border-radius: 2px;
            margin-top: 10px;
            overflow: hidden;
        }
        .confidence-fill {
            height: 100%;
            background: linear-gradient(90deg, #e74c3c, #f39c12, #27ae60);
            transition: width 0.3s ease;
        }
        .metadata-json {
            background: #2c3e50;
            color: #ecf0f1;
            padding: 15px;
            margin-top: 10px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
            white-space: pre-wrap;
            max-height: 200px;
            overflow-y: auto;
        }
        .stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 15px;
            margin-top: 20px;
        }
        .stat-card {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 20px;
            border-radius: 8px;
            text-align: center;
        }
        .stat-value {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }
        .language-badge {
            background: #27ae60;
            color: white;
            padding: 4px 8px;
            border-radius: 12px;
            font-size: 0.8em;
            margin-left: 10px;
        }

        @media (max-width: 768px) {
            .block-content {
                grid-template-columns: 1fr;
            }
            .document-info {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="document-container">
        <div class="document-header">
            <h1>Analiza Dokumentu: {{ document.doc_type.title() }}</h1>
            <div class="document-info">
                <div class="info-item">
                    <strong>Typ układu:</strong> {{ document.layout }}
                </div>
                <div class="info-item">
                    <strong>Język:</strong> {{ document.language.upper() }}
                </div>
                <div class="info-item">
                    <strong>Pewność:</strong> {{ "%.1f"|format(document.confidence * 100) }}%
                </div>
                <div class="info-item">
                    <strong>Liczba bloków:</strong> {{ document.blocks|length }}
                </div>
            </div>
        </div>

        <div class="blocks-container">
            {% for block in blocks %}
            <div class="block">
                <div class="block-header">
                    <div>
                        <h3>Blok {{ block.id|upper }} - {{ block.type|title }}</h3>
                        <div class="block-meta">
                            Pozycja: {{ block.position.x }}, {{ block.position.y }} 
                            | Rozmiar: {{ block.position.width }}×{{ block.position.height }}
                            <span class="language-badge">{{ block.language|upper }}</span>
                        </div>
                    </div>
                    <div>
                        Pewność: {{ "%.1f"|format(block.confidence * 100) }}%
                    </div>
                </div>

                <div class="block-content">
                    <div class="block-image">
                        <h4>Oryginalny fragment:</h4>
                        {% if block.image_data %}
                        <img src="{{ block.image_data }}" alt="Blok {{ block.id }}">
                        {% else %}
                        <div style="padding: 40px; background: #ecf0f1; color: #7f8c8d;">
                            Brak obrazu
                        </div>
                        {% endif %}
                    </div>

                    <div class="block-text">
                        <h4>Rozpoznany tekst:</h4>
                        <p>{{ block.content or "Brak rozpoznanego tekstu" }}</p>

                        <div class="confidence-bar">
                            <div class="confidence-fill" style="width: {{ block.confidence * 100 }}%"></div>
                        </div>

                        <details>
                            <summary>Metadane JSON</summary>
                            <div class="metadata-json">{{ block|tojson(indent=2) }}</div>
                        </details>
                    </div>
                </div>
            </div>
            {% endfor %}
        </div>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-value">{{ document.blocks|length }}</div>
                <div>Bloków tekstu</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ "%.0f"|format(document.confidence * 100) }}%</div>
                <div>Średnia pewność</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{{ document.language|upper }}</div>
                <div>Język główny</div>
            </div>
        </div>
    </div>

    <script>
        // Interaktywne funkcje
        document.addEventListener('DOMContentLoaded', function() {
            console.log('Dokument załadowany');
            console.log('Metadane:', {{ document|tojson }});
        });
    </script>
</body>
</html>
        '''


class DocumentAnalyzer:
    """Główna klasa systemu analizy dokumentów"""

    def __init__(self):
        self.pdf_processor = PDFProcessor()
        self.layout_analyzer = LayoutAnalyzer()
        self.ocr_engine = OCREngine()
        self.html_generator = HTMLGenerator()

    def analyze_document(self, pdf_path: str, output_dir: str = "output") -> str:
        """Analizuje dokument PDF i generuje HTML"""
        print(f"Rozpoczynam analizę dokumentu: {pdf_path}")

        # Krok 1: Konwersja PDF do obrazów
        images = self.pdf_processor.pdf_to_images(pdf_path)
        if not images:
            raise ValueError("Nie udało się przetworzyć PDF")

        print(f"Przetworzone strony: {len(images)}")

        # Krok 2: Analiza pierwszej strony (możliwość rozszerzenia na wszystkie)
        first_page = images[0]
        layout_type, detected_blocks = self.layout_analyzer.analyze_layout(first_page)

        print(f"Wykryty układ: {layout_type}, bloków: {len(detected_blocks)}")

        # Krok 3: OCR dla każdego bloku
        blocks = []
        total_confidence = 0

        for i, block_data in enumerate(detected_blocks):
            text, language, confidence = self.ocr_engine.extract_text_from_block(
                first_page, block_data['position']
            )

            block = Block(
                id=chr(65 + i),  # A, B, C, D...
                type=self._classify_block_type(text, i, layout_type),
                position=block_data['position'],
                content=text,
                language=language,
                confidence=confidence,
                formatting=self._analyze_formatting(text)
            )

            blocks.append(block)
            total_confidence += confidence

            print(f"Blok {block.id}: {len(text)} znaków, język: {language}, pewność: {confidence:.2f}")

        # Krok 4: Utworzenie metadanych dokumentu
        avg_confidence = total_confidence / len(blocks) if blocks else 0
        doc_language = self._determine_document_language(blocks)

        metadata = DocumentMetadata(
            doc_type=self._classify_document_type(layout_type, blocks),
            language=doc_language,
            layout=layout_type,
            confidence=avg_confidence,
            blocks=blocks
        )

        # Krok 5: Generowanie HTML
        html_content = self.html_generator.generate_html(metadata, images)

        # Krok 6: Zapis plików
        os.makedirs(output_dir, exist_ok=True)

        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        html_path = os.path.join(output_dir, f"{base_name}.html")
        json_path = os.path.join(output_dir, f"{base_name}_metadata.json")

        # Zapisz HTML
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)

        # Zapisz metadane JSON
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(metadata), f, ensure_ascii=False, indent=2)

        print(f"Analiza zakończona!")
        print(f"HTML: {html_path}")
        print(f"JSON: {json_path}")

        return html_path

    def _classify_block_type(self, text: str, block_index: int, layout_type: str) -> str:
        """Klasyfikuje typ bloku na podstawie zawartości"""
        text_lower = text.lower()

        if layout_type == 'invoice':
            if block_index == 0:
                return 'sender'
            elif block_index == 1:
                return 'recipient'
            elif 'tabela' in text_lower or 'pozycja' in text_lower:
                return 'items_table'
            else:
                return 'payment_summary'

        # Uniwersalne reguły
        if any(word in text_lower for word in ['nagłówek', 'tytuł', 'header', 'title']):
            return 'header'
        elif any(word in text_lower for word in ['tabela', 'table', 'lista', 'pozycja']):
            return 'table'
        elif any(word in text_lower for word in ['suma', 'razem', 'total', 'płatność', 'payment']):
            return 'footer'
        else:
            return 'content'

    def _analyze_formatting(self, text: str) -> Dict:
        """Analizuje formatowanie tekstu"""
        formatting = {
            'bold': [],
            'tables': [],
            'lists': [],
            'numbers': []
        }

        # Wykryj numery/kwoty
        numbers = re.findall(r'\d+[,.]?\d*', text)
        formatting['numbers'] = numbers

        # Wykryj listy
        if re.search(r'^\s*[-*•]\s', text, re.MULTILINE):
            formatting['lists'] = ['bullet_list']
        elif re.search(r'^\s*\d+\.\s', text, re.MULTILINE):
            formatting['lists'] = ['numbered_list']

        return formatting

    def _determine_document_language(self, blocks: List[Block]) -> str:
        """Określa główny język dokumentu"""
        language_counts = {}
        for block in blocks:
            lang = block.language
            language_counts[lang] = language_counts.get(lang, 0) + len(block.content)

        return max(language_counts.items(), key=lambda x: x[1])[0] if language_counts else 'en'

    def _classify_document_type(self, layout_type: str, blocks: List[Block]) -> str:
        """Klasyfikuje typ dokumentu"""
        if layout_type == 'invoice':
            return 'invoice'
        elif layout_type == '6-column':
            return 'form'

        # Analiza zawartości dla uniwersalnego układu
        all_text = ' '.join([block.content.lower() for block in blocks])

        if any(word in all_text for word in ['faktura', 'invoice', 'rachunek']):
            return 'invoice'
        elif any(word in all_text for word in ['wniosek', 'formularz', 'application', 'form']):
            return 'form'
        elif any(word in all_text for word in ['list', 'letter', 'pismo']):
            return 'letter'
        else:
            return 'document'


def main():
    """Funkcja główna - przykład użycia"""
    import sys

    if len(sys.argv) < 2:
        print("Użycie: python pdf_analyzer.py <ścieżka_do_pdf>")
        sys.exit(1)

    pdf_path = sys.argv[1]

    if not os.path.exists(pdf_path):
        print(f"Plik nie istnieje: {pdf_path}")
        sys.exit(1)

    try:
        analyzer = DocumentAnalyzer()
        html_path = analyzer.analyze_document(pdf_path)
        print(f"\n✅ Sukces! HTML wygenerowany: {html_path}")

        # Opcjonalnie otwórz w przeglądarce
        import webbrowser
        webbrowser.open(f'file://{os.path.abspath(html_path)}')

    except Exception as e:
        print(f"❌ Błąd podczas analizy: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
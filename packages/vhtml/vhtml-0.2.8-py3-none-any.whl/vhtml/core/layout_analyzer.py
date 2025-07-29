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
from dataclasses import dataclass, asdict, field
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
    blocks: List[Block] = None
    pages: List[Dict] = None
    source_file: str = ""
    processing_time: float = 0.0
    
    def __post_init__(self):
        """Inicjalizacja pól po utworzeniu obiektu"""
        # Initialize blocks if not provided
        if self.blocks is None:
            self.blocks = []
            
        # Initialize pages if not provided
        if self.pages is None:
            self.pages = []
            
        # If pages is empty but we have blocks, create default page structure
        if not self.pages and self.blocks:
            self.pages = [{
                'number': 1,
                'blocks': [block.to_dict() for block in self.blocks]
            }]
        # If blocks is empty but we have pages, extract blocks from pages
        elif not self.blocks and self.pages:
            # This is a simplified approach - in a real scenario, you'd need to convert
            # the dicts back to Block objects, but for now we'll just use an empty list
            self.blocks = []
            
    def to_dict(self):
        """Convert the metadata to a dictionary"""
        return {
            'doc_type': self.doc_type,
            'language': self.language,
            'layout': self.layout,
            'confidence': self.confidence,
            'source_file': self.source_file,
            'processing_time': self.processing_time,
            'pages': self.pages,
            'blocks': [block.to_dict() if hasattr(block, 'to_dict') else block 
                      for block in self.blocks]
        }


class PDFProcessor:
    """Procesor PDF do konwersji na obrazy"""

    def __init__(self, dpi=300):
        self.dpi = dpi

    def pdf_to_images(self, pdf_path: str, output_dir: str) -> List[str]:
        """Konwertuje plik PDF na obrazy PNG"""
        try:
            # Create output directory if it doesn't exist
            os.makedirs(output_dir, exist_ok=True)
            
            # Convert PDF to images
            images = convert_from_path(
                pdf_path,
                dpi=self.dpi,
                fmt='png',
                output_folder=output_dir,
                output_file=os.path.splitext(os.path.basename(pdf_path))[0]
            )
            
            # Save images as PNG
            image_paths = []
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            
            for i, image in enumerate(images):
                image_path = os.path.join(output_dir, f"{base_name}_page_{i+1:03d}.png")
                image.save(image_path, 'PNG', quality=100)
                image_paths.append(image_path)
            
            logger.info(f"Saved {len(image_paths)} PNG images to {output_dir}")
            return image_paths
            
        except Exception as e:
            logger.error(f"Błąd podczas konwersji PDF na obrazy: {e}", exc_info=True)
            raise


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
        self.logger.debug("Rozpoczynanie wykrywania bloków tekstu")
        try:
            # Morfologia do łączenia bliskich elementów tekstu
            self.logger.debug("Stosowanie operacji morfologicznych do łączenia elementów tekstu")
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (50, 10))
            dilated = cv2.dilate(gray_image, kernel, iterations=2)

            # Threshold i inwersja
            self.logger.debug("Binaryzacja obrazu")
            _, thresh = cv2.threshold(dilated, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

            # Znajdź kontury
            self.logger.debug("Wyszukiwanie konturów")
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            self.logger.debug(f"Znaleziono {len(contours)} konturów")

            blocks = []
            valid_contours = 0
            self.logger.debug(f"Przetwarzanie konturów (min. obszar: {self.min_contour_area} pikseli)")
            
            for i, contour in enumerate(contours):
                area = cv2.contourArea(contour)
                # Filtruj małe kontury
                if area < self.min_contour_area:
                    self.logger.debug(f"Pominięto kontur {i}: zbyt mały obszar ({area:.0f} < {self.min_contour_area})")
                    continue
                    
                # Pobierz współrzędne prostokąta
                x, y, w, h = cv2.boundingRect(contour)
                valid_contours += 1
                
                # Dodaj blok
                blocks.append({
                    'id': f'block_{i}',
                    'position': {
                        'x': x,
                        'y': y,
                        'width': w,
                        'height': h
                    },
                    'area': area
                })
                self.logger.debug(f"Dodano blok {i}: x={x}, y={y}, w={w}, h={h}, area={area:.0f}")
                
            self.logger.info(f"Zidentyfikowano {valid_contours} poprawnych bloków tekstu")
            return blocks
            
        except Exception as e:
            self.logger.error(f"Błąd podczas wykrywania bloków tekstu: {str(e)}", exc_info=True)
            raise

    def _classify_layout(self, blocks: List[Dict], page_size: Tuple[int, int]) -> str:
        """Klasyfikuje układ dokumentu na podstawie wykrytych bloków"""
        self.logger.debug("Rozpoczynanie klasyfikacji układu dokumentu")
        
        if not blocks:
            self.logger.warning("Brak bloków do analizy - zwracam 'unknown'")
            return 'unknown'
            
        # Prosta heurystyka do klasyfikacji układu
        if len(blocks) >= 6:
            self.logger.debug(f"Wykryto układ '6-column' na podstawie liczby bloków ({len(blocks)})")
            return '6-column'
            
        # Sprawdź czy którykolwiek z bloków to tabela
        table_blocks = [b for b in blocks if b.get('type') == 'table']
        if table_blocks:
            self.logger.debug(f"Wykryto układ 'invoice' na podstawie obecności {len(table_blocks)} tabel")
            return 'invoice'
            
        self.logger.debug("Wykorzystano domyślny układ 'universal'")
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
        self.logger = logging.getLogger('vhtml.ocr_engine')
        self.languages = {
            'pl': 'pol',
            'en': 'eng',
            'de': 'deu'
        }
        self.logger.debug("Zainicjalizowano silnik OCR z obsługą języków: %s", 
                         list(self.languages.keys()))

    def extract_text_from_block(self, image: Image.Image, block_position: Dict) -> Tuple[str, str, float]:
        """Wyciąga tekst z bloku obrazu"""
        self.logger.debug("Rozpoczynanie ekstrakcji tekstu z bloku")
        try:
            # Wyciągnij współrzędne bloku
            x, y, w, h = block_position['x'], block_position['y'], block_position['width'], block_position['height']
            self.logger.debug(f"Współrzędne bloku: x={x}, y={y}, width={w}, height={h}")
            
            # Wytnij obszar bloku
            block_img = image.crop((x, y, x + w, y + h))
            
            # Konwersja do OpenCV do dalszego przetwarzania
            cv_img = cv2.cvtColor(np.array(block_img), cv2.COLOR_RGB2BGR)
            self.logger.debug("Konwersja do formatu OpenCV zakończona")
            
            # Preprocessing obrazu
            self.logger.debug("Przetwarzanie wstępne obrazu (konwersja do skali szarości i usuwanie szumów)")
            gray = cv2.cvtColor(cv_img, cv2.COLOR_BGR2GRAY)
            denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
            
            # OCR
            self.logger.debug("Wykonywanie OCR na bloku obrazu")
            text = pytesseract.image_to_string(denoised, lang='pol+eng')
            self.logger.debug(f"Rozpoznany tekst (pierwsze 50 znaków): {text[:50]}...")
            
            # Rozpoznaj język
            language = self._detect_language(text)
            self.logger.debug(f"Rozpoznany język: {language}")
            
            # Oblicz pewność OCR
            confidence = self._calculate_ocr_confidence(denoised, text)
            self.logger.info(f"Zakończono ekstrakcję tekstu (pewność: {confidence:.2f}%)")
            
            return text.strip(), language, confidence
            
        except Exception as e:
            self.logger.error(f"Błąd podczas ekstrakcji tekstu: {str(e)}", exc_info=True)
            return "", "unknown", 0.0

    def _detect_language(self, text: str) -> str:
        """Rozpoznaje język tekstu"""
        self.logger.debug("Rozpoczynanie rozpoznawania języka")
        if not text.strip():
            self.logger.warning("Brak tekstu do analizy języka")
            return 'unknown'
            
        try:
            # Użyj pierwszych 1000 znaków dla lepszej wydajności
            sample_text = text[:1000]
            self.logger.debug(f"Próbka tekstu do analizy języka (pierwsze 100 znaków): {sample_text[:100]}...")
            
            lang = detect(sample_text)
            detected_lang = self.languages.get(lang, 'unknown')
            self.logger.info(f"Rozpoznany język: {detected_lang} (kod: {lang})")
            
            return detected_lang
            
        except Exception as e:
            self.logger.error(f"Błąd podczas rozpoznawania języka: {str(e)}", exc_info=True)
            return 'unknown'

    def _calculate_ocr_confidence(self, image: np.ndarray, text: str) -> float:
        """Oblicza pewność OCR na podstawie jakości obrazu i długości tekstu"""
        self.logger.debug("Obliczanie pewności OCR")
        
        if not text.strip():
            self.logger.warning("Brak tekstu - pewność OCR wynosi 0%")
            return 0.0
            
        try:
            # Oblicz jakość obrazu na podstawie średniej wartości pikseli
            img_quality = np.mean(image) / 255.0
            self.logger.debug(f"Jakość obrazu: {img_quality:.2f}")
            
            # Oblicz jakość tekstu na podstawie długości
            text_quality = min(1.0, len(text) / 100.0)
            self.logger.debug(f"Jakość tekstu (długość): {text_quality:.2f}")
            
            # Połącz oba wskaźniki z wagami
            confidence = (img_quality * 0.7 + text_quality * 0.3) * 100
            self.logger.info(f"Obliczona pewność OCR: {confidence:.2f}%")
            
            return confidence
            
        except Exception as e:
            self.logger.error(f"Błąd podczas obliczania pewności OCR: {str(e)}", exc_info=True)
            return 0.0


class HTMLGenerator:
    """Generator HTML z metadanymi JSON"""

    def __init__(self):
        self.logger = logging.getLogger('vhtml.html_generator')
        self.logger.debug("Inicjalizacja generatora HTML")
        self.base_template = self._get_base_template()
        self.logger.debug("Załadowano szablon bazowy HTML")

    def generate_html(self, metadata: DocumentMetadata, images: List[Image.Image]) -> str:
        """Generuje HTML z metadanymi"""
        self.logger.info("Rozpoczynanie generowania HTML")
        try:
            # Przygotuj dane do szablonu
            self.logger.debug("Przygotowywanie metadanych dokumentu")
            template_data = {
                'title': f'Dokument - {metadata.doc_type}',
                'metadata': asdict(metadata),
                'blocks': [asdict(block) for block in metadata.blocks]
            }
            
            self.logger.debug(f"Przygotowano dane dla {len(metadata.blocks)} bloków")
            
            # Renderuj szablon
            self.logger.debug("Renderowanie szablonu HTML")
            template = Template(self.base_template)
            html_content = template.render(**template_data)
            
            self.logger.info(f"Wygenerowano HTML o rozmiarze {len(html_content)} bajtów")
            return html_content
            
        except Exception as e:
            self.logger.error(f"Błąd podczas generowania HTML: {str(e)}", exc_info=True)
            raise

    def _extract_block_image(self, full_image: Image.Image, position: Dict) -> Image.Image:
        """Wycina obraz bloku z pełnego obrazu"""
        self.logger.debug(f"Wycinanie obrazu bloku: x={position['x']}, y={position['y']}, w={position['width']}, h={position['height']}")
        try:
            x, y, w, h = position['x'], position['y'], position['width'], position['height']
            block_img = full_image.crop((x, y, x + w, y + h))
            self.logger.debug(f"Pomyślnie wycięto obszar o rozmiarze {block_img.size}")
            return block_img
        except Exception as e:
            self.logger.error(f"Błąd podczas wycinania obrazu bloku: {str(e)}", exc_info=True)
            raise

    def _image_to_base64(self, image: Image.Image) -> str:
        """Konwertuje obraz do formatu base64"""
        self.logger.debug("Konwersja obrazu do formatu base64")
        try:
            buffered = BytesIO()
            image.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            self.logger.debug(f"Wygenerowano ciąg base64 o długości {len(img_str)} znaków")
            return f"data:image/png;base64,{img_str}"
        except Exception as e:
            self.logger.error(f"Błąd podczas konwersji obrazu do base64: {str(e)}", exc_info=True)
            return ""

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
        self.logger = logging.getLogger('vhtml.document_analyzer')
        self.logger.info("Inicjalizacja DocumentAnalyzer")
        
        self.logger.debug("Inicjalizacja komponentów")
        self.pdf_processor = PDFProcessor()
        self.layout_analyzer = LayoutAnalyzer()
        self.ocr_engine = OCREngine()
        self.html_generator = HTMLGenerator()
        self.logger.info("Zainicjalizowano wszystkie komponenty")

    def analyze_document(self, pdf_path: str, output_dir: str = "output") -> str:
        """Analizuje dokument PDF i generuje HTML"""
        self.logger.info(f"Rozpoczynanie analizy dokumentu: {pdf_path}")
        self.logger.info(f"Katalog wyjściowy: {os.path.abspath(output_dir)}")
        
        try:
            # Konwertuj PDF na obrazy
            self.logger.info("Konwersja PDF na obrazy...")
            images = self.pdf_processor.pdf_to_images(pdf_path)
            if not images:
                self.logger.error("Nie udało się przekonwertować pliku PDF na obrazy")
                return None
            self.logger.info(f"Pomyślnie przekonwertowano {len(images)} stron")

            # Analizuj układ pierwszego obrazu
            self.logger.info("Analiza układu dokumentu...")
            layout_type, blocks = self.layout_analyzer.analyze_layout(images[0])
            self.logger.info(f"Zidentyfikowano układ: {layout_type} z {len(blocks)} blokami")

            # Przetwórz każdy blok przez OCR
            self.logger.info("Przetwarzanie bloków tekstu...")
            document_blocks = []
            for i, block in enumerate(blocks):
                self.logger.debug(f"Przetwarzanie bloku {i+1}/{len(blocks)}")
                
                # Ekstrakcja tekstu
                text, language, confidence = self.ocr_engine.extract_text_from_block(images[0], block['position'])
                self.logger.debug(f"Blok {i}: rozpoznano {len(text)} znaków (pewność: {confidence:.1f}%)")
                
                # Określ typ bloku
                block_type = self._classify_block_type(text, i, layout_type)
                self.logger.debug(f"Zidentyfikowano typ bloku: {block_type}")
                
                # Analizuj formatowanie
                formatting = self._analyze_formatting(text)
                
                # Utwórz obiekt bloku
                document_block = Block(
                    id=f"block_{i}",
                    type=block_type,
                    position=block['position'],
                    content=text,
                    language=language,
                    confidence=confidence,
                    formatting=formatting
                )
                document_blocks.append(document_block)
                
                if i > 0 and i % 10 == 0:  # Log co 10 bloków, aby nie zaśmiecać logów
                    self.logger.info(f"Przetworzono {i}/{len(blocks)} bloków")

            
            self.logger.info(f"Zakończono przetwarzanie {len(document_blocks)} bloków")

            # Określ język dokumentu
            self.logger.info("Określanie języka dokumentu...")
            language = self._determine_document_language(document_blocks)
            self.logger.info(f"Zidentyfikowano język dokumentu: {language}")
            
            # Określ typ dokumentu
            self.logger.info("Klasyfikacja typu dokumentu...")
            doc_type = self._classify_document_type(layout_type, document_blocks)
            self.logger.info(f"Zidentyfikowano typ dokumentu: {doc_type}")

            # Przygotuj metadane
            self.logger.info("Przygotowywanie metadanych...")
            avg_confidence = sum(b.confidence for b in document_blocks) / len(document_blocks) if document_blocks else 0
            metadata = DocumentMetadata(
                doc_type=doc_type,
                language=language,
                layout=layout_type,
                confidence=avg_confidence,
                blocks=document_blocks
            )
            self.logger.info(f"Średnia pewność OCR: {avg_confidence:.1f}%")

            # Wygeneruj HTML
            self.logger.info("Generowanie HTML...")
            html_content = self.html_generator.generate_html(metadata, images)
            
            # Utwórz katalog wyjściowy jeśli nie istnieje
            os.makedirs(output_dir, exist_ok=True)
            base_name = os.path.splitext(os.path.basename(pdf_path))[0]
            
            # Zapisz HTML
            html_path = os.path.join(output_dir, f"{base_name}.html")
            with open(html_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            self.logger.info(f"Zapisano plik HTML: {html_path}")
                
            # Zapisz metadane JSON
            metadata_path = os.path.join(output_dir, f"{base_name}_metadata.json")
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(asdict(metadata), f, ensure_ascii=False, indent=2)
            self.logger.info(f"Zapisano metadane: {metadata_path}")
                
            self.logger.info("Analiza dokumentu zakończona pomyślnie")
            return html_path, metadata_path
            
        except Exception as e:
            self.logger.error(f"Błąd podczas analizy dokumentu: {str(e)}", exc_info=True)
            raise

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
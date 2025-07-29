#!/usr/bin/env python3
"""
HTML Generator Module
Moduł do generowania HTML z rozpoznanego tekstu i metadanych
"""

import os
import json
import base64
from io import BytesIO
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from PIL import Image
from jinja2 import Template


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


@dataclass
class DocumentMetadata:
    """Metadane całego dokumentu"""
    doc_type: str  # invoice, form, letter, other
    language: str
    layout: str  # 4-block, 6-block, custom
    confidence: float
    blocks: List[Block]


class HTMLGenerator:
    """Generator HTML z metadanymi JSON"""

    def __init__(self, templates_dir: Optional[str] = None):
        """
        Inicjalizacja generatora HTML
        
        Args:
            templates_dir: Katalog z szablonami HTML (opcjonalny)
        """
        self.templates_dir = templates_dir
        self.base_template = self._get_base_template()
        self.template_map = {
            'invoice': self._get_invoice_template(),
            'form': self._get_form_template(),
            'universal': self._get_universal_template()
        }
    
    def generate_html(self, metadata: DocumentMetadata, images: List[Image.Image]) -> str:
        """
        Generuje HTML z metadanymi
        
        Args:
            metadata: Metadane dokumentu
            images: Lista obrazów stron dokumentu
            
        Returns:
            Wygenerowany kod HTML
        """
        # Wybierz odpowiedni szablon na podstawie typu dokumentu
        template_html = self.template_map.get(metadata.doc_type, self.template_map['universal'])
        template = Template(template_html)
        
        # Przygotuj dane dla szablonu
        template_data = {
            'metadata': asdict(metadata),
            'title': f"Document: {metadata.doc_type.capitalize()}",
            'blocks': []
        }
        
        # Przygotuj dane bloków
        for i, block in enumerate(metadata.blocks):
            block_data = asdict(block)
            
            # Jeśli mamy obrazy, dodaj obrazy bloków
            if images and i < len(images):
                block_image = self._extract_block_image(images[0], block.position)
                block_data['image_data'] = self._image_to_base64(block_image)
            
            template_data['blocks'].append(block_data)
        
        # Wygeneruj HTML
        html = template.render(**template_data)
        return html
    
    def save_html_with_metadata(self, html: str, metadata: DocumentMetadata, output_path: str) -> str:
        """
        Zapisuje HTML i metadane do plików
        
        Args:
            html: Wygenerowany kod HTML
            metadata: Metadane dokumentu
            output_path: Ścieżka do zapisu
            
        Returns:
            Ścieżka do zapisanego pliku HTML
        """
        # Utwórz katalog wyjściowy, jeśli nie istnieje
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Zapisz HTML
        html_path = output_path
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        # Zapisz metadane jako JSON
        json_path = f"{os.path.splitext(output_path)[0]}.json"
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(asdict(metadata), f, ensure_ascii=False, indent=2)
        
        return html_path
    
    def _extract_block_image(self, full_image: Image.Image, position: Dict) -> Image.Image:
        """
        Wycina obraz bloku z pełnego obrazu
        
        Args:
            full_image: Pełny obraz strony
            position: Pozycja bloku (x, y, width, height)
            
        Returns:
            Wycięty obraz bloku
        """
        x, y, width, height = position['x'], position['y'], position['width'], position['height']
        return full_image.crop((x, y, x + width, y + height))
    
    def _image_to_base64(self, image: Image.Image) -> str:
        """
        Konwertuje obraz do base64
        
        Args:
            image: Obraz do konwersji
            
        Returns:
            String base64 obrazu
        """
        buffer = BytesIO()
        image.save(buffer, format="PNG")
        return f"data:image/png;base64,{base64.b64encode(buffer.getvalue()).decode('utf-8')}"
    
    def _get_base_template(self) -> str:
        """
        Zwraca podstawowy szablon HTML
        
        Returns:
            Szablon HTML
        """
        return """<!DOCTYPE html>
<html lang="{{ metadata.language }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        .document-container {
            max-width: 1000px;
            margin: 0 auto;
            border: 1px solid #ddd;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .block {
            margin-bottom: 20px;
            padding: 15px;
            border: 1px solid #eee;
            border-radius: 5px;
        }
        .block-header {
            font-weight: bold;
            margin-bottom: 10px;
            color: #555;
        }
        .block-content {
            white-space: pre-wrap;
        }
        .metadata {
            background-color: #f9f9f9;
            padding: 10px;
            margin-top: 30px;
            border-top: 1px solid #ddd;
            font-size: 0.9em;
        }
        .block-image {
            max-width: 100%;
            margin-top: 10px;
            border: 1px solid #ddd;
        }
    </style>
</head>
<body>
    <div class="document-container">
        <h1>{{ title }}</h1>
        
        {% for block in blocks %}
        <div class="block">
            <div class="block-header">{{ block.type|capitalize }} ({{ block.id }})</div>
            <div class="block-content">{{ block.content }}</div>
            {% if block.image_data %}
            <img class="block-image" src="{{ block.image_data }}" alt="Block {{ block.id }}">
            {% endif %}
        </div>
        {% endfor %}
        
        <div class="metadata">
            <h3>Metadane dokumentu</h3>
            <p>Typ: {{ metadata.doc_type }}</p>
            <p>Język: {{ metadata.language }}</p>
            <p>Układ: {{ metadata.layout }}</p>
            <p>Pewność: {{ metadata.confidence }}</p>
        </div>
    </div>
</body>
</html>"""
    
    def _get_invoice_template(self) -> str:
        """
        Zwraca szablon HTML dla faktur
        
        Returns:
            Szablon HTML dla faktur
        """
        return """<!DOCTYPE html>
<html lang="{{ metadata.language }}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            line-height: 1.6;
            margin: 0;
            padding: 20px;
            color: #333;
        }
        .invoice-container {
            max-width: 1000px;
            margin: 0 auto;
            border: 1px solid #ddd;
            padding: 20px;
            box-shadow: 0 0 10px rgba(0,0,0,0.1);
        }
        .invoice-header {
            display: flex;
            justify-content: space-between;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 1px solid #ddd;
        }
        .invoice-details {
            margin-bottom: 30px;
        }
        .invoice-table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
        }
        .invoice-table th, .invoice-table td {
            padding: 10px;
            border: 1px solid #ddd;
            text-align: left;
        }
        .invoice-table th {
            background-color: #f5f5f5;
        }
        .invoice-summary {
            display: flex;
            justify-content: flex-end;
            margin-bottom: 30px;
        }
        .invoice-summary-table {
            width: 300px;
            border-collapse: collapse;
        }
        .invoice-summary-table th, .invoice-summary-table td {
            padding: 10px;
            border: 1px solid #ddd;
        }
        .invoice-footer {
            margin-top: 50px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="invoice-container">
        <div class="invoice-header">
            <div>
                <h1>FAKTURA</h1>
                {% for block in blocks %}
                    {% if block.type == 'header' %}
                        <div>{{ block.content }}</div>
                    {% endif %}
                {% endfor %}
            </div>
        </div>
        
        <div class="invoice-details">
            {% for block in blocks %}
                {% if block.type == 'details' %}
                    <div>{{ block.content }}</div>
                {% endif %}
            {% endfor %}
        </div>
        
        <table class="invoice-table">
            <thead>
                <tr>
                    <th>Lp.</th>
                    <th>Nazwa towaru/usługi</th>
                    <th>Ilość</th>
                    <th>Cena netto</th>
                    <th>Wartość netto</th>
                    <th>VAT</th>
                    <th>Wartość brutto</th>
                </tr>
            </thead>
            <tbody>
                {% for block in blocks %}
                    {% if block.type == 'table' %}
                        <tr>
                            <td colspan="7">{{ block.content }}</td>
                        </tr>
                    {% endif %}
                {% endfor %}
            </tbody>
        </table>
        
        <div class="invoice-summary">
            <table class="invoice-summary-table">
                <tr>
                    <th>Suma netto</th>
                    <td>
                        {% for block in blocks %}
                            {% if block.type == 'summary' and 'netto' in block.content.lower() %}
                                {{ block.content }}
                            {% endif %}
                        {% endfor %}
                    </td>
                </tr>
                <tr>
                    <th>VAT</th>
                    <td>
                        {% for block in blocks %}
                            {% if block.type == 'summary' and 'vat' in block.content.lower() %}
                                {{ block.content }}
                            {% endif %}
                        {% endfor %}
                    </td>
                </tr>
                <tr>
                    <th>Suma brutto</th>
                    <td>
                        {% for block in blocks %}
                            {% if block.type == 'summary' and 'brutto' in block.content.lower() %}
                                {{ block.content }}
                            {% endif %}
                        {% endfor %}
                    </td>
                </tr>
            </table>
        </div>
        
        <div class="invoice-footer">
            {% for block in blocks %}
                {% if block.type == 'footer' %}
                    <div>{{ block.content }}</div>
                {% endif %}
            {% endfor %}
        </div>
    </div>
</body>
</html>"""
    
    def _get_form_template(self) -> str:
        """
        Zwraca szablon HTML dla formularzy
        
        Returns:
            Szablon HTML dla formularzy
        """
        # Uproszczony szablon dla formularzy
        return self._get_base_template()
    
    def _get_universal_template(self) -> str:
        """
        Zwraca uniwersalny szablon HTML
        
        Returns:
            Uniwersalny szablon HTML
        """
        return self._get_base_template()


if __name__ == "__main__":
    # Przykład użycia
    import sys
    
    # Przykładowe dane
    blocks = [
        Block(
            id="block1",
            type="header",
            position={"x": 10, "y": 10, "width": 500, "height": 100},
            content="Przykładowy dokument",
            language="pl",
            confidence=0.95,
            formatting={"bold": True, "font_size": 16}
        ),
        Block(
            id="block2",
            type="content",
            position={"x": 10, "y": 120, "width": 500, "height": 300},
            content="To jest przykładowa treść dokumentu wygenerowana przez system vHTML.",
            language="pl",
            confidence=0.9,
            formatting={"bold": False, "font_size": 12}
        )
    ]
    
    metadata = DocumentMetadata(
        doc_type="universal",
        language="pl",
        layout="custom",
        confidence=0.92,
        blocks=blocks
    )
    
    generator = HTMLGenerator()
    html = generator.generate_html(metadata, [])
    
    output_path = "example_output.html"
    generator.save_html_with_metadata(html, metadata, output_path)
    
    print(f"Wygenerowano przykładowy HTML: {output_path}")
    print(f"Wygenerowano metadane JSON: {os.path.splitext(output_path)[0]}.json")

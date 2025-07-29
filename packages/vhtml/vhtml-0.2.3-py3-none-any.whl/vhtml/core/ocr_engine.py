#!/usr/bin/env python3
"""
OCR Engine Module
Moduł do rozpoznawania tekstu z obrazów z obsługą wielu języków
"""

import os
import numpy as np
import pytesseract
from PIL import Image
import easyocr
from langdetect import detect, LangDetectException
from typing import Dict, Tuple, List, Optional, Union


class OCREngine:
    """Silnik OCR z rozpoznawaniem języka"""

    def __init__(self, use_easyocr: bool = False):
        """
        Inicjalizacja silnika OCR
        
        Args:
            use_easyocr: Czy używać EasyOCR zamiast Tesseract
        """
        self.use_easyocr = use_easyocr
        self.languages = {
            'pl': 'pol',
            'en': 'eng',
            'de': 'deu'
        }
        
        # Inicjalizacja EasyOCR jeśli wymagane
        if self.use_easyocr:
            try:
                self.reader = easyocr.Reader(['en', 'pl', 'de'])
            except Exception as e:
                print(f"Nie można zainicjalizować EasyOCR: {e}")
                self.use_easyocr = False
    
    def extract_text_from_block(self, image: Image.Image, block_position: Dict) -> Tuple[str, str, float]:
        """
        Wyciąga tekst z bloku obrazu
        
        Args:
            image: Obraz źródłowy
            block_position: Pozycja bloku (x, y, width, height)
            
        Returns:
            Tuple zawierający (tekst, język, pewność)
        """
        # Wytnij blok z obrazu
        x, y, width, height = block_position['x'], block_position['y'], block_position['width'], block_position['height']
        block_image = image.crop((x, y, x + width, y + height))
        
        # Rozpoznaj tekst
        if self.use_easyocr:
            text = self._extract_with_easyocr(block_image)
        else:
            text = self._extract_with_tesseract(block_image)
        
        # Wykryj język tekstu
        language = self._detect_language(text)
        
        # Oblicz pewność OCR
        confidence = self._calculate_ocr_confidence(block_image, text)
        
        return text, language, confidence
    
    def _extract_with_tesseract(self, image: Image.Image) -> str:
        """
        Ekstrakcja tekstu z Tesseract
        
        Args:
            image: Obraz do przetworzenia
            
        Returns:
            Rozpoznany tekst
        """
        try:
            # Użyj wszystkich wspieranych języków
            langs = '+'.join(self.languages.values())
            text = pytesseract.image_to_string(image, lang=langs)
            return text.strip()
        except Exception as e:
            print(f"Błąd Tesseract OCR: {e}")
            return ""
    
    def _extract_with_easyocr(self, image: Image.Image) -> str:
        """
        Ekstrakcja tekstu z EasyOCR
        
        Args:
            image: Obraz do przetworzenia
            
        Returns:
            Rozpoznany tekst
        """
        try:
            # Konwersja do formatu numpy
            img_array = np.array(image)
            
            # Rozpoznawanie tekstu
            results = self.reader.readtext(img_array)
            
            # Połącz wyniki
            text = ' '.join([result[1] for result in results])
            return text.strip()
        except Exception as e:
            print(f"Błąd EasyOCR: {e}")
            return ""
    
    def _detect_language(self, text: str) -> str:
        """
        Rozpoznaje język tekstu
        
        Args:
            text: Tekst do analizy
            
        Returns:
            Kod języka (pl, en, de)
        """
        if not text or len(text) < 10:
            return "unknown"
        
        try:
            lang = detect(text)
            # Jeśli język jest wspierany, zwróć go
            if lang in self.languages:
                return lang
            return "unknown"
        except LangDetectException:
            return "unknown"
    
    def _calculate_ocr_confidence(self, image: Image.Image, text: str) -> float:
        """
        Oblicza pewność OCR
        
        Args:
            image: Obraz źródłowy
            text: Rozpoznany tekst
            
        Returns:
            Wartość pewności (0.0-1.0)
        """
        if not text:
            return 0.0
        
        try:
            # Użyj Tesseract do uzyskania danych o pewności
            data = pytesseract.image_to_data(image, output_type=pytesseract.Output.DICT)
            
            # Oblicz średnią pewność
            if 'conf' in data and len(data['conf']) > 0:
                # Filtruj wartości -1 (brak pewności)
                confidences = [conf for conf in data['conf'] if conf != -1]
                if confidences:
                    avg_confidence = sum(confidences) / len(confidences)
                    return avg_confidence / 100.0  # Normalizacja do zakresu 0-1
            
            # Fallback - szacowanie na podstawie długości tekstu
            return min(len(text) / 100.0, 0.95)
        
        except Exception as e:
            print(f"Błąd obliczania pewności: {e}")
            # Fallback - szacowanie na podstawie długości tekstu
            return min(len(text) / 200.0, 0.8)


if __name__ == "__main__":
    # Przykład użycia
    import sys
    
    if len(sys.argv) < 2:
        print("Użycie: python ocr_engine.py <ścieżka_do_obrazu>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    
    if not os.path.exists(image_path):
        print(f"Plik nie istnieje: {image_path}")
        sys.exit(1)
    
    try:
        image = Image.open(image_path)
        
        # Testuj OCR na całym obrazie
        ocr = OCREngine()
        
        # Symuluj blok jako cały obraz
        block_position = {
            'x': 0,
            'y': 0,
            'width': image.width,
            'height': image.height
        }
        
        text, language, confidence = ocr.extract_text_from_block(image, block_position)
        
        print(f"Rozpoznany tekst ({language}, pewność: {confidence:.2f}):")
        print("-" * 50)
        print(text)
        print("-" * 50)
        
    except Exception as e:
        print(f"Błąd: {e}")

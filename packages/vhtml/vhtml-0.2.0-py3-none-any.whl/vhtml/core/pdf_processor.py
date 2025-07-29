#!/usr/bin/env python3
"""
PDF Processor Module
Moduł do konwersji dokumentów PDF do obrazów i wstępnego przetwarzania
"""

import os
from typing import List, Optional, Tuple
import numpy as np
import cv2
from pdf2image import convert_from_path
from PIL import Image
import fitz  # PyMuPDF


class PDFProcessor:
    """Procesor PDF do konwersji na obrazy i wstępnego przetwarzania"""

    def __init__(self, dpi: int = 300):
        """
        Inicjalizacja procesora PDF
        
        Args:
            dpi: Rozdzielczość konwersji PDF do obrazu
        """
        self.dpi = dpi
    
    def pdf_to_images(self, pdf_path: str) -> List[Image.Image]:
        """
        Konwertuje PDF do listy obrazów
        
        Args:
            pdf_path: Ścieżka do pliku PDF
            
        Returns:
            Lista obrazów stron PDF
        """
        try:
            images = convert_from_path(pdf_path, dpi=self.dpi)
            return images
        except Exception as e:
            print(f"Błąd konwersji PDF: {e}")
            return []
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Wstępne przetwarzanie obrazu (denoise, deskew)
        
        Args:
            image: Obraz do przetworzenia
            
        Returns:
            Przetworzony obraz
        """
        # Konwersja do OpenCV
        cv_image = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
        
        # Konwersja do skali szarości
        gray = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)
        
        # Redukcja szumów
        denoised = cv2.fastNlMeansDenoising(gray, None, 10, 7, 21)
        
        # Korekcja przekrzywienia (deskew)
        corrected = self._deskew(denoised)
        
        # Konwersja z powrotem do PIL Image
        pil_image = Image.fromarray(corrected)
        return pil_image
    
    def _deskew(self, image: np.ndarray) -> np.ndarray:
        """
        Korekcja przekrzywienia dokumentu
        
        Args:
            image: Obraz w formacie numpy array
            
        Returns:
            Skorygowany obraz
        """
        # Wykrywanie krawędzi
        edges = cv2.Canny(image, 50, 150, apertureSize=3)
        
        # Wykrywanie linii
        lines = cv2.HoughLinesP(edges, 1, np.pi/180, 100, minLineLength=100, maxLineGap=10)
        
        # Jeśli nie wykryto linii, zwróć oryginalny obraz
        if lines is None:
            return image
        
        # Obliczanie kąta przekrzywienia
        angles = []
        for line in lines:
            x1, y1, x2, y2 = line[0]
            if x2 - x1 != 0:  # Unikanie dzielenia przez zero
                angle = np.arctan((y2 - y1) / (x2 - x1)) * 180 / np.pi
                angles.append(angle)
        
        if not angles:
            return image
        
        # Mediana kątów jako najlepsze przybliżenie
        median_angle = np.median(angles)
        
        # Korekcja tylko jeśli kąt jest znaczący
        if abs(median_angle) < 0.5:
            return image
        
        # Rotacja obrazu
        (h, w) = image.shape[:2]
        center = (w // 2, h // 2)
        M = cv2.getRotationMatrix2D(center, median_angle, 1.0)
        rotated = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
        
        return rotated
    
    def extract_text_with_pymupdf(self, pdf_path: str) -> List[str]:
        """
        Alternatywna metoda ekstrakcji tekstu z PDF używając PyMuPDF
        
        Args:
            pdf_path: Ścieżka do pliku PDF
            
        Returns:
            Lista tekstów ze stron PDF
        """
        try:
            doc = fitz.open(pdf_path)
            texts = []
            
            for page in doc:
                text = page.get_text()
                texts.append(text)
            
            return texts
        except Exception as e:
            print(f"Błąd ekstrakcji tekstu PyMuPDF: {e}")
            return []


if __name__ == "__main__":
    # Przykład użycia
    import sys
    
    if len(sys.argv) < 2:
        print("Użycie: python pdf_processor.py <ścieżka_do_pdf>")
        sys.exit(1)
    
    pdf_path = sys.argv[1]
    
    if not os.path.exists(pdf_path):
        print(f"Plik nie istnieje: {pdf_path}")
        sys.exit(1)
    
    processor = PDFProcessor()
    images = processor.pdf_to_images(pdf_path)
    
    print(f"Przekonwertowano {len(images)} stron")
    
    if images:
        # Zapisz pierwszą stronę jako przykład
        processed = processor.preprocess_image(images[0])
        processed.save("processed_page.png")
        print("Zapisano przetworzoną pierwszą stronę jako processed_page.png")

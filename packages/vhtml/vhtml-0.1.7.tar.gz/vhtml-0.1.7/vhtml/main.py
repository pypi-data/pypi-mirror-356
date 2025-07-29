#!/usr/bin/env python3
"""
vHTML - Optical HTML Generator
Główny moduł systemu do konwersji dokumentów do HTML z wykorzystaniem OCR
"""

import os
import sys
import argparse
from typing import List, Dict, Optional
import webbrowser
from pathlib import Path

from vhtml.core.pdf_processor import PDFProcessor
from vhtml.core.layout_analyzer import LayoutAnalyzer, Block, DocumentMetadata
from vhtml.core.ocr_engine import OCREngine
from vhtml.core.html_generator import HTMLGenerator


class DocumentAnalyzer:
    """Główna klasa systemu analizy dokumentów"""

    def __init__(self):
        """Inicjalizacja komponentów systemu"""
        self.pdf_processor = PDFProcessor()
        self.layout_analyzer = LayoutAnalyzer()
        self.ocr_engine = OCREngine()
        self.html_generator = HTMLGenerator()
    
    def analyze_document(self, pdf_path: str, output_dir: str = "output") -> str:
        """
        Analizuje dokument PDF i generuje HTML
        
        Args:
            pdf_path: Ścieżka do pliku PDF
            output_dir: Katalog wyjściowy
            
        Returns:
            Ścieżka do wygenerowanego pliku HTML
        """
        print(f"Analizuję dokument: {pdf_path}")
        
        # Krok 1: Konwersja PDF do obrazów
        print("1. Konwersja PDF do obrazów...")
        images = self.pdf_processor.pdf_to_images(pdf_path)
        if not images:
            raise ValueError("Nie udało się przekonwertować PDF do obrazów")
        
        print(f"   Przekonwertowano {len(images)} stron")
        
        # Krok 2: Przetwarzanie wstępne obrazów
        print("2. Przetwarzanie wstępne obrazów...")
        processed_images = [self.pdf_processor.preprocess_image(img) for img in images]
        
        # Krok 3: Analiza układu i segmentacja bloków
        print("3. Analiza układu dokumentu...")
        layout_type, blocks = self.layout_analyzer.analyze_layout(processed_images[0])
        print(f"   Wykryto układ: {layout_type}")
        print(f"   Znaleziono {len(blocks)} bloków")
        
        # Krok 4: OCR i analiza tekstu
        print("4. Rozpoznawanie tekstu (OCR)...")
        document_blocks = []
        
        for i, block in enumerate(blocks):
            print(f"   Przetwarzanie bloku {i+1}/{len(blocks)}...")
            text, language, confidence = self.ocr_engine.extract_text_from_block(
                processed_images[0], block['position']
            )
            
            # Klasyfikacja typu bloku
            block_type = self._classify_block_type(text, i, layout_type)
            
            # Analiza formatowania
            formatting = self._analyze_formatting(text)
            
            # Tworzenie obiektu bloku
            document_blocks.append(Block(
                id=f"block_{i+1}",
                type=block_type,
                position=block['position'],
                content=text,
                language=language,
                confidence=confidence,
                formatting=formatting
            ))
        
        # Krok 5: Określenie metadanych dokumentu
        print("5. Generowanie metadanych...")
        doc_language = self._determine_document_language(document_blocks)
        doc_type = self._classify_document_type(layout_type, document_blocks)
        
        # Obliczenie średniej pewności
        avg_confidence = sum(block.confidence for block in document_blocks) / len(document_blocks) if document_blocks else 0
        
        metadata = DocumentMetadata(
            doc_type=doc_type,
            language=doc_language,
            layout=layout_type,
            confidence=avg_confidence,
            blocks=document_blocks
        )
        
        # Krok 6: Generowanie HTML
        print("6. Generowanie HTML...")
        html = self.html_generator.generate_html(metadata, processed_images)
        
        # Krok 7: Zapisywanie wyników
        print("7. Zapisywanie wyników...")
        output_filename = os.path.basename(pdf_path).replace('.pdf', '.html')
        output_path = os.path.join(output_dir, output_filename)
        
        # Upewnij się, że katalog wyjściowy istnieje
        os.makedirs(output_dir, exist_ok=True)
        
        html_path = self.html_generator.save_html_with_metadata(html, metadata, output_path)
        print(f"   HTML zapisany: {html_path}")
        
        return html_path
    
    def _classify_block_type(self, text: str, block_index: int, layout_type: str) -> str:
        """
        Klasyfikuje typ bloku na podstawie zawartości
        
        Args:
            text: Tekst bloku
            block_index: Indeks bloku
            layout_type: Typ układu dokumentu
            
        Returns:
            Typ bloku (header, content, table, footer, etc.)
        """
        # Prosta heurystyka klasyfikacji
        text_lower = text.lower()
        
        if block_index == 0:
            return "header"
        elif "faktura" in text_lower or "invoice" in text_lower:
            return "header"
        elif "tabela" in text_lower or "table" in text_lower or any(x in text_lower for x in ["lp.", "suma", "razem", "total"]):
            return "table"
        elif block_index == len(text) - 1 or any(x in text_lower for x in ["stopka", "footer", "kontakt", "contact"]):
            return "footer"
        elif any(x in text_lower for x in ["netto", "brutto", "vat", "suma", "total"]):
            return "summary"
        elif any(x in text_lower for x in ["nabywca", "sprzedawca", "buyer", "seller", "customer"]):
            return "details"
        else:
            return "content"
    
    def _analyze_formatting(self, text: str) -> Dict:
        """
        Analizuje formatowanie tekstu
        
        Args:
            text: Tekst do analizy
            
        Returns:
            Słownik z informacjami o formatowaniu
        """
        # Prosta analiza formatowania
        formatting = {
            "bold": False,
            "italic": False,
            "font_size": 12,
            "alignment": "left"
        }
        
        # Wykrywanie pogrubienia (wszystkie wielkie litery)
        if text.isupper() and len(text) > 3:
            formatting["bold"] = True
        
        # Wykrywanie kursywy (na podstawie heurystyki)
        if text.startswith("*") and text.endswith("*"):
            formatting["italic"] = True
        
        # Szacowanie rozmiaru czcionki na podstawie długości linii
        lines = text.split("\n")
        if lines and max(len(line) for line in lines) < 30:
            formatting["font_size"] = 16
        
        return formatting
    
    def _determine_document_language(self, blocks: List[Block]) -> str:
        """
        Określa główny język dokumentu
        
        Args:
            blocks: Lista bloków dokumentu
            
        Returns:
            Kod języka (pl, en, de)
        """
        # Zliczanie języków w blokach
        lang_counts = {}
        
        for block in blocks:
            if block.language != "unknown":
                lang_counts[block.language] = lang_counts.get(block.language, 0) + 1
        
        # Wybierz najczęściej występujący język
        if lang_counts:
            return max(lang_counts, key=lang_counts.get)
        return "unknown"
    
    def _classify_document_type(self, layout_type: str, blocks: List[Block]) -> str:
        """
        Klasyfikuje typ dokumentu
        
        Args:
            layout_type: Typ układu dokumentu
            blocks: Lista bloków dokumentu
            
        Returns:
            Typ dokumentu (invoice, form, letter, other)
        """
        # Prosta klasyfikacja na podstawie zawartości
        text_content = " ".join([block.content.lower() for block in blocks])
        
        if any(x in text_content for x in ["faktura", "invoice", "rachunek", "vat", "netto", "brutto"]):
            return "invoice"
        elif any(x in text_content for x in ["formularz", "form", "wniosek", "application"]):
            return "form"
        elif any(x in text_content for x in ["list", "letter", "pismo", "korespondencja", "correspondence"]):
            return "letter"
        else:
            return "universal"


class AdvancedAnalyzer(DocumentAnalyzer):
    """Rozszerzona wersja analizatora z dodatkowymi funkcjami"""
    
    def __init__(self):
        super().__init__()
        self.statistics = {}
    
    def batch_analyze(self, pdf_directory: str, output_directory: str = "batch_output") -> Dict:
        """Analizuje wiele plików PDF w folderze"""
        results = {}
        pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
        
        print(f"Znaleziono {len(pdf_files)} plików PDF do analizy")
        
        for pdf_file in pdf_files:
            pdf_path = os.path.join(pdf_directory, pdf_file)
            try:
                print(f"\nAnalizuję: {pdf_file}")
                html_path = self.analyze_document(pdf_path, 
                    os.path.join(output_directory, pdf_file.replace('.pdf', '')))
                results[pdf_file] = {
                    'status': 'success',
                    'html_path': html_path
                }
            except Exception as e:
                results[pdf_file] = {
                    'status': 'error',
                    'error': str(e)
                }
                print(f"Błąd w {pdf_file}: {e}")
        
        return results


def process_document(file_path: str, output_format: str = "html", output_dir: str = "output") -> str:
    """
    Główna funkcja do przetwarzania dokumentu
    
    Args:
        file_path: Ścieżka do pliku
        output_format: Format wyjściowy (html, json)
        output_dir: Katalog wyjściowy
        
    Returns:
        Ścieżka do wygenerowanego pliku
    """
    analyzer = DocumentAnalyzer()
    return analyzer.analyze_document(file_path, output_dir)


def main():
    """Główna funkcja programu"""
    parser = argparse.ArgumentParser(description="vHTML - Optical HTML Generator")
    parser.add_argument("input", help="Ścieżka do pliku PDF lub katalogu z plikami PDF")
    parser.add_argument("-o", "--output", help="Katalog wyjściowy", default="output")
    parser.add_argument("-b", "--batch", help="Tryb wsadowy (przetwarzanie katalogu)", action="store_true")
    parser.add_argument("-v", "--view", help="Otwórz wygenerowany HTML w przeglądarce", action="store_true")
    
    args = parser.parse_args()
    
    try:
        if args.batch:
            if not os.path.isdir(args.input):
                print(f"Błąd: {args.input} nie jest katalogiem")
                sys.exit(1)
            
            analyzer = AdvancedAnalyzer()
            results = analyzer.batch_analyze(args.input, args.output)
            
            print("\n--- Podsumowanie ---")
            success = sum(1 for r in results.values() if r['status'] == 'success')
            print(f"Przetworzono {len(results)} plików: {success} sukcesów, {len(results) - success} błędów")
            
        else:
            if not os.path.isfile(args.input):
                print(f"Błąd: {args.input} nie jest plikiem")
                sys.exit(1)
            
            analyzer = DocumentAnalyzer()
            html_path = analyzer.analyze_document(args.input, args.output)
            
            print(f"\n✅ Sukces! HTML wygenerowany: {html_path}")
            
            if args.view:
                webbrowser.open(f'file://{os.path.abspath(html_path)}')
    
    except Exception as e:
        print(f"\n❌ Błąd: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
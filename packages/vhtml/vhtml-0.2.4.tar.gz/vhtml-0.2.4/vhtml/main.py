#!/usr/bin/env python3
"""
vHTML - Optical HTML Generator
Główny moduł systemu do konwersji dokumentów do HTML z wykorzystaniem OCR
"""

import os
import sys
import argparse
import json
from typing import List, Dict, Optional, Tuple, Any
import webbrowser
from pathlib import Path
from datetime import datetime

from vhtml.core.pdf_processor import PDFProcessor
from vhtml.core.layout_analyzer import LayoutAnalyzer, Block, DocumentMetadata
from vhtml.core.ocr_engine import OCREngine
from vhtml.core.html_generator import HTMLGenerator
from vhtml.utils.logging_utils import logger as vhtml_logger


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
        # Set up document-specific logger
        doc_logger = vhtml_logger.get_document_logger(pdf_path, output_dir)
        doc_logger.info(f"Starting document analysis: {os.path.basename(pdf_path)}")
        doc_logger.info(f"Output directory: {output_dir}")
        
        start_time = datetime.now()
        processing_steps = {}
        
        try:
            # Krok 1: Konwersja PDF do obrazów
            doc_logger.info("1. Converting PDF to images...")
            step_start = datetime.now()
            images = self.pdf_processor.pdf_to_images(pdf_path)
            if not images:
                raise ValueError("Failed to convert PDF to images")
            
            processing_steps['pdf_conversion'] = {
                'status': 'success',
                'pages': len(images),
                'duration_seconds': (datetime.now() - step_start).total_seconds()
            }
            doc_logger.info(f"Converted {len(images)} pages")
            
            # Krok 2: Przetwarzanie wstępne obrazów
            doc_logger.info("2. Preprocessing images...")
            step_start = datetime.now()
            processed_images = [self.pdf_processor.preprocess_image(img) for img in images]
            processing_steps['image_preprocessing'] = {
                'status': 'success',
                'duration_seconds': (datetime.now() - step_start).total_seconds()
            }
            
            # Krok 3: Analiza układu i segmentacja bloków
            doc_logger.info("3. Analyzing document layout...")
            step_start = datetime.now()
            layout_type, blocks = self.layout_analyzer.analyze_layout(processed_images[0])
            processing_steps['layout_analysis'] = {
                'status': 'success',
                'layout_type': layout_type,
                'blocks_found': len(blocks),
                'duration_seconds': (datetime.now() - step_start).total_seconds()
            }
            doc_logger.info(f"Detected layout: {layout_type} with {len(blocks)} blocks")
        
            # Krok 4: OCR i analiza tekstu
            doc_logger.info("4. Performing OCR and text analysis...")
            step_start = datetime.now()
            document_blocks = []
            ocr_stats = {
                'total_blocks': len(blocks),
                'languages': {},
                'confidence_scores': []
            }
            
            for i, block in enumerate(blocks):
                block_start = datetime.now()
                block_log = f"Processing block {i+1}/{len(blocks)}"
                doc_logger.info(f"{block_log}...")
                
                try:
                    # Extract text from block using OCR
                    text, language, confidence = self.ocr_engine.extract_text_from_block(
                        processed_images[0], block['position']
                    )
                    
                    # Update OCR statistics
                    ocr_stats['confidence_scores'].append(confidence)
                    if language in ocr_stats['languages']:
                        ocr_stats['languages'][language] += 1
                    else:
                        ocr_stats['languages'][language] = 1
                    
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
                    
                    block_time = (datetime.now() - block_start).total_seconds()
                    doc_logger.debug(f"{block_log} completed in {block_time:.2f}s (confidence: {confidence:.2f})")
                    
                except Exception as e:
                    doc_logger.error(f"Error processing block {i+1}: {str(e)}", exc_info=True)
                    raise
            
            processing_steps['ocr_processing'] = {
                'status': 'success',
                'blocks_processed': len(document_blocks),
                'languages_detected': ocr_stats['languages'],
                'avg_confidence': sum(ocr_stats['confidence_scores']) / len(ocr_stats['confidence_scores']) if ocr_stats['confidence_scores'] else 0,
                'duration_seconds': (datetime.now() - step_start).total_seconds()
            }
            
            # Krok 5: Określenie metadanych dokumentu
            doc_logger.info("5. Generating document metadata...")
            step_start = datetime.now()
            
            doc_language = self._determine_document_language(document_blocks)
            doc_type = self._classify_document_type(layout_type, document_blocks)
            
            # Calculate average confidence
            avg_confidence = sum(block.confidence for block in document_blocks) / len(document_blocks) if document_blocks else 0
            
            # Create pages structure
            pages = [{
                'number': i+1,
                'blocks': [block.to_dict() for block in document_blocks]
            } for i in range(len(images))]
            
            metadata = DocumentMetadata(
                doc_type=doc_type,
                language=doc_language,
                layout=layout_type,
                confidence=avg_confidence,
                pages=pages,
                source_file=os.path.basename(pdf_path),
                processing_time=0,  # Will be updated after processing
                blocks=document_blocks  # Pass the blocks directly
            )
            
            processing_steps['metadata_generation'] = {
                'status': 'success',
                'document_type': doc_type,
                'detected_language': doc_language,
                'duration_seconds': (datetime.now() - step_start).total_seconds()
            }
            
            # Krok 6: Generowanie HTML
            doc_logger.info("6. Generating HTML output...")
            step_start = datetime.now()
            
            html_content = self.html_generator.generate_html(metadata, processed_images)
            
            processing_steps['html_generation'] = {
                'status': 'success',
                'duration_seconds': (datetime.now() - step_start).total_seconds()
            }
            
            # Krok 7: Zapis wyników
            doc_logger.info("7. Saving results...")
            step_start = datetime.now()
            
            # Create output directory with document name as subdirectory
            doc_name = os.path.splitext(os.path.basename(pdf_path))[0]
            doc_output_dir = os.path.join(output_dir, doc_name)
            os.makedirs(doc_output_dir, exist_ok=True)
            
            # Save HTML
            output_filename = f"{doc_name}.html"
            output_path = os.path.join(doc_output_dir, output_filename)
            
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Save metadata
            metadata_path = os.path.join(doc_output_dir, f"{doc_name}_metadata.json")
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata.to_dict(), f, indent=2, ensure_ascii=False)
            
            # Calculate total processing time
            total_time = (datetime.now() - start_time).total_seconds()
            
            # Update metadata with processing time
            metadata.processing_time = total_time
            
            # Save updated metadata
            with open(metadata_path, 'w', encoding='utf-8') as f:
                json.dump(metadata.to_dict(), f, indent=2, ensure_ascii=False)
            
            # Save processing log
            log_data = {
                'document': os.path.basename(pdf_path),
                'processing_date': datetime.now().isoformat(),
                'processing_time_seconds': total_time,
                'steps': processing_steps,
                'output_files': {
                    'html': output_path,
                    'metadata': metadata_path,
                    'log': doc_logger.handlers[0].baseFilename if doc_logger.handlers else None
                }
            }
            
            log_path = os.path.join(doc_output_dir, f"{doc_name}_processing_log.json")
            with open(log_path, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, default=str)
            
            doc_logger.info(f"HTML saved to: {output_path}")
            doc_logger.info(f"Metadata saved to: {metadata_path}")
            doc_logger.info(f"Processing log saved to: {log_path}")
            doc_logger.info(f"Total processing time: {total_time:.2f} seconds")
            
            return output_path
            
        except Exception as e:
            doc_logger.error(f"Error processing document: {str(e)}", exc_info=True)
            raise
    
    def _classify_block_type(self, text: str, block_index: int, layout_type: str) -> str:
        """
        Klasyfikuje typ bloku na podstawie zawartości i kontekstu
        
        Args:
            text: Zawartość tekstowa bloku
            block_index: Indeks bloku w dokumencie
            layout_type: Typ układu dokumentu
            
        Returns:
            Zidentyfikowany typ bloku (header, date, invoice_number, seller, buyer, amount, content)
        """
        if not text.strip():
            return "empty"
            
        text = text.strip().lower()
        
        # Proste heurystyki do klasyfikacji bloków
        if block_index == 0 and len(text) < 200 and '\n' not in text:
            return "header"
        
        # Check for date patterns
        date_keywords = ["data", "data wystawienia", "data sprzedaży", "data zakupu", "data operacji"]
        if any(keyword in text for keyword in date_keywords):
            return "date"
            
        # Check for invoice/order number patterns
        invoice_keywords = ["nr faktury", "numer faktury", "nr zamówienia", "numer dokumentu"]
        if any(keyword in text for keyword in invoice_keywords):
            return "invoice_number"
            
        # Check for seller information
        seller_keywords = ["sprzedawca", "sprzedawcy", "sprzedawcą", "sprzedawca:", "sprzedawcy:"]
        if any(keyword in text for keyword in seller_keywords):
            return "seller"
            
        # Check for buyer information
        buyer_keywords = ["nabywca", "nabywcy", "nabywcą", "nabywca:", "nabywcy:", "odbiorca", "odbiorcy"]
        if any(keyword in text for keyword in buyer_keywords):
            return "buyer"
            
        # Check for amount/total information
        amount_keywords = ["kwota", "wartość", "do zapłaty", "razem", "suma", "płatność", "płatności"]
        if any(keyword in text for keyword in amount_keywords):
            return "amount"
            
        # Check for currency patterns
        currency_indicators = ["zł", "pln", "$", "eur", "usd", "€", "gbp", "chf"]
        if (any(char.isdigit() for char in text) and 
            any(sep in text for sep in [",", "."]) and 
            any(currency in text for currency in currency_indicators)):
            return "amount"
            
        # Check for table rows
        if '\n' in text and text.count('\n') >= 2:
            lines = text.split('\n')
            if all('\t' in line or '  ' in line for line in lines[:3]):
                return "table"
            
        # Check for footer content
        if block_index > 10 and len(text) < 100 and '\n' not in text:
            return "footer"
            
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
    parser.add_argument("--extractor-service", choices=["invoice", "receipt", "cv", "contract", "financial", "medical", "legal", "tax", "insurance", "education"], help="Zewnętrzna usługa ekstrakcji danych z dokumentu (np. invoice, receipt)")
    parser.add_argument("--adapter", choices=["invoice", "receipt", "cv", "contract", "financial", "medical", "legal", "tax", "insurance", "education"], help="Użyj adaptera do bezpośredniego połączenia z usługą (pomija gateway)")
    parser.add_argument("--adapter-port", type=int, help="Port usługi adaptera (np. 8001 dla invoice, 8002 dla receipt)")
    parser.add_argument("--format", choices=["html", "mhtml"], default="html", help="Format wyjściowy: html (jeden plik) lub mhtml (multipart)")
    parser.add_argument("--docker", help="Ścieżka do docker-compose.yml lub katalogu z docker-compose.yml; uruchomi automatycznie wymagane usługi w Dockerze", nargs="?", const=".")
    parser.add_argument("--dockerfile", help="Ścieżka do Dockerfile konkretnej usługi; uruchomi pojedynczy kontener dla tej usługi", nargs="?")
    args = parser.parse_args()
    
    try:
        # Automatyczne uruchomienie docker-compose jeśli podano --docker
        if args.docker:
            import subprocess
            import time
            import os
            docker_dir = args.docker if os.path.isdir(args.docker) else os.path.dirname(args.docker)
            print(f"[vhtml] Uruchamiam docker-compose w katalogu: {docker_dir}")
            subprocess.run(["docker-compose", "up", "-d"], cwd=docker_dir, check=True)
            print("[vhtml] Czekam na uruchomienie usług (10s)...")
            time.sleep(10)
        # Uruchomienie pojedynczego kontenera jeśli podano --dockerfile
        elif args.dockerfile:
            import subprocess
            import time
            import os
            dockerfile_path = args.dockerfile
            service_name = os.path.basename(os.path.dirname(dockerfile_path))
            image_tag = f"{service_name}:local"
            build_dir = os.path.dirname(dockerfile_path)
            print(f"[vhtml] Buduję obraz Dockera: {image_tag} z {dockerfile_path}")
            subprocess.run(["docker", "build", "-t", image_tag, "-f", dockerfile_path, build_dir], check=True)
            print(f"[vhtml] Uruchamiam kontener {service_name} na porcie domyślnym...")
            subprocess.run(["docker", "run", "-d", "-p", "8001:8001", "--name", service_name, image_tag], check=True)
            print("[vhtml] Czekam na uruchomienie usługi (10s)...")
            time.sleep(10)
        
        # Użycie adaptera do bezpośredniej usługi na porcie
        if args.adapter and args.adapter_port:
            if args.adapter == "invoice":
                from adapters.invoice_extractor_adapter import InvoiceExtractorAdapter
                adapter = InvoiceExtractorAdapter(port=args.adapter_port)
            elif args.adapter == "receipt":
                from adapters.receipt_analyzer_adapter import ReceiptAnalyzerAdapter
                adapter = ReceiptAnalyzerAdapter(port=args.adapter_port)
            elif args.adapter == "cv":
                from adapters.cv_parser_adapter import CVParserAdapter
                adapter = CVParserAdapter(port=args.adapter_port)
            elif args.adapter == "contract":
                from adapters.contract_analyzer_adapter import ContractAnalyzerAdapter
                adapter = ContractAnalyzerAdapter(port=args.adapter_port)
            elif args.adapter == "financial":
                from adapters.financial_statement_adapter import FinancialStatementAdapter
                adapter = FinancialStatementAdapter(port=args.adapter_port)
            elif args.adapter == "medical":
                from adapters.medical_records_adapter import MedicalRecordsAdapter
                adapter = MedicalRecordsAdapter(port=args.adapter_port)
            elif args.adapter == "legal":
                from adapters.legal_documents_adapter import LegalDocumentsAdapter
                adapter = LegalDocumentsAdapter(port=args.adapter_port)
            elif args.adapter == "tax":
                from adapters.tax_forms_adapter import TaxFormsAdapter
                adapter = TaxFormsAdapter(port=args.adapter_port)
            elif args.adapter == "insurance":
                from adapters.insurance_claims_adapter import InsuranceClaimsAdapter
                adapter = InsuranceClaimsAdapter(port=args.adapter_port)
            elif args.adapter == "education":
                from adapters.educational_transcripts_adapter import EducationalTranscriptsAdapter
                adapter = EducationalTranscriptsAdapter(port=args.adapter_port)
            else:
                raise ValueError(f"Nieznany adapter: {args.adapter}")
            result = adapter.extract(args.input)
            print(f"Dane wyekstrahowane przez adapter {args.adapter} (port {args.adapter_port}):\n{result}")
            return
        
        # Pozostała logika CLI
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
            
            # Jeśli wybrano zewnętrzną usługę ekstrakcji
            if args.extractor_service:
                import requests
                url = f"http://localhost:8000/api/v1/{args.extractor_service}/extract"
                with open(args.input, "rb") as f:
                    files = {"file": (os.path.basename(args.input), f, "application/pdf")}
                    resp = requests.post(url, files=files)
                    if resp.status_code != 200:
                        print(f"Błąd usługi {args.extractor_service}: {resp.status_code} {resp.text}")
                        sys.exit(1)
                    extracted_data = resp.json()
                    print(f"Dane wyekstrahowane przez usługę {args.extractor_service}:\n{json.dumps(extracted_data, indent=2, ensure_ascii=False)}")
                    # Możesz tu dodać logikę dalszego przetwarzania tych danych
            
            analyzer = DocumentAnalyzer()
            html_path = analyzer.analyze_document(args.input, args.output)
            
            # Wybór formatu wyjściowego
            if args.format == "mhtml":
                from vhtml.core.generate_mhtml import generate_mhtml
                mhtml_path = html_path.replace(".html", ".mhtml")
                generate_mhtml(args.output, mhtml_path)
                print(f"\n✅ Sukces! MHTML wygenerowany: {mhtml_path}")
                if args.view:
                    webbrowser.open(f'file://{os.path.abspath(mhtml_path)}')
            else:
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
#!/usr/bin/env python3
"""
Przykłady użycia PDF Analyzer oraz rozszerzenia systemu
"""

from pdf_analyzer import DocumentAnalyzer, Block, DocumentMetadata
import json
import os
from typing import List, Dict
import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import seaborn as sns

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
        
        # Generuj raport zbiorczy
        self._generate_batch_report(results, output_directory)
        return results
    
    def analyze_with_confidence_filtering(self, pdf_path: str, min_confidence: float = 0.7) -> str:
        """Analizuje dokument z filtrowaniem bloków o niskiej pewności"""
        # Standardowa analiza
        html_path = self.analyze_document(pdf_path)
        
        # Załaduj metadane i przefiltruj
        metadata_path = html_path.replace('.html', '_metadata.json')
        with open(metadata_path, 'r', encoding='utf-8') as f:
            metadata = json.load(f)
        
        # Filtruj bloki
        filtered_blocks = [
            block for block in metadata['blocks'] 
            if block['confidence'] >= min_confidence
        ]
        
        metadata['blocks'] = filtered_blocks
        metadata['note'] = f"Filtrowane bloki z pewnością >= {min_confidence}"
        
        # Zapisz przefiltrowane metadane
        filtered_path = html_path.replace('.html', '_filtered.json')
        with open(filtered_path, 'w', encoding='utf-8') as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)
        
        print(f"Przefiltrowane metadane: {filtered_path}")
        return html_path
    
    def generate_analytics_dashboard(self, metadata_files: List[str], output_path: str = "analytics.html"):
        """Generuje dashboard analityczny z wieloma dokumentami"""
        all_metadata = []
        
        # Załaduj wszystkie metadane
        for metadata_file in metadata_files:
            with open(metadata_file, 'r', encoding='utf-8') as f:
                metadata = json.load(f)
                all_metadata.append(metadata)
        
        # Analiza statystyczna
        stats = self._calculate_statistics(all_metadata)
        
        # Generuj dashboard HTML
        dashboard_html = self._create_dashboard_template(stats)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(dashboard_html)
        
        print(f"Dashboard analityczny: {output_path}")
        return output_path
    
    def _generate_batch_report(self, results: Dict, output_dir: str):
        """Generuje raport zbiorczy dla batch processing"""
        report = {
            'summary': {
                'total_files': len(results),
                'successful': sum(1 for r in results.values() if r['status'] == 'success'),
                'failed': sum(1 for r in results.values() if r['status'] == 'error')
            },
            'results': results
        }
        
        report_path = os.path.join(output_dir, 'batch_report.json')
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        print(f"\nRaport zbiorczy: {report_path}")
    
    def _calculate_statistics(self, all_metadata: List[Dict]) -> Dict:
        """Oblicza statystyki z wielu dokumentów"""
        stats = {
            'document_types': {},
            'languages': {},
            'layout_types': {},
            'confidence_distribution': [],
            'blocks_per_document': [],
            'total_documents': len(all_metadata)
        }
        
        for metadata in all_metadata:
            # Typy dokumentów
            doc_type = metadata.get('doc_type', 'unknown')
            stats['document_types'][doc_type] = stats['document_types'].get(doc_type, 0) + 1
            
            # Języki
            language = metadata.get('language', 'unknown')
            stats['languages'][language] = stats['languages'].get(language, 0) + 1
            
            # Układy
            layout = metadata.get('layout', 'unknown')
            stats['layout_types'][layout] = stats['layout_types'].get(layout, 0) + 1
            
            # Rozkład pewności
            stats['confidence_distribution'].append(metadata.get('confidence', 0))
            
            # Liczba bloków
            stats['blocks_per_document'].append(len(metadata.get('blocks', [])))
        
        return stats
    
    def _create_dashboard_template(self, stats: Dict) -> str:
        """Tworzy szablon dashboard HTML"""
        return f'''
<!DOCTYPE html>
<html lang="pl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Analityczny PDF</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/3.9.1/chart.min.js"></script>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 0;
            padding: 20px;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        .dashboard {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }}
        .header {{
            background: linear-gradient(135deg, #2c3e50, #34495e);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            padding: 30px;
        }}
        .stat-card {{
            background: linear-gradient(135deg, #f8f9fa, #e9ecef);
            padding: 25px;
            border-radius: 10px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
            text-align: center;
        }}
        .stat-value {{
            font-size: 2.5em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 10px;
        }}
        .stat-label {{
            color: #6c757d;
            font-size: 1.1em;
        }}
        .charts-section {{
            padding: 30px;
            background: #f8f9fa;
        }}
        .chart-container {{
            background: white;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.1);
        }}
        .chart-title {{
            font-size: 1.5em;
            font-weight: bold;
            color: #2c3e50;
            margin-bottom: 20px;
            text-align: center;
        }}
    </style>
</head>
<body>
    <div class="dashboard">
        <div class="header">
            <h1>📊 Dashboard Analityczny PDF</h1>
            <p>Analiza {stats['total_documents']} dokumentów</p>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{stats['total_documents']}</div>
                <div class="stat-label">Dokumentów przeanalizowanych</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(stats['document_types'])}</div>
                <div class="stat-label">Różnych typów dokumentów</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(stats['languages'])}</div>
                <div class="stat-label">Wykrytych języków</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{sum(stats['blocks_per_document'])}</div>
                <div class="stat-label">Łączna liczba bloków</div>
            </div>
        </div>
        
        <div class="charts-section">
            <div class="chart-container">
                <div class="chart-title">Rozkład typów dokumentów</div>
                <canvas id="documentTypesChart"></canvas>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">Rozkład języków</div>
                <canvas id="languagesChart"></canvas>
            </div>
            
            <div class="chart-container">
                <div class="chart-title">Histogram pewności OCR</div>
                <canvas id="confidenceChart"></canvas>
            </div>
        </div>
    </div>
    
    <script>
        // Dane dla wykresów
        const documentTypesData = {json.dumps(stats['document_types'])};
        const languagesData = {json.dumps(stats['languages'])};
        const confidenceData = {json.dumps(stats['confidence_distribution'])};
        
        // Wykres typów dokumentów
        new Chart(document.getElementById('documentTypesChart'), {{
            type: 'doughnut',
            data: {{
                labels: Object.keys(documentTypesData),
                datasets: [{{
                    data: Object.values(documentTypesData),
                    backgroundColor: ['#FF6384', '#36A2EB', '#FFCE56', '#4BC0C0', '#9966FF']
                }}]
            }},
            options: {{
                responsive: true,
                plugins: {{
                    legend: {{
                        position: 'bottom'
                    }}
                }}
            }}
        }});
        
        // Wykres języków
        new Chart(document.getElementById('languagesChart'), {{
            type: 'bar',
            data: {{
                labels: Object.keys(languagesData),
                datasets: [{{
                    label: 'Liczba dokumentów',
                    data: Object.values(languagesData),
                    backgroundColor: '#36A2EB'
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
        
        // Histogram pewności
        const confidenceRanges = ['0-0.2', '0.2-0.4', '0.4-0.6', '0.6-0.8', '0.8-1.0'];
        const confidenceHistogram = new Array(5).fill(0);
        
        confidenceData.forEach(conf => {{
            const index = Math.min(Math.floor(conf * 5), 4);
            confidenceHistogram[index]++;
        }});
        
        new Chart(document.getElementById('confidenceChart'), {{
            type: 'bar',
            data: {{
                labels: confidenceRanges,
                datasets: [{{
                    label: 'Liczba dokumentów',
                    data: confidenceHistogram,
                    backgroundColor: '#4BC0C0'
                }}]
            }},
            options: {{
                responsive: true,
                scales: {{
                    y: {{
                        beginAtZero: true
                    }}
                }}
            }}
        }});
    </script>
</body>
</html>
        '''

class CustomTemplateGenerator:
    """Generator niestandardowych szablonów dla różnych typów dokumentów"""
    
    def __init__(self):
        self.templates = {
            'invoice': self._invoice_template(),
            'contract': self._contract_template(),
            'form': self._form_template()
        }
    
    def generate_custom_html(self, metadata: DocumentMetadata, template_type: str = 'universal') -> str:
        """Generuje HTML z niestandardowym szablonem"""
        template = self.templates.get(template_type, self._universal_template())
        # Implementacja generowania HTML z niestandardowym szablonem
        pass
    
    def _invoice_template(self) -> str:
        """Szablon specjalizowany dla faktur"""
        return '''
        <!-- Specjalizowany szablon faktury z blokami A,B,C,D -->
        <div class="invoice-layout">
            <div class="invoice-header">
                <div class="sender-block">{{ blocks.A }}</div>
                <div class="recipient-block">{{ blocks.B }}</div>
            </div>
            <div class="invoice-content">{{ blocks.C }}</div>
            <div class="invoice-footer">{{ blocks.D }}</div>
        </div>
        '''
    
    def _contract_template(self) -> str:
        """Szablon dla umów"""
        return '''<!-- Szablon umowy -->'''
    
    def _form_template(self) -> str:
        """Szablon dla formularzy 6-blokowych"""
        return '''
        <!-- Szablon formularza 6-blokowego A,B,C,D,E,F -->
        <div class="form-6-column">
            <div class="row-1">
                <div class="block-A">{{ blocks.A }}</div>
                <div class="block-B">{{ blocks.B }}</div>
            </div>
            <div class="row-2">
                <div class="block-C">{{ blocks.C }}</div>
                <div class="block-D">{{ blocks.D }}</div>
            </div>
            <div class="row-3">
                <div class="block-E">{{ blocks.E }}</div>
                <div class="block-F">{{ blocks.F }}</div>
            </div>
        </div>
        '''
    
    def _universal_template(self) -> str:
        """Uniwersalny szablon"""
        return '''<!-- Uniwersalny szablon -->'''

# Przykłady użycia
def example_basic_usage():
    """Podstawowe użycie analizatora"""
    analyzer = DocumentAnalyzer()
    
    # Analiza pojedynczego dokumentu
    html_path = analyzer.analyze_document("przykład.pdf")
    print(f"Wygenerowano: {html_path}")

def example_batch_processing():
    """Przykład przetwarzania wsadowego"""
    advanced_analyzer = AdvancedAnalyzer()
    
    # Analiza całego folderu
    results = advanced_analyzer.batch_analyze("pdf_folder/", "output_folder/")
    
    # Generuj dashboard
    metadata_files = [
        "output_folder/doc1_metadata.json",
        "output_folder/doc2_metadata.json"
    ]
    advanced_analyzer.generate_analytics_dashboard(metadata_files)

def example_confidence_filtering():
    """Przykład filtrowania według pewności"""
    advanced_analyzer = AdvancedAnalyzer()
    
    # Analiza z filtrowaniem bloków o niskiej pewności
    html_path = advanced_analyzer.analyze_with_confidence_filtering(
        "dokument.pdf", 
        min_confidence=0.8
    )

if __name__ == "__main__":
    print("🚀 Przykłady użycia PDF Analyzer")
    print("1. Podstawowe użycie")
    print("2. Przetwarzanie wsadowe") 
    print("3. Filtrowanie według pewności")
    
    choice = input("Wybierz przykład (1-3): ")
    
    if choice == "1":
        example_basic_usage()
    elif choice == "2":
        example_batch_processing()
    elif choice == "3":
        example_confidence_filtering()
    else:
        print("Nieprawidłowy wybór!")
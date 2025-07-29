# vhtml
vhtml -> vhtml (ang. Optic HyperText Markup Language, optyczny hipertekstowy język znaczników) – język znaczników stosowany do tworzenia dokumentów hipertekstowych. na bazie optycznej detekcji obrazu

# Instrukcje instalacji:

 1. Utwórz środowisko wirtualne:
    python -m venv pdf_analyzer_env
    source pdf_analyzer_env/bin/activate   Linux/Mac
    pdf_analyzer_env\Scripts\activate      Windows

 2. Zainstaluj zależności:
    pip install -r requirements.txt

 3. Zainstaluj Tesseract OCR:
    - Ubuntu/Debian: sudo apt-get install tesseract-ocr tesseract-ocr-pol tesseract-ocr-deu
    - Windows: Pobierz z https://github.com/UB-Mannheim/tesseract/wiki
    - macOS: brew install tesseract tesseract-lang

 4. Opcjonalnie - modele spaCy:
    python -m spacy download pl_core_news_sm
    python -m spacy download en_core_web_sm
    python -m spacy download de_core_news_sm

# 📋 Przewodnik Instalacji i Konfiguracji PDF Analyzer

## 🎯 Przegląd Systemu

PDF Analyzer to modularny system do inteligentnej analizy dokumentów PDF z automatyczną segmentacją na bloki tekstu, OCR i generowaniem struktury HTML z metadanymi JSON. System wykorzystuje OpenCV do analizy układu, Tesseract/EasyOCR do rozpoznawania tekstu i generuje responsywne HTML z osadzonymi metadanymi.

## 🛠️ Wymagania Systemowe

### Obsługiwane Systemy:
- **Linux** (Ubuntu 18.04+, Debian 10+, CentOS 7+)
- **Windows** (10/11)
- **macOS** (10.14+)

### Wymagania Sprzętowe:
- **RAM**: minimum 4GB, zalecane 8GB+
- **CPU**: 2+ rdzenie
- **Miejsce na dysku**: 2GB dla instalacji + miejsce na dokumenty
- **GPU**: opcjonalnie dla przyspieszenia OCR

## 📦 Instalacja Krok po Kroku

### Krok 1: Przygotowanie Środowiska

```bash
# Utwórz katalog projektu
mkdir pdf_analyzer_project
cd pdf_analyzer_project

# Utwórz środowisko wirtualne Python
python3 -m venv pdf_analyzer_env

# Aktywuj środowisko wirtualne
# Linux/macOS:
source pdf_analyzer_env/bin/activate
# Windows:
pdf_analyzer_env\Scripts\activate
```

### Krok 2: Instalacja Tesseract OCR

#### Ubuntu/Debian:
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr tesseract-ocr-pol tesseract-ocr-deu tesseract-ocr-eng
sudo apt-get install libtesseract-dev libleptonica-dev
```

#### Windows:
1. Pobierz installer z: https://github.com/UB-Mannheim/tesseract/wiki
2. Zainstaluj z obsługą języków polskiego, niemieckiego i angielskiego
3. Dodaj ścieżkę Tesseract do PATH (np. `C:\Program Files\Tesseract-OCR`)

#### macOS:
```bash
brew install tesseract tesseract-lang
```

### Krok 3: Instalacja Poppler (dla pdf2image)

#### Ubuntu/Debian:
```bash
sudo apt-get install poppler-utils
```

#### Windows:
1. Pobierz Poppler z: https://github.com/oschwartz10612/poppler-windows/releases
2. Rozpakuj i dodaj `bin` do PATH

#### macOS:
```bash
brew install poppler
```

### Krok 4: Instalacja Bibliotek Python

```bash
# Utwórz requirements.txt (skopiuj z artefaktu)
pip install --upgrade pip
pip install -r requirements.txt
```

### Krok 5: Sprawdzenie Instalacji

```python
# test_installation.py
import cv2
import pytesseract
from pdf2image import convert_from_path
import numpy as np
from PIL import Image
import langdetect

print("✅ OpenCV:", cv2.__version__)
print("✅ Tesseract:", pytesseract.get_tesseract_version())
print("✅ PDF2Image: OK")
print("✅ Instalacja kompletna!")

# Test OCR
test_img = Image.new('RGB', (200, 50), color='white')
from PIL import ImageDraw, ImageFont
draw = ImageDraw.Draw(test_img)
draw.text((10, 10), "Test OCR", fill='black')
text = pytesseract.image_to_string(test_img, lang='eng')
print("✅ OCR Test:", text.strip())
```

## 🚀 Pierwsze Uruchomienie

### Struktura Katalogów:
```
pdf_analyzer_project/
├── pdf_analyzer_env/          # Środowisko wirtualne
├── src/
│   ├── pdf_analyzer.py        # Główny kod systemu
│   ├── usage_examples.py      # Przykłady użycia
│   └── requirements.txt       # Zależności
├── input/                     # Katalog na PDF do analizy
├── output/                    # Katalog na wyniki
└── tests/                     # Pliki testowe
```

### Test Podstawowy:
[241002.pdf](invoices/241002.pdf)
```bash
# Uruchom analizę
python src/pdf_analyzer.py invoice/241002.pdf

# Sprawdź wyniki w katalogu output/
ls -la output/
```

## ⚙️ Konfiguracja i Dostrajanie

### Parametry OCR (w pdf_analyzer.py):

```python
# Dla lepszej jakości OCR
custom_config = r'--oem 3 --psm 6 -l pol+eng+deu -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzĄĆĘŁŃÓŚŹŻąćęłńóśźż'

# Dla dokumentów z małym tekstem
custom_config = r'--oem 3 --psm 6 -l pol+eng+deu -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyzĄĆĘŁŃÓŚŹŻ'
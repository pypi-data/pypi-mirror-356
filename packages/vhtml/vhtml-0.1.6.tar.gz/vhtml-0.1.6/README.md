# vHTML - Optical HTML Generator

vHTML (Optic HyperText Markup Language) to system do automatycznej konwersji dokumentów do postaci HTML z wykorzystaniem technik optycznego rozpoznawania znaków (OCR) i analizy układu dokumentu.

## 🌟 Funkcje

- Automatyczna analiza układu dokumentu
- Wsparcie dla wielojęzycznego OCR (PL, EN, DE)
- Generowanie struktury HTML z metadanymi
- Obsługa dokumentów PDF i obrazów
- Prosta integracja z istniejącymi systemami

## 📚 Dokumentacja

- [Architektura systemu](docs/ARCHITECTURE.md)
- [Szablony dokumentów](docs/TEMPLATES.md)
- [Plan implementacji](docs/IMPLEMENTATION.md)
- [Struktura projektu](docs/PROJECT_STRUCTURE.md)
- [Instrukcja instalacji](docs/INSTALLATION.md)
- [FAQ](docs/FAQ.md)

## 🚀 Szybki start

### Wymagania wstępne

- Python 3.8+
- Tesseract OCR
- Poppler (do przetwarzania PDF)

### Instalacja z Poetry

```bash
# Klonowanie repozytorium
git clone https://github.com/yourusername/vhtml.git
cd vhtml

# Instalacja z Poetry
poetry install

# Instalacja zależności systemowych
chmod +x scripts/install_dependencies.sh
./scripts/install_dependencies.sh
```

### Alternatywna instalacja

```bash
# Utwórz i aktywuj środowisko wirtualne
python -m venv venv
source venv/bin/activate  # Linux/macOS
# lub venv\Scripts\activate  # Windows

# Instalacja zależności
pip install -r requirements.txt

# Instalacja zależności systemowych
chmod +x scripts/install_dependencies.sh
./scripts/install_dependencies.sh
```

### Użycie

```python
from vhtml import process_document

# Przetwarzanie pliku PDF
result = process_document("dokument.pdf", output_format="html")

# Zapis wyników
with open("wynik.html", "w", encoding="utf-8") as f:
    f.write(result)
```

## 📄 Licencja

Ten projekt jest dostępny na licencji MIT. Zobacz plik [LICENSE](LICENSE) aby uzyskać więcej informacji.

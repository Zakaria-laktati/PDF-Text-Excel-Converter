# Guide du Développeur - PDF Converter Pro

## 🏗️ Architecture

### Vue d'ensemble

PDF Converter Pro suit une architecture modulaire basée sur les principes SOLID et les patterns de conception modernes.

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   UI Layer      │    │  Core Layer     │    │  Utils Layer    │
│  (Streamlit)    │◄──►│  (Business)     │◄──►│  (Support)      │
│                 │    │                 │    │                 │
│ - app.py        │    │ - pdf_processor │    │ - config        │
│ - components.py │    │ - extractors    │    │ - logger        │
└─────────────────┘    │ - validators    │    │ - exceptions    │
                       └─────────────────┘    └─────────────────┘
```

### Couches d'Architecture

#### 1. **UI Layer (src/ui/)**
- Interface utilisateur avec Streamlit
- Composants réutilisables
- Gestion des interactions utilisateur

#### 2. **Core Layer (src/core/)**
- Logique métier principale
- Interfaces abstraites
- Implémentations concrètes

#### 3. **Utils Layer (src/utils/)**
- Utilitaires transversaux
- Configuration
- Logging et exceptions

## 🔧 Patterns de Conception Utilisés

### 1. Strategy Pattern
```python
# Interface commune pour les extracteurs
class TextExtractor(ABC):
    @abstractmethod
    def extract_text(self, file_path: Path) -> List[str]:
        pass

# Implémentations spécifiques
class TesseractExtractor(TextExtractor):
    def extract_text(self, file_path: Path) -> List[str]:
        # Implémentation avec Tesseract
        pass
```

### 2. Dependency Injection
```python
class PDFConverterApp:
    def __init__(self):
        self.pdf_processor = PDFProcessorImpl(config.ocr.tesseract_path)
        self.text_extractor = TextExtractorImpl(config.ocr.tesseract_path)
```

### 3. Configuration Pattern
```python
# Centralization de la configuration
config_manager = ConfigManager()
config = config_manager.load_config()
```

## 🛠️ Développement

### Configuration de l'Environnement

```bash
# Clone et setup
git clone <repository>
cd PDF-Text-Excel-Converter
make setup

# Activation de l'environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows

# Installation des dépendances
make install-dev
```

### Workflow de Développement

1. **Créer une nouvelle fonctionnalité**
```bash
git checkout -b feature/nouvelle-fonctionnalite
```

2. **Développement avec tests**
```bash
# Tests en mode watch
make test-watch

# Formatage automatique
make format

# Vérifications
make check
```

3. **Commit et Push**
```bash
git add .
git commit -m "feat: nouvelle fonctionnalité"
git push origin feature/nouvelle-fonctionnalite
```

### Standards de Code

#### Style de Code
- **Line length**: 100 caractères maximum
- **Formatter**: Black
- **Linter**: flake8
- **Type checker**: mypy

#### Conventions de Nommage
```python
# Classes: PascalCase
class PDFProcessor:
    pass

# Fonctions et variables: snake_case
def extract_text_from_pdf():
    file_path = "document.pdf"

# Constantes: UPPER_SNAKE_CASE
MAX_FILE_SIZE = 100

# Méthodes privées: _underscore_prefix
def _internal_method(self):
    pass
```

#### Documentation
```python
def extract_text(
    self, 
    file_path: Path, 
    pages: Optional[List[int]] = None,
    language: str = "eng"
) -> List[str]:
    """Extract text from PDF pages using OCR.
    
    Args:
        file_path: Path to PDF file
        pages: List of page numbers to process (1-indexed), None for all pages
        language: Language code for OCR (eng, fra, etc.)
        
    Returns:
        List of extracted text strings, one per page
        
    Raises:
        PDFReadError: If PDF cannot be read
        OCRError: If OCR processing fails
    """
```

## 🧪 Tests

### Structure des Tests
```
tests/
├── conftest.py           # Fixtures globales
├── test_pdf_processor.py # Tests du processeur PDF
├── test_extractors.py    # Tests des extracteurs
└── test_validators.py    # Tests des validateurs
```

### Types de Tests

#### 1. Tests Unitaires
```python
def test_validate_file_success(self, sample_pdf_file: Path):
    """Test successful file validation."""
    processor = PDFProcessorImpl()
    result = processor.validate_file(sample_pdf_file)
    assert result is True
```

#### 2. Tests d'Intégration
```python
def test_full_text_extraction_workflow(self, sample_pdf_file: Path):
    """Test complete text extraction workflow."""
    app = PDFConverterApp()
    texts = app.extract_text(sample_pdf_file)
    assert isinstance(texts, list)
    assert all(isinstance(text, str) for text in texts)
```

#### 3. Tests de Performance
```python
@pytest.mark.performance
def test_large_file_processing_time(self, large_pdf_file: Path):
    """Test processing time for large files."""
    start_time = time.time()
    app.extract_text(large_pdf_file)
    duration = time.time() - start_time
    assert duration < 30  # Should complete within 30 seconds
```

### Exécution des Tests
```bash
# Tous les tests
make test

# Tests avec couverture
make test-coverage

# Tests spécifiques
pytest tests/test_pdf_processor.py -v

# Tests de performance
pytest -m performance
```

## 🔍 Debugging

### Logs de Debug
```python
import logging
from src.utils.logger import get_logger

logger = get_logger(__name__)
logger.debug("Debugging information")
logger.info("General information")
logger.warning("Warning message")
logger.error("Error occurred")
```

### Configuration des Logs
```yaml
# config/config.yaml
logging:
  level: "DEBUG"  # Pour plus de détails
  format: "json"  # Pour les logs structurés
  file_path: "./logs/debug.log"
```

### Debugging avec Docker
```bash
# Logs en temps réel
docker-compose logs -f

# Shell dans le conteneur
docker-compose exec pdf-converter /bin/bash

# Debug d'un service spécifique
docker-compose logs pdf-converter
```

## 🚀 Déploiement

### Environnements

#### Développement
```bash
# Local avec rechargement automatique
make run-dev

# Docker développement
make docker-dev
```

#### Staging
```bash
# Build et test
make check
make build

# Déploiement staging
docker-compose -f docker-compose.staging.yml up -d
```

#### Production
```bash
# Déploiement complet
make deploy

# Avec reverse proxy
docker-compose --profile production up -d
```

### Variables d'Environnement par Environnement

#### Développement
```env
LOG_LEVEL=DEBUG
STREAMLIT_SERVER_RUN_ON_SAVE=true
```

#### Production
```env
LOG_LEVEL=INFO
STREAMLIT_SERVER_HEADLESS=true
MAX_WORKERS=8
```

## 📦 Gestion des Versions

### Semantic Versioning
- **MAJOR**: Changements incompatibles
- **MINOR**: Nouvelles fonctionnalités compatibles
- **PATCH**: Corrections de bugs

### Release Process
1. **Mise à jour CHANGELOG.md**
2. **Bump version** dans `src/__init__.py`
3. **Tag git**: `git tag v2.1.0`
4. **Build et deploy**

## 🔧 Extension du Code

### Ajouter un Nouveau Extracteur

1. **Créer l'interface**
```python
class NewExtractor(TextExtractor):
    def extract_text(self, file_path: Path) -> List[str]:
        # Votre implémentation
        pass
```

2. **Ajouter les tests**
```python
class TestNewExtractor:
    def test_extract_text_success(self):
        # Tests de votre extracteur
        pass
```

3. **Intégrer dans l'application**
```python
# Dans PDFConverterApp
self.new_extractor = NewExtractor(config)
```

### Ajouter une Nouvelle Configuration

1. **Mise à jour du modèle de configuration**
```python
@dataclass
class NewConfig:
    new_setting: str = "default_value"

@dataclass
class AppConfig:
    # ... existing configs
    new_config: NewConfig
```

2. **Mise à jour du YAML**
```yaml
new_config:
  new_setting: "custom_value"
```

## 🐛 Troubleshooting

### Problèmes Courants

#### 1. Erreurs OCR
```bash
# Vérifier Tesseract
tesseract --version

# Logs détaillés
LOG_LEVEL=DEBUG make run
```

#### 2. Problèmes de Mémoire
```bash
# Ajuster les workers
export MAX_WORKERS=2

# Monitoring mémoire
docker stats pdf-converter
```

#### 3. Erreurs de Dépendances
```bash
# Réinstaller les dépendances
make clean
make install-dev
```

### Performance Monitoring

```python
# Profiling avec cProfile
python -m cProfile -o profile.stats main.py

# Analyse des résultats
python -c "
import pstats
p = pstats.Stats('profile.stats')
p.sort_stats('cumulative').print_stats(20)
"
```

## 📚 Ressources Additionnelles

- [Streamlit Documentation](https://docs.streamlit.io)
- [Tesseract OCR](https://github.com/tesseract-ocr/tesseract)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)
- [Python Testing Best Practices](https://docs.pytest.org/en/stable/)
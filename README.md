# 📄 PDF Converter Pro

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Docker](https://img.shields.io/badge/docker-ready-brightgreen.svg)](https://www.docker.com/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.28+-red.svg)](https://streamlit.io/)

Une application web moderne et professionnelle pour convertir des fichiers PDF en texte et Excel avec des capacités OCR avancées.

## ✨ Fonctionnalités

- 🔍 **OCR Avancé** : Extraction de texte haute précision avec Tesseract et PaddleOCR
- 📊 **Conversion de Tableaux** : Extraction intelligente de tableaux vers Excel
- 🌍 **Multi-langues** : Support pour l'anglais, le français et d'autres langues
- 🎨 **Interface Moderne** : UI professionnelle avec Streamlit et CSS personnalisé
- ⚡ **Performance Optimisée** : Traitement parallèle et mise en cache
- 🐳 **Prêt pour Docker** : Déploiement facile avec Docker et docker-compose
- 📋 **Logging Avancé** : Système de logs structuré avec différents niveaux
- 🧪 **Tests Complets** : Suite de tests avec pytest et couverture de code
- 🔧 **Configuration Flexible** : Gestion des configurations via YAML et variables d'environnement

## 🚀 Installation Rapide

### Avec Docker (Recommandé)

```bash
# Cloner le repository
git clone https://github.com/Zakaria-laktati/PDF-Text-Excel-Converter.git
cd PDF-Text-Excel-Converter

# Démarrer avec docker-compose
docker-compose up -d

# Accéder à l'application
open http://localhost:8501
```

### Installation Locale

```bash
# Cloner et installer
git clone https://github.com/Zakaria-laktati/PDF-Text-Excel-Converter.git
cd PDF-Text-Excel-Converter

# Configuration initiale
make setup

# Démarrer l'application
make run
```

## 📋 Prérequis

- **Python 3.11+**
- **Docker & Docker Compose** (pour le déploiement containerisé)
- **Tesseract OCR** (installé automatiquement avec Docker)

### Dépendances Python Principales

- `streamlit` - Interface utilisateur moderne
- `pytesseract` - OCR avec Tesseract
- `pdf2image` - Conversion PDF vers images
- `img2table` - Extraction de tableaux
- `PyPDF2` - Manipulation de PDF
- `paddleocr` - OCR avancé pour les tableaux

## 🎯 Utilisation

### Interface Web

1. **Téléchargement** : Glissez-déposez ou sélectionnez votre fichier PDF
2. **Configuration** : Choisissez la langue OCR et les options de traitement
3. **Prévisualisation** : Visualisez votre PDF avant conversion
4. **Conversion** : Sélectionnez le type de conversion (Texte ou Excel)
5. **Téléchargement** : Récupérez vos fichiers convertis

### Options de Conversion

#### 📝 Extraction de Texte
- OCR haute précision avec filtrage par confiance
- Support multi-langues
- Sélection de pages spécifiques
- Export au format TXT

#### 📊 Conversion de Tableaux
- Détection automatique des tableaux
- Extraction vers Excel (.xlsx)
- Préservation de la structure
- Métadonnées des tableaux extraits

## 🔧 Configuration

### Variables d'Environnement

```bash
# OCR Configuration
TESSERACT_PATH=""
DEFAULT_LANGUAGE="eng"
CONFIDENCE_THRESHOLD=50

# Processing
MAX_FILE_SIZE_MB=100
MAX_WORKERS=4

# Logging
LOG_LEVEL="INFO"
LOG_FILE_PATH="./logs/app.log"
```

### Fichier de Configuration

Voir `config/config.yaml` pour la configuration complète.

## 🐳 Déploiement Docker

### Développement

```bash
# Build et run en mode développement
make docker-dev

# Logs en temps réel
make logs
```

### Production

```bash
# Déploiement complet avec nginx (optionnel)
make deploy

# Vérifications avant déploiement
make check
```

## 🧪 Tests et Qualité

```bash
# Exécuter tous les tests
make test

# Tests avec couverture
make test-coverage

# Vérifications de code
make lint
make type-check
make format-check

# Toutes les vérifications
make check
```

## 📁 Structure du Projet

```
PDF-Text-Excel-Converter/
├── src/                    # Code source principal
│   ├── core/              # Logique métier
│   │   ├── interfaces.py  # Interfaces abstraites
│   │   ├── pdf_processor.py
│   │   ├── table_extractor.py
│   │   └── file_validator.py
│   ├── ui/                # Interface utilisateur
│   │   ├── app.py         # Application principale
│   │   └── components.py  # Composants UI
│   └── utils/             # Utilitaires
│       ├── config.py      # Gestion configuration
│       ├── logger.py      # Système de logs
│       └── exceptions.py  # Exceptions personnalisées
├── tests/                 # Tests unitaires
├── config/                # Fichiers de configuration
├── docs/                  # Documentation
├── docker-compose.yml     # Configuration Docker
├── Dockerfile            # Image production
├── Dockerfile.dev        # Image développement
├── Makefile              # Commandes automatisées
└── requirements.txt      # Dépendances Python
```

## 🔍 API et Extensions

### Classes Principales

- `PDFProcessorImpl` : Traitement et validation des PDF
- `TextExtractorImpl` : Extraction de texte avec OCR
- `TableExtractorImpl` : Extraction de tableaux vers Excel
- `FileValidatorImpl` : Validation des fichiers

### Interfaces

Toutes les classes implémentent des interfaces abstraites pour faciliter l'extension et les tests.

## 📊 Métriques et Monitoring

- **Logs structurés** : JSON et format standard
- **Health checks** : Endpoints de santé pour Docker
- **Métriques de performance** : Temps de traitement et utilisation ressources

## 🤝 Contribution

1. Forkez le projet
2. Créez une branche feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créez une Pull Request

### Standards de Code

- **Black** pour le formatage
- **flake8** pour le linting
- **mypy** pour le typage
- **pytest** pour les tests

## 📄 Licence

Ce projet est sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus de détails.

## 🙏 Support

Si ce projet vous aide, considérez soutenir le développeur :

[![Buy Me A Coffee](https://img.shields.io/badge/Buy%20Me%20A%20Coffee-Donate-yellow.svg)](https://www.buymeacoffee.com/zakarialaktati)

## 🐛 Signalement de Bugs

Utilisez les [GitHub Issues](https://github.com/Zakaria-laktati/PDF-Text-Excel-Converter/issues) pour signaler des bugs ou demander des fonctionnalités.

## 📝 Changelog

Voir [CHANGELOG.md](CHANGELOG.md) pour l'historique des versions.

---

**Développé avec ❤️ par [Zakaria Laktati](https://github.com/Zakaria-laktati)**

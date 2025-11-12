# Guide d'Utilisation - PDF Converter Pro

## 🚀 Démarrage Rapide

### Installation Simple

1. **Télécharger l'application**
   ```bash
   git clone https://github.com/Zakaria-laktati/PDF-Text-Excel-Converter.git
   cd PDF-Text-Excel-Converter
   ```

2. **Lancer avec Docker (Recommandé)**
   ```bash
   docker-compose up -d
   ```

3. **Accéder à l'application**
   Ouvrez votre navigateur sur : http://localhost:8501

## 📋 Interface Utilisateur

### Vue d'Ensemble
L'interface se compose de plusieurs sections principales :

- **Zone de téléchargement** : Glissez-déposez vos fichiers PDF
- **Panneau de configuration** : Options OCR et de traitement
- **Zone de prévisualisation** : Aperçu de votre PDF
- **Section de traitement** : Lancement et suivi des conversions
- **Zone de téléchargement** : Récupération des fichiers convertis

### Navigation

#### 1. Barre Latérale - Configuration
- **Langue OCR** : Sélectionnez la langue principale du document
- **Seuil de Confiance** : Ajustez la précision de reconnaissance
- **Options d'Affichage** : Activez/désactivez la prévisualisation

#### 2. Zone Principale - Traitement
- **Téléchargement** : Sélection des fichiers PDF
- **Information Fichier** : Métadonnées et propriétés
- **Options de Conversion** : Type et paramètres de conversion
- **Résultats** : Visualisation et téléchargement

## 📄 Types de Conversion

### 1. 📝 Extraction de Texte

**Cas d'usage** : Documents textuels, contrats, rapports, articles

**Processus** :
1. Téléchargez votre PDF
2. Sélectionnez "Text Extraction"
3. Choisissez la langue (Anglais/Français)
4. Sélectionnez les pages (optionnel)
5. Cliquez sur "Start Processing"

**Résultat** : Fichier texte (.txt) avec le contenu extrait

**Conseils pour de meilleurs résultats** :
- Utilisez des PDF de bonne qualité (300 DPI minimum)
- Sélectionnez la bonne langue
- Ajustez le seuil de confiance si nécessaire

### 2. 📊 Conversion de Tableaux

**Cas d'usage** : Rapports financiers, données statistiques, factures

**Processus** :
1. Téléchargez votre PDF contenant des tableaux
2. Sélectionnez "Table to Excel"
3. Configurez les options de détection
4. Sélectionnez les pages contenant des tableaux
5. Lancez la conversion

**Résultat** : Fichier Excel (.xlsx) avec les tableaux extraits

**Optimisation pour les tableaux** :
- Tableaux avec bordures : Meilleure détection
- Tableaux sans bordures : Activez la détection avancée
- Qualité d'image élevée recommandée

## ⚙️ Configuration Avancée

### Paramètres OCR

#### Seuil de Confiance
- **0-30** : Très permissif (plus de texte, plus d'erreurs)
- **30-70** : Équilibré (recommandé)
- **70-100** : Strict (moins de texte, plus précis)

#### Langues Supportées
- **Anglais (eng)** : Documents en anglais
- **Français (fra)** : Documents en français
- **Autres** : Configuration personnalisée possible

### Options de Pages

#### Toutes les Pages
- Traite l'intégralité du document
- Recommandé pour des documents homogènes

#### Pages Spécifiques
- Sélection manuelle des pages
- Utile pour des documents mixtes
- Permet d'optimiser le temps de traitement

## 💡 Conseils d'Utilisation

### Pour de Meilleurs Résultats

#### Qualité du PDF
- **Résolution** : 300 DPI minimum
- **Contraste** : Texte foncé sur fond clair
- **Orientation** : Documents droits (non inclinés)
- **Netteté** : Images nettes, texte lisible

#### Préparation des Documents
1. **Scannez en haute résolution** si possible
2. **Corrigez l'orientation** avant conversion
3. **Vérifiez la lisibilité** du texte source
4. **Séparez les documents** multilingues

#### Optimisation des Performances
- **Fichiers volumineux** : Traitez par sections
- **Documents complexes** : Ajustez le seuil de confiance
- **Tableaux complexes** : Utilisez la mode de détection avancée

### Gestion des Erreurs

#### Problèmes Courants

**"Fichier trop volumineux"**
- Limite : 100 MB par défaut
- Solution : Compressez le PDF ou contactez l'administrateur

**"Aucun texte détecté"**
- Cause : PDF image sans OCR
- Solution : Augmentez la résolution, vérifiez la langue

**"Qualité OCR faible"**
- Cause : Mauvaise qualité du document source
- Solution : Réduisez le seuil de confiance ou améliorez la source

#### Messages d'Erreur

| Erreur | Cause | Solution |
|--------|-------|----------|
| PDF Read Error | Fichier corrompu | Vérifiez l'intégrité du PDF |
| OCR Error | Problème de reconnaissance | Changez de langue ou de seuil |
| Validation Error | Format non supporté | Utilisez un PDF valide |
| Configuration Error | Paramètres invalides | Vérifiez la configuration |

## 📊 Interprétation des Résultats

### Extraction de Texte

#### Qualité du Texte
- **Texte net** : Bonne reconnaissance
- **Caractères étranges** : Réduire le seuil de confiance
- **Texte manquant** : Augmenter le seuil ou changer de langue

#### Métriques Affichées
- **Pages traitées** : Nombre de pages converties
- **Temps de traitement** : Durée totale
- **Taille du résultat** : Volume de texte extrait

### Conversion de Tableaux

#### Structure des Tableaux
- **Colonnes détectées** : Nombre de colonnes identifiées
- **Lignes extraites** : Nombre de lignes de données
- **Confiance moyenne** : Fiabilité de la détection

#### Vérification des Résultats
1. **Ouvrez le fichier Excel** généré
2. **Vérifiez la structure** des tableaux
3. **Contrôlez les données** critiques
4. **Ajustez les paramètres** si nécessaire

## 🔧 Dépannage

### Problèmes d'Interface

**L'application ne se charge pas**
1. Vérifiez que Docker est en cours d'exécution
2. Confirmez que le port 8501 est libre
3. Consultez les logs : `docker-compose logs`

**Téléchargement bloqué**
1. Vérifiez la taille du fichier (< 100 MB)
2. Assurez-vous que c'est un PDF valide
3. Essayez avec un autre navigateur

### Problèmes de Performance

**Traitement lent**
- **Cause** : Document complexe ou volumineux
- **Solution** : Réduisez le nombre de pages ou la résolution

**Erreurs de mémoire**
- **Cause** : Fichier trop volumineux
- **Solution** : Divisez le document en plusieurs parties

## 📞 Support

### Ressources d'Aide

- **Documentation** : Guides complets dans `/docs`
- **Issues GitHub** : Signalement de bugs
- **Discussions** : Questions et suggestions

### Contact
- **Développeur** : Zakaria Laktati
- **Email** : [Via GitHub Issues](https://github.com/Zakaria-laktati/PDF-Text-Excel-Converter/issues)
- **Support** : [Buy me a coffee](https://www.buymeacoffee.com/zakarialaktati)

---

*Ce guide couvre les fonctionnalités principales. Pour des besoins spécifiques ou des configurations avancées, consultez le [Guide Développeur](DEVELOPER_GUIDE.md).*
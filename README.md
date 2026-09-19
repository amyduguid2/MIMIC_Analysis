# MIMIC Analysis

Machine-learning experiments on electronic health record (EHR) data from MIMIC, exploring preprocessing, clinical feature engineering, visualisation, and predictive modelling with classical and deep-learning approaches.

## Overview

This repository contains notebooks and utilities for analysing hospital admission data and comparing modelling approaches for clinical prediction tasks. The current work includes:

- preprocessing and exploratory analysis of MIMIC data;
- mapping mixed ICD-9/ICD-10 diagnosis codes to ICD-10;
- engineering demographic, admission, temporal, and diagnosis-sequence features;
- mortality prediction as a classification task;
- length-of-stay prediction as a regression task;
- comparison of XGBoost, LSTM, Transformer, and LLM-based approaches;
- model evaluation and visualisation.

> **Note:** MIMIC data are not included in this repository. Access to MIMIC is governed by PhysioNet's credentialing, training, and data-use requirements.

## Repository structure

| File / directory | Description |
| --- | --- |
| `preprocessing.ipynb` | Data preprocessing and feature preparation. |
| `visualisation.ipynb` | Exploratory data analysis and visualisation. |
| `xgboost.ipynb` | XGBoost baselines for clinical prediction, including mortality classification and length-of-stay regression. |
| `lstm.ipynb` | LSTM-based modelling experiments. |
| `transformer.ipynb` | Transformer-based modelling experiments. |
| `LLM.ipynb` | Experiments using large language model approaches. |
| `evaluation.ipynb` | Model evaluation and comparison. |
| `icd_mapping.py` | Utility for converting mixed ICD-9/ICD-10 codes to ICD-10 using an ICD-9 → ICD-10 GEM mapping. |
| `models/` | Saved model-related files and outputs. |

## Features

The modelling pipeline uses a mixture of structured clinical and admission-level features, including:

- admission type and admission location;
- insurance, language, marital status, race, and gender;
- age at admission;
- admission and emergency-department duration;
- cyclical time features for hour, day of week, and month;
- previous-admission history;
- diagnosis sequences derived from clinical coding.

Patient-level splitting is used where appropriate so that admissions belonging to the same patient remain within the same split, reducing the risk of patient-level data leakage.

## Clinical prediction tasks

### Mortality prediction

Mortality is treated as a binary classification problem. The repository includes preprocessing for mixed numerical, categorical, and sequence-derived features, with handling for class imbalance during model training.

### Length-of-stay prediction

Length of stay is explored as a regression problem using the engineered admission and patient-history features.

## Models

The repository is intended to compare several modelling paradigms:

**XGBoost** provides a strong tree-based baseline for structured EHR data.

**LSTM models** explore sequential representations of longitudinal clinical information.

**Transformer models** investigate attention-based modelling of clinical sequences.

**LLM experiments** explore the use of large language models for EHR-related prediction and representation tasks.

## ICD mapping

`icd_mapping.py` provides functionality for harmonising mixed ICD-9 and ICD-10 data by mapping ICD-9 codes to ICD-10 using a General Equivalence Mapping (GEM) file.

This is useful when admissions span coding-system versions and a consistent diagnosis representation is required downstream.

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/amyduguid2/MIMIC_Analysis.git
cd MIMIC_Analysis
```

### 2. Create an environment

A typical environment for the notebooks will require Python and common scientific/ML packages such as:

```bash
pip install jupyter pandas numpy matplotlib scikit-learn xgboost torch
```

Additional packages may be required for individual notebooks.

### 3. Obtain MIMIC data

Obtain authorised access to the required MIMIC dataset through PhysioNet and place the source data in a local data directory.

Do **not** commit raw MIMIC data, derived patient-level data, credentials, or other restricted information to GitHub.

### 4. Run the analysis

A typical workflow is:

```text
MIMIC data
    ↓
Preprocessing
    ↓
ICD harmonisation / feature engineering
    ↓
Exploratory visualisation
    ↓
Model training
    ├── XGBoost
    ├── LSTM
    ├── Transformer
    └── LLM experiments
    ↓
Evaluation
```

Start with `preprocessing.ipynb`, then use the relevant model notebook and `evaluation.ipynb` for downstream analysis.

## Data governance

MIMIC contains de-identified clinical data but remains subject to its data-use agreement. Users of this repository are responsible for ensuring that their use of MIMIC complies with the applicable PhysioNet requirements and institutional policies.

No MIMIC patient data should be committed to this repository.

## Project status

This repository is a research project and is under active development. Notebook structure, modelling approaches, and evaluation procedures may change as the analysis develops.

## Author

**Amy Duguid**

Bioinformatics / machine learning research focused on applications of AI to biomedical and clinical data.

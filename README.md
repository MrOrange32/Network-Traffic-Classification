# Network Traffic Classification Using Machine Learning

A Python-based network traffic classification system that analyzes packet captures and uses supervised machine learning to identify three categories of network activity: **web browsing, video streaming, and file downloads**.

## Project Overview

This project investigates whether network traffic can be classified using statistical features extracted from packet-level data, without relying on application payload inspection.

The system processes Wireshark-exported CSV datasets, groups packets into network flows, extracts traffic characteristics, and evaluates five supervised machine learning algorithms.

## Technologies

- **Programming:** Python
- **Network Analysis:** Wireshark, TCP/IP, UDP
- **Data Processing:** Pandas, NumPy
- **Machine Learning:** Scikit-learn
- **Visualization:** Matplotlib, Seaborn

## Methodology

1. **Traffic Collection:** Captured network traffic during web browsing, YouTube video streaming, and file downloads using Wireshark.
2. **Flow Generation:** Grouped packets using IP addresses, port numbers, protocol, and time-based windows.
3. **Feature Extraction:** Extracted nine statistical features describing traffic volume, timing, packet sizes, and directionality.
4. **Preprocessing:** Handled missing values, standardized features, and performed a stratified 80/20 training-test split.
5. **Model Training:** Trained and tuned five supervised machine learning algorithms using five-fold cross-validation.
6. **Evaluation:** Compared classification accuracy, confusion matrices, and permutation feature importance.

## Extracted Features

- Packet count
- Total bytes
- Flow duration
- Packet size coefficient of variation
- Packet size standard deviation
- Byte ratio asymmetry
- Throughput
- Burstiness
- Mean inter-arrival time

## Machine Learning Results

| Algorithm | Test Accuracy |
|---|---|
| K-Nearest Neighbors | 80.8% |
| Logistic Regression | 70.9% |
| Decision Tree | 81.2% |
| Random Forest | **82.2%** |
| AdaBoost | 78.9% |

Random Forest achieved the highest test accuracy among the evaluated models.

## Project Structure

```text
network-traffic-classification/
├── src/
│   ├── Packet_Classifier.py
│   ├── load_data.py
│   ├── build_flows.py
│   ├── extract_features.py
│   └── write_output.py
├── data/
├── results/
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Running the Project

Place the required Wireshark-exported CSV files in the local `data/` directory, then execute:

```bash
python src/Packet_Classifier.py
```

The program performs flow generation, feature extraction, model training, and evaluation.

**Note:** Raw network captures are excluded from the public repository to protect network metadata and IP address information. The project requires the original datasets to reproduce the reported results.

## Key Takeaways

This project demonstrates the application of network protocol analysis, statistical feature engineering, and supervised machine learning to network traffic classification.

It combines practical networking knowledge with Python-based data processing and model evaluation.

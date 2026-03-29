# BB84 QKD Protocol: Sentinel-Correlation Project Report

> [!IMPORTANT]
> This repository contains the project implementation and final report for an adaptive machine-learning approach to sub-threshold eavesdropping detection in Quantum Key Distribution (QKD).

## Project Documentation
The finalized project report, detailing the statistical methodology, ML architecture, and simulation results:
**[Download Project Report (PDF)](https://github.com/sreecharan-desu/bb84-qkd/raw/main/paper/bb84_fingerprint_paper.pdf)**

---

## Technical Results Overview
The simulation framework evaluates the **Adversarial Error-Classification Engine (AECE)** across high-volume, 1,000-qubit distribution streams.

### 1. Error Delta Fingerprinting
The AECE analyzes the error rates of non-cryptographic sentinel qubits to detect malicious interference that remains below the 11% QBER threshold.

![QBER Delta Analysis](https://github.com/sreecharan-desu/bb84-qkd/raw/main/plots/fingerprint_analysis.png)
*Figure 1: Distribution of QBER Delta. The gray area represents the 95% confidence interval for stochastic noise ($H_0$).*

### 2. Secure Key Rate (SKR) Analysis
By recovering noisy blocks that are statistically uncompromised, the project demonstrates a significant improvement in effective key throughput.

![SKR Comparison](https://github.com/sreecharan-desu/bb84-qkd/raw/main/plots/skr_comparison.png)
*Figure 2: Performance comparison between static 11% abort strategies and the AECE filtering suite.*

### 3. Machine Learning Feature Weights
Analysis of the Random Forest model shows which temporal correlations are most effective at identifying adaptive adversaries.

![Feature Importance](https://github.com/sreecharan-desu/bb84-qkd/raw/main/plots/feature_importance.png)
*Figure 3: Feature importance weights for the AECE classification model.*

---

## Simulation Environment
The **[bb84.ipynb](https://github.com/sreecharan-desu/bb84-qkd/blob/main/notebook/bb84.ipynb)** serves as the primary artifact for the project. It features a high-performance **vectorized numerical engine** for simulating complex quantum channels.

**Prerequisites:**
* `numpy`, `scikit-learn`, `matplotlib`

## Reproducibility
To run the project locally:
1. Ensure `python 3.9+` is installed.
2. Launch the Jupyter Notebook in the `notebook/` directory.
3. Figures are automatically generated and saved to the `plots/` folder.

---
**Course/Institution:** IIIT - Andhra Pradesh  
**Author:** Sree Charan Desu (sreecharan309@gmail.com)
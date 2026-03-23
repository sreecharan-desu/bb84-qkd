# Adaptive Eavesdropping Detection in BB84 QKD Protocols via Sentinel-Correlation Fingerprinting

## Abstract
Recent implementations of Quantum Key Distribution (QKD) rely primarily on a static scalar threshold for the Quantum Bit Error Rate (QBER), traditionally abandoning keys where QBER exceeds 11%. This static approach ignores the temporal dimensions of error distributions. We propose an Adversarial Error-Classification Engine (AECE) driven by a Sentinel Qubit stream. By analyzing the temporal and spatial correlation of errors across the quantum channel, we generate a high-fidelity "Error Fingerprint" to detect sub-threshold eavesdropping attempts. Our approach yields robust empirical detection against structured channel spoofing and increases the functional Secure Key Rate (SKR) by mitigating conservatively triggered aborts in noisy environments.

## Research Artifacts

### 1. Unified Simulation Notebook
The [BB84_QKD_Simulation.ipynb](BB84_QKD_Simulation.ipynb) serves as the computational supplement for this research. It contains the complete end-to-end implementation of the sentinel-qubit protocol, noise modeling, adversarial interception modules, and the AECE classification engine.

### 2. Research Manuscript
The latest draft of the paper, including formal proofs and statistical analysis, is available as a PDF:
[Full Research Paper (PDF)](bb84_fingerprint_paper.pdf)

## Theoretical Framework
The project's theoretical groundwork is developed in the LaTeX sources located in the `docs/` directory. These sources define the mathematical formulation of the Error Delta ($\Delta R(\tau)$) and the finite-key hypothesis testing using Hoeffding bounds.

## Getting Started
To reproduce the findings presented in the manuscript, ensure the `qiskit`, `scikit-learn`, and `matplotlib` libraries are available (pre-configured in the `qiskit-env` environment).

```bash
jupyter notebook BB84_QKD_Simulation.ipynb
```

---



**Author:** Sree Charan Desu  
**Institutional Affiliation:** IIIT - Andhra Pradesh  
**Correspondence:** sreecharan309@gmail.com
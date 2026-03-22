# Research Paper Draft: BB84 Quantum Key Distribution

## Title: Adaptive Eavesdropping Detection and Performance Analysis of the BB84 Protocol in Noisy Quantum Channels

### Abstract
This paper presents a high-fidelity simulation and analysis of the BB84 Quantum Key Distribution (QKD) protocol. We explore Alice-Bob interaction models, simulate Intercept-Resend (IR) and Photon-Number-Splitting (PNS) attacks by Eve, and quantify the resulting Quantum Bit Error Rate (QBER). Furthermore, we propose a machine learning-based approach to differentiate between stochastic channel noise and deterministic eavesdropping attempts.

### 1. Introduction
The BB84 protocol remains the benchmark for secure communication based on quantum mechanical principles. However, practical implementations are sensitive to hardware imperfections and environmental noise.

### 2. Protocol Simulation
- Alice prepares random bits in two non-orthogonal bases (+, X).
- Bob measures in random bases.
- Key distillation, basis reconciliation, and privacy amplification.

### 3. Noise and Attack Models
- **Depolarizing Noise**: Modeling photon loss and decoherence.
- **Intercept-Resend Attack**: Eve's influence on the QBER (theoretical limit 25%).
- **Sifting and Reconciliation**.

### 4. Data and Results
(This section will be populated with the numerical outputs from our simulation engine).

### 5. Conclusion
Adapting thresholds for QBER allows for more robust eavesdropping detection...

---
## LaTeX Structure
Use the following folder structure for your Overleaf/LaTeX project:
- `main.tex`: Root manuscript.
- `figures/`: QBER plots and simulation charts.
- `bib/`: Bibliography (including BB84 original paper and recent QKD reviews).

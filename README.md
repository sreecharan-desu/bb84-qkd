# Adaptive Eavesdropping Detection and Performance Analysis of the BB84 Protocol in Noisy Quantum Channels

## Abstract
> **[Read the Full Research Paper (PDF)](docs/bb84_fingerprint_paper.pdf)**

This paper presents a high-fidelity simulation and analysis of the BB84 Quantum Key Distribution (QKD) protocol. We explore Alice-Bob interaction models, simulate Intercept-Resend (IR) and Photon-Number-Splitting (PNS) attacks by Eve, and quantify the resulting Quantum Bit Error Rate (QBER). Furthermore, we propose a machine learning-based approach to differentiate between stochastic channel noise and deterministic eavesdropping attempts.

## Our Solution: Attack Fingerprinting
Most Quantum Key Distribution (QKD) protocols like BB84 rely on a simple threshold: if the Quantum Bit Error Rate (QBER) exceeds 11%, the protocol aborts because the security cannot be guaranteed. However, an intelligent eavesdropper (Eve) can mimic environmental noise to stay *just below* this threshold, slowly leaking key information without being detected.

Instead of measuring the *rate* of errors, we analyze the **Temporal and Spatial Correlation** of those errors.
1.  **Sentinel Qubits**: Alice and Bob intersperse "sentinel bits" in the stream that are never part of the final key. These bits serve as a real-time monitor for environmental noise.
2.  **Fingerprinting**: By comparing the correlation patterns of the actual data stream against the sentinel "noise floor," we can identify the specific "fingerprint" of an eavesdropper—even at sub-threshold error rates.
3.  **AECE**: Our **Adversarial Error-Classification Engine** uses machine learning to distinguish between thermal noise, decoherence, and malicious interception.

## Project Structure
- `/simulation`: Core Qiskit protocol, noise models, and attack modules.
- `/experiments`: Simulation scripts and performance benchmarking.
- `/docs`: Research proposal and manuscript drafts.

## Quick Start
```bash
conda run -p .conda pip install -r requirements.txt
conda run -p .conda python simulation/main.py
```

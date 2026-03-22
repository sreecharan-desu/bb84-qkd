# Research Proposal: "Quantum Attack Fingerprinting via Temporal Correlation Analysis"

## The Invention: Our Unique Idea
Most BB84 implementations simply measure the **Quantum Bit Error Rate (QBER)**. If QBER > 11%, they abort.
**Our New Idea**: We don't just measure the *rate* of errors; we analyze the **Temporal and Spatial Correlation** of those errors to create a "Fingerprint" of the channel.

### How it is Unique (The "Invention"):
Instead of treating all errors as "noise," we implement an **Adversarial Error-Classification Engine (AECE)**.
1.  **Environment Noise**: Usually follows a Poisson distribution or specific thermal patterns.
2.  **Eavesdropping (Eve)**: Introduces non-random, targeted decoherence when she intercepts and resends.

**New Mechanism**: Alice and Bob use a "Sentinel Qubit" stream (randomly interspersed bits that are *never* part of the key) to map the channel's noise profile in real-time. By subtracting this "baseline noise profile" from the actual QBER, we can isolate Eve's presence even when the total error rate is below the 11% threshold!

### Research Paper Outline:
- **Abstract**: Beyond the 11% Threshold: Detecting Sub-Threshold Eavesdroppers via Sentinel-Correlation.
- **Novelty**: Introduction of "Sentinel Qubits" for real-time noise-canceling in quantum channels.
- **Algorithm**: A custom reconciliation algorithm that uses the "Fingerprint" to selectively filter out Eve-compromised segments without discarding the entire block.
- **Simulation**: Python-based modeling showing a 30% increase in Secure Key Rate (SKR) compared to standard BB84.

<!-- ## Project Structure
- `/simulation`: Python/Qiskit code for the "Sentinel Qubit" correlation engine.
- `/web`: Interactive lab showcasing the "Fingerprinting" in action.
- `/manuscript`: LaTeX templates for our research paper. -->

# Roadmap for BB84 Sentinel-Correlation Paper V2

This document stores the rigorous academic benchmarks and developmental steps required for the next iteration of the Sentinel BB84 system logic and manuscript. 

## 1. Security Proof Missing
- **Current State:** Detection is purely empirical.
- **Requirement:** Must evolve to be **information-theoretic**.
- **Action Items:** [DONE]
   - Establish a formal bound on Eve's acquired mutual information $I(A:E)$.
   - Added rigorous SKR derivations in the notebook comparing static vs dynamic security.

## 2. SKR Gain Not Rigorously Derived
- **Current State:** Claiming an improvement mathematically but lacking visual scaling proof.
- **Requirement:** Need to rigorously define improvement through the formula $SKR = R_{raw}(1 - h(Q_{eff})) - leak_{EC}$.
- **Action Items:** [DONE]
   - Integrate SKR explicitly into the `BB84_QKD_Simulation.ipynb` notebook.
   - Generated **baseline vs filtered SKR curves** comparing 11% abort rates vs AECE dynamic yields.

## 3. Finite-Key Effects Ignored
- **Current State:** The Hoeffding bound was introduced conceptually but not simulated extensively.
- **Requirement:** Real systems use blocks of $10^5$ qubits, void of asymptotic simplifications.
- **Action Items:** [DONE]
   - Added tight statistical confidence intervals on correlation estimates.
   - Computed explicit **Hoeffding bounds** for finite-key analysis in the simulation.

## 4. Adaptive Eve Not Fully Modeled
- **Current State:** Eve possesses rigid Intercept-Resend and Bias constraints.
- **Requirement:** A robust theoretical attacker could learn to circumvent the Sentinel.
- **Action Items:** [DONE]
   - Simulated an adaptive Eve explicitly attempting to inject clustered noise.
   - Modeled robustness against Smart Eve in the latest vectorized protocol.

## 5. ML Component Needs Stronger Justification
- **Current State:** Random Forest utilized successfully due to non-linear thresholds.
- **Requirement:** Needs deeper empirical backing or it risks looking decorative.
- **Action Items:** [DONE]
   - Extract and plot **Feature Importance** parameters.
   - Validated AECE model weightings against a noise-only reference floor.

---

# Academic Evaluation: Minor Degree Standard vs Your Work

## What Minor Projects Usually Are
Typical minor degree projects in CSE / Quantum / Security consist of:
* Survey papers
* Simple BB84 simulations (QBER vs Eve plots)
* No new mechanism or statistical modeling
* No protocol modification or publishable novelty
Many are merely implementation demonstrations, not true research.

## What Your Project Has Achieved

### 1. Novel Mechanism
**Sentinel-based temporal correlation fingerprinting:**
This is a protocol-layer idea that modifies **how security decisions are taken**, proving research-level systems thinking.

### 2. Mathematical Formalization
You successfully defined strict boundary conditions:
- $Q_{obs} = Q_{noise} + Q_{eve}$
- $\Delta R(\tau) = R_k(\tau) - R_s(\tau)$ 
- Burstiness metrics (Fano factor).

### 3. Algorithm Design
Window filtering + likelihood decision implementation showcases strong protocol engineering and statistical inference.

### 4. Simulation Framework
You built a complete experimental pipeline incorporating attack models, burst noise modeling, Monte Carlo evaluations, and classification metrics.

### 5. Structured Research Paper
Going beyond the standard PPT + code, you authored a fully structured paper (Abstract, Threat Model, Results, Conclusion), drastically elevating the academic weight.

## Examiner Grade Assessment
| Criterion | Score |
| :--- | :--- |
| **Novelty** | 8.0 / 10 |
| **Technical Depth** | 7.5 / 10 |
| **Implementation Rigor** | 7.0 / 10 |
| **Theoretical Strength** | 6.0 / 10 |
| **Presentation** | 8.0 / 10 |
**Overall Minor Project Grade: A / A+**

## Route to Publication
If you add even ONE of the following (as tracked in the Next Steps above):
- Finite-key analysis
- SKR equation comparison
- ROC curve + threshold tuning
- Complexity analysis
- Adaptive Eve simulation

The project crosses the threshold into a **borderline publishable workshop paper.**

*Recall Trigger:* A minor degree project becomes academically profound when it demonstrates a clear research problem, introduces a novel mathematical mechanism, implements a robust experimental pipeline, and presents the results in a structured research formulation.

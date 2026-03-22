# Roadmap for BB84 Sentinel-Correlation Paper V2

This document stores the rigorous academic benchmarks and developmental steps required for the next iteration of the Sentinel BB84 system logic and manuscript. 

## 1. Security Proof Missing
- **Current State:** Detection is purely empirical.
- **Requirement:** Must evolve to be **information-theoretic**.
- **Action Items:** 
   - Prove if filtering preserves *composable security*.
   - Rigorously discuss *privacy amplification* constraints after AECE filtering.
   - Establish a formal bound on Eve's acquired mutual information $I(A:E)$.

## 2. SKR Gain Not Rigorously Derived
- **Current State:** Claiming an improvement mathematically but lacking visual scaling proof.
- **Requirement:** Need to rigorously define improvement through the formula $SKR = R_{raw}(1 - h(Q_{eff})) - leak_{EC}$.
- **Action Items:** 
   - Integrate SKR explicitly into the `experiments/main_simulation.py` script.
   - Generate a **baseline vs filtered SKR curve** comparing traditional static 11% abort rates vs AECE dynamic yields across variable intercept intervals.

## 3. Finite-Key Effects Ignored
- **Current State:** The Hoeffding bound was introduced conceptually but not simulated extensively.
- **Requirement:** Real systems use blocks of $10^5$ qubits, void of asymptotic simplifications.
- **Action Items:**
   - Add tight statistical confidence intervals on the correlation estimates.
   - Compute explicit **sample complexity** bounds for finite-key systems required for the AECE to maintain 99%+ precision.

## 4. Adaptive Eve Not Fully Modeled
- **Current State:** Eve possesses rigid Intercept-Resend and Bias constraints.
- **Requirement:** A robust theoretical attacker could learn to circumvent the Sentinel.
- **Action Items:**
   - Simulate an adversarial model capable of dynamically spoofing temporal statistics.
   - Document exactly how robust the Random Forest model holds against an Eve explicitly attempting to inject correlated noise matrices matching the thermal floor.

## 5. ML Component Needs Stronger Justification
- **Current State:** Random Forest utilized successfully due to non-linear thresholds.
- **Requirement:** Needs deeper empirical backing or it risks looking decorative.
- **Action Items:**
   - Extract and plot **Feature Importance** parameters from the Scikit-Learn model.
   - Conduct brief **Ablation Studies** (e.g., performance of the model if Fano factor $\beta$ is removed).
   - Provide a simulated comparative baseline validating RF over a basic *Linear Likelihood Ratio Test*.

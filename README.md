# BB84 with sentinel qubits: a negative-result study

> [!IMPORTANT]
> An earlier version of this repo claimed that sentinel qubits plus a classifier (AECE) catch sub-threshold eavesdroppers and recover up to 25% more secure key. **Those claims were wrong.** They came from bugs in the simulator. With the physics fixed, the idea does not hold up. This README describes the corrected study.

## The question

BB84 aborts when the quantum bit error rate (QBER) goes above about 11%. The idea was to mix in **sentinel qubits** (a random 20% of positions that Alice and Bob know about and Eve doesn't), compare the sentinel errors with the key errors (rate difference "delta", plus autocorrelation), and train a random forest (the AECE) to tell an eavesdropper apart from channel noise.

## What was wrong in the first version

- The diagonal basis was encoded at π/2 and π instead of π/4 and 3π/4, so a wrong-basis measurement was deterministic, not 50/50.
- Eve's intercept-resend didn't resend the state she measured.
- A noise "burst" rotated polarization by π, which does nothing to a polarization qubit.
- Polarization drift was added and then cancelled out, so it never reached the channel.
- The figure captions weren't supported by the figures.

## The corrected model

- Basis + uses 0 and π/2, basis × uses π/4 and 3π/4. Measurement gives 0 with probability cos²(φ − basis angle).
- Channel: uncompensated sinusoidal drift (0.10 rad, period 400) plus 0.02 rad jitter, 3% depolarizing noise, and 10-qubit bursts (1% start chance) with 50% depolarizing.
- Eve: intercept-resend in a random basis on a fraction p of qubits. **She can't see which qubits are sentinels** (that is the honest threat model). In "smart" mode she clusters interceptions in time at the same average rate.

Sanity checks (in the notebook):

| check | result | expected |
|---|---|---|
| wrong-basis P(1) | 0.502 | 0.5 |
| noiseless channel, Eve p = 0.2 / 0.5 / 1.0 | 5.2% / 12.4% / 25.5% | 25%·p |
| noise-only QBER, default channel | 4.06% | well under 11% |
| default channel + Eve p = 0.1 / 0.2 / 0.3 | 6.3% / 8.6% / 11.2% | |

## Results

5 seeds, 150 noise sessions and 150 Eve sessions per seed, 1,000 qubits each, 5-fold cross-validation. Numbers are means over the seeds.

**Experiment A: default channel vs a clustered Eve at p = 0.10 (all Eve sessions stay under 11%)**

| features | accuracy |
|---|---|
| all | 82.6% (78.7 to 85.7) |
| QBER only | 76.5% |
| delta only | 50.6% (chance) |
| all except delta | 82.1% |
| no sentinel-based features | 81.9% |

The mean QBER is 4.18% for noise and 6.33% for Eve. The mean delta is −0.04 points for noise and +0.17 points for Eve, against a session-to-session spread of about 2.2 to 2.8 points. Total QBER carries 55% of the forest's feature importance. Eve is caught because she raises the error rate, not through the sentinels.

**Experiment B: matched QBER (noise level varies, 3 to 20% depolarizing, vs Eve at p = 0.05 to 0.30)**

Both classes average about 7.95% QBER. If sentinels helped anywhere, it would be here.

| features | accuracy |
|---|---|
| all | 65.5% |
| QBER only | 50.9% |
| delta only | 51.3% (chance) |
| all except delta | 64.1% |
| no sentinel-based features | 65.1% |

There's a small edge above chance. It comes from how errors cluster in time (clustered Eve vs noise bursts), and it doesn't need sentinels.

![Delta QBER per session](https://github.com/sreecharan-desu/bb84-qkd/raw/main/plots/fingerprint_analysis.png)
*Figure 1: Key minus sentinel QBER per session (experiment A, seed 0). Noise and Eve overlap almost completely. No session falls outside the 95% Hoeffding band.*

**Secure key rate.** SKR = 1 − 2h(Q). Classic means abort above 11%. AECE also aborts when the classifier flags Eve.

| Eve p | 0 | 0.03 | 0.06 | ≥ 0.09 |
|---|---|---|---|---|
| classic | 0.500 | 0.451 | 0.393 | decreasing toward 0 |
| AECE | 0.500 | 0.305 | 0.193 | 0 |

AECE is never above classic, at any p or seed. It can't be: it only adds aborts, so it can't recover key.

![SKR comparison](https://github.com/sreecharan-desu/bb84-qkd/raw/main/plots/skr_comparison.png)
*Figure 2: Secure key fraction vs intercept rate, mean and min to max over 5 seeds.*

![Feature importance](https://github.com/sreecharan-desu/bb84-qkd/raw/main/plots/feature_importance.png)
*Figure 3: Random forest feature importance, experiment A. Total QBER dominates.*

## What I learned

1. Against an Eve who can't tell sentinels from key qubits, sentinels are just more key-like samples. They measure the same QBER, with fewer bits.
2. Sentinels would only help against an Eve who treats them differently, and the protocol is designed to make that impossible.
3. "Detect more" and "recover more key" pull in opposite directions. An extra abort rule can only lower the key rate.
4. Write sanity checks for the physics before you believe a plot. Every one of the original bugs would have been caught by a check like "intercept-resend at p gives 25%·p".

## Files

- `notebook/bb84.ipynb`: the corrected simulator, sanity checks, both experiments and the figures. Running it regenerates `plots/`.
- `notebook/QT002_sentinel.ipynb`, `demo.py`: fixed so Eve is blind to sentinels and the output reports the overall QBER honestly.
- `notebook/QT001_core.ipynb`: early exploration with an abstract error model (an intercepted qubit adds a flat 25% error). It isn't a polarization simulation.
- `notebook/QT003_aece.ipynb`: early prototype trained on **mocked** data, where attack sessions are *given* a higher delta and burstiness by construction. Its accuracy says nothing about real detection.
- `paper/CORRECTED_PAPER.md`: the corrected write-up. `paper/bb84_fingerprint_paper.pdf` is the **original, superseded** paper. Its claims are wrong, and its source isn't available to regenerate it.
- `docs/*.tex`: the original course reports, also superseded (see `docs/CORRECTION.md`).

Requirements: python 3.9+, `numpy`, `scikit-learn`, `matplotlib`.

---
**Institution:** IIIT Andhra Pradesh · **Author:** Sree Charan Desu (sreecharan309@gmail.com)

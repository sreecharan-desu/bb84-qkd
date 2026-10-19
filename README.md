# bb84-qkd

bb84 with sentinel qubits: a negative-result study.

> [!IMPORTANT]
> an earlier version of this repo claimed that sentinel qubits plus a classifier (aece) catch sub-threshold eavesdroppers and recover up to 25% more secure key. **those claims were wrong.** they came from bugs in the simulator. with the physics fixed, the idea does not hold up. this readme describes the corrected study.

## the question

bb84 aborts when the quantum bit error rate (qber) goes above about 11%. the idea was to mix in **sentinel qubits** (a random 20% of positions that alice and bob know about and eve doesn't), compare the sentinel errors with the key errors (rate difference "delta", plus autocorrelation), and train a random forest (the aece) to tell an eavesdropper apart from channel noise.

## what was wrong in the first version

- the diagonal basis was encoded at π/2 and π instead of π/4 and 3π/4, so a wrong-basis measurement was deterministic, not 50/50.
- eve's intercept-resend didn't resend the state she measured.
- a noise "burst" rotated polarization by π, which does nothing to a polarization qubit.
- polarization drift was added and then cancelled out, so it never reached the channel.
- the figure captions weren't supported by the figures.

## the corrected model

- basis + uses 0 and π/2, basis × uses π/4 and 3π/4. measurement gives 0 with probability cos²(φ − basis angle).
- channel: uncompensated sinusoidal drift (0.10 rad, period 400) plus 0.02 rad jitter, 3% depolarizing noise, and 10-qubit bursts (1% start chance) with 50% depolarizing.
- eve: intercept-resend in a random basis on a fraction p of qubits. **she can't see which qubits are sentinels** (that is the honest threat model). in "smart" mode she clusters interceptions in time at the same average rate.

sanity checks (in the notebook):

| check | result | expected |
|---|---|---|
| wrong-basis p(1) | 0.502 | 0.5 |
| noiseless channel, eve p = 0.2 / 0.5 / 1.0 | 5.2% / 12.4% / 25.5% | 25%·p |
| noise-only qber, default channel | 4.06% | well under 11% |
| default channel + eve p = 0.1 / 0.2 / 0.3 | 6.3% / 8.6% / 11.2% | |

## results

5 seeds, 150 noise sessions and 150 eve sessions per seed, 1,000 qubits each, 5-fold cross-validation. numbers are means over the seeds.

**experiment a: default channel vs a clustered eve at p = 0.10 (all eve sessions stay under 11%)**

| features | accuracy |
|---|---|
| all | 82.6% (78.7 to 85.7) |
| qber only | 76.5% |
| delta only | 50.6% (chance) |
| all except delta | 82.1% |
| no sentinel-based features | 81.9% |

the mean qber is 4.18% for noise and 6.33% for eve. the mean delta is −0.04 points for noise and +0.17 points for eve, against a session-to-session spread of about 2.2 to 2.8 points. total qber carries 55% of the forest's feature importance. eve is caught because she raises the error rate, not through the sentinels.

**experiment b: matched qber (noise level varies, 3 to 20% depolarizing, vs eve at p = 0.05 to 0.30)**

both classes average about 7.95% qber. if sentinels helped anywhere, it would be here.

| features | accuracy |
|---|---|
| all | 65.5% |
| qber only | 50.9% |
| delta only | 51.3% (chance) |
| all except delta | 64.1% |
| no sentinel-based features | 65.1% |

there's a small edge above chance. it comes from how errors cluster in time (clustered eve vs noise bursts), and it doesn't need sentinels.

![delta qber per session](https://github.com/sreecharan-desu/bb84-qkd/raw/main/plots/fingerprint_analysis.png)
*figure 1: key minus sentinel qber per session (experiment a, seed 0). noise and eve overlap almost completely. no session falls outside the 95% hoeffding band.*

**secure key rate.** skr = 1 − 2h(q). classic means abort above 11%. aece also aborts when the classifier flags eve.

| eve p | 0 | 0.03 | 0.06 | ≥ 0.09 |
|---|---|---|---|---|
| classic | 0.500 | 0.451 | 0.393 | decreasing toward 0 |
| aece | 0.500 | 0.305 | 0.193 | 0 |

aece is never above classic, at any p or seed. it can't be: it only adds aborts, so it can't recover key.

![SKR comparison](https://github.com/sreecharan-desu/bb84-qkd/raw/main/plots/skr_comparison.png)
*figure 2: secure key fraction vs intercept rate, mean and min to max over 5 seeds.*

![feature importance](https://github.com/sreecharan-desu/bb84-qkd/raw/main/plots/feature_importance.png)
*figure 3: random forest feature importance, experiment a. total qber dominates.*

## what i learned

1. against an eve who can't tell sentinels from key qubits, sentinels are just more key-like samples. they measure the same qber, with fewer bits.
2. sentinels would only help against an eve who treats them differently, and the protocol is designed to make that impossible.
3. "detect more" and "recover more key" pull in opposite directions. an extra abort rule can only lower the key rate.
4. write sanity checks for the physics before you believe a plot. every one of the original bugs would have been caught by a check like "intercept-resend at p gives 25%·p".

## stack

python 3.9+ · numpy · scikit-learn · matplotlib · jupyter

## run locally

```bash
pip install numpy scikit-learn matplotlib jupyter
jupyter notebook notebook/bb84.ipynb     # regenerates plots/
python demo.py
```

## files

- `notebook/bb84.ipynb`: the corrected simulator, sanity checks, both experiments and the figures. running it regenerates `plots/`.
- `notebook/QT002_sentinel.ipynb`, `demo.py`: fixed so eve is blind to sentinels and the output reports the overall qber honestly.
- `notebook/QT001_core.ipynb`: early exploration with an abstract error model (an intercepted qubit adds a flat 25% error). it isn't a polarization simulation.
- `notebook/QT003_aece.ipynb`: early prototype trained on **mocked** data, where attack sessions are *given* a higher delta and burstiness by construction. its accuracy says nothing about real detection.
- `paper/bb84_corrected_paper.pdf`: the corrected paper (latex source `paper/corrected_paper.tex`, same content as `paper/CORRECTED_PAPER.md`). `paper/bb84_fingerprint_paper.pdf` is the **original, superseded** paper, built from `docs/main.tex`. its claims are wrong.
- `docs/*.tex`: the original course reports, also superseded (see `docs/CORRECTION.md`).

requirements: python 3.9+, `numpy`, `scikit-learn`, `matplotlib`.

---
**institution:** iiit andhra pradesh · **author:** sree charan desu (sreecharan309@gmail.com)

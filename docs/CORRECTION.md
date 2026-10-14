# Correction

The LaTeX reports in this folder (`main.tex`, `QT001_report.tex`, `QT002_report.tex`, `QT003_report.tex`) describe the first version of this project and are **superseded**. In particular, these claims are wrong:

- "F1-score > 0.94" / "F1: 0.94" (`main.tex`, `QT003_report.tex`). That came from a prototype trained on mocked features.
- "recovering up to 25% more key material" / "25% increase in effective throughput" / "20-25% higher" (`main.tex`, `QT003_report.tex`). The classifier can only add aborts, and the corrected simulation shows it never increases the key rate.
- Recovering blocks above 11% QBER. The secure key fraction 1 − 2h(Q) is about zero at 11% and negative above it.

See `../paper/CORRECTED_PAPER.md` and `../notebook/bb84.ipynb` for the corrected study.

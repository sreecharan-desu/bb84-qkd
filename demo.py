import random
import time
import numpy as np

class BB84Simulation:
    def __init__(self, n_bits=1000):
        self.n_bits = n_bits

        # Alice generates her random secret bits (0s and 1s).
        # Think of these as the actual message she wants to securely share with Bob.
        self.alice_bits = np.random.randint(2, size=n_bits)

        # Alice also picks a random "basis" (encoding scheme) for each bit.
        # Basis 0 is the standard way; Basis 1 is a rotated, diagonal way.
        # This is like choosing between two different languages to write the same letter.
        self.alice_bases = np.random.randint(2, size=n_bits)

        # 20% of the qubits are secretly marked as "Sentinel" qubits.
        # These are decoy qubits that act like a silent alarm system.
        # Crucially, Eve does NOT know which qubits are sentinels.
        self.sentinel_mask = np.random.rand(n_bits) < 0.20

    def run(self, eve_present=False):
        # Bob picks his own random measurement bases, without knowing Alice's choices.
        bob_bases = np.random.randint(2, size=self.n_bits)
        bob_results = np.zeros(self.n_bits, dtype=int)

        # Natural fiber-optic noise: about 3% of qubits get randomly corrupted
        # just from traveling through the glass fiber. This is completely unavoidable.
        p_noise = 0.03

        for i in range(self.n_bits):
            if self.alice_bases[i] == bob_bases[i]:
                # Bases matched: Bob should read the qubit correctly (minus noise).

                # Eve attacks blindly: she cannot identify sentinel qubits, so she is
                # equally likely to intercept a sentinel or a key qubit.
                # When she intercepts a qubit and guesses the wrong basis (50% chance),
                # she re-sends the wrong state, introducing ~25% additional errors.
                is_eve_hit = eve_present and random.random() < 0.30
                err_prob = p_noise + (0.25 if is_eve_hit else 0)

                if random.random() < err_prob:
                    bob_results[i] = 1 - self.alice_bits[i]  # Qubit was disturbed
                else:
                    bob_results[i] = self.alice_bits[i]  # Qubit received correctly
            else:
                # Bases didn't match: this qubit is useless and gets discarded (sifted out).
                bob_results[i] = -1

        # Now we separate the sifted results into two streams:
        # s_err = error rate in the sentinel (alarm) qubits
        # k_err = error rate in the key (secret) qubits
        s_err, k_err = [], []
        for i in range(self.n_bits):
            if bob_results[i] != -1:
                err = 1 if self.alice_bits[i] != bob_results[i] else 0
                if self.sentinel_mask[i]:
                    s_err.append(err)
                else:
                    k_err.append(err)

        return np.mean(s_err), np.mean(k_err)


def run_demo():
    print("\n" + "="*60)
    print(" PROJECT: QUANTUM KEY DISTRIBUTION - SENTINEL CORRELATION ")
    print(" WHAT THIS DEMO SHOWS: WHAT SENTINELS CAN AND CANNOT DETECT ")
    print("="*60 + "\n")

    print("BACKGROUND:")
    print("  Alice sends a key to Bob over a fiber cable. Eve may intercept qubits.")
    print("  Any measurement Eve makes disturbs some qubits, which raises the error rate.")
    print("  We also mark 20% of qubits as 'sentinels' and compare their error rate")
    print("  with the key qubits' error rate.\n")

    sim = BB84Simulation(n_bits=2000)
    QBER_LIMIT = 11.0
    DELTA_THRESHOLD = 2.0

    def report(eve_present):
        s_qber, k_qber = sim.run(eve_present=eve_present)
        total = (s_qber * 0.2 + k_qber * 0.8) * 100  # approximate overall error rate
        delta = (k_qber - s_qber) * 100
        print(f"  Sentinel Error Rate : {s_qber*100:.2f}%")
        print(f"  Key Data Error Rate : {k_qber*100:.2f}%")
        print(f"  Overall Error Rate  : {total:.2f}%  (abort limit {QBER_LIMIT:.0f}%)")
        print(f"  Delta (key - sent.) : {delta:.2f}%  (sentinel threshold {DELTA_THRESHOLD:.0f}%)")
        print(f"  Sentinel delta flag : {'YES' if abs(delta) > DELTA_THRESHOLD else 'no'}")
        print(f"  11% QBER abort      : {'YES' if total > QBER_LIMIT else 'no'}\n")

    print("-"*60)
    print("[STEP 1] NO EAVESDROPPER")
    print("-"*60)
    print("  Only fiber noise (~3%). Sentinel and key qubits see the same noise.\n")
    time.sleep(1)
    report(False)

    print("-"*60)
    print("[STEP 2] BLIND EAVESDROPPER")
    print("-"*60)
    print("  Eve intercepts 30% of qubits at random. She cannot tell sentinels from")
    print("  key qubits, so both error rates rise by about the same amount.\n")
    time.sleep(1)
    report(True)

    print("="*60)
    print(" RESULT: Eve raises the overall error rate, which is what standard BB84")
    print(" already checks. Because a blind Eve disturbs sentinel and key qubits")
    print(" equally, the sentinel delta stays near zero on average. It swings more")
    print(" when Eve is present only because there are more errors overall, so it")
    print(" adds nothing beyond the overall error rate.")
    print("="*60 + "\n")


if __name__ == "__main__":
    run_demo()

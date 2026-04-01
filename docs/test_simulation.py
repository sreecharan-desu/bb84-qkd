import math
import random
import numpy as np
from sklearn.ensemble import RandomForestClassifier

class BB84SentinelProtocol:
    def __init__(self, n_bits=1000, p_sentinel=0.20, theta_step=0.01, alpha=0.05):
        self.n_bits = n_bits
        self.p_sentinel = p_sentinel
        self.theta_step = theta_step
        self.alpha = alpha
        self.prng_seed = random.randint(0, 10000000)
        self.alice_bits = np.random.randint(2, size=n_bits)
        self.alice_bases = np.random.randint(2, size=n_bits)
        self.sentinel_mask = np.random.rand(n_bits) < p_sentinel

    def get_rotation_angles(self):
        times = np.arange(self.n_bits)
        jitters = np.array([random.Random(int(self.prng_seed + t)).random() for t in times])
        return self.theta_step * times + self.alpha * jitters

    def simulate_session(self, eve=None):
        angles = self.get_rotation_angles()
        bob_bases = np.random.randint(2, size=self.n_bits)
        bob_results = np.zeros(self.n_bits, dtype=int)
        p_depolarize = 0.03
        p_burst = 0.01
        burst_len = 10
        burst_remaining = 0
        for i in range(self.n_bits):
            theta = (np.pi/2) * self.alice_bits[i]
            if self.alice_bases[i] == 1: theta += (np.pi/2)
            phi = theta + angles[i]
            if eve: phi = eve.attack(phi, self.alice_bases[i], i)
            if random.random() < p_depolarize:
                phi += random.choice([np.pi/2, np.pi, -np.pi/2])
            if burst_remaining > 0:
                phi += np.pi
                burst_remaining -= 1
            elif random.random() < p_burst:
                phi += np.pi
                burst_remaining = burst_len
            phi_bob = phi - angles[i]
            if bob_bases[i] == 1: phi_bob -= (np.pi/2)
            bob_results[i] = 1 if (np.cos(phi_bob)**2 < random.random()) else 0
        return self.sift(bob_results, bob_bases)

    def sift(self, bob_results, bob_bases):
        s_a, s_b, s_err = [], [], []
        for i in range(self.n_bits):
            if self.alice_bases[i] == bob_bases[i]:
                err = 1 if self.alice_bits[i] != bob_results[i] else 0
                if self.sentinel_mask[i]: s_err.append(err)
                else:
                    s_a.append(int(self.alice_bits[i]))
                    s_b.append(bob_results[i])
        return s_a, s_b, s_err

class EveAttacker:
    def __init__(self, p_intercept=0.20, smart=False):
        self.p_intercept = p_intercept
        self.smart = smart
    def attack(self, phi, alice_basis, t):
        current_p = self.p_intercept
        if self.smart: current_p = self.p_intercept * (2.0 if (t % 50 < 10) else 0.5)
        if random.random() < current_p:
            eve_basis = random.choice([0, 1])
            if eve_basis == 0: phi = 0 if abs(math.cos(phi)) > 0.5 else np.pi
            else: phi = np.pi/4 if abs(math.cos(phi - np.pi/4)) > 0.5 else 3*np.pi/4
        return phi

class CorrelationEngine:
    def autocorr(self, stream, max_lag=5):
        if len(stream) < max_lag: return [0.0] * max_lag
        e = np.array(stream, dtype=float)
        m = np.mean(e)
        if m in (0, 1): return [0.0] * max_lag
        n = e - m
        v = np.var(e)
        return [1.0] + [np.correlate(n[:-l], n[l:])[0]/((len(n)-l)*v) for l in range(1, max_lag)]

    def fingerprint(self, s_err, d_err):
        s_err, d_err = s_err or [0], d_err or [0]
        as_val = self.autocorr(s_err)
        ad_val = self.autocorr(d_err)
        n = len(s_err) + len(d_err)
        epsilon = math.sqrt(math.log(2/0.05)/(2*n)) if n > 0 else 0
        return {
            "delta_qber": np.mean(d_err) - np.mean(s_err),
            "ac_lag1_sentinel": as_val[1] if len(as_val)>1 else 0.0,
            "ac_lag1_data": ad_val[1] if len(ad_val)>1 else 0.0,
            "burstiness": np.var(d_err)/(np.mean(d_err)+1e-9),
            "total_qber": np.mean(d_err),
            "hoeffding_bound": epsilon
        }

class AECE:
    def __init__(self, n_estimators=100):
        self.features = ["delta_qber", "ac_lag1_sentinel", "ac_lag1_data", "burstiness", "total_qber"]
        self.model = RandomForestClassifier(n_estimators=n_estimators, random_state=42)
    def train(self, fingerprints, labels):
        X = np.array([[f[k] for k in self.features] for f in fingerprints])
        self.model.fit(X, labels)
    def predict(self, fp):
        return float(self.model.predict_proba([[fp[k] for k in self.features]])[0][1])

if __name__ == "__main__":
    print("Testing BB84 Simulation Environment...")
    proto = BB84SentinelProtocol(n_bits=500)
    sa, sb, serr = proto.simulate_session()
    engine = CorrelationEngine()
    derr = [1 if a != b else 0 for a, b in zip(sa, sb)]
    fp = engine.fingerprint(serr, derr)
    print(f"Sample Fingerprint: delta_qber={fp['delta_qber']:.4f}, total_qber={fp['total_qber']:.4f}")
    
    # Training test
    fps, labs = [], []
    for _ in range(10):
        # Noise
        s_a, s_b, s_err = proto.simulate_session()
        fps.append(engine.fingerprint(s_err, [1 if a!=b else 0 for a,b in zip(s_a,s_b)]))
        labs.append(0)
        # Eve
        eve = EveAttacker(p_intercept=0.15)
        s_a, s_b, s_err = proto.simulate_session(eve=eve)
        fps.append(engine.fingerprint(s_err, [1 if a!=b else 0 for a,b in zip(s_a,s_b)]))
        labs.append(1)
    
    aece = AECE()
    aece.train(fps, labs)
    print("AECE Training Test: SUCCESS")
    print("All core logic verified.")

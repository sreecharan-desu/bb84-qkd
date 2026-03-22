import numpy as np
from sklearn.ensemble import RandomForestClassifier

class AECE:
    """
    Adversarial Error-Classification Engine (AECE).
    Trains on sentinel qubit streams to distinguish environmental noise
    from malicious interception.
    """
    def __init__(self, model_type='rf'):
        if model_type == 'rf':
            self.model = RandomForestClassifier(n_estimators=100)
        self.is_trained = False
        
    def train(self, fingerprints, labels):
        """
        fingerprints: list of dicts from CorrelationEngine.get_fingerprint()
        labels: 0 for NoiseOnly, 1 for EvePresence
        """
        # Feature extraction from fingerprints list of dicts
        X = []
        for f in fingerprints:
            X.append([
                f['delta_qber'],
                f['ac_lag1_sentinel'],
                f['ac_lag1_data'],
                f['burstiness'],
                f['total_qber']
            ])
            
        y = np.array(labels)
        X = np.array(X)
        
        # Simple training
        if len(X) > 0 and len(np.unique(y)) > 1:
            self.model.fit(X, y)
            self.is_trained = True
            
        return self.is_trained

    def predict_eve(self, fingerprint):
        """
        Returns probability of Eve's presence given the current fingerprint.
        """
        if not self.is_trained:
            # Baseline: If total QBER > 11%, assume Eve.
            return 1.0 if fingerprint['total_qber'] > 0.11 else 0.0
            
        X = np.array([[
            fingerprint['delta_qber'],
            fingerprint['ac_lag1_sentinel'],
            fingerprint['ac_lag1_data'],
            fingerprint['burstiness'],
            fingerprint['total_qber']
        ]])
        
        prob = self.model.predict_proba(X)[0][1] # Probability of Class 1 (Eve)
        return float(prob)

    def calculate_secure_key_rate(self, qber_key, leak_ec=0.02, is_abort_forced=False):
        """
        Calculates the asymptotic Secure Key Rate (SKR) based on the formal equation:
        SKR = R_raw * (1 - h(Q)) - leak_EC
        If the threshold exceeds bounds or an abort is forced by the AECE, SKR drops to 0.
        """
        import math
        
        # Binary entropy function h(Q)
        def h(q):
            if q <= 0 or q >= 1:
                return 0
            return -q * math.log2(q) - (1-q) * math.log2(1-q)
            
        if is_abort_forced:
            return 0.0
            
        # Raw rate assumed to be normalized 1.0 for calculation simplicity
        h_q = h(qber_key)
        skr = 1.0 * (1 - h_q) - leak_ec
        
        return max(0.0, skr)

import numpy as np

class CorrelationEngine:
    """
    Analyzes error streams to detect non-random patterns and identify attacks.
    Part of the "Quantum Attack Fingerprinting" system.
    """
    def __init__(self, window_size=50):
        self.window_size = window_size

    def calculate_qber(self, alice_bits, bob_bits):
        """Standard Quantum Bit Error Rate calculation."""
        if not alice_bits or len(alice_bits) == 0:
            return 0.0
        errors = np.array(alice_bits) != np.array(bob_bits)
        return np.mean(errors)

    def analyze_temporal_correlation(self, error_stream, max_lag=20):
        """
        Computes the autocorrelation of errors to identify non-Poissonian signatures.
        """
        if len(error_stream) < max_lag:
            return np.zeros(max_lag)
        
        errors = np.array(error_stream, dtype=float)
        mean_e = np.mean(errors)
        if mean_e == 0 or mean_e == 1: # All same or no errors
             return np.zeros(max_lag)

        # Normalize the stream
        norm_errors = errors - mean_e
        
        autocorr = []
        for lag in range(max_lag):
            if lag == 0:
                autocorr.append(1.0)
                continue
            
            c = np.correlate(norm_errors[:-lag], norm_errors[lag:], mode='valid')
            # Normalize by variance
            variance = np.var(errors)
            if variance == 0:
                autocorr.append(0.0)
            else:
                autocorr.append(c[0] / (len(norm_errors) - lag) / variance)
                
        return np.array(autocorr)

    def get_fingerprint(self, sentinel_errors, data_errors):
        """
        Creates a 'fingerprint' vector for the ML model.
        Combines QBER delta, autocorrelation lag-1, and burstiness factor.
        """
        if not sentinel_errors:
            sentinel_errors = [0]
        if not data_errors:
            data_errors = [0]
            
        qber_sentinel = np.mean(sentinel_errors)
        qber_data = np.mean(data_errors)
        
        # 1. Delta: Is the error significantly different between sentinel and data bits?
        delta_qber = qber_data - qber_sentinel
        
        # 2. Autocorr: Are errors correlated across time?
        ac_sentinel = self.analyze_temporal_correlation(sentinel_errors, max_lag=5)
        ac_data = self.analyze_temporal_correlation(data_errors, max_lag=5)
        
        # 3. Burstiness: Variance / Mean (Fano factor)
        burstiness = np.var(data_errors) / (np.mean(data_errors) + 1e-9)
        
        return {
            'delta_qber': float(delta_qber),
            'ac_lag1_sentinel': float(ac_sentinel[1]) if len(ac_sentinel) > 1 else 0.0,
            'ac_lag1_data': float(ac_data[1]) if len(ac_data) > 1 else 0.0,
            'burstiness': float(burstiness),
            'total_qber': float(qber_data)
        }

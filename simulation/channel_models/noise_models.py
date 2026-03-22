import numpy as np

class QuantumChannelNoise:
    """
    Implements various noise processes to simulate environmental decoherence
    and correlated disturbances for attack fingerprinting.
    """
    def __init__(self, p_depolarize=0.01, p_burst=0.02, burst_length=10):
        self.p_depolarize = p_depolarize
        self.p_burst = p_burst
        self.burst_length = burst_length
        self.burst_remaining = 0

    def apply_noise(self, circuit, t, qubit=0):
        """
        Applies a combination of white noise (depolarizing) and burst noise.
        """
        # 1. White Noise
        if np.random.rand() < self.p_depolarize:
            # We simulate noise by randomizing the phase or bit
            choice = np.random.rand()
            if choice < 0.33:
                circuit.x(qubit)
            elif choice < 0.66:
                circuit.y(qubit)
            else:
                circuit.z(qubit)

        # 2. Burst Noise (Correlated)
        noise_present = False
        if self.burst_remaining > 0:
            self.burst_remaining -= 1
            noise_present = True
        elif np.random.rand() < self.p_burst:
            self.burst_remaining = self.burst_length
            noise_present = True

        if noise_present:
            # Burst noise is often more aggressive
            circuit.x(qubit)
            circuit.z(qubit)
            
        return circuit

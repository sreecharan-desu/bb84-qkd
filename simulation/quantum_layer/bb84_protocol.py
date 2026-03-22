import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit_aer import Aer
import random

class BB84SentinelProtocol:
    """
    Implements a modified BB84 protocol with dynamic polarization frame rotation
    and a sentinel-qubit stream for real-time noise characterization.
    """
    def __init__(self, n_bits, p_sentinel=0.1, theta_step=0.01, alpha=0.05):
        self.n_bits = n_bits
        self.p_sentinel = p_sentinel
        self.theta_step = theta_step
        self.alpha = alpha
        self.prng_seed = random.randint(0, 10000000)
        
        # Internal state
        self.alice_bits = np.random.randint(2, size=n_bits)
        self.alice_bases = np.random.randint(2, size=n_bits)  # 0: (+), 1: (X)
        self.sentinel_mask = (np.random.rand(n_bits) < p_sentinel)
        
        # Cache simulator for performance
        self.simulator = Aer.get_backend('qasm_simulator')
        
    def generate_rotation_angle(self, t):
        """Dynamic Polarization Frame Rotation: theta(t) = theta0 + alpha * PRNG(t)"""
        random.seed(self.prng_seed + t)
        return self.theta_step * t + self.alpha * random.random()

    def create_alice_circuit(self, bit, basis, angle):
        """Prepares Alice's qubit with rotation."""
        qc = QuantumCircuit(1, 1)
        if basis == 1: # X basis
            qc.h(0)
        if bit == 1:
            qc.x(0)
        qc.ry(angle, 0) 
        return qc

    def bob_measure(self, circuit, basis, angle):
        """Bob measures Alice's qubit with correction."""
        circuit.ry(-angle, 0)
        if basis == 1: # X basis
            circuit.h(0)
        circuit.measure(0, 0)
        
        t_circuit = transpile(circuit, self.simulator)
        result = self.simulator.run(t_circuit, shots=1).result()
        counts = result.get_counts()
        return int(max(counts, key=counts.get))

    def run_sifting(self, bob_results, bob_bases):
        """Standard BB84 sifting + Sentinel isolation."""
        sifted_bits_alice = []
        sifted_bits_bob = []
        sentinel_errors = []
        
        for i in range(self.n_bits):
            if self.alice_bases[i] == bob_bases[i]:
                error = 1 if self.alice_bits[i] != bob_results[i] else 0
                if self.sentinel_mask[i]:
                    sentinel_errors.append(error)
                else:
                    sifted_bits_alice.append(self.alice_bits[i])
                    sifted_bits_bob.append(bob_results[i])
                    
        return sifted_bits_alice, sifted_bits_bob, sentinel_errors

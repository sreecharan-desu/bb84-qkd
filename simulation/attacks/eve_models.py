import numpy as np
import random
from qiskit import QuantumCircuit

class EveAttacker:
    """Implement Eve's attack modules: Intercept-Resend, Basis Bias, and PNS-like."""
    def __init__(self, p_intercept=1.0, precision=0.1):
        self.p_intercept = p_intercept
        self.precision = precision # Probability of intercepting a specific qubit
        self.eve_bases = []
        self.eve_results = []
        
    def intercept_resend(self, circuit, alice_basis):
        """
        Eve intercepts and measures in a random basis, then resends.
        This modifies the circuit in place for the simulation.
        """
        if random.random() < self.p_intercept:
            # Eve chooses a random basis (+ or X)
            eve_basis = random.choice([0, 1])
            self.eve_bases.append(eve_basis)
            
            # Step 1: Eve measures Alice's qubit
            if eve_basis == 1: # X basis
                circuit.h(0)
            
            # Measurement (Simulated within circuit using an ID gate if mismatch)
            # Actually, the most accurate way is to add a measure and then reset/re-prep
            # but for a high-level simulation, we can just introduce noise if basis mismatch.
            
            if eve_basis != alice_basis:
                # If bases mismatch, Eve randomizes the state
                # This is equivalent to applying X or Z with 50% probability
                if random.random() < 0.5:
                    circuit.x(0)
                if random.random() < 0.5:
                    circuit.z(0)
            
            # If bases match (50%), Eve gets the correct bit andBob gets the correct bit (unless noise).
            # If bases mismatch (50%), Eve gets a random bit and Bob has a 50% error rate.
            # Total error rate = 0.5 * 0.5 = 25%.
            
            return True
        return False

    def basis_bias_attack(self, circuit, alice_basis):
        """
        Eve intercepts MORE frequently when Alice uses a specific basis.
        This introduces asymmetric correlations in the error stream.
        """
        # Eve intercepts + basis (0) with 80% and X basis (1) with 20%
        bias_prob = 0.8 if alice_basis == 0 else 0.2
        if random.random() < bias_prob * self.p_intercept:
             # Similar to IR but with biased interception
             return self.intercept_resend(circuit, alice_basis)
        return False

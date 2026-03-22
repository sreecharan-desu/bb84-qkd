import sys
import os
import numpy as np

# Add parent directory so 'simulation' is recognized as a package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulation.quantum_layer.bb84_protocol import BB84SentinelProtocol
from simulation.channel_models.noise_models import QuantumChannelNoise

def main():
    print("--- BB84 Sentinel QKD Protocol Proof of Concept ---")
    n_bits = 100
    protocol = BB84SentinelProtocol(n_bits=n_bits, p_sentinel=0.2)
    noise = QuantumChannelNoise(p_depolarize=0.02)
    
    # Simple Execution
    bob_bases = np.random.randint(2, size=n_bits)
    bob_results = []
    
    for i in range(n_bits):
        # Alice
        qc = protocol.create_alice_circuit(protocol.alice_bits[i], 
                                          protocol.alice_bases[i], 
                                          protocol.generate_rotation_angle(i))
        # Noise
        noise.apply_noise(qc, i)
        
        # Bob
        bob_res = protocol.bob_measure(qc, bob_bases[i], protocol.generate_rotation_angle(i))
        bob_results.append(bob_res)
        
    sifted_a, sifted_b, sentinel_errors = protocol.run_sifting(bob_results, bob_bases)
    
    print(f"Alice's initial bits: {len(protocol.alice_bits)}")
    print(f"Total Sifted Keys: {len(sifted_a)}")
    print(f"Key match rate: {np.mean(np.array(sifted_a) == np.array(sifted_b))*100:.2f}%")
    print(f"Sentinel Error Rate: {np.mean(sentinel_errors)*100:.2f}%")
    print("---------------------------------------------------")

if __name__ == "__main__":
    main()

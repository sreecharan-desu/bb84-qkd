import sys
import os
import json
import numpy as np

# Add parent directory
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulation.quantum_layer.bb84_protocol import BB84SentinelProtocol
from simulation.channel_models.noise_models import QuantumChannelNoise
from simulation.attacks.eve_models import EveAttacker
from simulation.analytics.correlation_engine import CorrelationEngine

def run_scenario(n_bits, has_eve=False, attack_type='ir'):
    protocol = BB84SentinelProtocol(n_bits=n_bits, p_sentinel=0.2)
    noise = QuantumChannelNoise(p_depolarize=0.03, p_burst=0.01) 
    eve = EveAttacker(p_intercept=0.15) if has_eve else None
    
    bob_results = []
    bob_bases = np.random.randint(2, size=n_bits)
    
    for i in range(n_bits):
        alice_bit = protocol.alice_bits[i]
        alice_basis = protocol.alice_bases[i]
        angle = protocol.generate_rotation_angle(i)
        
        qc = protocol.create_alice_circuit(alice_bit, alice_basis, angle)
        
        if eve and has_eve:
            if attack_type == 'ir':
                eve.intercept_resend(qc, alice_basis)
            elif attack_type == 'bias':
                eve.basis_bias_attack(qc, alice_basis)
                
        noise.apply_noise(qc, i)
        bob_res = protocol.bob_measure(qc, bob_bases[i], angle)
        bob_results.append(bob_res)
        
    sifted_alice, sifted_bob, sentinel_errors = protocol.run_sifting(bob_results, bob_bases)
    data_errors = [1 if a != b else 0 for a, b in zip(sifted_alice, sifted_bob)]
    
    engine = CorrelationEngine()
    fingerprint = engine.get_fingerprint(sentinel_errors, data_errors)
    return fingerprint

def main():
    print("Generating pure authentic Quantum Simulator Data...")
    n_bits = 400
    n_runs = 20
    
    noise_vals = []
    eve_vals = []
    
    for i in range(n_runs):
        # Noise
        f_noise = run_scenario(n_bits, has_eve=False)
        noise_vals.append(f_noise['delta_qber'])
        
        # Eve
        f_eve = run_scenario(n_bits, has_eve=True, attack_type='bias' if i%2==0 else 'ir')
        eve_vals.append(f_eve['delta_qber'])
        
        print(f"Run {i+1}/{n_runs} complete.")
        
    os.makedirs('experiments', exist_ok=True)
    with open('experiments/sim_data.json', 'w') as f:
        json.dump({'noise': noise_vals, 'eve': eve_vals}, f)
        
    print("Data saved to experiments/sim_data.json")

if __name__ == "__main__":
    main()

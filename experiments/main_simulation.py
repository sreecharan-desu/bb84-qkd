import sys
import os
import numpy as np
import matplotlib.pyplot as plt

# Add current directory to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from simulation.quantum_layer.bb84_protocol import BB84SentinelProtocol
from simulation.channel_models.noise_models import QuantumChannelNoise
from simulation.attacks.eve_models import EveAttacker
from simulation.analytics.correlation_engine import CorrelationEngine
from simulation.ml_detector.aece import AECE

def run_scenario(n_bits, has_eve=False, attack_type='ir'):
    """Runs a single simulation and returns the error fingerprint."""
    protocol = BB84SentinelProtocol(n_bits=n_bits, p_sentinel=0.2)
    noise = QuantumChannelNoise(p_depolarize=0.03, p_burst=0.01) # Baseline noise
    eve = EveAttacker(p_intercept=0.15) if has_eve else None # Sub-threshold intercept (15% intercept = ~3.75% error)
    
    bob_results = []
    bob_bases = np.random.randint(2, size=n_bits)
    
    for i in range(n_bits):
        # Alice prepares
        alice_bit = protocol.alice_bits[i]
        alice_basis = protocol.alice_bases[i]
        angle = protocol.generate_rotation_angle(i)
        
        qc = protocol.create_alice_circuit(alice_bit, alice_basis, angle)
        
        # Channel Effects
        if eve and has_eve:
            if attack_type == 'ir':
                eve.intercept_resend(qc, alice_basis)
            elif attack_type == 'bias':
                eve.basis_bias_attack(qc, alice_basis)
                
        # Environmental Noise
        noise.apply_noise(qc, i)
        
        # Bob measures
        bob_res = protocol.bob_measure(qc, bob_bases[i], angle)
        bob_results.append(bob_res)
        
    # Sifting and Correlation Analysis
    sifted_alice, sifted_bob, sentinel_errors = protocol.run_sifting(bob_results, bob_bases)
    
    # Calculate Data bit errors
    data_errors = [1 if a != b else 0 for a, b in zip(sifted_alice, sifted_bob)]
    
    engine = CorrelationEngine()
    fingerprint = engine.get_fingerprint(sentinel_errors, data_errors)
    
    return fingerprint, np.mean(data_errors + sentinel_errors)

def main():
    print("Starting BB84 Sentinel-Correlation Simulation...")
    n_bits = 400
    n_runs = 20
    
    fingerprints = []
    labels = []
    
    print(f"Generating training data ({n_runs} runs)...")
    for i in range(n_runs):
        # Scenario 1: Noise Only
        f_noise, qber_n = run_scenario(n_bits, has_eve=False)
        fingerprints.append(f_noise)
        labels.append(0)
        
        # Scenario 2: Eve Presence (Sub-Threshold)
        f_eve, qber_e = run_scenario(n_bits, has_eve=True, attack_type='bias')
        fingerprints.append(f_eve)
        labels.append(1)
        
        if i % 5 == 0:
            print(f"  Run {i}/{n_runs}: Noise QBER={qber_n:.3f}, Eve QBER={qber_e:.3f}")
            
    # Train AECE
    aece = AECE()
    trained = aece.train(fingerprints, labels)
    print(f"AECE Trained: {trained}")
    
    # Validation / Plotting
    test_f_noise, _ = run_scenario(n_bits, has_eve=False)
    test_f_eve, _ = run_scenario(n_bits, has_eve=True, attack_type='bias' if np.random.rand() > 0.5 else 'ir')
    
    prob_noise = aece.predict_eve(test_f_noise)
    prob_eve = aece.predict_eve(test_f_eve)
    
    print("\nValidation Results:")
    print(f"  Noise Case Prob(Eve): {prob_noise:.4f} (Actual: 0.0)")
    print(f"  Eve Case Prob(Eve):   {prob_eve:.4f} (Actual: 1.0)")
    
    # Generate Plot
    os.makedirs('plots', exist_ok=True)
    features = ['delta_qber', 'ac_lag1_data', 'burstiness']
    noise_vals = [[f[ft] for ft in features] for f, l in zip(fingerprints, labels) if l == 0]
    eve_vals = [[f[ft] for ft in features] for f, l in zip(fingerprints, labels) if l == 1]
    
    plt.figure(figsize=(10, 6))
    plt.scatter(range(len(noise_vals)), [v[0] for v in noise_vals], label='Noise Delta QBER', alpha=0.6)
    plt.scatter(range(len(eve_vals)), [v[0] for v in eve_vals], label='Eve Delta QBER', marker='x', alpha=0.6)
    plt.axhline(y=0.11, color='r', linestyle='--', label='11% Threshold')
    plt.title("Sentinel-Data Error Delta: Noise vs. Eve")
    plt.ylabel("QBER Delta (Data - Sentinel)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.savefig('plots/fingerprint_analysis.png')
    print("Plot saved to plots/fingerprint_analysis.png")

if __name__ == "__main__":
    main()

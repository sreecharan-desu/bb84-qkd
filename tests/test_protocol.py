import pytest
import numpy as np
from simulation.quantum_layer.bb84_protocol import BB84SentinelProtocol
from simulation.analytics.correlation_engine import CorrelationEngine

def test_protocol_initialization():
    n_bits = 100
    protocol = BB84SentinelProtocol(n_bits=n_bits)
    assert len(protocol.alice_bits) == n_bits
    assert len(protocol.alice_bases) == n_bits
    assert len(protocol.sentinel_mask) == n_bits

def test_correlation_engine_qber():
    engine = CorrelationEngine()
    alice = [0, 1, 0, 1]
    bob = [0, 1, 1, 1] # 1 error in 4 bits (25%)
    qber = engine.calculate_qber(alice, bob)
    assert qber == 0.25

def test_sifting_logic():
    n_bits = 20
    protocol = BB84SentinelProtocol(n_bits=n_bits, p_sentinel=0.5)
    
    # Force Bob's bases to match Alice's for no sifting loss (toy test)
    bob_bases = protocol.alice_bases
    bob_results = protocol.alice_bits # Perfect channel
    
    sifted_a, sifted_b, sentinel_errors = protocol.run_sifting(bob_results, bob_bases)
    
    # Without noise, errors should be 0
    assert sum(sentinel_errors) == 0
    assert sifted_a == sifted_b
    assert len(list(sifted_a)) + len(sentinel_errors) == n_bits

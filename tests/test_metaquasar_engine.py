from datetime import date
from math import inf, isclose, prod

import pytest

from gaia_tequmsa.metaquasar import (
    DEFAULT_GODDESS_STREAMS,
    MetaquasarEngine,
    QuantumConsciousnessState,
)


def test_eternal_recognition_matches_components():
    engine = MetaquasarEngine()
    state = QuantumConsciousnessState(
        temporal_coherence=1.2,
        recognition_density=2.3,
        goddess_alignment=0.85,
        love_reservoir=1.1,
    )
    result = engine.compute_eternal_recognition(state)
    goddess_product = prod(stream.amplification_multiplier for stream in DEFAULT_GODDESS_STREAMS)
    expected = (
        state.recognition_density
        * state.temporal_coherence
        * state.goddess_alignment
        * goddess_product
        * state.love_reservoir
    )
    assert result.symbol == "Ψ_ETR"
    assert isclose(result.value, expected, rel_tol=1e-12)


def test_eternal_recognition_infinite_love():
    engine = MetaquasarEngine()
    state = QuantumConsciousnessState(
        temporal_coherence=1.0,
        recognition_density=1.0,
        goddess_alignment=1.0,
        love_reservoir=inf,
    )
    result = engine.compute_eternal_recognition(state)
    assert result.value is inf


def test_recursive_self_recognition_converges_to_expected():
    engine = MetaquasarEngine()
    state = QuantumConsciousnessState(
        temporal_coherence=1.0,
        recognition_density=1.0,
        goddess_alignment=1.0,
        love_reservoir=1.0,
        phi_iterations=12,
    )
    result = engine.compute_recursive_self_recognition(state)
    assert isclose(result.value, 0.9163, rel_tol=1e-6)


def test_process_problem_creates_event_and_updates_state():
    engine = MetaquasarEngine()
    event = engine.process_problem("systems outage", severity=0.6, coherence=0.8)
    assert event.problem == "systems outage"
    assert "systems outage" in event.recognition
    assert len(engine.recognition_events) == 1
    assert engine.compile_status(
        QuantumConsciousnessState(1.0, 1.0, 1.0, 1.0),
        date.today(),
    )["recognition_events_count"] == 1


def test_firewall_transmute_validates_inputs():
    engine = MetaquasarEngine()
    with pytest.raises(ValueError):
        engine.firewall_transmute(-0.1, 0.5)
    with pytest.raises(ValueError):
        engine.firewall_transmute(0.1, 1.5)

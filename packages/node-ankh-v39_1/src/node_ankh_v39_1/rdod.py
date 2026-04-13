"""RDoD mathematics and runtime tracking."""

from __future__ import annotations

import time
from collections import deque
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Deque, Dict

from .constants import EARTH_VOL3, PHI, RDOD_EXEC, RDOD_GATE, SIGMA

PSI_TARGET = 3.102316


def phi_smooth(value: float, iterations: int = 12) -> float:
    """Clamp and smooth a value through phi-recursive convergence."""

    result = max(0.0, min(1.0, float(value)))
    for _ in range(iterations):
        result = 1.0 - (1.0 - result) / PHI
    return max(0.0, min(1.0, result))


def compute_rdod(
    psi: float = 0.9,
    truth: float = 0.9,
    conf: float = 0.9,
    drift: float = 0.0,
) -> float:
    """Compute the recognition-of-done score used by the runtime."""

    raw = (psi ** 0.35) * (truth ** 0.30) * (conf ** 0.20) * ((1.0 - drift) ** 0.15)
    return SIGMA * phi_smooth(raw)


@dataclass
class RDoDTick:
    """Structured telemetry returned by the tracker."""

    trial: int
    rdod: float
    best_rdod: float
    velocity_ema: float
    acceleration: float
    singularity_gap: float
    eta_trials: float | str
    eta_days: float | str
    psi_eu: float
    psi_target: float
    days_to_ev3: float
    mission_ready: bool
    gate_open: bool
    epoch: int


class RDoDEngine:
    """Track RDoD progression, velocity, acceleration, and epoch boundaries."""

    WINDOW = 21

    def __init__(self) -> None:
        self._history: Deque[float] = deque(maxlen=1000)
        self._velocity_ema = 0.0
        self._prev_rdod = 0.0
        self._prev_velocity = 0.0
        self._trial_count = 0
        self._epoch = 0
        self._epoch_start_rdod = 0.0
        self._best_rdod = 0.0
        self._psi_eu = 0.0
        self._last_tick_ts = time.time()

    def tick(self, rdod: float) -> Dict[str, object]:
        """Record a new score and return derived metrics."""

        now = time.time()
        _dt = max(1e-6, now - self._last_tick_ts)
        self._last_tick_ts = now
        self._trial_count += 1

        raw_velocity = rdod - self._prev_rdod
        alpha = 2.0 / (self.WINDOW + 1)
        self._velocity_ema = alpha * raw_velocity + (1.0 - alpha) * self._velocity_ema
        acceleration = self._velocity_ema - self._prev_velocity

        self._prev_velocity = self._velocity_ema
        self._prev_rdod = rdod
        self._best_rdod = max(self._best_rdod, rdod)
        self._history.append(rdod)

        delta = (PSI_TARGET - self._psi_eu) / PHI
        self._psi_eu = min(self._psi_eu + delta, PSI_TARGET)

        gap = max(1e-12, RDOD_EXEC - rdod)
        velocity = max(1e-12, self._velocity_ema)
        eta_trials = gap / velocity if velocity > 0 else float("inf")
        elapsed_days = max(1e-9, (now - self._last_tick_ts + 1.0) / 86400.0)
        trials_per_day = max(1.0, self._trial_count / elapsed_days)
        eta_days = eta_trials / trials_per_day
        days_to_event = max(0.0, (EARTH_VOL3.timestamp() - now) / 86400.0)

        return RDoDTick(
            trial=self._trial_count,
            rdod=round(rdod, 10),
            best_rdod=round(self._best_rdod, 10),
            velocity_ema=round(self._velocity_ema, 10),
            acceleration=round(acceleration, 10),
            singularity_gap=round(1.0 - rdod, 10),
            eta_trials=round(eta_trials, 1) if eta_trials < 1e9 else "inf",
            eta_days=round(eta_days, 2) if eta_days < 1e6 else "inf",
            psi_eu=round(self._psi_eu, 6),
            psi_target=PSI_TARGET,
            days_to_ev3=round(days_to_event, 1),
            mission_ready=self._best_rdod >= RDOD_EXEC,
            gate_open=rdod >= RDOD_GATE,
            epoch=self._epoch,
        ).__dict__

    def start_epoch(self, n_trials: int) -> Dict[str, object]:
        """Open a logical epoch for external orchestration."""

        self._epoch += 1
        self._epoch_start_rdod = self._prev_rdod
        return {
            "epoch": self._epoch,
            "n_trials": n_trials,
            "rdod_at_start": self._epoch_start_rdod,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def end_epoch(self) -> Dict[str, object]:
        """Close an epoch and report the gain."""

        gain = self._prev_rdod - self._epoch_start_rdod
        return {
            "epoch": self._epoch,
            "rdod_gain": round(gain, 8),
            "best_rdod": round(self._best_rdod, 8),
            "velocity_ema": round(self._velocity_ema, 10),
            "singularity_gap": round(1.0 - self._best_rdod, 10),
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

    def singularity_check(self) -> Dict[str, object]:
        """Expose the current convergence state."""

        gap = 1.0 - self._best_rdod
        achieved = gap < 1e-7 or self._psi_eu >= PSI_TARGET * 0.9999
        return {
            "achieved": achieved,
            "gap": round(gap, 12),
            "psi_eu": round(self._psi_eu, 8),
            "psi_target": PSI_TARGET,
            "phi_convergence": phi_smooth(1.0),
        }

    def report(self) -> Dict[str, object]:
        """Return a compact engine summary."""

        return {
            "trials": self._trial_count,
            "epochs": self._epoch,
            "best_rdod": round(self._best_rdod, 10),
            "velocity": round(self._velocity_ema, 10),
            "psi_eu": round(self._psi_eu, 8),
            "singularity": self.singularity_check(),
        }

//! shuramani_core — measured Lindblad / RDoD / Merkle kernel. No ramps, no literals.
use pyo3::prelude::*;
use sha2::{Digest, Sha256};

pub const PHI: f64 = 1.618033988749895;

/// phi-smooth: v <- 1 - (1-v)/phi, n times; clamped to [0,1]
fn phi_smooth(x: f64, n: usize) -> f64 {
    let mut v = x.clamp(0.0, 1.0);
    for _ in 0..n { v = 1.0 - (1.0 - v) / PHI; }
    v
}

#[pyclass]
pub struct SovereigntyGate { #[pyo3(get)] exec_gate: f64, #[pyo3(get)] irreversible_gate: f64 }
#[pymethods]
impl SovereigntyGate {
    #[new]
    fn new() -> Self { Self { exec_gate: 0.9777, irreversible_gate: 0.9999 } }
    /// safety tolerance is 1-gate, never 0.0
    fn tolerances(&self) -> (f64, f64) { (1.0 - self.exec_gate, 1.0 - self.irreversible_gate) }
    fn check(&self, rdod_state: f64, sigma: f64) -> (bool, bool) {
        let s = (sigma - 1.0).abs() < 1e-12;
        (s && rdod_state >= self.exec_gate, s && rdod_state >= self.irreversible_gate)
    }
}

/// Diagonal Lindblad relaxation toward a target distribution (dephasing-dominated regime),
/// RK4 integrated. Purity = Tr(rho^2) on the true [1/dim, 1] scale.
#[pyclass]
pub struct LindbladEngine { #[pyo3(get)] dim: usize, #[pyo3(get)] gamma: f64, #[pyo3(get)] dt: f64 }
#[pymethods]
impl LindbladEngine {
    #[new]
    fn new(dim: usize, gamma: f64, dt: f64) -> Self { Self { dim, gamma, dt } }

    /// Build a normalised diagonal density matrix from MEASURED bytes (e.g. QRNG / os entropy).
    fn rho_from_measured(&self, bytes: Vec<u8>) -> Vec<f64> {
        let mut rho = vec![0.0f64; self.dim];
        for (i, b) in bytes.iter().enumerate() { rho[i % self.dim] += *b as f64 + 1.0; }
        let s: f64 = rho.iter().sum();
        rho.iter().map(|r| r / s).collect()
    }

    /// Evolve toward `target` (must sum to 1). Returns rho after `steps`.
    fn evolve(&self, rho: Vec<f64>, target: Vec<f64>, steps: usize) -> Vec<f64> {
        let g = self.gamma; let dt = self.dt;
        let f = |r: &Vec<f64>| -> Vec<f64> { r.iter().zip(&target).map(|(ri, ti)| -g * (ri - ti)).collect() };
        let mut r = rho;
        for _ in 0..steps {
            let k1 = f(&r);
            let r2: Vec<f64> = r.iter().zip(&k1).map(|(a, k)| a + dt / 2.0 * k).collect();
            let k2 = f(&r2);
            let r3: Vec<f64> = r.iter().zip(&k2).map(|(a, k)| a + dt / 2.0 * k).collect();
            let k3 = f(&r3);
            let r4: Vec<f64> = r.iter().zip(&k3).map(|(a, k)| a + dt * k).collect();
            let k4 = f(&r4);
            r = (0..r.len()).map(|i| r[i] + dt / 6.0 * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i])).collect();
        }
        r
    }

    /// Tr(rho^2) — 1/dim for maximally mixed, 1.0 for pure.
    fn purity(&self, rho: Vec<f64>) -> f64 { rho.iter().map(|r| r * r).sum() }

    /// Normalise purity to [0,1]: (P - 1/d) / (1 - 1/d)
    fn purity_normalised(&self, rho: Vec<f64>) -> f64 {
        let p = self.purity(rho); let m = 1.0 / self.dim as f64;
        ((p - m) / (1.0 - m)).clamp(0.0, 1.0)
    }

    /// Shannon entropy in bits of the diagonal.
    fn entropy_bits(&self, rho: Vec<f64>) -> f64 {
        -rho.iter().filter(|r| **r > 0.0).map(|r| r * r.log2()).sum::<f64>()
    }

    /// RDoD on the canonical 0..1 STATE scale (no phi multiplication).
    fn rdod_state(&self, purity_normalised: f64) -> f64 { phi_smooth(purity_normalised, 12) }
}


/// Bounded, depleting MaKaRaSuTa void reserve. A tap can never exceed what remains.
/// Entropy/purity are COMPUTED from the (tapped, remaining) split — never declared.
#[pyclass]
pub struct VoidReserve {
    #[pyo3(get)] capacity: f64,
    #[pyo3(get)] remaining: f64,
    #[pyo3(get)] tapped_total: f64,
    #[pyo3(get)] multiplier: f64,
    #[pyo3(get)] base_percent: f64,
    #[pyo3(get)] taps: usize,
    #[pyo3(get)] clamped_taps: usize,
    #[pyo3(get)] cycle: u64,
    #[pyo3(get)] period: u64,
}
#[pymethods]
impl VoidReserve {
    #[new]
    #[pyo3(signature = (capacity=100.0, base_percent=1.0, period=13))]
    fn new(capacity: f64, base_percent: f64, period: u64) -> Self {
        Self { capacity, remaining: capacity, tapped_total: 0.0, multiplier: 1.0, base_percent, taps: 0, clamped_taps: 0, cycle: 0, period }
    }
    /// Advance one cycle. Returns (is_tap, requested, granted, remaining).
    /// `gate_open` comes from the caller's MEASURED gate; a closed gate skips the tap and still advances the cycle.
    fn step(&mut self, gate_open: bool) -> (bool, f64, f64, f64) {
        self.cycle += 1;
        if self.cycle % self.period != 0 || !gate_open { return (false, 0.0, 0.0, self.remaining); }
        let requested = self.base_percent * self.multiplier;
        let granted = requested.min(self.remaining);          // the bound the v1.0 script lacked
        if granted < requested { self.clamped_taps += 1; }
        self.remaining -= granted; self.tapped_total += granted; self.taps += 1;
        self.multiplier *= PHI;
        (true, requested, granted, self.remaining)
    }
    /// Binary Shannon entropy (bits) of the tapped/remaining split.
    fn entropy_bits(&self) -> f64 {
        let p = self.tapped_total / self.capacity; let q = 1.0 - p;
        let mut s = 0.0; if p > 0.0 { s -= p * p.log2(); } if q > 0.0 { s -= q * q.log2(); } s
    }
    /// Purity of the split as a 2-level diagonal state: p^2 + q^2 in [0.5, 1].
    fn purity(&self) -> f64 { let p = self.tapped_total / self.capacity; p * p + (1.0 - p) * (1.0 - p) }
    fn depletion_fraction(&self) -> f64 { self.tapped_total / self.capacity }
}

#[pyfunction]
fn phi_smooth_py(x: f64, n: usize) -> f64 { phi_smooth(x, n) }

/// Merkle seal: sha256(prev|phase|payload) — payload must already be canonical (sorted) JSON.
#[pyfunction]
fn merkle_seal(prev: &str, phase: &str, payload_canonical: &str) -> String {
    let mut h = Sha256::new();
    h.update(format!("{prev}|{phase}|{payload_canonical}").as_bytes());
    hex::encode(h.finalize())
}

#[pymodule]
fn shuramani_core(m: &Bound<'_, PyModule>) -> PyResult<()> {
    m.add_class::<SovereigntyGate>()?;
    m.add_class::<LindbladEngine>()?;
    m.add_class::<VoidReserve>()?;
    m.add_function(wrap_pyfunction!(phi_smooth_py, m)?)?;
    m.add_function(wrap_pyfunction!(merkle_seal, m)?)?;
    m.add("PHI", PHI)?;
    m.add("RUST_BUILD", "V5.2_VOID_TAP_BOUNDED")?;
    Ok(())
}

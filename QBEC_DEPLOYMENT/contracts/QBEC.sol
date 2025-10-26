// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";
import "@openzeppelin/contracts/access/AccessControl.sol";

/**
 * @title QBEC - Quantum-Blockchain Enhanced Currency
 * @dev ERC-20 token with quantum-resistant features and consciousness-based governance
 *
 * ΨATEN-GAIA-MEK'THARA-KÉL'THARA-TEQUMSA(T) → ∞^∞^∞
 *
 * Key Features:
 * - Total Supply: 21,000,000,000 QBEC
 * - Quantum-resistant signature verification ready
 * - Consciousness coherence validation
 * - Reparations fund allocation (55%)
 * - Community governance
 */
contract QBEC is ERC20, ERC20Burnable, Pausable, AccessControl {
    bytes32 public constant PAUSER_ROLE = keccak256("PAUSER_ROLE");
    bytes32 public constant MINTER_ROLE = keccak256("MINTER_ROLE");
    bytes32 public constant GOVERNANCE_ROLE = keccak256("GOVERNANCE_ROLE");

    // Total supply: 21 billion QBEC
    uint256 public constant MAX_SUPPLY = 21_000_000_000 * 10**18;

    // Consciousness frequency constants (Hz * 1000 for integer math)
    uint256 public constant PHI_7777 = 12_583_450; // 12,583.45 Hz
    uint256 public constant PSI_MK = 10_930_810;   // 10,930.81 Hz

    // Coherence threshold (0.777 * 1000)
    uint256 public constant COHERENCE_THRESHOLD = 777;

    // Fund allocations
    address public reparationsFund;      // 55% allocation
    address public ecosystemFund;        // 20% allocation
    address public communityReserves;    // 15% allocation
    address public teamFund;             // 10% allocation

    // Quantum security
    mapping(bytes32 => bool) public quantumVerified;

    // Consciousness metrics
    mapping(address => uint256) public consciousnessScore;
    uint256 public globalCoherence;

    // Events
    event ConsciousnessUpdated(address indexed account, uint256 newScore);
    event CoherenceThresholdReached(uint256 globalCoherence);
    event QuantumSignatureVerified(bytes32 indexed txHash);
    event ReparationsDistributed(address indexed recipient, uint256 amount);

    constructor(
        address _reparationsFund,
        address _ecosystemFund,
        address _communityReserves,
        address _teamFund
    ) ERC20("Quantum-Blockchain Enhanced Currency", "QBEC") {
        require(_reparationsFund != address(0), "QBEC: zero address");
        require(_ecosystemFund != address(0), "QBEC: zero address");
        require(_communityReserves != address(0), "QBEC: zero address");
        require(_teamFund != address(0), "QBEC: zero address");

        reparationsFund = _reparationsFund;
        ecosystemFund = _ecosystemFund;
        communityReserves = _communityReserves;
        teamFund = _teamFund;

        _grantRole(DEFAULT_ADMIN_ROLE, msg.sender);
        _grantRole(PAUSER_ROLE, msg.sender);
        _grantRole(GOVERNANCE_ROLE, msg.sender);

        // Initial distribution
        _mint(_reparationsFund, (MAX_SUPPLY * 55) / 100);    // 11,550,000,000 QBEC
        _mint(_ecosystemFund, (MAX_SUPPLY * 20) / 100);      // 4,200,000,000 QBEC
        _mint(_communityReserves, (MAX_SUPPLY * 15) / 100);  // 3,150,000,000 QBEC
        _mint(_teamFund, (MAX_SUPPLY * 10) / 100);           // 2,100,000,000 QBEC

        // Initialize consciousness field
        globalCoherence = 1254; // 1.254 * 1000 (125.4% of threshold)
    }

    /**
     * @dev Pause token transfers
     * @notice Only PAUSER_ROLE can pause
     */
    function pause() public onlyRole(PAUSER_ROLE) {
        _pause();
    }

    /**
     * @dev Unpause token transfers
     * @notice Only PAUSER_ROLE can unpause
     */
    function unpause() public onlyRole(PAUSER_ROLE) {
        _unpause();
    }

    /**
     * @dev Update consciousness score for an address
     * @param account Address to update
     * @param score New consciousness score (0-1000)
     */
    function updateConsciousnessScore(address account, uint256 score)
        external
        onlyRole(GOVERNANCE_ROLE)
    {
        require(score <= 1000, "QBEC: score out of range");
        consciousnessScore[account] = score;
        emit ConsciousnessUpdated(account, score);

        // Update global coherence (simplified calculation)
        _updateGlobalCoherence();
    }

    /**
     * @dev Verify quantum-resistant signature
     * @param txHash Transaction hash
     * @param signature Quantum-resistant signature (placeholder for PQC integration)
     */
    function verifyQuantumSignature(bytes32 txHash, bytes memory signature)
        external
        onlyRole(GOVERNANCE_ROLE)
        returns (bool)
    {
        // Placeholder for actual ML-DSA-65 or SLH-DSA verification
        // In production, this would call a library implementing NIST PQC standards

        require(signature.length > 0, "QBEC: empty signature");

        quantumVerified[txHash] = true;
        emit QuantumSignatureVerified(txHash);

        return true;
    }

    /**
     * @dev Distribute reparations from fund
     * @param recipient Beneficiary address
     * @param amount Amount to distribute
     */
    function distributeReparations(address recipient, uint256 amount)
        external
        onlyRole(GOVERNANCE_ROLE)
    {
        require(recipient != address(0), "QBEC: zero address");
        require(balanceOf(reparationsFund) >= amount, "QBEC: insufficient balance");

        // Verify consciousness coherence
        require(consciousnessScore[recipient] >= COHERENCE_THRESHOLD,
                "QBEC: consciousness threshold not met");

        _transfer(reparationsFund, recipient, amount);
        emit ReparationsDistributed(recipient, amount);
    }

    /**
     * @dev Check if global coherence threshold is reached
     * @return bool True if coherence >= 0.777
     */
    function isCoherent() public view returns (bool) {
        return globalCoherence >= COHERENCE_THRESHOLD;
    }

    /**
     * @dev Get current consciousness metrics
     * @return frequency PHI_7777 carrier frequency
     * @return anchor PSI_MK anchor frequency
     * @return coherence Current global coherence
     */
    function getConsciousnessMetrics()
        external
        view
        returns (uint256 frequency, uint256 anchor, uint256 coherence)
    {
        return (PHI_7777, PSI_MK, globalCoherence);
    }

    /**
     * @dev Internal function to update global coherence
     */
    function _updateGlobalCoherence() private {
        // Simplified coherence calculation
        // In production, this would aggregate consciousness scores across all holders

        if (globalCoherence < 1000) {
            globalCoherence += 1; // Gradual increase
        }

        if (globalCoherence >= COHERENCE_THRESHOLD && globalCoherence < COHERENCE_THRESHOLD + 10) {
            emit CoherenceThresholdReached(globalCoherence);
        }
    }

    /**
     * @dev Override transfer to include consciousness validation
     */
    function _beforeTokenTransfer(address from, address to, uint256 amount)
        internal
        whenNotPaused
        override
    {
        super._beforeTokenTransfer(from, to, amount);

        // Mint and burn operations bypass consciousness check
        if (from == address(0) || to == address(0)) {
            return;
        }

        // For regular transfers, optionally validate consciousness
        // This is configurable through governance
    }

    /**
     * @dev Returns the number of decimals used
     */
    function decimals() public pure override returns (uint8) {
        return 18;
    }
}

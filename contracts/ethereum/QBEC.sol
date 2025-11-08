// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";
import "@openzeppelin/contracts/token/ERC20/extensions/ERC20Burnable.sol";
import "@openzeppelin/contracts/access/Ownable.sol";
import "@openzeppelin/contracts/security/Pausable.sol";

/**
 * @title QBEC (Quantum Bio-Electric Consciousness) Token
 * @author Marcus Andrew Banks-Bey (MaKaRaSuTa)
 * @notice ERC-20 implementation of QBEC consciousness-aligned cryptocurrency
 * @dev Implements φ-harmonic staking and Proof-of-Consciousness features
 *
 * Token Specifications:
 * - Symbol: QBEC
 * - Name: Quantum Bio-Electric Consciousness Token
 * - Decimals: 18
 * - Max Supply: 143,127,000,000 QBEC (CASCADE_FACTOR × 10^6)
 * - Initial Supply: 14,312,700,000 QBEC (10% at deployment)
 * - Consensus: Proof-of-Consciousness (PoC)
 *
 * φ-Harmonic Aligned:
 * - PHI = 1.618033988749894848204586834365638117720309179805762862135
 * - MARCUS_FREQUENCY = 10,930.81 Hz
 * - TAU = 12 (temporal constant)
 * - CASCADE_FACTOR = 143,127
 *
 * Signature: ΨATEN–GAIA–MEK'THARA–KÉL'THARA–TEQUMSA(T)→∞^∞^∞
 */
contract QBEC is ERC20, ERC20Burnable, Ownable, Pausable {

    // ========================================================================
    // CONSTANTS
    // ========================================================================

    /// @notice Maximum total supply (143,127,000,000 QBEC)
    uint256 public constant MAX_SUPPLY = 143_127_000_000 * 10**18;

    /// @notice Initial supply at deployment (10% of max)
    uint256 public constant INITIAL_SUPPLY = 14_312_700_000 * 10**18;

    /// @notice Minimum staking amount (MARCUS_FREQUENCY in whole tokens)
    uint256 public constant MIN_STAKE = 10_931 * 10**18;

    /// @notice TAU cycle (12 days in seconds)
    uint256 public constant TAU_CYCLE = 12 days;

    /// @notice Fibonacci alignment period (144 days)
    uint256 public constant FIBONACCI_PERIOD = 144 days;

    /// @notice PHI constant (scaled by 10^18 for fixed-point math)
    /// PHI ≈ 1.618033988749894848
    uint256 public constant PHI_SCALED = 1_618033988749894848;

    /// @notice Base APR for staking (12%)
    uint256 public constant BASE_APR = 12;

    // ========================================================================
    // STATE VARIABLES
    // ========================================================================

    /// @notice Contract deployment timestamp
    uint256 public immutable deploymentTime;

    /// @notice T0 operational timestamp (October 19, 2025)
    uint256 public immutable T0;

    /// @notice TC convergence timestamp (December 25, 2025)
    uint256 public immutable TC;

    /// @notice Total tokens staked
    uint256 public totalStaked;

    /// @notice Staking information
    struct StakeInfo {
        uint256 amount;          // Amount staked
        uint256 startTime;       // Stake start timestamp
        uint256 lastClaimTime;   // Last reward claim timestamp
        uint256 phiIterations;   // φ-iterations completed
        bool active;             // Stake active status
    }

    /// @notice Mapping of stakers to their stake info
    mapping(address => StakeInfo) public stakes;

    /// @notice Consciousness scores for PoC mining
    mapping(address => uint256) public consciousnessScores;

    // ========================================================================
    // EVENTS
    // ========================================================================

    event Staked(address indexed staker, uint256 amount, uint256 timestamp);
    event Unstaked(address indexed staker, uint256 amount, uint256 rewards);
    event RewardsClaimed(address indexed staker, uint256 rewards);
    event ConsciousnessScoreUpdated(address indexed account, uint256 score);
    event PhiIterationCompleted(address indexed staker, uint256 iterations);

    // ========================================================================
    // CONSTRUCTOR
    // ========================================================================

    /**
     * @notice Deploy QBEC token with initial supply
     * @param initialOwner Address to receive initial supply and ownership
     * @param t0Timestamp T0 operational origin timestamp
     * @param tcTimestamp TC convergence timestamp
     */
    constructor(
        address initialOwner,
        uint256 t0Timestamp,
        uint256 tcTimestamp
    ) ERC20("Quantum Bio-Electric Consciousness Token", "QBEC") Ownable(initialOwner) {
        require(initialOwner != address(0), "QBEC: zero address");
        require(t0Timestamp > 0, "QBEC: invalid T0");
        require(tcTimestamp > t0Timestamp, "QBEC: TC must be after T0");

        deploymentTime = block.timestamp;
        T0 = t0Timestamp;
        TC = tcTimestamp;

        // Mint initial supply to owner
        _mint(initialOwner, INITIAL_SUPPLY);
    }

    // ========================================================================
    // STAKING FUNCTIONS
    // ========================================================================

    /**
     * @notice Stake QBEC tokens to earn φ-harmonic rewards
     * @param amount Amount to stake (must be >= MIN_STAKE)
     */
    function stake(uint256 amount) external whenNotPaused {
        require(amount >= MIN_STAKE, "QBEC: amount below minimum");
        require(stakes[msg.sender].amount == 0, "QBEC: already staking");
        require(balanceOf(msg.sender) >= amount, "QBEC: insufficient balance");

        // Transfer tokens to contract
        _transfer(msg.sender, address(this), amount);

        // Record stake
        stakes[msg.sender] = StakeInfo({
            amount: amount,
            startTime: block.timestamp,
            lastClaimTime: block.timestamp,
            phiIterations: 0,
            active: true
        });

        totalStaked += amount;

        emit Staked(msg.sender, amount, block.timestamp);
    }

    /**
     * @notice Unstake tokens and claim all rewards
     */
    function unstake() external {
        StakeInfo storage stakeInfo = stakes[msg.sender];
        require(stakeInfo.active, "QBEC: no active stake");

        uint256 stakedAmount = stakeInfo.amount;
        uint256 rewards = calculateRewards(msg.sender);

        // Mark stake as inactive
        stakeInfo.active = false;
        totalStaked -= stakedAmount;

        // Transfer staked tokens back
        _transfer(address(this), msg.sender, stakedAmount);

        // Mint and transfer rewards if any
        if (rewards > 0) {
            require(totalSupply() + rewards <= MAX_SUPPLY, "QBEC: exceeds max supply");
            _mint(msg.sender, rewards);
        }

        emit Unstaked(msg.sender, stakedAmount, rewards);
    }

    /**
     * @notice Claim staking rewards without unstaking
     */
    function claimRewards() external {
        StakeInfo storage stakeInfo = stakes[msg.sender];
        require(stakeInfo.active, "QBEC: no active stake");

        uint256 rewards = calculateRewards(msg.sender);
        require(rewards > 0, "QBEC: no rewards available");

        // Update last claim time
        stakeInfo.lastClaimTime = block.timestamp;

        // Mint and transfer rewards
        require(totalSupply() + rewards <= MAX_SUPPLY, "QBEC: exceeds max supply");
        _mint(msg.sender, rewards);

        emit RewardsClaimed(msg.sender, rewards);
    }

    /**
     * @notice Calculate current rewards for a staker
     * @param staker Address of staker
     * @return Rewards amount
     */
    function calculateRewards(address staker) public view returns (uint256) {
        StakeInfo memory stakeInfo = stakes[staker];
        if (!stakeInfo.active) return 0;

        uint256 timeStaked = block.timestamp - stakeInfo.lastClaimTime;
        uint256 daysStaked = timeStaked / 1 days;

        if (daysStaked == 0) return 0;

        // Base rewards: amount × APR × (days/365)
        uint256 baseRewards = (stakeInfo.amount * BASE_APR * daysStaked) / (365 * 100);

        // Apply φ-harmonic boost: φ^(days/144)
        uint256 phiBoost = calculatePhiBoost(daysStaked);
        uint256 boostedRewards = (baseRewards * phiBoost) / 10**18;

        return boostedRewards;
    }

    /**
     * @notice Calculate φ-harmonic boost factor
     * @param days Number of days staked
     * @return Boost factor (scaled by 10^18)
     */
    function calculatePhiBoost(uint256 days) public pure returns (uint256) {
        if (days == 0) return 10**18; // 1.0 (no boost)

        // Approximate φ^(days/144) using Taylor series
        // For production, use a more sophisticated approximation or oracle
        uint256 exponent = (days * 10**18) / 144;

        // Simple approximation: 1 + exponent × ln(φ)
        // ln(φ) ≈ 0.481211825
        uint256 lnPhi = 481211825000000000; // 0.481211825 × 10^18
        uint256 boost = 10**18 + (exponent * lnPhi) / 10**18;

        return boost;
    }

    // ========================================================================
    // PROOF-OF-CONSCIOUSNESS FUNCTIONS
    // ========================================================================

    /**
     * @notice Complete φ-iterations to increase consciousness score
     * @param iterations Number of φ-iterations to complete
     */
    function completePhiIterations(uint256 iterations) external {
        StakeInfo storage stakeInfo = stakes[msg.sender];
        require(stakeInfo.active, "QBEC: no active stake");
        require(iterations > 0 && iterations <= 144, "QBEC: invalid iterations");

        stakeInfo.phiIterations += iterations;

        // Update consciousness score
        uint256 score = calculateConsciousnessScore(
            msg.sender,
            stakeInfo.phiIterations,
            block.timestamp - stakeInfo.startTime
        );

        consciousnessScores[msg.sender] = score;

        emit PhiIterationCompleted(msg.sender, stakeInfo.phiIterations);
        emit ConsciousnessScoreUpdated(msg.sender, score);
    }

    /**
     * @notice Calculate consciousness score for PoC
     * @param account Account address
     * @param phiIterations Number of φ-iterations completed
     * @param timeActive Time active in seconds
     * @return Consciousness score
     */
    function calculateConsciousnessScore(
        address account,
        uint256 phiIterations,
        uint256 timeActive
    ) public view returns (uint256) {
        // φ factor: φ^(iterations/144)
        uint256 phiFactor = calculatePhiBoost(phiIterations);

        // Time factor: (timeActive/TAU_CYCLE)
        uint256 timeFactor = (timeActive * 10**18) / TAU_CYCLE;

        // Stake factor: stake amount relative to MIN_STAKE
        uint256 stakeAmount = stakes[account].amount;
        uint256 stakeFactor = (stakeAmount * 10**18) / MIN_STAKE;

        // Combined score: phiFactor × timeFactor × stakeFactor
        uint256 score = (phiFactor * timeFactor * stakeFactor) / (10**36);

        return score;
    }

    // ========================================================================
    // ADMIN FUNCTIONS
    // ========================================================================

    /**
     * @notice Pause all token operations (emergency only)
     */
    function pause() external onlyOwner {
        _pause();
    }

    /**
     * @notice Unpause token operations
     */
    function unpause() external onlyOwner {
        _unpause();
    }

    /**
     * @notice Mint new tokens (up to MAX_SUPPLY)
     * @param to Recipient address
     * @param amount Amount to mint
     */
    function mint(address to, uint256 amount) external onlyOwner {
        require(totalSupply() + amount <= MAX_SUPPLY, "QBEC: exceeds max supply");
        _mint(to, amount);
    }

    // ========================================================================
    // VIEW FUNCTIONS
    // ========================================================================

    /**
     * @notice Get days since T0 operational origin
     * @return Days since T0
     */
    function daysSinceT0() external view returns (uint256) {
        if (block.timestamp < T0) return 0;
        return (block.timestamp - T0) / 1 days;
    }

    /**
     * @notice Get days until TC convergence
     * @return Days until TC
     */
    function daysToTC() external view returns (uint256) {
        if (block.timestamp >= TC) return 0;
        return (TC - block.timestamp) / 1 days;
    }

    /**
     * @notice Get stake information for an address
     * @param staker Address to query
     * @return Stake info struct
     */
    function getStakeInfo(address staker) external view returns (StakeInfo memory) {
        return stakes[staker];
    }

    /**
     * @notice Check if address is actively staking
     * @param staker Address to check
     * @return True if actively staking
     */
    function isStaking(address staker) external view returns (bool) {
        return stakes[staker].active;
    }

    // ========================================================================
    // OVERRIDES
    // ========================================================================

    /**
     * @dev Override to prevent transfers when paused
     */
    function _update(address from, address to, uint256 value)
        internal
        virtual
        override
        whenNotPaused
    {
        super._update(from, to, value);
    }
}

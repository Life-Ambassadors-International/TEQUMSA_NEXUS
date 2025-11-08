/**
 * Hardhat Configuration for QBEC Token Deployment
 * ================================================
 *
 * Testnet Configuration:
 * - Sepolia (Ethereum testnet)
 * - BSC Testnet
 * - Polygon Mumbai
 * - Arbitrum Sepolia
 * - Optimism Sepolia
 *
 * Author: Marcus Andrew Banks-Bey (MaKaRaSuTa)
 */

require("@nomicfoundation/hardhat-toolbox");
require("dotenv").config();

// T0 and TC timestamps
const T0_TIMESTAMP = Math.floor(new Date('2025-10-19T00:00:00Z').getTime() / 1000);
const TC_TIMESTAMP = Math.floor(new Date('2025-12-25T00:00:00Z').getTime() / 1000);

module.exports = {
  solidity: {
    version: "0.8.20",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },

  networks: {
    // Local development
    hardhat: {
      chainId: 31337
    },

    // Ethereum Sepolia testnet
    sepolia: {
      url: process.env.SEPOLIA_RPC_URL || "https://rpc.sepolia.org",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
      chainId: 11155111
    },

    // BSC Testnet
    bscTestnet: {
      url: "https://data-seed-prebsc-1-s1.binance.org:8545",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
      chainId: 97
    },

    // Polygon Mumbai testnet
    mumbai: {
      url: "https://rpc-mumbai.maticvigil.com",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
      chainId: 80001
    },

    // Arbitrum Sepolia
    arbitrumSepolia: {
      url: "https://sepolia-rollup.arbitrum.io/rpc",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
      chainId: 421614
    },

    // Optimism Sepolia
    optimismSepolia: {
      url: "https://sepolia.optimism.io",
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
      chainId: 11155420
    }
  },

  etherscan: {
    apiKey: {
      sepolia: process.env.ETHERSCAN_API_KEY || "",
      bscTestnet: process.env.BSCSCAN_API_KEY || "",
      polygonMumbai: process.env.POLYGONSCAN_API_KEY || "",
      arbitrumSepolia: process.env.ARBISCAN_API_KEY || "",
      optimismSepolia: process.env.OPTIMISTIC_ETHERSCAN_API_KEY || ""
    }
  },

  paths: {
    sources: "./",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  },

  // Custom deployment parameters
  qbec: {
    t0: T0_TIMESTAMP,
    tc: TC_TIMESTAMP,
    initialSupply: "14312700000000000000000000000", // 14.3B with 18 decimals
    maxSupply: "143127000000000000000000000000"     // 143.1B with 18 decimals
  }
};

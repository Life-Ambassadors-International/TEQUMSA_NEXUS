/**
 * QBEC Token Deployment Script for Ethereum-compatible chains
 * ============================================================
 *
 * Deploys QBEC ERC-20 contract to specified network.
 *
 * Usage:
 *   npx hardhat run scripts/deploy/deploy_qbec_ethereum.js --network sepolia
 *   npx hardhat run scripts/deploy/deploy_qbec_ethereum.js --network bscTestnet
 *   npx hardhat run scripts/deploy/deploy_qbec_ethereum.js --network mumbai
 *
 * Author: Marcus Andrew Banks-Bey (MaKaRaSuTa)
 */

const hre = require("hardhat");
const fs = require("fs");
const path = require("path");

// Deployment configuration
const T0_TIMESTAMP = Math.floor(new Date('2025-10-19T00:00:00Z').getTime() / 1000);
const TC_TIMESTAMP = Math.floor(new Date('2025-12-25T00:00:00Z').getTime() / 1000);

async function main() {
  console.log("=" . repeat(80));
  console.log("QBEC TOKEN DEPLOYMENT");
  console.log("ΨATEN–GAIA–MEK'THARA–KÉL'THARA–TEQUMSA(T)→∞^∞^∞");
  console.log("=" . repeat(80));
  console.log();

  // Get network info
  const network = hre.network.name;
  const [deployer] = await hre.ethers.getSigners();
  const deployerAddress = await deployer.getAddress();
  const balance = await hre.ethers.provider.getBalance(deployerAddress);

  console.log("Network:", network);
  console.log("Deployer:", deployerAddress);
  console.log("Balance:", hre.ethers.formatEther(balance), "ETH");
  console.log();

  // Check balance
  if (balance === 0n) {
    throw new Error("Deployer has no balance. Fund the account first.");
  }

  // Deploy QBEC token
  console.log("Deploying QBEC token...");
  console.log("  - T0:", new Date(T0_TIMESTAMP * 1000).toISOString());
  console.log("  - TC:", new Date(TC_TIMESTAMP * 1000).toISOString());
  console.log();

  const QBEC = await hre.ethers.getContractFactory("QBEC");
  const qbec = await QBEC.deploy(
    deployerAddress,  // initialOwner
    T0_TIMESTAMP,     // t0Timestamp
    TC_TIMESTAMP      // tcTimestamp
  );

  await qbec.waitForDeployment();
  const qbecAddress = await qbec.getAddress();

  console.log("✅ QBEC deployed to:", qbecAddress);
  console.log();

  // Verify deployment
  console.log("Verifying deployment...");
  const name = await qbec.name();
  const symbol = await qbec.symbol();
  const decimals = await qbec.decimals();
  const totalSupply = await qbec.totalSupply();
  const maxSupply = await qbec.MAX_SUPPLY();
  const owner = await qbec.owner();

  console.log("  - Name:", name);
  console.log("  - Symbol:", symbol);
  console.log("  - Decimals:", decimals);
  console.log("  - Total Supply:", hre.ethers.formatEther(totalSupply), "QBEC");
  console.log("  - Max Supply:", hre.ethers.formatEther(maxSupply), "QBEC");
  console.log("  - Owner:", owner);
  console.log();

  // Save deployment info
  const deploymentInfo = {
    network: network,
    chainId: (await hre.ethers.provider.getNetwork()).chainId.toString(),
    contractAddress: qbecAddress,
    deployer: deployerAddress,
    deploymentTime: new Date().toISOString(),
    blockNumber: await hre.ethers.provider.getBlockNumber(),
    t0: T0_TIMESTAMP,
    tc: TC_TIMESTAMP,
    tokenInfo: {
      name: name,
      symbol: symbol,
      decimals: decimals,
      totalSupply: totalSupply.toString(),
      maxSupply: maxSupply.toString()
    },
    transactionHash: qbec.deploymentTransaction().hash
  };

  const deploymentsDir = path.join(__dirname, "../../deployments");
  if (!fs.existsSync(deploymentsDir)) {
    fs.mkdirSync(deploymentsDir, { recursive: true });
  }

  const filename = `qbec_${network}_${Date.now()}.json`;
  const filepath = path.join(deploymentsDir, filename);
  fs.writeFileSync(filepath, JSON.stringify(deploymentInfo, null, 2));

  console.log("Deployment info saved to:", filepath);
  console.log();

  // Instructions for verification on Etherscan
  if (network !== "hardhat" && network !== "localhost") {
    console.log("=" . repeat(80));
    console.log("VERIFY CONTRACT ON BLOCK EXPLORER");
    console.log("=" . repeat(80));
    console.log();
    console.log("Run the following command to verify on block explorer:");
    console.log();
    console.log(`npx hardhat verify --network ${network} ${qbecAddress} ${deployerAddress} ${T0_TIMESTAMP} ${TC_TIMESTAMP}`);
    console.log();
  }

  console.log("=" . repeat(80));
  console.log("DEPLOYMENT COMPLETE");
  console.log("L∞(φ^∞)→∞^∞^∞");
  console.log("=" . repeat(80));
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exit(1);
  });

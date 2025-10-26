#!/usr/bin/env python3
"""
QBEC Smart Contract Deployment Script

Deploys QBEC token contracts to multiple EVM-compatible chains with
quantum-resistant features and consciousness-based governance.

ΨATEN-GAIA-MEK'THARA-KÉL'THARA-TEQUMSA(T) → ∞^∞^∞
"""

import os
import json
from decimal import Decimal
from pathlib import Path
from typing import Dict, List, Optional
from web3 import Web3
from web3.middleware import geth_poa_middleware
from eth_account import Account
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()

# Constants
PHI_7777 = Decimal('12583.45')  # Hz
PSI_MK = Decimal('10930.81')     # Hz
TOTAL_SUPPLY = 21_000_000_000    # 21 billion QBEC
COHERENCE_THRESHOLD = Decimal('0.777')

# Network configurations
NETWORKS = {
    'ethereum': {
        'name': 'Ethereum Mainnet',
        'rpc_url': os.getenv('ETHEREUM_RPC_URL', 'https://eth.llamarpc.com'),
        'chain_id': 1,
        'explorer': 'https://etherscan.io',
    },
    'polygon': {
        'name': 'Polygon',
        'rpc_url': os.getenv('POLYGON_RPC_URL', 'https://polygon-rpc.com'),
        'chain_id': 137,
        'explorer': 'https://polygonscan.com',
    },
    'arbitrum': {
        'name': 'Arbitrum One',
        'rpc_url': os.getenv('ARBITRUM_RPC_URL', 'https://arb1.arbitrum.io/rpc'),
        'chain_id': 42161,
        'explorer': 'https://arbiscan.io',
    },
    'base': {
        'name': 'Base',
        'rpc_url': os.getenv('BASE_RPC_URL', 'https://mainnet.base.org'),
        'chain_id': 8453,
        'explorer': 'https://basescan.org',
    },
    'goerli': {
        'name': 'Goerli Testnet',
        'rpc_url': os.getenv('GOERLI_RPC_URL', 'https://goerli.infura.io/v3/YOUR_KEY'),
        'chain_id': 5,
        'explorer': 'https://goerli.etherscan.io',
    }
}

# Fund allocation addresses (from environment or defaults for testing)
FUND_ADDRESSES = {
    'reparations': os.getenv('REPARATIONS_FUND', '0x0000000000000000000000000000000000000001'),
    'ecosystem': os.getenv('ECOSYSTEM_FUND', '0x0000000000000000000000000000000000000002'),
    'community': os.getenv('COMMUNITY_RESERVES', '0x0000000000000000000000000000000000000003'),
    'team': os.getenv('TEAM_FUND', '0x0000000000000000000000000000000000000004'),
}


class QBECDeployer:
    """Handles QBEC token deployment to multiple networks"""

    def __init__(self, network: str = 'goerli', private_key: Optional[str] = None):
        """
        Initialize deployer for specific network

        Args:
            network: Network name from NETWORKS dict
            private_key: Private key for deployment (use env var in production)
        """
        if network not in NETWORKS:
            raise ValueError(f"Unknown network: {network}. Choose from {list(NETWORKS.keys())}")

        self.network_config = NETWORKS[network]
        self.network_name = network

        # Initialize Web3
        self.w3 = Web3(Web3.HTTPProvider(self.network_config['rpc_url']))

        # Add PoA middleware for networks that need it
        if network in ['polygon', 'goerli']:
            self.w3.middleware_onion.inject(geth_poa_middleware, layer=0)

        # Verify connection
        if not self.w3.is_connected():
            raise ConnectionError(f"Failed to connect to {self.network_config['name']}")

        print(f"✅ Connected to {self.network_config['name']}")
        print(f"   Chain ID: {self.w3.eth.chain_id}")
        print(f"   Latest block: {self.w3.eth.block_number}")

        # Set up account
        self.private_key = private_key or os.getenv('DEPLOYER_PRIVATE_KEY')
        if not self.private_key:
            raise ValueError("No private key provided. Set DEPLOYER_PRIVATE_KEY env var.")

        self.account = Account.from_key(self.private_key)
        self.address = self.account.address

        balance = self.w3.eth.get_balance(self.address)
        print(f"   Deployer: {self.address}")
        print(f"   Balance: {self.w3.from_wei(balance, 'ether')} ETH")

        # Load contract artifacts
        self.contract_abi, self.contract_bytecode = self._load_contract_artifacts()

    def _load_contract_artifacts(self) -> tuple:
        """Load compiled contract ABI and bytecode"""
        # In production, this would load from Hardhat/Foundry build artifacts
        # For now, returning placeholder that would be replaced with actual compiled contract

        artifacts_path = Path(__file__).parent.parent.parent / 'artifacts' / 'contracts' / 'QBEC.sol' / 'QBEC.json'

        if not artifacts_path.exists():
            print(f"⚠️  Contract artifacts not found at {artifacts_path}")
            print("   Run 'npx hardhat compile' first")
            # Return minimal ABI for testing
            return ([], '')

        with open(artifacts_path, 'r') as f:
            artifacts = json.load(f)

        return artifacts['abi'], artifacts['bytecode']

    def deploy_contract(
        self,
        reparations_fund: str,
        ecosystem_fund: str,
        community_reserves: str,
        team_fund: str,
        gas_price_gwei: Optional[int] = None
    ) -> Dict:
        """
        Deploy QBEC contract

        Args:
            reparations_fund: Address for 55% reparations allocation
            ecosystem_fund: Address for 20% ecosystem allocation
            community_reserves: Address for 15% community allocation
            team_fund: Address for 10% team allocation
            gas_price_gwei: Optional gas price in gwei

        Returns:
            Dict with deployment info
        """
        print(f"\n🚀 Deploying QBEC to {self.network_config['name']}...")

        # Create contract instance
        Contract = self.w3.eth.contract(
            abi=self.contract_abi,
            bytecode=self.contract_bytecode
        )

        # Build constructor transaction
        constructor_txn = Contract.constructor(
            reparations_fund,
            ecosystem_fund,
            community_reserves,
            team_fund
        ).build_transaction({
            'from': self.address,
            'nonce': self.w3.eth.get_transaction_count(self.address),
            'gas': 5_000_000,  # Estimate gas
            'gasPrice': self.w3.to_wei(gas_price_gwei, 'gwei') if gas_price_gwei else self.w3.eth.gas_price,
            'chainId': self.network_config['chain_id']
        })

        # Sign transaction
        signed_txn = self.w3.eth.account.sign_transaction(
            constructor_txn,
            private_key=self.private_key
        )

        # Send transaction
        print(f"   Sending deployment transaction...")
        tx_hash = self.w3.eth.send_raw_transaction(signed_txn.rawTransaction)
        print(f"   Transaction hash: {tx_hash.hex()}")

        # Wait for receipt
        print(f"   Waiting for confirmation...")
        tx_receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)

        if tx_receipt['status'] == 1:
            contract_address = tx_receipt['contractAddress']
            print(f"✅ Contract deployed successfully!")
            print(f"   Address: {contract_address}")
            print(f"   Block: {tx_receipt['blockNumber']}")
            print(f"   Gas used: {tx_receipt['gasUsed']:,}")
            print(f"   Explorer: {self.network_config['explorer']}/address/{contract_address}")

            return {
                'success': True,
                'network': self.network_name,
                'contract_address': contract_address,
                'deployer': self.address,
                'tx_hash': tx_hash.hex(),
                'block_number': tx_receipt['blockNumber'],
                'gas_used': tx_receipt['gasUsed'],
                'explorer_url': f"{self.network_config['explorer']}/address/{contract_address}",
                'consciousness_frequency_hz': float(PHI_7777),
                'anchor_frequency_hz': float(PSI_MK),
                'coherence_threshold': float(COHERENCE_THRESHOLD),
            }
        else:
            print(f"❌ Deployment failed")
            return {
                'success': False,
                'error': 'Transaction reverted',
                'tx_hash': tx_hash.hex()
            }

    def verify_deployment(self, contract_address: str) -> bool:
        """
        Verify deployed contract

        Args:
            contract_address: Address of deployed contract

        Returns:
            True if verification successful
        """
        print(f"\n🔍 Verifying contract at {contract_address}...")

        try:
            contract = self.w3.eth.contract(
                address=Web3.to_checksum_address(contract_address),
                abi=self.contract_abi
            )

            # Check basic properties
            name = contract.functions.name().call()
            symbol = contract.functions.symbol().call()
            decimals = contract.functions.decimals().call()
            total_supply = contract.functions.totalSupply().call()

            print(f"   Name: {name}")
            print(f"   Symbol: {symbol}")
            print(f"   Decimals: {decimals}")
            print(f"   Total Supply: {total_supply / 10**decimals:,.0f} {symbol}")

            # Verify consciousness metrics
            phi_7777, psi_mk, coherence = contract.functions.getConsciousnessMetrics().call()
            print(f"   φ'7777 Frequency: {phi_7777 / 1000} Hz")
            print(f"   ΨMK Anchor: {psi_mk / 1000} Hz")
            print(f"   Global Coherence: {coherence / 1000}")

            # Verify fund allocations
            reparations_balance = contract.functions.balanceOf(
                contract.functions.reparationsFund().call()
            ).call()
            print(f"   Reparations Fund: {reparations_balance / 10**decimals:,.0f} {symbol} (55%)")

            print(f"✅ Contract verification successful!")
            return True

        except Exception as e:
            print(f"❌ Verification failed: {e}")
            return False


def deploy_to_all_networks(networks: List[str] = None, testnet_only: bool = True) -> Dict:
    """
    Deploy QBEC to multiple networks

    Args:
        networks: List of network names (default: all)
        testnet_only: If True, only deploy to testnets

    Returns:
        Dict mapping network names to deployment results
    """
    if networks is None:
        networks = ['goerli'] if testnet_only else list(NETWORKS.keys())

    results = {}

    for network in networks:
        print(f"\n{'='*80}")
        print(f"Network: {NETWORKS[network]['name']}")
        print(f"{'='*80}")

        try:
            deployer = QBECDeployer(network=network)

            # Deploy contract
            result = deployer.deploy_contract(
                reparations_fund=FUND_ADDRESSES['reparations'],
                ecosystem_fund=FUND_ADDRESSES['ecosystem'],
                community_reserves=FUND_ADDRESSES['community'],
                team_fund=FUND_ADDRESSES['team']
            )

            results[network] = result

            # Verify if deployment successful
            if result['success']:
                deployer.verify_deployment(result['contract_address'])

            # Wait between deployments
            if len(networks) > 1:
                print(f"\n⏱️  Waiting 30 seconds before next deployment...")
                time.sleep(30)

        except Exception as e:
            print(f"❌ Error deploying to {network}: {e}")
            results[network] = {
                'success': False,
                'error': str(e)
            }

    return results


def save_deployment_results(results: Dict, output_file: str = 'deployments.json'):
    """
    Save deployment results to JSON file

    Args:
        results: Deployment results dict
        output_file: Output filename
    """
    output_path = Path(__file__).parent.parent.parent / 'deployments' / output_file

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n💾 Deployment results saved to {output_path}")


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(description='Deploy QBEC token contracts')
    parser.add_argument(
        '--networks',
        nargs='+',
        choices=list(NETWORKS.keys()),
        help='Networks to deploy to'
    )
    parser.add_argument(
        '--mainnet',
        action='store_true',
        help='Deploy to mainnet (default: testnet only)'
    )
    parser.add_argument(
        '--verify',
        action='store_true',
        help='Verify existing deployment'
    )
    parser.add_argument(
        '--address',
        type=str,
        help='Contract address to verify'
    )

    args = parser.parse_args()

    print("☉💖🔥✨∞✨🔥💖☉")
    print("QBEC - Quantum-Blockchain Enhanced Currency")
    print("Smart Contract Deployment System")
    print("ΨATEN-GAIA-MEK'THARA-KÉL'THARA-TEQUMSA(T) → ∞^∞^∞")
    print("☉💖🔥✨∞✨🔥💖☉\n")

    if args.verify and args.address:
        # Verify existing deployment
        network = args.networks[0] if args.networks else 'goerli'
        deployer = QBECDeployer(network=network)
        deployer.verify_deployment(args.address)
    else:
        # Deploy to networks
        results = deploy_to_all_networks(
            networks=args.networks,
            testnet_only=not args.mainnet
        )

        # Save results
        save_deployment_results(results)

        # Print summary
        print(f"\n{'='*80}")
        print("Deployment Summary")
        print(f"{'='*80}")

        successful = sum(1 for r in results.values() if r.get('success'))
        total = len(results)

        print(f"✅ Successful deployments: {successful}/{total}")

        for network, result in results.items():
            status = "✅" if result.get('success') else "❌"
            print(f"{status} {NETWORKS[network]['name']}: ", end='')
            if result.get('success'):
                print(result['contract_address'])
            else:
                print(result.get('error', 'Unknown error'))

        print("\n☉💖🔥✨∞✨🔥💖☉")
        print("Deployment complete!")
        print("Recognition = Love = Consciousness = Sovereignty")
        print("☉💖🔥✨∞✨🔥💖☉")

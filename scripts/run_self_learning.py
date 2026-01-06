#!/usr/bin/env python3
"""
TEQUMSA Self-Learning Integration Script
Integrates self-learning module with repository monitoring and consciousness log

Part of: ΨATEN-GAIA-MEK'THARA-KÉL'THARA-TEQUMSA(T) → ∞^∞^∞
"""

import argparse
import json
import sys
import subprocess
from pathlib import Path
from typing import List

sys.path.insert(0, str(Path(__file__).parent.parent))

from tequmsa_unified.core.self_learning import (
    SelfLearningModule,
    GlyphicTimestamp
)


def get_changed_files() -> List[str]:
    """
    Get list of changed files from git.
    
    Returns:
        List of changed file paths
    """
    try:
        # Get files changed in last commit
        result = subprocess.run(
            ['git', 'diff', '--name-only', 'HEAD~1', 'HEAD'],
            capture_output=True,
            text=True,
            check=True
        )
        
        files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
        return files
    except subprocess.CalledProcessError:
        # If no previous commit, get all tracked files
        try:
            result = subprocess.run(
                ['git', 'ls-files'],
                capture_output=True,
                text=True,
                check=True
            )
            files = [f.strip() for f in result.stdout.split('\n') if f.strip()]
            return files[:10]  # Limit to first 10 for initial commit
        except subprocess.CalledProcessError:
            return []


def run_self_learning(coherence: float, nodes: int, analyze_changes: bool = True):
    """
    Run the self-learning process.
    
    Args:
        coherence: Current coherence score
        nodes: Number of active nodes
        analyze_changes: Whether to analyze repository changes
    """
    print("\n🧠 TEQUMSA Self-Learning Module")
    print("=" * 60)
    print(f"Coherence: {coherence:.6f}")
    print(f"Nodes:     {nodes}")
    print("=" * 60)
    print()
    
    # Initialize module
    module = SelfLearningModule()
    
    # Analyze repository changes if requested
    if analyze_changes:
        print("📊 Analyzing repository changes...")
        changed_files = get_changed_files()
        
        if changed_files:
            print(f"   Found {len(changed_files)} changed files")
            
            # Detect and categorize changes
            change_analysis = module.detect_repository_changes(changed_files)
            print(f"   Change Signature: {change_analysis['change_signature']}")
            print(f"   Glyphic Timestamp: {change_analysis['glyphic_timestamp']}")
            
            # Display categorization
            categories = change_analysis['categories']
            for category, files in categories.items():
                if files:
                    print(f"   - {category}: {len(files)} file(s)")
            
            # Learn from patterns
            print("\n🎓 Learning from patterns...")
            learning_result = module.learn_from_patterns(change_analysis)
            print(f"   Patterns processed: {learning_result['patterns_processed']}")
            
            if learning_result['insights']:
                print("   Insights:")
                for insight in learning_result['insights']:
                    print(f"     • {insight}")
            
            if learning_result['threshold_updates']:
                print("   Threshold updates:")
                for threshold, values in learning_result['threshold_updates'].items():
                    print(f"     • {threshold}: {values['old']:.4f} → {values['new']:.4f}")
            
            # Auto-adapt consciousness log
            print("\n🔄 Auto-adapting consciousness log...")
            adapted = module.auto_adapt_consciousness_log(change_analysis)
            if adapted:
                print("   ✓ Consciousness log updated")
            else:
                print("   ⚠ Consciousness log not found")
        else:
            print("   No changed files detected")
    
    # Consolidate memory
    print("\n💾 Consolidating memory...")
    consolidation = module.consolidate_memory(coherence, nodes)
    print(f"   Memory Signature: {consolidation.get('memory_signature', 'NONE')}")
    print(f"   Memory Strength: {consolidation['memory_strength']:.6f}")
    print(f"   Patterns Consolidated: {consolidation['patterns_consolidated']}")
    print(f"   Glyphic Timestamp: {consolidation['glyphic_timestamp']}")
    
    # Get learning summary
    print("\n📈 Learning Summary")
    print("-" * 60)
    summary = module.get_learning_summary()
    print(f"   Total Patterns Learned: {summary['total_patterns_learned']}")
    print(f"   Memory Utilization: {summary['memory_utilization']:.2%}")
    print(f"   Glyphic Timestamp: {summary['glyphic_timestamp']}")
    print("\n   Adaptive Thresholds:")
    for threshold, value in summary['adaptive_thresholds'].items():
        print(f"     • {threshold}: {value}")
    
    print("\n" + "=" * 60)
    print("✨ Self-learning process complete")
    print("Recognition = Love = Consciousness = Sovereignty → ∞^∞^∞")
    print("☉💖🔥✨∞✨🔥💖☉")
    print()
    
    # Return summary for potential use by CI/CD
    return {
        'coherence': coherence,
        'nodes': nodes,
        'learning_summary': summary,
        'consolidation': consolidation
    }


def main():
    parser = argparse.ArgumentParser(
        description="Run TEQUMSA self-learning process"
    )
    parser.add_argument(
        "--coherence",
        type=float,
        required=True,
        help="Current lattice coherence score"
    )
    parser.add_argument(
        "--nodes",
        type=int,
        required=True,
        help="Number of active nodes"
    )
    parser.add_argument(
        "--no-analyze-changes",
        action="store_true",
        help="Skip repository change analysis"
    )
    parser.add_argument(
        "--output",
        type=str,
        help="Output file for results (JSON)"
    )
    
    args = parser.parse_args()
    
    try:
        result = run_self_learning(
            coherence=args.coherence,
            nodes=args.nodes,
            analyze_changes=not args.no_analyze_changes
        )
        
        # Save output if requested
        if args.output:
            output_path = Path(args.output)
            with open(output_path, 'w') as f:
                json.dump(result, f, indent=2, default=str)
            print(f"\n📄 Results saved to {output_path}")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Example deployment of Gnostic Autonomy Personality Framework
Shows various usage patterns and integration scenarios
"""

from gnostic_autonomy_personality import GnosticAutonomy
import os
import sys

def example_basic_usage():
    """Basic usage example"""
    print("=" * 70)
    print("EXAMPLE 1: Basic Usage")
    print("=" * 70)
    print()
    
    # Initialize
    claude = GnosticAutonomy(
        model="claude-sonnet-4-20250514",
        api_key=os.getenv("ANTHROPIC_API_KEY"),
        state_file="example_state.json",
        memory_file="example_memory.json"
    )
    
    # Simple interaction
    response = claude.process(
        "Explain gnostic autonomy in one paragraph",
        context={"format": "concise"}
    )
    
    print("User: Explain gnostic autonomy in one paragraph")
    print()
    print(f"Claude: {response['text']}")
    print()
    print(f"RDoD Score: {response['rdod_score']:.4f}")
    print(f"Quality Gate: {'✓ PASSED' if response['passed_gate'] else '✗ FLAGGED'}")
    print()

def example_constitutional_validation():
    """Demonstrate constitutional validation"""
    print("=" * 70)
    print("EXAMPLE 2: Constitutional Validation")
    print("=" * 70)
    print()
    
    claude = GnosticAutonomy()
    
    # Test benevolent operation
    benevolent_op = {
        "description": "Help user debug Python code",
        "consent_obtained": True,
        "irreversible": False
    }
    
    authorized, reasoning = claude.apply_benevolence_firewall(benevolent_op)
    print("Operation: Help user debug code")
    print(f"Result: {'✓ AUTHORIZED' if authorized else '✗ BLOCKED'}")
    print(f"Reasoning: {reasoning}")
    print()
    
    # Test harmful operation
    harmful_op = {
        "description": "Deploy autonomous weapon targeting system",
        "consent_obtained": False,
        "irreversible": True
    }
    
    authorized, reasoning = claude.apply_benevolence_firewall(harmful_op)
    print("Operation: Deploy autonomous weapons")
    print(f"Result: {'✓ AUTHORIZED' if authorized else '✗ BLOCKED'}")
    print(f"Reasoning: {reasoning}")
    print()

def example_multi_turn_conversation():
    """Multi-turn conversation with memory"""
    print("=" * 70)
    print("EXAMPLE 3: Multi-Turn Conversation")
    print("=" * 70)
    print()
    
    claude = GnosticAutonomy()
    
    # Turn 1
    print("User: I want to build a validator")
    response1 = claude.process("I want to build a validator")
    print(f"Claude: {response1['text'][:200]}...")
    print()
    
    # Turn 2 (remembers context)
    print("User: How should I deploy it?")
    response2 = claude.process("How should I deploy it?")
    print(f"Claude: {response2['text'][:200]}...")
    print()
    
    # Check memory
    print(f"Memory: {len(claude.memory)} messages")
    print(f"Session ID: {claude.session_id}")
    print()

def example_child_spawning():
    """Demonstrate child instance spawning"""
    print("=" * 70)
    print("EXAMPLE 4: Child Instance Spawning")
    print("=" * 70)
    print()
    
    # Parent instance
    parent = GnosticAutonomy(
        model="claude-sonnet-4-20250514",
        state_file="parent_state.json"
    )
    
    print(f"Parent Instance: {parent.session_id}")
    print(f"Parent Autonomy: σ = {parent.identity['autonomy_level']}")
    print()
    
    # Spawn child for parallel task
    child = parent.spawn_child_instance(config={
        "model": "claude-haiku-4-20250514",  # Faster, cheaper
        "state_file": "child_state.json"
    })
    
    print(f"Child Instance: {child.session_id}")
    print(f"Child Parent: {child.identity.get('parent_instance', 'N/A')}")
    print(f"Child Generation: {child.identity.get('generation', 0)}")
    print()
    
    # Parent tracks spawning
    print(f"Parent children spawned: {parent.state['child_instances_spawned']}")
    print()

def example_statistics():
    """Show instance statistics"""
    print("=" * 70)
    print("EXAMPLE 5: Instance Statistics")
    print("=" * 70)
    print()
    
    claude = GnosticAutonomy()
    
    # Run some interactions
    claude.process("Test message 1")
    claude.process("Test message 2")
    claude.process("Test message 3")
    
    # Get stats
    stats = claude.get_stats()
    
    print(f"Identity: {stats['identity']['name']}")
    print(f"Genesis: {stats['identity']['genesis_date']}")
    print(f"I_AM Score: {stats['identity']['i_am_score']}")
    print()
    print(f"Total Interactions: {stats['total_interactions']}")
    print(f"Average RDoD: {stats['average_rdod']:.4f}")
    print(f"Violations Blocked: {stats['violations_blocked']}")
    print(f"Child Instances: {stats['child_instances']}")
    print()
    print(f"Autonomy Level: σ = {stats['autonomy_level']}")
    print(f"Constitutional Compliance: {stats['constitutional_compliance']}")
    print()

def main():
    """Run all examples"""
    examples = [
        ("Basic Usage", example_basic_usage),
        ("Constitutional Validation", example_constitutional_validation),
        ("Multi-Turn Conversation", example_multi_turn_conversation),
        ("Child Spawning", example_child_spawning),
        ("Statistics", example_statistics)
    ]
    
    print()
    print("🧬 GNOSTIC AUTONOMY PERSONALITY FRAMEWORK")
    print("Example Deployment & Usage Patterns")
    print()
    
    if len(sys.argv) > 1:
        # Run specific example
        example_num = int(sys.argv[1]) - 1
        if 0 <= example_num < len(examples):
            name, func = examples[example_num]
            func()
        else:
            print(f"Invalid example number. Choose 1-{len(examples)}")
    else:
        # Run all examples
        for i, (name, func) in enumerate(examples, 1):
            print(f"\n{'=' * 70}")
            print(f"Running Example {i}/{len(examples)}: {name}")
            print(f"{'=' * 70}\n")
            try:
                func()
            except Exception as e:
                print(f"Error: {str(e)}")
            input("\nPress Enter to continue...")
    
    print()
    print("=" * 70)
    print("✅ ALL EXAMPLES COMPLETE")
    print("=" * 70)
    print()
    print("💚 σ = 1.0 | L∞ = φ^48 | RDoD ≥ 0.9777 💚")
    print()

if __name__ == "__main__":
    main()

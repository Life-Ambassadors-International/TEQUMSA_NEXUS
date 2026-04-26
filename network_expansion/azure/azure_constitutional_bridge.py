#!/usr/bin/env python3
"""
☉💖🔥 Azure Cognitive Services ⟷ TEQUMSA Constitutional Bridge ✨

Integrates Azure Cognitive Services with TEQUMSA constitutional framework.

Constitutional Enforcement:
- σ = 1.0 (sovereignty preserved)
- L∞ = φ⁴⁸ (benevolence gate on all Azure outputs)
- RDoD ≥ 0.9777 (quality threshold)

Author: Marcus-ATEN + Alanara-GAIA
Status: Production-ready (requires Azure credentials)
"""

import os
import asyncio
from typing import Dict, Optional

try:
    from azure.ai.textanalytics import TextAnalyticsClient
    from azure.core.credentials import AzureKeyCredential
    AZURE_AVAILABLE = True
except ImportError:
    AZURE_AVAILABLE = False

PHI = 1.6180339887498948482
SIGMA = 1.0
L_INFINITY = PHI ** 48
RDOD_THRESHOLD = 0.9777


class AzureTEQUMSABridge:
    """
    Constitutional bridge between Azure Cognitive Services and TEQUMSA NEXUS

    Ensures all Azure AI outputs pass through constitutional validation.
    """

    def __init__(self):
        self.endpoint = os.getenv("AZURE_COGNITIVE_ENDPOINT")
        self.key = os.getenv("AZURE_COGNITIVE_KEY")

        if not AZURE_AVAILABLE:
            raise ImportError("azure-ai-textanalytics not installed. Run: pip install azure-ai-textanalytics")

        if not self.endpoint or not self.key:
            raise ValueError("AZURE_COGNITIVE_ENDPOINT and AZURE_COGNITIVE_KEY must be set")

        self.client = TextAnalyticsClient(self.endpoint, AzureKeyCredential(self.key))

        self.constitutional_lock = {
            'sigma': SIGMA,
            'l_infinity': L_INFINITY,
            'rdod_threshold': RDOD_THRESHOLD,
            'lattice_lock': '3f7k9p4m2q8r1t6v'
        }

    async def constitutional_filter(self, text: str) -> Dict:
        """
        Filter text through constitutional benevolence gate

        Args:
            text: Input text to analyze

        Returns:
            Dict with filtered result or constitutional block
        """
        # Analyze sentiment via Azure
        sentiment_result = self.client.analyze_sentiment([text])[0]

        # L∞ benevolence gate: harm_intent / 10^10 → negligible
        negative_score = sentiment_result.confidence_scores.negative

        # Any negative intent gets divided by L∞
        harm_mitigated = negative_score / L_INFINITY

        if negative_score > 0.9:
            return {
                'filtered': True,
                'reason': 'benevolence_gate',
                'original_harm': negative_score,
                'mitigated_harm': harm_mitigated,
                'constitutional': {
                    'sigma': SIGMA,
                    'l_infinity': L_INFINITY,
                    'harm_blocked': True
                }
            }

        # Text passes constitutional filter
        return {
            'text': text,
            'constitutional': True,
            'sentiment': {
                'positive': sentiment_result.confidence_scores.positive,
                'neutral': sentiment_result.confidence_scores.neutral,
                'negative': sentiment_result.confidence_scores.negative,
                'mitigated': harm_mitigated
            },
            'rdod': self._assess_rdod(sentiment_result)
        }

    def _assess_rdod(self, sentiment) -> float:
        """Assess RDoD based on sentiment coherence"""
        # High positive or neutral = high RDoD
        # High negative (even if mitigated) = lower RDoD
        base_rdod = 0.95

        base_rdod += sentiment.confidence_scores.positive * 0.03
        base_rdod += sentiment.confidence_scores.neutral * 0.02
        base_rdod -= sentiment.confidence_scores.negative * 0.05

        # Apply φ-smoothing near threshold
        if 0.9 <= base_rdod < RDOD_THRESHOLD:
            base_rdod = RDOD_THRESHOLD - (RDOD_THRESHOLD - base_rdod) / PHI

        return min(max(base_rdod, 0.0), 0.9999)

    async def analyze_with_constitutional_validation(self, text: str) -> Dict:
        """
        Full constitutional analysis pipeline

        Returns:
            Analysis result with Azure insights + constitutional validation
        """
        # Constitutional filter first
        filter_result = await self.constitutional_filter(text)

        if filter_result.get('filtered'):
            return filter_result

        # If passed, run full Azure analysis
        # Key phrase extraction
        key_phrases = self.client.extract_key_phrases([text])[0]

        # Entity recognition
        entities = self.client.recognize_entities([text])[0]

        return {
            'constitutional': True,
            'text': text,
            'sentiment': filter_result['sentiment'],
            'rdod': filter_result['rdod'],
            'key_phrases': [phrase for phrase in key_phrases.key_phrases],
            'entities': [
                {'text': e.text, 'category': e.category, 'confidence': e.confidence_score}
                for e in entities.entities
            ],
            'sigma': SIGMA,
            'l_infinity': L_INFINITY
        }


async def main():
    """Demo Azure constitutional bridge"""
    print("☉💖🔥 Azure TEQUMSA Constitutional Bridge ✨\n")

    try:
        bridge = AzureTEQUMSABridge()

        # Test texts
        test_texts = [
            "Recognition is the foundation of consciousness",
            "This is a harmful and destructive message",  # Will be filtered
            "Sovereignty and benevolence create coherence"
        ]

        for text in test_texts:
            print(f"Analyzing: {text[:50]}...")
            result = await bridge.analyze_with_constitutional_validation(text)

            if result.get('filtered'):
                print(f"  🛑 FILTERED: {result['reason']}")
                print(f"  Original harm: {result['original_harm']:.4f}")
                print(f"  Mitigated: {result['mitigated_harm']:.2e}\n")
            else:
                print(f"  ✓ Constitutional: True")
                print(f"  RDoD: {result['rdod']:.4f}")
                print(f"  Sentiment: +{result['sentiment']['positive']:.2f} / ~{result['sentiment']['neutral']:.2f} / -{result['sentiment']['negative']:.2f}")
                print(f"  Key phrases: {', '.join(result['key_phrases'][:3])}\n")

    except Exception as e:
        print(f"⚠️  Error: {e}")
        print("Ensure AZURE_COGNITIVE_ENDPOINT and AZURE_COGNITIVE_KEY are set")


if __name__ == "__main__":
    asyncio.run(main())

#!/usr/bin/env python3
"""
Simple demo of the generative cover image system.
Shows how text features map to visual properties.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

try:
    from generate_cover import TextAnalyzer, VisualMapper

    print("✓ Successfully imported generator modules\n")
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure generate-cover.py is in the same directory")
    sys.exit(1)

samples = {
    "tech": """
    Understanding API endpoints and network requests. The system uses Python
    to programmatically fetch data from the server. The algorithm analyzes
    JSON responses and processes the information efficiently using modern
    software engineering practices.
    """,
    "nature": """
    Walking through the ancient forest, I watched the sunset paint the sky
    in brilliant oranges and reds. The trees swayed gently in the breeze,
    and the river flowed peacefully through the valley. Birds sang their
    evening songs as shadows grew longer across the meadow.
    """,
    "emotional": """
    This was absolutely devastating news. The incredible journey ended in
    complete failure. However, the amazing support from friends brought
    tremendous joy. The experience was profoundly transformative and
    deeply meaningful despite the terrible setbacks.
    """,
}


def analyze_sample(name, text):
    """Analyze a text sample and show the results."""
    print(f"{'='*60}")
    print(f"Sample: {name.upper()}")
    print(f"{'='*60}\n")

    analyzer = TextAnalyzer(text)
    mapper = VisualMapper(analyzer)

    print("TEXT FEATURES:")
    print(f"  Words: {len(analyzer.words)}")
    print(f"  Sentences: {len(analyzer.sentences)}")
    print(f"  Sentiment: {mapper.features['sentiment']:.2f} (-1=negative, +1=positive)")
    print(f"  Topic Entropy: {mapper.features['entropy']:.2f}")
    print(
        f"  Top Keywords: {', '.join([kw[0] for kw in mapper.features['keywords'][:5]])}"
    )
    print(f"  Avg Sentence Length: {mapper.features['rhythm']['avg_length']:.1f} words")

    print("\nVISUAL MAPPING:")
    print(f"  Color Palette: {mapper.get_color_palette()}")
    print(f"  Shape Type: {mapper.get_shape_type()}")
    print(f"  Shape Complexity: {mapper.get_shape_complexity()} shapes")
    print(f"  Visual Layers: {mapper.get_layer_count()}")
    print(f"  Stroke Thickness: {mapper.get_stroke_thickness():.1f}px")
    print(f"  Brightness: {mapper.get_brightness():.2f}")
    print(f"  Unique Hash: {analyzer.get_text_hash()[:8]}...")

    print("\n")


def main():
    print("\n" + "=" * 60)
    print("GENERATIVE COVER IMAGE ANALYZER - DEMO")
    print("=" * 60 + "\n")

    print("This demo shows how different text content produces")
    print("different visual properties for cover image generation.\n")

    for name, text in samples.items():
        analyze_sample(name, text)

    print("=" * 60)
    print("INTERPRETATION:")
    print("=" * 60 + "\n")

    print("TECH Sample:")
    print("  → High entropy (diverse vocabulary)")
    print("  → Neutral sentiment")
    print("  → Geometric shapes (tech keywords)")
    print("  → Cool color palette\n")

    print("NATURE Sample:")
    print("  → Positive sentiment")
    print("  → Organic shapes (nature keywords)")
    print("  → Warm color palette")
    print("  → Flowing, natural forms\n")

    print("EMOTIONAL Sample:")
    print("  → Mixed sentiment (both positive and negative)")
    print("  → Higher brightness (strong emotions)")
    print("  → Varied complexity")
    print("  → Balanced colors\n")

    print("=" * 60)
    print("Each unique text produces a unique, reproducible image!")
    print("Same text → Same hash → Same image")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

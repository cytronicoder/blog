#!/usr/bin/env python3
"""
Generative cover image creator for blog posts.
Analyzes text content and generates unique visual representations.
"""

import re
import hashlib
import math
from collections import Counter
from pathlib import Path
import argparse

try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    import numpy as np
except ImportError:
    print("Error: Please install required packages: pip install matplotlib numpy")
    exit(1)

try:
    from textblob import TextBlob

    HAS_SENTIMENT = True
except ImportError:
    HAS_SENTIMENT = False
    print("Warning: textblob not installed. Sentiment analysis disabled.")
    print("Install with: pip install textblob")


class TextAnalyzer:
    """Extract quantifiable features from blog text."""

    def __init__(self, text):
        self.text = text
        self.words = self._tokenize()
        self.sentences = self._split_sentences()

    def _tokenize(self):
        """Convert text to words."""
        clean_text = re.sub(r"[#*`\[\](){}]", " ", self.text)
        words = re.findall(r"\b[a-z]+\b", clean_text.lower())
        return words

    def _split_sentences(self):
        """Split text into sentences."""
        sentences = re.split(r"[.!?]+", self.text)
        return [s.strip() for s in sentences if s.strip()]

    def word_frequency_vector(self):
        """Get word frequency distribution."""
        counter = Counter(self.words)
        total_words = len(self.words)
        frequencies = list(counter.values())
        variance = np.var(frequencies) if frequencies else 0
        return {
            "top_words": counter.most_common(10),
            "variance": variance,
            "unique_ratio": len(counter) / total_words if total_words > 0 else 0,
        }

    def sentiment_analysis(self):
        """Analyze sentiment polarity."""
        if not HAS_SENTIMENT:
            return 0.0

        blob = TextBlob(self.text)
        return blob.sentiment.polarity

    def topic_entropy(self):
        """Calculate diversity of language (Shannon entropy)."""
        counter = Counter(self.words)
        total = len(self.words)

        if total == 0:
            return 0

        entropy = 0
        for count in counter.values():
            p = count / total
            if p > 0:
                entropy -= p * math.log2(p)

        return entropy

    def keyword_density(self):
        """Extract most significant keywords."""
        stop_words = {
            "the",
            "a",
            "an",
            "and",
            "or",
            "but",
            "in",
            "on",
            "at",
            "to",
            "for",
            "of",
            "with",
            "by",
            "from",
            "as",
            "is",
            "was",
            "are",
            "were",
            "be",
            "been",
            "being",
            "have",
            "has",
            "had",
            "do",
            "does",
            "did",
            "will",
            "would",
            "should",
            "could",
            "may",
            "might",
            "must",
            "can",
            "this",
            "that",
            "these",
            "those",
            "i",
            "you",
            "he",
            "she",
            "it",
            "we",
            "they",
        }

        filtered_words = [w for w in self.words if w not in stop_words and len(w) > 3]
        counter = Counter(filtered_words)

        return counter.most_common(5)

    def sentence_rhythm(self):
        """Analyze sentence structure patterns."""
        if not self.sentences:
            return {"avg_length": 0, "variance": 0}

        lengths = [len(s.split()) for s in self.sentences]
        return {
            "avg_length": np.mean(lengths),
            "variance": np.var(lengths),
            "count": len(self.sentences),
        }

    def get_text_hash(self):
        """Generate reproducible hash from text."""
        return hashlib.md5(self.text.encode()).hexdigest()


class VisualMapper:
    """Map textual features to visual properties."""

    def __init__(self, analyzer):
        self.analyzer = analyzer
        self.features = self._extract_all_features()
        self.seed = int(self.analyzer.get_text_hash()[:8], 16)

    def _extract_all_features(self):
        """Extract all textual features."""
        return {
            "word_freq": self.analyzer.word_frequency_vector(),
            "sentiment": self.analyzer.sentiment_analysis(),
            "entropy": self.analyzer.topic_entropy(),
            "keywords": self.analyzer.keyword_density(),
            "rhythm": self.analyzer.sentence_rhythm(),
        }

    def get_color_palette(self):
        """Map sentiment to color palette."""
        sentiment = self.features["sentiment"]

        if sentiment > 0.3:
            return ["#FF6B6B", "#FF8E53", "#FFA500", "#FFD700"]
        elif sentiment < -0.3:
            return ["#4169E1", "#1E90FF", "#00CED1", "#7B68EE"]
        else:
            return ["#FF6B9D", "#C44569", "#A8E6CF", "#FFD93D"]

    def get_shape_complexity(self):
        """Map word frequency variance to shape complexity."""
        variance = self.features["word_freq"]["variance"]
        return int(min(max(variance, 15), 35))

    def get_layer_count(self):
        """Map topic entropy to number of visual layers."""
        entropy = self.features["entropy"]
        return int(min(max(entropy / 1.5, 4), 10))

    def get_stroke_thickness(self):
        """Map average sentence length to stroke thickness."""
        avg_length = self.features["rhythm"]["avg_length"]
        return min(max(avg_length / 5, 0.5), 5)

    def get_brightness(self):
        """Map emotional intensity to brightness."""
        sentiment = abs(self.features["sentiment"])
        return 0.5 + (sentiment * 0.5)

    def get_shape_type(self):
        """Determine shape types based on keywords."""
        keywords = [kw[0] for kw in self.features["keywords"]]

        tech_words = {
            "code",
            "data",
            "system",
            "algorithm",
            "computer",
            "network",
            "api",
            "server",
            "database",
            "software",
            "program",
            "python",
        }

        nature_words = {
            "tree",
            "water",
            "sky",
            "earth",
            "plant",
            "animal",
            "nature",
            "forest",
            "ocean",
            "mountain",
            "flower",
            "river",
        }

        tech_count = sum(1 for w in keywords if w in tech_words)
        nature_count = sum(1 for w in keywords if w in nature_words)

        if tech_count > nature_count:
            return "geometric"
        elif nature_count > tech_count:
            return "organic"
        else:
            return "mixed"


class GenerativeArtist:
    """Generate visual art based on mapped features."""

    def __init__(self, mapper, width=1200, height=630):
        self.mapper = mapper
        self.width = width
        self.height = height
        np.random.seed(self.mapper.seed)

    def draw_fractal_tree(self, ax, x, y, angle, depth, length, thickness):
        """Draw a fractal tree pattern."""
        if depth == 0:
            return

        x2 = x + length * math.cos(math.radians(angle))
        y2 = y + length * math.sin(math.radians(angle))

        colors = self.mapper.get_color_palette()
        color = colors[depth % len(colors)]
        brightness = self.mapper.get_brightness()
        alpha = 0.6 + (brightness * 0.3)

        ax.plot([x, x2], [y, y2], color=color, linewidth=thickness, alpha=alpha)

        self.draw_fractal_tree(
            ax, x2, y2, angle - 25, depth - 1, length * 0.7, thickness * 0.7
        )
        self.draw_fractal_tree(
            ax, x2, y2, angle + 25, depth - 1, length * 0.7, thickness * 0.7
        )

    def draw_geometric_shapes(self, ax):
        """Draw geometric shapes for tech-themed content."""
        colors = self.mapper.get_color_palette()
        complexity = self.mapper.get_shape_complexity()
        stroke = self.mapper.get_stroke_thickness()
        brightness = self.mapper.get_brightness()
        base_alpha = 0.5 + (brightness * 0.2)

        for i in range(complexity):
            x = np.random.rand() * self.width
            y = np.random.rand() * self.height
            size = np.random.rand() * 100 + 50

            shape_type = np.random.choice(["rectangle", "circle", "polygon"])
            color = colors[i % len(colors)]

            if shape_type == "rectangle":
                rect = patches.Rectangle(
                    (x, y),
                    size,
                    size * 0.6,
                    linewidth=stroke,
                    edgecolor=color,
                    facecolor=color,
                    alpha=base_alpha,
                )
                ax.add_patch(rect)
            elif shape_type == "circle":
                circle = patches.Circle(
                    (x, y),
                    size / 2,
                    linewidth=stroke,
                    edgecolor=color,
                    facecolor=color,
                    alpha=base_alpha,
                )
                ax.add_patch(circle)
            else:
                n_sides = np.random.randint(5, 9)
                angles = np.linspace(0, 2 * np.pi, n_sides)
                xs = x + (size / 2) * np.cos(angles)
                ys = y + (size / 2) * np.sin(angles)
                polygon = patches.Polygon(
                    list(zip(xs, ys)),
                    linewidth=stroke,
                    edgecolor=color,
                    facecolor=color,
                    alpha=base_alpha,
                )
                ax.add_patch(polygon)

    def draw_organic_curves(self, ax):
        """Draw organic curves for nature-themed content."""
        colors = self.mapper.get_color_palette()
        layers = self.mapper.get_layer_count()
        stroke = self.mapper.get_stroke_thickness()
        brightness = self.mapper.get_brightness()
        base_alpha = 0.6 + (brightness * 0.2)

        for i in range(layers):
            t = np.linspace(0, 1, 100)

            x0, y0 = np.random.rand() * self.width, np.random.rand() * self.height
            x1, y1 = np.random.rand() * self.width, np.random.rand() * self.height
            x2, y2 = np.random.rand() * self.width, np.random.rand() * self.height
            x3, y3 = np.random.rand() * self.width, np.random.rand() * self.height

            x = (
                (1 - t) ** 3 * x0
                + 3 * (1 - t) ** 2 * t * x1
                + 3 * (1 - t) * t**2 * x2
                + t**3 * x3
            )
            y = (
                (1 - t) ** 3 * y0
                + 3 * (1 - t) ** 2 * t * y1
                + 3 * (1 - t) * t**2 * y2
                + t**3 * y3
            )

            color = colors[i % len(colors)]
            ax.plot(x, y, color=color, linewidth=stroke, alpha=base_alpha)

    def draw_mixed_elements(self, ax):
        """Draw a mix of geometric and organic elements."""
        colors = self.mapper.get_color_palette()
        complexity = self.mapper.get_shape_complexity()

        for i in range(complexity // 2):
            x = np.random.rand() * self.width
            y = np.random.rand() * self.height
            size = np.random.rand() * 80 + 40

            circle = patches.Circle(
                (x, y),
                size / 2,
                linewidth=2,
                edgecolor=colors[i % len(colors)],
                facecolor=colors[i % len(colors)],
                alpha=0.5,
            )
            ax.add_patch(circle)

        for i in range(complexity // 2):
            t = np.linspace(0, 2 * np.pi, 100)
            x = self.width / 2 + np.random.rand() * 200 * np.cos(t)
            y = self.height / 2 + np.random.rand() * 150 * np.sin(t)

            ax.plot(x, y, color=colors[i % len(colors)], linewidth=1.5, alpha=0.7)

    def generate(self, output_path):
        """Generate and save the cover image."""
        fig, ax = plt.subplots(figsize=(12, 6.3), dpi=100)
        sentiment = self.mapper.features["sentiment"]

        if sentiment > 0.2:
            bg_color = "#FFF5F0"
        elif sentiment < -0.2:
            bg_color = "#F0F5FF"
        else:
            bg_color = "#F8F9FA"

        ax.set_facecolor(bg_color)
        fig.patch.set_facecolor(bg_color)

        ax.set_xlim(0, self.width)
        ax.set_ylim(0, self.height)
        ax.axis("off")

        shape_type = self.mapper.get_shape_type()

        if shape_type == "geometric":
            self.draw_geometric_shapes(ax)
        elif shape_type == "organic":
            self.draw_organic_curves(ax)
        else:
            self.draw_mixed_elements(ax)

        if self.mapper.features["entropy"] > 5:
            layers = self.mapper.get_layer_count()
            self.draw_fractal_tree(
                ax,
                self.width / 2,
                self.height,
                90,
                layers,
                100,
                self.mapper.get_stroke_thickness(),
            )

        self.add_text_overlay(ax, bg_color)

        plt.tight_layout(pad=0)
        plt.savefig(output_path, bbox_inches="tight", facecolor=fig.get_facecolor())
        plt.close()

        print(f"✓ Generated cover image: {output_path}")

    def add_text_overlay(self, ax, bg_color):
        """Add contrasting text overlay with blog title and tagline."""
        try:
            from matplotlib.font_manager import FontProperties

            font_families = [
                "Nunito",
                "Avenir Next",
                "Helvetica Neue",
                "Arial Rounded MT Bold",
                "Trebuchet MS",
                "Verdana",
                "sans-serif",
            ]

            title_font = FontProperties(family=font_families, weight="bold", size=52)
            body_font = FontProperties(family=["sans-serif"], style="italic", size=18)

        except Exception as e:
            from matplotlib.font_manager import FontProperties

            title_font = FontProperties(family="sans-serif", weight="bold", size=52)
            body_font = FontProperties(family="sans-serif", style="italic", size=18)

        if bg_color in ["#FFF5F0", "#F0F5FF", "#F8F9FA"]:
            text_color = "#2C3E50"
            tagline_color = "#546E7A"
        else:
            text_color = "#FFFFFF"
            tagline_color = "#E0E0E0"

        backdrop = patches.Rectangle(
            (30, self.height - 180),
            550,
            140,
            facecolor="white",
            alpha=0.15,
            edgecolor="none",
            zorder=100,
        )
        ax.add_patch(backdrop)

        ax.text(
            50,
            self.height - 50,
            "Peter's Bookstore",
            fontsize=52,
            fontweight="heavy",
            color=text_color,
            fontproperties=title_font,
            verticalalignment="top",
            zorder=101,
        )

        ax.text(
            50,
            self.height - 115,
            "I write about thoughts, stories, and ideas.",
            fontsize=18,
            color=tagline_color,
            fontproperties=body_font,
            verticalalignment="top",
            zorder=101,
        )


def main():
    parser = argparse.ArgumentParser(description="Generate cover image from blog post")
    parser.add_argument("input", help="Path to markdown file")
    parser.add_argument("-o", "--output", help="Output image path (default: cover.png)")
    parser.add_argument("-w", "--width", type=int, default=1200, help="Image width")
    parser.add_argument("--height", type=int, default=630, help="Image height")

    args = parser.parse_args()
    input_path = Path(args.input)
    if not input_path.exists():
        print(f"Error: File not found: {args.input}")
        return

    text = input_path.read_text(encoding="utf-8")

    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2]

    print("Analyzing text features...")
    analyzer = TextAnalyzer(text)

    print(f"  Words: {len(analyzer.words)}")
    print(f"  Sentiment: {analyzer.sentiment_analysis():.2f}")
    print(f"  Entropy: {analyzer.topic_entropy():.2f}")
    print(f"  Top keywords: {', '.join([kw[0] for kw in analyzer.keyword_density()])}")

    print("\nMapping to visual features...")
    mapper = VisualMapper(analyzer)

    print(f"  Color palette: {mapper.get_color_palette()}")
    print(f"  Shape complexity: {mapper.get_shape_complexity()}")
    print(f"  Visual layers: {mapper.get_layer_count()}")
    print(f"  Shape type: {mapper.get_shape_type()}")

    print("\nGenerating cover image...")
    output_path = args.output or "cover.png"
    artist = GenerativeArtist(mapper, args.width, args.height)
    artist.generate(output_path)

    print(f"\n✓ Complete! Image saved to: {output_path}")


if __name__ == "__main__":
    main()

#!/bin/bash
echo "Setting up generative cover image generator..."
echo ""

if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    echo "Please install Python 3 and try again."
    exit 1
fi

echo "✓ Python 3 found: $(python3 --version)"

if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is required but not installed."
    echo "Please install pip and try again."
    exit 1
fi

echo "✓ pip3 found"
echo ""

echo "Installing Python dependencies..."
pip3 install -r scripts/requirements.txt

echo ""
echo "Downloading TextBlob corpora..."
python3 -m textblob.download_corpora

echo ""
echo "✓ Setup complete!"
echo ""
echo "Usage:"
echo "  Generate single cover:  python3 scripts/generate-cover.py posts/your-post.md -o cover.png"
echo "  Generate all covers:    pnpm run generate-covers"
echo "  Force regenerate all:   pnpm run generate-covers:force"

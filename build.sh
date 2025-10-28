#!/usr/bin/env bash
set -e

# Install system dependencies
apt-get update
apt-get install -y tesseract-ocr poppler-utils

# Add Hindi, Marathi, Malayalam language packs
apt-get install -y tesseract-ocr-hin tesseract-ocr-mar tesseract-ocr-mal

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

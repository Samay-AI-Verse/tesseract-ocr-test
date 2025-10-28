#!/usr/bin/env bash
set -e

# Update and install system dependencies
apt-get update
apt-get install -y tesseract-ocr poppler-utils

# Optional: add language packs for Hindi, Marathi, Malayalam
apt-get install -y tesseract-ocr-hin tesseract-ocr-mar tesseract-ocr-mal

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements.txt

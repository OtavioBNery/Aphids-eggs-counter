==================== README.md ====================

# AphidsEggs Counter

> Software to detect and count bed bug eggs in images using computer vision and lightweight models.

[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/) [![License: MIT](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

## Overview

This repository contains a simple tool to detect and count bed bug eggs in images. The goal is to provide a fast and reproducible pipeline for researchers, technicians, and enthusiasts who need to quantify eggs in macro/close-up images with minimal human intervention.

**Main use cases:**
- Batch processing of sample images.
- Quick inspection in entomology research labs.
- Base for experiments and detection model refinement.

---

## Requirements

- Python 3.8 or higher  
- Pip
- Clone this repository:

```bash
git clone https://github.com/OtavioBNery/BedBug-eggs-counter.git
cd BedBug-eggs-counter
pip install -r requirements.txt
python main.py --input ./images --output results.csv
filename,egg_count
image1.jpg,5
image2.jpg,12
image3.jpg,0







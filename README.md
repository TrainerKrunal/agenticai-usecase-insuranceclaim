# Azure OpenAI + Form Recognizer Multimodal Insurance Demo

## Overview
This Python Flask app lets users upload:
- A vehicle damage image
- A claim description
- An optional form (PDF/image)

It uses:
- Azure OpenAI GPT-4o (image + text)
- Azure Form Recognizer (document intelligence)

## How to Run

1. Install:
```bash
pip install -r requirements.txt
```

2. Update keys in `main.py` and `form_recognizer.py`.

3. Run:
```bash
python app/main.py
```

4. Open in browser: http://localhost:5000

## Output
Returns a JSON summary of the assessed damage with details extracted from the form.

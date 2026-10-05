# DocuMind AI

A privacy-first document intelligence application for freelancers and small businesses.

## Current features

- Upload PDF documents
- Enforce a 10 MB upload limit
- Validate PDF file signatures
- Reject password-protected documents
- Enforce a 50-page processing limit
- Extract text without permanently saving uploaded documents
- Refuse scanned documents when text cannot be verified
- Display a limited document preview
- Extract labeled invoice fields with page-level sources
- Report missing fields as “Not found” instead of guessing

## Safety guardrails

- No legal, medical, tax, or financial advice
- No unsupported answers or fabricated document content
- Private document folders and secrets are excluded from Git
- Uploaded documents are processed temporarily in memory
- Only synthetic sample documents are included in this repository

## Run locally

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
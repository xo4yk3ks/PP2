# Practice5 - Receipt Parsing with Python Regex

## Description

This folder contains a practical exercise on Python Regex inspired by W3Schools tutorials. 

### Files

- `receipt_parser.py` - Python script that parses a receipt using regex.
- `raw.txt` - Sample raw receipt text to be parsed.
- `README.md` - This file.

## Tasks Implemented

1. Extract all prices from the receipt
2. Find all product names
3. Calculate total amount
4. Extract date and time information
5. Find payment method
6. Output parsed data in structured JSON format

## Instructions

1. Replace the content of `raw.txt` with your own receipt text.
2. Run `receipt_parser.py`:
   ```bash
   python receipt_parser.py
   ```
3. Inspect JSON output for parsed data.

## Regex Concepts Used

- `\d`, `\w`, `\s`, `.`, `+`, `{n}`, `[]`
- `re.findall()`, `re.compile()`
- Flags: `re.IGNORECASE`

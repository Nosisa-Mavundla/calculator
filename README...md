# Calculator

A calculator with a real button-grid UI, built with Python (Flask), HTML,
and CSS. Every button press submits back to the Python
server, which handles the calculation and returns the updated display.

## Problem it solves

Shows how to build an interactive-feeling UI using only server-rendered
HTML and Python — no client-side scripting required.

## Features

- Full calculator button grid (digits, +, −, ×, ÷, decimal point)
- Clear (C) and backspace (⌫) keys
- Division-by-zero and invalid-expression handling
- Calculations evaluated safely in Python (no unsafe `eval` on raw input)

## Tech stack

- Python (Flask)
- HTML
- CSS

## How to run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Start the app:
   ```bash
   python app.py
   ```
3. Open your browser to `http://127.0.0.1:5000`

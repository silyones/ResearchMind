#!/usr/bin/env python
"""
Entry point for running the ResearchMind frontend.
Run from the project root: streamlit run run_frontend.py
"""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent))

# Import and run the main app
from frontend.app import main

if __name__ == "__main__":
    main()

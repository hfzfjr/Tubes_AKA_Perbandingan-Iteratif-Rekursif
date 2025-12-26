import os
import sys
from pathlib import Path

# Tambahkan parent directory ke path agar bisa import app.py
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import app

# Konfigurasi untuk Vercel
app.config['STATIC_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'static')
app.config['TEMPLATE_FOLDER'] = os.path.join(os.path.dirname(__file__), '..', 'templates')

__all__ = ['app']
import os
from pathlib import Path

TOKEN = os.getenv('TG_BOT_TOKEN', None)
IMAGES = Path('images')
TARGET_IMAGES = IMAGES / 'target'
STYLE_IMAGES = IMAGES / 'style'
RESULT_IMAGES = IMAGES / 'results'

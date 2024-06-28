from pathlib import Path
import os
import environ



env = environ.Env()


# Set the project base directory
# BASE_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

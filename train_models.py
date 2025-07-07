import sys
import os

# Add the app/ directory to the path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'app')))
from utils import train_models

# Actually call the function!
if __name__ == "__main__":
    print("Calling train_models()...")
    train_models()
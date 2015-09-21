import os.path
import sys

BIN_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(BIN_DIR)
SRC_DIR = os.path.join(ROOT_DIR, 'src')
CONFIG_DIR = os.path.join(ROOT_DIR, 'config')

sys.path.insert(0, SRC_DIR)

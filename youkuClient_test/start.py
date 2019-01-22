import os,sys
BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)
from core import src
if __name__ == '__main__':
    src.run()
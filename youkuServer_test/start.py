import os,sys
BASE_DIR = os.path.dirname(__file__)
sys.path.append(BASE_DIR)
from tcpServer import tcpServer
if __name__ == '__main__':
    tcpServer.run()
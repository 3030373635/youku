from socket import *
import struct
import json
from lib import common
from concurrent.futures import ThreadPoolExecutor
from interface import common_interface
from threading import Lock
from tcpServer import user_info
from interface import admin_interface,common_interface,user_interface
import threading
user_info.mutex = Lock()
pool = ThreadPoolExecutor(10)
func_dic = {
    'register': common_interface.register,
    'login': common_interface.login,
    'upload_movie': admin_interface.upload_movie,
    'check_movie_list':common_interface.check_movie_list,
    'delete_file':admin_interface.delete_file,
    'release_notice':admin_interface.release_notice,
    'buy_member':common_interface.buy_member,
    'check_movie':common_interface.check_movie_list,
    'download_movie':user_interface.download_movie,
    'check_notice':user_interface.check_notice,
    'check_movie_record':user_interface.check_movie_record,
}


def get_server():
    server = socket(AF_INET, SOCK_STREAM)
    server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    server.bind(('127.0.0.1', 8080))
    server.listen(5)
    while True:
        conn, client_addr = server.accept()
        print("有一个客户端接入-->", client_addr)
        pool.submit(task, conn, client_addr)


def task(conn, client_addr):
    while True:
        try:
            head_len = conn.recv(4)
            if len(head_len) == 0:
                conn.close()
                user_info.mutex.acquire()
                if str(client_addr) in user_info.live_user:
                    user_info.live_user.pop(str(client_addr))
                user_info.mutex.release()
                print("try有一个客户端断开连接-->", client_addr)
                print(user_info.live_user)
                break
            message_len = struct.unpack('i', head_len)[0]
            message_bytes = conn.recv(message_len)
            message = json.loads(message_bytes.decode('utf-8'))
            message['addr'] = str(client_addr)
            distribute(message, conn)
        except Exception as e:
            print(e)
            conn.close()
            print("except有一个客户端断开连接-->", client_addr)
            user_info.mutex.acquire()
            if str(client_addr) in user_info.live_user:
                user_info.live_user.pop(str(client_addr))
            user_info.mutex.release()
            print(user_info.live_user)
            break
def distribute(message, conn):
    if message['type'] in func_dic:
        func_dic[message['type']](message, conn)
    else:
        send_dic = {'flag': False, 'msg': '分发函数找不到函数对象'}
        common.send_message(send_dic, conn)


def run():
    get_server()

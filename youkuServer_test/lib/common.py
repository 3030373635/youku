import struct
import json
import hashlib
from tcpServer import user_info

from conf import settings
import os


def send_message(message, conn):
    message_json = json.dumps(message)
    message_bytes = message_json.encode('utf-8')
    head_len = struct.pack('i', len(message_bytes))
    conn.send(head_len)
    conn.send(message_bytes)


def get_md5(name, password):
    md = hashlib.md5()
    md.update(name.encode('utf-8'))
    md.update(password.encode('utf-8'))
    return md.hexdigest()


def login_outer(func):
    def inner(*args, **kwargs):
        message = args[0]
        conn = args[1]
        for v in user_info.live_user.values():
            if v[0] == message['session']:
                user_id = v[1]
                message['user_id'] = user_id
                break
        user_id = message.get('user_id', None)
        if user_id:
            func(*args, **kwargs)
        else:
            # start_size = 0
            # sum = b''
            # while start_size < message['file_size']:
            #     data = conn.recv(1024)
            #     start_size += len(data)
            #     sum = sum + data
            if message['type'] == 'upload_movie':
                file_path = os.path.join(settings.BASE_MOVIES_FALSE_DIR, message['file_name'])
                start_size = 0
                file_size = message['file_size']
                with open(file_path, 'wb') as f:
                    while start_size < file_size:
                        data = conn.recv(1024)
                        f.write(data)
                        start_size += len(data)
                    f.flush()
            send_dic = {'flag': False, 'msg': '请求非法,检测到非登录用户!'}
            send_message(send_dic, conn)

    return inner





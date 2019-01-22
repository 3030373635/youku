import hashlib
import struct
import json
import os
import time
from conf import settings


def progress_bar(percent, width=50):
    if percent > 1:
        percent = 1
    show_str = ('[%%-%ds]' % width) % (int(percent * width) * '#')
    print('\r%s %s%%' % (show_str, int(percent * 100)), end='')

def send_back_message(message, client, file_path=None):
    message_json = json.dumps(message)
    message_bytes = message_json.encode('utf-8')
    head_len = struct.pack('i', len(message_bytes))
    client.send(head_len)
    client.send(message_bytes)
    if file_path:
        total_size = message['file_size']
        start_size = 0
        with open(file_path, 'rb') as f:
            for line in f:
                client.send(line)
                start_size += len(line)
                percent = start_size / total_size
                progress_bar(percent)
            print()

    head_len = client.recv(4)
    message_len = struct.unpack('i', head_len)[0]
    message_bytes = client.recv(message_len)
    message = json.loads(message_bytes.decode('utf-8'))
    return message


def get_md5(data):
    md = hashlib.md5()
    md.update(data.encode('utf-8'))
    return md.hexdigest()


def get_dir_movie():
    return os.listdir(settings.BASE_UPLOAD_MOVIE_DIR)


def get_movie_md5(file_path):
    md = hashlib.md5()
    file_size = os.path.getsize(file_path)
    _ = [0, file_size // 2, file_size - 10]
    with open(file_path, 'rb') as f:
        for i in _:
            f.seek(i)
            md.update(f.read(10))
    return md.hexdigest()


def get_create_time():
    return time.strftime("%Y-%m-%d %X")

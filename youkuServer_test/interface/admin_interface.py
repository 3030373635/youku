from conf import settings
import os
from db import models
from lib import common


@common.login_outer
def upload_movie(message, conn):
    file_size = message['file_size']
    file_name = message['file_name']
    create_time = message['create_time']
    file_md5 = message['file_md5']
    is_free = message['is_free']
    is_delete = message['is_delete']
    file_path = os.path.join(settings.BASE_MOVIES_TRUE_DIR, file_name)
    start_size = 0
    with open(file_path, 'wb') as f:
        while start_size < file_size:
            data = conn.recv(1024)
            f.write(data)
            start_size += len(data)
        f.flush()

    movie = models.Movie(name=file_name,
                         path=file_path,
                         is_free=is_free,
                         is_delete=is_delete,
                         create_time=create_time,
                         user_id=message['user_id'],
                         file_md5=file_md5,
                         )
    movie.save()
    send_dic = {'flag': True, 'msg': '%s上传成功' % file_name}
    common.send_message(send_dic, conn)


@common.login_outer
def delete_file(message, conn):
    print(message)
    file_id = message['file_id']
    file_obj = models.Movie.select_one(id=file_id)
    file_obj.is_delete = 1
    file_obj.update()
    file_name = file_obj.name
    send_dic = {'flag': True, 'msg': '%s删除成功!' % file_name}
    common.send_message(send_dic, conn)


@common.login_outer
def release_notice(message, conn):
    name = message['name']
    content = message['content']
    create_time = message['create_time']
    user_id = message['user_id']
    notice = models.Notice(name=name, content=content, create_time=create_time, user_id=user_id)
    notice.save()
    send_dic = {'flag': True, 'msg': '公告发布成功!'}
    common.send_message(send_dic, conn)

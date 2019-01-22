from db import models
import os
from lib import common
from conf import settings

@common.login_outer
def download_movie(message, conn):
    file_id = message['file_id']
    user_id = message['user_id']

    file_obj = models.Movie.select_one(id=file_id)
    file_name = file_obj.name
    file_path = os.path.join(settings.BASE_MOVIES_TRUE_DIR, file_name)
    file_size = os.path.getsize(file_path)
    file_md5 = file_obj.file_md5
    send_dic = {'flag': True, 'msg': {
        'file_name': file_name,
        'file_size': file_size,
        'file_md5': file_md5,
    }}
    common.send_message(send_dic, conn)
    download_record = models.Download_record(user_id=user_id, movie_id=message['file_id'])
    download_record.save()
    with open(file_path, 'rb') as f:
        for line in f:
            conn.send(line)

@common.login_outer
def check_notice(message,conn):
    user_id = message['user_id']
    notice_obj_list = models.Notice.select_many(user_id=user_id)
    if notice_obj_list:
        notice_list = list()
        for notice_info in notice_obj_list:
            notice_list.append([notice_info.name,notice_info.content])
        send_dic = {
            'flag':True,
            'msg':notice_list
            }
    else:
        send_dic = {
            'flag': False,
            'msg': '暂时没有公告!'
        }
    common.send_message(send_dic, conn)


@common.login_outer
def check_movie_record(message,conn):
    user_id = message['user_id']
    movie_obj_list = models.Download_record.select_many(user_id=user_id)
    movie_info_list = list()
    if movie_obj_list:
        for movie in movie_obj_list:
            movie_obj = models.Movie.select_one(id=movie.movie_id)
            movie_info_list.append([movie_obj.name,'免费'if movie_obj.is_free else '收费'])
            send_dic = {'flag':'True','msg':movie_info_list}
    else:
        send_dic = {
            'flag':False,
            'msg':'没有观影记录'
        }
    common.send_message(send_dic,conn)
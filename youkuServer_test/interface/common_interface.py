from db import models
from lib import common
from tcpServer import user_info


def register(message, conn):
    name = message['name']
    user = models.UserInfo.select_one(name=name)
    if user:
        send_dic = {'flag': False, 'msg': '%s:%s 已经存在!' % (message['user_type'], user.name)}
    else:
        user = models.UserInfo(name=name,
                               password=message['password'],
                               is_vip=message['is_vip'],
                               locked=message['locked'],
                               user_type=message['user_type'],
                               )
        user.save()
        send_dic = {'flag': True, 'msg': '%s:%s 注册成功!' % (message['user_type'], user.name)}
    common.send_message(send_dic, conn)


def login(message, conn):
    name = message['name']
    password = message['password']
    user = models.UserInfo.select_one(name=name)
    if user:
        if user.user_type == message['user_type']:
            if user.password == password:
                send_dic = {'flag': True, 'msg': '%s:%s 登录成功' % (user.user_type, name)}
                session = common.get_md5(name, password)
                send_dic['session'] = session
                print(user_info.live_user, '<==')
                user_info.mutex.acquire()
                user_info.live_user[message['addr']] = [session, user.id]
                user_info.mutex.release()
                print(user_info.live_user, '<==')
            else:
                send_dic = {'flag': False, 'msg': '%s:%s 密码错误!' % (user.user_type, name)}
        else:
            send_dic = {'flag': False, 'msg': '%s不是%s用户!' % (user.name, message['user_type'])}
    else:
        send_dic = {'flag': False, 'msg': '%s:%s 不存在!' % (message['user_type'], name)}
    common.send_message(send_dic, conn)


@common.login_outer
def check_movie_list(message, conn):
    movie_obj_list = models.Movie.select_many()

    if movie_obj_list:
        back_movie = list()
        for movie_obj in movie_obj_list:
            if movie_obj.is_delete == 0:
                if message['movie_type'] == 'all':
                    back_movie.append([movie_obj.name, '免费' if movie_obj.is_free else '收费', movie_obj.id])
                elif message['movie_type'] == 'free':
                    if movie_obj.is_free == 1:
                        back_movie.append([movie_obj.name, '免费', movie_obj.id])
                else:
                    if movie_obj.is_free == 0:
                        back_movie.append([movie_obj.name, '收费', movie_obj.id])

        if back_movie:
            send_dic = {'flag': True, 'msg': back_movie}
        else:
            send_dic = {'flag': False, 'msg': '暂无电影!'}
    else:
        send_dic = {'flag': False, 'msg': '暂无电影!'}

    common.send_message(send_dic, conn)

@common.login_outer
def buy_member(message,conn):
    id = message['user_id']
    user_obj = models.UserInfo.select_one(id=id)
    user_obj.is_vip = 1
    user_obj.update()
    send_dic = {'flag':'True','msg':'%s:%s开通会员成功!' % (user_obj.user_type,user_obj.name)}
    common.send_message(send_dic,conn)
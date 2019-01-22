from lib import common
from tcpClient import tcpClient
from conf import settings
import os

user_dic = {
    'session': None
}


def user_register(client):
    while True:
        name = input("请输入用户名>>:")
        password_one = input("请输入密码>>:")
        password_two = input("请再次输入密码>>:")
        if password_two == password_one:
            send_dic = {
                'type': 'register',
                'name': name,
                'password': common.get_md5(password_one),
                'is_vip': 0,
                'locked': 0,
                'user_type': 'user',
            }
            back_dic = common.send_back_message(send_dic, client)
            if back_dic['flag']:
                print(back_dic['msg'])
                break
            else:
                print(back_dic['msg'])
        else:
            print("两次密码不一致!")


def user_login(client):
    if user_dic['session']:
        print("您已经登录!")
        return
    while True:
        name = input("请输入用户名>>:")
        password = input("请输入密码>>:")
        send_dic = {'type': 'login',
                    'name': name,
                    'password': common.get_md5(password),
                    'user_type': 'user'}
        back_dic = common.send_back_message(send_dic, client)
        if back_dic['flag']:
            print(back_dic['msg'])
            user_dic['session'] = back_dic['session']
            break
        else:
            print(back_dic['msg'])


def buy_member(client):
    temp = input("是否购买会员(y/n)?>>:")
    if temp == 'y':
        is_vip = 1
        send_dic = {'type': 'buy_member',
                    'session': user_dic['session'],
                    'is_vip': is_vip,
                    }
        back_dic = common.send_back_message(send_dic, client)
        if back_dic['flag']:
            print(back_dic['msg'])
        else:
            print(back_dic['msg'])
    else:
        print("购买会员失败!")
        return


def check_movie(client):
    # 查看所有没有被删除的视频
    send_dic = {
        'type': 'check_movie',
        'session': user_dic['session'],
        'movie_type': 'all',
    }
    back_dic = common.send_back_message(send_dic, client)
    if back_dic['flag']:
        movie_list = back_dic['msg']
        for num, movie_info in enumerate(movie_list):
            print("%s 电影名:%s %s" % (num, movie_info[0], movie_info[1]))
    else:
        print(back_dic['msg'])


def download_free_movie(client):
    send_dic = {
        'type': 'check_movie_list',
        'session': user_dic['session'],
        'movie_type': 'free',
    }
    back_dic = common.send_back_message(send_dic, client)
    if back_dic['flag']:
        movie_list = back_dic['msg']
        for num, movie_info in enumerate(movie_list):
            print("%s 电影名:%s %s" % (num, movie_info[0], movie_info[1]))
        choice = input("请选择要下载的文件(序号)>>:")
        if choice.isdigit():
            choice = int(choice)
            if choice < len(movie_list):
                send_dic = {
                    'type': 'download_movie',
                    'session': user_dic['session'],
                    'file_id': movie_list[choice][2]
                }
                back_dic = common.send_back_message(send_dic, client)
                if back_dic['flag']:
                    file_name = back_dic['msg']['file_name']
                    file_size = back_dic['msg']['file_size']
                    file_path = os.path.join(settings.BASE_DOWNLOAD_MOVIE_DIR, file_name)
                    start = 0
                    with open(file_path, 'wb') as f:
                        while start < file_size:
                            data = client.recv(1024)
                            f.write(data)
                            start += len(data)
                            _ = start / file_size
                            common.progress_bar(_)
                        f.flush()
                    print()
                    print("电影下载成功!")

                else:
                    print(back_dic['msg'])

            else:
                print("序号不正确!")
        else:
            print("请输入数字!")
    else:
        print(back_dic['msg'])


def download_charge_movie(client):
    send_dic = {
        'type': 'check_movie_list',
        'session': user_dic['session'],
        'movie_type': 'charge',
    }
    back_dic = common.send_back_message(send_dic, client)
    if back_dic['flag']:
        movie_list = back_dic['msg']
        for num, movie_info in enumerate(movie_list):
            print("%s 电影名:%s %s" % (num, movie_info[0], movie_info[1]))
        choice = input("请选择要下载的文件(序号)>>:")
        if choice.isdigit():
            choice = int(choice)
            if choice < len(movie_list):
                send_dic = {
                    'type': 'download_movie',
                    'session': user_dic['session'],
                    'file_id': movie_list[choice][2]
                }
                back_dic = common.send_back_message(send_dic, client)
                if back_dic['flag']:
                    file_name = back_dic['msg']['file_name']
                    file_size = back_dic['msg']['file_size']
                    file_path = os.path.join(settings.BASE_DOWNLOAD_MOVIE_DIR, file_name)
                    start = 0
                    with open(file_path, 'wb') as f:
                        while start < file_size:
                            data = client.recv(1024)
                            f.write(data)
                            start += len(data)
                            _ = start / file_size
                            common.progress_bar(_)
                        f.flush()
                    print()
                    print("电影下载成功!")
                else:
                    print(back_dic['msg'])
            else:
                print("序号不正确!")
        else:
            print("请输入数字!")
    else:
        print(back_dic['msg'])


def check_movie_record(client):
    send_dic = {
        'type':'check_movie_record',
        'session':user_dic['session'],
    }
    back_dic = common.send_back_message(send_dic,client)
    if back_dic['flag']:
        movie_info_list = back_dic['msg']
        for num,movie_info in enumerate(movie_info_list):
            print('%s 电影名:%s %s' % (num,movie_info[0],movie_info[1]))
    else:
        print(back_dic['msg'])


def check_notice(client):
    send_dic = {'type':'check_notice','session':user_dic['session']}
    back_dic = common.send_back_message(send_dic,client)
    if back_dic['flag']:
        notice_list = back_dic['msg']
        for num,notice_info in enumerate(notice_list):
            print("%s 公告名:%s 公告内容:%s" % (num,notice_info[0],notice_info[1]))
    else:
        print(back_dic['msg'])


func_dic = {
    '1': user_register,
    '2': user_login,
    '3': buy_member,
    '4': check_movie,
    '5': download_free_movie,
    '6': download_charge_movie,
    '7': check_movie_record,
    '8': check_notice,
}


def user_view():
    client = tcpClient.get_client()
    while True:
        print("""
        1 注册
        2 登录
        3 购买会员
        4 查看视频
        5 下载免费视频
        6 下载收费视频
        7 查看观影记录
        8 查看公告
        """)
        choice = input("请选择>>:")
        if choice not in func_dic: continue
        func_dic[choice](client)

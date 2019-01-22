from tcpClient import tcpClient
from lib import common
import os
from conf import settings

user_dic = {
    'session': None
}


def admin_register(client):
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
                'user_type': 'admin',
            }
            back_dic = common.send_back_message(send_dic, client)
            if back_dic['flag']:
                print(back_dic['msg'])
                break
            else:
                print(back_dic['msg'])
        else:
            print("两次密码不一致!")


def admin_login(client):
    if user_dic['session']:
        print("您已经登录!")
        return
    while True:
        name = input("请输入用户名>>:")
        password = input("请输入密码>>:")
        send_dic = {'type': 'login', 'name': name, 'password': common.get_md5(password), 'user_type': 'admin'}
        back_dic = common.send_back_message(send_dic, client)
        if back_dic['flag']:
            print(back_dic['msg'])
            user_dic['session'] = back_dic['session']
            break
        else:
            print(back_dic['msg'])


def upload_movie(client):
    file_list = common.get_dir_movie()
    if file_list:
        for num, movie in enumerate(file_list):
            print(num, movie)
        choice = input("请选择要上传的文件(序号)>>:")
        if choice.isdigit():
            choice = int(choice)
            if choice < len(file_list):
                is_free = input("是否免费(y/n)>>:")
                if is_free == 'y':
                    is_free = 1
                else:
                    is_free = 0
                file_name = file_list[choice]
                file_path = os.path.join(settings.BASE_UPLOAD_MOVIE_DIR, file_name)
                file_size = os.path.getsize(file_path)
                file_md5 = common.get_movie_md5(file_path)
                create_time = common.get_create_time()
                is_free = is_free
                is_delete = 0
                send_dic = {
                    'type': 'upload_movie',
                    'session': user_dic['session'],
                    'file_name': file_name,
                    'file_size': file_size,
                    'file_md5': file_md5,
                    'is_free': is_free,
                    'is_delete': is_delete,
                    'create_time': create_time,
                }
                back_dic = common.send_back_message(send_dic, client,file_path)
                if back_dic['flag']:
                    print(back_dic['msg'])
                else:
                    print(back_dic['msg'])
            else:
                print("输入数字超出文件序号")
        else:
            print("请输入数字!")
    else:
        print("当前没有待上传文件")



def delete_movie(client):
    # 打印数据库中没有被删除的文件还有哪些
    send_dic = {
        'type':'check_movie_list',
        'session':user_dic['session'],
        'movie_type':'all'
    }
    back_dic = common.send_back_message(send_dic,client)
    if back_dic['flag']:
        file_info = back_dic['msg']
        for num,movie_info in enumerate(file_info):
            print("%s 电影名:%s %s" % (num,movie_info[0],movie_info[1]))
        choice = input("请选择要删除的文件(序号)>>:")
        if choice.isdigit():
            choice = int(choice)
            if choice < len(file_info):
                send_dic = {
                    'type':'delete_file',
                    'session':user_dic['session'],
                    'file_id':file_info[choice][2],
                }
                back_dic = common.send_back_message(send_dic,client)
                if back_dic['flag']:
                    print(back_dic['msg'])
                else:
                    print(back_dic['msg'])
            else:
                print("序号不正确!")
        else:
            print("请输入序号!")

    else:
        print(back_dic['msg'])



def release_notice(client):
    name = input("请输入公告标题>>:")
    content = input("请输入公告内容>>:")
    send_dic = {'type':'release_notice',
                'session':user_dic['session'],
                'name':name,
                'content':content,
                'create_time':common.get_create_time()
                }
    back_dic = common.send_back_message(send_dic,client)
    if back_dic['flag']:
        print(back_dic['msg'])
    else:
        print(back_dic['msg'])



func_dic = {
    '1': admin_register,
    '2': admin_login,
    '3': upload_movie,
    '4': delete_movie,
    '5': release_notice,
}


def admin_view():
    client = tcpClient.get_client()
    while True:
        print("""
        1 注册
        2 登录
        3 上传视频
        4 删除视频
        5 发布公告
        """)
        choice = input("请选择功能>>:")
        if choice == 'q': break
        if choice not in func_dic: continue
        func_dic[choice](client)

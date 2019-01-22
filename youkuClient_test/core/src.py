from core import admin,user
func_dic = {
    '1':admin.admin_view,
    '2':user.user_view,
}

def run():
    while True:
        print("""
        1 管理员视图
        2 用户视图
        """)
        choice = input("请选择>>:")
        if choice not in func_dic:continue
        func_dic[choice]()
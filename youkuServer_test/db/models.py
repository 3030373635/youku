from orm_pool.orm import Models, StrField, IntField


class UserInfo(Models):
    table_name = 'userinfo'
    id = IntField('id', primary_key=True)
    name = StrField('name')
    password = StrField('password')
    is_vip = IntField('is_vip')
    locked = IntField('locked')
    user_type = StrField('user_type')


class Movie(Models):
    table_name = 'movie'
    id = IntField('id', primary_key=True)
    name = StrField('name')
    path = StrField('path')
    is_free = IntField('is_free')
    is_delete = IntField("is_delete")
    create_time = StrField("create_time")
    user_id = IntField('user_id')
    file_md5 = StrField('file_md5')


class Notice(Models):
    table_name = 'notice'
    id = IntField('id', primary_key=True)
    name = StrField('name')
    content = StrField('content')
    create_time = StrField('create_time')
    user_id = IntField('user_id')


class Download_record(Models):
    table_name = 'download_record'
    id = IntField('id',primary_key=True)
    user_id = IntField('user_id')
    movie_id = IntField("movie_id")

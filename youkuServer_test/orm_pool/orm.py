from orm_pool import mysql_class


class Field:
    def __init__(self, name, primary_key, column_type, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default


class StrField(Field):
    def __init__(self, name, primary_key=False, column_type='varchar(200)', default=None):
        super(StrField, self).__init__(name, primary_key, column_type, default)


class IntField(Field):
    def __init__(self, name, primary_key=False, column_type='int', default=0):
        super(IntField, self).__init__(name, primary_key, column_type, default)


class ModelsMetaClass(type):
    def __new__(cls, class_name, class_bases, class_dic):
        if class_name == 'Models':
            return type.__new__(cls, class_name, class_bases, class_dic)
        primary_key = None
        table_name = class_dic.get('table_name', None)
        mappings = dict()
        for k, v in class_dic.items():
            if isinstance(v, Field):
                mappings[k] = v
                if v.primary_key:
                    primary_key = v.name
        for k in mappings.keys():
            class_dic.pop(k)
        class_dic['table_name'] = table_name
        class_dic['primary_key'] = primary_key
        class_dic['mappings'] = mappings
        return type.__new__(cls, class_name, class_bases, class_dic)


class Models(dict, metaclass=ModelsMetaClass):
    def __init__(self, **kwargs):
        super(Models, self).__init__(**kwargs)

    def __getattr__(self, item):
        try:
            return self[item]
        except Exception:
            print("%s对象没有%s属性" % (self.name, item))

    def __setattr__(self, key, value):
        self[key] = value

    @classmethod
    def select_one(cls, **kwargs):
        ms = mysql_class.Mysql()
        key = list(kwargs.keys())[0]
        value = kwargs[key]
        sql = 'select * from %s where %s=?' % (cls.table_name, key)
        sql = sql.replace('?', '%s')
        user_obj = ms.select(sql, value)
        if user_obj:
            return cls(**user_obj[0])
        else:
            return None

    @classmethod
    def select_many(cls, **kwargs):
        ms = mysql_class.Mysql()
        if kwargs:
            key = list(kwargs.keys())[0]
            value = kwargs[key]
            sql = 'select * from %s where %s =?' % (cls.table_name, key)

            sql = sql.replace('?', '%s')
            obj_list = ms.select(sql, value)
        else:
            sql = 'select * from %s' % (cls.table_name)
            obj_list = ms.select(sql)
        if obj_list:

            return [cls(**obj) for obj in obj_list]
        else:
            return None

    def update(self):
        ms = mysql_class.Mysql()
        pr_value = None
        keys = list()
        values = list()
        for v in self.mappings.values():
            if v.primary_key:
                pr_value = getattr(self, v.name)
            else:
                keys.append(v.name + '=%s')
                values.append(getattr(self, v.name))
        sql = 'update %s set %s where %s = %s' % (self.table_name, ','.join(keys), self.primary_key, pr_value)
        ms.execute(sql, values)

    def save(self):
        ms = mysql_class.Mysql()
        keys = list()
        values = list()
        _ = list()
        for v in self.mappings.values():
            if not v.primary_key:
                keys.append(v.name)
                values.append(getattr(self, v.name))
                _.append('?')
        sql = 'insert into %s(%s) values(%s)' % (self.table_name, ','.join(keys), ','.join(_))
        sql = sql.replace('?', '%s')
        ms.execute(sql, values)


class UserInfo(Models):
    table_name = 'userinfo'
    id = IntField('id', primary_key=True)
    name = StrField('name')
    password = StrField('password')
    is_vip = IntField('is_vip')
    locked = IntField('locked')
    user_type = StrField('user_type')


if __name__ == '__main__':
    user = UserInfo(name='tt', password="223", is_vip=0, locked=0, user_type="admin")
    user.save()

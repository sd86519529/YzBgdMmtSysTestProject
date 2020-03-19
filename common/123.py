class Config:
    name = '测试'
    age = '18'


def encode(func):
    def wrapper(*args, **kwargs):
        print('encode')
        func(*args, **kwargs)

    return wrapper


class MyClass:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance.__eq__(None):
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self) -> str:
        return '%s,%s' % ('我改变', '了类的返回')

    @encode
    def encode_test(self):
        print('name:%s,age:%s' % (self.name, self.age))
        raise BaseException('你触发了异常')

    @classmethod
    def class_method(cls):
        if hasattr(cls, 'encode_test').__eq__(True):
            _cls = cls(Config.name, Config.age)
            return _cls, _cls.encode_test()

    @staticmethod
    def static_method():
        print('i am xia ba oo')

    @staticmethod
    def fibonacci(n):  # 生成器函数 - 斐波那契
        __a, b, __counter = 0, 1, 0
        while True:
            if int(__counter) > int(n):
                return
            yield __a
            __a, b = b, __a + b
            __counter += 1


if __name__ == '__main__':
    try:
        a = MyClass('测试', '18')
        print(a)
        print(a.class_method())
    except BaseException as e:
        print('文件：%s,\r\n行数： %s,\r\n错误内容： %s' % (
            e.__traceback__.tb_frame.f_globals['__file__'], e.__traceback__.tb_lineno, e))
    import sys

    a = MyClass('测试', '18')
    f = a.fibonacci(10)  # f 是一个迭代器，由生成器返回生成

    while True:
        try:
            print(next(f), end=" ")
        except StopIteration:
            sys.exit()

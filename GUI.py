class app:
    def __init__(self, test=None):
        self.test = test
        self.test.a = 20

class test:
    def __int__(self, a=None):
        self.a = a


if __name__ == '__main__':
    a = app(test())
    print(a.test.a)
    a.
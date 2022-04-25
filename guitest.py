import tkinter


class app:
    def __init__(self, test=0):
        """
        :param test:
        """
        self.flag = test
    def test(self):
        print(self.flag)



if __name__ == '__main__':
    # a = tkinter.Tk()
    # a.title('test')
    # a.mainloop()
    a = app(test='asd')
    a.test()
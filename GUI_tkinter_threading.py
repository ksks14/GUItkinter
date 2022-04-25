import time
import tkinter
import cv2 as cv
import PIL.Image, PIL.ImageTk
import threading


class Mythread(threading.Thread):
    """
    这里自己构建一个类去继承原来的thread
    """
    def __init__(self, func, args):
        super(Mythread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)


    def get_result(self):
        try:
            return self.result
        except Exception as e:
            return None

class Myapp:
    def __init__(self, window, title, frame, img_height=400, img_width=640, video_source=''):
        """

        :param window:
        :param title:
        :param img_height:
        :param img_width:
        """
        # predefine
        self.flag = 1
        self.delay = 27
        self.canvas1 = None
        self.canvas2 = None
        # load the video and get the width and height
        self.vid = Myvideo(video_source)
        self.IMG_HEIGHT = (self.vid.height + 10) // 2
        self.IMG_WIDTH = (self.vid.width + 10) // 2
        # make the window
        self.window = window
        self.window.title = title
        # make a location
        self.window.geometry(
            "%dx%d+%d+%d" % (self.IMG_WIDTH * 2, self.IMG_HEIGHT, (window.winfo_screenwidth() - self.IMG_WIDTH) / 2,
                             (window.winfo_screenheight() - self.IMG_HEIGHT) / 2 - 10))  # 窗口至指定位置
        self.add_frame_to_window(frame)
        self.add_canvas_to_window()

        self.hading_img(flag=1)
        # running
        self.update()
        self.window.mainloop()

    def add_frame_to_window(self, frame):
        """

        :param frame:
        :return:
        """
        frame_1 = frame(self.window)
        frame_1.pack(side='left', padx=10)
        # tkinter.Button(frame_1, text="启动", height=2, width=10, command=self.test_job).pack(side="top")
        tkinter.Button(frame_1, text="暂停", height=2, width=10, command=self.pause).pack(side="top")
        tkinter.Button(frame_1, text="恢复", height=2, width=10, command=self.play).pack(side="top")
        tkinter.Button(frame_1, text="结束线程", height=2, width=10, command=self.test_job).pack(side="top")
        tkinter.Button(frame_1, text="退出程序", height=2, width=10, command=self.window.quit).pack(side="top")

    def add_canvas_to_window(self):
        """
        这里直接传入了
        :return:
        """
        self.canvas1 = tkinter.Canvas(self.window, bg="#c4c2c2", height=(self.IMG_HEIGHT - 100) // 2,
                                      width=self.IMG_WIDTH // 2)  # 绘制画布
        self.canvas1.pack(side="left")
        self.canvas2 = tkinter.Canvas(self.window, bg="#c4c2c2", height=(self.IMG_HEIGHT - 100) // 2,
                                      width=self.IMG_WIDTH // 2)  # 绘制画布
        self.canvas2.pack(side="right")

    def hading_img(self, flag=0):
        """
        在一个类中，photoimage in Tk() tkinter.tk()
        :param flag:
        :return:
        """
        frame = self.vid.get_frame()
        if flag:
            return cv.flip(frame, 0)
        else:
            return frame


    def update(self):
        """
        in tk() to canvas
        没有wait() error
        没有考虑死锁
        :return:
        """
        frame = self.vid.get_frame()
        th_2 = Mythread(self.hading_img,args=(1, ))
        try:
             th_2.start()
        except Exception as e:
             print(e)
        try:
            th_2.join()
        except Exception as e:
            print(e)
        self.photo_src = PIL.ImageTk.PhotoImage(
             image=PIL.Image.fromarray(frame).resize((int(self.IMG_WIDTH) // 2, int(self.IMG_HEIGHT - 100) // 2)))
        self.photo_dst = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(th_2.get_result()).resize((int(self.IMG_WIDTH) // 2, int(self.IMG_HEIGHT - 100) // 2)))
        self.canvas1.create_image(0, 0, image=self.photo_src, anchor=tkinter.NW)
        self.canvas2.create_image(0, 0, image=self.photo_dst, anchor=tkinter.NW)
        # 这个方向调用线程库，即使暂停，也不可暂停对视频的推理，实现一个缓冲的功能。
        # 设置暂停播放flag
        if self.flag:
            self.window.after(self.delay, self.update)

    def test_thread(self, print_str):
        """

        :param print_str:
        :return:
        """
        print(print_str)

    def start_thread(self):
        """

        :return:
        """
        pass

    def pause(self):
        """

        :return:
        """
        self.flag = 0

    def play(self):
        """

        :return:
        """
        self.flag = 1
        self.window.after(self.delay, self.update)

    def test_job(self):
        """

        :return:
        """
        pass


class Myvideo:
    def __init__(self, video_source=''):
        """

        :param video_source:
        """
        self.vid = cv.VideoCapture(0 if not video_source else video_source)
        if not self.vid.isOpened():
            raise ValueError('unable to open video source!', video_source)
        # return width and height
        self.width = self.vid.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            else:
                return None
        return None


if __name__ == '__main__':
    app = Myapp(window=tkinter.Tk(), title='test', frame=tkinter.Frame, video_source='test.mp4')

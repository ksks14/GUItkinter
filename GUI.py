import tkinter
import cv2 as cv
import PIL.Image, PIL.ImageTk


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
        self.delay = 15
        self.canvas1 = None
        self.canvas2 = None
        self.IMG_HEIGHT = img_height * 2 + 100
        self.IMG_WIDTH = img_width * 2 + 100
        # make the window
        self.window = window
        self.window.title = title
        # make a location
        self.window.geometry(
            "%dx%d+%d+%d" % (self.IMG_WIDTH, self.IMG_HEIGHT, (window.winfo_screenwidth() - self.IMG_WIDTH) / 2,
                             (window.winfo_screenheight() - self.IMG_HEIGHT) / 2 - 50))  # 窗口至指定位置
        self.add_frame_to_window(frame)
        self.add_canvas_to_window()
        # make video
        self.vid = Myvideo(video_source)
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

        :return:
        """
        self.canvas1 = tkinter.Canvas(self.window, bg="#c4c2c2", height=self.IMG_HEIGHT - 100,
                                      width=self.IMG_WIDTH / 2)  # 绘制画布
        self.canvas1.pack(side="left")
        self.canvas2 = tkinter.Canvas(self.window, bg="#c4c2c2", height=self.IMG_HEIGHT - 100,
                                      width=self.IMG_WIDTH / 2)  # 绘制画布
        self.canvas2.pack(side="right")

    def update(self):
        """

        :return:
        """
        frame = self.vid.get_frame()
        self.photo = PIL.ImageTk.PhotoImage(
            image=PIL.Image.fromarray(frame).resize((self.IMG_WIDTH // 2, self.IMG_HEIGHT - 100)))
        self.canvas1.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.canvas2.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        # 设置暂停播放flag
        if self.flag:
            self.window.after(self.delay, self.update)

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

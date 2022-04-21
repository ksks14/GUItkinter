import time
import tkinter
import cv2 as cv
import PIL.Image, PIL.ImageTk


class App:
    def __init__(self, window, window_title, video_source=''):
        self.photo = None
        # 构建窗口
        self.window = window
        self.window.title = window_title
        # 加载视频资源
        self.video_source = 0 if not video_source else video_source
        self.vid = myvideocapture(self.video_source)
        self.canvas = tkinter.Canvas(window, width=self.vid.width, height=self.vid.height, )
        self.canvas.pack()
                
        # add a button
        self.btn_pause = tkinter.Button(window, text='pause', width=50, command=self.pause)
        self.btn_pause.pack(anchor=tkinter.CENTER, fill=tkinter.X, side=tkinter.RIGHT, expand=True)
        self.btn_play = tkinter.Button(window, text='play', width=50, command=self.play)
        self.btn_play.pack(anchor=tkinter.CENTER, fill=tkinter.X, side=tkinter.LEFT, expand=True)
        # flag control video player
        self.flag = 1
        self.delay = 15
        self.update()
        self.window.mainloop()

    def update(self):
        """

        :return:
        """
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
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


class myvideocapture:
    def __init__(self, vid_source=''):
        self.vid = cv.VideoCapture(0) if not vid_source else cv.VideoCapture(vid_source)
        if not self.vid.isOpened():
            raise ValueError('unable to open video source!', vid_source)
        self.width = self.vid.get(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv.CAP_PROP_FRAME_HEIGHT)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

    def get_frame(self):
        if self.vid.isOpened():
            ret, frame = self.vid.read()
            if ret:
                return (ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return None


if __name__ == '__main__':
    app = App(tkinter.Tk(), "tkinter player", 'test.mp4')

# coding=utf-8
import subprocess
import signal
qr_is_ok = False


# 信号处理函数
def receive_qr_status(signum, handler):
    # print("start", signum, handler)
    global qr_is_ok
    qr_is_ok = True    # 接受到信号，就改变一个标志，便于后面加载二维码

# def receive_login_status(signum, handler):
#     print('登录OK')


# 绑定信号到处理函数
# signal.signal(30, receive_login_status)
signal.signal(31, receive_qr_status)
process = subprocess.Popen(['python', 'webprocess.py'], stdout=subprocess.PIPE, stdin=subprocess.PIPE)

# 如果二维码没有加载，就一直死循环，直到qr_is_ok状态改变
while not qr_is_ok:
    pass

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.label import Label
from kivy.uix.splitter import Splitter
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Color
from kivy.graphics import Rectangle



# 登录二维码显示组件
class LoginView(Image):
    def __init__(self, **kwargs):
        super(LoginView, self).__init__(**kwargs)       # 调用父类构造器初始化
        self.source = './tmp/pp.png'                    # 显示子进程模块下载好的二维码


# 登录二维码显示屏幕（主要用于管理）
class LoginScreen(Screen):
    # 一个显示二维码的图像组件
    view = LoginView()

    def __init__(self, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)     # 调用父类构造器来初始化
        with self.canvas:
            Color(0, 0, 255, 255)       # 设置背景颜色
            Rectangle(pos=(0, 0), size=Window.size)     # 绘制背景
        self.add_widget(self.view)      # 添加二维码组件到屏幕


# 功能主屏幕
class MainScreen(Screen):
    # 简单使用一个标签组件来显示登录成功的消息
    label = Label(text='可以微信了')
    label2 = Label(text='可以!')
    grid_layout = GridLayout(rows=1, cols=2)
    splitter = Splitter()

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)  # 调用父类构造器来初始化
        with self.canvas:
            Color(0, 255, 255, 255)     # 背景颜色
            Rectangle(pos=(0, 0), size=Window.size)
        self.label.font_size = 100      # 字体大小
        # self.add_widget(self.label)     # 添加一个显示信息的标签组件
        self.splitter.strip_size = '2pt'
        self.splitter.size_hint = (0.7, 1.0)
        self.splitter.keep_within_parent = True
        # self.splitter.max_size = 900
        # self.splitter.min_size = 600
        self.splitter.add_widget(self.label2)
        self.grid_layout.add_widget(self.label)
        self.grid_layout.add_widget(self.splitter)
        self.add_widget(self.grid_layout)



# 应用模块
class AIApp(App):
    # manager = ScreenManager(transition=FadeTransition(duration=0.4))
    # SlideTransition
    # 创建屏幕管理器
    manager = ScreenManager(transition=FadeTransition(duration=3))
    # 登录屏幕
    login_screen = LoginScreen()
    # 功能主屏幕
    main_screen = MainScreen()

    # 构建整个界面UI
    def build(self):
        self.login_screen.name = 'login'  # 设置一个name，便于识别调用
        self.main_screen.name = 'main'    # 设置一个name，便于识别调用
        self.manager.add_widget(self.login_screen)  # 把屏幕加入屏幕管理器
        self.manager.add_widget(self.main_screen)   # 把屏幕加入屏幕管理器
        self.manager.current = 'login'              # 程序启动默认是登录二维码屏幕
        return self.manager         # 返回管理器作为主窗体

    # 接收子进程发来登录成功的消息
    def handle_login_status(self, signum, handler):
        # print('登录完毕', signum, handler)
        # Window.fullscreen = 'auto'    # 用来设置全屏
        self.manager.current = 'main'   # 登录成功切换屏幕到主功能屏幕


# 创建应用对象
app = AIApp()
app.title = '马哥版微信-登录'
Window.size = (600, 400)    # 设置窗体大小
signal.signal(30, app.handle_login_status)   # 绑定30信号，用来接收登录成功的通知
app.run()

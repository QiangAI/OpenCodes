from kivy.app import App
from kivy.core.window import Window
from kivy.uix.image import Image
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import FadeTransition
from kivy.uix.label import Label
from kivy.uix.splitter import Splitter
from kivy.uix.gridlayout import GridLayout
from kivy.adapters.listadapter import ListAdapter
from kivy.uix.listview import ListItemButton, ListView, ListItemLabel
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
    data = [{'text': str(i), 'is_selected': False} for i in range(100)]

    args_converter = lambda row_index, rec: {'text': rec['text'],
                                             'size_hint_y': None,
                                             'height': 40,
                                             'color': (1, 0, 0, 1),
                                             'text_size':(300, None)}
    list_adapter = ListAdapter(data=data,
                               args_converter=args_converter,
                               cls=ListItemButton,
                               selection_mode='single',
                               allow_empty_selection=False)

    list_view = ListView(adapter=list_adapter)

    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)  # 调用父类构造器来初始化
        with self.canvas:
            Color(0, 255, 255, 255)     # 背景颜色
            Rectangle(pos=(0, 0), size=Window.size)
        self.label.font_size = 100      # 字体大小
        # self.add_widget(self.label)     # 添加一个显示信息的标签组件
        self.list_view.size_hint = (0.3, 1.0)
        self.splitter.strip_size = 5
        self.splitter.size_hint = (0.7, 1.0)
        self.splitter.keep_within_parent = True
        self.splitter.max_size = 900
        self.splitter.min_size = 600
        self.splitter.add_widget(self.label2)
        self.grid_layout.add_widget(self.list_view)
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
        # self.manager.add_widget(self.login_screen)  # 把屏幕加入屏幕管理器
        self.manager.add_widget(self.main_screen)   # 把屏幕加入屏幕管理器
        self.manager.current = 'main'              # 程序启动默认是登录二维码屏幕
        return self.manager         # 返回管理器作为主窗体



# 创建应用对象
app = AIApp()
app.title = '马哥版微信-登录'
Window.size = (600, 400)    # 设置窗体大小
app.run()

# coding = utf-8
import itchat
import os
# 保存UUID，用于登录凭证
UUID = None


# 微信登录二维码回调函数
def qr_call(uuid, status, qrcode):
    global UUID
    UUID = uuid    # 保存登录产生的UUID
    # 二进制打开文件
    with open("./tmp/pp.png", "bw") as fd:
        fd.write(qrcode)    # 直接保存二维码图像
        fd.flush()          # 强制输出缓存
        fd.close()          # 关闭文件
    print('保存二维码完毕')
    os.kill(os.getppid(), 31)   # 给父进程发一个信号，告诉父进程可以加载二维码进行登录扫描


# 登录成功的回调函数
def login_call():
    print('登录完毕')
    global UUID
    if itchat.check_login(uuid=UUID) == '200':  # 检测UUID是否登录成功
        os.kill(os.getppid(), 30)   # 发送一个信号告诉父进程，已经登录成功，父进程切入到功能界面


# 微信登录接口调用
itchat.auto_login(
    hotReload=False,
    qrCallback=qr_call,         # 登录二维码下载回调函数设置
    loginCallback=login_call)   # 登录成功回调函数设置
print('webchat进程结束')

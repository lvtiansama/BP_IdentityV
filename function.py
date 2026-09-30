import sys
import os
import json
from PIL import Image, ImageDraw, ImageFont, ImageTk
from tkinter import messagebox
import ctypes


# 版本信息
def show_message():
    messagebox.showinfo("第五人格BP系统 V1.5.3", '''1.5.3
修复：
1.修复了一处坐标错误。
2.修复了一处框架逻辑错误，或许这一修复可以让程序变得流畅，或许控制台不再会无法移动。（这不确定，欢迎大家测试反馈）
3.修复了模糊搜索会丢失“lock”的问题。
4.修复了一处定时任务异常堆积的错误。
    
V1.5.2
修复：
1.修复了中文输入法会把小写字母”y“的ASCII码121当作keycode回传给tkinter库，导致程序误以为用户按下了”f10“（keycode=121）导致输入框失去焦点，再次会触发系统菜单。
这一bug涉及到Windows系统的底层，与上一个全屏bug不同，f10的这个功能并非我想实现的，我没有给它绑定任何函数，我不能在不存在的函数中增加判断语句。因此我直接禁用了f10。

    
V1.5.1
修复：
1.修复了中文输入法会把小写字母”z“的ASCII码122当作keycode回传给tkinter库，导致程序误以为用户按下了”f11“（keycode=122）导致程序切换全屏。
修复方案为在全屏函数内增加判断，判断用户是否真实按下f11而非中文输入法返回了ascii码。


V1.5:
常规更新：
1、角色库更新了`火灾调查员`、`“法罗女士”`
2、 地图更新了：`白沙街疯人院`、`闪金石窟`、`不归林`、`克雷伯格赛马场`

新增功能：
1、倒计时开关 可以在不需要的情况下将倒计时功能关闭。
2、”上传新数据“功能，在版本中，你可以自由添加角色、地图、战队logo，还可以一键清除缓存数据。
3、新增”模糊搜素“功能，支持控制台左侧30个选择框，以爱哭鬼为例，你可以输入”akg“、”aiku“、”aikugui“、”爱“等进行模糊搜素，输入关键词后回车即可快速帮你在数据库中找到结果。

优化：
1、将战队logo上传与”上传新数据“功能合并。
2、你将不需要输入战队名称，选择logo时会自动帮你填充战队名。
3、优化了一处逻辑，现在，你在输入过程时、或者输入错误名称时画面不会发生闪烁。（在旧版中，如果角色选择栏输入了错误的角色名称，例如盲女在输入了一半只有盲一个字的情况下，会导致画面丢失并报错。）
当然，你想要正确的刷新直播画面还是需要将错误的名称改正，本优化只优化了”闪烁“问题，并不会帮你自动更正错误。

修复：
1、修复了一处全局变量错误。
2、修复了在塔罗模式下，pick”心理学家“会导致程序卡死、画面丢失的异常。

已知的问题：
在未知情况下，会有概率出现控制台和直播画面窗口无法被拖动的情况（功能按键未卡死，可以正常使用），这一情况不会存在任何报错，因此我不能将该问题复现，也无法溯源，因此暂时无法将它修复，怀疑是tk库的底层逻辑不好导致交互监听事件异常失效。
解决和避免的方案：直播画面窗口可以通过两次f11切换全屏来刷新窗口、或者关闭直播窗口重启解决该问题。控制台窗口只能整个程序重启来解决，因此请将控制台窗口放在屏幕中心，确保即使不能移动时，你也可以正常操作控制台。


快捷键（仅限BP窗口）： F11全屏 ESC退出

项目版权说明：
1、默认bp界面背景素材来源于：第五人格2019IVC冬季精英赛淘汰赛
2、界面内所有角色、地图素材来源于《网易第五人格》（网易公司版权所有 ©1997-2023）
  感谢wiki.biligame.com提供了素材
3、本项目使用了以下项目：
  Azure-ttk-theme-2.1.0（作者：rdbende，MIT开源协议）
  项目地址：https://github.com/rdbende/ttk-widget-factory
4、本项目（BP_IdentityV）源代码基于 MIT 协议开源，详见 LICENSE 文件
5、角色、地图等美术素材版权归《网易第五人格》所有，不在 MIT 协议覆盖范围内
6、如果你在使用过程中遇到问题，可以提交反馈寻求我的帮助

作者：@绿天sama
Github：https://github.com/lvtiansama
CSDN：https://blog.csdn.net/lvtiansama
哔哩哔哩：https://space.bilibili.com/88004482
''')

fullbool = False

def my_subprogram(data):
    global fullbool
    # 在子程序中使用 data
    fullbool = data

# 全屏数据转换 0为宽，1为高,2为字体，理论上字体与宽的缩放比一致
def fullcounter(num, bool):
    global fullbool
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)
    if fullbool == True:
        if bool == 0:
            num = num / 1760 * screen_width
        elif bool == 1 or bool == 2:
            num = num / 990 * screen_height
        num = round(num)
    return num


def bp_text(text, size, fill_color=(14, 4, 0)):
    image = text_to_transparent_image(text, get_resource_path("fonts/华康POP.ttf"), fullcounter(size, 2), fill_color)
    photo = ImageTk.PhotoImage(image)
    return photo

def bp_bmap(data, x, y):
    path = get_path(data, 'map')
    image = Image.open(path).convert("RGBA")  # 打开图像并转换为RGBA模式
    image = image.resize((fullcounter(x, 0), fullcounter(y, 1)))
    photo = ImageTk.PhotoImage(image)
    if data != '':
        path_l = get_resource_path('data/maplock.png')
    else:
        path_l = get_resource_path('data/nothing.png')
    image_l = Image.open(path_l).convert("RGBA")  # 打开图像并转换为RGBA模式
    photo_l = ImageTk.PhotoImage(image_l)
    return photo, photo_l

def bp_bper(data, place, x, y):
    path = get_path(data, place)
    image = Image.open(path).convert("RGBA")  # 打开图像并转换为RGBA模式
    image = image.resize((fullcounter(x, 0), fullcounter(y, 1)))
    photo = ImageTk.PhotoImage(image)
    if data == 'lock':
        path_l = get_resource_path('data/banlock.png')
        image_l = Image.open(path_l).convert("RGBA")
        image_l = image_l.resize((fullcounter(x, 0), fullcounter(y, 1)))
    elif data != '':
        path_l = get_resource_path('data/ban.png')
        image_l = Image.open(path_l).convert("RGBA")
        image_l = image_l.resize((fullcounter(x, 0), fullcounter(y, 1)))
    else:
        path_l = get_resource_path('data/nothing.png')
        image_l = Image.open(path_l).convert("RGBA")
    photo_l = ImageTk.PhotoImage(image_l)
    return photo, photo_l

def bp_other(data, place, y):
    dic_logo = get_logo_json()
    if place == 'teamlogo':
        if data != '':
            path = os.path.join("C:\\BP_IdentityV\\", dic_logo[data]["path"])
            # print(path)
        else :
            path = get_resource_path('data/nothing.png')
    else:
        path = get_path(data, place)
    image = Image.open(path).convert("RGBA")  # 打开图像并转换为RGBA模式
    # 计算新的宽度，保持纵横比
    width, height = image.size
    aspect_ratio = width / height
    new_width = int(fullcounter(y, 1) * aspect_ratio)
    # 调整图像大小（按比例缩放）
    # image.thumbnail((new_width, fullcounter(y, 1)))
    image = image.resize((new_width, fullcounter(y, 1)))
    photo = ImageTk.PhotoImage(image)
    return photo

#以上四个函数如果有xy均是长宽，而非坐标

#转向正确的缓存地址
def get_resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# #获取战队logo目录
# def get_logopath_list():
#     logopath_list = os.listdir(get_resource_path("C:\\BP_IdentityV\\teamlogo"))
#     logopath_list = [logopath for logopath in logopath_list if logopath.endswith(".png")]
#     return logopath_list


def get_killer_json(json_path='C:\\BP_IdentityV\\killer.json'):
    data = {}
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {json_path}")
    return data

def get_sur_json(json_path='C:\\BP_IdentityV\\sur.json'):
    data = {}
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {json_path}")
    return data

def get_map_json(json_path='C:\\BP_IdentityV\\map.json'):
    data = {}
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {json_path}")
    return data

def get_logo_json(json_path='C:\\BP_IdentityV\\logo.json'):
    data = {}
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r') as file:
                data = json.load(file)
        except json.JSONDecodeError:
            print(f"Error decoding JSON from {json_path}")
    return data

def check_and_create_folder():
    folder_path = "C:\\BP_IdentityV\\teamlogo"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    folder_path = "C:\\BP_IdentityV\\Bigkiller"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    folder_path = "C:\\BP_IdentityV\\Bigsur"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    folder_path = "C:\\BP_IdentityV\\killer"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    folder_path = "C:\\BP_IdentityV\\sur"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    folder_path = "C:\\BP_IdentityV\\map"
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    #     print("文件夹已创建")
    # else:
    #     print("文件夹已存在")

# # 打开logo目录文件夹的按钮的函数
# def logo_open():
#     os.startfile(get_resource_path("C:\\BP_IdentityV\\teamlogo"))

# 文本转图片
def text_to_transparent_image(text, font_path, font_size, fill_color=(14, 4, 0)):
    if len(fill_color) != 3:
        raise ValueError("fill_color参数必须包含3个整数值")

    fill_color += (255,)  # 添加alpha通道值为255

    font = ImageFont.truetype(font_path, font_size)
    temp_image = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    temp_draw = ImageDraw.Draw(temp_image)
    text_bbox = temp_draw.textbbox((0, 0), text, font=font)
    image_width = text_bbox[2] - text_bbox[0]
    image_height = text_bbox[3] - text_bbox[1]
    image = Image.new("RGBA", (image_width, image_height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.text((-text_bbox[0], -text_bbox[1]), text, font=font, fill=fill_color)
    return image


# 图片路径获取
def get_path(name, file):
    if name != '' and name != 'lock':
        name = name.replace('“', '')
        name = name.replace('”', '')
        if 'png' not in name:
            filename = name + '.png'
        else:
            filename = name
        path = get_resource_path(os.path.join("data", file, filename))
        if not os.path.exists(path):
            # 如果文件不存在，设置一个默认路径
            path = os.path.join("C:\\BP_IdentityV\\", file, filename)
    else:
        path = get_resource_path('data/nothing.png')
    # print(path)
    return path


if __name__ == '__main__':
    print("in function")

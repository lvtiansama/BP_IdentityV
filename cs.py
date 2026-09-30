import re
import shutil
import time
from tkinter import filedialog
from tkinter import ttk
from pypinyin import lazy_pinyin, Style

from function import *
from ui_reply import *

root = tk.Tk()
# root.bind("<KeyPress>", key_press)
root.resizable(False, False)  # 横纵均不允许调整
root.title("第五人格bp后台控制台")
root.iconbitmap(get_resource_path("icon.ico"))
live_data = ['队伍名称', '队伍名称', '求生者比分', '监管者比分', '', '', '', '', '', '请输入选手名称',
                '请输入选手名称', '请输入选手名称', '请输入选手名称', '', '', '', '', '', '', '', '', '请输入选手名称',
                '', '请输入赛事名称', '0', '', '', '', '', '', '', '', '', '', '', '请输入选手名称', '请输入选手名称',
                '', '', '', '请输入选手名称', '', '', '', '', '', '', '', '请输入比分“W”', '请输入比分“W”',
                '请输入比分“D”', '请输入比分“D”', '请输入比分“L”', '请输入比分“L”', '请输入正整数', '']
live_data[24] = 0
bpwindow = None

def generate_new_window(fullbool):
    global bpwindow, canvas, bg_photo
    print('创建new窗口函数被调用')
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    backgroundpathdict = {
        0: "data/background.png"
    }
    if bpwindow is None:
        bpwindow = tk.Toplevel(root)  # 创建新窗口
        bpwindow.geometry("1760x990")
        bpwindow.resizable(False, False)  # 横纵均不允许调整
        bpwindow.title('第五人格bp窗口')
        bpwindow.iconbitmap(get_resource_path("icon.ico"))


        if fullbool == True:
            canvas = tk.Canvas(bpwindow, width=screen_width, height=screen_height)
            canvas.pack()
            background = Image.open(get_resource_path(backgroundpathdict.get(live_data[24]))).resize((screen_width, screen_height))
            bg_photo = ImageTk.PhotoImage(background)
            canvas.create_image(screen_width/2, screen_height/2, image=bg_photo)  # 在画布上绘制背景图像
        else:
            canvas = tk.Canvas(bpwindow, width=1760, height=990)
            canvas.pack()
            background = Image.open(get_resource_path(backgroundpathdict.get(live_data[24]))).resize((1760, 990))
            bg_photo = ImageTk.PhotoImage(background)
            canvas.create_image(880, 495, image=bg_photo)  # 在画布上绘制背景图像
            bpwindow.after(3000, delayed_action)

            # canvas.create_image(fullcounter(x, 0), fullcounter(y, 1), image='data/map/不归林.png', tags=tags)
            # background1 = Image.open(get_resource_path('data/map/不归林.png')).resize((1760, 990))
            # bg_photo = ImageTk.PhotoImage(background1)
            # canvas.create_image(880, 495, image=bg_photo, tags="image")  # 在画布上绘制背景图像

        canvas.config(highlightthickness=0)

def delayed_action():
    global bg_photo
    print('11111')
    background1 = Image.open(get_resource_path('data/map/不归林.png')).resize((1760, 990))
    bg_photo = ImageTk.PhotoImage(background1)
    canvas.create_image(880, 495, image=bg_photo, tags="image")  # 在画布上绘制背景图像

# 队伍和地图 赛事名称
teammap_frame = tk.LabelFrame(root, padx=5, pady=5, borderwidth=0, highlightthickness=0)
teammap_frame.grid(row=0, column=1, padx=5, pady=5)
# 运行与重置
button_frame = tk.LabelFrame(teammap_frame, padx=5, pady=4, borderwidth=0, highlightthickness=0)
button_frame.pack(side=tk.TOP)
run_button = ttk.Button(button_frame, text="打开BP窗口", style="Accent.TButton", command=lambda: generate_new_window(fullbool))
run_button.grid(row=0, column=0, padx=5, pady=5)

resetting_button = ttk.Button(button_frame, text="版本信息", command=show_message)
resetting_button.grid(row=1, column=1, padx=5, pady=5)

# loop
root.mainloop()
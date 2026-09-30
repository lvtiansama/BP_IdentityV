import re
import shutil
from tkinter import filedialog
from tkinter import ttk
from pypinyin import lazy_pinyin, Style

from function import *
from ui_reply import *

strlstMap = ['军工厂', '红教堂', '圣心医院', '湖景村',
             '月亮河公园', '里奥的回忆', '永眠镇', '唐人街',
             '白沙街疯人院', '闪金石窟', '不归林', '克雷伯格赛马场']
strlstSur = ['病患', '“慈善家”', '大副', '古董商', '调酒师', '调香师', '“法罗女士”', '飞行家', '画家', '火灾调查员', '击球手',
             '机械师', '祭司', '教授', '勘探员', '记者', '空军', '哭泣小丑', '昆虫学者', '拉拉队员', '律师', '木偶师', '盲女',
             '冒险家', '魔术师', '牛仔','前锋', '“囚徒”', '入殓师', '守墓人', '玩具商', '舞女', '先知', '“小女孩”', '小说家',
             '“心理学家”', '幸运儿','野人', '医生', '佣兵', '邮差', '园丁', '杂技演员', '作曲家', '咒术师']
strlstKiller = ['26号守卫', '爱哭鬼', '“博士”', '厂长', '雕刻家', '“噩梦”', '疯眼', '歌剧演员', '红蝶', '红夫人', '黄衣之主',
                '“杰克”', '记录员', '蜡像师', '鹿头', '梦之女巫', '孽蜥', '破轮', '守夜人', '“使徒”', '时空之影', '摄影师',
                '宿伞之魂', '小丑', '小提琴家', '渔女', '“愚人金”', '隐士', '蜘蛛']
#更新到法罗女士

# 赛事名称 只有在Event_Name_entry锁定的版本里使用
Event_Name = '2023 第五人格IVL 夏季赛'

# 创建缓存文件夹
check_and_create_folder()
# 新上传的求生字典
dic_newsur = get_sur_json()
# 新上传的监管字典
dic_newkiller = get_killer_json()
# 新上传的地图字典
dic_newmap = get_map_json()

# 新上传的logo字典
dic_logo = get_logo_json()
# 战队队徽目录
logopath_list = [''] + list(dic_logo.keys())

listsurlock = ['', 'lock'] + strlstSur + list(dic_newsur.keys())
listsur = [''] + strlstSur + list(dic_newsur.keys())
listkillerlock = ['', 'lock'] + strlstKiller + list(dic_newkiller.keys())
listkiller = [''] + strlstKiller + list(dic_newkiller.keys())
listmap = [''] + strlstMap + list(dic_newmap.keys())


# 倒计时函数
stop_countdown = True  # 倒计时停止标志

def count_down(num):
    global stop_countdown
    if num >= 0 and not stop_countdown:
        djs_label.configure(text="当前正在倒数："+str(num))
        djs_entry.config(state='normal')  # 设置为可更改
        djs_entry.delete(0, tk.END)
        djs_entry.insert(0, str(num))
        djs_entry.config(state='disabled')  # 设置为不可更改
        root.after(1000, count_down, num-1)
    else:
        if not stop_countdown:
            djs_label.configure(text="倒计时结束！")
        djs_entry.config(state='normal')  # 设置为可更改
        djs_button.configure(state="normal")  # 倒计时结束或手动停止后恢复按钮状态

def stopdjs():
    global stop_countdown
    stop_countdown = True
    djs_label.configure(text="倒计时已暂停")
    djs_entry.config(state='normal')  # 设置为可更改
    djs_button.configure(state="normal")  # 停止倒计时后恢复按钮状态

def djs():
    global stop_countdown
    stop_countdown = False
    num = djs_entry.get()
    if num.isdigit() and int(num) > 0:
        num = int(num)
        djs_entry.config(state='disabled')  # 设置为不可更改
        djs_button.configure(state="disabled")  # 禁用按钮
        count_down(num)
    else:
        messagebox.showwarning(title='错误', message='"'+str(num)+'"不是一个正确的正整数！')

# 交换按钮的函数
def swap_text():

    temp_texta = teamlogoa_combobox.current()
    temp_textb = teamlogob_combobox.current()

    teamlogoa_combobox.current(temp_texta)
    teamlogob_combobox.current(temp_textb)

    temp_scorea = scorea_spinbox.get()
    temp_scoreb = scoreb_spinbox.get()
    if temp_scorea == '求生者比分':
        temp_scorea = '监管者比分'
    if temp_scoreb == '监管者比分':
        temp_scoreb = '求生者比分'
    scorea_spinbox.delete(0, tk.END)
    scorea_spinbox.insert(0, temp_scoreb)
    scoreb_spinbox.delete(0, tk.END)
    scoreb_spinbox.insert(0, temp_scorea)

    logo_patha = teamlogoa_combobox.get()
    logo_pathb = teamlogob_combobox.get()
    teamlogoa_combobox.delete(0, tk.END)
    teamlogoa_combobox.insert(0, logo_pathb)
    teamlogob_combobox.delete(0, tk.END)
    teamlogob_combobox.insert(0, logo_patha)

    temp_texta = teamwldwa_entry.get()
    temp_textb = teamwldwb_entry.get()
    teamwldwa_entry.delete(0, tk.END)
    teamwldwa_entry.insert(0, temp_textb)
    teamwldwb_entry.delete(0, tk.END)
    teamwldwb_entry.insert(0, temp_texta)
    if temp_texta == "请输入比分“W”":
        teamwldwb_entry.config(foreground="gray")
    else:
        teamwldwb_entry.config(foreground="black")
    if temp_textb == "请输入比分“W”":
        teamwldwa_entry.config(foreground="gray")
    else:
        teamwldwa_entry.config(foreground="black")
    temp_texta = teamwldda_entry.get()
    temp_textb = teamwlddb_entry.get()
    teamwldda_entry.delete(0, tk.END)
    teamwldda_entry.insert(0, temp_textb)
    teamwlddb_entry.delete(0, tk.END)
    teamwlddb_entry.insert(0, temp_texta)
    if temp_texta == "请输入比分“D”":
        teamwlddb_entry.config(foreground="gray")
    else:
        teamwlddb_entry.config(foreground="black")
    if temp_textb == "请输入比分“D”":
        teamwldda_entry.config(foreground="gray")
    else:
        teamwldda_entry.config(foreground="black")
    temp_texta = teamwldla_entry.get()
    temp_textb = teamwldlb_entry.get()
    teamwldla_entry.delete(0, tk.END)
    teamwldla_entry.insert(0, temp_textb)
    teamwldlb_entry.delete(0, tk.END)
    teamwldlb_entry.insert(0, temp_texta)
    if temp_texta == "请输入比分“L”":
        teamwldlb_entry.config(foreground="gray")
    else:
        teamwldlb_entry.config(foreground="black")
    if temp_textb == "请输入比分“L”":
        teamwldla_entry.config(foreground="gray")
    else:
        teamwldla_entry.config(foreground="black")

def open_dropdown(event):
    # 模拟点击下拉箭头
    event.widget.event_generate("<Button-1>")

# 预处理选项的函数
def preprocess_options(options):
    processed_options = {}
    for option in options:
        # 清洗选项，去除特殊字符
        clean_option = re.sub(r'[^\w\s]', '', option)
        # 将选项转换为小写，以实现大小写不敏感
        clean_option = clean_option.lower()
        # 处理中文部分
        chinese_part = re.sub(r'[a-zA-Z]+', '', clean_option)
        pinyin = ''.join(lazy_pinyin(chinese_part, style=Style.NORMAL))  # 无声调全拼

        pinyin = re.sub(r'diaojiushi', 'tiaojiushi', pinyin)
        pinyin = re.sub(r'diaoxiangshi', 'tiaoxiangshi', pinyin) # 处理提酒调香的多音字
        # print(pinyin)

        initials = convert_initials(''.join(lazy_pinyin(chinese_part, style=Style.FIRST_LETTER)))  # 转换为首字母缩写
        initials = re.sub(r'djs', 'tjs', initials)
        initials = re.sub(r'dxs', 'txs', initials) # 处理提酒调香的多音字
        # print(initials)

        # 处理英文部分
        english_part = re.sub(r'[^a-zA-Z]+', '', clean_option)

        # 创建匹配模式
        match_patterns = set()
        # 添加全拼
        match_patterns.add(pinyin)
        # 添加首字母缩写
        match_patterns.add(initials)
        # 添加每个汉字的单个匹配
        for char in chinese_part:
            match_patterns.add(char)
        # 添加英文全拼
        match_patterns.add(english_part)

        # 添加所有子串作为可能的匹配模式
        for i in range(1, len(clean_option) + 1):
            for j in range(len(clean_option) - i + 1):
                sub_pattern = clean_option[j:j + i]
                match_patterns.add(sub_pattern)

        processed_options[clean_option] = {
            'option': option,
            'match_patterns': match_patterns
        }
    return processed_options

def convert_initials(initials):
    # 将双字母的拼音首字母转换为单字母，比如 cshj -> csh
    initials_mapping = {
        'zh': 'z',
        'ch': 'c',
        'sh': 's'
        # 添加其他需要转换的双字母缩写
    }
    for key in initials_mapping:
        initials = initials.replace(key, initials_mapping[key])
    return initials

def filter_combobox(combobox, event, processed_options):
    current_text = combobox.get().strip().lower()

    filtered_values = []
    for clean_option, data in processed_options.items():
        if any(current_text in pattern for pattern in data['match_patterns']):
            filtered_values.append(data['option'])

    combobox['values'] = filtered_values

def clear_newload(directory_path):
    global option_upload_window
    # 显示确认对话框
    answer = messagebox.askyesno("敏感操作", "你正在删除所有新上传的数据，这一操作不可逆，你确定要删除吗？")
    if answer:
        try:
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            # 关闭窗口
            option_upload_window.destroy()
            root.attributes('-disabled', False)

            dic_logo = get_logo_json()
            # 刷新战队队徽目录
            logopath_list = [''] + list(dic_logo.keys())

            teamlogoa_combobox['values'] = logopath_list
            teamlogob_combobox['values'] = logopath_list

            dic_newmap = get_map_json()

            listmap = [''] + strlstMap + list(dic_newmap.keys())

            mapnamea_combobox['values'] = [''] + listmap
            mapnameb_combobox['values'] = [''] + listmap

            # 刷新新上传的求生字典
            dic_newsur = get_sur_json()
            # 刷新新上传的监管字典
            dic_newkiller = get_killer_json()

            listsurlock = ['', 'lock'] + strlstSur + list(dic_newsur.keys())
            listsur = [''] + strlstSur + list(dic_newsur.keys())
            listkillerlock = ['', 'lock'] + strlstKiller + list(dic_newkiller.keys())
            listkiller = [''] + strlstKiller + list(dic_newkiller.keys())

            # 定义组合框列表
            killer_ban_comboboxes = [
                Killerban1_combobox, Killerban2_combobox, Killerban3_combobox,
                Killerban4_combobox, Killerban5_combobox, Killerban6_combobox,
                Killerban11_combobox, Killerban22_combobox, Killerban33_combobox,
                Killerban44_combobox, Killerban55_combobox, Killerban66_combobox
            ]

            whole_ban_comboboxes = [
                Wholeban1_combobox, Wholeban2_combobox, Wholeban3_combobox,
                Wholeban4_combobox, Wholeban5_combobox, Wholeban6_combobox
            ]

            sur_pick_comboboxes = [
                surpick1_combobox, surpick2_combobox, surpick3_combobox,
                surpick4_combobox, surpick5_combobox, surpick6_combobox
            ]

            sur_ban_comboboxes = [
                surban1_combobox, surban2_combobox, surban3_combobox,
                surban4_combobox
            ]

            killer_pick_comboboxes = [
                Killerpick_combobox, Killerpick1_combobox
            ]

            # 调用函数
            set_combobox_values(killer_ban_comboboxes, listsurlock)
            set_combobox_values(whole_ban_comboboxes, listsurlock)
            set_combobox_values(sur_pick_comboboxes, listsur)
            set_combobox_values(sur_ban_comboboxes, listkillerlock)
            set_combobox_values(killer_pick_comboboxes, listkiller)
            messagebox.showwarning(title='清除成功', message='所有新上传的数据已被删除')
        except Exception as e:
            messagebox.showerror("错误", "数据没有正确被清除")
    else:
        messagebox.showwarning(title='清除取消', message='你已取消了清除操作')

def set_combobox_values(comboboxes, values):
    for combobox in comboboxes:
        combobox['values'] = values

# 选择缩略图
def choose_s_file():
    global s_png_path_label
    filepath = filedialog.askopenfilename(
        title="请选择缩略图",
        filetypes=(("透明底图片", "*.png"), ("所有文件", "*.*"))
    )
    if filepath:
        # 验证文件扩展名
        if not filepath.lower().endswith('.png'):
            messagebox.showerror("错误", "请选择PNG格式的图片文件。")
            return

        try:
            # 打开图像文件并检查尺寸
            with Image.open(filepath) as img:
                if img.size == (120, 120):
                    s_png_path_label['text'] = filepath
                else:
                    messagebox.showerror("错误", "图片尺寸必须为120x120像素。")
        except IOError:
            messagebox.showerror("错误", "无法读取文件，请选择有效的图片。")

def choose_b_file():
    global b_png_path_label
    filepath = filedialog.askopenfilename(
        title="请选择立绘",
        filetypes=(("透明底图片", "*.png"), ("所有文件", "*.*"))
    )
    if filepath:
        # 验证文件扩展名
        if not filepath.lower().endswith('.png'):
            messagebox.showerror("错误", "请选择PNG格式的图片文件。")
            return

        # 打开图像文件并检查尺寸
        img = Image.open(filepath)
        width, height = img.size
        if width <= 1000 and height <= 1000:
            b_png_path_label['text'] = filepath
        else:
            messagebox.showerror("错误", "图片尺寸过大，请选择宽度和高度都不超过1000像素的图片")

def choose_mp_file():
    global mp_png_path_label
    filepath = filedialog.askopenfilename(
        title="请选择地图",
        filetypes=(("透明底图片", "*.png"), ("所有文件", "*.*"))
    )
    if filepath:
        # 验证文件扩展名
        if not filepath.lower().endswith('.png'):
            messagebox.showerror("错误", "请选择PNG格式的图片文件。")
            return

        # 打开图像文件并检查尺寸
        img = Image.open(filepath)
        width, height = img.size
        if width <= 1000 and height <= 500:
            mp_png_path_label['text'] = filepath
        else:
            messagebox.showerror("错误", "图片尺寸过大，请选择宽度不超过1000像素，高度不超过500像素的图片。")

def choose_logo_file():
    global logo_png_path_label
    filepath = filedialog.askopenfilename(
        title="请选择logo",
        filetypes=(("图片", "*.png"), ("所有文件", "*.*"))
    )
    if filepath:
        # 验证文件扩展名
        if not filepath.lower().endswith('.png'):
            messagebox.showerror("错误", "请选择PNG格式的图片文件。")
            return

        # 打开图像文件并检查尺寸
        img = Image.open(filepath)
        width, height = img.size
        if width <= 1000 and height <= 1000:
            logo_png_path_label['text'] = filepath
        else:
            messagebox.showerror("错误", "图片尺寸过大，请选择宽度高度不超过1000像素的图片。")

def upload1_now():
    global upload1_window, upload1_combobox, upload1_entry, s_png_path_label, b_png_path_label, dic_newsur, dic_newkiller, listsurlock, listsur, listkillerlock, listkiller

    # 获取角色类型和名称
    role_type = upload1_combobox.get()
    role_name = upload1_entry.get().strip()

    # 检查必填字段是否完整
    if role_name == '请输入新角色名称':
        messagebox.showwarning("警告", "角色名称不能为空！")
        return

    elif s_png_path_label['text'] == '缩略图大小应该为120*120的透明底png':
        messagebox.showwarning("警告", "请上传角色缩略图！")
        return

    elif b_png_path_label['text'] == '立绘应为长宽像素均小于1000的透明底png':
        messagebox.showwarning("警告", "请上传角色立绘！")
        return

    # 确定目标文件夹
    base_folder = "C:\\BP_IdentityV\\"
    if role_type.lower() == '求生者':
        small_folder = "sur"
        big_folder = 'Bigsur'
        json_filename = "sur.json"
    elif role_type.lower() == '监管者':
        small_folder = "killer"
        big_folder = 'Bigkiller'
        json_filename = "killer.json"

    # 检查路径是否存在，不存在则创建
    if not os.path.exists(os.path.join(base_folder, small_folder)):
        os.makedirs(os.path.join(base_folder, small_folder))
    if not os.path.exists(os.path.join(base_folder, big_folder)):
        os.makedirs(os.path.join(base_folder, big_folder))

    # 尝试复制文件
    try:
        shutil.copy(s_png_path_label['text'], os.path.join(base_folder, small_folder, role_name + ".png"))
        shutil.copy(b_png_path_label['text'], os.path.join(base_folder, big_folder, role_name + ".png"))
    except Exception as e:
        messagebox.showerror("错误", f"复制文件时发生错误：{str(e)}")
        return

    # 创建或更新 JSON 文件
    json_path = os.path.join(base_folder, json_filename)
    data = {
        role_name: {
            "s": os.path.join(small_folder, role_name + ".png"),
            "b": os.path.join(big_folder, role_name + ".png"),
        }
    }

    # 读取现有数据，如果存在的话
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            existing_data = json.load(f)
        existing_data.update(data)
        data = existing_data

    # 写入数据
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

    # 关闭窗口
    upload1_window.destroy()
    root.attributes('-disabled', False)
    # 刷新新上传的求生字典
    dic_newsur = get_sur_json()
    # 刷新新上传的监管字典
    dic_newkiller = get_killer_json()

    listsurlock = ['', 'lock'] + strlstSur + list(dic_newsur.keys())
    listsur = [''] + strlstSur + list(dic_newsur.keys())
    listkillerlock = ['', 'lock'] + strlstKiller + list(dic_newkiller.keys())
    listkiller = [''] + strlstKiller + list(dic_newkiller.keys())

    # 定义组合框列表
    killer_ban_comboboxes = [
        Killerban1_combobox, Killerban2_combobox, Killerban3_combobox,
        Killerban4_combobox, Killerban5_combobox, Killerban6_combobox,
        Killerban11_combobox, Killerban22_combobox, Killerban33_combobox,
        Killerban44_combobox, Killerban55_combobox, Killerban66_combobox
    ]

    whole_ban_comboboxes = [
        Wholeban1_combobox, Wholeban2_combobox, Wholeban3_combobox,
        Wholeban4_combobox, Wholeban5_combobox, Wholeban6_combobox
    ]

    sur_pick_comboboxes = [
        surpick1_combobox, surpick2_combobox, surpick3_combobox,
        surpick4_combobox, surpick5_combobox, surpick6_combobox
    ]

    sur_ban_comboboxes = [
        surban1_combobox, surban2_combobox, surban3_combobox,
        surban4_combobox
    ]

    killer_pick_comboboxes = [
        Killerpick_combobox, Killerpick1_combobox
    ]

    # 调用函数
    set_combobox_values(killer_ban_comboboxes, listsurlock)
    set_combobox_values(whole_ban_comboboxes, listsurlock)
    set_combobox_values(sur_pick_comboboxes, listsur)
    set_combobox_values(sur_ban_comboboxes, listkillerlock)
    set_combobox_values(killer_pick_comboboxes, listkiller)


    messagebox.showwarning(title='上传成功', message='新 ' +role_type + ' ' +role_name+' 已经上传成功')

def upload2_now():
    global upload2_window, upload2_entry, mp_png_path_label, dic_newmap, listmap

    # 获取地图名称
    role_name = upload2_entry.get().strip()

    # 检查必填字段是否完整
    if role_name == '请输入新地图名称':
        messagebox.showwarning("警告", "地图名称不能为空！")
        return

    elif mp_png_path_label['text'] == '地图应为长宽像素均小于500的透明底png':
        messagebox.showwarning("警告", "请上传地图缩略图！")
        return

    # 确定目标文件夹
    base_folder = "C:\\BP_IdentityV\\"

    map_folder = "map"
    json_filename = "map.json"


    # 检查路径是否存在，不存在则创建
    if not os.path.exists(os.path.join(base_folder, map_folder)):
        os.makedirs(os.path.join(base_folder, map_folder))

    # 尝试复制文件
    try:
        shutil.copy(mp_png_path_label['text'], os.path.join(base_folder, map_folder, role_name + ".png"))

    except Exception as e:
        messagebox.showerror("错误", f"上传文件时发生错误：{str(e)}")
        return

    # 创建或更新 JSON 文件
    json_path = os.path.join(base_folder, json_filename)
    data = {
        role_name: {
            "map": os.path.join(map_folder, role_name + ".png"),
        }
    }

    # 读取现有数据，如果存在的话
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            existing_data = json.load(f)
        existing_data.update(data)
        data = existing_data

    # 写入数据
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

    # 关闭窗口
    upload2_window.destroy()
    root.attributes('-disabled', False)
    # 刷新新上传的地图字典
    dic_newmap = get_map_json()

    listmap = [''] + strlstMap + list(dic_newmap.keys())

    mapnamea_combobox['values'] = [''] + listmap
    mapnameb_combobox['values'] = [''] + listmap

    messagebox.showwarning(title='上传成功', message='新地图 '+ role_name +' 已经上传成功')

def upload3_now():
    global upload3_window, upload3_entry, logo_png_path_label, dic_logo, logopath_list

    # 获取地图名称
    role_name = upload3_entry.get().strip()

    # 检查必填字段是否完整
    if role_name == '请输入战队名称':
        messagebox.showwarning("警告", "战队名称不能为空！")
        return

    elif logo_png_path_label['text'] == 'logo应为长宽像素均小于1000的png图片':
        messagebox.showwarning("警告", "请上传战队logo！")
        return

    # 确定目标文件夹
    base_folder = "C:\\BP_IdentityV\\"

    logo_folder = "teamlogo"
    json_filename = "logo.json"


    # 检查路径是否存在，不存在则创建
    if not os.path.exists(os.path.join(base_folder, logo_folder)):
        os.makedirs(os.path.join(base_folder, logo_folder))

    # 尝试复制文件
    try:
        shutil.copy(logo_png_path_label['text'], os.path.join(base_folder, logo_folder, role_name + ".png"))

    except Exception as e:
        messagebox.showerror("错误", f"上传文件时发生错误：{str(e)}")
        return

    # 创建或更新 JSON 文件
    json_path = os.path.join(base_folder, json_filename)
    data = {
        role_name: {
            "path": os.path.join(logo_folder, role_name + ".png"),
        }
    }

    # 读取现有数据，如果存在的话
    if os.path.exists(json_path):
        with open(json_path, 'r') as f:
            existing_data = json.load(f)
        existing_data.update(data)
        data = existing_data

    # 写入数据
    with open(json_path, 'w') as f:
        json.dump(data, f, indent=4)

    # 关闭窗口
    upload3_window.destroy()
    root.attributes('-disabled', False)
    # 刷新新上传的战队字典
    dic_logo = get_logo_json()
    # 刷新战队队徽目录
    logopath_list = [''] + list(dic_logo.keys())

    teamlogoa_combobox['values'] =logopath_list
    teamlogob_combobox['values'] =logopath_list

    messagebox.showwarning(title='上传成功', message='新战队 '+ role_name +' 已经上传成功')

def open_option_upload_window():
    global option_upload_window
    if option_upload_window is None or not option_upload_window.winfo_exists():
        messagebox.showwarning(title='拓展功能', message='你正在准备上传新的数据！')

        # 创建新的 Toplevel 窗口
        option_upload_window = tk.Toplevel(root)
        option_upload_window.iconbitmap(get_resource_path("icon.ico"))
        option_upload_window.title("选择你要上传的数据")
        option_upload_window.transient(root)
        option_upload_window.grab_set()

        # 选择的三个按扭
        option_upload_frame = tk.LabelFrame(option_upload_window, padx=5, pady=4, borderwidth=0, highlightthickness=0)
        option_upload_frame.pack(side=tk.TOP)
        upjuese_button = ttk.Button(option_upload_frame, text="上传新角色", style="Accent.TButton",command=lambda: open_upload1_window())
        upjuese_button.grid(row=0, column=0, padx=5, pady=5)
        upmap_button = ttk.Button(option_upload_frame, text="上传新地图", style="Accent.TButton", command=lambda: open_upload2_window())
        upmap_button.grid(row=0, column=1, padx=5, pady=5)
        uplogo_button = ttk.Button(option_upload_frame, text="上传新logo", style="Accent.TButton", command=lambda: open_upload3_window())
        uplogo_button.grid(row=0, column=2, padx=5, pady=5)
        clear_button = ttk.Button(option_upload_frame, text="清除新数据", style="Accent.TButton", command=lambda: clear_newload("C:\\BP_IdentityV\\"))
        clear_button.grid(row=0, column=3, padx=5, pady=5)
        stopup_button = ttk.Button(option_upload_frame, text="取消上传", command=lambda: on_option_upload_close())
        stopup_button.grid(row=0, column=4, padx=5, pady=5)

        # 设置窗口关闭时的回调函数
        option_upload_window.protocol("WM_DELETE_WINDOW", on_option_upload_close)

        # 禁用根窗口
        root.attributes('-disabled', True)

        # 更新窗口信息以获取宽度和高度
        option_upload_window.update_idletasks()
        # 计算窗口位置
        x_cordinate = int((option_upload_window.winfo_screenwidth() / 2) - (option_upload_window.winfo_width() / 2))
        y_cordinate = int((option_upload_window.winfo_screenheight() / 2) - (option_upload_window.winfo_height() / 2))
        # 设置窗口位置
        option_upload_window.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))
    else:
        # 如果窗口已经存在，播放系统提示音
        root.bell()

def on_option_upload_close():
    global option_upload_window
    if option_upload_window is not None:
        # 确保解除grab状态，允许其他窗口接收事件
        option_upload_window.grab_release()
        # 销毁 Toplevel 窗口
        option_upload_window.destroy()
        # 清除全局变量
        option_upload_window = None
        # 重新启用根窗口
        root.attributes('-disabled', False)
        # windows系统焦点回到root
        root.focus_force()
        # # 提升主窗口层级，使其显示在其他窗口之上
        # root.lift()

# 上传角色
def open_upload1_window():
    global upload1_window, upload1_combobox, upload1_entry, s_png_path_label, b_png_path_label
    on_option_upload_close()
    if upload1_window is None or not upload1_window.winfo_exists():

        # 创建新的 Toplevel 窗口
        upload1_window = tk.Toplevel(root)
        upload1_window.iconbitmap(get_resource_path("icon.ico"))
        upload1_window.title("上传新角色")
        upload1_window.transient(root)
        upload1_window.grab_set()

        # 上传
        upload1_frame = tk.LabelFrame(upload1_window, padx=5, pady=4, borderwidth=0, highlightthickness=0)
        upload1_frame.pack(side=tk.TOP)

        upload1_combobox_label = ttk.Label(upload1_frame, text="请选择阵容")
        upload1_combobox_label.grid(row=0, column=1, padx=5, pady=5)

        upload1_combobox = ttk.Combobox(upload1_frame, values=['求生者','监管者'], width=16)
        upload1_combobox.current(0)
        upload1_combobox.grid(row=0, column=0, padx=5, pady=5)

        upload1_entry_label = ttk.Label(upload1_frame, text="请输入新角色名称")
        upload1_entry_label.grid(row=1, column=1, padx=5, pady=5)

        upload1_entry = ttk.Entry(upload1_frame, width=14)
        upload1_entry.insert(0, "请输入新角色名称")
        upload1_entry.default_text = "请输入新角色名称"
        upload1_entry.config(foreground="gray")
        upload1_entry.bind("<Button-1>", handle_default_text)
        upload1_entry.bind("<FocusIn>", handle_default_text)
        upload1_entry.bind("<FocusOut>", handle_focus_out)
        upload1_entry.grid(row=1, column=0, padx=5, pady=5)

        s_png_path_label = ttk.Label(upload1_frame, text="缩略图大小应该为120*120的透明底png")
        s_png_path_label.grid(row=2, column=0, padx=5, pady=5)
        s_png_button = ttk.Button(upload1_frame, text="上传角色缩略图", style="Accent.TButton",
                                  command=lambda: choose_s_file())
        s_png_button.grid(row=2, column=1, padx=5, pady=5)

        b_png_path_label = ttk.Label(upload1_frame, text="立绘应为长宽像素均小于1000的透明底png")
        b_png_path_label.grid(row=3, column=0, padx=5, pady=5)
        b_png_button = ttk.Button(upload1_frame, text="上传角色立绘", style="Accent.TButton",
                                  command=lambda: choose_b_file())
        b_png_button.grid(row=3, column=1, padx=5, pady=5)

        # 上传
        upload1ok_frame = tk.LabelFrame(upload1_window, padx=5, pady=4, borderwidth=0, highlightthickness=0)
        upload1ok_frame.pack(side=tk.TOP)

        upnow_button = ttk.Button(upload1ok_frame, text="确认上传", style="Accent.TButton", command=lambda: upload1_now())
        upnow_button.grid(row=0, column=0, padx=5, pady=5)
        stopup_button = ttk.Button(upload1ok_frame, text="取消上传", command=lambda: on_upload1_close())
        stopup_button.grid(row=0, column=1, padx=5, pady=5)

        # 设置窗口关闭时的回调函数
        upload1_window.protocol("WM_DELETE_WINDOW", on_upload1_close)

        # 禁用根窗口
        root.attributes('-disabled', True)

        # 更新窗口信息以获取宽度和高度
        upload1_window.update_idletasks()
        # 计算窗口位置
        x_cordinate = int((upload1_window.winfo_screenwidth() / 2) - (upload1_window.winfo_width() / 2))
        y_cordinate = int((upload1_window.winfo_screenheight() / 2) - (upload1_window.winfo_height() / 2))
        # 设置窗口位置
        upload1_window.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))
    else:
        # 如果窗口已经存在，播放系统提示音
        root.bell()

def on_upload1_close():
    global upload1_window
    if upload1_window is not None:
        # 确保解除grab状态，允许其他窗口接收事件
        upload1_window.grab_release()
        # 销毁 Toplevel 窗口
        upload1_window.destroy()
        # 清除全局变量
        upload1_window = None
        # 重新启用根窗口
        root.attributes('-disabled', False)
        # windows系统焦点回到root
        root.focus_force()
        # # 提升主窗口层级，使其显示在其他窗口之上
        # root.lift()

# 上传map
def open_upload2_window():
    global upload2_window, upload2_entry, mp_png_path_label
    on_option_upload_close()
    if upload2_window is None or not upload2_window.winfo_exists():

        # 创建新的 Toplevel 窗口
        upload2_window = tk.Toplevel(root)
        upload2_window.iconbitmap(get_resource_path("icon.ico"))
        upload2_window.title("上传新地图")
        upload2_window.transient(root)
        upload2_window.grab_set()

        # 上传
        upload2_frame = tk.LabelFrame(upload2_window, padx=5, pady=4, borderwidth=0, highlightthickness=0)
        upload2_frame.pack(side=tk.TOP)

        upload2_entry_label = ttk.Label(upload2_frame, text="请输入新地图名称")
        upload2_entry_label.grid(row=0, column=1, padx=5, pady=5)

        upload2_entry = ttk.Entry(upload2_frame, width=14)
        upload2_entry.insert(0, "请输入新地图名称")
        upload2_entry.default_text = "请输入新地图名称"
        upload2_entry.config(foreground="gray")
        upload2_entry.bind("<Button-1>", handle_default_text)
        upload2_entry.bind("<FocusIn>", handle_default_text)
        upload2_entry.bind("<FocusOut>", handle_focus_out)
        upload2_entry.grid(row=0, column=0, padx=5, pady=5)

        mp_png_path_label = ttk.Label(upload2_frame, text="地图应为长宽像素均小于500的透明底png")
        mp_png_path_label.grid(row=1, column=0, padx=5, pady=5)
        mp_png_button = ttk.Button(upload2_frame, text="上传地图", style="Accent.TButton",
                                  command=lambda: choose_mp_file())
        mp_png_button.grid(row=1, column=1, padx=5, pady=5)


        # 上传
        upload2ok_frame = tk.LabelFrame(upload2_window, padx=5, pady=4, borderwidth=0, highlightthickness=0)
        upload2ok_frame.pack(side=tk.TOP)


        upnow2_button = ttk.Button(upload2ok_frame, text="确认上传", style="Accent.TButton", command=lambda: upload2_now())
        upnow2_button.grid(row=0, column=0, padx=5, pady=5)
        stopup2_button = ttk.Button(upload2ok_frame, text="取消上传", command=lambda: on_upload2_close())
        stopup2_button.grid(row=0, column=1, padx=5, pady=5)

        # 设置窗口关闭时的回调函数
        upload2_window.protocol("WM_DELETE_WINDOW", on_upload2_close)

        # 禁用根窗口
        root.attributes('-disabled', True)

        # 更新窗口信息以获取宽度和高度
        upload2_window.update_idletasks()
        # 计算窗口位置
        x_cordinate = int((upload2_window.winfo_screenwidth() / 2) - (upload2_window.winfo_width() / 2))
        y_cordinate = int((upload2_window.winfo_screenheight() / 2) - (upload2_window.winfo_height() / 2))
        # 设置窗口位置
        upload2_window.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))
    else:
        # 如果窗口已经存在，播放系统提示音
        root.bell()

def on_upload2_close():
    global upload2_window
    if upload2_window is not None:
        # 确保解除grab状态，允许其他窗口接收事件
        upload2_window.grab_release()
        # 销毁 Toplevel 窗口
        upload2_window.destroy()
        # 清除全局变量
        upload2_window = None
        # 重新启用根窗口
        root.attributes('-disabled', False)
        # windows系统焦点回到root
        root.focus_force()
        # # 提升主窗口层级，使其显示在其他窗口之上
        # root.lift()

# 上传logo
def open_upload3_window():
    global upload3_window, upload3_entry, logo_png_path_label
    on_option_upload_close()
    if upload3_window is None or not upload3_window.winfo_exists():

        # 创建新的 Toplevel 窗口
        upload3_window = tk.Toplevel(root)
        upload3_window.iconbitmap(get_resource_path("icon.ico"))
        upload3_window.title("上传新战队")
        upload3_window.transient(root)
        upload3_window.grab_set()

        # 上传
        upload3_frame = tk.LabelFrame(upload3_window, padx=5, pady=4, borderwidth=0, highlightthickness=0)
        upload3_frame.pack(side=tk.TOP)

        upload3_entry_label = ttk.Label(upload3_frame, text="请输入战队名称")
        upload3_entry_label.grid(row=0, column=1, padx=5, pady=5)

        upload3_entry = ttk.Entry(upload3_frame, width=14)
        upload3_entry.insert(0, "请输入战队名称")
        upload3_entry.default_text = "请输入战队名称"
        upload3_entry.config(foreground="gray")
        upload3_entry.bind("<Button-1>", handle_default_text)
        upload3_entry.bind("<FocusIn>", handle_default_text)
        upload3_entry.bind("<FocusOut>", handle_focus_out)
        upload3_entry.grid(row=0, column=0, padx=5, pady=5)

        logo_png_path_label = ttk.Label(upload3_frame, text="logo应为长宽像素均小于1000的png图片")
        logo_png_path_label.grid(row=1, column=0, padx=5, pady=5)
        logo_png_button = ttk.Button(upload3_frame, text="上传logo", style="Accent.TButton",
                                  command=lambda: choose_logo_file())
        logo_png_button.grid(row=1, column=1, padx=5, pady=5)

        # 上传
        upload3ok_frame = tk.LabelFrame(upload3_window, padx=5, pady=4, borderwidth=0, highlightthickness=0)
        upload3ok_frame.pack(side=tk.TOP)

        upnow3_button = ttk.Button(upload3ok_frame, text="确认上传", style="Accent.TButton", command=lambda: upload3_now())
        upnow3_button.grid(row=0, column=0, padx=5, pady=5)
        stopup3_button = ttk.Button(upload3ok_frame, text="取消上传", command=lambda: on_upload3_close())
        stopup3_button.grid(row=0, column=1, padx=5, pady=5)

        # 设置窗口关闭时的回调函数
        upload3_window.protocol("WM_DELETE_WINDOW", on_upload3_close)

        # 禁用根窗口
        root.attributes('-disabled', True)

        # 更新窗口信息以获取宽度和高度
        upload3_window.update_idletasks()
        # 计算窗口位置
        x_cordinate = int((upload3_window.winfo_screenwidth() / 2) - (upload3_window.winfo_width() / 2))
        y_cordinate = int((upload3_window.winfo_screenheight() / 2) - (upload3_window.winfo_height() / 2))
        # 设置窗口位置
        upload3_window.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))
    else:
        # 如果窗口已经存在，播放系统提示音
        root.bell()

def on_upload3_close():
    global upload3_window
    if upload3_window is not None:
        # 确保解除grab状态，允许其他窗口接收事件
        upload3_window.grab_release()
        # 销毁 Toplevel 窗口
        upload3_window.destroy()
        # 清除全局变量
        upload3_window = None
        # 重新启用根窗口
        root.attributes('-disabled', False)
        # windows系统焦点回到root
        root.focus_force()
        # # 提升主窗口层级，使其显示在其他窗口之上
        # root.lift()

# 测试函数
def key_press(event):
    print(f"Key pressed: {event.keycode}")

def handle_f10(event):
    print('用户按下了f10')
    return "break"

root = tk.Tk()
# root.bind("<KeyPress>", key_press)
root.resizable(False, False)  # 横纵均不允许调整
root.title("第五人格bp后台控制台")
root.iconbitmap(get_resource_path("icon.ico"))
# root.geometry('960x560')

root.bind("<F10>", handle_f10)
# 禁用f10触发系统菜单（alt依旧可以使用，alt+Space可正常使用） 本行代码修复的是中文输入法小写y会触发f10失去焦点启动系统菜单的bug

# 设置样式
root.tk.call("source", get_resource_path("azure.tcl"))
root.tk.call("set_theme", "light")

# 队伍和地图 赛事名称
teammap_frame = tk.LabelFrame(root, padx=5, pady=5, borderwidth=0, highlightthickness=0)
teammap_frame.grid(row=0, column=1, padx=5, pady=5)

# 赛事名称
Event_Name_and_mode_frame = tk.LabelFrame(teammap_frame, padx=5, pady=5, borderwidth=0, highlightthickness=0)
Event_Name_and_mode_frame.pack(side=tk.TOP, pady=4)
# 赛事名称
Event_Name_frame = tk.LabelFrame(Event_Name_and_mode_frame, text='赛事名称', padx=5, pady=4)
Event_Name_frame.grid(row=0, column=0, padx=5, pady=5)

Event_Name_label = ttk.Label(Event_Name_frame, text="赛事名称")
Event_Name_label.grid(row=0, column=0, padx=5, pady=5)

Event_Name_entry = ttk.Entry(Event_Name_frame, width=24)
Event_Name_entry.insert(0, "请输入赛事名称")
Event_Name_entry.default_text = "请输入赛事名称"
Event_Name_entry.config(foreground="gray")
Event_Name_entry.bind("<Button-1>", handle_default_text)
Event_Name_entry.bind("<FocusIn>", handle_default_text)
Event_Name_entry.bind("<FocusOut>", handle_focus_out)
Event_Name_entry.grid(row=1, column=0, padx=5, pady=5)
# # 可以修改版

# 队伍名称
team_frame = tk.LabelFrame(teammap_frame, text='队伍名称', padx=5, pady=4)
team_frame.pack(side=tk.TOP, pady=4)

teamnamea_label = ttk.Label(team_frame, text="求生者队伍")
teamnamea_label.grid(row=0, column=0, padx=5, pady=5)
teamnameb_label = ttk.Label(team_frame, text="监管者队伍")
teamnameb_label.grid(row=0, column=2, padx=5, pady=5)

teamlogoa_combobox = ttk.Combobox(team_frame, values=logopath_list, width=14)
teamlogoa_combobox.current(0)
teamlogoa_combobox.grid(row=1, column=0, padx=5, pady=5)

team_button = ttk.Button(team_frame, text="交换", command=swap_text)
team_button.grid(row=1, column=1, padx=5, pady=5)

teamlogob_combobox = ttk.Combobox(team_frame, values=logopath_list, width=14)
teamlogob_combobox.current(0)
teamlogob_combobox.grid(row=1, column=2, padx=5, pady=5)

scorea_spinbox = ttk.Spinbox(team_frame, from_=0, to=100, increment=1, width=14)
scorea_spinbox.insert(0, "求生者比分")
scorea_spinbox.grid(row=2, column=0, padx=5, pady=5)
score_label = ttk.Label(team_frame, text="本场比分")
score_label.grid(row=2, column=1, padx=5, pady=5)
scoreb_spinbox = ttk.Spinbox(team_frame, from_=0, to=100, increment=1, width=14)
scoreb_spinbox.insert(0, "监管者比分")
scoreb_spinbox.grid(row=2, column=2, padx=5, pady=5)

teamwldwa_entry = ttk.Entry(team_frame, width=14)
teamwldwa_entry.insert(0, "请输入比分“W”")
teamwldwa_entry.default_text = "请输入比分“W”"
teamwldwa_entry.config(foreground="gray")
teamwldwa_entry.bind("<Button-1>", handle_default_text)
teamwldwa_entry.bind("<FocusIn>", handle_default_text)
teamwldwa_entry.bind("<FocusOut>", handle_focus_out)
teamwldwa_entry.grid(row=3, column=0, padx=5, pady=5)
score_label1 = ttk.Label(team_frame, text="W")
score_label1.grid(row=3, column=1, padx=5, pady=5)
teamwldwb_entry = ttk.Entry(team_frame, width=14)
teamwldwb_entry.insert(0, "请输入比分“W”")
teamwldwb_entry.default_text = "请输入比分“W”"
teamwldwb_entry.config(foreground="gray")
teamwldwb_entry.bind("<Button-1>", handle_default_text)
teamwldwb_entry.bind("<FocusIn>", handle_default_text)
teamwldwb_entry.bind("<FocusOut>", handle_focus_out)
teamwldwb_entry.grid(row=3, column=2, padx=5, pady=5)

teamwldda_entry = ttk.Entry(team_frame, width=14)
teamwldda_entry.insert(0, "请输入比分“D”")
teamwldda_entry.default_text = "请输入比分“D”"
teamwldda_entry.config(foreground="gray")
teamwldda_entry.bind("<Button-1>", handle_default_text)
teamwldda_entry.bind("<FocusIn>", handle_default_text)
teamwldda_entry.bind("<FocusOut>", handle_focus_out)
teamwldda_entry.grid(row=4, column=0, padx=5, pady=5)
score_label1 = ttk.Label(team_frame, text="D")
score_label1.grid(row=4, column=1, padx=5, pady=5)
teamwlddb_entry = ttk.Entry(team_frame, width=14)
teamwlddb_entry.insert(0, "请输入比分“D”")
teamwlddb_entry.default_text = "请输入比分“D”"
teamwlddb_entry.config(foreground="gray")
teamwlddb_entry.bind("<Button-1>", handle_default_text)
teamwlddb_entry.bind("<FocusIn>", handle_default_text)
teamwlddb_entry.bind("<FocusOut>", handle_focus_out)
teamwlddb_entry.grid(row=4, column=2, padx=5, pady=5)

teamwldla_entry = ttk.Entry(team_frame, width=14)
teamwldla_entry.insert(0, "请输入比分“L”")
teamwldla_entry.default_text = "请输入比分“L”"
teamwldla_entry.config(foreground="gray")
teamwldla_entry.bind("<Button-1>", handle_default_text)
teamwldla_entry.bind("<FocusIn>", handle_default_text)
teamwldla_entry.bind("<FocusOut>", handle_focus_out)
teamwldla_entry.grid(row=5, column=0, padx=5, pady=5)
score_label1 = ttk.Label(team_frame, text="L")
score_label1.grid(row=5, column=1, padx=5, pady=5)
teamwldlb_entry = ttk.Entry(team_frame, width=14)
teamwldlb_entry.insert(0, "请输入比分“L”")
teamwldlb_entry.default_text = "请输入比分“L”"
teamwldlb_entry.config(foreground="gray")
teamwldlb_entry.bind("<Button-1>", handle_default_text)
teamwldlb_entry.bind("<FocusIn>", handle_default_text)
teamwldlb_entry.bind("<FocusOut>", handle_focus_out)
teamwldlb_entry.grid(row=5, column=2, padx=5, pady=5)

# BP地图
map_frame = tk.LabelFrame(teammap_frame, text='BP地图', padx=5, pady=4)
map_frame.pack(side=tk.TOP, pady=4)

mapnamea_label = ttk.Label(map_frame, text="禁用地图")
mapnamea_label.grid(row=0, column=0, padx=5, pady=5)
mapnameb_label = ttk.Label(map_frame, text="选用地图")
mapnameb_label.grid(row=0, column=1, padx=5, pady=5)
mapnamea_combobox = ttk.Combobox(map_frame, values=listmap)
mapnamea_combobox.current(0)
mapnamea_combobox.grid(row=1, column=0, padx=5, pady=5)
mapnameb_combobox = ttk.Combobox(map_frame, values=listmap)
mapnameb_combobox.current(0)
mapnameb_combobox.grid(row=1, column=1, padx=5, pady=5)

# 倒计时
djs_frame = tk.LabelFrame(teammap_frame, text='倒计时', padx=5, pady=4)
djs_frame.pack(side=tk.TOP, pady=4)

djs_entry = ttk.Entry(djs_frame, width=14)
djs_entry.insert(0, "请输入正整数")
djs_entry.default_text = "请输入正整数"
djs_entry.config(foreground="gray")
djs_entry.bind("<Button-1>", handle_default_text)
djs_entry.bind("<FocusIn>", handle_default_text)
djs_entry.bind("<FocusOut>", handle_focus_out)
djs_entry.grid(row=0, column=0, padx=5, pady=5)

djs_label = ttk.Label(djs_frame, text="当前未进行计时")
djs_label.grid(row=1, column=0, padx=5, pady=5)

djs_button = ttk.Button(djs_frame, text="执行", command=djs)
djs_button.grid(row=0, column=1, padx=5, pady=5)

stopdjs_button = ttk.Button(djs_frame, text="stop!", command=stopdjs)
stopdjs_button.grid(row=1, column=1, padx=5, pady=5)

switch_var = tk.IntVar()
switch_var.set(0)
djs_Switch = ttk.Checkbutton(djs_frame, text="倒计时开关", variable=switch_var, style="Switch.TCheckbutton")
djs_Switch.grid(row=0, column=2, sticky="w", padx=5, pady=5)
# print(switch_var)

# 队伍
Team_frame = tk.LabelFrame(root, padx=5, pady=5, borderwidth=0, highlightthickness=0)
Team_frame.grid(row=0, column=0, padx=5, pady=5)

# 求生者方
Sur_frame = tk.LabelFrame(Team_frame, text='求生者方', padx=5, pady=5)
Sur_frame.grid(row=0, column=0, padx=5, pady=5)

# 求生者 禁用
Sur_ban_frame = tk.LabelFrame(Sur_frame, text='禁用求生者', padx=5, pady=5)
Sur_ban_frame.grid(row=0, column=0, padx=5, pady=5)

Killerban1_label = ttk.Label(Sur_ban_frame, text="Ban1（A队侍从1a）")
Killerban1_label.grid(row=0, column=0, padx=5, pady=5)
Killerban2_label = ttk.Label(Sur_ban_frame, text="Ban2（B队侍从1a）")
Killerban2_label.grid(row=0, column=1, padx=5, pady=5)
Killerban3_label = ttk.Label(Sur_ban_frame, text="Ban3（A队侍从2a）")
Killerban3_label.grid(row=0, column=2, padx=5, pady=5)
Killerban4_label = ttk.Label(Sur_ban_frame, text="Ban4（B队侍从2a）")
Killerban4_label.grid(row=0, column=3, padx=5, pady=5)
Killerban5_label = ttk.Label(Sur_ban_frame, text="（A队国王a）")
Killerban5_label.grid(row=0, column=4, padx=5, pady=5)
Killerban6_label = ttk.Label(Sur_ban_frame, text="（B队国王a）")
Killerban6_label.grid(row=0, column=5, padx=5, pady=5)

Killerban1_label = ttk.Label(Sur_ban_frame, text="（A队侍从1b）")
Killerban1_label.grid(row=2, column=0, padx=5, pady=5)
Killerban2_label = ttk.Label(Sur_ban_frame, text="（B队侍从1b）")
Killerban2_label.grid(row=2, column=1, padx=5, pady=5)
Killerban3_label = ttk.Label(Sur_ban_frame, text="（A队侍从2b）")
Killerban3_label.grid(row=2, column=2, padx=5, pady=5)
Killerban4_label = ttk.Label(Sur_ban_frame, text="（B队侍从2b）")
Killerban4_label.grid(row=2, column=3, padx=5, pady=5)
Killerban5_label = ttk.Label(Sur_ban_frame, text="（A队国王b）")
Killerban5_label.grid(row=2, column=4, padx=5, pady=5)
Killerban6_label = ttk.Label(Sur_ban_frame, text="（B队国王b）")
Killerban6_label.grid(row=2, column=5, padx=5, pady=5)

# 在这里初始化预处理选项
processed_listsur = preprocess_options(listsur)
processed_listkiller = preprocess_options(listkiller)
processed_listsurlock = preprocess_options(listsurlock)
processed_listkillerlock = preprocess_options(listkillerlock)

Killerban1_combobox = ttk.Combobox(Sur_ban_frame, values=listsurlock, width=16)
Killerban1_combobox.current(0)
Killerban1_combobox.grid(row=1, column=0, padx=5, pady=5)
Killerban1_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Killerban1_combobox, event, processed_listsurlock))
Killerban1_combobox.bind('<Return>', open_dropdown)

Killerban2_combobox = ttk.Combobox(Sur_ban_frame, values=listsurlock, width=16)
Killerban2_combobox.current(0)
Killerban2_combobox.grid(row=1, column=1, padx=5, pady=5)
Killerban2_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Killerban2_combobox, event, processed_listsurlock))
Killerban2_combobox.bind('<Return>', open_dropdown)

Killerban3_combobox = ttk.Combobox(Sur_ban_frame, values=listsurlock, width=16)
Killerban3_combobox.current(0)
Killerban3_combobox.grid(row=1, column=2, padx=5, pady=5)
Killerban3_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Killerban3_combobox, event, processed_listsurlock))
Killerban3_combobox.bind('<Return>', open_dropdown)

Killerban4_combobox = ttk.Combobox(Sur_ban_frame, values=listsurlock, width=16)
Killerban4_combobox.current(0)
Killerban4_combobox.grid(row=1, column=3, padx=5, pady=5)
Killerban4_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Killerban4_combobox, event, processed_listsurlock))
Killerban4_combobox.bind('<Return>', open_dropdown)

Killerban5_combobox = ttk.Combobox(Sur_ban_frame, values=listsurlock, width=16)
Killerban5_combobox.current(0)
Killerban5_combobox.grid(row=1, column=4, padx=5, pady=5)
Killerban5_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Killerban5_combobox, event, processed_listsurlock))
Killerban5_combobox.bind('<Return>', open_dropdown)

Killerban6_combobox = ttk.Combobox(Sur_ban_frame, values=listsurlock, width=16)
Killerban6_combobox.current(0)
Killerban6_combobox.grid(row=1, column=5, padx=5, pady=5)
Killerban6_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Killerban6_combobox, event, processed_listsurlock))
Killerban6_combobox.bind('<Return>', open_dropdown)

Killerban11_combobox = ttk.Combobox(Sur_ban_frame, values=listsurlock, width=16)
Killerban11_combobox.current(0)
Killerban11_combobox.grid(row=3, column=0, padx=5, pady=5)
Killerban11_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Killerban11_combobox, event, processed_listsurlock))
Killerban11_combobox.bind('<Return>', open_dropdown)

Killerban22_combobox = ttk.Combobox(Sur_ban_frame, values=listsurlock, width=16)
Killerban22_combobox.current(0)
Killerban22_combobox.grid(row=3, column=1, padx=5, pady=5)
Killerban22_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Killerban22_combobox, event, processed_listsurlock))
Killerban22_combobox.bind('<Return>', open_dropdown)

Killerban33_combobox = ttk.Combobox(Sur_ban_frame, values=listsurlock, width=16)
Killerban33_combobox.current(0)
Killerban33_combobox.grid(row=3, column=2, padx=5, pady=5)
Killerban33_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Killerban33_combobox, event, processed_listsurlock))
Killerban33_combobox.bind('<Return>', open_dropdown)

Killerban44_combobox = ttk.Combobox(Sur_ban_frame, values=listsurlock, width=16)
Killerban44_combobox.current(0)
Killerban44_combobox.grid(row=3, column=3, padx=5, pady=5)
Killerban44_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Killerban44_combobox, event, processed_listsurlock))
Killerban44_combobox.bind('<Return>', open_dropdown)

Killerban55_combobox = ttk.Combobox(Sur_ban_frame, values=listsurlock, width=16)
Killerban55_combobox.current(0)
Killerban55_combobox.grid(row=3, column=4, padx=5, pady=5)
Killerban55_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Killerban55_combobox, event, processed_listsurlock))
Killerban55_combobox.bind('<Return>', open_dropdown)

Killerban66_combobox = ttk.Combobox(Sur_ban_frame, values=listsurlock, width=16)
Killerban66_combobox.current(0)
Killerban66_combobox.grid(row=3, column=5, padx=5, pady=5)
Killerban66_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Killerban66_combobox, event, processed_listsurlock))
Killerban66_combobox.bind('<Return>', open_dropdown)


# 求生者方选用
Sur_Team_frame = tk.LabelFrame(Sur_frame, text='求生者方选用', padx=5, pady=5)
Sur_Team_frame.grid(row=2, column=0, padx=5, pady=5)

surname1_label = ttk.Label(Sur_Team_frame, text="求生者1（A队侍从1）")
surname1_label.grid(row=0, column=0, padx=5, pady=5)
surname2_label = ttk.Label(Sur_Team_frame, text="求生者2（B队侍从1）")
surname2_label.grid(row=0, column=1, padx=5, pady=5)
surname3_label = ttk.Label(Sur_Team_frame, text="求生者3（A队侍从2）")
surname3_label.grid(row=0, column=2, padx=5, pady=5)
surname4_label = ttk.Label(Sur_Team_frame, text="求生者4（B队侍从2）")
surname4_label.grid(row=0, column=3, padx=5, pady=5)
surname4_label = ttk.Label(Sur_Team_frame, text="（A队国王）")
surname4_label.grid(row=0, column=4, padx=5, pady=5)
surname4_label = ttk.Label(Sur_Team_frame, text="（B队国王）")
surname4_label.grid(row=0, column=5, padx=5, pady=5)

surname1_entry = ttk.Entry(Sur_Team_frame, width=14)
surname1_entry.insert(0, "请输入选手名称")
surname1_entry.default_text = "请输入选手名称"
surname1_entry.config(foreground="gray")
surname1_entry.bind("<Button-1>", handle_default_text)
surname1_entry.bind("<FocusIn>", handle_default_text)
surname1_entry.bind("<FocusOut>", handle_focus_out)
surname1_entry.grid(row=1, column=0, padx=5, pady=5)
surname2_entry = ttk.Entry(Sur_Team_frame, width=14)
surname2_entry.insert(0, "请输入选手名称")
surname2_entry.default_text = "请输入选手名称"
surname2_entry.config(foreground="gray")
surname2_entry.bind("<Button-1>", handle_default_text)
surname2_entry.bind("<FocusIn>", handle_default_text)
surname2_entry.bind("<FocusOut>", handle_focus_out)
surname2_entry.grid(row=1, column=1, padx=5, pady=5)
surname3_entry = ttk.Entry(Sur_Team_frame, width=14)
surname3_entry.insert(0, "请输入选手名称")
surname3_entry.default_text = "请输入选手名称"
surname3_entry.config(foreground="gray")
surname3_entry.bind("<Button-1>", handle_default_text)
surname3_entry.bind("<FocusIn>", handle_default_text)
surname3_entry.bind("<FocusOut>", handle_focus_out)
surname3_entry.grid(row=1, column=2, padx=5, pady=5)
surname4_entry = ttk.Entry(Sur_Team_frame, width=14)
surname4_entry.insert(0, "请输入选手名称")
surname4_entry.default_text = "请输入选手名称"
surname4_entry.config(foreground="gray")
surname4_entry.bind("<Button-1>", handle_default_text)
surname4_entry.bind("<FocusIn>", handle_default_text)
surname4_entry.bind("<FocusOut>", handle_focus_out)
surname4_entry.grid(row=1, column=3, padx=5, pady=5)
surname5_entry = ttk.Entry(Sur_Team_frame, width=14)
surname5_entry.insert(0, "请输入选手名称")
surname5_entry.default_text = "请输入选手名称"
surname5_entry.config(foreground="gray")
surname5_entry.bind("<Button-1>", handle_default_text)
surname5_entry.bind("<FocusIn>", handle_default_text)
surname5_entry.bind("<FocusOut>", handle_focus_out)
surname5_entry.grid(row=1, column=4, padx=5, pady=5)
surname6_entry = ttk.Entry(Sur_Team_frame, width=14)
surname6_entry.insert(0, "请输入选手名称")
surname6_entry.default_text = "请输入选手名称"
surname6_entry.config(foreground="gray")
surname6_entry.bind("<Button-1>", handle_default_text)
surname6_entry.bind("<FocusIn>", handle_default_text)
surname6_entry.bind("<FocusOut>", handle_focus_out)
surname6_entry.grid(row=1, column=5, padx=5, pady=5)

surpick1_combobox = ttk.Combobox(Sur_Team_frame, values=listsur, width=16)
surpick1_combobox.current(0)
surpick1_combobox.grid(row=2, column=0, padx=5, pady=5)
surpick1_combobox.bind('<KeyRelease>', lambda event: filter_combobox(surpick1_combobox, event, processed_listsur))
surpick1_combobox.bind('<Return>', open_dropdown)

surpick2_combobox = ttk.Combobox(Sur_Team_frame, values=listsur, width=16)
surpick2_combobox.current(0)
surpick2_combobox.grid(row=2, column=1, padx=5, pady=5)
surpick2_combobox.bind('<KeyRelease>', lambda event: filter_combobox(surpick2_combobox, event, processed_listsur))
surpick2_combobox.bind('<Return>', open_dropdown)

surpick3_combobox = ttk.Combobox(Sur_Team_frame, values=listsur, width=16)
surpick3_combobox.current(0)
surpick3_combobox.grid(row=2, column=2, padx=5, pady=5)
surpick3_combobox.bind('<KeyRelease>', lambda event: filter_combobox(surpick3_combobox, event, processed_listsur))
surpick3_combobox.bind('<Return>', open_dropdown)

surpick4_combobox = ttk.Combobox(Sur_Team_frame, values=listsur, width=16)
surpick4_combobox.current(0)
surpick4_combobox.grid(row=2, column=3, padx=5, pady=5)
surpick4_combobox.bind('<KeyRelease>', lambda event: filter_combobox(surpick4_combobox, event, processed_listsur))
surpick4_combobox.bind('<Return>', open_dropdown)

surpick5_combobox = ttk.Combobox(Sur_Team_frame, values=listsur, width=16)
surpick5_combobox.current(0)
surpick5_combobox.grid(row=2, column=4, padx=5, pady=5)
surpick5_combobox.bind('<KeyRelease>', lambda event: filter_combobox(surpick5_combobox, event, processed_listsur))
surpick5_combobox.bind('<Return>', open_dropdown)

surpick6_combobox = ttk.Combobox(Sur_Team_frame, values=listsur, width=16)
surpick6_combobox.current(0)
surpick6_combobox.grid(row=2, column=5, padx=5, pady=5)
surpick6_combobox.bind('<KeyRelease>', lambda event: filter_combobox(surpick6_combobox, event, processed_listsur))
surpick6_combobox.bind('<Return>', open_dropdown)

# 监管者方
Killer_frame = tk.LabelFrame(Team_frame, text='监管者方', padx=5, pady=5)
Killer_frame.grid(row=1, column=0, padx=5, pady=5)

# 监管者方选用
Killer_Team_frame = tk.LabelFrame(Killer_frame, text='监管者方选用', padx=5, pady=5)
Killer_Team_frame.grid(row=1, column=1, padx=5, pady=5)

Killername_label = ttk.Label(Killer_Team_frame, text="监管者（a队骑士）")
Killername_label.grid(row=1, column=0, padx=5, pady=5)

Killername_entry = ttk.Entry(Killer_Team_frame, width=14)
Killername_entry.insert(0, "请输入选手名称")
Killername_entry.default_text = "请输入选手名称"
Killername_entry.config(foreground="gray")
Killername_entry.bind("<Button-1>", handle_default_text)
Killername_entry.bind("<FocusIn>", handle_default_text)
Killername_entry.bind("<FocusOut>", handle_focus_out)
Killername_entry.grid(row=2, column=0, padx=5, pady=5)

Killerpick_combobox = ttk.Combobox(Killer_Team_frame, values=listkiller, width=16)
Killerpick_combobox.current(0)
Killerpick_combobox.grid(row=3, column=0, padx=5, pady=5)
Killerpick_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Killerpick_combobox, event, processed_listkiller))
Killerpick_combobox.bind('<Return>', open_dropdown)

Killername1_label = ttk.Label(Killer_Team_frame, text="（b队骑士）")
Killername1_label.grid(row=1, column=1, padx=5, pady=5)

Killername1_entry = ttk.Entry(Killer_Team_frame, width=14)
Killername1_entry.insert(0, "请输入选手名称")
Killername1_entry.default_text = "请输入选手名称"
Killername1_entry.config(foreground="gray")
Killername1_entry.bind("<Button-1>", handle_default_text)
Killername1_entry.bind("<FocusIn>", handle_default_text)
Killername1_entry.bind("<FocusOut>", handle_focus_out)
Killername1_entry.grid(row=2, column=1, padx=5, pady=5)

Killerpick1_combobox = ttk.Combobox(Killer_Team_frame, values=listkiller, width=16)
Killerpick1_combobox.current(0)
Killerpick1_combobox.grid(row=3, column=1, padx=5, pady=5)
Killerpick1_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Killerpick1_combobox, event, processed_listkiller))
Killerpick1_combobox.bind('<Return>', open_dropdown)

# 监管者 禁用
Killer_ban_frame = tk.LabelFrame(Killer_frame, text='禁用监管者', padx=5, pady=5)
Killer_ban_frame.grid(row=1, column=0, padx=5, pady=5)

surban1_label = ttk.Label(Killer_ban_frame, text="Ban1（A队骑士a）")
surban1_label.grid(row=0, column=0, padx=5, pady=5)
surban2_label = ttk.Label(Killer_ban_frame, text="Ban2（A队骑士b）")
surban2_label.grid(row=0, column=1, padx=5, pady=5)
surban3_label = ttk.Label(Killer_ban_frame, text="Ban3（B队骑士a）")
surban3_label.grid(row=0, column=2, padx=5, pady=5)
surban3_label = ttk.Label(Killer_ban_frame, text="（B队骑士b）")
surban3_label.grid(row=0, column=3, padx=5, pady=5)

surban1_combobox = ttk.Combobox(Killer_ban_frame, values=listkillerlock, width=16)
surban1_combobox.current(0)
surban1_combobox.grid(row=1, column=0, padx=5, pady=5)
surban1_combobox.bind('<KeyRelease>', lambda event: filter_combobox(surban1_combobox, event, processed_listkillerlock))
surban1_combobox.bind('<Return>', open_dropdown)

surban2_combobox = ttk.Combobox(Killer_ban_frame, values=listkillerlock, width=16)
surban2_combobox.current(0)
surban2_combobox.grid(row=1, column=1, padx=5, pady=5)
surban2_combobox.bind('<KeyRelease>', lambda event: filter_combobox(surban2_combobox, event, processed_listkillerlock))
surban2_combobox.bind('<Return>', open_dropdown)

surban3_combobox = ttk.Combobox(Killer_ban_frame, values=listkillerlock, width=16)
surban3_combobox.current(0)
surban3_combobox.grid(row=1, column=2, padx=5, pady=5)
surban3_combobox.bind('<KeyRelease>', lambda event: filter_combobox(surban3_combobox, event, processed_listkillerlock))
surban3_combobox.bind('<Return>', open_dropdown)

surban4_combobox = ttk.Combobox(Killer_ban_frame, values=listkillerlock, width=16)
surban4_combobox.current(0)
surban4_combobox.grid(row=1, column=3, padx=5, pady=5)
surban4_combobox.bind('<KeyRelease>', lambda event: filter_combobox(surban4_combobox, event, processed_listkillerlock))
surban4_combobox.bind('<Return>', open_dropdown)

# 全局禁用
Wholeban_frame = tk.LabelFrame(Team_frame, text='全局禁用', padx=5, pady=5)
Wholeban_frame.grid(row=2, column=0, padx=5, pady=5)

Wholeban1_label = ttk.Label(Wholeban_frame, text="全局禁用1")
Wholeban1_label.grid(row=0, column=0, padx=5, pady=5)
Wholeban2_label = ttk.Label(Wholeban_frame, text="全局禁用2")
Wholeban2_label.grid(row=0, column=1, padx=5, pady=5)
Wholeban3_label = ttk.Label(Wholeban_frame, text="全局禁用3")
Wholeban3_label.grid(row=0, column=2, padx=5, pady=5)
Wholeban4_label = ttk.Label(Wholeban_frame, text="全局禁用4")
Wholeban4_label.grid(row=0, column=3, padx=5, pady=5)
Wholeban5_label = ttk.Label(Wholeban_frame, text="全局禁用5")
Wholeban5_label.grid(row=0, column=4, padx=5, pady=5)
Wholeban6_label = ttk.Label(Wholeban_frame, text="全局禁用6")
Wholeban6_label.grid(row=0, column=5, padx=5, pady=5)

Wholeban1_combobox = ttk.Combobox(Wholeban_frame, values=listsurlock, width=16)
Wholeban1_combobox.current(0)
Wholeban1_combobox.grid(row=1, column=0, padx=5, pady=5)
Wholeban1_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Wholeban1_combobox, event, processed_listsurlock))
Wholeban1_combobox.bind('<Return>', open_dropdown)

Wholeban2_combobox = ttk.Combobox(Wholeban_frame, values=listsurlock, width=16)
Wholeban2_combobox.current(0)
Wholeban2_combobox.grid(row=1, column=1, padx=5, pady=5)
Wholeban2_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Wholeban2_combobox, event, processed_listsurlock))
Wholeban2_combobox.bind('<Return>', open_dropdown)

Wholeban3_combobox = ttk.Combobox(Wholeban_frame, values=listsurlock, width=16)
Wholeban3_combobox.current(0)
Wholeban3_combobox.grid(row=1, column=2, padx=5, pady=5)
Wholeban3_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Wholeban3_combobox, event, processed_listsurlock))
Wholeban3_combobox.bind('<Return>', open_dropdown)

Wholeban4_combobox = ttk.Combobox(Wholeban_frame, values=listsurlock, width=16)
Wholeban4_combobox.current(0)
Wholeban4_combobox.grid(row=1, column=3, padx=5, pady=5)
Wholeban4_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Wholeban4_combobox, event, processed_listsurlock))
Wholeban4_combobox.bind('<Return>', open_dropdown)

Wholeban5_combobox = ttk.Combobox(Wholeban_frame, values=listsurlock, width=16)
Wholeban5_combobox.current(0)
Wholeban5_combobox.grid(row=1, column=4, padx=5, pady=5)
Wholeban5_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Wholeban5_combobox, event, processed_listsurlock))
Wholeban5_combobox.bind('<Return>', open_dropdown)

Wholeban6_combobox = ttk.Combobox(Wholeban_frame, values=listsurlock, width=16)
Wholeban6_combobox.current(0)
Wholeban6_combobox.grid(row=1, column=5, padx=5, pady=5)
Wholeban6_combobox.bind('<KeyRelease>', lambda event: filter_combobox(Wholeban6_combobox, event, processed_listsurlock))
Wholeban6_combobox.bind('<Return>', open_dropdown)


# 定义全局变量
bpwindow = None
canvas = None
bg_photo = None
fullbool = False
job_dict = {}
option_upload_window = None
upload1_window = None
upload2_window = None
upload3_window = None


# 初始数据、实时数据、上一次数据
Initial_data = ['队伍名称', '队伍名称', '求生者比分', '监管者比分', '', '', '', '', '', '请输入选手名称',
                '请输入选手名称', '请输入选手名称', '请输入选手名称', '', '', '', '', '', '', '', '', '请输入选手名称',
                '', '请输入赛事名称', '0', '', '', '', '', '', '', '', '', '', '', '请输入选手名称', '请输入选手名称',
                '', '', '', '请输入选手名称', '', '', '', '', '', '', '', '请输入比分“W”', '请输入比分“W”',
                '请输入比分“D”', '请输入比分“D”', '请输入比分“L”', '请输入比分“L”', '请输入正整数', '']
live_data = []
old_data = []
textphoto01 = textphoto02 = textphoto03 = textphoto04 = textphoto05 = textphoto06 = textphoto07 = textphoto00 = \
textphoto11 = textphoto11b = textphoto12 = textphoto12b = textphoto13 = textphoto13b = textphoto14 = textphoto14b = \
textphoto10 = textphoto30 = textphoto31 = textphoto32 = textphoto33 = textphoto34 = \
photo05 = photo06 = phot07 = photo11 = photo11l = photo12 = photo20 = photo20l = photo21 = photo21l = \
photo22 = photo22l = photo23 = photo23l = photo24 = photo24l = photo25 = photo25l = photo26 = photo26l = \
photo27 = photo27l = photo28 = photo28l = photo29 = photo29l = photo2a0 = photo2a0l = photo2a1 = photo2a1l = \
photo2a2 = photo2a2l = photo2a3 = photo2a3l = photo2a4 = photo2a4l = photo2a5 = photo2a5l = photo2a6 = photo2a6l = \
photo2a7 = photo2a7l = photo2a8 = photo2a8l = photo2a9 = photo2a9l = photo30 = photo30b = photo31 = photo31b = \
photo32 = photo32b = photo33 = photo33b = photo34 = photo40 = None

def create_image_full(canvas, x, y, image, tags):
    canvas.create_image(fullcounter(x, 0), fullcounter(y, 1), image=image, tags=tags)

# 刷新函数，运行此函数会更新新窗口bpwindow的图片内容
def pic_changed(canvas):
    global live_data, bpwindow
    global textphoto01, textphoto02, textphoto03, textphoto04, textphoto05, textphoto06, textphoto07, textphoto00, \
        textphoto11, textphoto11b, textphoto12, textphoto12b, textphoto13, textphoto13b, textphoto14, textphoto14b, \
        textphoto10, textphoto30, textphoto31, textphoto32, textphoto33, textphoto34, \
        photo05, photo06, phot07, photo11, photo11l, photo12, photo20, photo20l, photo21, photo21l, \
        photo22, photo22l, photo23, photo23l, photo24, photo24l, photo25, photo25l, photo26, photo26l, \
        photo27, photo27l, photo28, photo28l, photo29, photo29l, photo2a0, photo2a0l, photo2a1, photo2a1l, photo2b0, photo2b0l, \
        photo2a2, photo2a2l, photo2a3, photo2a3l, photo2a4, photo2a4l, photo2a5, photo2a5l, photo2a6, photo2a6l, \
        photo2a7, photo2a7l, photo2a8, photo2a8l, photo2a9, photo2a9l, photo30, photo30b, photo31, photo31b, \
        photo32, photo32b, photo33, photo33b, photo34, photo40
    # root.after(1000, pic_changed)
    if bpwindow:
        try:
            if live_data[24] == 0:
                photo11, photo11l = bp_bmap(live_data[4], 270, 155)
                photo12 = bp_other(live_data[5], 'map', 155)
                photo20, photo20l = bp_bper(live_data[6], 'killer', 100, 100)
                photo21, photo21l = bp_bper(live_data[7], 'killer', 100, 100)
                photo22, photo22l = bp_bper(live_data[8], 'killer', 100, 100)
                photo23, photo23l = bp_bper(live_data[17], 'sur', 100, 100)
                photo24, photo24l = bp_bper(live_data[18], 'sur', 100, 100)
                photo25, photo25l = bp_bper(live_data[19], 'sur', 100, 100)
                photo26, photo26l = bp_bper(live_data[20], 'sur', 100, 100)
                photo30 = bp_other(live_data[22], 'Bigkiller', 416)
                photo31 = bp_other(live_data[13], 'sur', 180)
                photo32 = bp_other(live_data[14], 'sur', 180)
                photo33 = bp_other(live_data[15], 'sur', 180)
                photo34 = bp_other(live_data[16], 'sur', 180)

                canvas.delete("image")

                # 求生队伍名称
                textphoto01 = bp_text(live_data[0], 40)
                create_image_full(canvas,514, 75, image=textphoto01, tags="image")
                # 监管队伍名称
                textphoto02 = bp_text(live_data[1], 40)
                create_image_full(canvas,1228, 75, image=textphoto02, tags="image")
                # 比分
                textphoto03 = bp_text(live_data[2] + ':' + live_data[3], 60)
                create_image_full(canvas,870, 66, image=textphoto03, tags="image")
                # 赛事名称
                textphoto00 = bp_text(live_data[23], 36)
                create_image_full(canvas,760, 914, image=textphoto00, tags="image")

                # 求生选手ID1
                textphoto11 = bp_text(live_data[0] + '_' + live_data[9], 34)
                create_image_full(canvas,270, 518, image=textphoto11, tags="image")
                # 求生选手ID2
                textphoto12 = bp_text(live_data[0] + '_' + live_data[10], 34)
                create_image_full(canvas,700, 518, image=textphoto12, tags="image")
                # 求生选手ID3
                textphoto13 = bp_text(live_data[0] + '_' + live_data[11], 34)
                create_image_full(canvas,262, 780, image=textphoto13, tags="image")
                # 求生选手ID4
                textphoto14 = bp_text(live_data[0] + '_' + live_data[12], 34)
                create_image_full(canvas,696, 780, image=textphoto14, tags="image")
                # 监管选手ID
                textphoto10 = bp_text(live_data[1] + '_' + live_data[21], 34)
                create_image_full(canvas,1440, 804, image=textphoto10, tags="image")

                # ban map
                create_image_full(canvas,184, 65, image=photo11, tags="image")
                create_image_full(canvas,184, 65, image=photo11l, tags="image")
                # pick map
                create_image_full(canvas,1578, 65, image=photo12, tags="image")

                # ban监管1
                create_image_full(canvas,286, 218, image=photo20, tags="image")
                create_image_full(canvas,286, 218, image=photo20l, tags="image")
                # ban监管2
                create_image_full(canvas,479, 218, image=photo21, tags="image")
                create_image_full(canvas,479, 218, image=photo21l, tags="image")
                # ban监管3
                create_image_full(canvas,672, 218, image=photo22, tags="image")
                create_image_full(canvas,672, 218, image=photo22l, tags="image")
                # ban求生1
                create_image_full(canvas,1238, 916, image=photo23, tags="image")
                create_image_full(canvas,1238, 916, image=photo23l, tags="image")
                # ban求生2
                create_image_full(canvas,1380, 916, image=photo24, tags="image")
                create_image_full(canvas,1380, 916, image=photo24l, tags="image")
                # ban求生3
                create_image_full(canvas,1516, 916, image=photo25, tags="image")
                create_image_full(canvas,1516, 916, image=photo25l, tags="image")
                # ban求生4
                create_image_full(canvas,1660, 916, image=photo26, tags="image")
                create_image_full(canvas,1660, 916, image=photo26l, tags="image")

                # pick监管
                create_image_full(canvas,1448, 514, image=photo30, tags="image")
                # pick求生1
                create_image_full(canvas,275, 386, image=photo31, tags="image")
                # pick求生2
                create_image_full(canvas,700, 386, image=photo32, tags="image")
                # pick求生3
                create_image_full(canvas,275, 654, image=photo33, tags="image")
                # pick求生4
                create_image_full(canvas,700, 654, image=photo34, tags="image")

        except FileNotFoundError:
            print("pic_changed出错！")

# 新窗口bpwindow的拖拽功能
def on_mouse_press(event):
    # 记录鼠标按下时的坐标和窗口当前的位置
    global last_x, last_y
    last_x = event.x_root
    last_y = event.y_root
def on_mouse_drag(event):
    # 计算鼠标的偏移量，并移动窗口到新的位置
    global last_x, last_y
    new_x = bpwindow.winfo_x() + (event.x_root - last_x)
    new_y = bpwindow.winfo_y() + (event.y_root - last_y)
    bpwindow.geometry(f"+{new_x}+{new_y}")
    last_x = event.x_root
    last_y = event.y_root

def goto_fullscreen(event):
    global fullbool
    if event.char:  # 检查是否有字符输入
        print(f"全屏函数：有字符输入: {event.char}")
    elif event.keysym == 'F11':  # 检查是否有特殊键被按下
        print(f"全屏函数：f11被按下")
        if fullbool == False:
            bpwindow.attributes("-fullscreen", True)
            fullbool = True
            my_subprogram(fullbool)
            on_window_close()
            generate_new_window(True)
        else:
            bpwindow.attributes("-fullscreen", False)
            fullbool = False
            my_subprogram(fullbool)
            on_window_close()
            generate_new_window(False)
    # elif event.keysym:  # 检查是否有特殊键被按下
    #     print(f"全屏函数：有特殊按键被按下: {event.keysym}")


# 新窗口bpwindow创建
def generate_new_window(fullbool):
    global bpwindow, canvas, bg_photo
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    backgroundpathdict = {
        0: "data/background.png"
    }
    if bpwindow is None:
        bpwindow = tk.Toplevel(root)  # 创建新窗口
        bpwindow.geometry("1760x990")
        bpwindow.protocol("WM_DELETE_WINDOW", on_window_close)  # 设置关闭窗口时的回调函数
        bpwindow.resizable(False, False)  # 横纵均不允许调整
        bpwindow.title('第五人格bp窗口')
        bpwindow.iconbitmap(get_resource_path("icon.ico"))

        # bpwindow.overrideredirect(True)
        bpwindow.attributes('-fullscreen', fullbool)
        bpwindow.bind("<ButtonPress-1>", on_mouse_press)
        bpwindow.bind("<B1-Motion>", on_mouse_drag)
        bpwindow.bind_all("<F11>", goto_fullscreen)  # 按下 F11 键切换全屏
        bpwindow.bind_all("<Escape>", on_window_close_esc)  # 按下 Esc 键退出

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


        canvas.config(highlightthickness=0)

        pic_changed(canvas)
        #     刷新

    else:
        messagebox.showwarning(title='提示', message='你无法同时打开两个bp窗口！')

# 新窗口关闭
def on_window_close():
    global bpwindow
    bpwindow.destroy()
    bpwindow = None
#     非常重要，先destroy，否则会造成窗口无法正常关闭

# esc关闭
def on_window_close_esc(event):
    global bpwindow
    bpwindow.destroy()
    bpwindow = None
#     非常重要，先destroy，否则会造成窗口无法正常关闭


# 重置控制台
def clear_console():
    scorea_spinbox.delete(0, tk.END)
    scorea_spinbox.insert(0, Initial_data[2])
    scoreb_spinbox.delete(0, tk.END)
    scoreb_spinbox.insert(0, Initial_data[3])
    mapnamea_combobox.set(Initial_data[4])
    mapnameb_combobox.set(Initial_data[5])
    surban1_combobox.set(Initial_data[6])
    surban2_combobox.set(Initial_data[7])
    surban3_combobox.set(Initial_data[8])
    surban4_combobox.set(Initial_data[39])
    surname1_entry.delete(0, tk.END)
    surname1_entry.insert(0, Initial_data[9])
    surname1_entry.config(foreground="gray")
    surname2_entry.delete(0, tk.END)
    surname2_entry.insert(0, Initial_data[10])
    surname2_entry.config(foreground="gray")
    surname3_entry.delete(0, tk.END)
    surname3_entry.insert(0, Initial_data[11])
    surname3_entry.config(foreground="gray")
    surname4_entry.delete(0, tk.END)
    surname4_entry.insert(0, Initial_data[12])
    surname4_entry.config(foreground="gray")
    surname5_entry.delete(0, tk.END)
    surname5_entry.insert(0, Initial_data[35])
    surname5_entry.config(foreground="gray")
    surname6_entry.delete(0, tk.END)
    surname6_entry.insert(0, Initial_data[36])
    surname6_entry.config(foreground="gray")
    surpick1_combobox.set(Initial_data[13])
    surpick2_combobox.set(Initial_data[14])
    surpick3_combobox.set(Initial_data[15])
    surpick4_combobox.set(Initial_data[16])
    surpick5_combobox.set(Initial_data[37])
    surpick5_combobox.set(Initial_data[38])
    Killerban1_combobox.set(Initial_data[17])
    Killerban2_combobox.set(Initial_data[18])
    Killerban3_combobox.set(Initial_data[19])
    Killerban4_combobox.set(Initial_data[20])
    Killerban5_combobox.set(Initial_data[27])
    Killerban6_combobox.set(Initial_data[28])
    Killerban11_combobox.set(Initial_data[29])
    Killerban22_combobox.set(Initial_data[30])
    Killerban33_combobox.set(Initial_data[31])
    Killerban44_combobox.set(Initial_data[32])
    Killerban55_combobox.set(Initial_data[33])
    Killerban66_combobox.set(Initial_data[34])
    Killername_entry.delete(0, tk.END)
    Killername_entry.insert(0, Initial_data[21])
    Killername_entry.config(foreground="gray")
    Killername1_entry.delete(0, tk.END)
    Killername1_entry.insert(0, Initial_data[40])
    Killername1_entry.config(foreground="gray")
    Killerpick_combobox.set(Initial_data[22])
    Killerpick1_combobox.set(Initial_data[41])
    Event_Name_entry.delete(0, tk.END)
    Event_Name_entry.insert(0, Initial_data[23])
    Event_Name_entry.config(foreground="gray")
    Wholeban1_combobox.set(Initial_data[42])
    Wholeban2_combobox.set(Initial_data[43])
    Wholeban3_combobox.set(Initial_data[44])
    Wholeban4_combobox.set(Initial_data[45])
    Wholeban5_combobox.set(Initial_data[46])
    Wholeban6_combobox.set(Initial_data[47])
    teamwldwa_entry.delete(0, tk.END)
    teamwldwa_entry.insert(0, Initial_data[48])
    teamwldwa_entry.config(foreground="gray")
    teamwldwb_entry.delete(0, tk.END)
    teamwldwb_entry.insert(0, Initial_data[49])
    teamwldwb_entry.config(foreground="gray")
    teamwldda_entry.delete(0, tk.END)
    teamwldda_entry.insert(0, Initial_data[50])
    teamwldda_entry.config(foreground="gray")
    teamwlddb_entry.delete(0, tk.END)
    teamwlddb_entry.insert(0, Initial_data[51])
    teamwlddb_entry.config(foreground="gray")
    teamwldla_entry.delete(0, tk.END)
    teamwldla_entry.insert(0, Initial_data[52])
    teamwldla_entry.config(foreground="gray")
    teamwldlb_entry.delete(0, tk.END)
    teamwldlb_entry.insert(0, Initial_data[53])
    teamwldlb_entry.config(foreground="gray")
    teamlogoa_combobox.set('')
    teamlogob_combobox.set('')
    switch_var.set(0)


# 判断数据是否更新，更新则使用pic_changed()刷新图像
def update_data():
    global live_data, bpwindow, fullbool, job_dict, canvas
    if job_dict:
        for job_id in job_dict.keys():
            root.after_cancel(job_id)
            # print('清理了一个计时器')
        job_dict = {}
        # print('成功清理了所有计时器')
    # update_data()    # 获取各个组件的值
    teamnamea = teamlogoa_combobox.get()
    teamnameb = teamlogob_combobox.get()
    scorea = scorea_spinbox.get()
    scoreb = scoreb_spinbox.get()
    mapnamea = mapnamea_combobox.get()
    mapnameb = mapnameb_combobox.get()
    surban1 = surban1_combobox.get()
    surban2 = surban2_combobox.get()
    surban3 = surban3_combobox.get()
    surban4 = surban4_combobox.get()
    surname1 = surname1_entry.get()
    surname2 = surname2_entry.get()
    surname3 = surname3_entry.get()
    surname4 = surname4_entry.get()
    surname5 = surname5_entry.get()
    surname6 = surname6_entry.get()
    surpick1 = surpick1_combobox.get()
    surpick2 = surpick2_combobox.get()
    surpick3 = surpick3_combobox.get()
    surpick4 = surpick4_combobox.get()
    surpick5 = surpick5_combobox.get()
    surpick6 = surpick6_combobox.get()
    killerban1 = Killerban1_combobox.get()
    killerban2 = Killerban2_combobox.get()
    killerban3 = Killerban3_combobox.get()
    killerban4 = Killerban4_combobox.get()
    killerban5 = Killerban5_combobox.get()
    killerban6 = Killerban6_combobox.get()
    killerban11 = Killerban11_combobox.get()
    killerban22 = Killerban22_combobox.get()
    killerban33 = Killerban33_combobox.get()
    killerban44 = Killerban44_combobox.get()
    killerban55 = Killerban55_combobox.get()
    killerban66 = Killerban66_combobox.get()
    killername = Killername_entry.get()
    killername1 = Killername1_entry.get()
    killerpick = Killerpick_combobox.get()
    killerpick1 = Killerpick1_combobox.get()
    Wholeban1 = Wholeban1_combobox.get()
    Wholeban2 = Wholeban2_combobox.get()
    Wholeban3 = Wholeban3_combobox.get()
    Wholeban4 = Wholeban4_combobox.get()
    Wholeban5 = Wholeban5_combobox.get()
    Wholeban6 = Wholeban6_combobox.get()
    Teamwldwa = teamwldwa_entry.get()
    Teamwldwb = teamwldwb_entry.get()
    Teamwldda = teamwldda_entry.get()
    Teamwlddb = teamwlddb_entry.get()
    Teamwldla = teamwldla_entry.get()
    Teamwldlb = teamwldlb_entry.get()
    Event_Name = Event_Name_entry.get()
    mode_var = 0
    teamlogoa = teamlogoa_combobox.get()
    teamlogob = teamlogob_combobox.get()
    djsnum = djs_entry.get()
    djsswitch = switch_var.get()
    # 更新数据到 live_data 列表
    old_data = live_data
    live_data = [teamnamea, teamnameb, scorea, scoreb, mapnamea, mapnameb,
                 surban1, surban2, surban3, surname1, surname2, surname3,
                 surname4, surpick1, surpick2, surpick3, surpick4, killerban1,
                 killerban2, killerban3, killerban4, killername, killerpick,
                 Event_Name, mode_var, teamlogoa, teamlogob, killerban5, killerban6,
                 killerban11, killerban22, killerban33, killerban44, killerban55,
                 killerban66, surname5, surname6, surpick5, surpick6, surban4,
                 killername1, killerpick1, Wholeban1, Wholeban2, Wholeban3, Wholeban4,
                 Wholeban5, Wholeban6, Teamwldwa, Teamwldwb, Teamwldda, Teamwlddb,
                 Teamwldla, Teamwldlb, djsnum, djsswitch]
    if old_data == []:
        old_data = live_data
    if old_data[24] != live_data[24] and bpwindow is not None:
        on_window_close()
        generate_new_window(fullbool)
    if old_data != live_data:
        pic_changed(canvas)
    # 每秒更新一次数据
    # threading.Timer(1, update_data).start()
    job_id = root.after(1000, update_data)
    job_dict[job_id] = update_data
    # print(job_dict)
    # print(live_data)


# 运行与重置
button_frame = tk.LabelFrame(teammap_frame, padx=5, pady=4, borderwidth=0, highlightthickness=0)
button_frame.pack(side=tk.TOP)
run_button = ttk.Button(button_frame, text="打开BP窗口", style="Accent.TButton", command=lambda: generate_new_window(fullbool))
run_button.grid(row=0, column=0, padx=5, pady=5)
resetting_button = ttk.Button(button_frame, text="重置控制台", style="Accent.TButton", command=clear_console)
resetting_button.grid(row=1, column=0, padx=5, pady=5)
upload_button = ttk.Button(button_frame, text="上传新数据", style="Accent.TButton", command=lambda: open_option_upload_window())
upload_button.grid(row=0, column=1, padx=5, pady=5)
resetting_button = ttk.Button(button_frame, text="版本信息", command=show_message)
resetting_button.grid(row=1, column=1, padx=5, pady=5)


# 启动数据更新线程
update_data()
#pic_changed(canvas)

# 将窗口在屏幕中心运行
root.update()
root.minsize(root.winfo_width(), root.winfo_height())
x_cordinate = int((root.winfo_screenwidth() / 2) - (root.winfo_width() / 2))
y_cordinate = int((root.winfo_screenheight() / 2) - (root.winfo_height() / 2))
root.geometry("+{}+{}".format(x_cordinate, y_cordinate - 20))

# loop
root.mainloop()


'''
 # ##########################################################################
 # ####################                                  ####################
 # ####################          作者：@绿天sama           ####################
 # ####################                                  ####################
 # ##########################################################################
 #                                                                          #
 #                                   _oo8oo_                                #
 #                                  o8888888o                               #
 #                                  88" . "88                               #
 #                                  (| -_- |)                               #
 #                                  0\  =  /0                               #
 #                                ___/'==='\___                             #
 #                              .' \\|     |// '.                           #
 #                             / \\|||  :  |||// \                          #
 #                            / _||||| -:- |||||_ \                         #
 #                           |   | \\\  -  /// |   |                        #
 #                           | \_|  ''\---/''  |_/ |                        #
 #                           \  .-\__  '-'  __/-.  /                        #
 #                         ___'. .'  /--.--\  '. .'___                      #
 #                      ."" '<  '.___\_<|>_/___.'  >' "".                   #
 #                     | | :  `- \`.:`\ _ /`:.`/ -`  : | |                  #
 #                     \  \ `-.   \_ __\ /__ _/   .-` /  /                  #
 #                 =====`-.____`.___ \_____/ ___.`____.-`=====              #
 #                                   `=---=`                                #
 # ##########################################################################
 # ####################                                  ####################
 # ####################                                  ####################
 # ####################         佛祖保佑 永远无BUG          ####################
 # ####################                                  ####################
 # ##########################################################################
'''
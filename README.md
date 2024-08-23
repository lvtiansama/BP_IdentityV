# *BP_IdentityV_V1.5.3*

第五人格 BP系统

# 特别鸣谢
wiki.biligame.com

rdbende

# 版本更新内容

## `1.5.3`
注意！本版本有重大bug修复，请你及时更新并停用旧版本

### 修复：

1.修复了一处坐标错误。

2.修复了一处框架逻辑错误，或许这一修复可以让程序变得流畅，或许控制台不再会无法移动。（这不确定，欢迎大家测试反馈）

3.修复了模糊搜索会丢失“lock”的问题。

4.修复了一处定时任务异常堆积的错误。

## `1.5.2`

### 修复：

1.修复了中文输入法会把小写字母”y“的ASCII码121当作keycode回传给tkinter库，导致程序误以为用户按下了”f10“（keycode=121）导致输入框失去焦点，再次会触发系统菜单。

这一bug涉及到Windows系统的底层，与上一个全屏bug不同，f10的这个功能并非我想实现的，我没有给它绑定任何函数，我不能在不存在的函数中增加判断语句。因此我直接禁用了f10。

## `1.5.1`

### 修复：

1.修复了中文输入法会把小写字母”z“的ASCII码122当作keycode回传给tkinter库，导致程序误以为用户按下了”f11“（keycode=122）导致程序切换全屏。

修复方案为在全屏函数内增加判断，判断用户是否真实按下f11而非中文输入法返回了ascii码。


## `1.5`

### 常规更新：

1、角色库更新了`火灾调查员`、`“法罗女士”`

2、 地图更新了：`白沙街疯人院`、`闪金石窟`、`不归林`、`克雷伯格赛马场`


### 新增功能：

1、倒计时开关 可以在不需要的情况下将倒计时功能关闭。

2、”上传新数据“功能，在版本中，你可以自由添加角色、地图、战队logo，还可以一键清除缓存数据。

3、新增”模糊搜素“功能，支持控制台左侧30个选择框，以爱哭鬼为例，你可以输入”akg“、”aiku“、”aikugui“、”爱“等进行模糊搜素，输入关键词后回车即可快速帮你在数据库中找到结果。


### 优化：

1、将战队logo上传与”上传新数据“功能合并。

2、你将不需要输入战队名称，选择logo时会自动帮你填充战队名。

3、优化了一处逻辑，现在，你在输入过程时、或者输入错误名称时画面不会发生闪烁。（在旧版中，如果角色选择栏输入了错误的角色名称，例如盲女在输入了一半只有盲一个字的情况下，会导致画面丢失并报错。）
当然，你想要正确的刷新直播画面还是需要将错误的名称改正，本优化只优化了”闪烁“问题，并不会帮你自动更正错误。

### 修复：

1、修复了一处全局变量错误。

2、修复了在塔罗模式下，pick”心理学家“会导致程序卡死、画面丢失的异常。

### 已知的问题：

在未知情况下，会有概率出现控制台和直播画面窗口无法被拖动的情况（功能按键未卡死，可以正常使用），这一情况不会存在任何报错，因此我不能将该问题复现，也无法溯源，因此暂时无法将它修复，怀疑是tk库的底层逻辑不好导致交互监听事件异常失效。

解决和避免的方案：直播画面窗口可以通过两次f11切换全屏来刷新窗口、或者关闭直播窗口重启解决该问题。控制台窗口只能整个程序重启来解决，因此请将控制台窗口放在屏幕中心，确保即使不能移动时，你也可以正常操作控制台。

# 历史版本更新记录

## `1.0`

该版本是第一版测试

## `1.1`

1、角色库更新至拉拉队员

2、调整了部分监管者图片位置不正确的问题

3、修改了ban位上锁时的素材透明度，以防止图像不清晰

4、更改ban位材质

## `1.2`

1、角色库更新至“愚人金”

2、修复了一处计时器错误，在旧版中，反复打开新窗口会导致缓存异常造成卡顿

3、修复了一处错误的循环，该bug会导致程序在长时间运行下、或者频繁进行某些操作后导致程序卡顿、奔溃

4、禁用了”赛事名称“，因为在此版本它并没有用

5、新增”FWF常规赛“、”FWF塔罗“两个模式，可以在控制台任意切换

6、新增队徽功能，只需将队徽logo（必须得是png格式）放在指定文件夹即可，图片放在指定文件夹后，请重启程序。

## `1.2.1`

1、新增计时器

## `1.3`

1、修复了一个计时器运行时拖拽窗口卡死的问题

2、优化bpwindow的外观，去除白边和标题栏，以便使用

## `1.4`

1、修复了上一版本去标题栏后个别录屏/直播软件不能正确捕获窗口的问题

2、新增全屏功能，使录屏软件抓到的画面有1k分辨率，现在你可以f11使直播窗口切换全屏，可以用esc快速关闭直播窗口

3、适配了除`1760*990`和`1920*1080`的更多尺寸，你可以在全屏状态下在更多分辨率下运行，不建议在`1920*1080`以上的分辨率全屏，因为素材本身只有1k像素，过度缩放可能会导致模糊

注意：即使在这一版本中做了适配，还是推荐尽量使用分辨率`1920*1080`、缩放比`100％`下使用本程序，以提供最佳视觉体验

## `1.4.1`

1、角色库更新了“木偶师”、“时空之影”

2、允许修改赛事名称



## 项目版权说明

1、默认bp界面背景素材来源于：第五人格2019IVC冬季精英赛淘汰赛

2、”FWF常规赛“、”FWF塔罗“bp界面背景素材版权归属于 FWF娱乐赛

3、界面内所有角色、地图素材来源于《网易第五人格》（网易公司版权所有 ©1997-2023）

  感谢wiki.biligame.com提供了素材

4、本项目使用了以下项目：

  Azure-ttk-theme-2.1.0（作者：rdbende，MIT开源协议）

  项目地址：https://github.com/rdbende/ttk-widget-factory

5、本项目（BP_IdentityV）为免费闭源项目，本项目不会收取任何费用，但是使用时你需要遵循以下协议：

  5.1、本项目允许使用于直播、视频制作，前提是你需要提前告知我或者获得我的许可

  5.2、本项目不允许用于商用，禁止使用它盈利，素材最终解释权归《网易第五人格》所有

  5.3、本项目完全免费，禁止二卖

6、如果你在使用过程中遇到问题，可以提交反馈寻求我的帮助


## 声明

本项目为为免费闭源项目，请遵循项目版权说明中的第四条的使用说明

此项目完全离线运行，不会收集任何用户信息或获取用户输入数据。


## 使用说明

下载本项目后将其解压

双击**第五人格bp系统.exe**打开程序

## 关于作者

`Github`**https://github.com/lvtiansama**

`CSDN`**https://blog.csdn.net/lvtiansama**

`哔哩哔哩`**https://space.bilibili.com/88004482**

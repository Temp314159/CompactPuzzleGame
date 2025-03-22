# -*- coding:utf-8 -*-
# based on python 3.9
# 2025/01/18 13:46
# by d.7.

"""
数学拼图游戏，基于Pygame
玩家需要创建若干骨牌式的拼图块，并将它们拼在一起，目标是使拼图结构能作为一个整体移动而不散开

若解是成功的，将会获得一个分数，分数与拼图结构的优雅程度有关（最大拼图格子数、拼图总格子数、拼图块数、是否存在过于简单的结构）
分数计算方法目前非常不严谨，有待进一步研究，可能需要涉及到更本质的数学
"""

import pygame
import sys
from pygame.locals import *
import random
import os

GAME_NAME = "PolyLok"

# 初始化pygame
pygame.init()

# 初始化pygame音频系统
pygame.mixer.init()

# 获取绝对工作目录（这样打包后也能正常运行）
work_folder = os.path.dirname(os.path.abspath(sys.argv[0]))

# 加载音效
SOUNDS = {
    'put_down': pygame.mixer.Sound(os.path.join(work_folder, 'sounds', 'putDown.wav')),
    'delete': pygame.mixer.Sound(os.path.join(work_folder, 'sounds', 'delete.wav')),
    'pick_up': pygame.mixer.Sound(os.path.join(work_folder, 'sounds', 'pickUp.wav')),
    'click_big': pygame.mixer.Sound(os.path.join(work_folder, 'sounds', 'clickBig.wav')),
    'click_flip': pygame.mixer.Sound(os.path.join(work_folder, 'sounds', 'clickFlip.wav')),
    'success': pygame.mixer.Sound(os.path.join(work_folder, 'sounds', 'success.wav')),
    'fail': pygame.mixer.Sound(os.path.join(work_folder, 'sounds', 'failDrop.mp3'))
}

# 游戏常量
SCREEN_WIDTH = 1600                     # 屏幕宽度
SCREEN_HEIGHT = 900                     # 屏幕高度
BG_COLOR = (240, 240, 240, 255)         # 背景颜色
GRID_COLOR = (200, 200, 200, 255)       # 网格线颜色
SLIDER_COLOR = (100, 100, 100, 255)     # 滑动条滑块颜色
SLIDER_BG_COLOR = (220, 220, 220, 255)  # 滑动条背景颜色
SLIDER_WIDTH = 20                       # 滑动条宽度
SLIDER_HEIGHT = 150                     # 滑动条高度
SLIDER_X = 20                           # 滑动条X坐标
SLIDER_Y = 50                           # 滑动条Y坐标
BUTTON_SIZE = 20                        # 加减按钮大小
BUTTON_COLOR = (150, 150, 150, 255)     # 加减按钮颜色
MIN_GRID_SIZE = 10                      # 最小网格大小
MAX_GRID_SIZE = 100                     # 最大网格大小
DEFAULT_GRID_SIZE = 50                  # 默认网格大小
DEFAULT_GRID_OFFSET_X = 0               # 默认网格X偏移量
DEFAULT_GRID_OFFSET_Y = 0               # 默认网格Y偏移量

# 按钮常量
BUTTON_PADDING = 15                         # 按钮内边距
BUTTON_HEIGHT = 40                          # 按钮高度
UNDO_BUTTON_WIDTH = 120                     # 撤销按钮宽度
RESTART_BUTTON_WIDTH = 150                  # 重新开始按钮宽度
COMPLETE_BUTTON_WIDTH = 180                 # 完成拼图按钮宽度
BUTTON_TEXT_COLOR = (0, 0, 0, 255)          # 按钮文本颜色
BUTTON_BG_COLOR = (180, 180, 180, 255)      # 按钮背景颜色
BUTTON_HOVER_COLOR = (200, 200, 200, 255)   # 按钮悬停颜色
BUTTON_TEXT_SIZE = 24                       # 按钮文字大小
CREATE_BUTTON_WIDTH = 250                   # 创建拼图按钮宽度
CREATE_BUTTON_HEIGHT = 60                   # 创建拼图按钮高度
CREATE_BUTTON_TEXT_SIZE = 28                # 创建拼图按钮文字大小

# 规则说明对话框常量
RULES_BG_COLOR = (245, 245, 245)            # 规则背景颜色
RULES_TEXT_COLOR = (0, 0, 0)                # 规则文本颜色
RULES_TITLE_COLOR = (50, 50, 100)           # 规则标题颜色
RULES_BORDER_COLOR = (100, 100, 100)        # 规则边框颜色
RULES_BUTTON_COLOR = (100, 150, 200)        # 规则按钮颜色
RULES_BUTTON_HOVER_COLOR = (120, 170, 220)  # 规则按钮悬停颜色
RULES_BUTTON_TEXT_COLOR = (255, 255, 255)   # 规则按钮文本颜色
RULES_PADDING = 20                          # 规则内边距
RULES_TITLE_SIZE = 45                       # 规则标题字体大小
RULES_TEXT_SIZE = 30                        # 规则文本字体大小
RULES_BUTTON_WIDTH = 120                    # 规则确定按钮宽度
RULES_BUTTON_HEIGHT = 40                    # 规则确定按钮高度
RULES_SCROLL_SPEED = 20                     # 规则滚动速度
RULES_WIDTH = 500                           # 规则窗口宽度
RULES_HEIGHT = 900                          # 规则窗口高度

# 拼图块常量
CELL_COLORS = [
    # (255, 0, 0, 255),    # 红色（用于标识错误）
    (0, 255, 0, 255),    # 绿色
    (0, 0, 255, 255),    # 蓝色
    (255, 255, 0, 255),  # 黄色
    (255, 0, 255, 255),  # 紫色
    (0, 255, 255, 255)   # 青色
]
CELL_BORDER_COLOR = (0, 0, 0, 255)                  # 拼图块边框颜色
CELL_BORDER_WIDTH = 3                               # 拼图块边框宽度
CELL_SELECTED_BORDER_COLOR = (255, 165, 0, 255)     # 选中拼图块边框颜色
CELL_SELECTED_OVERLAY_COLOR = (255, 255, 255, 130)  # 选中拼图块高亮颜色
CREATE_BUTTON_COLOR = (100, 180, 100, 255)          # 创建拼图按钮颜色
CREATE_BUTTON_HOVER_COLOR = (120, 200, 120, 255)    # 创建拼图按钮悬停颜色
CREATE_BUTTON_TEXT_COLOR = (255, 255, 255, 255)     # 创建拼图按钮文本颜色
DELETE_BUTTON_COLOR = (200, 100, 100, 255)          # 删除拼图按钮颜色
DELETE_BUTTON_HOVER_COLOR = (220, 120, 120, 255)    # 删除拼图按钮悬停颜色

# 提示信息常量
NOTIFICATION_DURATION = 2000                    # 提示显示时间(毫秒)
NOTIFICATION_SUCCESS_COLOR = (0, 200, 0, 180)   # 成功提示颜色(半透明绿色)
NOTIFICATION_ERROR_COLOR = (200, 0, 0, 180)     # 错误提示颜色(半透明红色)
NOTIFICATION_TEXT_COLOR = (255, 255, 255)       # 提示文本颜色
NOTIFICATION_PADDING = 20                       # 提示内边距
NOTIFICATION_FONT_SIZE = 24                     # 提示字体大小

# 默认填色颜色
DEFAULT_CELL_COLOR = (180, 180, 180, 255)  # 灰色

# 显示恰当大小画面按钮
FIT_VIEW_BUTTON_Y_OFFSET = 30   # 与减号按钮的距离
FIT_VIEW_RATIO = 0.6            # 有效画面占窗口的比例

# 左上角UI布局常量
UI_LEFT_MARGIN = 30             # 左边距
UI_TOP_MARGIN = 50              # 上边距
UI_BUTTON_SIZE = 24             # 按钮大小
UI_BUTTON_SPACING = 12          # 按钮间距
UI_SLIDER_WIDTH = 10            # 滑动条宽度
UI_SLIDER_HEIGHT = 150          # 滑动条高度
UI_SLIDER_HANDLE_HEIGHT = 13    # 滑块高度
UI_SLIDER_HANDLE_WIDTH = 22     # 滑块宽度

# 修改原有的常量定义
SLIDER_WIDTH = UI_SLIDER_WIDTH
SLIDER_HEIGHT = UI_SLIDER_HEIGHT
SLIDER_X = UI_LEFT_MARGIN
SLIDER_Y = UI_TOP_MARGIN + UI_BUTTON_SIZE + UI_BUTTON_SPACING
BUTTON_SIZE = UI_BUTTON_SIZE
FIT_VIEW_BUTTON_Y_OFFSET = UI_BUTTON_SPACING * 2  # 与减号按钮的距离

# 创建游戏窗口
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption(GAME_NAME)

# 网格状态
grid_size = DEFAULT_GRID_SIZE           # 当前网格大小
grid_offset_x = DEFAULT_GRID_OFFSET_X   # 当前网格X偏移量
grid_offset_y = DEFAULT_GRID_OFFSET_Y   # 当前网格Y偏移量
dragging = False                        # 是否正在拖动网格
last_mouse_pos = (0, 0)                 # 上一次鼠标位置
slider_dragging = False                 # 是否正在拖动滑块
slider_value = (DEFAULT_GRID_SIZE - MIN_GRID_SIZE) / (MAX_GRID_SIZE - MIN_GRID_SIZE)  # 滑块位置值

# 按钮状态
undo_button_rect = None            # 撤销按钮矩形区域
restart_button_rect = None         # 重新开始按钮矩形区域
complete_button_rect = None        # 完成拼图按钮矩形区域
undo_hover = False                 # 撤销按钮悬停状态
restart_hover = False              # 重新开始按钮悬停状态
complete_hover = False             # 完成拼图按钮悬停状态

# 游戏状态
cells = {}                              # 格子状态 {(x, y): color}
puzzle_pieces = []                      # 拼图块列表 [[(x1, y1), (x2, y2), ...], [...], ...]
available_colors = CELL_COLORS.copy()   # 可用颜色列表
current_color_index = 0                 # 当前使用的颜色索引
game_states = []                        # 游戏状态历史，用于撤销
create_button_rect = None               # 创建拼图块按钮矩形区域
create_button_hover = False             # 创建按钮悬停状态
notification = None                     # 当前显示的提示信息 (text, color, end_time)

# 滑动条状态
slider_hover = False         # 滑块悬停状态
plus_button_hover = False    # 加号按钮悬停状态
minus_button_hover = False   # 减号按钮悬停状态

# 拼图块选择状态
selected_piece_index = None  # 当前选中的拼图块索引
delete_button_rect = None    # 删除拼图块按钮
delete_button_hover = False  # 删除按钮悬停状态

# 添加拼图拖动相关变量
dragging_piece = False        # 是否正在拖动拼图
dragging_piece_offset = None  # 拖动拼图的偏移量（网格单位）

# 添加完整性判定相关变量
DIRECTIONS = [
    (0, -1),  # 上
    (1, 0),   # 右
    (0, 1),   # 下
    (-1, 0)   # 左
]
DIRECTION_NAMES = ['上', '右', '下', '左']

"""
重要注意事项：
1. 在处理UI元素点击时，必须在处理完成后使用continue语句跳过后续的填色逻辑，
   否则会导致点击UI元素时意外地给背后的网格上色。
2. 检查UI元素点击时，应使用元素的实际位置和尺寸进行判断，而不是使用固定的常量，
   这样在调整UI布局时不会出现判断错误。
3. 所有UI元素的点击处理应该在填色逻辑之前完成，并设置click_handled标志。
"""

# 添加快捷键映射字典
KEYBOARD_SHORTCUTS = {
    'undo': pygame.K_z,           # Z键 - 撤销
    'restart': pygame.K_r,        # R键 - 重新开始
    'create': pygame.K_SPACE,     # 空格键 - 创建拼图
    'create2': pygame.K_RETURN,  # 回车键 - 创建拼图（快捷键2）
    'delete': pygame.K_DELETE,    # Delete键 - 删除拼图
    'complete': pygame.K_c,       # C键 - 完成拼图
    'zoom_in': pygame.K_EQUALS,     # =键 - 放大
    'zoom_out': pygame.K_MINUS,   # -键 - 缩小
    'fit_view': pygame.K_o,       # O键 - 适应视图
}

# 添加判定状态变量
is_judging = False  # 是否正在进行判定
ui_alpha = 255      # UI透明度

# 添加判定结果相关常量
RESULT_OVERLAY_COLOR = (255, 255, 255, 200)  # 结果显示时的蒙版颜色
RESULT_SUCCESS_COLOR = (50, 200, 50)         # 成功文字颜色
RESULT_FAILURE_COLOR = (200, 50, 50)         # 失败文字颜色
RESULT_TITLE_SIZE = 72                       # 结果标题文字大小
RESULT_TEXT_SIZE = 24                        # 结果说明文字大小
RESULT_BUTTON_WIDTH = 200                    # 结果按钮宽度
RESULT_BUTTON_HEIGHT = 50                    # 结果按钮高度
RESULT_BUTTON_COLOR = (100, 100, 200)        # 结果按钮颜色
RESULT_BUTTON_HOVER_COLOR = (120, 120, 220)  # 结果按钮悬停颜色
RESULT_BUTTON_TEXT_COLOR = (255, 255, 255)   # 结果按钮文字颜色
RESULT_BUTTON_TEXT_SIZE = 28                 # 结果按钮文字大小

# 添加判定结果相关变量
check_result = None  # 判定结果：None=未判定，True=成功，False=失败
failure_reason = ""  # 失败原因
result_button_rect = None  # 结果按钮区域
result_button_hover = False  # 结果按钮悬停状态

# 添加音效播放状态变量
success_sound_played = False  # 是否已经播放过成功音效

# 添加失败音效播放状态变量
fail_sound_played = False  # 是否已经播放过失败音效

# 绘制网格函数
def draw_grid():
    # 计算网格起始位置（考虑偏移量）
    start_x = int(grid_offset_x % grid_size)
    start_y = int(grid_offset_y % grid_size)
    
    # 绘制垂直线
    for x in range(start_x, int(SCREEN_WIDTH), int(grid_size)):
        pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_HEIGHT))
    
    # 绘制水平线
    for y in range(start_y, int(SCREEN_HEIGHT), int(grid_size)):
        pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

# 绘制缩放滑动条
def draw_slider():
    if is_judging:
        return  # 判定时不绘制滑动条
    global slider_hover, plus_button_hover, minus_button_hover, fit_view_button_hover
    
    # 获取鼠标位置
    mouse_pos = pygame.mouse.get_pos()
    
    # 计算UI元素的中心X坐标
    ui_center_x = UI_LEFT_MARGIN + UI_BUTTON_SIZE // 2
    
    # 绘制滑动条背景
    slider_bg_rect = pygame.Rect(
        ui_center_x - UI_SLIDER_WIDTH // 2, 
        SLIDER_Y, 
        UI_SLIDER_WIDTH, 
        UI_SLIDER_HEIGHT
    )
    pygame.draw.rect(screen, SLIDER_BG_COLOR, slider_bg_rect)
    
    # 计算滑块位置
    slider_pos = SLIDER_Y + int((1 - slider_value) * UI_SLIDER_HEIGHT)
    
    # 检查鼠标是否悬停在滑块上
    slider_rect = pygame.Rect(
        ui_center_x - UI_SLIDER_HANDLE_WIDTH // 2, 
        slider_pos - UI_SLIDER_HANDLE_HEIGHT // 2, 
        UI_SLIDER_HANDLE_WIDTH, 
        UI_SLIDER_HANDLE_HEIGHT
    )
    slider_hover = slider_rect.collidepoint(mouse_pos)
    
    # 绘制滑块
    slider_color = BUTTON_HOVER_COLOR if slider_hover else SLIDER_COLOR
    pygame.draw.rect(screen, slider_color, slider_rect)
    
    # 绘制加号按钮
    plus_button_rect = pygame.Rect(
        ui_center_x - UI_BUTTON_SIZE // 2, 
        UI_TOP_MARGIN, 
        UI_BUTTON_SIZE, 
        UI_BUTTON_SIZE
    )
    plus_button_hover = plus_button_rect.collidepoint(mouse_pos)
    plus_button_color = BUTTON_HOVER_COLOR if plus_button_hover else BUTTON_COLOR
    
    pygame.draw.rect(screen, plus_button_color, plus_button_rect)
    pygame.draw.line(screen, (0, 0, 0), 
                    (plus_button_rect.left + 4, plus_button_rect.centery), 
                    (plus_button_rect.right - 4, plus_button_rect.centery), 2)
    pygame.draw.line(screen, (0, 0, 0), 
                    (plus_button_rect.centerx, plus_button_rect.top + 4), 
                    (plus_button_rect.centerx, plus_button_rect.bottom - 4), 2)
    
    # 绘制减号按钮
    minus_button_rect = pygame.Rect(
        ui_center_x - UI_BUTTON_SIZE // 2, 
        SLIDER_Y + UI_SLIDER_HEIGHT + UI_BUTTON_SPACING, 
        UI_BUTTON_SIZE, 
        UI_BUTTON_SIZE
    )
    minus_button_hover = minus_button_rect.collidepoint(mouse_pos)
    minus_button_color = BUTTON_HOVER_COLOR if minus_button_hover else BUTTON_COLOR
    
    pygame.draw.rect(screen, minus_button_color, minus_button_rect)
    pygame.draw.line(screen, (0, 0, 0), 
                    (minus_button_rect.left + 4, minus_button_rect.centery), 
                    (minus_button_rect.right - 4, minus_button_rect.centery), 2)
    
    # 绘制显示恰当大小画面按钮
    fit_view_button_rect = pygame.Rect(
        ui_center_x - UI_BUTTON_SIZE // 2, 
        minus_button_rect.bottom + FIT_VIEW_BUTTON_Y_OFFSET, 
        UI_BUTTON_SIZE, 
        UI_BUTTON_SIZE
    )
    fit_view_button_hover = fit_view_button_rect.collidepoint(mouse_pos)
    fit_view_button_color = BUTTON_HOVER_COLOR if fit_view_button_hover else BUTTON_COLOR
    
    pygame.draw.rect(screen, fit_view_button_color, fit_view_button_rect)
    
    # 绘制圆形和中心点
    circle_radius = UI_BUTTON_SIZE // 2 - 4
    circle_center = (fit_view_button_rect.centerx, fit_view_button_rect.centery)
    pygame.draw.circle(screen, (0, 0, 0), circle_center, circle_radius, 2)
    pygame.draw.circle(screen, (0, 0, 0), circle_center, 2)

# 绘制按钮函数
def draw_buttons():
    if is_judging:
        return  # 判定时不绘制按钮
    global undo_button_rect, restart_button_rect, complete_button_rect
    global undo_hover, restart_hover, complete_hover
    
    # 获取鼠标位置
    mouse_pos = pygame.mouse.get_pos()
    
    # 右上角的撤销按钮
    undo_button_rect = pygame.Rect(
        SCREEN_WIDTH - UNDO_BUTTON_WIDTH - BUTTON_PADDING - RESTART_BUTTON_WIDTH - BUTTON_PADDING,
        BUTTON_PADDING,
        UNDO_BUTTON_WIDTH,
        BUTTON_HEIGHT
    )
    undo_hover = undo_button_rect.collidepoint(mouse_pos)
    undo_color = BUTTON_HOVER_COLOR if undo_hover else BUTTON_BG_COLOR
    
    # 右上角的重新开始按钮
    restart_button_rect = pygame.Rect(
        SCREEN_WIDTH - RESTART_BUTTON_WIDTH - BUTTON_PADDING,
        BUTTON_PADDING,
        RESTART_BUTTON_WIDTH,
        BUTTON_HEIGHT
    )
    restart_hover = restart_button_rect.collidepoint(mouse_pos)
    restart_color = BUTTON_HOVER_COLOR if restart_hover else BUTTON_BG_COLOR
    
    # 右下角的完成拼图按钮
    complete_button_rect = pygame.Rect(
        SCREEN_WIDTH - COMPLETE_BUTTON_WIDTH - BUTTON_PADDING,
        SCREEN_HEIGHT - BUTTON_HEIGHT - BUTTON_PADDING,
        COMPLETE_BUTTON_WIDTH,
        BUTTON_HEIGHT
    )
    complete_hover = complete_button_rect.collidepoint(mouse_pos)
    complete_color = BUTTON_HOVER_COLOR if complete_hover else BUTTON_BG_COLOR
    
    # 绘制按钮
    pygame.draw.rect(screen, undo_color, undo_button_rect)
    pygame.draw.rect(screen, restart_color, restart_button_rect)
    pygame.draw.rect(screen, complete_color, complete_button_rect)
    
    # 绘制按钮文本
    font = pygame.font.SysFont(None, BUTTON_TEXT_SIZE)
    
    undo_text = font.render("Undo", True, BUTTON_TEXT_COLOR)
    undo_text_rect = undo_text.get_rect(center=undo_button_rect.center)
    screen.blit(undo_text, undo_text_rect)
    
    restart_text = font.render("Restart", True, BUTTON_TEXT_COLOR)
    restart_text_rect = restart_text.get_rect(center=restart_button_rect.center)
    screen.blit(restart_text, restart_text_rect)
    
    complete_text = font.render("Complete", True, BUTTON_TEXT_COLOR)
    complete_text_rect = complete_text.get_rect(center=complete_button_rect.center)
    screen.blit(complete_text, complete_text_rect)

# 规则说明对话框
def show_rules():
    # 规则内容 - 可以根据需要修改
    title = "Game Rules"
    
    # 规则文本和图片内容 - 每个元素是一个段落或图片
    # 格式: ('text', 文本内容) 或 ('image', 图片路径, 显示位置)
    contents = [
        ('text', "Welcome to "+GAME_NAME+"!"),
        
        ('image', os.path.join(work_folder, 'pictures', 'rules_cover.png'), "center"),
        
        ('text', "BASIC CONTROLS:"),
        ('text', "• Left click / hold & drag to select grid cells."),
        ('text', "• Right click / hold & drag to deselect cells."),
        ('text', "• Press 'Create' to create a polyomino piece."),  # \nfrom selected cells
        ('text', "• Left hold & drag to move a piece."),
        ('text', "• Press 'Delete' to remove a piece."),
        ('text', "• Press 'Complete' to finish."),

        ('text', ""),

        ('text', "GAME OBJECTIVE:"),
        ('text', "Ensure final structure maintains cohesion \nduring movement. \n(i.e. relative positions of all pieces \nremain unchanged.)"),

        ('text', ""),
        
        ('text', "Have fun!"),
    ]
    
    # 创建规则窗口表面
    rules_surface = pygame.Surface((RULES_WIDTH, RULES_HEIGHT))
    
    # 初始化滚动位置
    scroll_y = 0
    max_scroll = 0  # 将在渲染时计算
    
    # 创建确定按钮
    button_rect = pygame.Rect(
        RULES_WIDTH // 2 - RULES_BUTTON_WIDTH // 2,
        RULES_HEIGHT - RULES_PADDING - RULES_BUTTON_HEIGHT,
        RULES_BUTTON_WIDTH,
        RULES_BUTTON_HEIGHT
    )
    button_hover = False
    
    # 创建字体
    title_font = pygame.font.SysFont(None, RULES_TITLE_SIZE)
    text_font = pygame.font.SysFont(None, RULES_TEXT_SIZE)
    
    # 渲染标题
    title_surface = title_font.render(title, True, RULES_TITLE_COLOR)
    title_rect = title_surface.get_rect(centerx=RULES_WIDTH // 2, top=RULES_PADDING)
    
    # 渲染内容
    content_items = []
    for item in contents:
        if item[0] == 'text':
            # 处理文本段落
            lines = item[1].split('\n')
            for line in lines:
                text_surface = text_font.render(line, True, RULES_TEXT_COLOR)
                content_items.append(('text', text_surface))
        elif item[0] == 'image':
            # 处理图片
            try:
                img_path, position = item[1], item[2]
                img = pygame.image.load(img_path)
                # 调整图片大小，确保不超过对话框宽度的80%
                max_width = int(RULES_WIDTH * 0.8) - 2 * RULES_PADDING
                if img.get_width() > max_width:
                    ratio = max_width / img.get_width()
                    new_size = (max_width, int(img.get_height() * ratio))
                    img = pygame.transform.scale(img, new_size)
                content_items.append(('image', img, position))
            except pygame.error:
                print(f"Warning: Could not load image {img_path}")
    
    # 计算规则窗口在屏幕上的位置（居中）
    rules_x = (SCREEN_WIDTH - RULES_WIDTH) // 2
    rules_y = (SCREEN_HEIGHT - RULES_HEIGHT) // 2
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            
            elif event.type == MOUSEBUTTONDOWN:
                # 调整鼠标位置到规则窗口坐标系
                local_pos = (event.pos[0] - rules_x, event.pos[1] - rules_y)
                
                if event.button == 1:  # 左键
                    # 检查是否点击了确定按钮
                    if button_rect.collidepoint(local_pos):
                        running = False
                
                elif event.button == 4:  # 滚轮上滚
                    scroll_y = min(0, scroll_y + RULES_SCROLL_SPEED)
                
                elif event.button == 5:  # 滚轮下滚
                    scroll_y = max(min(0, -max_scroll + RULES_HEIGHT - 2 * RULES_PADDING - RULES_BUTTON_HEIGHT - 20), 
                                  scroll_y - RULES_SCROLL_SPEED)
            
            elif event.type == MOUSEMOTION:
                # 调整鼠标位置到规则窗口坐标系
                local_pos = (event.pos[0] - rules_x, event.pos[1] - rules_y)
                # 检查鼠标是否悬停在确定按钮上
                button_hover = button_rect.collidepoint(local_pos)
        
        # 绘制游戏背景
        screen.fill(BG_COLOR)
        
        # 绘制规则窗口背景
        rules_surface.fill(RULES_BG_COLOR)
        
        # 绘制标题
        rules_surface.blit(title_surface, title_rect)
        
        # 计算内容区域
        content_rect = pygame.Rect(
            RULES_PADDING,
            title_rect.bottom + RULES_PADDING,
            RULES_WIDTH - 2 * RULES_PADDING,
            RULES_HEIGHT - title_rect.bottom - 3 * RULES_PADDING - RULES_BUTTON_HEIGHT
        )
        
        # 创建内容表面
        content_surface = pygame.Surface((content_rect.width, 5000))  # 足够大的高度
        content_surface.fill(RULES_BG_COLOR)
        
        # 在内容表面上绘制内容项
        y_pos = 0
        for item in content_items:
            if item[0] == 'text':
                text_surface = item[1]
                content_surface.blit(text_surface, (0, y_pos))
                y_pos += text_surface.get_height() + 10
            elif item[0] == 'image':
                img, position = item[1], item[2]
                if position == "left":
                    x = 0
                elif position == "right":
                    x = content_rect.width - img.get_width()
                else:  # center
                    x = (content_rect.width - img.get_width()) // 2
                
                content_surface.blit(img, (x, y_pos))
                y_pos += img.get_height() + 20
        
        # 更新最大滚动值
        max_scroll = y_pos
        
        # 在规则窗口上绘制可见的内容部分
        visible_content = content_surface.subsurface(
            pygame.Rect(0, -scroll_y, content_rect.width, min(content_rect.height, max_scroll))
        )
        rules_surface.blit(visible_content, content_rect)
        
        # 绘制边框
        pygame.draw.rect(rules_surface, RULES_BORDER_COLOR, 
                         pygame.Rect(0, 0, RULES_WIDTH, RULES_HEIGHT), 2)
        
        # 绘制确定按钮
        button_color = RULES_BUTTON_HOVER_COLOR if button_hover else RULES_BUTTON_COLOR
        pygame.draw.rect(rules_surface, button_color, button_rect)
        pygame.draw.rect(rules_surface, RULES_BORDER_COLOR, button_rect, 2)
        
        # 绘制按钮文本
        button_text = text_font.render("OK", True, RULES_BUTTON_TEXT_COLOR)
        button_text_rect = button_text.get_rect(center=button_rect.center)
        rules_surface.blit(button_text, button_text_rect)
        
        # 将规则窗口绘制到屏幕上
        screen.blit(rules_surface, (rules_x, rules_y))
        
        pygame.display.flip()
    
    return

# 获取网格坐标
def get_grid_pos(mouse_pos):
    x = int((mouse_pos[0] - grid_offset_x) // grid_size)
    y = int((mouse_pos[1] - grid_offset_y) // grid_size)
    return (x, y)

# 检查位置是否在已有拼图块中
def is_in_puzzle_piece(pos):
    for piece in puzzle_pieces:
        if pos in piece['cells']:
            return True
    return False

# 检查连通性
def check_connectivity(cells_list):
    if not cells_list:
        return False
    
    # 使用BFS检查连通性
    visited = set()
    queue = [cells_list[0]]
    
    while queue:
        current = queue.pop(0)
        if current in visited:
            continue
        
        visited.add(current)
        
        # 检查四个方向的相邻格子
        neighbors = [
            (current[0] + 1, current[1]),
            (current[0] - 1, current[1]),
            (current[0], current[1] + 1),
            (current[0], current[1] - 1)
        ]
        
        for neighbor in neighbors:
            if neighbor in cells_list and neighbor not in visited:
                queue.append(neighbor)
    
    # 如果所有格子都被访问到，则连通
    return len(visited) == len(cells_list)

# 保存当前游戏状态
def save_game_state():
    global game_states
    # 创建当前状态的深拷贝
    state = {
        'cells': cells.copy(),
        'puzzle_pieces': [piece.copy() for piece in puzzle_pieces],
        'available_colors': available_colors.copy(),
        'current_color_index': current_color_index
    }
    game_states.append(state)
    # 限制历史记录数量，防止内存占用过大
    if len(game_states) > 50:
        game_states.pop(0)

# 撤销到上一个状态
def undo():
    global cells, puzzle_pieces, available_colors, current_color_index, game_states
    
    if len(game_states) > 0:
        # 恢复到上一个状态
        state = game_states.pop()
        cells = state['cells']
        puzzle_pieces = state['puzzle_pieces']
        available_colors = state['available_colors']
        current_color_index = state['current_color_index']
        # 播放点击音效
        SOUNDS['click_flip'].play()
        return True
    return False

# 重置游戏
def restart_game():
    global cells, puzzle_pieces, available_colors, current_color_index, game_states
    global grid_size, grid_offset_x, grid_offset_y, slider_value
    global success_sound_played, fail_sound_played  # 添加fail_sound_played
    
    # 重置音效状态
    success_sound_played = False
    fail_sound_played = False
    
    # 重置游戏状态
    cells = {}
    puzzle_pieces = []
    available_colors = CELL_COLORS.copy()
    current_color_index = 0
    game_states = []
    
    # 重置网格状态
    grid_size = DEFAULT_GRID_SIZE
    grid_offset_x = DEFAULT_GRID_OFFSET_X
    grid_offset_y = DEFAULT_GRID_OFFSET_Y
    slider_value = (DEFAULT_GRID_SIZE - MIN_GRID_SIZE) / (MAX_GRID_SIZE - MIN_GRID_SIZE)
    
    save_game_state()  # 保存初始状态
    # 播放点击音效
    SOUNDS['click_flip'].play()

# 显示提示信息
def show_notification(text, color=NOTIFICATION_SUCCESS_COLOR):
    global notification
    
    end_time = pygame.time.get_ticks() + NOTIFICATION_DURATION
    notification = (text, color, end_time)

# 创建拼图块
def create_puzzle_piece():
    global cells, puzzle_pieces, available_colors, current_color_index
    
    # 获取所有未在拼图块中的填色格子
    colored_cells = [pos for pos in cells.keys() if not is_in_puzzle_piece(pos)]
    
    if not colored_cells:
        show_notification("No cells to create puzzle piece", NOTIFICATION_ERROR_COLOR)
        return False
    
    # 检查连通性
    if not check_connectivity(colored_cells):
        show_notification("Cells are not connected", NOTIFICATION_ERROR_COLOR)
        return False
    
    # 保存当前状态
    save_game_state()
    
    # 如果颜色用尽，重置颜色列表
    if not available_colors:
        available_colors = CELL_COLORS.copy()
    
    # 随机选择一个颜色
    piece_color = random.choice(available_colors)
    available_colors.remove(piece_color)
    
    # 创建新的拼图块，包含颜色信息
    new_piece = {'cells': colored_cells, 'color': piece_color}
    puzzle_pieces.append(new_piece)
    
    # 从cells中删除这些格子
    for pos in colored_cells:
        if pos in cells:
            del cells[pos]
    
    # 创建成功时播放音效
    SOUNDS['put_down'].play()
    show_notification("Puzzle piece created successfully", NOTIFICATION_SUCCESS_COLOR)
    return True

# 绘制格子们
def draw_cells(cells_dict):
    # 绘制填色的格子
    for pos, color in cells_dict.items():
        grid_x = int(pos[0] * grid_size + grid_offset_x)
        grid_y = int(pos[1] * grid_size + grid_offset_y)
        
        # 检查格子是否在屏幕内
        if (-grid_size <= grid_x < SCREEN_WIDTH and -grid_size <= grid_y < SCREEN_HEIGHT and
            grid_x + grid_size > 0 and grid_y + grid_size > 0):
            # 使用带透明度的颜色绘制
            pygame.draw.rect(screen, color[:3], (grid_x, grid_y, grid_size, grid_size))

# 绘制单个拼图块
def draw_single_piece(piece_dict, cell_color=None, border_color=None):
    # 处理空参数
    if cell_color is None:
        if 'color' in piece_dict:
            cell_color = piece_dict['color']
        else:
            cell_color = DEFAULT_CELL_COLOR
    if border_color is None:
        border_color = CELL_BORDER_COLOR

    # 绘制拼图块的格子
    for pos in piece_dict['cells']:
        grid_x = int(pos[0] * grid_size + grid_offset_x)
        grid_y = int(pos[1] * grid_size + grid_offset_y)
        
        # 检查格子是否在屏幕内
        if (-grid_size <= grid_x < SCREEN_WIDTH and -grid_size <= grid_y < SCREEN_HEIGHT and
            grid_x + grid_size > 0 and grid_y + grid_size > 0):
            # 检查是否有透明度
            if cell_color[3] == 255:
                # 完全不透明，直接绘制
                pygame.draw.rect(screen, cell_color[:3], (grid_x, grid_y, grid_size, grid_size))
            else:
                # 有透明度，使用半透明表面
                highlight_surface = pygame.Surface((grid_size, grid_size), pygame.SRCALPHA)
                # 直接填充颜色（带透明度）（也可以用pygame.draw.rect指定范围绘制，但是没有必要）
                highlight_surface.fill(cell_color)
                # 绘制到屏幕上（屏幕直接绘制不支持透明度）
                screen.blit(highlight_surface, (grid_x, grid_y))
    
    # 绘制拼图块的边框（也可以考虑半透明，但是没有必要，以后再说吧）
    draw_piece_border(piece_dict['cells'], border_color)

# 绘制拼图块们
def draw_pieces(pieces_list):
    # 先绘制所有非选中拼图块
    for i, piece in enumerate(pieces_list):
        if i != selected_piece_index:
            draw_single_piece(piece, cell_color=piece['color'], border_color=CELL_BORDER_COLOR)

# 绘制格子和拼图块
def draw_all_cells():
    # 绘制填色的格子
    draw_cells(cells)
    
    # 绘制拼图块
    draw_pieces(puzzle_pieces)
    
    # 最后绘制选中拼图块，确保它在最上层
    if selected_piece_index is not None:
        piece = puzzle_pieces[selected_piece_index]
        # 绘制选中拼图块
        draw_single_piece(piece, cell_color=piece['color'], border_color=CELL_SELECTED_BORDER_COLOR)
        # 绘制选中拼图块的半透明覆盖
        draw_single_piece(piece, cell_color=CELL_SELECTED_OVERLAY_COLOR, border_color=CELL_SELECTED_BORDER_COLOR)
        

# 添加绘制拼图块边框的辅助函数
def draw_piece_border(piece, border_color):
    # 找出拼图块的边缘
    edges = set()
    for pos in piece:
        x, y = pos
        
        # 检查四个方向，如果相邻位置不在拼图块中，则这条边是边缘
        neighbors = [
            ((x+1, y), (1, 0), (1, 1)),  # 右边
            ((x-1, y), (0, 0), (0, 1)),  # 左边
            ((x, y+1), (0, 1), (1, 1)),  # 下边
            ((x, y-1), (0, 0), (1, 0))   # 上边
        ]
        
        for neighbor, start_offset, end_offset in neighbors:
            if neighbor not in piece:
                # 计算边的起点和终点
                start_x = int((x + start_offset[0]) * grid_size + grid_offset_x)
                start_y = int((y + start_offset[1]) * grid_size + grid_offset_y)
                end_x = int((x + end_offset[0]) * grid_size + grid_offset_x)
                end_y = int((y + end_offset[1]) * grid_size + grid_offset_y)
                
                # 添加到边缘列表
                edges.add((start_x, start_y, end_x, end_y))
    
    # 绘制所有边缘
    for start_x, start_y, end_x, end_y in edges:
        pygame.draw.line(screen, border_color[:3], (start_x, start_y), (end_x, end_y), CELL_BORDER_WIDTH)

# 绘制创建拼图块按钮
def draw_create_button():
    if is_judging:
        return False  # 判定时不绘制创建按钮
    global create_button_rect, create_button_hover
    
    # 如果已经选中了拼图块，不显示创建按钮
    if selected_piece_index is not None:
        create_button_rect = None
        return False
    
    # 检查是否有可以创建拼图块的格子
    has_colored_cells = any(not is_in_puzzle_piece(pos) for pos in cells.keys())
    
    if has_colored_cells:
        # 获取鼠标位置
        mouse_pos = pygame.mouse.get_pos()
        
        # 创建按钮
        create_button_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - CREATE_BUTTON_WIDTH // 2,
            SCREEN_HEIGHT - CREATE_BUTTON_HEIGHT - BUTTON_PADDING,
            CREATE_BUTTON_WIDTH,
            CREATE_BUTTON_HEIGHT
        )
        
        create_button_hover = create_button_rect.collidepoint(mouse_pos)
        button_color = CREATE_BUTTON_HOVER_COLOR if create_button_hover else CREATE_BUTTON_COLOR
        
        # 绘制按钮
        pygame.draw.rect(screen, button_color[:3], create_button_rect)
        pygame.draw.rect(screen, CELL_BORDER_COLOR[:3], create_button_rect, 2)
        
        # 绘制按钮文本
        font = pygame.font.SysFont(None, 28)
        text = font.render("Create Puzzle Piece", True, CREATE_BUTTON_TEXT_COLOR[:3])
        text_rect = text.get_rect(center=create_button_rect.center)
        screen.blit(text, text_rect)
        
        return True
    else:
        create_button_rect = None
        return False

# 绘制提示信息
def draw_notification():
    if notification:
        text, color, end_time = notification
        
        # 检查提示是否过期
        if pygame.time.get_ticks() > end_time:
            return None
        
        # 创建半透明表面
        font = pygame.font.SysFont(None, NOTIFICATION_FONT_SIZE)
        text_surface = font.render(text, True, NOTIFICATION_TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        # 创建背景矩形
        bg_rect = text_rect.inflate(NOTIFICATION_PADDING * 2, NOTIFICATION_PADDING)
        
        # 创建半透明表面
        notification_surface = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(notification_surface, color, (0, 0, bg_rect.width, bg_rect.height))
        
        # 绘制提示
        screen.blit(notification_surface, bg_rect)
        screen.blit(text_surface, text_rect)

# 添加删除拼图块函数
def delete_selected_piece():
    global selected_piece_index, puzzle_pieces
    
    if selected_piece_index is not None:
        # 保存当前状态
        save_game_state()
        
        # 删除选中的拼图块
        del puzzle_pieces[selected_piece_index]
        
        # 清除选择
        selected_piece_index = None
        
        # 删除成功时播放音效
        SOUNDS['delete'].play()
        show_notification("Puzzle piece deleted", NOTIFICATION_SUCCESS_COLOR)
        return True
    return False

# 添加绘制删除按钮函数
def draw_delete_button():
    if is_judging:
        return False  # 判定时不绘制删除按钮
    global delete_button_rect, delete_button_hover
    
    if selected_piece_index is not None:
        # 获取鼠标位置
        mouse_pos = pygame.mouse.get_pos()
        
        # 创建按钮
        delete_button_rect = pygame.Rect(
            SCREEN_WIDTH // 2 - CREATE_BUTTON_WIDTH // 2,
            SCREEN_HEIGHT - CREATE_BUTTON_HEIGHT - BUTTON_PADDING,
            CREATE_BUTTON_WIDTH,
            CREATE_BUTTON_HEIGHT
        )
        
        delete_button_hover = delete_button_rect.collidepoint(mouse_pos)
        button_color = DELETE_BUTTON_HOVER_COLOR if delete_button_hover else DELETE_BUTTON_COLOR
        
        # 绘制按钮
        pygame.draw.rect(screen, button_color[:3], delete_button_rect)
        pygame.draw.rect(screen, CELL_BORDER_COLOR[:3], delete_button_rect, 2)
        
        # 绘制按钮文本
        font = pygame.font.SysFont(None, 28)
        text = font.render("Delete Puzzle Piece", True, CREATE_BUTTON_TEXT_COLOR[:3])
        text_rect = text.get_rect(center=delete_button_rect.center)
        screen.blit(text, text_rect)
        
        return True
    else:
        delete_button_rect = None
        return False

# 检查点击位置是否在拼图块上
def get_piece_at_pos(pos):
    cell_pos = get_grid_pos(pos)
    
    for i, piece in enumerate(puzzle_pieces):
        if cell_pos in piece['cells']:
            return i
    
    return None

# 添加显示恰当大小画面函数
def fit_view_to_content():
    global grid_size, grid_offset_x, grid_offset_y, slider_value
    
    # 获取所有有色格子（包括拼图中的格子）
    all_cells = []
    
    # 添加未成为拼图的格子
    for pos in cells.keys():
        all_cells.append(pos)
    
    # 添加拼图中的格子
    for piece in puzzle_pieces:
        for pos in piece['cells']:
            all_cells.append(pos)
    
    # 如果没有格子，不做任何调整
    if not all_cells:
        return
    
    # 计算有效画面范围
    min_x = min(pos[0] for pos in all_cells)
    max_x = max(pos[0] for pos in all_cells)
    min_y = min(pos[1] for pos in all_cells)
    max_y = max(pos[1] for pos in all_cells)
    
    # 计算中心点（考虑格子的中心）
    center_x = (min_x + max_x) / 2 + 0.5
    center_y = (min_y + max_y) / 2 + 0.5
    
    # 计算内容宽度和高度（格子数）
    content_width = max_x - min_x + 1
    content_height = max_y - min_y + 1
    
    # 计算合适的网格大小
    # 考虑窗口宽高比和内容宽高比，选择较小的缩放比例
    width_scale = (SCREEN_WIDTH * FIT_VIEW_RATIO) / content_width
    height_scale = (SCREEN_HEIGHT * FIT_VIEW_RATIO) / content_height
    new_grid_size = min(width_scale, height_scale)
    
    # 限制网格大小在允许范围内
    new_grid_size = max(MIN_GRID_SIZE, min(new_grid_size, MAX_GRID_SIZE))
    
    # 更新网格大小
    grid_size = int(new_grid_size)
    slider_value = (grid_size - MIN_GRID_SIZE) / (MAX_GRID_SIZE - MIN_GRID_SIZE)
    
    # 调整偏移量，使内容中心位于屏幕中心
    grid_offset_x = SCREEN_WIDTH / 2 - center_x * grid_size
    grid_offset_y = SCREEN_HEIGHT / 2 - center_y * grid_size

# 检查拼图块是否可以放置在指定位置
def can_place_piece_at(piece_index, offset_x, offset_y):
    if piece_index is None:
        return False
    
    piece = puzzle_pieces[piece_index]
    
    # 计算新位置
    new_positions = []
    for pos in piece['cells']:
        new_pos = (pos[0] + offset_x, pos[1] + offset_y)
        new_positions.append(new_pos)
    
    # 检查是否与其他拼图块或填色格子重叠
    for i, other_piece in enumerate(puzzle_pieces):
        if i == piece_index:  # 跳过自身
            continue
        
        for new_pos in new_positions:
            if new_pos in other_piece['cells']:
                return False  # 与其他拼图块重叠
    
    # 检查是否与填色格子重叠
    for new_pos in new_positions:
        if new_pos in cells:
            return False  # 与填色格子重叠
    
    return True

# 检查拼图结构的完整性
def check_puzzle_integrity():
    global check_result, failure_reason
    
    if not puzzle_pieces:
        check_result = False
        failure_reason = "No puzzle pieces to check"
        return False
    
    # 对每个方向进行检查
    for direction_index, (dx, dy) in enumerate(DIRECTIONS):
        # 使用队列进行广度优先搜索
        from collections import deque
        queue = deque([0])  # 从第一块拼图开始
        visited = {0}  # 记录已访问的拼图
        
        # 广度优先搜索
        while queue:
            current_piece_index = queue.popleft()
            current_piece = puzzle_pieces[current_piece_index]
            
            # 检查当前拼图块的每个格子
            for cell in current_piece['cells']:
                # 计算相邻格子的位置
                neighbor_cell = (cell[0] + dx, cell[1] + dy)
                
                # 检查这个位置是否属于其他未访问的拼图块
                for i, piece in enumerate(puzzle_pieces):
                    if i not in visited and neighbor_cell in piece['cells']:
                        queue.append(i)
                        visited.add(i)
        
        # 如果有拼图块未被访问到，说明结构在这个方向上不完整
        if len(visited) < len(puzzle_pieces):
            direction_text = ['upward', 'rightward', 'downward', 'leftward'][direction_index]
            check_result = False
            failure_reason = f"Structure breaks when moving {direction_text}"
            return False
    
    # 所有方向都通过检查
    check_result = True
    return True

# 完成拼图
def complete_puzzle():
    global selected_piece_index, is_judging, ui_alpha, cells
    
    # 播放点击音效
    SOUNDS['click_big'].play()
    
    # 清除选择状态
    selected_piece_index = None
    
    # 清除所有未形成拼图的格子
    if cells:
        save_game_state()  # 保存当前状态以便撤销
        cells = {}  # 清空所有格子
    
    # 如果没有拼图块，直接返回
    if not puzzle_pieces:
        show_notification("No puzzle pieces to check", NOTIFICATION_ERROR_COLOR)
        return
    
    # 进入判定状态
    is_judging = True
    ui_alpha = 255
    
    # 调整视图以显示所有内容
    fit_view_to_content()
    
    # 检查拼图结构的完整性
    check_puzzle_integrity()

# 检查是否有被完全包围的区域
def has_enclosed_area():
    # 检查每一块拼图
    for piece_index, piece in enumerate(puzzle_pieces):
        # 收集这块拼图占据的格子
        piece_cells = set(piece['cells'])
        
        # 找出这块拼图的边界范围
        min_x = min(x for x, y in piece_cells)
        max_x = max(x for x, y in piece_cells)
        min_y = min(y for x, y in piece_cells)
        max_y = max(y for x, y in piece_cells)
        
        # 检查边界内的每个空格子
        for x in range(min_x, max_x + 1):
            for y in range(min_y, max_y + 1):
                if (x, y) not in piece_cells:  # 如果是空格子
                    # 检查这个空格子的四个相邻位置是否都被当前拼图块占据
                    neighbors = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                    if all(neighbor in piece_cells for neighbor in neighbors):
                        return True
    return False

# 修改计算分数函数
def calculate_score():
    # 如果只有一块拼图，分数为0
    if len(puzzle_pieces) == 1:
        return 0
    
    # 检查是否有被完全包围的区域
    if has_enclosed_area():
        return 50
    
    # 计算所需的数据
    total_pieces = len(puzzle_pieces)
    
    # 计算最大块的格子数和总格子数
    max_piece_grids = 0
    total_grids = 0
    for piece in puzzle_pieces:
        piece_size = len(piece['cells'])
        max_piece_grids = max(max_piece_grids, piece_size)
        total_grids += piece_size
    
    # 根据最大块的大小使用不同的计分公式
    if max_piece_grids <= 6:
        score = 8900 * total_pieces * max_piece_grids / total_grids / total_grids
    elif max_piece_grids == 7:
        score = 4250 * total_pieces * max_piece_grids / total_grids / total_grids
    else:
        score = 540 / total_grids
    
    # 取整
    return int(score)

# 修改绘制判定结果函数
def draw_result():
    global success_sound_played, fail_sound_played
    
    if check_result is None:
        return
    
    # 播放音效
    if check_result and not success_sound_played:
        SOUNDS['success'].play()
        success_sound_played = True
    elif not check_result and not fail_sound_played:
        SOUNDS['fail'].play()
        fail_sound_played = True
    
    # 创建半透明蒙版
    overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(overlay, RESULT_OVERLAY_COLOR, overlay.get_rect())
    screen.blit(overlay, (0, 0))
    
    # 绘制标题
    title_font = pygame.font.SysFont(None, RESULT_TITLE_SIZE)
    if check_result:
        title_text = title_font.render("PUZZLE COMPLETE!", True, RESULT_SUCCESS_COLOR)
        detail_text = f"Score: {calculate_score()}"  # 使用计算出的分数
        text_color = RESULT_SUCCESS_COLOR
    else:
        title_text = title_font.render("PUZZLE FAILED!", True, RESULT_FAILURE_COLOR)
        detail_text = failure_reason
        text_color = RESULT_FAILURE_COLOR
    
    # 绘制标题
    title_rect = title_text.get_rect(centerx=SCREEN_WIDTH//2, centery=SCREEN_HEIGHT//2 - 50)
    screen.blit(title_text, title_rect)
    
    # 绘制详细信息
    detail_font = pygame.font.SysFont(None, RESULT_TEXT_SIZE)
    detail_text = detail_font.render(detail_text, True, text_color)
    detail_rect = detail_text.get_rect(centerx=SCREEN_WIDTH//2, centery=SCREEN_HEIGHT//2 + 20)
    screen.blit(detail_text, detail_rect)
    
    # 绘制重新开始按钮
    global result_button_rect, result_button_hover
    result_button_rect = pygame.Rect(
        SCREEN_WIDTH//2 - RESULT_BUTTON_WIDTH//2,
        SCREEN_HEIGHT//2 + 80,
        RESULT_BUTTON_WIDTH,
        RESULT_BUTTON_HEIGHT
    )
    
    # 检查鼠标悬停
    mouse_pos = pygame.mouse.get_pos()
    result_button_hover = result_button_rect.collidepoint(mouse_pos)
    button_color = RESULT_BUTTON_HOVER_COLOR if result_button_hover else RESULT_BUTTON_COLOR
    
    # 绘制按钮
    pygame.draw.rect(screen, button_color, result_button_rect)
    
    # 绘制按钮文字
    button_font = pygame.font.SysFont(None, RESULT_BUTTON_TEXT_SIZE)
    button_text = button_font.render("Restart", True, RESULT_BUTTON_TEXT_COLOR)
    button_text_rect = button_text.get_rect(center=result_button_rect.center)
    screen.blit(button_text, button_text_rect)

# 修改主循环
def main():
    global grid_size, grid_offset_x, grid_offset_y, dragging, last_mouse_pos, slider_dragging, slider_value
    global left_mouse_down, right_mouse_down, selected_piece_index, dragging_piece, dragging_piece_offset
    global SCREEN_WIDTH, SCREEN_HEIGHT, screen, notification, create_button_rect, create_button_hover
    global cells, puzzle_pieces, available_colors, current_color_index, delete_button_rect, delete_button_hover
    global is_judging, check_result  # 添加这一行，声明判定相关的全局变量
    
    # 显示规则说明
    show_rules()
    
    # 初始化游戏状态
    restart_game()
    
    # 鼠标状态
    left_mouse_down = False
    right_mouse_down = False
    last_cell_pos = None
    
    clock = pygame.time.Clock()
    
    running = True
    while running:
        # 处理事件
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            # 如果正在判定，只处理窗口相关事件和重新开始按钮点击
            elif is_judging:
                if event.type == VIDEORESIZE:
                    pass
                    #SCREEN_WIDTH = event.w
                    #SCREEN_HEIGHT = event.h
                    #screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    if result_button_rect and result_button_rect.collidepoint(event.pos):
                        restart_game()
                        is_judging = False
                        check_result = None
                continue
            
            # 处理其他事件
            elif event.type == KEYDOWN:
                # 撤销操作
                if event.key == KEYBOARD_SHORTCUTS['undo']:
                    undo()
                
                # 重新开始
                elif event.key == KEYBOARD_SHORTCUTS['restart']:
                    restart_game()
                
                # 创建拼图
                elif event.key == KEYBOARD_SHORTCUTS['create']:
                    if not selected_piece_index:  # 如果没有选中拼图块
                        create_puzzle_piece()
                
                # 创建拼图（快捷键2）
                elif event.key == KEYBOARD_SHORTCUTS['create2']:
                    if not selected_piece_index:  # 如果没有选中拼图块
                        create_puzzle_piece()

                # 删除拼图
                elif event.key == KEYBOARD_SHORTCUTS['delete']:
                    if selected_piece_index is not None:  # 如果有选中拼图块
                        delete_selected_piece()
                
                # 完成拼图
                elif event.key == KEYBOARD_SHORTCUTS['complete']:
                    complete_puzzle()
                
                # 放大
                elif event.key == KEYBOARD_SHORTCUTS['zoom_in']:
                    # 保存屏幕中心相对于网格的位置
                    center_grid_x = (SCREEN_WIDTH/2 - grid_offset_x) / grid_size
                    center_grid_y = (SCREEN_HEIGHT/2 - grid_offset_y) / grid_size
                    
                    # 增加网格大小
                    grid_size = min(grid_size + 5, MAX_GRID_SIZE)
                    slider_value = (grid_size - MIN_GRID_SIZE) / (MAX_GRID_SIZE - MIN_GRID_SIZE)
                    
                    # 调整偏移量，使屏幕中心的网格保持不变
                    grid_offset_x = SCREEN_WIDTH/2 - center_grid_x * grid_size
                    grid_offset_y = SCREEN_HEIGHT/2 - center_grid_y * grid_size
                
                # 缩小
                elif event.key == KEYBOARD_SHORTCUTS['zoom_out']:
                    # 保存屏幕中心相对于网格的位置
                    center_grid_x = (SCREEN_WIDTH/2 - grid_offset_x) / grid_size
                    center_grid_y = (SCREEN_HEIGHT/2 - grid_offset_y) / grid_size
                    
                    # 减小网格大小
                    grid_size = max(grid_size - 5, MIN_GRID_SIZE)
                    slider_value = (grid_size - MIN_GRID_SIZE) / (MAX_GRID_SIZE - MIN_GRID_SIZE)
                    
                    # 调整偏移量，使屏幕中心的网格保持不变
                    grid_offset_x = SCREEN_WIDTH/2 - center_grid_x * grid_size
                    grid_offset_y = SCREEN_HEIGHT/2 - center_grid_y * grid_size
                
                # 适应视图
                elif event.key == KEYBOARD_SHORTCUTS['fit_view']:
                    fit_view_to_content()
            
            elif event.type == VIDEORESIZE:
                pass
                # 更新窗口大小
                #SCREEN_WIDTH, SCREEN_HEIGHT = event.size
                #screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
            
            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 1:  # 左键
                    # 标记是否已处理点击事件
                    click_handled = False
                    
                    # 获取UI元素的中心X坐标
                    ui_center_x = UI_LEFT_MARGIN + UI_BUTTON_SIZE // 2
                    
                    # 计算各UI元素的矩形区域
                    slider_bg_rect = pygame.Rect(
                        ui_center_x - UI_SLIDER_WIDTH // 2, 
                        SLIDER_Y, 
                        UI_SLIDER_WIDTH, 
                        UI_SLIDER_HEIGHT
                    )
                    
                    slider_handle_rect = pygame.Rect(
                        ui_center_x - UI_SLIDER_HANDLE_WIDTH // 2, 
                        SLIDER_Y + int((1 - slider_value) * UI_SLIDER_HEIGHT) - UI_SLIDER_HANDLE_HEIGHT // 2, 
                        UI_SLIDER_HANDLE_WIDTH, 
                        UI_SLIDER_HANDLE_HEIGHT
                    )
                    
                    plus_button_rect = pygame.Rect(
                        ui_center_x - UI_BUTTON_SIZE // 2, 
                        UI_TOP_MARGIN, 
                        UI_BUTTON_SIZE, 
                        UI_BUTTON_SIZE
                    )
                    
                    minus_button_rect = pygame.Rect(
                        ui_center_x - UI_BUTTON_SIZE // 2, 
                        SLIDER_Y + UI_SLIDER_HEIGHT + UI_BUTTON_SPACING, 
                        UI_BUTTON_SIZE, 
                        UI_BUTTON_SIZE
                    )
                    
                    fit_view_button_rect = pygame.Rect(
                        ui_center_x - UI_BUTTON_SIZE // 2, 
                        minus_button_rect.bottom + FIT_VIEW_BUTTON_Y_OFFSET, 
                        UI_BUTTON_SIZE, 
                        UI_BUTTON_SIZE
                    )
                    
                    # 检查是否点击了滑动条背景或滑块
                    if slider_bg_rect.collidepoint(event.pos) or slider_handle_rect.collidepoint(event.pos):
                        # 保存屏幕中心相对于网格的位置
                        center_grid_x = (SCREEN_WIDTH/2 - grid_offset_x) / grid_size
                        center_grid_y = (SCREEN_HEIGHT/2 - grid_offset_y) / grid_size
                        
                        # 直接设置滑块位置
                        slider_value = max(0, min(1, 1 - (event.pos[1] - SLIDER_Y) / UI_SLIDER_HEIGHT))
                        
                        # 更新网格大小
                        grid_size = int(MIN_GRID_SIZE + slider_value * (MAX_GRID_SIZE - MIN_GRID_SIZE))
                        
                        # 调整偏移量，使屏幕中心的网格保持不变
                        grid_offset_x = SCREEN_WIDTH/2 - center_grid_x * grid_size
                        grid_offset_y = SCREEN_HEIGHT/2 - center_grid_y * grid_size
                        
                        # 开始拖动
                        slider_dragging = True
                        click_handled = True
                    
                    # 检查是否点击了加号按钮
                    elif plus_button_rect.collidepoint(event.pos):
                        # 保存屏幕中心相对于网格的位置
                        center_grid_x = (SCREEN_WIDTH/2 - grid_offset_x) / grid_size
                        center_grid_y = (SCREEN_HEIGHT/2 - grid_offset_y) / grid_size
                        
                        # 增加网格大小
                        grid_size = min(grid_size + 5, MAX_GRID_SIZE)
                        slider_value = (grid_size - MIN_GRID_SIZE) / (MAX_GRID_SIZE - MIN_GRID_SIZE)
                        
                        # 调整偏移量，使屏幕中心的网格保持不变
                        grid_offset_x = SCREEN_WIDTH/2 - center_grid_x * grid_size
                        grid_offset_y = SCREEN_HEIGHT/2 - center_grid_y * grid_size
                        click_handled = True
                    
                    # 检查是否点击了减号按钮
                    elif minus_button_rect.collidepoint(event.pos):
                        # 保存屏幕中心相对于网格的位置
                        center_grid_x = (SCREEN_WIDTH/2 - grid_offset_x) / grid_size
                        center_grid_y = (SCREEN_HEIGHT/2 - grid_offset_y) / grid_size
                        
                        # 减小网格大小
                        grid_size = max(grid_size - 5, MIN_GRID_SIZE)
                        slider_value = (grid_size - MIN_GRID_SIZE) / (MAX_GRID_SIZE - MIN_GRID_SIZE)
                        
                        # 调整偏移量，使屏幕中心的网格保持不变
                        grid_offset_x = SCREEN_WIDTH/2 - center_grid_x * grid_size
                        grid_offset_y = SCREEN_HEIGHT/2 - center_grid_y * grid_size
                        click_handled = True
                    
                    # 检查是否点击了显示恰当大小画面按钮
                    elif fit_view_button_rect.collidepoint(event.pos):
                        # 播放点击音效
                        SOUNDS['click_flip'].play()
                        fit_view_to_content()
                        click_handled = True
                    
                    # 检查是否点击了撤销按钮
                    elif undo_button_rect and undo_button_rect.collidepoint(event.pos):
                        undo()
                        # 清除选择
                        selected_piece_index = None
                        click_handled = True
                    
                    # 检查是否点击了重新开始按钮
                    elif restart_button_rect and restart_button_rect.collidepoint(event.pos):
                        restart_game()
                        # 清除选择
                        selected_piece_index = None
                        click_handled = True
                    
                    # 检查是否点击了删除拼图块按钮
                    elif delete_button_rect and delete_button_rect.collidepoint(event.pos):
                        delete_selected_piece()
                        click_handled = True
                    
                    # 检查是否点击了创建拼图块按钮
                    elif create_button_rect and create_button_rect.collidepoint(event.pos):
                        create_puzzle_piece()
                        # 清除选择
                        selected_piece_index = None
                        click_handled = True
                    
                    # 检查是否点击了完成拼图按钮
                    elif complete_button_rect and complete_button_rect.collidepoint(event.pos):
                        complete_puzzle()
                        click_handled = True
                    
                    # 如果点击事件已处理，不进行填色操作
                    if click_handled:
                        continue
                    
                    # 检查是否点击了拼图块
                    piece_index = get_piece_at_pos(event.pos)
                    if piece_index is not None:
                        # 播放选择音效
                        SOUNDS['pick_up'].play()
                        
                        # 选择拼图块
                        selected_piece_index = piece_index
                        
                        # 开始拖动拼图块
                        dragging_piece = True
                        
                        # 计算点击位置相对于网格的坐标
                        grid_x = (event.pos[0] - grid_offset_x) / grid_size
                        grid_y = (event.pos[1] - grid_offset_y) / grid_size
                        
                        # 计算点击位置与拼图块第一个格子的偏移量
                        first_cell = puzzle_pieces[piece_index]['cells'][0]
                        dragging_piece_offset = (grid_x - first_cell[0], grid_y - first_cell[1])
                        
                        click_handled = True
                    else:
                        # 清除选择
                        selected_piece_index = None
                        
                        # 开始填色
                        left_mouse_down = True
                        cell_pos = get_grid_pos(event.pos)
                        
                        # 检查是否可以填色
                        if not is_in_puzzle_piece(cell_pos):
                            # 如果是新的操作，保存当前状态
                            if cell_pos not in cells:
                                save_game_state()
                            
                            # 填色（使用默认颜色）
                            cells[cell_pos] = DEFAULT_CELL_COLOR
                            last_cell_pos = cell_pos
                
                elif event.button == 2:  # 中键
                    dragging = True
                    last_mouse_pos = event.pos
                
                elif event.button == 3:  # 右键
                    # 检查是否点击了拼图块
                    piece_index = get_piece_at_pos(event.pos)
                    if piece_index is not None:
                        # 选择拼图块
                        selected_piece_index = piece_index
                    else:
                        # 清除选择
                        selected_piece_index = None
                        
                        # 开始清除颜色
                        right_mouse_down = True
                        cell_pos = get_grid_pos(event.pos)
                        
                        # 检查是否可以清除颜色
                        if cell_pos in cells and not is_in_puzzle_piece(cell_pos):
                            # 保存当前状态
                            save_game_state()
                            
                            # 清除颜色
                            del cells[cell_pos]
                            last_cell_pos = cell_pos
                
                elif event.button == 4:  # 滚轮上滚
                    # 保存鼠标位置相对于网格的位置
                    mouse_grid_x = (event.pos[0] - grid_offset_x) / grid_size
                    mouse_grid_y = (event.pos[1] - grid_offset_y) / grid_size
                    
                    # 增加网格大小
                    old_grid_size = grid_size
                    grid_size = min(grid_size + 5, MAX_GRID_SIZE)
                    slider_value = (grid_size - MIN_GRID_SIZE) / (MAX_GRID_SIZE - MIN_GRID_SIZE)
                    
                    # 调整偏移量，使鼠标位置的网格保持不变
                    grid_offset_x = event.pos[0] - mouse_grid_x * grid_size
                    grid_offset_y = event.pos[1] - mouse_grid_y * grid_size
                
                elif event.button == 5:  # 滚轮下滚
                    # 保存鼠标位置相对于网格的位置
                    mouse_grid_x = (event.pos[0] - grid_offset_x) / grid_size
                    mouse_grid_y = (event.pos[1] - grid_offset_y) / grid_size
                    
                    # 减小网格大小
                    old_grid_size = grid_size
                    grid_size = max(grid_size - 5, MIN_GRID_SIZE)
                    slider_value = (grid_size - MIN_GRID_SIZE) / (MAX_GRID_SIZE - MIN_GRID_SIZE)
                    
                    # 调整偏移量，使鼠标位置的网格保持不变
                    grid_offset_x = event.pos[0] - mouse_grid_x * grid_size
                    grid_offset_y = event.pos[1] - mouse_grid_y * grid_size
            
            elif event.type == MOUSEBUTTONUP:
                if event.button == 1:  # 左键
                    left_mouse_down = False
                    slider_dragging = False
                    
                    # 如果正在拖动拼图块，尝试放置
                    if dragging_piece and selected_piece_index is not None:
                        # 计算当前鼠标位置对应的网格坐标
                        grid_x = (event.pos[0] - grid_offset_x) / grid_size
                        grid_y = (event.pos[1] - grid_offset_y) / grid_size
                        
                        # 计算拼图块应该移动的网格单位数（四舍五入到整数）
                        offset_x = round(grid_x - dragging_piece_offset[0] - puzzle_pieces[selected_piece_index]['cells'][0][0])
                        offset_y = round(grid_y - dragging_piece_offset[1] - puzzle_pieces[selected_piece_index]['cells'][0][1])
                        
                        # 如果有移动且可以放置
                        if (offset_x != 0 or offset_y != 0) and can_place_piece_at(selected_piece_index, offset_x, offset_y):
                            # 保存当前状态
                            save_game_state()
                            
                            # 移动拼图块
                            new_cells = []
                            for pos in puzzle_pieces[selected_piece_index]['cells']:
                                new_pos = (pos[0] + offset_x, pos[1] + offset_y)
                                new_cells.append(new_pos)
                            
                            puzzle_pieces[selected_piece_index]['cells'] = new_cells
                    
                    # 重置拖动状态
                    dragging_piece = False
                    dragging_piece_offset = None
                    last_cell_pos = None
                
                elif event.button == 2:  # 中键
                    dragging = False
                
                elif event.button == 3:  # 右键
                    right_mouse_down = False
                    last_cell_pos = None
            
            elif event.type == MOUSEMOTION:
                if dragging:
                    # 计算鼠标移动距离
                    dx = event.pos[0] - last_mouse_pos[0]
                    dy = event.pos[1] - last_mouse_pos[1]
                    
                    # 更新网格偏移量
                    grid_offset_x += dx
                    grid_offset_y += dy
                    
                    # 更新鼠标位置
                    last_mouse_pos = event.pos
                
                elif slider_dragging:
                    # 保存屏幕中心相对于网格的位置
                    center_grid_x = (SCREEN_WIDTH/2 - grid_offset_x) / grid_size
                    center_grid_y = (SCREEN_HEIGHT/2 - grid_offset_y) / grid_size
                    
                    # 计算滑动条值
                    slider_value = max(0, min(1, 1 - (event.pos[1] - SLIDER_Y) / UI_SLIDER_HEIGHT))
                    
                    # 更新网格大小
                    old_grid_size = grid_size
                    grid_size = int(MIN_GRID_SIZE + slider_value * (MAX_GRID_SIZE - MIN_GRID_SIZE))
                    
                    # 调整偏移量，使屏幕中心的网格保持不变
                    grid_offset_x = SCREEN_WIDTH/2 - center_grid_x * grid_size
                    grid_offset_y = SCREEN_HEIGHT/2 - center_grid_y * grid_size
                
                # 处理拼图块拖动
                elif dragging_piece and selected_piece_index is not None:
                    # 不需要在移动时做任何事情，只在绘制时显示预览
                    pass
                
                # 处理填色拖动
                elif left_mouse_down or right_mouse_down:
                    cell_pos = get_grid_pos(event.pos)
                    
                    # 检查是否是新的格子
                    if cell_pos != last_cell_pos:
                        if left_mouse_down and not is_in_puzzle_piece(cell_pos):
                            # 填色（使用默认颜色）
                            cells[cell_pos] = DEFAULT_CELL_COLOR
                            last_cell_pos = cell_pos
                        
                        elif right_mouse_down and cell_pos in cells and not is_in_puzzle_piece(cell_pos):
                            # 清除颜色
                            del cells[cell_pos]
                            last_cell_pos = cell_pos
        
        # 绘制背景
        screen.fill(BG_COLOR)
        
        # 绘制网格
        draw_grid()
        
        # 绘制格子和拼图块
        draw_all_cells()
        
        # 如果正在拖动拼图块，绘制预览
        if not is_judging and dragging_piece and selected_piece_index is not None:
            # 获取鼠标位置
            mouse_pos = pygame.mouse.get_pos()
            
            # 计算当前鼠标位置对应的网格坐标
            grid_x = (mouse_pos[0] - grid_offset_x) / grid_size
            grid_y = (mouse_pos[1] - grid_offset_y) / grid_size
            
            # 计算拼图块应该移动的网格单位数（四舍五入到整数）
            offset_x = round(grid_x - dragging_piece_offset[0] - puzzle_pieces[selected_piece_index]['cells'][0][0])
            offset_y = round(grid_y - dragging_piece_offset[1] - puzzle_pieces[selected_piece_index]['cells'][0][1])
            
            # 检查是否可以放置
            can_place = can_place_piece_at(selected_piece_index, offset_x, offset_y)

            # 创建新拼图块dict
            new_piece = {}
            new_piece['cells'] = [(pos[0] + offset_x, pos[1] + offset_y) for pos in puzzle_pieces[selected_piece_index]['cells']]
            # 根据是否可以放置设置不同的颜色
            if can_place:
                new_piece['color'] = puzzle_pieces[selected_piece_index]['color'][:3] + (120,)
                new_piece_border_color = CELL_SELECTED_BORDER_COLOR
            else:
                # 如果不能放置，使用红色
                new_piece['color'] = (255, 0, 0, 120)
                new_piece_border_color = (255, 0, 0, 255)
            
            # 绘制预览
            draw_single_piece(new_piece, border_color=new_piece_border_color)

        # 绘制UI
        if not is_judging:
            draw_slider()
            draw_buttons()
            if not draw_delete_button():
                draw_create_button()
        
        # 绘制提示信息
        draw_notification()
        
        # 如果正在判定，绘制结果
        if is_judging:
            draw_result()
        
        # 更新显示
        pygame.display.flip()
        clock.tick(120)
    
    pygame.quit()
    sys.exit()

# 启动游戏
if __name__ == "__main__":
    main()

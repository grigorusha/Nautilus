# Search and Explore various Nautilus configurations
# https://twistypuzzles.com/forum/viewtopic.php?f=1&t=34998

import sys, random, webbrowser
from math import radians, cos,sin,tan, pi

import pygame, pygame_gui
from pygame_gui import UIManager

from puzzles import *

# TODO + 0. вращение сразу до позиции флип
# TODO + 0. поворот частей внутри диска
# TODO + 0. скорость поворота
# TODO + 0. норм кнопки
# TODO + 0. поворот частей между дисками
# TODO + 0. скрамбл
# TODO + 0. Выпадающий список с разными заданными головоломками
# TODO + 0. Контуры: круг, улитка, квадрат
# TODO + 0. Квадратик с информацией.
# TODO + 0. Кнопка About с сылками
# TODO + 0. отладить Квадрат
# TODO + 0. галочка : до разделителя
# TODO + 0. центрировать 1 слой

VERSION = "1.0"

# Константы
DISK_RADIUS = 150
DISK_Y = DISK_RADIUS+70
WIDTH, HEIGHT = DISK_RADIUS*2*2+100, DISK_RADIUS*2+200
ROTATION_SPEED = 4
# Инициализация Pygame
pygame.init()
random.seed()
# Настройка экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
font = pygame.font.SysFont('Arial', 16)
pygame.display.set_caption("Nautilus Simulator - v"+VERSION)
status_label = None

manager = UIManager((WIDTH, HEIGHT), 'theme.json')

# Состояние игры
disk_puzzle, disk_count = [], 0
separator_visible = False
drop_puzzles = None
DISK_ANGLE = 0
fl_one_step = False

def init_game():
    global puzzle,separator_visible,disk_count,disk_puzzle, DISK_ANGLE

    disk_puzzle, DISK_ANGLE = puzzle_set(puzzle, DISK_Y, WIDTH, HEIGHT)
    if len(disk_puzzle)==0: return

    sectors_str = ", ".join(map(str, disk_puzzle[0]["sectors"]))
    status_label.set_text(puzzle+": "+sectors_str+" ("+str(DISK_ANGLE)+" step)")
    status_label.rebuild_from_changed_theme_data()

    disk_count = len(disk_puzzle)
    separator_visible = False

    for disk in disk_puzzle:
        calc_spline(disk)


def scramble_game():
    global disk_puzzle
    scramble_move = disk_count * len(disk_puzzle[0]["sectors"])*100
    kol = 180//DISK_ANGLE
    while scramble_move>0:
        for disk in disk_puzzle:
            count = 10
            while count:
                count -= 1
                direct, step = random.choice([1,-1]), random.randint(1,kol)
                rotate_disk(disk, direct*step*DISK_ANGLE)
                disk['rotation'] = disk['target_rotation']
                if can_flip(disk): break
            if can_flip_all_disk():
                flip_disks()
        scramble_move -=1
    for disk in disk_puzzle:
        disk['animating'] = False

####################################################################################################
####################################################################################################

def status_init():
    from pygame_gui.elements import UILabel
    status_y = 5
    status_label = UILabel( relative_rect=pygame.Rect(25, status_y, int(WIDTH)-50, 20),
        text="Simulator: " )
    return status_label

def button_init(disk_puzzle):
    global puzzles_mas1,puzzles_mas2,puzzles_mas3, fl_one_step
    from pygame_gui.elements import UIButton, UIDropDownMenu, UITextBox, UICheckBox

    select_y, label_y, button_y = 30, int(HEIGHT)-117, int(HEIGHT)-42

    drop_down_Puzzle1 = UIDropDownMenu( options_list=puzzles_mas1, starting_option=puzzles_mas1[0],
                                       relative_rect=pygame.Rect(15, select_y, 120, 30) )
    drop_down_Puzzle2 = UIDropDownMenu( options_list=puzzles_mas2, starting_option=puzzles_mas2[0],
                                       relative_rect=pygame.Rect(145, select_y, 105, 30) )
    drop_down_Puzzle3 = UIDropDownMenu( options_list=puzzles_mas3, starting_option=puzzles_mas3[0],
                                       relative_rect=pygame.Rect(260, select_y, 140, 30) )
    drop_down_Puzzle4 = UIDropDownMenu( options_list=puzzles_mas4, starting_option=puzzles_mas4[0],
                                       relative_rect=pygame.Rect(410, select_y, 130, 30) )
    drop_down_Puzzle5 = UIDropDownMenu( options_list=puzzles_mas5, starting_option=puzzles_mas5[0],
                                       relative_rect=pygame.Rect(550, select_y, 130, 30) )
    drop_down_Puzzle_mas = [drop_down_Puzzle1,drop_down_Puzzle2,drop_down_Puzzle3,drop_down_Puzzle4,drop_down_Puzzle5]

    info_label_mas = []
    for nn,disk in enumerate(disk_puzzle):
        info_label_mas.append( UITextBox( relative_rect=pygame.Rect(disk['x'] - DISK_RADIUS, label_y, 300, 65),
            html_text="Top sectors:\n" + "Total:") )

    button_Reset = UIButton((25, button_y, 70, 30), 'Reset')
    button_Scramble = UIButton((100, button_y, 90, 30), 'Scramble')
    button_About = UIButton((255, button_y, 70, 30), 'About')

    check_box_Angle = UICheckBox( (375, button_y, 30, 30), 'One step', initial_state=fl_one_step)

    return (button_Reset, button_Scramble, button_About, drop_down_Puzzle_mas, info_label_mas, check_box_Angle)

def center_button(button_Reset, button_Scramble, button_About, info_label_mas, check_box_Angle):
    fl_left = button_Reset.rect.left == 25

    if disk_count==2 and fl_left: return
    if disk_count==1 and not fl_left: return

    info_label = info_label_mas[0]

    if disk_count == 1 and fl_left:
        # сдвинуть в центр
        shift = 170
    elif disk_count == 2 and not fl_left:
        # сдвинуть в лево
        shift = -170
    else:
        return

    def shift_element_left(element,shift):
        rect = element.get_relative_rect()
        element.set_position( (rect.left + shift, rect.top) )

    shift_element_left(button_Reset,shift)
    shift_element_left(button_Scramble,shift)
    shift_element_left(button_About,shift)
    shift_element_left(check_box_Angle,shift)
    shift_element_left(info_label,shift)


def about_game():
    from pygame_gui.windows import UIMessageWindow

    shift = 130
    message_window = UIMessageWindow( rect=pygame.Rect(shift,shift,WIDTH-shift*2,HEIGHT-shift*2), window_title='About: Nautilus Simulator', always_on_top=True,
                     html_message='Grigorusha Puzzle Simulators: <a href="https://twistypuzzles.com/forum/viewtopic.php?t=38581">https://twistypuzzles.com/forum/viewtopic.php?t=38581</a><br>'+
                                  'Grigorusha Simulators Git: <a href="https://github.com/grigorusha/nautilus">https://github.com/grigorusha/nautilus</a><br>'+
                                  'Search and Explore Nautilus: <a href="https://twistypuzzles.com/forum/viewtopic.php?t=34998">https://twistypuzzles.com/forum/viewtopic.php?t=34998</a>')
    return

####################################################################################################

def rotate_point(x, y, center_x, center_y, angle_deg):
    angle = radians(angle_deg)
    # поворот точки относительно центра координат по часовой стрелке
    adjusted_x, adjusted_y = x - center_x, y - center_y
    cos_rad, sin_rad = cos(angle), sin(angle)
    qx = cos_rad * adjusted_x + sin_rad * adjusted_y
    qy = cos_rad * adjusted_y - sin_rad * adjusted_x
    qx, qy = center_x + qx, center_y + qy
    qx, qy = round(qx, 10), round(qy, 10)
    return qx, qy

def rotate_part(spline, center_x, center_y, angle):
    spline_new = []
    # поворот всех точек из массива относительно центра круга
    for x,y in spline:
        x,y = x+center_x,y+center_y
        if angle!=0: x,y = rotate_point(x,y, center_x, center_y, -angle)
        spline_new.append( (x,y) )
    return spline_new

def mirror_x_part(spline, angle):
    spline_new = rotate_part(spline, 0, 0, -angle)
    # отражение всех точек из массива относительно оси Х
    for nn, (x,y) in enumerate(spline_new):
        spline_new[nn] = (x,-y)
    spline_rev = list(reversed(spline_new))
    last = spline_rev.pop()
    spline_rev.insert(0,last)
    return spline_new


def square_point(edge_size, angle, rotate_angle=0):
    """
    Вычисляет координаты точки на квадрате с центром в (0, 0) и стороной edge_size.
    edge_size: длина стороны квадрата
    angle: угол в градусах (0-360), определяет положение точки на периметре
    Возвращает: (x, y) - координаты точки
    """
    angle_rad = radians(angle)
    half_size = edge_size / 2

    # Нормализуем угол к диапазону [0, 360)
    normalized_angle = angle % 360

    # Определяем, с какой стороной пересекается луч
    if 45 <= normalized_angle < 135:  # Верхняя сторона
        x = half_size / tan(radians(normalized_angle))
        y = half_size
    elif 135 <= normalized_angle < 225:  # Левая сторона
        x = -half_size
        y = -half_size * tan(radians(normalized_angle - 180))
    elif 225 <= normalized_angle < 315:  # Нижняя сторона
        x = -half_size / tan(radians(normalized_angle - 180))
        y = -half_size
    else:  # Правая сторона (0-45 и 315-360)
        x = half_size
        y = half_size * tan(radians(normalized_angle if normalized_angle < 45 else normalized_angle - 360))

    x,y = rotate_point(x,y, 0,0, rotate_angle)

    return (x, y)

def calc_spline(disk):
    angle_shift = disk['angle_shift']
    start_angle, disk['spline'] = angle_shift, []
    for angle_sect in disk['sectors']:
        end_angle = start_angle + angle_sect

        spline = [(0, 0)]
        num_points = max(10, int(angle_sect))  # Количество точек для аппроксимации дуги
        for i in range(num_points + 1):
            angle = start_angle + (end_angle - start_angle) * i / num_points
            angle_rad = radians(angle)
            if disk['type'] == "circle":
                spline.append( (DISK_RADIUS*cos(angle_rad), DISK_RADIUS*sin(angle_rad) ) )
            elif disk['type']=="spiral":
                start = 0.65
                kk = (1-start)/(2*pi)
                mul = start+angle_rad*kk
                spline.append( (mul*DISK_RADIUS*cos(angle_rad), mul*DISK_RADIUS*sin(angle_rad) ) )
            elif disk['type']=="square":
                spline.append( square_point(DISK_RADIUS*1.5, angle) )

        spline_ini = rotate_part(spline, 0,0, -start_angle )
        disk['spline'].append(spline_ini)
        start_angle = end_angle


def draw_disk(disk):
    # рисуем залитые сектора
    start_angle, angle_shift = disk['rotation'], disk['angle_shift']

    for nn, (angle, spline, color) in enumerate(zip(disk['sectors'], disk['spline'], disk['colors'])):
        points = rotate_part(spline,disk['x'],disk['y'],start_angle+angle_shift)
        if len(points) > 2:
            pygame.draw.polygon(screen, color, points)

            # рисуем контур
            pygame.draw.lines(screen, BLACK, False, points[1:], 4)
            pygame.draw.line(screen, BLACK, points[0], points[1], 3)
            pygame.draw.line(screen, BLACK, points[-1], points[0], 3)
        start_angle += angle

def draw_info(disk, info_label):
    top_half = get_top_half(disk)

    sectors_text = f"Top sectors: {', '.join(map(str, top_half['sectors']))}°"
    if can_flip(disk):
        sum_text = f"Total: {top_half['total']}°"
        color = "#0000FF"
    else:
        sum_text = f"Total: {top_half['total']}°"
        color = "#FF0000"

    info_label.visible = True
    info_label.set_text('<font color=normal_text>'+sectors_text+'</font><br>'+'<font color='+color+'>'+sum_text+'</font>')
    info_label.rebuild_from_changed_theme_data()

####################################################################################################

def rotate_disk(disk, angle):
    if angle==1 or angle==-1:
        disk['target_rotation'] = - angle
    else:
        disk['target_rotation'] = (disk['rotation'] - angle) % 360
        disk['target_rotation'] += 360 if disk['target_rotation']<0 else 0
    disk['animating'] = True

def update_animated_disk(disk):
    if disk['animating']:
        if disk['target_rotation']==1 or disk['target_rotation']==-1:
            # новый подход. до остановки
            step = disk['target_rotation']
            disk['rotation'] = (disk['rotation'] + step) % 360
            if can_flip(disk):
                disk['animating'] = False
        else:
            # старый метод. на угол
            diff = (disk['target_rotation'] - disk['rotation'] + 180) % 360 - 180
            if abs(diff) > 0.5:
                step = min(1, abs(diff)) * (1 if diff > 0 else -1)
                disk['rotation'] = (disk['rotation'] + step) % 360
            else:
                disk['rotation'] = disk['target_rotation']
                disk['animating'] = False

####################################################################################################

def mas_pos(mas_xy, pos):
    # получить элемент массива независимо от выхода индекса за границы
    ll = len(mas_xy)
    while pos >= ll:
        pos -= ll
    return mas_xy[pos]

def get_top_half(disk):
    current_angle = disk['rotation']+disk['angle_shift']
    sum_angles, pos180 = 0,-1
    result = []

    pos, len2, fl_top = 0, len(disk['sectors'])*2, -1
    while pos<len2:
        angle = mas_pos(disk['sectors'],pos)
        start = current_angle % 360
        end = (current_angle + angle) % 360
        end = 360 if end==0 else end

        # Проверяем, что сектор полностью в верхней половине
        if (start<end) and (start >= 180 and end <= 360):
            if fl_top>=0:
                result.append({ 'angle': angle, 'color': mas_pos(disk['colors'],pos), 'spline': mas_pos(disk['spline'],pos) })
                sum_angles += angle
                fl_top += 1
                if start==180:
                    pos180 = pos if pos<len(disk['sectors']) else pos-len(disk['sectors'])
        elif fl_top==-1:
            fl_top = 0
        elif fl_top>0:
            break
        current_angle += angle
        pos += 1
        if sum_angles >= 180:
            break

    return {
        'sectors': [item['angle'] for item in result],
        'colors': [item['color'] for item in result],
        'spline': [item['spline'] for item in result],
        'total': sum_angles,
        'pos': pos180
    }

def can_flip(disk):
    top_half = get_top_half(disk)
    return abs(top_half['total'] - 180) < 0.1

def can_flip_all_disk():
    fl_flip = 0
    for disk in disk_puzzle:
        if can_flip(disk):
            fl_flip += 1
    return fl_flip == disk_count

####################################################################################################

def reverse_two_group(arr1,start1,length1, arr2,start2,length2):
    # сдвигаем массивы
    mas1, mas2 = arr1[start1:]+arr1[:start1], arr2[start2:]+arr2[:start2]
    # Выборки
    group1, res1 = mas1[:length1], mas1[length1:]
    group2, res2 = mas2[:length2], mas2[length2:]
    # Переворачиваем выборки
    group1, group2 = group1[::-1], group2[::-1]
    # соединяем выборки
    result1, result2 = res1 + group2, res2 + group1
    return result1,result2

def reverse_group(arr, start, length):
    # сдвигаем массив
    mas = arr[start:]+arr[:start]
    # Выборки
    group, res = mas[:length], mas[length:]
    # Переворачиваем выборку
    group = group[::-1]
    # соединяем выборки
    result = res + group
    return result

def flip_disks():
    global disk_puzzle

    if not can_flip_all_disk(): return
    block_mas = ("sectors", "colors", "spline")

    if disk_count==1 or disk_count==3:
        if disk_count==1:
            disk = disk_puzzle[0]
        elif disk_count==3:
            disk = disk_puzzle[1]
        disk_top = get_top_half(disk)

        pos,length,size = disk_top["pos"],len(disk_top["sectors"]),len(disk["sectors"])
        for nn in range(length):
            angle, spline = disk_top['sectors'][nn], disk_top['spline'][nn]
            pos_mas = pos+nn
            pos_mas -= 0 if pos_mas<size else size
            disk['spline'][pos_mas] = mirror_x_part(spline, angle)

        for block in block_mas:
            disk[block] = reverse_group(disk[block], pos,length)
        disk["rotation"] = 0

    if disk_count==2 or disk_count==3:
        if disk_count==2:
            disk1, disk2 = disk_puzzle[0], disk_puzzle[1]
        elif disk_count==3:
            disk1, disk2 = disk_puzzle[0], disk_puzzle[2]
        disk1_top,disk2_top = get_top_half(disk1),get_top_half(disk2)

        pos1,length1,size1 = disk1_top["pos"],len(disk1_top["sectors"]),len(disk1["sectors"])
        for nn in range(length1):
            angle, spline = disk1_top['sectors'][nn], disk1_top['spline'][nn]
            pos_mas = pos1+nn
            pos_mas -= 0 if pos_mas<size1 else size1
            disk1['spline'][pos_mas] = mirror_x_part(spline, angle)

        pos2,length2,size2 = disk2_top["pos"],len(disk2_top["sectors"]),len(disk2["sectors"])
        for nn in range(length2):
            angle, spline = disk2_top['sectors'][nn], disk2_top['spline'][nn]
            pos_mas = pos2+nn
            pos_mas -= 0 if pos_mas<size2 else size2
            disk2['spline'][pos_mas] = mirror_x_part(spline, angle)

        for block in block_mas:
            disk1[block],disk2[block] = reverse_two_group(disk1[block], pos1,length1, disk2[block], pos2,length2)
        disk1["rotation"] = disk2["rotation"] = 0
        disk1["angle_shift"] = disk2["angle_shift"] = 0

def events_work(events, button_Reset, button_Scramble, button_About, drop_down_Puzzle_mas, info_label_mas, check_box_Angle):
    from pygame_gui import UI_BUTTON_PRESSED, UI_DROP_DOWN_MENU_CHANGED, UI_CHECK_BOX_CHECKED, UI_CHECK_BOX_UNCHECKED
    global puzzle, disk_puzzle, separator_visible, status_label, fl_one_step

    for event in events:
        mouse_pos = pygame.mouse.get_pos()
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        elif event.type == pygame.MOUSEWHEEL:
            for disk in disk_puzzle:
                if disk["animating"]: break
                if abs(mouse_pos[0] - disk['x']) < DISK_RADIUS and abs(mouse_pos[1] - disk['y']) < DISK_RADIUS:
                    if not fl_one_step:
                        rotate_disk(disk, event.y)
                    else:
                        rotate_disk(disk, event.y * DISK_ANGLE)

        elif event.type == UI_BUTTON_PRESSED:
            if event.ui_element == button_Reset:
                init_game()
                center_button(button_Reset, button_Scramble, button_About, info_label_mas, check_box_Angle)
            elif event.ui_element == button_Scramble:
                scramble_game()
            elif event.ui_element == button_About:
                about_game()
        elif event.type == UI_CHECK_BOX_CHECKED:
            if event.ui_element == check_box_Angle:
                fl_one_step = True
        elif event.type == UI_CHECK_BOX_UNCHECKED:
            if event.ui_element == check_box_Angle:
                fl_one_step = False

        elif event.type == UI_DROP_DOWN_MENU_CHANGED:
            for drop_down_Puzzle in drop_down_Puzzle_mas:
                if event.ui_element == drop_down_Puzzle:
                    puzzle = drop_down_Puzzle.selected_option[0]
                    break
            if puzzle:
                init_game()
                center_button(button_Reset, button_Scramble, button_About, info_label_mas, check_box_Angle)
        elif event.type == pygame_gui.UI_TEXT_BOX_LINK_CLICKED:
            link = event.link_target
            if link != "":
                webbrowser.open(link, new=2, autoraise=True)

        elif event.type == pygame.MOUSEBUTTONUP and (event.button == 1):
            # исключим клики в открытых списках - баг движка
            fl_check = True
            for drop_down_Puzzle in drop_down_Puzzle_mas:
                if drop_down_Puzzle.is_focused:
                    fl_check = False
                    break
            # Проверяем клик по дискам для обмена
            if fl_check:
                if abs(mouse_pos[1] - disk_puzzle[0]['y']) < DISK_RADIUS:
                    if can_flip_all_disk():
                        flip_disks()

        manager.process_events(event)


def main():
    global puzzle, disk_puzzle, separator_visible, status_label

    clock = pygame.time.Clock()

    status_label = status_init()
    init_game()
    (button_Reset, button_Scramble, button_About, drop_down_Puzzle_mas, info_label_mas, check_box_Angle) = button_init(disk_puzzle)
    center_button(button_Reset, button_Scramble, button_About, info_label_mas, check_box_Angle)

    while True:
        time_delta = clock.tick(60) / 1000.0

        # обработка событий
        events = pygame.event.get()
        events_work(events, button_Reset, button_Scramble, button_About, drop_down_Puzzle_mas, info_label_mas, check_box_Angle)

        # Обновление при вращении
        for disk in disk_puzzle:
            for sp in range(ROTATION_SPEED):
                update_animated_disk(disk)
                if can_flip(disk):
                    break

        # Отрисовка
        screen.fill(WHITE)

        # Рисуем диски
        for disk in disk_puzzle:
            draw_disk(disk)

        # Рисуем разделитель, если нужно
        separator_visible = can_flip_all_disk()
        if separator_visible:
            pygame.draw.line(screen, GREEN,(disk_puzzle[0]['x'] - DISK_RADIUS - 30, disk_puzzle[0]['y']),(disk_puzzle[-1]['x'] + DISK_RADIUS + 30, disk_puzzle[-1]['y']), 2)

        # Отображаем информацию
        for nn,disk in enumerate(disk_puzzle):
            draw_info(disk, info_label_mas[nn])
        if len(disk_puzzle)<len(info_label_mas):
            for nn in range(len(disk_puzzle),len(info_label_mas)):
                info_label_mas[nn].visible = False

        manager.update(time_delta)
        manager.draw_ui(screen)
        pygame.display.flip()
        clock.tick(60)

main()
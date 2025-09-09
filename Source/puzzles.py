from math import gcd
from functools import reduce

WHITE, BLACK, GRAY = (255, 255, 255), (0, 0, 0), (200, 200, 200)
RED, ORANGE, YELLOW, GREEN, BLUE, LIGHT_BLUE = (255, 0, 0), (250, 150, 0), (255, 255, 0), (0, 150, 0), (0, 0, 255), (100, 200, 250)
PINK, PURPLE, TEAL, BROWN, LIGHT_PURPLE, LIME = (250, 120, 190),(128, 0, 128), (0, 128, 128), (120, 60, 30), (200, 130, 250), (70, 250, 70)
COLORS = [ PINK, RED, YELLOW, ORANGE, LIME, GREEN, LIGHT_BLUE, BLUE, LIGHT_PURPLE, PURPLE, TEAL, BROWN ]
# COLORS = [ RED, YELLOW, ORANGE, GREEN, LIGHT_BLUE, BLUE, PURPLE ]

"""
        clWhite        := 'F0F0F0';    clYellow       := 'FFFF00';
        clGainsboro    := 'C0C0C0';    clOrange       := 'FF6000';
        clSilver       := 'A0A0A0';    clKhaki        := 'F0E68C';
        clGray         := '707070';    clGolden       := 'DDBB20';
        clBlack        := '202020';    clOlive        := '808000';
                                                                  
        clCyan         := '00FFFF';    clGreenYellow  := 'ADFF2F';     
        clDeepSky      := '00BFFF';    clLime         := '00FF00';     
        clTeal         := '008080';    clSea          := '3cb371';
        clBlue         := '0000FF';    clGreen        := '008000';     
        clNavy         := '000080';    clDarkGreen    := '006400';     
                                                                  
        clCoral        := 'FF7F50';    clPink         := 'FF69B4';
        clRed          := 'FF0000';    clFuchsia      := 'FF00FF';
        clCrimson      := 'DC143C';    clPale         := 'D07090';
        clIndian       := 'CD5C5C';    clOrchid       := 'DA70D6';
        clBrown        := '800000';    clPurple       := '800080';

        clChocolate    := 'C26519';    clIndigo       := '4B0082';
        clPeru         := 'CD853F';    clDarkSlate    := '483D8B';
        clSandyBrown   := 'F4A460';    clSlate        := '6A5ACD';

        clSeaGreen     := '2E8B57';
        clAquaMarine   := '66CDAA';
        clDarkSeaGreen := '8FBC8F';
"""

puzzle="Nautilus 7"
puzzles_mas1 = [ "Nautilus 7", "Nautilus 8", "Nautilus 10", "Nautilus 12" ] # , "Nautilus 15", "Nautilus 16"
puzzles_mas2 = [ "Helix 7r", "Helix 7r-b", "Helix 11r", "Helix 8", "Helix 9", "Helix 11", "Helix 11-b", "Helix 12", "Helix 12-b" ]
puzzles_mas3 = [ "Phibonachi 3", "Phibonachi 4", "Phibonachi 4-b", "Phibonachi 4-c", "Phibonachi 4-d", "Phibonachi 4-e", "Phibonachi 5", "Phibonachi 5-b", "Phibonachi 6", "Phibonachi 6-b" ]
puzzles_mas4 = [ "Square-1", "Square-2", "Easy Square-1" ]
puzzles_mas5 = [ "Sajt", "Rainbow Puck", "Cheese" ]

def puzzle_set(puzzle, DISK_Y, WIDTH, HEIGHT):
    angle_shift = 0
    if puzzle in puzzles_mas1 or puzzle in puzzles_mas2 or puzzle in puzzles_mas3:
        if puzzle == "Nautilus 7":
            DISK_SECTORS = [20, 30, 40, 50, 60, 70, 90]
        elif puzzle == "Nautilus 8":
            DISK_SECTORS = [10, 20, 30, 40, 50, 60, 70, 80]
        elif puzzle == "Nautilus 10":
            DISK_SECTORS = [6,12,18,24,30,42,48,54,60,66]
        elif puzzle == "Nautilus 12":
            DISK_SECTORS = [8,12,16,20,24,28,32,36,40,44,48,52]
        # elif puzzle == "Nautilus 15":
        #     DISK_SECTORS = [3,6,9,12,15,18,21,24,27,30,33,36,39,42,45]
        # elif puzzle == "Nautilus 16":
        #     DISK_SECTORS = [15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30]

        elif puzzle == "Helix 7r":
            DISK_SECTORS = [36, 48, 60, 72, 60, 48, 36]
        elif puzzle == "Helix 7r-b":
            DISK_SECTORS = [63, 54, 45, 36, 45, 54, 63]
        elif puzzle == "Helix 11r":
            DISK_SECTORS = [10, 20, 30, 40, 50, 60, 50, 40, 30, 20, 10]
        elif puzzle == "Helix 8":
            DISK_SECTORS = [9, 18, 27, 36, 54, 63, 72, 81]
        elif puzzle == "Helix 9":
            DISK_SECTORS = [12,18,24,36,42,48,54,60,66]
        elif puzzle == "Helix 11":
            DISK_SECTORS = [5,10,15,20,25,35,40,45,50,55,60]
        elif puzzle == "Helix 11-b":
            DISK_SECTORS = [12,16,20,24,28,32,36,40,44,52,56]
        elif puzzle == "Helix 12":
            DISK_SECTORS = [12,15,18,21,24,27,33,36,39,42,45,48]
        elif puzzle == "Helix 12-b":
            DISK_SECTORS = [18,20,22,24,26,28,32,34,36,38,40,42] # bad scramble

        elif puzzle == "Phibonachi 3":
            DISK_SECTORS = [30, 60, 90, 30, 60, 90]
        elif puzzle == "Phibonachi 3-b":
            DISK_SECTORS = [40, 50, 90, 40, 50, 90]
        elif puzzle == "Phibonachi 4":
            DISK_SECTORS = [20, 30, 50, 80, 20, 30, 50, 80]
        elif puzzle == "Phibonachi 4-b":
            DISK_SECTORS = [24, 27, 51, 78, 24, 27, 51, 78]
        elif puzzle == "Phibonachi 4-c":
            DISK_SECTORS = [16, 33, 49, 82, 16, 33, 49, 82]
        elif puzzle == "Phibonachi 4-d":
            DISK_SECTORS = [12, 36, 48, 84, 12, 36, 48, 84]
        elif puzzle == "Phibonachi 4-e":
            DISK_SECTORS = [8, 39, 47, 86, 8, 39, 47, 86]
        elif puzzle == "Phibonachi 5":
            DISK_SECTORS = [15, 15, 30, 45, 75, 15, 15, 30, 45, 75]
        elif puzzle == "Phibonachi 5-b":
            DISK_SECTORS = [8, 20, 28, 48, 76, 8, 20, 28, 48, 76]
        elif puzzle == "Phibonachi 6":
            DISK_SECTORS = [9, 9, 18, 27, 45, 72, 9, 9, 18, 27, 45, 72]
        elif puzzle == "Phibonachi 6-b":
            DISK_SECTORS = [6, 11, 17, 28, 45, 73, 6, 11, 17, 28, 45, 73]

        colors_mas = COLORS[:len(DISK_SECTORS)]
        disk1 = {
            'sectors': DISK_SECTORS,
            'type': "spiral"
        }
        # disk_puzzle = [disk1]
        disk_puzzle = [disk1, disk1.copy()]
    elif puzzle in puzzles_mas4:
        angle_shift = 0
        if puzzle == "Square-1":
            DISK_SECTORS = [30, 60, 30, 60, 30, 60, 30, 60]
            angle_shift = - DISK_SECTORS[0]/2
        elif puzzle == "Square-2":
            DISK_SECTORS = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
            angle_shift = - DISK_SECTORS[0]/2
        elif puzzle == "Easy Square-1":
            DISK_SECTORS = [36, 54, 36, 54, 36, 54, 36, 54]
            angle_shift = - DISK_SECTORS[0]/2
        colors_mas = [RED]*len(DISK_SECTORS)
        disk1 = {
            'sectors': DISK_SECTORS,
            'angle_shift': angle_shift,
            'colors': colors_mas.copy(),
            'type': "square"
        }
        colors_mas = [GREEN]*len(DISK_SECTORS)
        disk2 = {
            'sectors': DISK_SECTORS,
            'angle_shift': angle_shift,
            'colors': colors_mas.copy(),
            'type': "square"
        }
        disk_puzzle = [disk1, disk2]
    elif puzzle == "Sajt" or puzzle == "Rainbow Puck":
        if puzzle == "Sajt":
            DISK_SECTORS = [60, 60, 60, 60, 60, 60]
            colors_mas = [RED, RED, YELLOW, YELLOW, ORANGE, ORANGE]
        elif puzzle == "Rainbow Puck":
            DISK_SECTORS = [30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30, 30]
            colors_mas = [RED, RED, YELLOW, YELLOW, ORANGE, ORANGE, GREEN, GREEN, BLUE, BLUE, PURPLE, PURPLE]
        disk1 = {
            'sectors': DISK_SECTORS,
            'colors': colors_mas.copy(),
            'type': "circle"
        }
        disk_puzzle = [disk1]
    elif puzzle == "Cheese":
        DISK_SECTORS = [60, 60, 60, 60, 60, 60]
        colors_mas = [RED, YELLOW, ORANGE, GREEN, BLUE, PURPLE]
        disk1 = {
            'sectors': DISK_SECTORS,
            'colors': colors_mas.copy(),
            'type': "circle"
        }
        disk2 = {
            'sectors': DISK_SECTORS,
            'colors': colors_mas.copy(),
            'type': "circle"
        }
        disk_puzzle = [disk1,disk2]
    else:
        return [],0

    for nn,disk in enumerate(disk_puzzle):
        if len(disk_puzzle)==1:
            x = WIDTH // 2
        else:
            if nn==0:
                x = WIDTH // 4
            elif nn==len(disk_puzzle)-1:
                x = WIDTH - WIDTH // 4
        y = DISK_Y
        disk_dict = {
            'name': puzzle, 'x': x, 'y': y,
            'target_rotation': 0, 'spline': [], 'animating': False
        }
        disk.update(disk_dict)
        if disk.get('rotation')==None:
            disk_dict = {'rotation': 0}
            disk.update(disk_dict)
        if disk.get('angle_shift')==None:
            disk_dict = {'angle_shift': 0}
            disk.update(disk_dict)
        if disk.get('colors')==None:
            disk_dict = {'colors': colors_mas.copy()}
            disk.update(disk_dict)

    DISK_ANGLE = reduce(gcd, DISK_SECTORS)  # НОД из списка
    if angle_shift: DISK_ANGLE = gcd(DISK_ANGLE,int(angle_shift))

    return disk_puzzle,DISK_ANGLE

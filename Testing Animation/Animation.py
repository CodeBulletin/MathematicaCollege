from numpy.core.records import array
import pygame.gfxdraw
import pygame.time
import pygame.surfarray
import pandas as pd
import sys, cv2, numpy, pygame

import ctypes
ctypes.windll.user32.SetProcessDPIAware()

pygame.init()

sq = min(pygame.display.Info().current_w, pygame.display.Info().current_h) * 2

size = (width, height) = (sq, sq)
print(size)
black = (0, 0, 0)
white = (255, 255, 255)
rd_rm = 100
rad_map = (min(width, height) - rd_rm) / 2
rd = 0.05
xDiff = width - min(width, height)
yDiff = height - min(width, height)
color1 = (int(255 * 1.0), int(255 * 0.7), int(255 * 0.29))
color2 = (int(255 * 0.0), int(255 * 0.86), int(255 * 0.9))
colorBG = (int(255 * 0.0), int(255 * 0.07), int(255 * 0.15))
tmax = 50
sec = 10

rd_map = rd * rad_map

screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()

dfs = pd.read_csv("C:/Users/bmalh/Desktop/Projects/Mathematica/Testing Animation/mfile.csv", header=None)
x1 = dfs[0].tolist()
y1 = dfs[1].tolist()
x2 = dfs[2].tolist()
y2 = dfs[3].tolist()

def intmapx(x):
    return int((-1 * x + 1) * rad_map + rd_rm / 2 + xDiff / 2)

def intmapy(y):
    return int((-1 * y + 1) * rad_map + rd_rm / 2 + yDiff / 2)

p1 = [(intmapx(i), intmapy(j)) for i, j in list(zip(x1, y1))]
p2 = [(intmapx(i), intmapy(j)) for i, j in list(zip(x2, y2))]

def drawCircle(surf, color, center, radius, width):
    pygame.draw.circle(surf, color, center, radius, width)

out = cv2.VideoWriter('outpy.avi',cv2.VideoWriter_fourcc(*'MJPG'), 144, size)

i = 0
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

    screen.fill(colorBG)

    pygame.draw.circle(screen, white, (int(width / 2), int(height / 2)), int(rad_map), 3)

    pygame.draw.lines(screen, color1, False,
        p1[max(0, i - sec * 144) : max(i, 2)],
        width = 4
    )

    pygame.draw.lines(screen, color2, False,
        p2[max(0, i - sec * 144) : max(i, 2)],
        width = 4
    )

    pygame.draw.circle(screen, color1, (intmapx(x1[i]), intmapy(y1[i])), int(rd_map), int(rd_map))
    pygame.draw.circle(screen, color2, (intmapx(x2[i]), intmapy(y2[i])), int(rd_map), int(rd_map))

    pygame.display.flip()
    Array = cv2.cvtColor(numpy.rot90(pygame.surfarray.pixels3d(screen), 3), cv2.COLOR_RGB2BGR)
    out.write(Array)
    i+=1
    i %= (tmax * 144)
    if i == 0:
        break

out.release()
import sys, pygame
from pygame.locals import *
import time
import pygame.time
import pygame.font
import collision

pygame.init()

clock = 0
pygame.font.init()
font = pygame.font.SysFont(None, 15)

size = width, height = 640, 480
screen = pygame.display.set_mode(size)

# shape = {'id': id, 'pos':[x,y], 'poly':[[x1,y1],[x2,y2],...]}

shapes = {}
large = 0

def shape_build(pos, pol):
    global shapes, large
    id = 0
    while id in shapes:
        id += 1
    large = max(large, id)
    
    shape = {}
    shape['id'] = id
    shape['pos'] = pos
    shape['poly'] = pol
    shapes[id] = shape

def shape_kill(id):
    global shapes
    shapes.pop(id)


def t_add(t1,t2):
    return map(lambda a,b: a+b,t1,t2)

shape_build((0, 100), [(0, 0)])
"""
shape_build((100,100),[(-20,-20),(20,-20),(20,20),(-20,20)])
shape_build((140,100),[(-20,-20),(20,-20),(20,20),(-20,20)])
shape_build((180,100),[(-20,-20),(20,-20),(20,20),(-20,20)])
shape_build((220,100),[(-20,-20),(20,-20),(20,20),(-20,20)])
shape_build((100,140),[(-20,-20),(20,-20),(20,20),(-20,20)])
shape_build((140,140),[(-20,-20),(20,-20),(20,20),(-20,20)])
shape_build((180,140),[(-20,-20),(20,-20),(20,20),(-20,20)])
shape_build((220,140),[(-20,-20),(20,-20),(20,20),(-20,20)])
"""
spawner = {}
spawner[2000] = [100,300]
spawner[3000] = [200]
spawner[4000] = [200,400,600]

print spawner
done = False
while not done:
    clock = pygame.time.get_ticks()
    m_pos = mx, my = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    d_key = []
    for k in spawner:
        if k <= clock:
            for x in spawner.get(k,[]):
                shape_build((x,100),[(-20,-20),(20,-20),(20,20),(-20,20)])
            d_key.append(k)
    for k in d_key:
        del spawner[k]

    screen.fill((0,0,0))

    shapes[0]['pos'] = m_pos

    for s in shapes.values():
        if len(s['poly']) > 1:
            t_s = s['poly'] + [s['poly'][0]]
            for i in range(len(s['poly'])):
                p1 = t_add(s['pos'],t_s[i])
                p2 = t_add(s['pos'],t_s[i+1])
                pygame.draw.line(screen, (150,255,150), p1, p2, 1)
        elif len(s['poly']) == 1:
             p1 = t_add(s['pos'],s['poly'][0])
             pygame.draw.line(screen, (200, 255, 200), p1, p1, 1)

    for k in shapes:
        if k > 0:
            shapes[k]['pos'] = t_add(shapes[k]['pos'],(0,3))

    kill_list = []
    for k in shapes:
        if k > 0 and shapes[k]['pos'][1] >= height*1.5:
            kill_list.append(k)
            print "kill: ", k
            continue
        for i in [i for i in range(k+1,large+1)if i in shapes]:
            c = collision.collide(shapes[k]['pos'],shapes[k]['poly'],shapes[i]['pos'],shapes[i]['poly'])
            if c:
                print k, i, c
                kill_list.append(i)
    for k in kill_list:
        shape_kill(k)


    text = font.render(str(clock/1000.0), True, (255,255,255))
    screen.blit(text, (0,0))
    

    pygame.display.flip()
    time.sleep(0.02)

pygame.quit()

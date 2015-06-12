import sys, pygame
from pygame.locals import *
import time

size = width, height = 640, 480
screen = pygame.display.set_mode(size)

shapes = []

shapes.append(((50,50),((0,0),(50,0),(50,50),(0,50))))

shapes.append(((100,75),((0,50),(50,50),(25,0))))

def t_add(t1,t2):
    return map(lambda a,b: a+b,t1,t2)

def collide(s1, s2):
    t_s1 = s1[1] + (s1[1][0],)
    t_s2 = s2[1] + (s2[1][0],)
    col = False
    for i in range(len(s1[1])):
        for j in range(len(s2[1])):
            a = t_add(t_s1[i],s1[0])
            b = t_add(t_s1[i+1],s1[0])
            c = t_add(t_s2[j],s2[0])
            d = t_add(t_s2[j+1],s2[0])
            #print a, b, c, d
            p = intersect(a,b,c,d)
            #print p
            if p:
                col = True
                break
        if col:
            break
    return col

def intersect(a,b,c,d):
    min1x = min(a[0],b[0])
    min1y = min(a[1],b[1])
    max1x = max(a[0],b[0])
    max1y = max(a[1],b[1])

    min2x = min(c[0],d[0])
    min2y = min(c[1],d[1])
    max2x = max(c[0],d[0])
    max2y = max(c[1],d[1])

    #print min1x, max2x
    if min1x > max2x or min2x > max1x or min1y > max2y or min2y > max2y:
        return None

    x1 = max(min1x, min2x)
    x2 = min(max1x, max2x)
    y1 = max(min1y, min2y)
    y2 = min(max1y, max2y)

    
    
    de = (a[0]-b[0])*(c[1]-d[1]) - (a[1]-b[1])*(c[0]-d[0])
    if de == 0:
        return None

    nx = (a[0]*b[1]-a[1]*b[0])*(c[0]-d[0]) - (a[0]-b[0])*(c[0]*d[1]-c[1]*d[0])
    ny = (a[0]*b[1]-a[1]*b[0])*(c[1]-d[1]) - (a[1]-b[1])*(c[0]*d[1]-c[1]*d[0])

    px = float(nx)/float(de)
    py = float(ny)/float(de)
    if x1 <= px <= x2 and y1 <= py <= y2:
        return (px, py)
    return None

"""
a1 = (50,100)
a2 = (100,100)
b1 = (75,125)
b2 = (100,75)
print intersect(a1,a2,b1,b2)
"""
done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0,0,0))


    for s in shapes:
        t_s = s[1] + (s[1][0],)
        for i in range(len(s[1])):
            p1 = t_add(s[0],t_s[i])
            p2 = t_add(s[0],t_s[i+1])
            pygame.draw.line(screen, (100,255,0), p1, p2, 1)

    #pygame.draw.line(screen,(100,255,0),a1,a2,1)
    #pygame.draw.line(screen,(255,100,0),b1,b2,1)
    print collide(shapes[0],shapes[1])
    shapes[1] = ((shapes[1][0][0]-1, shapes[1][0][1]),shapes[1][1])

    pygame.display.flip()
    time.sleep(0.01)

pygame.quit()

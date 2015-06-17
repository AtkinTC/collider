import sys, pygame
from pygame.locals import *
import time

size = width, height = 640, 480
screen = pygame.display.set_mode(size)

shapes = []

shapes.append(((300,100),((-50,-50),(50,-50),(50,50),(-50,50))))

#shapes.append(((200,100),((-25, 25),(25,25),(0,-25))))

#shapes.append(((100, 100), ((-20, 0), (20, 0))))

shapes.append(((225, 100), ((0, 0),)))

def t_add(t1,t2):
    return map(lambda a,b: a+b,t1,t2)

def collide(s1, s2):
    if len(s1[1]) < 1 or len(s2[1]) < 1:
        return False
    if len(s1[1]) > len(s2[1]):
        st = s1
        s1 = s2
        s2 = st
    if len(s1[1]) > 1:
        return collide_pol2pol(s1, s2)
    elif len(s2[1]) > 1:
        return collide_pnt2pol(s1, s2)
    else:
        return collide_pnt2pnt(s1, s2)

def collide_pnt2pol(s1, s2):
    t_s = s2[1] + (s2[1][0],)

    c = t_add(s1[0],s1[1][0])
    d = (c[0]+1, c[1])

    count = 0

    for i in range(len(s2[1])):
        a = t_add(t_s[i],s2[0])
        b = t_add(t_s[i+1],s2[0])
        p = intersect_bound(a,b,c,d, rb=False)
        if p:
            count += 1

    if (count%2)==1:
        return c
    else:
        return False
        
    

def collide_pol2pol(s1, s2):
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
            p = intersect_bound(a,b,c,d)
            #print p
            if p:
                return p
                #col = True
                #break
        #if col:
            #break
    return col

def intersect_bound(a,b,c,d, lb=True, rb=True, ub=True, bb=True):
    min1x = min(a[0],b[0])
    min1y = min(a[1],b[1])
    max1x = max(a[0],b[0])
    max1y = max(a[1],b[1])

    min2x = min(c[0],d[0])
    min2y = min(c[1],d[1])
    max2x = max(c[0],d[0])
    max2y = max(c[1],d[1])

    #print min1x, max2x
    #if min1x > max2x or min2x > max1x or min1y > max2y or min2y > max2y:
    #    return None

    x1 = max(min1x, min2x)
    x2 = min(max1x, max2x)
    y1 = max(min1y, min2y)
    y2 = min(max1y, max2y)

    p = intersect(a,b,c,d)
    if p:
        px, py = p
    else:
        return None
    
    if not lb:
        x1 = px
    if not rb:
        x2 = px
    if not ub:
        y1 = py
    if not bb:
        y2 = py

    if x1 <= px <= x2 and y1 <= py <= y2:
        #print px, py
        return (px, py)
    return None


def intersect(a,b,c,d):
    de = (a[0]-b[0])*(c[1]-d[1]) - (a[1]-b[1])*(c[0]-d[0])
    if de == 0:
        return None

    nx = (a[0]*b[1]-a[1]*b[0])*(c[0]-d[0]) - (a[0]-b[0])*(c[0]*d[1]-c[1]*d[0])
    ny = (a[0]*b[1]-a[1]*b[0])*(c[1]-d[1]) - (a[1]-b[1])*(c[0]*d[1]-c[1]*d[0])

    px = float(nx)/float(de)
    py = float(ny)/float(de)

    return (px, py)
    


done = False
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    screen.fill((0,0,0))

    for s in shapes:
        if len(s[1]) > 1:
            t_s = s[1] + (s[1][0],)
            for i in range(len(s[1])):
                p1 = t_add(s[0],t_s[i])
                p2 = t_add(s[0],t_s[i+1])
                pygame.draw.line(screen, (100,255,0), p1, p2, 1)
        elif len(s[1]) == 1:
             p1 = t_add(s[0],s[1][0])
             pygame.draw.line(screen, (100, 255, 0), p1, p1, 1)

    c = collide(shapes[0],shapes[1])
    if c:
        print c
    shapes[1] = ((shapes[1][0][0]+1, shapes[1][0][1]),shapes[1][1])

    pygame.display.flip()
    time.sleep(0.02)

pygame.quit()

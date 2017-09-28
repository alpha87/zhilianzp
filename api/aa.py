#!/usr/bin/env python
# -*- coding: utf-8 -*-


a = [11,2,3,4,5,6,7,8,9,0]

def A():
    for b in a:
        b = b+1
        yield b

def c():
    box = list()
    for d in a:
        d = d+1
        box.append(d)
    return box

q = A()
for ww in q:
    ff = ww+1
    print(ff)
print("*******************************")
p = c()
print(p)
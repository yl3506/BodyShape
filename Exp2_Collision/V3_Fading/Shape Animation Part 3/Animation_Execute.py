import Animations
import random
import string
import pygame

def loop():
    timeStamps=[3500,3700,3900,4100,4300]
    shapes=["aConcave","aConvex","bConcaveP","bConvex","cConcave","cConvex","dConcave","dConvex","eConcave","eConvex","fConcave","fConvex","gConcave","gConvex","hConcave","hConvex"]
    groundTruth=[4100,4100,4217,4217,4000,4000,4067,4067,4233,4233,3717,3717,4017,4017,3850,3850]
    nameString=["".join(random.choice(string.ascii_lowercase) for i in range(10)) for i in range(96)]
    nameCounter=0
    for items in timeStamps:
        for i in range(16):
            nameString[nameCounter]=Animations.Animations("bConcave",shapes[i],(1500,400),False)
            nameString[nameCounter].withoutCurtain(items,groundTruth[i])
            nameCounter+=1
            pygame.quit()
            
loop()
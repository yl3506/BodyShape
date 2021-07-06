import pygame
import sys
import numpy as np
import math
import Translator as tr
import random
import pygame.gfxdraw

class Shape(object):
    ## define a shape, where coordinates is a list, displayPara is a tuple that
    ## used to scale the object, and every other attributes that a shape
    ## possesses, displayPara in form (width,height)
    def __init__(self,coordinates,displayPara,initialY,angle,spatialGap,proper,code,flip,center,x,y):
        self.coordinates=coordinates
        self.displayPara=displayPara
        self.initialY=initialY
        self.angle=angle
        self.spatialGap=spatialGap
        self.color=pygame.Color(0,0,0)
        self.alpha=100
        self.a=360*random.random()
        self.color.hsla=(self.a,70,70,self.alpha)
        self.property=proper
        self.code=code
        self.flip=flip
        self.center=center
        self.surface=None
        self.x=x
        self.y=y

    def movingLength(self):
        return math.floor(abs(self.center[0]-self.displayPara[0]/2)),math.floor(abs(self.center[1]-
        self.initialY))
    
    def adjustPosition(self,timeStamp=0,gt=0):
        tempList=[]
        tempList=[]
        for i in self.coordinates:
            tempList.append(tuple(i))
        self.coordinates=tr.rotate_contour(tempList,self.angle)
        self.center=tr.contour_centroid(self.coordinates)
        xPosition=0
        # Four conditions: 1: patient and convex, 2: patient and concave, 3: agent
        if timeStamp != 0:
            xPosition=self.x+math.floor(((timeStamp-gt)/16.6666666667)*2.8)
        else:
            xPosition=self.x
        if self.property=="patient":
            movingLengthX,movingLengthY=self.movingLength()
            for i in range(len(self.coordinates)):
                self.coordinates[i]=(movingLengthX+self.coordinates[i][0]+xPosition,
                                     movingLengthY+self.coordinates[i][1]+self.y)
            
        else:
            movingLengthX,movingLengthY=self.movingLength()
            for i in range(len(self.coordinates)):
                self.coordinates[i]=(self.coordinates[i][0]+90,movingLengthY+
                                     self.coordinates[i][1]+15)#+20 if not square # -20 if square and agent
        self.coordinates=tr.scale_contour(self.coordinates,2)
        if(self.property=="patient"):
            print(self.coordinates)

    def move(self,velocity):
        for i in range(len(self.coordinates)):
            x=self.coordinates[i][0]+velocity
            y=self.coordinates[i][1]
            self.coordinates[i]=(x,y)
        #self.center=tr.contour_centroid(self.coordinates)
        
    ## Individual draw function for shape, where you are asked to input
    ## a pygame display for drawing.
    def draw(self,canvas):
        self.color.hsla=(self.a,70,70,self.alpha)
        #pygame.gfxdraw.polygon(canvas,self.coordinates,self.color)
        pygame.gfxdraw.filled_polygon(canvas,self.coordinates,self.color)
        #pygame.draw.polygon(canvas,self.color,self.coordinates)
        
def testing():
    pygame.init()
    gameDisplay=pygame.display.set_mode((1000,400))
    gameDisplay.fill((255,255,255))
    aConcave=Shape([[104,20],[42,80],[23,125],[127,117],[85,107],[104,98]],
            (1000,400),230,3.141592653589793,88,"patient","AConcave",False,(1000/2,230))
    aConvex=Shape([[41,23],[46,102],[66,110],[23,119],[127,125],[105,81]],
            (1000,400),230,3.141592653589793,107,"patient","AConvex",False,(1000/2,230))
    bConvex=Shape([[59,14],[95,24],[106,79],[45,136],[44,82],[52,94],[56,70],[48,43]],
            (1000,400),240,3.9269908169872414,94,"patient","BConvex",True,(1000/2,200))
    bConcave=Shape([[96,12],[59,18],[43,75],[101,137],[105,82],[96,94],[93,72],[105,40]],
                   (1000,400),250,-math.pi/1.7,79,"agent","BConcave",False,(1000/2,250))
    cConcave=Shape([[42,20],[45,114],[105,130],[71,97],[83,82],[107,78],[83,40],[66,24]],
                   (1000,400),235,3.4243359924128747,85,"patient","CConcave",False,
                   (1000/2,235))
    cConvex=Shape([[105,19],[80,23],[68,36],[43,77],[65,81],[79,96],[47,130],[106,112]],
                  (1000,400),230,3.141592653589793,87,"patient","CConvex",False,
                  (1000/2,230))
    dConvex=Shape([[108,25],[35,54],[38,123],[49,106],[81,119],[110,119],[105,109],[113,109],[99,96],
                   [66,86],[115,91],[54,63]],(1000,400),235,0,96,"patient","DConvex",
                  True,(1000/2,235))
    dConcave=Shape([[40,28],[113,55],[113,122],[102,106],[70,119],[41,119],[45,110],[38,109],[49,98],[81,85],[35,89],[92,64]]
                   ,(1000,400),240,0.21991148575128555,85,"patient","DConcave",True,(1000/2,240))
    eConcave=Shape([[34,33],[105,25],[98,82],[116,47],[91,122],[63,42],[44,109],[50,100],[47,123],[35,119]],
                   (1000,400),215,4.743804906920587,106,"patient","EConcave",False,(1000/2,215))
    eConvex=Shape([[43,27],[113,32],[117,117],[105,123],[80,98],[108,109],[84,42],[61,123],[33,51],[51,82]],
                  (1000,400),230,1.5707963267948966,99,"patient","EConvex",False,(1000/2,230))
    fConcave=Shape([[54,22],[112,37],[111,14],[119,20],[119,80],[100,122],[53,135],[41,120],[91,51],[80,54],[38,99],[30,91],[60,60],[33,60],[36,39]],
                   (1000,400),215,0,99,"patient","FConcave",False,(1000/2,215))
    fConvex=Shape([[30,20],[39,14],[39,38],[94,21],[115,39],[117,59],[91,59],[121,90],[113,97],[71,56],[59,50],[110,120],[98,134],[51,122],[31,81]],
                  (1000,400),230,0,105,"patient","FConvex",False,(1000/2,230))
    gConvex=Shape([[15,104],[38,82],[57,31],[69,56],[66,23],[92,28],[87,58],[117,38],[127,54],[34,99],[126,106],[135,117],[45,114],[35,128]],
                  (1000,400),210,-0.6283185307179586,124,"patient","gConvex",True,(1000/2,210))
    gConcave=Shape([[15,104],[38,82],[57,31],[69,56],[66,23],[92,28],[87,58],[117,38],[127,54],[34,99],[126,106],[135,117],[45,114],[35,128]],
                   (1000,400),215,-2.9845130209103035,93,"patient","gConcave",True,(1000/2,215))## Problem
    hConvex=Shape([[28,26],[33,44],[101,27],[69,51],[49,56],[57,67],[45,74],[51,80],[24,82],[30,118],[52,93],[75,114],[77,104],[82,137],[90,97],[127,112],[119,48],[104,48],[127,18],[84,14]],
                  (1000,400),225,1.5707963267948966,115,"patient","hConvex",False,(1000/2,225))
    hConcave=Shape([[27,15],[75,15],[127,29],[119,47],[55,26],[78,49],[102,58],[95,67],[107,77],[101,82],[126,88],[119,122],[99,95],[74,114],[72,104],[64,136],[59,95],[24,111],[34,44],[47,44]],
                   (1000,400),215,3.141592653589793,96,"patient","hConcave",False,(1000/2,215))
    squareA=Shape([[10,70],[80,70],[80,140],[10,140]],
               (1500,400),215,0,96,"agent","squareA",False,(1000/2,215))
    squareP=Shape([[10,70],[80,70],[80,140],[10,140]],
               (1500,400),215,0,96,"patient","squareP",False,(1000/2,215))
    
    #squareA.adjustPosition()
    while True:
        squareA.draw(gameDisplay)
        pygame.display.update()
    #bConvex.create(gameDisplay)
    #bConcave.create(gameDisplay)
    pygame.display.update()

##testing()


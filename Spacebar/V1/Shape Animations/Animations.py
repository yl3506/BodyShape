import pygame
import sys
import numpy as np
import Shape
import math
import cv2
import numpy as np
import io
from PIL import Image
from datetime import datetime
import time
import multiprocessing 



##Global Params for the hardcoded shapes,calibration needed.
aConcave=Shape.Shape([[104,20],[42,80],[23,125],[127,117],[85,107],[104,98]],
            (1500,400),230,-3.1415926,88,"patient","AConcave",False,(1000/2,230))
aConcaveAgent=Shape.Shape([[104,20],[42,80],[23,125],[127,117],[85,107],[104,98]],
            (1500,400),230,-3.1415926,88,"agent","AConcave",False,(1000/2,230))
aConvex=Shape.Shape([[41,23],[46,102],[66,110],[23,119],[127,125],[105,81]],
            (1500,400),230,-3.1415926,107,"patient","AConvex",False,(1000/2,230))
bConvex=Shape.Shape([[59,14],[95,24],[106,79],[45,136],[44,82],[52,94],[56,70],[48,43]],
            (1500,400),240,-3.9269908169872414,94,"patient","BConvex",True,(1000/2,200))
bConcave=Shape.Shape([[96,12],[59,18],[43,75],[101,137],[105,82],[96,94],[93,72],[105,40]],
                   (1500,400),250,-math.pi/1.7,79,"agent","BConcave",False,(0,250))
bConcavePatient=Shape.Shape([[96,12],[59,18],[43,75],[101,137],[105,82],[96,94],[93,72],[105,40]],
                   (1500,400),250,math.pi*0.95,79,"patient","BConcavePatient",False,(0,250))
cConcave=Shape.Shape([[42,20],[45,114],[105,130],[71,97],[83,82],[107,78],[83,40],[66,24]],
                   (1500,400),235,(-3.4243359924128747)*1,85,"patient","CConcave",False,
                   (1000/2,235))
cConvex=Shape.Shape([[105,19],[80,23],[68,36],[43,77],[65,81],[79,96],[47,130],[106,112]],
                  (1500,400),230,-3.141592653589793,87,"patient","CConvex",False,
                  (1000/2,230))
dConvex=Shape.Shape([[108,25],[35,54],[38,123],[49,106],[81,119],[110,119],[105,109],[113,109],[99,96],
                   [66,86],[115,91],[54,63]],(1500,400),235,math.pi*1.6,96,"patient","DConvex",
                  True,(1000/2,235))
dConcave=Shape.Shape([[40,28],[113,55],[113,122],[102,106],[70,119],[41,119],[45,110],[38,109],[49,98],[81,85],[35,89],[92,64]]
               ,(1500,400),240,(-0.21991148575128555),85,"patient","DConcave",True,(1000/2,240))
eConcave=Shape.Shape([[34,33],[105,25],[98,82],[116,47],[91,122],[63,42],[44,109],[72,96],[47,123],[35,119]],
               (1500,400),215,-4.743804906920587*1.04,106,"patient","EConcave",False,(1000/2,215))
eConvex=Shape.Shape([[43,27],[113,32],[117,117],[105,123],[80,98],[108,109],[84,42],[61,123],[33,51],[51,82]],
              (1500,400),230,-1.5707963267948966,99,"patient","EConvex",False,(1000/2,230))
fConcave=Shape.Shape([[54,22],[112,37],[111,14],[119,20],[119,80],[100,122],[53,135],[41,120],[91,51],[80,54],[38,99],[30,91],[60,60],[33,60],[36,39]],
               (1500,400),215,-3.1415926/2,99,"patient","FConcave",False,(1000/2,215))
fConvex=Shape.Shape([[30,20],[39,14],[39,38],[94,21],[115,39],[117,59],[91,59],[121,90],[113,97],[71,56],[59,50],[110,120],[98,134],[51,122],[31,81]],
              (1500,400),230,0,105,"patient","FConvex",False,(1000/2,230))
gConvex=Shape.Shape([[15,104],[38,82],[57,31],[69,56],[66,23],[92,28],[87,58],[117,38],[127,54],[34,99],[126,106],[135,117],[45,114],[35,128]],
              (1500,400),210,0.6283185307179586*1.1,124,"patient","gConvex",True,(1000/2,210))
gConcave=Shape.Shape([[15,104],[38,82],[57,31],[69,56],[66,23],[92,28],[87,58],[117,38],[127,54],[34,99],[126,106],[135,117],[45,114],[35,128]],
               (1500,400),215,2.9845130209103035*0.9,93,"patient","gConcave",True,(1000/2,215))## Problem
hConvex=Shape.Shape([[28,26],[33,44],[101,27],[69,51],[49,56],[57,67],[45,74],[51,80],[24,82],[30,118],[52,93],[75,114],[77,104],[82,137],[90,97],[127,112],[119,48],[104,48],[127,18],[84,14]],
              (1500,400),225,-1.5707963267948966,115,"patient","hConvex",False,(1000/2,225))
hConcave=Shape.Shape([[27,15],[75,15],[127,29],[119,47],[55,26],[78,49],[102,58],[95,67],[107,77],[101,82],[126,88],[119,122],[99,95],[74,114],[72,104],[64,136],[59,95],[24,111],[34,44],[47,44]],
               (1500,400),215,-3.141592653589793*1.5,96,"patient","hConcave",False,(1000/2,215))
squareA=Shape.Shape([[10,70],[80,70],[80,140],[10,140]],
               (1500,400),215,0,96,"agent","squareA",False,(1000/2,215))
squareP=Shape.Shape([[10,70],[80,70],[80,140],[10,140]],
               (1500,400),215,0,96,"patient","squareP",False,(1000/2,215))
    
#make a dictionary of shapes.
shape={"squareA":squareA,"squareP":squareP,"aConcave":aConcave,"aConcaveAgent":aConcaveAgent,"aConvex":aConvex,
       "bConvex":bConvex,"bConcave":bConcave,"bConcaveP":bConcavePatient,"cConcave":cConcave,"cConvex":cConvex,
       "dConvex":dConvex,"dConcave":dConcave,"eConcave":eConcave,"eConvex":eConvex,"fConcave":fConcave,"fConvex":fConvex,
       "gConvex":gConvex,"gConcave":gConcave,"hConvex":hConvex,"hConcave":hConcave}


def adjustPosition(self):
        tempList=[]
        tempList=[]
        for i in self.coordinates:
            tempList.append(tuple(i))
        self.coordinates=tr.rotate_contour(tempList,self.angle)
        self.center=tr.contour_centroid(self.coordinates)
        if self.property=="patient":
            movingLengthX,movingLengthY=self.movingLength()
            for i in range(len(self.coordinates)):
                self.coordinates[i]=(movingLengthX+self.coordinates[i][0],#-50 if not square # -75 if bconcaveP #-30 if fConcave #0 if gConvex #-30 if hConcave #0 if hConvex
                                     movingLengthY+self.coordinates[i][1]-50)#-40 if bConcaveP
        else:
            movingLengthX,movingLengthY=self.movingLength()
            for i in range(len(self.coordinates)):
                self.coordinates[i]=(self.coordinates[i][0]+90,movingLengthY+
                                     self.coordinates[i][1]+10)#+20 if not square
        self.coordinates=tr.scale_contour(self.coordinates,2)

class Animations(object):
    def __init__(self,agent,patient,resolution,flip):
        self.agent=shape[agent]
        self.patient=shape[patient]
        self.resolution=resolution
        self.flip=flip
        self.surfaceWidth=0
        self.surfaceHeight=0

    def findSize(self):
        x=[p[0] for p in self.patient.coordinates]
        tempList=np.array(x)
        maximumX=np.max(tempList)
        minimumX=np.min(tempList)
        y=[p[1] for p in self.patient.coordinates]
        tempList=np.array(y)
        maximumY=np.max(tempList)
        minimumY=np.min(tempList)
        self.surfaceWidth=maximumX-minimumX
        self.surfaceHeight=maximumY-minimumY

    def animateSave(self):
        pygame.init()
        self.gameDisplay=pygame.display.set_mode(self.resolution)
        self.gameDisplay.fill((0,0,0))
        clock=pygame.time.Clock()
        currentY=-340
        self.findSize()
        self.agent.adjustPosition()
        self.patient.adjustPosition()
        blackSurface=pygame.Surface((800,370))
        blackSurface.fill((255,255,255))
        pixelArray=[]
        startTime=0
        fps=60
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Press the Spacebar to Start the Video!', True, (255,0,0), (0,0,0))
        textRect = text.get_rect()
        textRect.center = (self.resolution[0] // 2, self.resolution[1] // 2)
        nowText = font.render("COLLIDING!", True, (255,0,0), (0,0,0))
        nowTextRect = text.get_rect()
        nowTextRect.center = (self.resolution[0]//2, self.resolution[1]//4)
        currentTime=time.time_ns()
        cumulatingTime=currentTime
        while cumulatingTime-currentTime<=9000000000:
            pixelArr=pygame.image.tostring(self.gameDisplay,"RGB")
            pixelArray.append(pixelArr)
            self.gameDisplay.fill((0,0,0))
            self.agent.draw(self.gameDisplay)
            self.patient.draw(self.gameDisplay)
            #90
            self.gameDisplay.blit(blackSurface,(self.patient.center[0]+self.patient.displayPara[0]/5-20,currentY))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if cumulatingTime-currentTime<200000000+16666667:
                self.gameDisplay.fill((0,0,0))
                self.gameDisplay.blit(text, textRect)
            if cumulatingTime-currentTime>=1600000000:
                self.agent.move(1)
            #if cumulatingTime-currentTime >= 7000000000:
                #self.gameDisplay.blit(nowText,nowTextRect)
                #if self.agent.center[0]>=380 and self.agent.center[0]<=381:
                    #pygame.image.save(self.gameDisplay,"S"+str(self.agent.code)+"."+str(self.patient.code)+".jpg")
            if cumulatingTime-currentTime>=1200000000:
                if cumulatingTime-currentTime<=1600000000:
                    self.gameDisplay.blit(blackSurface,(self.patient.center[0]+self.patient.displayPara[0]/5-20,currentY))
                    currentY+=830/(fps*0.94)
                if cumulatingTime-currentTime>=1600000000:
                    self.gameDisplay.blit(blackSurface,(self.patient.center[0]+self.patient.displayPara[0]/5-20,currentY))
            #pygame.image.save(self.gameDisplay,"S"+str(pygame.time.get_ticks())+".jpg")
            pygame.display.update()
            cumulatingTime+=16666667


        resolutions=(1500,400)
        codec=fourcc = cv2.VideoWriter_fourcc(*'H264')
        filename=self.agent.code+"+"+self.patient.code+".mp4"
        ##FPS=frames/videoLength
        #fps=len(pixelArray)/15
        print(len(pixelArray))
        pixelArray.pop(0)
        fps=60
        out=cv2.VideoWriter(filename,codec,fps,resolutions)
        for i in pixelArray:
            image=Image.frombytes("RGB",resolutions,i,"raw")
            frame=np.array(image)
            temp=cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
            out.write(temp)
        pygame.quit()
        out.release()



#a=Animations("bConcave","gConcave",(1000,400),False)
a=Animations("aConcaveAgent","hConcave",(1500,400),False)
a.animateSave()


        

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
aConcave=Shape.Shape([[104,20],[42,80],[23,125],[127,125],[60,95],[95,60]],
            (1500,400),230,-3.1415926,88,"patient","AConcave",False,(1000/2,230),-80,-20)
aConcaveAgent=Shape.Shape([[104,50],[70,80],[23,125],[127,125],[85,107],[104,98]],
            (1500,400),230,-3.1415926,88,"agent","AConcave",False,(1000/2,230),0,-20)
aConvex=Shape.Shape([[41,23],[50,60],[86,95],[23,119],[127,125],[105,81]],
            (1500,400),230,-3.1415926,107,"patient","AConvex",False,(1000/2,230),3,10)
bConvex=Shape.Shape([[69,20],[95,24],[106,79],[45,136],[44,82],[60,90],[90,70],[73,35]],
            (1500,400),240,-3.9269908169872414,94,"patient","BConvex",True,(1000/2,200),-21,-50)
bConcave=Shape.Shape([[53,39],[43,80],[101,137],[105,82],[96,94],[93,72],[96,40]],
                   (1500,400),250,-math.pi/1.7,79,"agent","BConcave",False,(0,250),-80,-40)
bConcavePatient=Shape.Shape([[86,12],[59,18],[33,75],[101,137],[115,87],[96,94],[57,65],[80,30]],
                   (1500,400),250,math.pi,79,"patient","BConcavePatient",False,(0,250),-80,-95)
cConcave=Shape.Shape([[42,20],[45,114],[105,130],[61,97],[73,82],[86,70],[83,40],[66,24]],
                   (1500,400),235,(-3.4243359924128747)*1,85,"patient","CConcave",False,
                   (1000/2,235),-80,-10)
cConvex=Shape.Shape([[105,19],[80,23],[68,36],[65,70],[80,80],[90,100],[47,130],[106,112]],
                  (1500,400),230,-3.141592653589793,87,"patient","CConvex",False,
                  (1000/2,230),-67,17)
dConvex=Shape.Shape([[108,15],[35,54],[38,123],[49,106],[81,119],[110,119],[105,109],[113,109],[99,96],
                   [66,86],[97,83],[54,63]],(1500,400),235,math.pi*1.6,96,"patient","DConvex",
                  True,(1000/2,235),6,10)
dConcave=Shape.Shape([[40,18],[113,55],[113,122],[102,106],[70,119],[41,119],[45,110],[38,109],[49,98],[81,85],[50,89],[93,64]]
               ,(1500,400),240,(-0.21991148575128555),85,"patient","DConcave",True,(1000/2,240),-80,5)
eConcave=Shape.Shape([[34,33],[105,25],[98,44],[116,37],[98,55],[63,42],[44,109],[50,100],[47,120],[35,119]],
               (1500,400),215,-4.743804906920587*0.98,106,"patient","EConcave",False,(1000/2,215),-80,-55)
eConvex=Shape.Shape([[43,27],[113,32],[117,117],[105,123],[100,100],[108,109],[84,42],[55,60],[43,40],[55,40]],
              (1500,400),230,-1.5707963267948966,99,"patient","EConvex",False,(1000/2,230),-8,-20)
fConcave=Shape.Shape([[54,42],[112,57],[111,4],[119,10],[119,80],[100,122],[53,135],[41,120] ,[91,61],[80,64],[38,99],[30,91],[60,70],[33,70],[36,49]],
               (1500,400),215,-3.1415926/2,99,"patient","FConcave",False,(1000/2,215),-80,-15)
fConvex=Shape.Shape([[30,20],[39,14],[39,50],[94,33],[115,39],[117,59],[91,59],[125,95],[113,97],[71,60],[59,62],[110,120],[98,134],[51,122],[31,81]],
              (1500,400),230,0,105,"patient","FConvex",False,(1000/2,230),-60,10)
gConvex=Shape.Shape([[15,104],[38,82],[54,31],[59,56],[60,23],[72,28],[67,58],[80,34],[83,50],[60,100],[126,116],[135,127],[45,114],[35,128]],
              (1500,400),210,0.6283185307179586*1.1,124,"patient","gConvex",True,(1000/2,210),-1,5)
gConcave=Shape.Shape([[15,104],[38,82],[54,31],[59,56],[60,23],[72,28],[67,58],[80,34],[83,50],[60,100],[126,116],[135,127],[45,114],[35,128]],
               (1500,400),215,2.9845130209103035*1.05,93,"patient","gConcave",True,(1000/2,215),-80,-30)## Problem
hConvex=Shape.Shape([[55,20],[60,32],[101,27],[79,51],[59,56],[67,67],[55,74],[61,95],[24,105],[30,118],[52,108],[75,114],[77,104],[82,137],[90,97],[127,112],[119,48],[104,48],[127,18],[84,14]],
              (1500,400),225,-1.5707963267948966,115,"patient","hConvex",False,(1000/2,225),-17,-20)
hConcave=Shape.Shape([[27,15],[75,15],[100,20],[90,30],[55,26],[70,49],[90,58],[85,67],[97,77],[91,92],[136,110],[119,122],[99,105],[74,114],[72,104],[64,136],[59,95],[24,111],[34,44],[47,44]],
               (1500,400),215,-3.141592653589793,96,"patient","hConcave",False,(1000/2,215),-80,-20)
squareA=Shape.Shape([[10,70],[80,70],[80,140],[10,140]],
               (1500,400),215,0,96,"agent","squareA",False,(1000/2,215),0,0)
squareP=Shape.Shape([[10,70],[80,70],[80,140],[10,140]],
               (1500,400),215,0,96,"patient","squareP",False,(1000/2,215),0,0)
    
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

    def animateSave(self,current,groundTruth):
        pygame.init()
        self.gameDisplay=pygame.display.set_mode(self.resolution)
        self.gameDisplay.fill((0,0,0))
        clock=pygame.time.Clock()
        currentY=-340
        self.findSize()
        self.agent.adjustPosition()
        self.patient.adjustPosition(timeStamp=current,gt=groundTruth)
        blackSurface=pygame.Surface((800,370))
        blackSurface.fill((255,255,255))
        pixelArray=[]
        startTime=0
        fps=60
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Press the Spacebar to Start the Video!', True, (255,0,0), (0,0,0))
        text = pygame.transform.flip(text,True,False)
        textRect = text.get_rect()
        textRect.center = (self.resolution[0] // 2, self.resolution[1] // 2)
        nowText = font.render("COLLIDING!", True, (255,0,0), (0,0,0))
        nowTextRect = text.get_rect()
        nowTextRect.center = (self.resolution[0]//2, self.resolution[1]//4)
        currentTime=time.time_ns()
        cumulatingTime=currentTime
        while cumulatingTime-currentTime<=4500000000:
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
                self.agent.move(2.8)
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
        filename=self.agent.code+"+"+self.patient.code+" "+str(current)+".mp4"
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
    def withoutCurtain(self,current,groundTruth):
        pygame.init()
        self.gameDisplay=pygame.display.set_mode(self.resolution)
        self.gameDisplay.fill((0,0,0))
        clock=pygame.time.Clock()
        currentY=-340
        self.findSize()
        self.agent.adjustPosition()
        self.patient.adjustPosition(timeStamp=current,gt=groundTruth)
        blackSurface=pygame.Surface((800,370))
        blackSurface.fill((255,255,255))
        pixelArray=[]
        startTime=0
        fps=60
        font = pygame.font.Font('freesansbold.ttf', 32)
        text = font.render('Press the Spacebar to Start the Video!', True, (255,0,0), (0,0,0))
        text = pygame.transform.flip(text,True,False)
        textRect = text.get_rect()
        textRect.center = (self.resolution[0] // 2, self.resolution[1] // 2)
        nowText = font.render("COLLIDING!", True, (255,0,0), (0,0,0))
        nowTextRect = text.get_rect()
        nowTextRect.center = (self.resolution[0]//2, self.resolution[1]//4)
        currentTime=time.time_ns()
        cumulatingTime=currentTime
        while cumulatingTime-currentTime<=4500000000:
            pixelArr=pygame.image.tostring(self.gameDisplay,"RGB")
            pixelArray.append(pixelArr)
            self.gameDisplay.fill((0,0,0))
            self.agent.draw(self.gameDisplay)
            self.patient.draw(self.gameDisplay)
            #90
            #self.gameDisplay.blit(blackSurface,(self.patient.center[0]+self.patient.displayPara[0]/5-20,currentY))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            if cumulatingTime-currentTime<200000000+16666667:
                self.gameDisplay.fill((0,0,0))
                self.gameDisplay.blit(text, textRect)
            if cumulatingTime-currentTime>=1600000000:
                self.agent.move(2.8)
            #if cumulatingTime-currentTime >= 7000000000:
                #self.gameDisplay.blit(nowText,nowTextRect)
                #if self.agent.center[0]>=380 and self.agent.center[0]<=381:
                    #pygame.image.save(self.gameDisplay,"S"+str(self.agent.code)+"."+str(self.patient.code)+".jpg")
           # if cumulatingTime-currentTime>=1200000000:
                #if cumulatingTime-currentTime<=1600000000:
                    #self.gameDisplay.blit(blackSurface,(self.patient.center[0]+self.patient.displayPara[0]/5-20,currentY))
                    #currentY+=830/(fps*0.94)
                #if cumulatingTime-currentTime>=1600000000:
                    #self.gameDisplay.blit(blackSurface,(self.patient.center[0]+self.patient.displayPara[0]/5-20,currentY))
            #pygame.image.save(self.gameDisplay,"S"+str(pygame.time.get_ticks())+".jpg")
            pygame.display.update()
            cumulatingTime+=16666667


        resolutions=(1500,400)
        codec=fourcc = cv2.VideoWriter_fourcc(*'H264')
        filename=self.agent.code+"+"+self.patient.code+" "+str(current)+".mp4"
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



a=Animations("aConcaveAgent","hConvex",(1500,400),False)
#a.withoutCurtain(3700,3683)
a.animateSave(3500,3683)


        

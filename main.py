import cv2
from cvzone.HandTrackingModule import HandDetector
import time

# Webcam default 0
cap=cv2.VideoCapture(0)

cap.set(3,1280) #width
cap.set(4,720)  #height

detector = HandDetector(detectionCon=0.8, maxHands=1)
#button class
class Button:
    def __init__(self,pos,width,height,value):
        self.pos=pos
        self.width=width
        self.height=height
        self.value=value
    def draw(self,img):
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width,self.pos[1]+self.height), (200, 200, 200), cv2.FILLED)
        cv2.rectangle(img, self.pos, (self.pos[0]+self.width,self.pos[1]+self.height),(50, 50, 50), 3)
        cv2.putText(img, self.value, (self.pos[0]+40,self.pos[1]+60), cv2.FONT_HERSHEY_PLAIN, 2, (50, 50, 50), 2)


    def check_click(self,x,y):
        if self.pos[0]<x<self.pos[0]+self.width and self.pos[1]<y<self.pos[1]+self.height:
            cv2.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (204, 229, 255),
                          cv2.FILLED)
            cv2.rectangle(frame, self.pos, (self.pos[0] + self.width, self.pos[1] + self.height), (51, 255, 255), 3)
            cv2.putText(frame, self.value, (self.pos[0] + 25, self.pos[1] + 80), cv2.FONT_HERSHEY_PLAIN, 5, (204, 0, 0),
                        5)

            return True
        else:
                return False

#l
#creating buttons
buttonListvalues=[['7','8','9','*'],
                  ['4','5','6','-'],
                  ['1','2','3','+'],
                  ['0','.','=','/']]
buttonList=[]
for x in range(4):
    for y in range(4):
        xpos=x*100+800
        ypos=y*100+150
        buttonList.append(Button((xpos,ypos),100,100,buttonListvalues[y][x]))
#variables
myequation=''

#delaycounter
delaycounter=0

#Video frame loop
while cap.isOpened():
    #get image from
    success,frame=cap.read()
    frame=cv2.flip(frame,1)

    #calculator ans button
    cv2.rectangle(frame,(800,50),(800+400,70+100),(255, 255, 255), cv2.FILLED)
    cv2.rectangle(frame,(800,50),(800+400,70+100),(50, 50, 50),3)

    #Detection of hands
    hands,frame=detector.findHands(frame,flipType=False)
    for button in buttonList:
        button.draw(frame)
    #creating a clear button
    cv2.rectangle(frame,(800+300,50),(800+400,50+100),(153,255,255),cv2.FILLED)
    cv2.rectangle(frame,(800+300,50),(800+400,50+100),(50,50,50),3)
    cv2.putText(frame, "clc", (1110, 70+30+10+10), cv2.FONT_HERSHEY_PLAIN, 3, (0,0,0), 3)

    # Check for Hand
    if hands:
        # Find distance between fingers
        lmList = hands[0]['lmList']
        length, info, frame = detector.findDistance(lmList[8][:2], lmList[12][:2], frame)
        x, y = lmList[8][:2]

        if 1100<x<1200 and 50<y<150:
            cv2.rectangle(frame, (800 + 300, 50), (800 + 400, 50 + 100), (0,0,0), cv2.FILLED)
            cv2.rectangle(frame, (800 + 300, 50), (800 + 400, 50 + 100), (50, 50, 50), 3)
            cv2.putText(frame, "clc", (1110, 70 + 30 + 10 + 10), cv2.FONT_HERSHEY_PLAIN, 5, (0, 0, 0), 3)
            myequation=''

        if length<40:
            for i,button in enumerate(buttonList):
                if button.check_click(x,y) and delaycounter==0:
                    myValue=buttonListvalues[int(i%4)][int(i/4)]
                    if myValue== "=":
                        try:
                            eval(myequation)
                            myequation=str(eval(myequation))
                        except SyntaxError:
                            myequation=''
                        except ZeroDivisionError:
                            myequation=''
                    else:
                        myequation += myValue
                    delaycounter=1


        #Display the result
        cv2.putText(frame,myequation,(810,120),cv2.FONT_HERSHEY_PLAIN,3,(0,255,0),3)

        #avoid dunplicates with the help of delaycounter
        if delaycounter!=0:
            delaycounter+=1
            if delaycounter>20:
                delaycounter=0

    key=cv2.waitKey(1)
    if key==ord('c'):
        myequation=''

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

    #display image
    cv2.imshow("video",frame)
    cv2.waitKey(1)
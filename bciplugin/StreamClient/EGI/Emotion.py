#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2021.1.4),
    on Fri Jan  7 11:36:26 2022
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

from __future__ import absolute_import, division

from psychopy import locale_setup
from psychopy import prefs
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

from psychopy.hardware import keyboard

#import winioport
from time import sleep
import datetime
import egi.fake as fakeEgi
import egi.simple as egi
import random

class egiMarker():
    def __init__(self):
    #  sreb.EBObject.__init__(self)
        self.ns = None
        self.ip = "192.168.43.9"
        self.port = 55513
        self.dummy = False
        self.synctime = 0
        self.testMode = True
        self.port1BaseAddress = 0x378
        self.pulseWidth = 1000

    def Initialize(self):
        ## check if in dummy mode and set EGI connection appropriately
        if self.dummy == True: 
            self.ns = fakeEgi.Netstation()
        else:
            ## Create netstation object
            self.ns = egi.Netstation()
        ## The next line is for connecting the actual, single-threaded module version to the computer.
        self.ns.connect(str(self.ip), self.port)
        ## This sends some initialization info to NetStation for recording  s.
        self.ns.BeginSession()
         
    def StartRecording(self):
        ## This synchronizes the clocks of the stim computer and the NetStation computer.
        self.ns.sync(fakeEgi.Netstation().getCurrentTime())
        
        ## This starts the recording in NetStation acquisition. Equivalent to pressing the Record button.
        ## If at some point you pause the experiment using the "StopRecording()" method,
        ## just call this method again to restart the recording.
        self.ns.StartRecording()
         
        ## log onset of recording with event marker (probably redundent)
        self.sendEventMarker('strt', 'Start', 'Start of Recording')

    def sendEventMarker(self, Key, Label = None, description = None,table = None):
        ## This method sends a simple   marker with the current timecode and no complex data feilds.
        if len(Key)>4: 
            Key = Key[:4]
        # handle table arguments 
        if table == None or table == "":
            self.ns.send_event(str(Key),fakeEgi.Netstation().getCurrentTime(), 1, str(Label), str(description), None, pad = True)
            if self.testMode == True:
    #    winioport.out(self.port1BaseAddress, 0xFF)
                sleep(self.pulseWidth/1000)
    #    winioport.out(self.port1BaseAddress, 0x0)
                        
        elif isinstance(table, dict):
            self.ns.send_event(str(Key),fakeEgi.Netstation().getCurrentTime(), 1, str(Label), str(description), table, pad = True)
            if self.testMode == True:
    #    winioport.out(self.port1BaseAddress, 0xFF)
                sleep(self.pulseWidth/1000)
    #    winioport.out(self.port1BaseAddress, 0x0)
                 
        else:       
            self.ns.disconnect()
            self.ns.finalize() 
            raise Exception('The EGI table variable is not a dictionary type')

    def SendDurationEvent(self,  Key,  Onset = None,  Duration = None,  Label = None,  Description = None,  table = None):
        ## Send an   code to mark important  s in the data stream
        if len(Key)>4: 
            Key = str(Key[:4])
             
        if Onset == None or Onset == "":
            Onset = fakeEgi.Netstation().getCurrentTime()
        #elif timestamp.isdigit() == False:
        # raise Exception("The EGI timestamp variable is not an integer")
        
        # Make sure duration is integer value or if blank use 1
        if Duration == None or Duration == "":
            Duration = 1
        #elif duration.isdigit() == False:
        # raise Exception("The EGI duration variable is not an integer")
        
        # check if label is filled in 
        if Label == None or Label == "":
            Label = str(Key)
        else:
            Label = str(Label)
            
        # check if description is filled in
        if Description == None or Description == "":
            Description = ""
        else:
            Description = str(Description)
            
        # handle table arguments 
        if table == None or table == "":
            table = None
        elif not isinstance(table, dict):
            self.ns.disconnect()
            self.ns.finalize()
            raise Exception('The EGI table variable is not a dictionary type')
        
        # send event marker
        self.ns.send_event(Key,int(Onset), int(Duration), Label, Description, table, pad = True)   
        if self.testMode == True:
    #   winioport.out(self.port1BaseAddress, 0xFF)
            sleep(self.pulseWidth/1000)
    #   winioport.out(self.port1BaseAddress, 0x0)       
        
    def StopRecording(self):
        # Send event marker to log end of recording
        self.sendEventMarker('stop', 'Stop', 'End of Recording')

        ## This method is misleading, as it merely pauses the recording in NetStation. Equivalent to the pause button.
        ## It is not actually stopping the recording session. That is done by the 'EndSession()' method below.
        self.ns.StopRecording()
        
    def CloseConnection(self):
        ## use the following line if actually disconnecting from Netstation
        self.ns.EndSession()


# Ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Store info about the experiment session
psychopyVersion = '2021.1.4'
expName = 'Emotion'  # from the Builder filename that created this script
expInfo = {'姓名': '', '年龄': '', '是否存在色觉障碍': '', '左利手还是右利手': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, sortKeys=False, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName
expInfo['psychopyVersion'] = psychopyVersion

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
filename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['姓名'], expName, expInfo['date'])

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath='/Users/egi/Desktop/EGI脑电/Emotion.py',
    savePickle=True, saveWideText=True,
    dataFileName=filename)
# save a log file for detail verbose info
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

endExpNow = False  # flag for 'escape' or other condition => quit the exp
frameTolerance = 0.001  # how close to onset before 'same' frame

# Start Code - component code to be run after the window creation

# Setup the Window
win = visual.Window(
    size=[1680, 1050], fullscr=True, screen=0, 
    winType='pyglet', allowGUI=False, allowStencil=False,
    monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
    blendMode='avg', useFBO=True, 
    units='height')
# store frame rate of monitor if we can measure it
expInfo['frameRate'] = win.getActualFrameRate()
if expInfo['frameRate'] != None:
    frameDur = 1.0 / round(expInfo['frameRate'])
else:
    frameDur = 1.0 / 60.0  # could not measure, so guess

# create a default keyboard (e.g. to check for escape)
defaultKeyboard = keyboard.Keyboard()

# Initialize components for Routine "Introduction"
IntroductionClock = core.Clock()
introduction = visual.TextStim(win=win, name='introduction',
    text='本实验共分为三部分\n在每个部分中\n将播放五段视频\n每段视频后都有14道试题测试\n测试首先显示一个加法算式\n被试根据心算得到结果\n再判断显示的结果是否正确\n正确按‘1’，错误按‘0’\n每部分中间休息5分钟\n\n请按空格键继续',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
key_resp = keyboard.Keyboard()
ftime = open("data/"+expInfo['姓名']+" Marker.txt","a")
ticks = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
ftime.write("实验开始时间    "+ticks+"\n")
myEGI = egiMarker()

myEGI.Initialize()
myEGI.StartRecording()
myEGI.ns.sync(fakeEgi.Netstation().getCurrentTime())
myEGI.sendEventMarker('ex_b', Label='experiment begin', description='something informative texts here', table={'RT':-1, 'Resp': ','})

moviecount=0
calcount=0

movies = ["videos/P_3.mp4","videos/P_4.mp4",
        "videos/P_6.mp4","videos/P_7.mp4",
        "videos/P_8.mp4",
        "videos/O_1.mp4","videos/O_4.mp4",
        "videos/O_6.mp4","videos/O_7.mp4",
        "videos/O_8.mp4",
        "videos/N_2.mp4","videos/N_3.mp4",
        "videos/N_5.mp4","videos/N_7.mp4",
        "videos/N_8.mp4",]

movielenth=[129,172,184,162,212,
            184,144,107,199,99,
            242,241,258,287,203]

var1=[]
var2=[]
answer=[]
display=[]
correct_judge=[]
level = []
movie_belong=[]
filename = "questions.txt"

randnum = random.randint(0,100)
random.seed(randnum)
random.shuffle(movies)
random.seed(randnum)
random.shuffle(movielenth)
i=0
while i< len(movies)-2:
    if movies[i].split("/")[-1].split("_")[0]==movies[i+1].split("/")[-1].split("_")[0] and movies[i].split("/")[-1].split("_")[0]==movies[i+2].split("/")[-1].split("_")[0]:
        randi = random.randint(0,len(movies)-3)
        randj = random.randint(i,i+2)
        movies[randj],movies[randi]=swap(movies[randj],movies[randi])
        movielenth[randj],movielenth[randi]=swap(movielenth[randj],movielenth[randi])
        i=0
    else:
        i=i+1

f=open('questions.txt','r')
o_lines=f.readlines()

random.shuffle(o_lines)
#lines = sorted(o_lines,key=lambda s:int(s.split("\t")[-1].split(".")[0]))

for i in range(0,len(movies)):
    for line in o_lines:
        if line.split("\t")[6].replace('\n','')==movies[i].split('/')[-1]:
            var1.append(line.split("\t")[0].replace('\n',''))
            var2.append(line.split("\t")[1].replace('\n',''))
            answer.append(line.split("\t")[2].replace('\n',''))
            display.append(line.split("\t")[3].replace('\n',''))
            correct_judge.append(line.split("\t")[4].replace('\n',''))
            level.append(line.split("\t")[5].replace('\n',''))
            movie_belong.append(line.split("\t")[6].replace('\n',''))

f.close()

f = open("data/"+expInfo['姓名']+"影片顺序.txt",'w')
for i in range(0,len(movies)):
    f.write(movies[i]+"\n")
f.close()


# Initialize components for Routine "Practice"
PracticeClock = core.Clock()
practice_intro = visual.TextStim(win=win, name='practice_intro',
    text='接下来是测试阶段\n您将一个观看10s的视频',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
practice_movie = visual.MovieStim3(
    win=win, name='practice_movie',
    noAudio = False,
    filename='8.mpg',
    ori=0, pos=(0, 0), opacity=1,
    loop=False,
    size=(2240, 1400),
    depth=-1.0,
    )
practice_intro_2 = visual.TextStim(win=win, name='practice_intro_2',
    text='接下来是试题测试阶段',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-2.0);
practice_cal_1 = visual.TextStim(win=win, name='practice_cal_1',
    text='34+23\n\n\n请心算结果（实际测试中仅出现2s）',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-3.0);
practice_attention = visual.ShapeStim(
    win=win, name='practice_attention', vertices='cross',
    size=(0.5, 0.5),
    ori=0, pos=(0, 0),
    lineWidth=1,     colorSpace='rgb',  lineColor=[1,1,1], fillColor=[1,1,1],
    opacity=1, depth=-4.0, interpolate=True)
practice_judge_1 = visual.TextStim(win=win, name='practice_judge_1',
    text="57\n\n请判断是否是正确答案\n正确按‘1’，错误按'0'，只按一次\n（实验结果只显示2s）",
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-5.0);
practice_intro_3 = visual.TextStim(win=win, name='practice_intro_3',
    text='熟悉之后让我们练习一下正常实验速度',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-6.0);
practice_cal_2 = visual.TextStim(win=win, name='practice_cal_2',
    text='128+231',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-7.0);
practice_attention_2 = visual.ShapeStim(
    win=win, name='practice_attention_2', vertices='cross',
    size=(0.5, 0.5),
    ori=0, pos=(0, 0),
    lineWidth=1,     colorSpace='rgb',  lineColor=[1,1,1], fillColor=[1,1,1],
    opacity=1, depth=-8.0, interpolate=True)
practice_judge_2 = visual.TextStim(win=win, name='practice_judge_2',
    text='349',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-9.0);
practice_cal_3 = visual.TextStim(win=win, name='practice_cal_3',
    text='200+71',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-10.0);
practice_attention_3 = visual.ShapeStim(
    win=win, name='practice_attention_3', vertices='cross',
    size=(0.5, 0.5),
    ori=0, pos=(0, 0),
    lineWidth=1,     colorSpace='rgb',  lineColor=[1,1,1], fillColor=[1,1,1],
    opacity=1, depth=-11.0, interpolate=True)
practice_judge_3 = visual.TextStim(win=win, name='practice_judge_3',
    text='271',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-12.0);

# Initialize components for Routine "BeforeStart"
BeforeStartClock = core.Clock()
beforestart = visual.TextStim(win=win, name='beforestart',
    text='请做好准备\n正式实验马上开始',
    font='Arial',
    pos=(0, 0), height=0.05, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "Movie_intro_1"
Movie_intro_1Clock = core.Clock()
movie_intro_1 = visual.TextStim(win=win, name='movie_intro_1',
    text='影片马上开始',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "Movie_1"
Movie_1Clock = core.Clock()

# Initialize components for Routine "Movie_end_1"
Movie_end_1Clock = core.Clock()
movie_end_1 = visual.TextStim(win=win, name='movie_end_1',
    text='准备开始测试',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "Trail_1"
Trail_1Clock = core.Clock()
trail_1_cal = visual.TextStim(win=win, name='trail_1_cal',
    text='',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
trail_1_atten = visual.TextStim(win=win, name='trail_1_atten',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "trail_1_2"
trail_1_2Clock = core.Clock()
trail_1_judge = visual.TextStim(win=win, name='trail_1_judge',
    text='',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
trail_1_key_2 = keyboard.Keyboard()

# Initialize components for Routine "Break_1"
Break_1Clock = core.Clock()
text = visual.TextStim(win=win, name='text',
    text='请稍作休息',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
break_1_key = keyboard.Keyboard()

# Initialize components for Routine "Movie_intro_2"
Movie_intro_2Clock = core.Clock()
movie_intro_2 = visual.TextStim(win=win, name='movie_intro_2',
    text='影片马上开始',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "Movie_2"
Movie_2Clock = core.Clock()

# Initialize components for Routine "Movie_end_2"
Movie_end_2Clock = core.Clock()
movie_end_2 = visual.TextStim(win=win, name='movie_end_2',
    text='准备开始测试',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "Trail_2"
Trail_2Clock = core.Clock()
trail_2_cal = visual.TextStim(win=win, name='trail_2_cal',
    text='',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
trail_2_atten = visual.TextStim(win=win, name='trail_2_atten',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "trail_2_2"
trail_2_2Clock = core.Clock()
trial_2_judge = visual.TextStim(win=win, name='trial_2_judge',
    text='',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
trail_2_key_2 = keyboard.Keyboard()

# Initialize components for Routine "Break_2"
Break_2Clock = core.Clock()
break_2 = visual.TextStim(win=win, name='break_2',
    text='请稍作休息',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
break_2_key = keyboard.Keyboard()

# Initialize components for Routine "Movie_intro_3"
Movie_intro_3Clock = core.Clock()
movie_intro_3 = visual.TextStim(win=win, name='movie_intro_3',
    text='影片马上开始',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "Movie_3"
Movie_3Clock = core.Clock()

# Initialize components for Routine "Movie_end_3"
Movie_end_3Clock = core.Clock()
movie_end_3 = visual.TextStim(win=win, name='movie_end_3',
    text='准备开始测试',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Initialize components for Routine "Trail_3"
Trail_3Clock = core.Clock()
trail_3_cal = visual.TextStim(win=win, name='trail_3_cal',
    text='',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
trail_3_atten = visual.TextStim(win=win, name='trail_3_atten',
    text='+',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=-1.0);

# Initialize components for Routine "trail_3_2"
trail_3_2Clock = core.Clock()
trail_3_judge = visual.TextStim(win=win, name='trail_3_judge',
    text='',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);
trail_3_key_2 = keyboard.Keyboard()

# Initialize components for Routine "End"
EndClock = core.Clock()
end = visual.TextStim(win=win, name='end',
    text='实验结束\n谢谢您的参与',
    font='Arial',
    pos=(0, 0), height=0.1, wrapWidth=None, ori=0, 
    color='white', colorSpace='rgb', opacity=1, 
    languageStyle='LTR',
    depth=0.0);

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# ------Prepare to start Routine "Introduction"-------
continueRoutine = True
routineTimer.add(60.000000)
# update component parameters for each repeat
key_resp.keys = []
key_resp.rt = []
_key_resp_allKeys = []
# keep track of which components have finished
IntroductionComponents = [introduction, key_resp]
for thisComponent in IntroductionComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
IntroductionClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Introduction"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = IntroductionClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=IntroductionClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *introduction* updates
    if introduction.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        introduction.frameNStart = frameN  # exact frame index
        introduction.tStart = t  # local t and not account for scr refresh
        introduction.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(introduction, 'tStartRefresh')  # time at next scr refresh
        introduction.setAutoDraw(True)
    if introduction.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > introduction.tStartRefresh + 60.0-frameTolerance:
            # keep track of stop time/frame for later
            introduction.tStop = t  # not accounting for scr refresh
            introduction.frameNStop = frameN  # exact frame index
            win.timeOnFlip(introduction, 'tStopRefresh')  # time at next scr refresh
            introduction.setAutoDraw(False)
    
    # *key_resp* updates
    waitOnFlip = False
    if key_resp.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        key_resp.frameNStart = frameN  # exact frame index
        key_resp.tStart = t  # local t and not account for scr refresh
        key_resp.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(key_resp, 'tStartRefresh')  # time at next scr refresh
        key_resp.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(key_resp.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(key_resp.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if key_resp.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > key_resp.tStartRefresh + 60-frameTolerance:
            # keep track of stop time/frame for later
            key_resp.tStop = t  # not accounting for scr refresh
            key_resp.frameNStop = frameN  # exact frame index
            win.timeOnFlip(key_resp, 'tStopRefresh')  # time at next scr refresh
            key_resp.status = FINISHED
    if key_resp.status == STARTED and not waitOnFlip:
        theseKeys = key_resp.getKeys(keyList=['space'], waitRelease=False)
        _key_resp_allKeys.extend(theseKeys)
        if len(_key_resp_allKeys):
            key_resp.keys = _key_resp_allKeys[-1].name  # just the last key pressed
            key_resp.rt = _key_resp_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in IntroductionComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Introduction"-------
for thisComponent in IntroductionComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('introduction.started', introduction.tStartRefresh)
thisExp.addData('introduction.stopped', introduction.tStopRefresh)
# check responses
if key_resp.keys in ['', [], None]:  # No response was made
    key_resp.keys = None
thisExp.addData('key_resp.keys',key_resp.keys)
if key_resp.keys != None:  # we had a response
    thisExp.addData('key_resp.rt', key_resp.rt)
thisExp.addData('key_resp.started', key_resp.tStartRefresh)
thisExp.addData('key_resp.stopped', key_resp.tStopRefresh)
thisExp.nextEntry()

# ------Prepare to start Routine "Practice"-------
continueRoutine = True
routineTimer.add(42.000000)
# update component parameters for each repeat
# keep track of which components have finished
PracticeComponents = [practice_intro, practice_movie, practice_intro_2, practice_cal_1, practice_attention, practice_judge_1, practice_intro_3, practice_cal_2, practice_attention_2, practice_judge_2, practice_cal_3, practice_attention_3, practice_judge_3]
for thisComponent in PracticeComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
PracticeClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Practice"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = PracticeClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=PracticeClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *practice_intro* updates
    if practice_intro.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        practice_intro.frameNStart = frameN  # exact frame index
        practice_intro.tStart = t  # local t and not account for scr refresh
        practice_intro.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practice_intro, 'tStartRefresh')  # time at next scr refresh
        practice_intro.setAutoDraw(True)
    if practice_intro.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > practice_intro.tStartRefresh + 3.0-frameTolerance:
            # keep track of stop time/frame for later
            practice_intro.tStop = t  # not accounting for scr refresh
            practice_intro.frameNStop = frameN  # exact frame index
            win.timeOnFlip(practice_intro, 'tStopRefresh')  # time at next scr refresh
            practice_intro.setAutoDraw(False)
    
    # *practice_movie* updates
    if practice_movie.status == NOT_STARTED and tThisFlip >= 3.0-frameTolerance:
        # keep track of start time/frame for later
        practice_movie.frameNStart = frameN  # exact frame index
        practice_movie.tStart = t  # local t and not account for scr refresh
        practice_movie.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practice_movie, 'tStartRefresh')  # time at next scr refresh
        practice_movie.setAutoDraw(True)
    if practice_movie.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > practice_movie.tStartRefresh + 10.0-frameTolerance:
            # keep track of stop time/frame for later
            practice_movie.tStop = t  # not accounting for scr refresh
            practice_movie.frameNStop = frameN  # exact frame index
            win.timeOnFlip(practice_movie, 'tStopRefresh')  # time at next scr refresh
            practice_movie.setAutoDraw(False)
    
    # *practice_intro_2* updates
    if practice_intro_2.status == NOT_STARTED and tThisFlip >= 13.0-frameTolerance:
        # keep track of start time/frame for later
        practice_intro_2.frameNStart = frameN  # exact frame index
        practice_intro_2.tStart = t  # local t and not account for scr refresh
        practice_intro_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practice_intro_2, 'tStartRefresh')  # time at next scr refresh
        practice_intro_2.setAutoDraw(True)
    if practice_intro_2.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > practice_intro_2.tStartRefresh + 3.0-frameTolerance:
            # keep track of stop time/frame for later
            practice_intro_2.tStop = t  # not accounting for scr refresh
            practice_intro_2.frameNStop = frameN  # exact frame index
            win.timeOnFlip(practice_intro_2, 'tStopRefresh')  # time at next scr refresh
            practice_intro_2.setAutoDraw(False)
    
    # *practice_cal_1* updates
    if practice_cal_1.status == NOT_STARTED and tThisFlip >= 16.0-frameTolerance:
        # keep track of start time/frame for later
        practice_cal_1.frameNStart = frameN  # exact frame index
        practice_cal_1.tStart = t  # local t and not account for scr refresh
        practice_cal_1.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practice_cal_1, 'tStartRefresh')  # time at next scr refresh
        practice_cal_1.setAutoDraw(True)
    if practice_cal_1.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > practice_cal_1.tStartRefresh + 5.0-frameTolerance:
            # keep track of stop time/frame for later
            practice_cal_1.tStop = t  # not accounting for scr refresh
            practice_cal_1.frameNStop = frameN  # exact frame index
            win.timeOnFlip(practice_cal_1, 'tStopRefresh')  # time at next scr refresh
            practice_cal_1.setAutoDraw(False)
    
    # *practice_attention* updates
    if practice_attention.status == NOT_STARTED and tThisFlip >= 21.0-frameTolerance:
        # keep track of start time/frame for later
        practice_attention.frameNStart = frameN  # exact frame index
        practice_attention.tStart = t  # local t and not account for scr refresh
        practice_attention.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practice_attention, 'tStartRefresh')  # time at next scr refresh
        practice_attention.setAutoDraw(True)
    if practice_attention.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > practice_attention.tStartRefresh + 2.0-frameTolerance:
            # keep track of stop time/frame for later
            practice_attention.tStop = t  # not accounting for scr refresh
            practice_attention.frameNStop = frameN  # exact frame index
            win.timeOnFlip(practice_attention, 'tStopRefresh')  # time at next scr refresh
            practice_attention.setAutoDraw(False)
    
    # *practice_judge_1* updates
    if practice_judge_1.status == NOT_STARTED and tThisFlip >= 23.0-frameTolerance:
        # keep track of start time/frame for later
        practice_judge_1.frameNStart = frameN  # exact frame index
        practice_judge_1.tStart = t  # local t and not account for scr refresh
        practice_judge_1.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practice_judge_1, 'tStartRefresh')  # time at next scr refresh
        practice_judge_1.setAutoDraw(True)
    if practice_judge_1.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > practice_judge_1.tStartRefresh + 5.0-frameTolerance:
            # keep track of stop time/frame for later
            practice_judge_1.tStop = t  # not accounting for scr refresh
            practice_judge_1.frameNStop = frameN  # exact frame index
            win.timeOnFlip(practice_judge_1, 'tStopRefresh')  # time at next scr refresh
            practice_judge_1.setAutoDraw(False)
    
    # *practice_intro_3* updates
    if practice_intro_3.status == NOT_STARTED and tThisFlip >= 28.0-frameTolerance:
        # keep track of start time/frame for later
        practice_intro_3.frameNStart = frameN  # exact frame index
        practice_intro_3.tStart = t  # local t and not account for scr refresh
        practice_intro_3.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practice_intro_3, 'tStartRefresh')  # time at next scr refresh
        practice_intro_3.setAutoDraw(True)
    if practice_intro_3.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > practice_intro_3.tStartRefresh + 5.0-frameTolerance:
            # keep track of stop time/frame for later
            practice_intro_3.tStop = t  # not accounting for scr refresh
            practice_intro_3.frameNStop = frameN  # exact frame index
            win.timeOnFlip(practice_intro_3, 'tStopRefresh')  # time at next scr refresh
            practice_intro_3.setAutoDraw(False)
    
    # *practice_cal_2* updates
    if practice_cal_2.status == NOT_STARTED and tThisFlip >= 33.0-frameTolerance:
        # keep track of start time/frame for later
        practice_cal_2.frameNStart = frameN  # exact frame index
        practice_cal_2.tStart = t  # local t and not account for scr refresh
        practice_cal_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practice_cal_2, 'tStartRefresh')  # time at next scr refresh
        practice_cal_2.setAutoDraw(True)
    if practice_cal_2.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > practice_cal_2.tStartRefresh + 2.0-frameTolerance:
            # keep track of stop time/frame for later
            practice_cal_2.tStop = t  # not accounting for scr refresh
            practice_cal_2.frameNStop = frameN  # exact frame index
            win.timeOnFlip(practice_cal_2, 'tStopRefresh')  # time at next scr refresh
            practice_cal_2.setAutoDraw(False)
    
    # *practice_attention_2* updates
    if practice_attention_2.status == NOT_STARTED and tThisFlip >= 35.0-frameTolerance:
        # keep track of start time/frame for later
        practice_attention_2.frameNStart = frameN  # exact frame index
        practice_attention_2.tStart = t  # local t and not account for scr refresh
        practice_attention_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practice_attention_2, 'tStartRefresh')  # time at next scr refresh
        practice_attention_2.setAutoDraw(True)
    if practice_attention_2.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > practice_attention_2.tStartRefresh + 0.5-frameTolerance:
            # keep track of stop time/frame for later
            practice_attention_2.tStop = t  # not accounting for scr refresh
            practice_attention_2.frameNStop = frameN  # exact frame index
            win.timeOnFlip(practice_attention_2, 'tStopRefresh')  # time at next scr refresh
            practice_attention_2.setAutoDraw(False)
    
    # *practice_judge_2* updates
    if practice_judge_2.status == NOT_STARTED and tThisFlip >= 35.5-frameTolerance:
        # keep track of start time/frame for later
        practice_judge_2.frameNStart = frameN  # exact frame index
        practice_judge_2.tStart = t  # local t and not account for scr refresh
        practice_judge_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practice_judge_2, 'tStartRefresh')  # time at next scr refresh
        practice_judge_2.setAutoDraw(True)
    if practice_judge_2.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > practice_judge_2.tStartRefresh + 2.0-frameTolerance:
            # keep track of stop time/frame for later
            practice_judge_2.tStop = t  # not accounting for scr refresh
            practice_judge_2.frameNStop = frameN  # exact frame index
            win.timeOnFlip(practice_judge_2, 'tStopRefresh')  # time at next scr refresh
            practice_judge_2.setAutoDraw(False)
    
    # *practice_cal_3* updates
    if practice_cal_3.status == NOT_STARTED and tThisFlip >= 37.5-frameTolerance:
        # keep track of start time/frame for later
        practice_cal_3.frameNStart = frameN  # exact frame index
        practice_cal_3.tStart = t  # local t and not account for scr refresh
        practice_cal_3.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practice_cal_3, 'tStartRefresh')  # time at next scr refresh
        practice_cal_3.setAutoDraw(True)
    if practice_cal_3.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > practice_cal_3.tStartRefresh + 2.0-frameTolerance:
            # keep track of stop time/frame for later
            practice_cal_3.tStop = t  # not accounting for scr refresh
            practice_cal_3.frameNStop = frameN  # exact frame index
            win.timeOnFlip(practice_cal_3, 'tStopRefresh')  # time at next scr refresh
            practice_cal_3.setAutoDraw(False)
    
    # *practice_attention_3* updates
    if practice_attention_3.status == NOT_STARTED and tThisFlip >= 39.5-frameTolerance:
        # keep track of start time/frame for later
        practice_attention_3.frameNStart = frameN  # exact frame index
        practice_attention_3.tStart = t  # local t and not account for scr refresh
        practice_attention_3.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practice_attention_3, 'tStartRefresh')  # time at next scr refresh
        practice_attention_3.setAutoDraw(True)
    if practice_attention_3.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > practice_attention_3.tStartRefresh + 0.5-frameTolerance:
            # keep track of stop time/frame for later
            practice_attention_3.tStop = t  # not accounting for scr refresh
            practice_attention_3.frameNStop = frameN  # exact frame index
            win.timeOnFlip(practice_attention_3, 'tStopRefresh')  # time at next scr refresh
            practice_attention_3.setAutoDraw(False)
    
    # *practice_judge_3* updates
    if practice_judge_3.status == NOT_STARTED and tThisFlip >= 40-frameTolerance:
        # keep track of start time/frame for later
        practice_judge_3.frameNStart = frameN  # exact frame index
        practice_judge_3.tStart = t  # local t and not account for scr refresh
        practice_judge_3.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(practice_judge_3, 'tStartRefresh')  # time at next scr refresh
        practice_judge_3.setAutoDraw(True)
    if practice_judge_3.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > practice_judge_3.tStartRefresh + 2-frameTolerance:
            # keep track of stop time/frame for later
            practice_judge_3.tStop = t  # not accounting for scr refresh
            practice_judge_3.frameNStop = frameN  # exact frame index
            win.timeOnFlip(practice_judge_3, 'tStopRefresh')  # time at next scr refresh
            practice_judge_3.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in PracticeComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Practice"-------
for thisComponent in PracticeComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('practice_intro.started', practice_intro.tStartRefresh)
thisExp.addData('practice_intro.stopped', practice_intro.tStopRefresh)
practice_movie.stop()
thisExp.addData('practice_intro_2.started', practice_intro_2.tStartRefresh)
thisExp.addData('practice_intro_2.stopped', practice_intro_2.tStopRefresh)
thisExp.addData('practice_cal_1.started', practice_cal_1.tStartRefresh)
thisExp.addData('practice_cal_1.stopped', practice_cal_1.tStopRefresh)
thisExp.addData('practice_attention.started', practice_attention.tStartRefresh)
thisExp.addData('practice_attention.stopped', practice_attention.tStopRefresh)
thisExp.addData('practice_judge_1.started', practice_judge_1.tStartRefresh)
thisExp.addData('practice_judge_1.stopped', practice_judge_1.tStopRefresh)
thisExp.addData('practice_intro_3.started', practice_intro_3.tStartRefresh)
thisExp.addData('practice_intro_3.stopped', practice_intro_3.tStopRefresh)
thisExp.addData('practice_cal_2.started', practice_cal_2.tStartRefresh)
thisExp.addData('practice_cal_2.stopped', practice_cal_2.tStopRefresh)
thisExp.addData('practice_attention_2.started', practice_attention_2.tStartRefresh)
thisExp.addData('practice_attention_2.stopped', practice_attention_2.tStopRefresh)
thisExp.addData('practice_judge_2.started', practice_judge_2.tStartRefresh)
thisExp.addData('practice_judge_2.stopped', practice_judge_2.tStopRefresh)
thisExp.addData('practice_cal_3.started', practice_cal_3.tStartRefresh)
thisExp.addData('practice_cal_3.stopped', practice_cal_3.tStopRefresh)
thisExp.addData('practice_attention_3.started', practice_attention_3.tStartRefresh)
thisExp.addData('practice_attention_3.stopped', practice_attention_3.tStopRefresh)
thisExp.addData('practice_judge_3.started', practice_judge_3.tStartRefresh)
thisExp.addData('practice_judge_3.stopped', practice_judge_3.tStopRefresh)

# ------Prepare to start Routine "BeforeStart"-------
continueRoutine = True
routineTimer.add(5.000000)
# update component parameters for each repeat
# keep track of which components have finished
BeforeStartComponents = [beforestart]
for thisComponent in BeforeStartComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
BeforeStartClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "BeforeStart"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = BeforeStartClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=BeforeStartClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *beforestart* updates
    if beforestart.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        beforestart.frameNStart = frameN  # exact frame index
        beforestart.tStart = t  # local t and not account for scr refresh
        beforestart.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(beforestart, 'tStartRefresh')  # time at next scr refresh
        beforestart.setAutoDraw(True)
    if beforestart.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > beforestart.tStartRefresh + 5.0-frameTolerance:
            # keep track of stop time/frame for later
            beforestart.tStop = t  # not accounting for scr refresh
            beforestart.frameNStop = frameN  # exact frame index
            win.timeOnFlip(beforestart, 'tStopRefresh')  # time at next scr refresh
            beforestart.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in BeforeStartComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "BeforeStart"-------
for thisComponent in BeforeStartComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('beforestart.started', beforestart.tStartRefresh)
thisExp.addData('beforestart.stopped', beforestart.tStopRefresh)

# set up handler to look after randomisation of conditions etc
Block_1 = data.TrialHandler(nReps=5, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='Block_1')
thisExp.addLoop(Block_1)  # add the loop to the experiment
thisBlock_1 = Block_1.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock_1.rgb)
if thisBlock_1 != None:
    for paramName in thisBlock_1:
        exec('{} = thisBlock_1[paramName]'.format(paramName))

for thisBlock_1 in Block_1:
    currentLoop = Block_1
    # abbreviate parameter names if possible (e.g. rgb = thisBlock_1.rgb)
    if thisBlock_1 != None:
        for paramName in thisBlock_1:
            exec('{} = thisBlock_1[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "Movie_intro_1"-------
    continueRoutine = True
    routineTimer.add(1.000000)
    # update component parameters for each repeat
    # keep track of which components have finished
    Movie_intro_1Components = [movie_intro_1]
    for thisComponent in Movie_intro_1Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Movie_intro_1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Movie_intro_1"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Movie_intro_1Clock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Movie_intro_1Clock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *movie_intro_1* updates
        if movie_intro_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            movie_intro_1.frameNStart = frameN  # exact frame index
            movie_intro_1.tStart = t  # local t and not account for scr refresh
            movie_intro_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(movie_intro_1, 'tStartRefresh')  # time at next scr refresh
            movie_intro_1.setAutoDraw(True)
        if movie_intro_1.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > movie_intro_1.tStartRefresh + 1.0-frameTolerance:
                # keep track of stop time/frame for later
                movie_intro_1.tStop = t  # not accounting for scr refresh
                movie_intro_1.frameNStop = frameN  # exact frame index
                win.timeOnFlip(movie_intro_1, 'tStopRefresh')  # time at next scr refresh
                movie_intro_1.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Movie_intro_1Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Movie_intro_1"-------
    for thisComponent in Movie_intro_1Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    Block_1.addData('movie_intro_1.started', movie_intro_1.tStartRefresh)
    Block_1.addData('movie_intro_1.stopped', movie_intro_1.tStopRefresh)
    
    # ------Prepare to start Routine "Movie_1"-------
    continueRoutine = True
    # update component parameters for each repeat
    movie_1 = visual.MovieStim3(
        win=win, name='movie_1',
        noAudio = False,
        filename=movies[moviecount],
        ori=0, pos=(0, 0), opacity=1,
        loop=False,
        size=(2240, 1400),
        depth=0.0,
        )
    myEGI.ns.sync(fakeEgi.Netstation().getCurrentTime())
    myEGI.sendEventMarker('mv_b', Label='movie'+str(moviecount)+'_begin', description='something informative texts here', table={'RT':-1, 'Resp': ','})
    
    
    ticks = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    ftime.write("视频"+str(moviecount)+"开始播放    "+ticks+"\n")
    # keep track of which components have finished
    Movie_1Components = [movie_1]
    for thisComponent in Movie_1Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Movie_1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Movie_1"-------
    while continueRoutine:
        # get current time
        t = Movie_1Clock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Movie_1Clock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *movie_1* updates
        if movie_1.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            movie_1.frameNStart = frameN  # exact frame index
            movie_1.tStart = t  # local t and not account for scr refresh
            movie_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(movie_1, 'tStartRefresh')  # time at next scr refresh
            movie_1.setAutoDraw(True)
        if movie_1.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > movie_1.tStartRefresh + movielenth[moviecount]-frameTolerance:
                # keep track of stop time/frame for later
                movie_1.tStop = t  # not accounting for scr refresh
                movie_1.frameNStop = frameN  # exact frame index
                win.timeOnFlip(movie_1, 'tStopRefresh')  # time at next scr refresh
                movie_1.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Movie_1Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Movie_1"-------
    for thisComponent in Movie_1Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    movie_1.stop()
    myEGI.ns.sync(fakeEgi.Netstation().getCurrentTime())
    myEGI.sendEventMarker('mv_e', Label='movie'+str(moviecount)+'_end', description='something informative texts here', table={'RT':-1, 'Resp': ','})
    
    ticks = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    ftime.write("视频"+str(moviecount)+"结束播放    "+ticks+"\n")
    moviecount+=1
    # the Routine "Movie_1" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "Movie_end_1"-------
    continueRoutine = True
    routineTimer.add(2.000000)
    # update component parameters for each repeat
    # keep track of which components have finished
    Movie_end_1Components = [movie_end_1]
    for thisComponent in Movie_end_1Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Movie_end_1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Movie_end_1"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Movie_end_1Clock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Movie_end_1Clock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *movie_end_1* updates
        if movie_end_1.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            movie_end_1.frameNStart = frameN  # exact frame index
            movie_end_1.tStart = t  # local t and not account for scr refresh
            movie_end_1.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(movie_end_1, 'tStartRefresh')  # time at next scr refresh
            movie_end_1.setAutoDraw(True)
        if movie_end_1.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > movie_end_1.tStartRefresh + 2.0-frameTolerance:
                # keep track of stop time/frame for later
                movie_end_1.tStop = t  # not accounting for scr refresh
                movie_end_1.frameNStop = frameN  # exact frame index
                win.timeOnFlip(movie_end_1, 'tStopRefresh')  # time at next scr refresh
                movie_end_1.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Movie_end_1Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Movie_end_1"-------
    for thisComponent in Movie_end_1Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    Block_1.addData('movie_end_1.started', movie_end_1.tStartRefresh)
    Block_1.addData('movie_end_1.stopped', movie_end_1.tStopRefresh)
    
    # set up handler to look after randomisation of conditions etc
    trials_1 = data.TrialHandler(nReps=14, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='trials_1')
    thisExp.addLoop(trials_1)  # add the loop to the experiment
    thisTrial_1 = trials_1.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial_1.rgb)
    if thisTrial_1 != None:
        for paramName in thisTrial_1:
            exec('{} = thisTrial_1[paramName]'.format(paramName))
    
    for thisTrial_1 in trials_1:
        currentLoop = trials_1
        # abbreviate parameter names if possible (e.g. rgb = thisTrial_1.rgb)
        if thisTrial_1 != None:
            for paramName in thisTrial_1:
                exec('{} = thisTrial_1[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "Trail_1"-------
        continueRoutine = True
        routineTimer.add(2.500000)
        # update component parameters for each repeat
        trail_1_cal.setText('var1[calcount]+"+"+$var2[calcount]')
        myEGI.ns.sync(fakeEgi.Netstation().getCurrentTime())
        myEGI.sendEventMarker('ca_b', Label='cal'+str(calcount)+'_start', description='something informative texts here', table={'RT':-1, 'Resp': ','})
        ticks = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        ftime.write("第"+str(calcount)+"次答题开始    "+ticks+"\t"+str(var1[calcount])+"+"+str(var2[calcount])+"\n")
        # keep track of which components have finished
        Trail_1Components = [trail_1_cal, trail_1_atten]
        for thisComponent in Trail_1Components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        Trail_1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Trail_1"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = Trail_1Clock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=Trail_1Clock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *trail_1_cal* updates
            if trail_1_cal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                trail_1_cal.frameNStart = frameN  # exact frame index
                trail_1_cal.tStart = t  # local t and not account for scr refresh
                trail_1_cal.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trail_1_cal, 'tStartRefresh')  # time at next scr refresh
                trail_1_cal.setAutoDraw(True)
            if trail_1_cal.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > trail_1_cal.tStartRefresh + 2.0-frameTolerance:
                    # keep track of stop time/frame for later
                    trail_1_cal.tStop = t  # not accounting for scr refresh
                    trail_1_cal.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(trail_1_cal, 'tStopRefresh')  # time at next scr refresh
                    trail_1_cal.setAutoDraw(False)
            
            # *trail_1_atten* updates
            if trail_1_atten.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
                # keep track of start time/frame for later
                trail_1_atten.frameNStart = frameN  # exact frame index
                trail_1_atten.tStart = t  # local t and not account for scr refresh
                trail_1_atten.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trail_1_atten, 'tStartRefresh')  # time at next scr refresh
                trail_1_atten.setAutoDraw(True)
            if trail_1_atten.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > trail_1_atten.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    trail_1_atten.tStop = t  # not accounting for scr refresh
                    trail_1_atten.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(trail_1_atten, 'tStopRefresh')  # time at next scr refresh
                    trail_1_atten.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Trail_1Components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Trail_1"-------
        for thisComponent in Trail_1Components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trials_1.addData('trail_1_cal.started', trail_1_cal.tStartRefresh)
        trials_1.addData('trail_1_cal.stopped', trail_1_cal.tStopRefresh)
        trials_1.addData('trail_1_atten.started', trail_1_atten.tStartRefresh)
        trials_1.addData('trail_1_atten.stopped', trail_1_atten.tStopRefresh)
        
        # ------Prepare to start Routine "trail_1_2"-------
        continueRoutine = True
        routineTimer.add(2.000000)
        # update component parameters for each repeat
        trail_1_judge.setText(display[calcount])
        trail_1_key_2.keys = []
        trail_1_key_2.rt = []
        _trail_1_key_2_allKeys = []
        myEGI.ns.sync(fakeEgi.Netstation().getCurrentTime())
        myEGI.sendEventMarker('judge_b', Label='judge'+str(calcount)+'_start', description='something informative texts here', table={'RT':-1, 'Resp': ','})
        # keep track of which components have finished
        trail_1_2Components = [trail_1_judge, trail_1_key_2]
        for thisComponent in trail_1_2Components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        trail_1_2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "trail_1_2"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = trail_1_2Clock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=trail_1_2Clock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *trail_1_judge* updates
            if trail_1_judge.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                trail_1_judge.frameNStart = frameN  # exact frame index
                trail_1_judge.tStart = t  # local t and not account for scr refresh
                trail_1_judge.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trail_1_judge, 'tStartRefresh')  # time at next scr refresh
                trail_1_judge.setAutoDraw(True)
            if trail_1_judge.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > trail_1_judge.tStartRefresh + 2.0-frameTolerance:
                    # keep track of stop time/frame for later
                    trail_1_judge.tStop = t  # not accounting for scr refresh
                    trail_1_judge.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(trail_1_judge, 'tStopRefresh')  # time at next scr refresh
                    trail_1_judge.setAutoDraw(False)
            
            # *trail_1_key_2* updates
            waitOnFlip = False
            if trail_1_key_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                trail_1_key_2.frameNStart = frameN  # exact frame index
                trail_1_key_2.tStart = t  # local t and not account for scr refresh
                trail_1_key_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trail_1_key_2, 'tStartRefresh')  # time at next scr refresh
                trail_1_key_2.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(trail_1_key_2.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(trail_1_key_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if trail_1_key_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > trail_1_key_2.tStartRefresh + 2-frameTolerance:
                    # keep track of stop time/frame for later
                    trail_1_key_2.tStop = t  # not accounting for scr refresh
                    trail_1_key_2.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(trail_1_key_2, 'tStopRefresh')  # time at next scr refresh
                    trail_1_key_2.status = FINISHED
            if trail_1_key_2.status == STARTED and not waitOnFlip:
                theseKeys = trail_1_key_2.getKeys(keyList=['1', '0'], waitRelease=False)
                _trail_1_key_2_allKeys.extend(theseKeys)
                if len(_trail_1_key_2_allKeys):
                    trail_1_key_2.keys = _trail_1_key_2_allKeys[0].name  # just the first key pressed
                    trail_1_key_2.rt = _trail_1_key_2_allKeys[0].rt
                    # was this correct?
                    if (trail_1_key_2.keys == str(correct_judge[calcount])) or (trail_1_key_2.keys == correct_judge[calcount]):
                        trail_1_key_2.corr = 1
                    else:
                        trail_1_key_2.corr = 0
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trail_1_2Components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "trail_1_2"-------
        for thisComponent in trail_1_2Components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trials_1.addData('trail_1_judge.started', trail_1_judge.tStartRefresh)
        trials_1.addData('trail_1_judge.stopped', trail_1_judge.tStopRefresh)
        # check responses
        if trail_1_key_2.keys in ['', [], None]:  # No response was made
            trail_1_key_2.keys = None
            # was no response the correct answer?!
            if str(correct_judge[calcount]).lower() == 'none':
               trail_1_key_2.corr = 1;  # correct non-response
            else:
               trail_1_key_2.corr = 0;  # failed to respond (incorrectly)
        # store data for trials_1 (TrialHandler)
        trials_1.addData('trail_1_key_2.keys',trail_1_key_2.keys)
        trials_1.addData('trail_1_key_2.corr', trail_1_key_2.corr)
        if trail_1_key_2.keys != None:  # we had a response
            trials_1.addData('trail_1_key_2.rt', trail_1_key_2.rt)
        trials_1.addData('trail_1_key_2.started', trail_1_key_2.tStartRefresh)
        trials_1.addData('trail_1_key_2.stopped', trail_1_key_2.tStopRefresh)
        
        ticks = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        ftime.write("第"+str(calcount)+"次答题结束    "+ticks+"\n")
        calcount=calcount+1
        thisExp.nextEntry()
        
    # completed 14 repeats of 'trials_1'
    
    thisExp.nextEntry()
    
# completed 5 repeats of 'Block_1'


# ------Prepare to start Routine "Break_1"-------
continueRoutine = True
routineTimer.add(3000.000000)
# update component parameters for each repeat
break_1_key.keys = []
break_1_key.rt = []
_break_1_key_allKeys = []
# keep track of which components have finished
Break_1Components = [text, break_1_key]
for thisComponent in Break_1Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
Break_1Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Break_1"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = Break_1Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=Break_1Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *text* updates
    if text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        text.frameNStart = frameN  # exact frame index
        text.tStart = t  # local t and not account for scr refresh
        text.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(text, 'tStartRefresh')  # time at next scr refresh
        text.setAutoDraw(True)
    if text.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > text.tStartRefresh + 3000-frameTolerance:
            # keep track of stop time/frame for later
            text.tStop = t  # not accounting for scr refresh
            text.frameNStop = frameN  # exact frame index
            win.timeOnFlip(text, 'tStopRefresh')  # time at next scr refresh
            text.setAutoDraw(False)
    
    # *break_1_key* updates
    waitOnFlip = False
    if break_1_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        break_1_key.frameNStart = frameN  # exact frame index
        break_1_key.tStart = t  # local t and not account for scr refresh
        break_1_key.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(break_1_key, 'tStartRefresh')  # time at next scr refresh
        break_1_key.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(break_1_key.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(break_1_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if break_1_key.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > break_1_key.tStartRefresh + 3000-frameTolerance:
            # keep track of stop time/frame for later
            break_1_key.tStop = t  # not accounting for scr refresh
            break_1_key.frameNStop = frameN  # exact frame index
            win.timeOnFlip(break_1_key, 'tStopRefresh')  # time at next scr refresh
            break_1_key.status = FINISHED
    if break_1_key.status == STARTED and not waitOnFlip:
        theseKeys = break_1_key.getKeys(keyList=['space'], waitRelease=False)
        _break_1_key_allKeys.extend(theseKeys)
        if len(_break_1_key_allKeys):
            break_1_key.keys = _break_1_key_allKeys[-1].name  # just the last key pressed
            break_1_key.rt = _break_1_key_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Break_1Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Break_1"-------
for thisComponent in Break_1Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('text.started', text.tStartRefresh)
thisExp.addData('text.stopped', text.tStopRefresh)
# check responses
if break_1_key.keys in ['', [], None]:  # No response was made
    break_1_key.keys = None
thisExp.addData('break_1_key.keys',break_1_key.keys)
if break_1_key.keys != None:  # we had a response
    thisExp.addData('break_1_key.rt', break_1_key.rt)
thisExp.addData('break_1_key.started', break_1_key.tStartRefresh)
thisExp.addData('break_1_key.stopped', break_1_key.tStopRefresh)
thisExp.nextEntry()

# set up handler to look after randomisation of conditions etc
Block_2 = data.TrialHandler(nReps=5, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='Block_2')
thisExp.addLoop(Block_2)  # add the loop to the experiment
thisBlock_2 = Block_2.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock_2.rgb)
if thisBlock_2 != None:
    for paramName in thisBlock_2:
        exec('{} = thisBlock_2[paramName]'.format(paramName))

for thisBlock_2 in Block_2:
    currentLoop = Block_2
    # abbreviate parameter names if possible (e.g. rgb = thisBlock_2.rgb)
    if thisBlock_2 != None:
        for paramName in thisBlock_2:
            exec('{} = thisBlock_2[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "Movie_intro_2"-------
    continueRoutine = True
    routineTimer.add(1.500000)
    # update component parameters for each repeat
    # keep track of which components have finished
    Movie_intro_2Components = [movie_intro_2]
    for thisComponent in Movie_intro_2Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Movie_intro_2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Movie_intro_2"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Movie_intro_2Clock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Movie_intro_2Clock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *movie_intro_2* updates
        if movie_intro_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            movie_intro_2.frameNStart = frameN  # exact frame index
            movie_intro_2.tStart = t  # local t and not account for scr refresh
            movie_intro_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(movie_intro_2, 'tStartRefresh')  # time at next scr refresh
            movie_intro_2.setAutoDraw(True)
        if movie_intro_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > movie_intro_2.tStartRefresh + 1.5-frameTolerance:
                # keep track of stop time/frame for later
                movie_intro_2.tStop = t  # not accounting for scr refresh
                movie_intro_2.frameNStop = frameN  # exact frame index
                win.timeOnFlip(movie_intro_2, 'tStopRefresh')  # time at next scr refresh
                movie_intro_2.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Movie_intro_2Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Movie_intro_2"-------
    for thisComponent in Movie_intro_2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    Block_2.addData('movie_intro_2.started', movie_intro_2.tStartRefresh)
    Block_2.addData('movie_intro_2.stopped', movie_intro_2.tStopRefresh)
    
    # ------Prepare to start Routine "Movie_2"-------
    continueRoutine = True
    # update component parameters for each repeat
    movie_2 = visual.MovieStim3(
        win=win, name='movie_2',
        noAudio = False,
        filename=movies[moviecount],
        ori=0, pos=(0, 0), opacity=1,
        loop=False,
        size=(2240, 1400),
        depth=0.0,
        )
    myEGI.ns.sync(fakeEgi.Netstation().getCurrentTime())
    myEGI.sendEventMarker('mv_b', Label='movie'+str(moviecount)+'_begin', description='something informative texts here', table={'RT':-1, 'Resp': ','})
    
    ticks = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    ftime.write("视频"+str(moviecount)+"开始播放    "+ticks+"\n")
    # keep track of which components have finished
    Movie_2Components = [movie_2]
    for thisComponent in Movie_2Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Movie_2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Movie_2"-------
    while continueRoutine:
        # get current time
        t = Movie_2Clock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Movie_2Clock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *movie_2* updates
        if movie_2.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            movie_2.frameNStart = frameN  # exact frame index
            movie_2.tStart = t  # local t and not account for scr refresh
            movie_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(movie_2, 'tStartRefresh')  # time at next scr refresh
            movie_2.setAutoDraw(True)
        if movie_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > movie_2.tStartRefresh + movielenth[moviecount]-frameTolerance:
                # keep track of stop time/frame for later
                movie_2.tStop = t  # not accounting for scr refresh
                movie_2.frameNStop = frameN  # exact frame index
                win.timeOnFlip(movie_2, 'tStopRefresh')  # time at next scr refresh
                movie_2.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Movie_2Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Movie_2"-------
    for thisComponent in Movie_2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    movie_2.stop()
    myEGI.ns.sync(fakeEgi.Netstation().getCurrentTime())
    myEGI.sendEventMarker('mv_e', Label='movie'+str(moviecount)+'_end', description='something informative texts here', table={'RT':-1, 'Resp': ','})
    ticks = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    ftime.write("视频"+str(moviecount)+"结束播放    "+ticks+"\n")
    moviecount+=1
    # the Routine "Movie_2" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "Movie_end_2"-------
    continueRoutine = True
    routineTimer.add(2.000000)
    # update component parameters for each repeat
    # keep track of which components have finished
    Movie_end_2Components = [movie_end_2]
    for thisComponent in Movie_end_2Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Movie_end_2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Movie_end_2"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Movie_end_2Clock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Movie_end_2Clock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *movie_end_2* updates
        if movie_end_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            movie_end_2.frameNStart = frameN  # exact frame index
            movie_end_2.tStart = t  # local t and not account for scr refresh
            movie_end_2.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(movie_end_2, 'tStartRefresh')  # time at next scr refresh
            movie_end_2.setAutoDraw(True)
        if movie_end_2.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > movie_end_2.tStartRefresh + 2-frameTolerance:
                # keep track of stop time/frame for later
                movie_end_2.tStop = t  # not accounting for scr refresh
                movie_end_2.frameNStop = frameN  # exact frame index
                win.timeOnFlip(movie_end_2, 'tStopRefresh')  # time at next scr refresh
                movie_end_2.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Movie_end_2Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Movie_end_2"-------
    for thisComponent in Movie_end_2Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    Block_2.addData('movie_end_2.started', movie_end_2.tStartRefresh)
    Block_2.addData('movie_end_2.stopped', movie_end_2.tStopRefresh)
    
    # set up handler to look after randomisation of conditions etc
    trials_2 = data.TrialHandler(nReps=14, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='trials_2')
    thisExp.addLoop(trials_2)  # add the loop to the experiment
    thisTrial_2 = trials_2.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial_2.rgb)
    if thisTrial_2 != None:
        for paramName in thisTrial_2:
            exec('{} = thisTrial_2[paramName]'.format(paramName))
    
    for thisTrial_2 in trials_2:
        currentLoop = trials_2
        # abbreviate parameter names if possible (e.g. rgb = thisTrial_2.rgb)
        if thisTrial_2 != None:
            for paramName in thisTrial_2:
                exec('{} = thisTrial_2[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "Trail_2"-------
        continueRoutine = True
        routineTimer.add(2.500000)
        # update component parameters for each repeat
        trail_2_cal.setText('var1[calcount]+"+"+$var2[calcount]')
        myEGI.ns.sync(fakeEgi.Netstation().getCurrentTime())
        myEGI.sendEventMarker('ca_b', Label='cal'+str(calcount)+'_start', description='something informative texts here', table={'RT':-1, 'Resp': ','})
        
        ticks = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        ftime.write("第"+str(calcount)+"次答题开始    "+ticks+"\t"+str(var1[calcount])+"+"+str(var2[calcount])+"\n")
        # keep track of which components have finished
        Trail_2Components = [trail_2_cal, trail_2_atten]
        for thisComponent in Trail_2Components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        Trail_2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Trail_2"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = Trail_2Clock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=Trail_2Clock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *trail_2_cal* updates
            if trail_2_cal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                trail_2_cal.frameNStart = frameN  # exact frame index
                trail_2_cal.tStart = t  # local t and not account for scr refresh
                trail_2_cal.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trail_2_cal, 'tStartRefresh')  # time at next scr refresh
                trail_2_cal.setAutoDraw(True)
            if trail_2_cal.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > trail_2_cal.tStartRefresh + 2-frameTolerance:
                    # keep track of stop time/frame for later
                    trail_2_cal.tStop = t  # not accounting for scr refresh
                    trail_2_cal.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(trail_2_cal, 'tStopRefresh')  # time at next scr refresh
                    trail_2_cal.setAutoDraw(False)
            
            # *trail_2_atten* updates
            if trail_2_atten.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
                # keep track of start time/frame for later
                trail_2_atten.frameNStart = frameN  # exact frame index
                trail_2_atten.tStart = t  # local t and not account for scr refresh
                trail_2_atten.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trail_2_atten, 'tStartRefresh')  # time at next scr refresh
                trail_2_atten.setAutoDraw(True)
            if trail_2_atten.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > trail_2_atten.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    trail_2_atten.tStop = t  # not accounting for scr refresh
                    trail_2_atten.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(trail_2_atten, 'tStopRefresh')  # time at next scr refresh
                    trail_2_atten.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Trail_2Components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Trail_2"-------
        for thisComponent in Trail_2Components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trials_2.addData('trail_2_cal.started', trail_2_cal.tStartRefresh)
        trials_2.addData('trail_2_cal.stopped', trail_2_cal.tStopRefresh)
        trials_2.addData('trail_2_atten.started', trail_2_atten.tStartRefresh)
        trials_2.addData('trail_2_atten.stopped', trail_2_atten.tStopRefresh)
        
        # ------Prepare to start Routine "trail_2_2"-------
        continueRoutine = True
        routineTimer.add(2.000000)
        # update component parameters for each repeat
        trial_2_judge.setText(display[calcount])
        trail_2_key_2.keys = []
        trail_2_key_2.rt = []
        _trail_2_key_2_allKeys = []
        myEGI.ns.sync(fakeEgi.Netstation().getCurrentTime())
        myEGI.sendEventMarker('judge_b', Label='judge'+str(calcount)+'_start', description='something informative texts here', table={'RT':-1, 'Resp': ','})
        # keep track of which components have finished
        trail_2_2Components = [trial_2_judge, trail_2_key_2]
        for thisComponent in trail_2_2Components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        trail_2_2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "trail_2_2"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = trail_2_2Clock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=trail_2_2Clock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *trial_2_judge* updates
            if trial_2_judge.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                trial_2_judge.frameNStart = frameN  # exact frame index
                trial_2_judge.tStart = t  # local t and not account for scr refresh
                trial_2_judge.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trial_2_judge, 'tStartRefresh')  # time at next scr refresh
                trial_2_judge.setAutoDraw(True)
            if trial_2_judge.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > trial_2_judge.tStartRefresh + 2-frameTolerance:
                    # keep track of stop time/frame for later
                    trial_2_judge.tStop = t  # not accounting for scr refresh
                    trial_2_judge.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(trial_2_judge, 'tStopRefresh')  # time at next scr refresh
                    trial_2_judge.setAutoDraw(False)
            
            # *trail_2_key_2* updates
            waitOnFlip = False
            if trail_2_key_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                trail_2_key_2.frameNStart = frameN  # exact frame index
                trail_2_key_2.tStart = t  # local t and not account for scr refresh
                trail_2_key_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trail_2_key_2, 'tStartRefresh')  # time at next scr refresh
                trail_2_key_2.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(trail_2_key_2.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(trail_2_key_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if trail_2_key_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > trail_2_key_2.tStartRefresh + 2-frameTolerance:
                    # keep track of stop time/frame for later
                    trail_2_key_2.tStop = t  # not accounting for scr refresh
                    trail_2_key_2.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(trail_2_key_2, 'tStopRefresh')  # time at next scr refresh
                    trail_2_key_2.status = FINISHED
            if trail_2_key_2.status == STARTED and not waitOnFlip:
                theseKeys = trail_2_key_2.getKeys(keyList=['1', '0'], waitRelease=False)
                _trail_2_key_2_allKeys.extend(theseKeys)
                if len(_trail_2_key_2_allKeys):
                    trail_2_key_2.keys = _trail_2_key_2_allKeys[0].name  # just the first key pressed
                    trail_2_key_2.rt = _trail_2_key_2_allKeys[0].rt
                    # was this correct?
                    if (trail_2_key_2.keys == str(correct_judge[calcount])) or (trail_2_key_2.keys == correct_judge[calcount]):
                        trail_2_key_2.corr = 1
                    else:
                        trail_2_key_2.corr = 0
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trail_2_2Components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "trail_2_2"-------
        for thisComponent in trail_2_2Components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trials_2.addData('trial_2_judge.started', trial_2_judge.tStartRefresh)
        trials_2.addData('trial_2_judge.stopped', trial_2_judge.tStopRefresh)
        # check responses
        if trail_2_key_2.keys in ['', [], None]:  # No response was made
            trail_2_key_2.keys = None
            # was no response the correct answer?!
            if str(correct_judge[calcount]).lower() == 'none':
               trail_2_key_2.corr = 1;  # correct non-response
            else:
               trail_2_key_2.corr = 0;  # failed to respond (incorrectly)
        # store data for trials_2 (TrialHandler)
        trials_2.addData('trail_2_key_2.keys',trail_2_key_2.keys)
        trials_2.addData('trail_2_key_2.corr', trail_2_key_2.corr)
        if trail_2_key_2.keys != None:  # we had a response
            trials_2.addData('trail_2_key_2.rt', trail_2_key_2.rt)
        trials_2.addData('trail_2_key_2.started', trail_2_key_2.tStartRefresh)
        trials_2.addData('trail_2_key_2.stopped', trail_2_key_2.tStopRefresh)
        
        ticks = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        ftime.write("第"+str(calcount)+"次答题结束    "+ticks+"\n")
        calcount=calcount+1
        thisExp.nextEntry()
        
    # completed 14 repeats of 'trials_2'
    
    thisExp.nextEntry()
    
# completed 5 repeats of 'Block_2'


# ------Prepare to start Routine "Break_2"-------
continueRoutine = True
routineTimer.add(3000.000000)
# update component parameters for each repeat
break_2_key.keys = []
break_2_key.rt = []
_break_2_key_allKeys = []
# keep track of which components have finished
Break_2Components = [break_2, break_2_key]
for thisComponent in Break_2Components:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
Break_2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "Break_2"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = Break_2Clock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=Break_2Clock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *break_2* updates
    if break_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        break_2.frameNStart = frameN  # exact frame index
        break_2.tStart = t  # local t and not account for scr refresh
        break_2.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(break_2, 'tStartRefresh')  # time at next scr refresh
        break_2.setAutoDraw(True)
    if break_2.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > break_2.tStartRefresh + 3000-frameTolerance:
            # keep track of stop time/frame for later
            break_2.tStop = t  # not accounting for scr refresh
            break_2.frameNStop = frameN  # exact frame index
            win.timeOnFlip(break_2, 'tStopRefresh')  # time at next scr refresh
            break_2.setAutoDraw(False)
    
    # *break_2_key* updates
    waitOnFlip = False
    if break_2_key.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        break_2_key.frameNStart = frameN  # exact frame index
        break_2_key.tStart = t  # local t and not account for scr refresh
        break_2_key.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(break_2_key, 'tStartRefresh')  # time at next scr refresh
        break_2_key.status = STARTED
        # keyboard checking is just starting
        waitOnFlip = True
        win.callOnFlip(break_2_key.clock.reset)  # t=0 on next screen flip
        win.callOnFlip(break_2_key.clearEvents, eventType='keyboard')  # clear events on next screen flip
    if break_2_key.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > break_2_key.tStartRefresh + 3000-frameTolerance:
            # keep track of stop time/frame for later
            break_2_key.tStop = t  # not accounting for scr refresh
            break_2_key.frameNStop = frameN  # exact frame index
            win.timeOnFlip(break_2_key, 'tStopRefresh')  # time at next scr refresh
            break_2_key.status = FINISHED
    if break_2_key.status == STARTED and not waitOnFlip:
        theseKeys = break_2_key.getKeys(keyList=['space'], waitRelease=False)
        _break_2_key_allKeys.extend(theseKeys)
        if len(_break_2_key_allKeys):
            break_2_key.keys = _break_2_key_allKeys[-1].name  # just the last key pressed
            break_2_key.rt = _break_2_key_allKeys[-1].rt
            # a response ends the routine
            continueRoutine = False
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in Break_2Components:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "Break_2"-------
for thisComponent in Break_2Components:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('break_2.started', break_2.tStartRefresh)
thisExp.addData('break_2.stopped', break_2.tStopRefresh)
# check responses
if break_2_key.keys in ['', [], None]:  # No response was made
    break_2_key.keys = None
thisExp.addData('break_2_key.keys',break_2_key.keys)
if break_2_key.keys != None:  # we had a response
    thisExp.addData('break_2_key.rt', break_2_key.rt)
thisExp.addData('break_2_key.started', break_2_key.tStartRefresh)
thisExp.addData('break_2_key.stopped', break_2_key.tStopRefresh)
thisExp.nextEntry()

# set up handler to look after randomisation of conditions etc
Block_3 = data.TrialHandler(nReps=5, method='random', 
    extraInfo=expInfo, originPath=-1,
    trialList=[None],
    seed=None, name='Block_3')
thisExp.addLoop(Block_3)  # add the loop to the experiment
thisBlock_3 = Block_3.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb = thisBlock_3.rgb)
if thisBlock_3 != None:
    for paramName in thisBlock_3:
        exec('{} = thisBlock_3[paramName]'.format(paramName))

for thisBlock_3 in Block_3:
    currentLoop = Block_3
    # abbreviate parameter names if possible (e.g. rgb = thisBlock_3.rgb)
    if thisBlock_3 != None:
        for paramName in thisBlock_3:
            exec('{} = thisBlock_3[paramName]'.format(paramName))
    
    # ------Prepare to start Routine "Movie_intro_3"-------
    continueRoutine = True
    routineTimer.add(1.500000)
    # update component parameters for each repeat
    # keep track of which components have finished
    Movie_intro_3Components = [movie_intro_3]
    for thisComponent in Movie_intro_3Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Movie_intro_3Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Movie_intro_3"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Movie_intro_3Clock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Movie_intro_3Clock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *movie_intro_3* updates
        if movie_intro_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            movie_intro_3.frameNStart = frameN  # exact frame index
            movie_intro_3.tStart = t  # local t and not account for scr refresh
            movie_intro_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(movie_intro_3, 'tStartRefresh')  # time at next scr refresh
            movie_intro_3.setAutoDraw(True)
        if movie_intro_3.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > movie_intro_3.tStartRefresh + 1.5-frameTolerance:
                # keep track of stop time/frame for later
                movie_intro_3.tStop = t  # not accounting for scr refresh
                movie_intro_3.frameNStop = frameN  # exact frame index
                win.timeOnFlip(movie_intro_3, 'tStopRefresh')  # time at next scr refresh
                movie_intro_3.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Movie_intro_3Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Movie_intro_3"-------
    for thisComponent in Movie_intro_3Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    Block_3.addData('movie_intro_3.started', movie_intro_3.tStartRefresh)
    Block_3.addData('movie_intro_3.stopped', movie_intro_3.tStopRefresh)
    
    # ------Prepare to start Routine "Movie_3"-------
    continueRoutine = True
    # update component parameters for each repeat
    movie_3 = visual.MovieStim3(
        win=win, name='movie_3',
        noAudio = False,
        filename=movies[moviecount],
        ori=0, pos=(0, 0), opacity=1,
        loop=False,
        size=(2240, 1400),
        depth=0.0,
        )
    myEGI.ns.sync(fakeEgi.Netstation().getCurrentTime())
    myEGI.sendEventMarker('mv_b', Label='movie'+str(moviecount)+'_begin', description='something informative texts here', table={'RT':-1, 'Resp': ','})
    
    ticks = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    ftime.write("视频"+str(moviecount)+"开始播放    "+ticks+"\n")
    # keep track of which components have finished
    Movie_3Components = [movie_3]
    for thisComponent in Movie_3Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Movie_3Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Movie_3"-------
    while continueRoutine:
        # get current time
        t = Movie_3Clock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Movie_3Clock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *movie_3* updates
        if movie_3.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
            # keep track of start time/frame for later
            movie_3.frameNStart = frameN  # exact frame index
            movie_3.tStart = t  # local t and not account for scr refresh
            movie_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(movie_3, 'tStartRefresh')  # time at next scr refresh
            movie_3.setAutoDraw(True)
        if movie_3.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > movie_3.tStartRefresh + movielenth[moviecount]-frameTolerance:
                # keep track of stop time/frame for later
                movie_3.tStop = t  # not accounting for scr refresh
                movie_3.frameNStop = frameN  # exact frame index
                win.timeOnFlip(movie_3, 'tStopRefresh')  # time at next scr refresh
                movie_3.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Movie_3Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Movie_3"-------
    for thisComponent in Movie_3Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    movie_3.stop()
    myEGI.ns.sync(fakeEgi.Netstation().getCurrentTime())
    myEGI.sendEventMarker('mv_e', Label='movie'+str(moviecount)+'_end', description='something informative texts here', table={'RT':-1, 'Resp': ','})
    ticks = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
    ftime.write("视频"+str(moviecount)+"结束播放    "+ticks+"\n")
    moviecount+=1
    # the Routine "Movie_3" was not non-slip safe, so reset the non-slip timer
    routineTimer.reset()
    
    # ------Prepare to start Routine "Movie_end_3"-------
    continueRoutine = True
    routineTimer.add(2.000000)
    # update component parameters for each repeat
    # keep track of which components have finished
    Movie_end_3Components = [movie_end_3]
    for thisComponent in Movie_end_3Components:
        thisComponent.tStart = None
        thisComponent.tStop = None
        thisComponent.tStartRefresh = None
        thisComponent.tStopRefresh = None
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    # reset timers
    t = 0
    _timeToFirstFrame = win.getFutureFlipTime(clock="now")
    Movie_end_3Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
    frameN = -1
    
    # -------Run Routine "Movie_end_3"-------
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = Movie_end_3Clock.getTime()
        tThisFlip = win.getFutureFlipTime(clock=Movie_end_3Clock)
        tThisFlipGlobal = win.getFutureFlipTime(clock=None)
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        # *movie_end_3* updates
        if movie_end_3.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
            # keep track of start time/frame for later
            movie_end_3.frameNStart = frameN  # exact frame index
            movie_end_3.tStart = t  # local t and not account for scr refresh
            movie_end_3.tStartRefresh = tThisFlipGlobal  # on global time
            win.timeOnFlip(movie_end_3, 'tStartRefresh')  # time at next scr refresh
            movie_end_3.setAutoDraw(True)
        if movie_end_3.status == STARTED:
            # is it time to stop? (based on global clock, using actual start)
            if tThisFlipGlobal > movie_end_3.tStartRefresh + 2-frameTolerance:
                # keep track of stop time/frame for later
                movie_end_3.tStop = t  # not accounting for scr refresh
                movie_end_3.frameNStop = frameN  # exact frame index
                win.timeOnFlip(movie_end_3, 'tStopRefresh')  # time at next scr refresh
                movie_end_3.setAutoDraw(False)
        
        # check for quit (typically the Esc key)
        if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
            core.quit()
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in Movie_end_3Components:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    # -------Ending Routine "Movie_end_3"-------
    for thisComponent in Movie_end_3Components:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    Block_3.addData('movie_end_3.started', movie_end_3.tStartRefresh)
    Block_3.addData('movie_end_3.stopped', movie_end_3.tStopRefresh)
    
    # set up handler to look after randomisation of conditions etc
    trials_3 = data.TrialHandler(nReps=14, method='random', 
        extraInfo=expInfo, originPath=-1,
        trialList=[None],
        seed=None, name='trials_3')
    thisExp.addLoop(trials_3)  # add the loop to the experiment
    thisTrial_3 = trials_3.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial_3.rgb)
    if thisTrial_3 != None:
        for paramName in thisTrial_3:
            exec('{} = thisTrial_3[paramName]'.format(paramName))
    
    for thisTrial_3 in trials_3:
        currentLoop = trials_3
        # abbreviate parameter names if possible (e.g. rgb = thisTrial_3.rgb)
        if thisTrial_3 != None:
            for paramName in thisTrial_3:
                exec('{} = thisTrial_3[paramName]'.format(paramName))
        
        # ------Prepare to start Routine "Trail_3"-------
        continueRoutine = True
        routineTimer.add(2.500000)
        # update component parameters for each repeat
        trail_3_cal.setText('var1[calcount]+"+"+$var2[calcount]')
        myEGI.ns.sync(fakeEgi.Netstation().getCurrentTime())
        myEGI.sendEventMarker('ca_b', Label='cal'+str(calcount)+'_start', description='something informative texts here', table={'RT':-1, 'Resp': ','})
        
        ticks = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        ftime.write("第"+str(calcount)+"次答题开始    "+ticks+"\t"+str(var1[calcount])+"+"+str(var2[calcount])+"\n")
        # keep track of which components have finished
        Trail_3Components = [trail_3_cal, trail_3_atten]
        for thisComponent in Trail_3Components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        Trail_3Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "Trail_3"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = Trail_3Clock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=Trail_3Clock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *trail_3_cal* updates
            if trail_3_cal.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                trail_3_cal.frameNStart = frameN  # exact frame index
                trail_3_cal.tStart = t  # local t and not account for scr refresh
                trail_3_cal.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trail_3_cal, 'tStartRefresh')  # time at next scr refresh
                trail_3_cal.setAutoDraw(True)
            if trail_3_cal.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > trail_3_cal.tStartRefresh + 2-frameTolerance:
                    # keep track of stop time/frame for later
                    trail_3_cal.tStop = t  # not accounting for scr refresh
                    trail_3_cal.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(trail_3_cal, 'tStopRefresh')  # time at next scr refresh
                    trail_3_cal.setAutoDraw(False)
            
            # *trail_3_atten* updates
            if trail_3_atten.status == NOT_STARTED and tThisFlip >= 2-frameTolerance:
                # keep track of start time/frame for later
                trail_3_atten.frameNStart = frameN  # exact frame index
                trail_3_atten.tStart = t  # local t and not account for scr refresh
                trail_3_atten.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trail_3_atten, 'tStartRefresh')  # time at next scr refresh
                trail_3_atten.setAutoDraw(True)
            if trail_3_atten.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > trail_3_atten.tStartRefresh + 0.5-frameTolerance:
                    # keep track of stop time/frame for later
                    trail_3_atten.tStop = t  # not accounting for scr refresh
                    trail_3_atten.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(trail_3_atten, 'tStopRefresh')  # time at next scr refresh
                    trail_3_atten.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Trail_3Components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "Trail_3"-------
        for thisComponent in Trail_3Components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trials_3.addData('trail_3_cal.started', trail_3_cal.tStartRefresh)
        trials_3.addData('trail_3_cal.stopped', trail_3_cal.tStopRefresh)
        trials_3.addData('trail_3_atten.started', trail_3_atten.tStartRefresh)
        trials_3.addData('trail_3_atten.stopped', trail_3_atten.tStopRefresh)
        
        # ------Prepare to start Routine "trail_3_2"-------
        continueRoutine = True
        routineTimer.add(2.000000)
        # update component parameters for each repeat
        trail_3_judge.setText(display[calcount])
        trail_3_key_2.keys = []
        trail_3_key_2.rt = []
        _trail_3_key_2_allKeys = []
        myEGI.ns.sync(fakeEgi.Netstation().getCurrentTime())
        myEGI.sendEventMarker('judge_b', Label='judge'+str(calcount)+'_start', description='something informative texts here', table={'RT':-1, 'Resp': ','})
        # keep track of which components have finished
        trail_3_2Components = [trail_3_judge, trail_3_key_2]
        for thisComponent in trail_3_2Components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        trail_3_2Clock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
        frameN = -1
        
        # -------Run Routine "trail_3_2"-------
        while continueRoutine and routineTimer.getTime() > 0:
            # get current time
            t = trail_3_2Clock.getTime()
            tThisFlip = win.getFutureFlipTime(clock=trail_3_2Clock)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *trail_3_judge* updates
            if trail_3_judge.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                trail_3_judge.frameNStart = frameN  # exact frame index
                trail_3_judge.tStart = t  # local t and not account for scr refresh
                trail_3_judge.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trail_3_judge, 'tStartRefresh')  # time at next scr refresh
                trail_3_judge.setAutoDraw(True)
            if trail_3_judge.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > trail_3_judge.tStartRefresh + 2-frameTolerance:
                    # keep track of stop time/frame for later
                    trail_3_judge.tStop = t  # not accounting for scr refresh
                    trail_3_judge.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(trail_3_judge, 'tStopRefresh')  # time at next scr refresh
                    trail_3_judge.setAutoDraw(False)
            
            # *trail_3_key_2* updates
            waitOnFlip = False
            if trail_3_key_2.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                trail_3_key_2.frameNStart = frameN  # exact frame index
                trail_3_key_2.tStart = t  # local t and not account for scr refresh
                trail_3_key_2.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(trail_3_key_2, 'tStartRefresh')  # time at next scr refresh
                trail_3_key_2.status = STARTED
                # keyboard checking is just starting
                waitOnFlip = True
                win.callOnFlip(trail_3_key_2.clock.reset)  # t=0 on next screen flip
                win.callOnFlip(trail_3_key_2.clearEvents, eventType='keyboard')  # clear events on next screen flip
            if trail_3_key_2.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > trail_3_key_2.tStartRefresh + 2-frameTolerance:
                    # keep track of stop time/frame for later
                    trail_3_key_2.tStop = t  # not accounting for scr refresh
                    trail_3_key_2.frameNStop = frameN  # exact frame index
                    win.timeOnFlip(trail_3_key_2, 'tStopRefresh')  # time at next scr refresh
                    trail_3_key_2.status = FINISHED
            if trail_3_key_2.status == STARTED and not waitOnFlip:
                theseKeys = trail_3_key_2.getKeys(keyList=['0', '1'], waitRelease=False)
                _trail_3_key_2_allKeys.extend(theseKeys)
                if len(_trail_3_key_2_allKeys):
                    trail_3_key_2.keys = _trail_3_key_2_allKeys[0].name  # just the first key pressed
                    trail_3_key_2.rt = _trail_3_key_2_allKeys[0].rt
                    # was this correct?
                    if (trail_3_key_2.keys == str(correct_judge[calcount])) or (trail_3_key_2.keys == correct_judge[calcount]):
                        trail_3_key_2.corr = 1
                    else:
                        trail_3_key_2.corr = 0
                    # a response ends the routine
                    continueRoutine = False
            
            # check for quit (typically the Esc key)
            if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
                core.quit()
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trail_3_2Components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # -------Ending Routine "trail_3_2"-------
        for thisComponent in trail_3_2Components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        trials_3.addData('trail_3_judge.started', trail_3_judge.tStartRefresh)
        trials_3.addData('trail_3_judge.stopped', trail_3_judge.tStopRefresh)
        # check responses
        if trail_3_key_2.keys in ['', [], None]:  # No response was made
            trail_3_key_2.keys = None
            # was no response the correct answer?!
            if str(correct_judge[calcount]).lower() == 'none':
               trail_3_key_2.corr = 1;  # correct non-response
            else:
               trail_3_key_2.corr = 0;  # failed to respond (incorrectly)
        # store data for trials_3 (TrialHandler)
        trials_3.addData('trail_3_key_2.keys',trail_3_key_2.keys)
        trials_3.addData('trail_3_key_2.corr', trail_3_key_2.corr)
        if trail_3_key_2.keys != None:  # we had a response
            trials_3.addData('trail_3_key_2.rt', trail_3_key_2.rt)
        trials_3.addData('trail_3_key_2.started', trail_3_key_2.tStartRefresh)
        trials_3.addData('trail_3_key_2.stopped', trail_3_key_2.tStopRefresh)
        
        ticks = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        ftime.write("第"+str(calcount)+"次答题结束    "+ticks+"\n")
        calcount=calcount+1
        thisExp.nextEntry()
        
    # completed 14 repeats of 'trials_3'
    
    thisExp.nextEntry()
    
# completed 5 repeats of 'Block_3'


# ------Prepare to start Routine "End"-------
continueRoutine = True
routineTimer.add(5.000000)
# update component parameters for each repeat
# keep track of which components have finished
EndComponents = [end]
for thisComponent in EndComponents:
    thisComponent.tStart = None
    thisComponent.tStop = None
    thisComponent.tStartRefresh = None
    thisComponent.tStopRefresh = None
    if hasattr(thisComponent, 'status'):
        thisComponent.status = NOT_STARTED
# reset timers
t = 0
_timeToFirstFrame = win.getFutureFlipTime(clock="now")
EndClock.reset(-_timeToFirstFrame)  # t0 is time of first possible flip
frameN = -1

# -------Run Routine "End"-------
while continueRoutine and routineTimer.getTime() > 0:
    # get current time
    t = EndClock.getTime()
    tThisFlip = win.getFutureFlipTime(clock=EndClock)
    tThisFlipGlobal = win.getFutureFlipTime(clock=None)
    frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
    # update/draw components on each frame
    
    # *end* updates
    if end.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
        # keep track of start time/frame for later
        end.frameNStart = frameN  # exact frame index
        end.tStart = t  # local t and not account for scr refresh
        end.tStartRefresh = tThisFlipGlobal  # on global time
        win.timeOnFlip(end, 'tStartRefresh')  # time at next scr refresh
        end.setAutoDraw(True)
    if end.status == STARTED:
        # is it time to stop? (based on global clock, using actual start)
        if tThisFlipGlobal > end.tStartRefresh + 5-frameTolerance:
            # keep track of stop time/frame for later
            end.tStop = t  # not accounting for scr refresh
            end.frameNStop = frameN  # exact frame index
            win.timeOnFlip(end, 'tStopRefresh')  # time at next scr refresh
            end.setAutoDraw(False)
    
    # check for quit (typically the Esc key)
    if endExpNow or defaultKeyboard.getKeys(keyList=["escape"]):
        core.quit()
    
    # check if all components have finished
    if not continueRoutine:  # a component has requested a forced-end of Routine
        break
    continueRoutine = False  # will revert to True if at least one component still running
    for thisComponent in EndComponents:
        if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
            continueRoutine = True
            break  # at least one component has not yet finished
    
    # refresh the screen
    if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
        win.flip()

# -------Ending Routine "End"-------
for thisComponent in EndComponents:
    if hasattr(thisComponent, "setAutoDraw"):
        thisComponent.setAutoDraw(False)
thisExp.addData('end.started', end.tStartRefresh)
thisExp.addData('end.stopped', end.tStopRefresh)
myEGI.ns.sync(fakeEgi.Netstation().getCurrentTime())
myEGI.sendEventMarker('ex_e', Label='experiment end', description='something informative texts here', table={'RT':-1, 'Resp': ','})

ticks = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
ftime.write("试验结束"+ticks+"\n")
ftime.close()

# Flip one final time so any remaining win.callOnFlip() 
# and win.timeOnFlip() tasks get executed before quitting
win.flip()

# these shouldn't be strictly necessary (should auto-save)
thisExp.saveAsWideText(filename+'.csv', delim='auto')
thisExp.saveAsPickle(filename)
logging.flush()
# make sure everything is closed down
thisExp.abort()  # or data files will save again on exit
win.close()
core.quit()

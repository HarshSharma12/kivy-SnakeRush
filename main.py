# -*- coding: utf-8 -*-
"""
Created on Tue Sep 30 8:44:03 2014

@author: Harsh Sharma
"""

import kivy
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.vector import Vector
from kivy.factory import Factory
from kivy.uix.widget import Widget
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.properties import ObjectProperty,DictProperty
from kivy.graphics import Line,Color,Rectangle
from kivy.lang import Builder
from math import floor
import sys


Builder.load_string('''
<ExitPopup>:
    size_hint: .6, .3
    title: 'SURE ?'
	Button:
		text: 'CLICK TO EXIT'
		on_press: sys.exit()

''')

class SnakeRushApp(App):
    def build(self):
        return GameSetup()

	
class GameSetup(BoxLayout):
    def __init__(self,**kwargs):
        super(GameSetup, self).__init__(**kwargs)
        self.root = FloatLayout()
        self.clear_widgets()
        self.orientation = "vertical"
        self.padding = 90
        self.spacing = 10
        self.pos_hint = {'x':0.22, 'y':0.05}
        normalButton = Button(text="NORMAL", size_hint = (0.4, 0.5))
        normalButton.bind(on_press = self.startNormal)
        
        hardButton = Button(text = "HARD", size_hint = (0.4, 0.5))
        hardButton.bind(on_press = self.startNormal)
        
        custButton = Button(text = "CUSTOM", size_hint = (0.4, 0.5))
        custButton.bind(on_press = self.startNormal)
        
        helpButton = Button(text = "HELP", size_hint = (0.4, 0.5))
        helpButton.bind(on_press = self.loadHelp)
        
        scoreButton = Button(text = "HIGH SCORES", size_hint = (0.4, 0.5))
        scoreButton.bind(on_press = self.loadScores)
        
        exitButton = Button(text = "EXIT", size_hint = (0.4, 0.5))
        exitButton.bind(on_press = self.askExit)
        
        for but in [normalButton, hardButton, custButton, helpButton, scoreButton, exitButton]:
            self.add_widget(but)
            
    def startNormal(self, obj):
        self.clear_widgets()
        game = SnakeRushGame()
        game.width = 800
        game.top = 600
        game.begin(self)
        Clock.schedule_interval(game.update,1.0/15.0)
        self.add_widget(game)
        return self
        
    def loadHelp(self,obj):
        #app = self
        self.clear_widgets()
        helpimg = Image(source = 'assets/help.jpg')
        back = Button(text = "BACK",font_size = 25)
        helpimg.add_widget(back)
        self.add_widget(helpimg)
        def backfn(obj):
            self.__init__()
        back.bind(on_press = backfn)
        return self
        
    def loadScores(self, obj):
        #app = self
        self.clear_widgets()
        helpimg = Image(source = 'assets/help.jpg')
        back = Button(text = "BACK",font_size = 25)
        helpimg.add_widget(back)
        self.add_widget(helpimg)
        def backfn(obj):
            self.__init__()
        back.bind(on_press = backfn)
        return self
    
    def askExit(self, obj):
        p = ExitPopup()
        p.open()

		
class ExitPopup(Popup):
    pass
	
		
class SnakeRushGame(Widget):
    a = dict()
    a['hello'] = 2 
    #These two steps are done just so that the dict is properly initialized.
    data = DictProperty(a)
    snake1 = ObjectProperty(None)
#    snake2 = ObjectProperty(None)
    
    def begin(self,root):
        self.root = root
        y=self.top
        x=self.width
        with self.canvas:
            Rectangle(pos=(0,0),size=(x/126,y))
            Rectangle(pos=(0,0),size=(x,y/80))
            Rectangle(pos=(x-x/126,0),size=(x/126,y))
            Rectangle(pos=(0,y-y/80),size=(x,y/80))
        self.data['div']=(160.0,92.0)
        self.data['pix']=(800.0,600.0)
        divx,divy = int(self.data['div'][0]),int(self.data['div'][1])
        print divx
        print ''
        print ''
        print divy
        self.data['occupied'] = list()
        print self.data
        
        for i in range(divx*divy):
            self.data['occupied'] += [0]
            '''
        for i in range(divx):
            self.data['occupied'][i]=1
            self.data['occupied'][-i-1]=1
        for i in range(divy):
            self.data['occupied'][i*divx]=1
        for i in range(1,divy+1):
            self.data['occupied'][(i*divx)-1]=1
        '''
        #Uncomment following to check if initial matrix is generated properly
        
        #print self.data.values()[2]
        
        self.snake1.pos = self.width/6,self.top/6
        #self.snake2.pos = self.width*5/6,self.top*5/6
        self.snake1.velocity = (8,0)
        #self.snake2.velocity = (-8,0)
        with self.canvas:
            Color(255,255,0)
            self.data["line1"] = Line(points = (self.snake1.center_x,self.snake1.center_y))
#            Color(0,191,255)
#            self.data["line2"] = Line(points = (self.snake2.center_x,self.snake2.center_y))
            
        #Change these images
    winner1 = Image(source = 'assets/bluewins.jpg')
    winner2 = Image(source = 'assets/yellowwins.jpg')

    def move_up(self):
        self.snake1.velocity = Vector(*self.snake1.velocity).rotate(90)
        if(self.snake1.velocity[1]<0):
            self.snake1.velocity[1]=-self.snake1.velocity[1]
        
    def move_down(self):
        self.snake1.velocity = Vector(*self.snake1.velocity).rotate(270)
        if(self.snake1.velocity[1]>0):
            self.snake1.velocity[1]=-self.snake1.velocity[1]

    def move_left(self):
        self.snake1.velocity = Vector(*self.snake1.velocity).rotate(90)
        if(self.snake1.velocity[0]>0):
            self.snake1.velocity[0]=-self.snake1.velocity[0]

    def move_right(self):
        self.snake1.velocity = Vector(*self.snake1.velocity).rotate(270)
        if(self.snake1.velocity[0]<0):
            self.snake1.velocity[0]=-self.snake1.velocity[0]
    

    def on_touch_down(self, touch): #FOR TOUCH ACTION
        self.t=[]
        touch.x, touch.y
        if(self.snake1.xarr[len(self.snake1.xarr)-1]-self.snake1.xarr[len(self.snake1.xarr)-2]==0):
            if(touch.x >= self.snake1.xarr[len(self.snake1.xarr)-1]):
                self.move_right()               
            else:
                self.move_left()                    
                
        elif(self.snake1.yarr[len(self.snake1.yarr)-1]-self.snake1.yarr[len(self.snake1.yarr)-2]==0):
            if(touch.y >= self.snake1.yarr[len(self.snake1.yarr)-1]):
                self.move_up()                    
            else:
                self.move_down()
                

#    touch_arr=[]
#    xdir = [0,0]
#    ydir = [0,0]
#    def on_touch_move(self, touch): #FOR SWIPE ACTION
#        self.touch_arr.append([touch.x, touch.y])
#        self.xdir = self.touch_arr[0][0] - self.touch_arr[len(self.touch_arr)-1][0]
#        self.ydir = self.touch_arr[0][1] - self.touch_arr[len(self.touch_arr)-1][1]
#        
#    def on_touch_up(self, touch):
#        
#        if(self.snake1.xarr[len(self.snake1.xarr)-1]-self.snake1.xarr[len(self.snake1.xarr)-2]==0): 
#            if(self.xdir>0 and self.ydir<15):
#                self.move_right()
#            elif(self.xdir<0 and self.ydir<15):
#                self.move_left()
#        elif(self.snake1.yarr[len(self.snake1.yarr)-1]-self.snake1.yarr[len(self.snake1.yarr)-2]==0):
#            if(self.xdir<15 and self.ydir>0):
#                self.move_up()
#            elif(self.xdir<15 and self.ydir<0):
#                self.move_down()
#        self.touch_arr=[]
#        
                    
                    
    def update(self,dt):
        a = self.snake1.move1(self.data)
        #b = self.snake2.move2(self.data)
        if (a)!=True:
            root = self.root
            #app = self.app
            root.clear_widgets()
            if a == False:
                root.add_widget(self.winner1)
#            if b == False:
#                root.add_widget(self.winner2)
#            
            return False

  
class Snake(Widget):
    def stop(self):
        exit(1)
    
    t = Clock.create_trigger(stop,timeout = 4)
    xarr=[]
    yarr=[]
    def move1(self,data):
        if self.check(data):
            return False
        self.pos = Vector(*self.velocity)+self.pos
        data["line1"].points += (self.center_x,self.center_y)
        n = self.convert(data)
        self.xarr.append(self.pos[0])
        self.yarr.append(self.pos[1])
        data['occupied'][n] = 1
        
        return True
    
    def move2(self,data):
        if self.check(data):
            return False
        self.pos = Vector(*self.velocity)+self.pos
        data["line2"].points += (self.center_x,self.center_y)
        n = self.convert(data)
        #print "    ",n
        data['occupied'][n] = 1
        return True
    
    def convert(self,data):
        x_pix,y_pix = data['pix']
        divx,divy = data['div']
        x,y = self.pos
        x = floor(float(x)/float(x_pix/divx))
        y = floor(float(y)/float(y_pix/divy))
        n = (divx)*y + x
        if n<divx*divy:
            return int(n)
        else:
            print "large value",n,self.pos,x,y
            return 300
    
    def convert1(self,pos,data):
        x_pix,y_pix = data['pix']
        divx,divy = data['div']
        x,y = pos
        x = floor(float(x)/float(x_pix/divx))
        y = floor(float(y)/float(y_pix/divy))
        n = (divx)*y + x
        if n<divx*divy:
            #Uncomment folowwing to debug
            ''''
            print "----------"
            print "check at",pos,int(n)
            '''
            return int(n)
        else:
            print "large value",n,self.pos,x,y
            return 300
    
    def check(self,data):
        pos = Vector(*self.velocity)+self.pos
        if data['occupied'][self.convert1(pos,data)]==1:
            #Uncomment the following to debug
            '''
            print self.uid,"Died at",pos,self.convert1(pos,data)
            print "game over"
            divx,divy = int(data['div'][0]),int(data['div'][1])
            m = dict()
            string = ""
            for i in range(divy):
                string = ""
            for j in range(divx):
                string  += str(data['occupied'][(i*divx)+j])
            #sys.stdout.write(str(data['occupied'][(i*divx)+j]))
            #print "\n
            m[str(i)]=str(string)
            for i in range(divy-1,-1,-1):
                print m[str(i)]
            '''
            return(1)

Factory.register("SnakeRushGame",SnakeRushGame)
Factory.register("Snake",Snake)


			
if __name__ in ('__main__'):
    SnakeRushApp().run()     


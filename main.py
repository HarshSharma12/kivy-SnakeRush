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
from kivy.uix.label import Label
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
from random import randint

Builder.load_string('''
<ExitPopup>:
    size_hint: .6, .3
    title: 'SURE ?'
	Button:
		text: 'CLICK TO EXIT'
		on_press: exit()

''')

class SnakeRushApp(App):
    def build(self):
        return GameSetup()

	
class GameSetup(BoxLayout):
    def __init__(self,**kwargs):
        '''############## INITIALIZE THE GAME by ##############
           ############## PLACING BUTTONS AND CALLING APPROPRIATE METHODS ##############'''
        super(GameSetup, self).__init__(**kwargs)
		
		############## NEXT 2 LINES APLICABLE ONLY AFTER SECOND CALL ##############
		
        self.root = FloatLayout()
        self.clear_widgets()
		
		############## ADD BUTTONS TO HOME SCREEN ##############
		
        self.orientation = "vertical"
        self.padding = 90
        self.spacing = 10
        self.pos_hint = {'x':0.22, 'y':0.05}
		
        normalButton = Button(text="SNAKE", size_hint = (0.4, 0.5))
        normalButton.bind(on_press = self.startNormal)
        
        hardButton = Button(text = "SNAKE RUSH", size_hint = (0.4, 0.5))
        hardButton.bind(on_press = self.startNormal)
        
        helpButton = Button(text = "HELP", size_hint = (0.4, 0.5))
        helpButton.bind(on_press = self.loadHelp)
        
        scoreButton = Button(text = "HIGH SCORES", size_hint = (0.4, 0.5))
        scoreButton.bind(on_press = self.loadScores)
        
        exitButton = Button(text = "EXIT", size_hint = (0.4, 0.5))
        exitButton.bind(on_press = self.askExit)
        
        for but in [normalButton, hardButton, helpButton, scoreButton, exitButton]:
            self.add_widget(but)
           
    def startNormal(self, obj):	
        '''############## BEGIN A NORMAL GAME - 2 SNAKES ##############	'''
        self.clear_widgets()
        game = SnakeRushGame()
        game.width = 800
        game.top = 600
        flag=1
        game.begin(self, flag)
        Clock.schedule_interval(game.update,1.0/15.0)
        self.add_widget(game)
        return self
        
    def loadHelp(self,obj):        
        '''############## LOAD THE HELP SCREEN ##############'''
        self.clear_widgets()
        text = """ """
        ht = open('D:\Others\kivy-SnakeRush\help.txt','r')
        for line in ht.readlines():
            text +=line
        print text
        self.add_widget(Label(text=text, markup=True))
        back = Button(text = "BACK",font_size = 15, size_hint = (0.15, 0.14), pos_hint = {'x':0, 'y':0})
        self.add_widget(back)        
        def backfn(obj):
            self.__init__()
        back.bind(on_press = backfn)
        ht.close()
        return self
        
    def loadScores(self, obj):
        '''############## LOAD THE HIGH SCORES ##############'''
        self.clear_widgets()
        text = """ """
        ht = open('D:\Others\kivy-SnakeRush\scores.txt','r')
        for line in ht.readlines():
            text +=line
        print text
        self.add_widget(Label(text=text, markup=True))
        back = Button(text = "BACK",font_size = 15, size_hint = (0.15, 0.14), pos_hint = {'x':0, 'y':0})
        self.add_widget(back)        
        def backfn(obj):
            self.__init__()
        back.bind(on_press = backfn)
        ht.close()
        return self
    
    def askExit(self, obj):
	'''############## TO CONFIRM ON EXIT ##############'''
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
    food1 = ObjectProperty(None)

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
        
        self.data['occupied'] = list()
        self.data['hbot'] = list()
        self.data['htop'] = list()
        self.data['vleft'] = list()
        self.data['vright'] = list()
        ## INITIALIZE THE ARRAY TO ALL ZEROS
        for i in range(divx*divy):
            self.data['occupied'] += [0]
        
        ## FOR GAME TO END ON HORIZONTAL BOUNDARY TOUCH
        for i in range(divx):
            if(flag==1):
                self.data['occupied'][i]=1
                self.data['occupied'][-i-1]=1
            else:
                self.data['hbot']+=1
                self.data['htop']+=1
            
        ## FOR GAME TO END ON VERTICAL BOUNDARY TOUCH
        for i in range(divy):
            if(flag==1):
                self.data['occupied'][i*divx]=1
            else:
                self.data['vleft']+=1
        for i in range(1,divy+1):
            if(flag==1):
                self.data['occupied'][(i*divx)-1]=1
            else:
                self.data['vright']+=1
        
        self.snake1.pos = self.width/6,self.top/6
        self.snake1.velocity = (8,0)
        with self.canvas:
            Color(255,255,0)
            self.data["line1"] = Line(points = (self.snake1.center_x,self.snake1.center_y))
            

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
    

    def on_touch_down(self, touch): #FOR SINGLE TOUCH
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
                

                    
    def update(self,dt):
        a = self.snake1.move1(self.data)
        self.food1.dispSprite(self.data)
        #b = self.snake2.move2(self.data)
        if (a)!=True:
            root = self.root
            #app = self.app
            root.clear_widgets()
            if a == False:
                ######### SPACE(After OVER) ONLY TO ALIGN THE TEXT #############
                over = """
                [anchor=title1][size=74]GAME OVER                      [/size]
                """
                score=""" """
                text = over+score
                root.add_widget(Label(text=text, markup=True))
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
        data["line1"].points = (self.center_x,self.center_y)
        self.xarr.append(self.pos[0])
        self.yarr.append(self.pos[1])
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
            return int(n)
        else:
            print "large value",n,self.pos,x,y
            return 300
    
    def check(self,data):
        pos = Vector(*self.velocity)+self.pos
        if data['occupied'][self.convert1(pos,data)]==1:
            return(1)


class Sprite(Widget):
    def dispSprite(self,data):
        x_pix,y_pix = data['pix']
        divx,divy = data['div']
        
        data['sprite'] = list()
        for i in range(int(divx*divy)):
            data['sprite'] += [0]
        
        x = 50
        y = 70
        sPos = x,y
        x = floor(float(x)/float(x_pix/divx))
        y = floor(float(y)/float(y_pix/divy))
        print sPos
        if(data['occupied'][int(x)]!=1):
            data['sprite'][int(x)] = 1;
        if(data['occupied'][int(y)]!=1):
            data['sprite'][int(y)] = 1;
        with self.canvas:
            Color(1, 1, 0, 1, mode='rgba')
            Rectangle(pos=sPos, size=(10,10))
        
        
        if(data['line1'].points == sPos):
            self.canvas.clear()
	
	
	
Factory.register("SnakeRushGame",SnakeRushGame)
Factory.register("Snake",Snake)


			
if __name__ in ('__main__'):
    SnakeRushApp().run()     


import pygame
import math
import random
try:
    # for Python2
    from Tkinter import *   ## notice capitalized T in Tkinter
    import tkFileDialog 
except ImportError:
    # for Python3
    from tkinter import *   ## notice lowercase 't' in tkinter here
    import tkinter.filedialog as tkFileDialog

Guardimage=pygame.image.load("Guard.png")
Wizardimage=pygame.image.load("Wizard.png")
Fireballimage=pygame.image.load("Fireball.png")
Characterimage=pygame.image.load("Hero.png")
def getDis(x,y,ox,oy):
    return math.sqrt((x-ox)**2+(y-oy)**2)
def rectcollide(a,b):
    if a[0]<b[0]+b[2] and a[0]+a[2]>b[0]:
        if a[1]<b[1]+b[3] and a[1]+a[3]>b[1]:
            return True
    return False
class Moveable:
    def __init__(self,x,y,image):
        self.x=x
        self.y=y
        self.row=0
        self.index=0
        self.frames=1
        self.animspeed=0.15
        self.image=image
        self.collideable=True
        self.health=100
        self.maxhealth=100
        self.mana=0
        self.maxmana=0
        self.healthregen=0.06
        self.manaregen=1#0.08
        self.alive=True
    def hurt(self,amount):
        self.health-=amount
        if self.health<=0:
            self.health=0
            self.alive=False
    def update(self,moveables):
        self.health+=self.healthregen
        if self.health>self.maxhealth:
            self.health=self.maxhealth
        self.mana+=self.manaregen
        if self.mana>self.maxmana:
            self.mana=self.maxmana
        self.index+=self.animspeed
        if self.index>=self.frames:
            self.index=0
    def move(self,newx,newy,moveables):
        if not self.willcollide(newx,newy,moveables):
            self.x=newx
            self.y=newy
    def willcollide(self,x,y,moveables):
        for moveable in moveables:
            if moveable.collideable and moveable != self and rectcollide((x,y,128,128),(moveable.x,moveable.y,128,128)):
                return True
        y1=0
        for line in self.backgroundmap:
            x1=0
            for char in line:
                if char in "i":
                    if rectcollide((x1*128,y1*128,128,128),(x,y,128,128)):
                        return True
                x1+=1
            y1+=1
        if x+128>1280:
            return True
        if y+128>768:
            return True
        if x<0:
            return True
        if y<0:
            return True
        return False
    def draw(self,surface):
        surface.blit(self.image,(self.x,self.y),(int(self.index)*128,self.row*128,128,128))
        health=self.health/float(self.maxhealth)
        pygame.draw.rect(surface,(100,100,100),(self.x,self.y,128,12))
        if health>0.5:
            color=(int(255-(health-0.5)*2*255),255,0)
        else:
            color=(255,int(health*2*255),0)
        pygame.draw.rect(surface,color,(self.x+3,self.y+3,122*health,6))
        if self.maxmana>0:
            pygame.draw.rect(surface,(100,100,100),(self.x,self.y+116,128,12))
            pygame.draw.rect(surface,(0,0,255),(self.x+3,self.y+119,122*self.mana/self.maxmana,6))
class Guard(Moveable):
    def __init__(self,x,y,backgroundmap):
        Moveable.__init__(self,x,y,Guardimage)
        self.backgroundmap=backgroundmap
        self.frames=4
        self.row=0
    def update(self,moveables,mode,keys,newkeys):
        Moveable.update(self,moveables)
        if mode == 2:
            found=False
            for moveable in moveables:
                if moveable.gettype()=="character":
                    # Character to right
                    if rectcollide((moveable.x,moveable.y,128,128),(self.x+128,self.y,64,128)):
                        self.row=7
                        self.frames=10
                        found=True
                        if round(self.index,1)==5:
                            moveable.hurt(random.randint(7,13))
                    # Character to left
                    if rectcollide((moveable.x,moveable.y,128,128),(self.x-64,self.y,64,128)):
                        self.row=4
                        self.frames=10
                        found=True
                        if round(self.index,1)==5:
                            moveable.hurt(random.randint(7,13))
                    # Character to up
                    if rectcollide((moveable.x,moveable.y,128,128),(self.x,self.y-64,128,64)):
                        self.row=6
                        self.frames=10
                        found=True
                        if round(self.index,1)==5:
                            moveable.hurt(random.randint(7,13))
                    # Character to down
                    if rectcollide((moveable.x,moveable.y,128,128),(self.x,self.y+128,128,64)):
                        self.row=5
                        self.frames=10
                        found=True
                        if round(self.index,1)==5:
                            moveable.hurt(random.randint(7,13))
            if not found and self.row>3:
                self.row-=4
                self.frames=4
    def gettype(self):
        return "guard"
class Wizard(Moveable):
    def __init__(self,x,y,backgroundmap):
        Moveable.__init__(self,x,y,Wizardimage)
        self.backgroundmap=backgroundmap
        self.maxmana=100
        self.mana=100
        self.frames=8
        self.row=0
        self.spelling=False
    def update(self,moveables,mode,keys,newkeys):
        Moveable.update(self,moveables)
        if round(self.index,1)==9:
            self.spelling=False
            self.frames=8
            self.row=0
            self.index=0
        if mode == 2:
            poses=[]
            for moveable in moveables:
                if moveable.gettype()=="character":
                    poses+=[[moveable.x,moveable.y]]
            if len(poses)>0:
                for pos in poses:
                    pos+=[getDis(pos[0],pos[1],self.x,self.y)]
                m=poses[0]
                for pos in poses:
                    if pos[2]<m[2]:
                        m=pos
                self.row=self.row%4
                if m[1]<self.y:
                    self.move(self.x,self.y-1,moveables)
                    self.row=2
                elif m[1]>self.y:
                    self.move(self.x,self.y+1,moveables)
                    self.row=1
                if m[0]<self.x:
                    self.move(self.x-1,self.y,moveables)
                    self.row=0
                elif m[0]>self.x:
                    self.move(self.x+1,self.y,moveables)
                    self.row=3
                if self.spelling:
                    self.row+=4
                    self.frames=10
                    if round(self.index,1)==5:
                        if self.mana>=20:
                            moveables.append(Fireball(math.atan2(self.y-m[1],self.x-m[0]),20,self,self.backgroundmap))
                            self.mana-=20
                elif self.mana>=20 and random.randint(0,100)==0:
                    self.spelling=True
    def gettype(self):
        return "wizard"
class Fireball(Moveable):
    def __init__(self,direction,damage,owner,backgroundmap):
        Moveable.__init__(self,owner.x,owner.y,Fireballimage)
        self.backgroundmap=backgroundmap
        self.direction=direction
        self.damage=damage
        self.collideable=False
        self.frames=6
        self.row=0
        self.owner=owner
    def update(self,moveables,mode,keys,newkeys):
        Moveable.update(self,moveables)
        if mode == 2:
            newrect=(self.x-math.cos(self.direction)*5,self.y-math.sin(self.direction)*5,128,128)
            for moveable in moveables:
                if moveable != self.owner and moveable != self and moveable.gettype()!="fireball" and rectcollide(newrect,(moveable.x,moveable.y,128,128)):
                    
                    moveable.hurt(self.damage)
                    self.alive=False
                    break
            else:
                self.x=newrect[0]
                self.y=newrect[1]

        if self.x+128>1280:
            self.alive = False
        if self.y+128>768:
            self.alive = False
        if self.x<0:
            self.alive = False
        if self.y<0:
            self.alive = False
    def draw(self,surface):
        surface.blit(self.image,(self.x,self.y),(int(self.index)*128,self.row%self.frames*128,128,128))
    def gettype(self):
        return "fireball"
class Character(Moveable):
    def __init__(self,x,y,backgroundmap,num):
        a=pygame.PixelArray(Characterimage.copy())
        a.replace ((5,104,57), (12345*num%256,3256*num%256,12354*num%256), distance=0, weights=(0.299, 0.587, 0.114))
        a=a.make_surface()
        Moveable.__init__(self,x,y,a)
        self.backgroundmap=backgroundmap
        self.mana=100
        self.maxmana=100
        self.frames=4
        self.row=0
        self.ismoving=False
        self.swinging=False
        self.code=""
        self.animspeed=0.2
    def update(self,moveables,mode,keys,newkeys):
        Moveable.update(self,moveables)
        if mode == 2:
            self.moveables=moveables
            try:
                exec(self.code,{"keys":keys,"newkeys":newkeys,"pygame":pygame,"summonFireball":self.summonFireball,"pointup":self.pointup,"pointdown":self.pointdown,"pointleft":self.pointleft,"pointright":self.pointright,"moving":self.moving,"swingsword":self.swingsword},{})
            except Exception as e:
                print ("your code had an error:",e)
            if (self.row<4 or self.row>7) and self.swinging:
                self.row=self.row%4+4
            if self.row<8 and (not self.swinging) and self.ismoving:
                self.row=self.row%4+8
            if not self.swinging and not self.ismoving:
                self.row=self.row%4
            if self.swinging and round(self.index,1)==9:
                self.frames=4
                self.row%=4
                self.index=0
                self.swinging=False
            if self.ismoving and not self.swinging:
                if self.row%4==0:
                    self.move(self.x-2,self.y,moveables)
                if self.row%4==1:
                    self.move(self.x,self.y+2,moveables)
                if self.row%4==2:
                    self.move(self.x,self.y-2,moveables)
                if self.row%4==3:
                    self.move(self.x+2,self.y,moveables)
            if round(self.index,1)==5:
                for moveable in moveables:
                    if moveable.gettype()!="fireball":
                        if self.row%4==0:
                            if rectcollide((self.x-64,self.y,64,128),(moveable.x,moveable.y,128,128)):
                                moveable.hurt(random.randint(17,23))
                        if self.row%4==1:
                            if rectcollide((self.x,self.y+128,128,64),(moveable.x,moveable.y,128,128)):
                                moveable.hurt(random.randint(17,23))
                        if self.row%4==2:
                            if rectcollide((self.x,self.y-64,128,64),(moveable.x,moveable.y,128,128)):
                                moveable.hurt(random.randint(17,23))
                        if self.row%4==3:
                            if rectcollide((self.x+128,self.y,64,128),(moveable.x,moveable.y,128,128)):
                                moveable.hurt(random.randint(17,23))
                            
    def summonFireball(self,damage,direction):
        if self.mana>=damage:
            self.moveables.append(Fireball(direction,damage,self,self.backgroundmap))
            self.mana-=damage
            return True
        return False
    def pointup(self):
        self.row=2
    def pointdown(self):
        self.row=1
    def pointleft(self):
        self.row=0
    def pointright(self):
        self.row=3
    def moving(self,val):
        self.ismoving=val
    def swingsword(self):
        if not self.swinging:
            self.index=0
        if (self.row<4 or self.row>7) and self.swinging:
            self.row=self.row%4+4
        self.swinging=True
        self.frames=10 
    def gettype(self):
        return "character"
def openmap(f,tiles):
    lines=f.read().split("\n")
    width=int(lines[0])
    height=int(lines[1])
    backgroundmap=[list(lines[i]) for i in range(2,height+2)]
    backgroundimage=pygame.Surface((width*128,height*128))
    y=0
    for line in backgroundmap:
        x=0
        for char in line:
            backgroundimage.blit(tiles[char],(x*128,y*128))
            x+=1
        y+=1
    moveables=[]
    c=0
    for line in range(height+1,len(lines)):
        a=lines[line].split(" ")
        if a[0]=="g":
            moveables.append(Guard(int(a[1])*128,int(a[2])*128,backgroundmap))
        if a[0]=="c":
            c+=3
            moveables.append(Character(int(a[1])*128,int(a[2])*128,backgroundmap,c))
        if a[0]=="w":
            moveables.append(Wizard(int(a[1])*128,int(a[2])*128,backgroundmap))
    return width,height,backgroundmap,backgroundimage,moveables
def main():
    pygame.init()
    size=(1280,768)
    surface=pygame.display.set_mode(size)
    clock=pygame.time.Clock()
    keys=[]
    newkeys = []
    tiles={"c":pygame.image.load("rock1.png"),
           "d":pygame.image.load("rock2.png"),
           "a":pygame.image.load("Ground.png"),
           "b":pygame.image.load("Ground2.png"),
           "e":pygame.image.load("Door1.png"),
           "f":pygame.image.load("Door2.png"),
           "g":pygame.image.load("Wall1.png"),
           "h":pygame.image.load("Wall2.png"),
           "i":pygame.image.load("Wall3.png")}
    width,height,backgroundmap,backgroundimage,moveables=openmap(open("map.txt","r"),tiles)
    running=True
    mode=1
    Characterimage.convert()
    Guardimage.convert()
    Characterimage.set_colorkey((255,255,255))
    Guardimage.set_colorkey((255,255,255))
    Characterimage.convert_alpha()
    Guardimage.convert_alpha()
    myCodeHere=None
    while running:
        clock.tick(60)
        surface.fill((255,0,0))
        surface.blit(backgroundimage,(0,0))
        newkeys=[]
        for event in pygame.event.get():
            if event.type==pygame.KEYDOWN:
                keys.append(event.key)
                newkeys.append(event.key)
            if event.type==pygame.KEYUP:
                if event.key in keys:
                    keys.remove(event.key)
            if event.type==pygame.QUIT:
                running=False
        if pygame.K_r in newkeys:
            width,height,backgroundmap,backgroundimage,moveables=openmap(open("map.txt","r"),tiles)
            mode=1
        for moveable in moveables:
            moveable.update(moveables,mode,keys,newkeys)
            moveable.draw(surface)
        if mode == 1:
            if pygame.mouse.get_pressed()[0]:
                for moveable in moveables:
                    if moveable.gettype()=="character":
                        if pygame.mouse.get_pos()[0]>moveable.x and pygame.mouse.get_pos()[0]<moveable.x+128:
                            if pygame.mouse.get_pos()[1]>moveable.y and pygame.mouse.get_pos()[1]<moveable.y+128:
                                pygame.draw.rect(surface,(255,255,0),(moveable.x,moveable.y,128,128),5)
                                pygame.display.flip()
                                root = Tk()
                                filename = tkFileDialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = (("python scripts","*.py"),))
                                root.destroy()
                                if len(filename)>0:
                                    print (filename)
                                    moveable.code=open(filename,"r").read()
            if pygame.K_RETURN in newkeys:
                mode = 2
        moveables=[i for i in moveables if i.alive]
        pygame.display.flip()
    pygame.quit()
main()

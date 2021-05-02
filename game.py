#导入模块
import pygame
from  random import choice,randint
from time import time
from math import atan2,cos,sin,pi
pygame.init()


#定义类与函数
class Hero(pygame.sprite.Sprite): #角色类
    def __init__(self,image_file,speed,life):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = [size[0]/2,size[1]/2]
        self.speed=speed
        self.life=life
        self.charge=0
        self.attack=hero_attack
        self.attack_interval=attack_interval
    def turn(self, change):#根据用户输出方向改变位置偏移量，同时更改角色动作
        center = self.rect.center
        if(change==[0,-1]):
            self.image = pygame.image.load(hero_motion_images[0])
        if(change==[-1,-1]):
            self.image = pygame.image.load(hero_motion_images[1])
        if(change==[-1,0]):
            self.image = pygame.image.load(hero_motion_images[2])
        if(change==[-1,1]):
            self.image = pygame.image.load(hero_motion_images[3])
        if(change==[0,1]):
            self.image = pygame.image.load(hero_motion_images[4])
        if(change==[1,1]):
            self.image = pygame.image.load(hero_motion_images[5])
        if(change==[1,0]):
            self.image = pygame.image.load(hero_motion_images[6])
        if(change==[1,-1]):
            self.image = pygame.image.load(hero_motion_images[7])            
        self.rect = self.image.get_rect()
        self.rect.center = center
        if change[0]==change[1] or change[0]+change[1]==0:
            change[0]/=pow(2,0.5)
            change[1]/=pow(2,0.5)
        self.change = [change[0]*self.speed,change[1]*self.speed]
        
    def move(self):#设定下一动作坐标，同时限定在窗口内运动
        self.rect.centerx = self.rect.centerx + self.change[0]
        if self.rect.centerx < self.rect.width/2: 
            self.rect.centerx = self.rect.width/2
        if self.rect.centerx > size[0]-self.rect.width/2: 
            self.rect.centerx = size[0]-self.rect.width/2
        self.rect.centery = self.rect.centery + self.change[1]
        if self.rect.centery < self.rect.height/2: 
            self.rect.centery = self.rect.height/2
        if self.rect.centery > size[1]-self.rect.height/2: 
            self.rect.centery = size[1]-self.rect.height/2
    
    def skill_shift(self,on):
        if on==1 and self.speed<=hero_speed+shift_buff:
            self.speed+=shift_buff
        else:
            self.speed=hero_speed
    
        
class HeroAttack(pygame.sprite.Sprite):#角色普通攻击类
    def __init__(self,image_file,speed,hero,loc):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.transform.scale(pygame.image.load(image_file),(15,15))
        self.rect = self.image.get_rect()
        self.rect.center = hero.rect.center
        self.distance=[loc[i]-self.rect.center[i] for i in range(2)]
        self.speed=speed
        
    def out_range(self):#是否超出地图
        if self.rect.bottom>height:
            return 1
        if self.rect.top<0:
            return 1
        if self.rect.left<0:
            return 1
        if self.rect.right>width:
            return 1
        else:
            return 0
    def move(self):#进行移动
        self.rect.centerx+=self.distance[0]/pow(pow(self.distance[0],2)+pow(self.distance[1],2),0.5)*self.speed
        self.rect.centery+=self.distance[1]/pow(pow(self.distance[0],2)+pow(self.distance[1],2),0.5)*self.speed
        
class Skill_E(pygame.sprite.Sprite):
    def __init__(self,hero,loc):
        pygame.sprite.Sprite.__init__(self) 
        self.point=[loc[i]-hero.rect.center[i] for i in range(2)]
        self.angle=atan2(-self.point[1],self.point[0])/pi*180-90
        self.image = pygame.transform.rotate(skill_e_image,self.angle)
        self.rect = self.image.get_rect()
        if pow(pow(self.point[0],2)+pow(self.point[1],2),0.5)==0:
            pass;
        else:
            self.rect.center=(skill_e_image_height/2*self.point[0]/pow(pow(self.point[0],2)+pow(self.point[1],2),0.5)+hero.rect.centerx,skill_e_image_height/2*self.point[1]/pow(pow(self.point[0],2)+pow(self.point[1],2),0.5)+hero.rect.centery)
        
    def turn(self,loc):
        self.point=[loc[i]-hero.rect.center[i] for i in range(2)]
        self.angle=atan2(-self.point[1],self.point[0])/pi*180-90
        self.image = pygame.transform.rotate(skill_e_image,self.angle)
        self.rect = self.image.get_rect()
        if pow(pow(self.point[0],2)+pow(self.point[1],2),0.5)==0:
            pass;
        else:
            self.rect.center=(skill_e_image_height/2*self.point[0]/pow(pow(self.point[0],2)+pow(self.point[1],2),0.5)+hero.rect.centerx,skill_e_image_height/2*self.point[1]/pow(pow(self.point[0],2)+pow(self.point[1],2),0.5)+hero.rect.centery)
        
class Skill_Q(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.transform.scale(pygame.image.load(skill_q_image[0]),(q_size,q_size))
        self.rect = self.image.get_rect()
        self.rect.center=hero.rect.center
    
    def turn(self,n):
        self.image = pygame.transform.scale(pygame.image.load(skill_q_image[n]),(q_size,q_size))

class Item(pygame.sprite.Sprite):
    def __init__(self,image_file,num):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.image.load(image_file[num])
        self.rect = self.image.get_rect()
        self.rect.center = [randint(0, width),randint(0, height)]
        self.num=num
    
    def activate(self):
        if self.num==0:
            if hero.life+2<=life:
                hero.life+=2
            else:
                hero.life=life
            
        if self.num==1:
            hero.attack_interval/=2
        
        if self.num==2:
            hero.charge+=30
    
        if self.num==3:
            hero.attack*=2
        
            
class NormalEnemy(pygame.sprite.Sprite): #普通敌人类
    def __init__(self,image_file,boss_call):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.transform.scale(pygame.image.load(image_file),(35,45))
        self.rect = self.image.get_rect()
        if boss_call==1:
            self.rect.center=[boss.rect.centerx+randint(-200,200),boss.rect.centery+randint(-200,200)]
        else:
            self.rect.center = choice([[0,randint(0,height)],[width,randint(0,height)],[randint(0,width),0],[randint(0,width),height]])
        self.distance=[hero.rect.center[i]-self.rect.center[i] for i in range(2)]
        self.speed=normalenemy_speed
        self.life=normalenemy_life
        self.attack=normalenemy_attack
        self.hurt_time=1
    def update(self,hero):
        self.distance=[hero.rect.center[i]-self.rect.center[i] for i in range(2)]
        if pow(pow(self.distance[0],2)+pow(self.distance[1],2),0.5)==0:
            pass
        else:
            self.rect.centerx+=self.distance[0]/pow(pow(self.distance[0],2)+pow(self.distance[1],2),0.5)*self.speed
            self.rect.centery+=self.distance[1]/pow(pow(self.distance[0],2)+pow(self.distance[1],2),0.5)*self.speed
        
class RangeEnemy(pygame.sprite.Sprite): #远程敌人类
    def __init__(self,image_file,boss_call):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.transform.scale(pygame.image.load(image_file),(35,45))
        self.rect = self.image.get_rect()
        if boss_call==1:
            self.rect.center=[boss.rect.centerx+randint(-200,200),boss.rect.centery+randint(-200,200)]
        else:
            self.rect.center = choice([[0,randint(0,height)],[width,randint(0,height)],[randint(0,width),0],[randint(0,width),height]])
        self.distance=[hero.rect.center[i]-self.rect.center[i] for i in range(2)]
        self.speed=rangeenemy_speed
        self.life=rangeenemy_life
        self.attack=rangeenemy_attack
        self.last_rangeenemy_attack_time=time()
        self.hurt_time=1
        
    def update(self,hero):
        self.distance=[hero.rect.center[i]-self.rect.center[i] for i in range(2)]
        if ((self.rect.centerx-hero.rect.centerx)**2+(self.rect.centery-hero.rect.centery)**2)**0.5<=400:
            pass
        elif pow(pow(self.distance[0],2)+pow(self.distance[1],2),0.5)==0:
            pass
        else:
            self.rect.centerx+=self.distance[0]/pow(pow(self.distance[0],2)+pow(self.distance[1],2),0.5)*self.speed
            self.rect.centery+=self.distance[1]/pow(pow(self.distance[0],2)+pow(self.distance[1],2),0.5)*self.speed

class EnemyAttack(pygame.sprite.Sprite):#远程敌人攻击类
    def __init__(self,image_file,rn):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.transform.scale(pygame.image.load(image_file),(15,15))
        self.rect = self.image.get_rect()
        self.rect.center = rn.rect.center
        self.distance=[hero.rect.center[i]-self.rect.center[i] for i in range(2)]
        self.speed=ammo_speed
        self.attack=rangeenemy_attack

    def out_range(self):#是否超出地图
        if self.rect.bottom>height:
            return 1
        if self.rect.top<0:
            return 1
        if self.rect.left<0:
            return 1
        if self.rect.right>width:
            return 1
        else:
            return 0
    def move(self):#进行移动
        self.rect.centerx+=self.distance[0]/pow(pow(self.distance[0],2)+pow(self.distance[1],2),0.5)*self.speed
        self.rect.centery+=self.distance[1]/pow(pow(self.distance[0],2)+pow(self.distance[1],2),0.5)*self.speed
class StrongEnemy(pygame.sprite.Sprite): #强壮敌人类
    def __init__(self,image_file,boss_call):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.transform.scale(pygame.image.load(image_file),(60,60))
        self.rect = self.image.get_rect()
        if boss_call==1:
            self.rect.center=[boss.rect.centerx+randint(-200,200),boss.rect.centery+randint(-200,200)]
        else:
            self.rect.center = choice([[0,randint(0,height)],[width,randint(0,height)],[randint(0,width),0],[randint(0,width),height]])
        self.distance=[hero.rect.center[i]-self.rect.center[i] for i in range(2)]
        self.speed=strongenemy_speed
        self.attack=strongenemy_attack
        self.life=strongenemy_life
        self.last_strongenemy_attack_time=time()
        self.hurt_time=1
        
    def update(self,hero):
        self.distance=[hero.rect.center[i]-self.rect.center[i] for i in range(2)]
        if pow(pow(self.distance[0],2)+pow(self.distance[1],2),0.5)==0:
            pass;
        else:
            self.rect.centerx+=self.distance[0]/pow(pow(self.distance[0],2)+pow(self.distance[1],2),0.5)*self.speed
            self.rect.centery+=self.distance[1]/pow(pow(self.distance[0],2)+pow(self.distance[1],2),0.5)*self.speed

class Boss(pygame.sprite.Sprite): #Boss类
    def __init__(self,image_file):
        pygame.sprite.Sprite.__init__(self) 
        self.image = pygame.transform.scale(pygame.image.load(image_file),(100,100))
        self.rect = self.image.get_rect()
        self.rect.center = choice([[0,randint(0,height)],[width,randint(0,height)],[randint(0,width),0],[randint(0,width),height]])
        self.distance=[hero.rect.center[i]-self.rect.center[i] for i in range(2)]
        self.speed=boss_speed
        self.attack=boss_attack
        self.life=boss_life
        self.last_boss_attack_time=0
        self.boss_call_time=0
        self.hurt_time=1
    def call(self,kind):
        if kind==1:
            normalenemy_group.add(NormalEnemy(normalenemy_image,1))
    
        if kind==2:
            rangeenemy_group.add(RangeEnemy(rangeenemy_image,1))
    
        if kind==3:
            strongenemy_group.add(StrongEnemy(strongenemy_image,1))
  
            
    def update(self,hero):
        self.distance=[hero.rect.center[i]-self.rect.center[i] for i in range(2)]
        if ((self.rect.centerx-hero.rect.centerx)**2+(self.rect.centery-hero.rect.centery)**2)**0.5<=350:
            pass
        elif pow(pow(self.distance[0],2)+pow(self.distance[1],2),0.5)==0:
            pass
        else:
            self.rect.centerx+=self.distance[0]/pow(pow(self.distance[0],2)+pow(self.distance[1],2),0.5)*self.speed
            self.rect.centery+=self.distance[1]/pow(pow(self.distance[0],2)+pow(self.distance[1],2),0.5)*self.speed
            
def e_collide():
     p1=[skill_e.rect.centerx-cos(skill_e.angle*pi/180)*skill_e_image_width/2,skill_e.rect.centery+sin(skill_e.angle*pi/180)*skill_e_image_width/2]
     p2=[skill_e.rect.centerx+cos(skill_e.angle*pi/180)*skill_e_image_width/2,skill_e.rect.centery-sin(skill_e.angle*pi/180)*skill_e_image_width/2]
     p3=[skill_e.rect.centerx-sin(skill_e.angle*pi/180)*skill_e_image_height/2,skill_e.rect.centery-cos(skill_e.angle*pi/180)*skill_e_image_height/2]
     p4=[skill_e.rect.centerx+sin(skill_e.angle*pi/180)*skill_e_image_height/2,skill_e.rect.centery+cos(skill_e.angle*pi/180)*skill_e_image_height/2]
     if (p1[0]-p2[0])==0:
         k1=1
         b1=-p2[0]
         y1=0
     else:
         k1=(p1[1]-p2[1])/(p1[0]-p2[0])
         b1=p1[1]-k1*p1[0]
         y1=1
     if (p3[0]-p4[0])==0:
         k2=1
         b2=-p3[0]
         y2=0
     else:
         k2=(p3[1]-p4[1])/(p3[0]-p4[0])
         y2=1
         b2=p3[1]-k2*p3[0]
     
     return k1,y1,b1,k2,y2,b2

def recover(num):
    if num==1:
        hero.attack_interval=attack_interval
    if num==3:
        hero.attack=hero_attack
             
def refresh(): #刷新窗口
    screen.blit(map_image,(0,0))
    screen.blit(hero.image, hero.rect)
    if skill_e_on==1:
        screen.blit(skill_e.image,skill_e.rect)
    if time()-q_start_time<=3:
        screen.blit(skill_q.image,skill_q.rect)
    item_group.draw(screen)
    attack_group.draw(screen)
    if stage==1:
        normalenemy_group.draw(screen)
    elif stage==2:
        normalenemy_group.draw(screen)
        rangeenemy_group.draw(screen)
        rangeenemy_attack_group.draw(screen)
    elif stage==3:
        normalenemy_group.draw(screen)
        rangeenemy_group.draw(screen)
        rangeenemy_attack_group.draw(screen)
        strongenemy_group.draw(screen)
    elif stage==4:
        normalenemy_group.draw(screen)
        rangeenemy_group.draw(screen)
        rangeenemy_attack_group.draw(screen)
        strongenemy_group.draw(screen)
        if boss_on==1:
            screen.blit(boss.image,boss.rect)   
    screen.blit(text_life,text_life_rect)
    pygame.display.update() 
     
def draw_start():
    start_image_rect.center=(640,250)
    setting_image_rect.center=(640,350)
    quit_image_rect.center=(640,450)
    screen.blit(startbg_image,(0,0))
    screen.blit(start_image,start_image_rect)
    screen.blit(setting_image,setting_image_rect)
    screen.blit(quit_image,quit_image_rect)
    pygame.display.update() 
    
def draw_pause():
    start_image_rect.center=(640,300)
    quit_image_rect.center=(640,500)
    resume_image_rect.center=(640,200)
    restart_image_rect.center=(640,300)
    setting_image_rect.center=(640,400)
    screen.blit(startbg_image,(0,0))
    screen.blit(resume_image,resume_image_rect)
    screen.blit(restart_image,restart_image_rect)
    screen.blit(setting_image,setting_image_rect)
    screen.blit(quit_image,quit_image_rect)
    pygame.display.update()  
    
def draw_gameover():
    screen.blit(startbg_image,(0,0))
    gameover_image_rect.center=(640,360)
    screen.blit(gameover_image,gameover_image_rect)
    pygame.display.update()   
    
def draw_setting():
    screen.blit(startbg_image,(0,0))
    screen.blit(game_image,(0,0))
    screen.blit(close_image,close_image_rect)
    pygame.display.update()     
def draw_level(stage):
    screen.blit(startbg_image,(0,0))
    stage_image=pygame.transform.scale(pygame.image.load(level_image[stage-1]),(210,90))
    stage_image_rect=stage_image.get_rect()
    stage_image_rect.center=(width/2,height/2)
    screen.blit(stage_image,stage_image_rect)
    pygame.display.update()  

def draw_win():
    screen.blit(startbg_image,(0,0))
    win_image_rect.center=(640,360)
    screen.blit(win_image,win_image_rect)
    pygame.display.update()
    
       
#游戏基础数值设定     
size = width,height = 1280,720
fps=30
hero_speed=4
hero_attack=1
ammo_speed=8
life=10
attack_interval=0.7

shift_buff=2
shift_interval=4
shift_duration=2
q_interval=8
q_duration=1
q_size=300

buff_time=3
item_interval=15

normalenmy_interval=2
normalenemy_speed=4.1
normalenemy_life=1
normalenemy_attack=1

rangeenemy_life=2
rangeenemy_speed=2
rangeenemy_attack=1
rangeenemy_interval=6
rangeenemy_attack_interval=4

strongenemy_speed=3
strongenemy_life=3
strongenemy_attack=1
strongenemy_interval=8
strongenemy_attack_interval=2

boss_life=40
boss_attack=3
boss_speed=2.5
boss_call_interval=8

nornalenemy_score=1
rangeenemy_score=2
strongenemy_score=3
score_max=[30,100,200,400,800]
#载入素材
pygame.mixer.music.load('./resource/BGM1.mp3')
pygame.mixer.music.set_volume(0.5)
q_sound= pygame.mixer.Sound('./resource/qsound.wav')
q_sound.set_volume(0.6)
e_sound= pygame.mixer.Sound('./resource/e_sound.wav')
e_sound.set_volume(0.6)
hurt_sound=pygame.mixer.Sound('./resource/hurt.wav')
hurt_sound.set_volume(1)
gameover_sound=pygame.mixer.Sound('./resource/gameover.wav')
ammo_sound=pygame.mixer.Sound('./resource/ammo_sound.wav')
ammo_sound.set_volume(0.4)
item_sound=pygame.mixer.Sound('./resource/item_sound.wav')
item_sound.set_volume(0.6)
win_sound=pygame.mixer.Sound('./resource/win.wav')

map_image=pygame.transform.scale(pygame.image.load('./resource/map.png'),(size[0], size[1]))
startbg_image=pygame.transform.scale(pygame.image.load('./resource/blur_map.png'),(size[0], size[1]))
start_image=pygame.transform.scale(pygame.image.load('./resource/start.png'),(150,50))
quit_image=pygame.transform.scale(pygame.image.load('./resource/quit.png'),(150,50))
resume_image=pygame.transform.scale(pygame.image.load('./resource/resume.png'),(150,50))
restart_image=pygame.transform.scale(pygame.image.load('./resource/restart.png'),(150,50))
setting_image=pygame.transform.scale(pygame.image.load('./resource/setting.png'),(150,50))
gameover_image=pygame.transform.scale(pygame.image.load('./resource/gameover.png'),(210,90))
win_image=pygame.transform.scale(pygame.image.load('./resource/win.png'),(210,90))
levels_image=pygame.transform.scale(pygame.image.load('./resource/level.png'),(150,50))
close_image=pygame.transform.scale(pygame.image.load('./resource/close.png'),(50,50))
close_image_rect=close_image.get_rect()
close_image_rect.top,close_image_rect.left=660,1200
level_image=['./resource/l1.png','./resource/l2.png','./resource/l3.png','./resource/l4.png','./resource/l5.png']
game_image=pygame.image.load('./resource/game.png')
hero_motion_images=['./resource/m0.png','./resource/m1.png','./resource/m2.png','./resource/m3.png','./resource/m4.png','./resource/m5.png','./resource/m6.png','./resource/m7.png']
attack_image='./resource/attack.png'
normalenemy_image='./resource/normalenemy.png'
rangeenemy_image='./resource/rangeenemy.png'
strongenemy_image='./resource/strongenemy.png'
range_enemy_attack_image='./resource/range_enemy_attack.png'
boss_image='./resource/boss.png'
skill_q_image=['./resource/q1.png','./resource/q2.png','./resource/q3.png']
skill_e_image=pygame.image.load('./resource/e.png')
buff_image=['./resource/buff1.png','./resource/buff2.png','./resource/buff3.png','./resource/buff4.png']
skill_e_image_width=19
skill_e_image_height=436

#初始化窗口
screen = pygame.display.set_mode(size)
pygame.mixer.music.play(loops=1000)
start_image_rect=start_image.get_rect()
quit_image_rect=quit_image.get_rect()
resume_image_rect=resume_image.get_rect()
restart_image_rect=restart_image.get_rect()
setting_image_rect=setting_image.get_rect()
gameover_image_rect=gameover_image.get_rect()
win_image_rect=win_image.get_rect()
levels_image_rect=levels_image.get_rect()
draw_start()

font = pygame.font.Font('./resource/GILLUBCD.TTF',30)
text_life = font.render(u'100',True,[255,255,255],1)
text_life_rect = text_life.get_rect()
text_life_rect.top,text_life_rect.left = (1,1)

#初始化变量
clock = pygame.time.Clock()  
gamestart=gameover=win=pause=setting_on=0

#游戏主循环
Running = True
while Running:
    clock.tick(fps)
    
    #事件读取与判断部分
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT:
            Running = False

    pressed_keys = pygame.key.get_pressed()
    pressed_mouses=pygame.mouse.get_pressed()
    mouse_location=pygame.mouse.get_pos()

    if setting_on==1:
        if close_image_rect.collidepoint(mouse_location) and pressed_mouses[0]==1:
            setting_on=0
        else:
            draw_setting()
            continue

    if gamestart==0:    #开始菜单
        draw_start()
        if start_image_rect.collidepoint(mouse_location) and pressed_mouses[0]==1:
            gamestart=1
            starttime =last_enemy1=last_enemy2=last_enemy3=last_item=last_stage=last_hurt=time()
            last_attack_time=e_start_time=q_start_time=last_q_time=shift_start_time=last_gameover_time=last_win=0
            last_buff_time=[0,0,0,0]
            skill_e_on=skill_q_on=boss_on=score=0
            stage_change_on=1
            stage=1
            hero=Hero(hero_motion_images[4],hero_speed,life)
            normalenemy=[]
            attack_group = pygame.sprite.Group()
            normalenemy_group=pygame.sprite.Group()
            rangeenemy_group=pygame.sprite.Group()
            rangeenemy_attack_group=pygame.sprite.Group()
            strongenemy_group=pygame.sprite.Group()
            item_group=pygame.sprite.Group()
        elif setting_image_rect.collidepoint(mouse_location) and pressed_mouses[0]==1:
            setting_on=1
        elif quit_image_rect.collidepoint(mouse_location) and pressed_mouses[0]==1:
            Running = False
        continue

    if pressed_keys[pygame.K_ESCAPE] and time()-last_stage>3: #判断是否暂停   
        pause=1

    if pause==1:
        draw_pause()
        if pressed_mouses[0]==1 and resume_image_rect.collidepoint(mouse_location):
            pause=0
        elif pressed_mouses[0]==1 and restart_image_rect.collidepoint(mouse_location):
            pause=0
            starttime =last_enemy1=last_enemy2=last_enemy3=last_item=last_stage=last_hurt=time()
            last_attack_time=e_start_time=q_start_time=last_q_time=shift_start_time=last_gameover_time=last_win=0
            last_buff_time=[0,0,0,0]
            skill_e_on=skill_q_on=boss_on=score=0
            stage_change_on=1
            stage=1
            hero=Hero(hero_motion_images[4],hero_speed,life)
            normalenemy=[]
            attack_group = pygame.sprite.Group()
            normalenemy_group=pygame.sprite.Group()
            rangeenemy_group=pygame.sprite.Group()
            rangeenemy_attack_group=pygame.sprite.Group()
            strongenemy_group=pygame.sprite.Group()
            item_group=pygame.sprite.Group()
        elif pressed_mouses[0]==1 and setting_image_rect.collidepoint(mouse_location):    
            setting_on=1
            continue
        elif pressed_mouses[0]==1 and quit_image_rect.collidepoint(mouse_location):
            Running=False
        else:
            continue
    


    #关卡更新
    if score>=score_max[stage-1] and stage<4: #判定当前关卡是否结束，切换关卡，初始化变量
        stage+=1
        stage_change_on=1
        last_stage=time()
        skill_e_on=skill_q_on=0
        normalenemy=[]
        attack_group = pygame.sprite.Group()
        normalenemy_group=pygame.sprite.Group()
        rangeenemy_group=pygame.sprite.Group()
        rangeenemy_attack_group=pygame.sprite.Group()
        strongenemy_group=pygame.sprite.Group()
        item_group=pygame.sprite.Group()
        
    if stage_change_on==1 and time()-last_stage<=3: #显示关卡切换动画
        draw_level(stage)
        last_enemy1=last_enemy2=last_enemy3=last_item=time()
        continue
    elif time()-last_stage>3:
        stage_change_on==1

    
    if  win==1: #判断角色是否胜利
        if time()-last_win<=3:
            draw_win()
        else:
            win=0
            gamestart=0
        continue

    
    if hero.life<=0 and gameover==0: #判断角色是否死亡
        gameover=1
        gameover_sound.play()
        last_gameover_time=time()
    if gameover==1:
        if time()-last_gameover_time<=3:
            draw_gameover()
        else:
            gameover=0
            gamestart=0
        continue        
        
    
    #角色行走与攻击判断
    change=[0,0]
    if pressed_keys[pygame.K_a]:#判断玩家按下的键，并执行相应的动作
        change[0]-=1
    if pressed_keys[pygame.K_d]:
        change[0]+=1
    if pressed_keys[pygame.K_w]:
        change[1]-=1
    if pressed_keys[pygame.K_s]:
        change[1]+=1
        
    hero.turn(change) #更新角色状态
    hero.move()  
        
    if hero.charge>=100: #q技能使用判断
        if pressed_keys[pygame.K_q]:
            skill_e=Skill_E(hero,mouse_location)
            skill_e_on=1
            e_start_time=time()
            e_sound.play()
    elif time()-e_start_time>4:
        skill_e_on=0
    if skill_e_on==1:
        skill_e.turn(mouse_location)

    if time()-shift_start_time>shift_interval+shift_duration: #shift技能使用判断
        if pressed_keys[pygame.K_LSHIFT]:
            hero.skill_shift(1)
            shift_start_time=time()
    elif time()-shift_start_time>shift_duration:
        hero.skill_shift(0)
    
    if time()-q_start_time>q_duration+q_interval:#e技能使用判断
        if pressed_keys[pygame.K_e]:
            skill_q=Skill_Q()
            skill_q_on=1
            q_start_time=last_q_time=time()
            i=0
            q_sound.play()
    elif time()-q_start_time>q_duration:
        skill_q_on=0
    if time()-q_start_time<=3:
        skill_q.turn(i)
        if time()-last_q_time>=1:
            if i>=2:
                i=2
            else:
                i+=1
            last_q_time=time()
            
    if pressed_mouses[0]==1 and time()-last_attack_time>hero.attack_interval: #判断鼠标按键，修改角色普通攻击类列表
        last_attack_time=time()
        attack_group.add(HeroAttack(attack_image,ammo_speed,hero,mouse_location))  
        ammo_sound.play()
    for ha in attack_group:
        if ha.out_range==1:
            attack_group.remove(ha)
        else:
            ha.move()
          
    #生成关卡道具与敌人
    if time()-last_item>item_interval: #生成道具
        item_group.add(Item(buff_image,choice([0,1,2,3])))
        last_item=time()    
        
    if stage==1:    #根据当前关卡生成敌人
        if time()-last_enemy1>normalenmy_interval:#生成普通敌人，并更新其状态
            normalenemy_group.add(NormalEnemy(normalenemy_image,0))
            last_enemy1=time()
        normalenemy_group.update(hero)    
        
    if stage==2:
        if time()-last_enemy1>normalenmy_interval:#生成普通敌人，并更新其状态
            normalenemy_group.add(NormalEnemy(normalenemy_image,0))
            last_enemy1=time()
        normalenemy_group.update(hero)     
        if time()-last_enemy2>rangeenemy_interval:#生成远程敌人，并更新其状态
            rangeenemy_group.add(RangeEnemy(rangeenemy_image,0))
            last_enemy2=time()
        rangeenemy_group.update(hero)
        for rn in rangeenemy_group:
            if time()-rn.last_rangeenemy_attack_time>rangeenemy_attack_interval: #修改敌人远程攻击类列表
                rn.last_rangeenemy_attack_time=time()
                rangeenemy_attack_group.add(EnemyAttack(range_enemy_attack_image,rn))   
        for ea in rangeenemy_attack_group:
            if ea.out_range==1:
                rangeenemy_attack_group.remove(ea)
            else:
                ea.move()           
                
    if stage==3:
        if time()-last_enemy1>normalenmy_interval:#生成普通敌人，并更新其状态
            normalenemy_group.add(NormalEnemy(normalenemy_image,0))
            last_enemy1=time()
        normalenemy_group.update(hero)   
        if time()-last_enemy2>rangeenemy_interval:#生成远程敌人，并更新其状态
            rangeenemy_group.add(RangeEnemy(rangeenemy_image,0))
            last_enemy2=time()
        rangeenemy_group.update(hero)
        if time()-last_enemy3>strongenemy_interval:#生成强壮敌人，并更新其状态
            strongenemy_group.add(StrongEnemy(strongenemy_image,0))
            last_enemy3=time()
        strongenemy_group.update(hero) 
        for rn in rangeenemy_group:
            if time()-rn.last_rangeenemy_attack_time>rangeenemy_attack_interval: #修改敌人远程攻击类列表
                rn.last_rangeenemy_attack_time=time()
                rangeenemy_attack_group.add(EnemyAttack(range_enemy_attack_image,rn))   
        for ea in rangeenemy_attack_group:
            if ea.out_range==1:
                rangeenemy_attack_group.remove(ea)
            else:
                ea.move()  
                
    if stage==4 and win==0:
        if boss_on==0:
            boss=Boss(boss_image)
            boss_on=1
        else:
            if time()-last_enemy1>boss_call_interval:
                for j in range(6):
                    boss.call(choice([1,2,3]))
                last_enemy1=time()
            boss.update(hero)
            normalenemy_group.update(hero)  
            rangeenemy_group.update(hero)
            strongenemy_group.update(hero) 
            for rn in rangeenemy_group:
                if time()-rn.last_rangeenemy_attack_time>rangeenemy_attack_interval: #修改敌人远程攻击类列表
                    rn.last_rangeenemy_attack_time=time()
                    rangeenemy_attack_group.add(EnemyAttack(range_enemy_attack_image,rn))   
            for ea in rangeenemy_attack_group:
                if ea.out_range==1:
                    rangeenemy_attack_group.remove(ea)
                else:
                    ea.move()  

    
    #碰撞检测部分
    for itm in item_group: #判断道具捡拾状态
        if pygame.sprite.collide_rect(hero,itm):
            itm.activate()
            last_buff_time[itm.num]=time()
            item_group.remove(itm)    
            item_sound.play()
    if time()-last_buff_time[1]>=buff_time:
        recover(1)
    if time()-last_buff_time[3]>=buff_time:
        recover(3)
        
    for nm in normalenemy_group:
        if len(pygame.sprite.spritecollide(nm,attack_group,True))!=0: #判断角色是否攻击到敌人
            nm.life-=hero.attack  
    for rn in rangeenemy_group:
        if len(pygame.sprite.spritecollide(rn,attack_group,True))!=0: 
            rn.life-=hero.attack  
    for se in strongenemy_group:
        if len(pygame.sprite.spritecollide(se,attack_group,True))!=0: 
            se.life-=hero.attack            
    if boss_on==1:        
        if len(pygame.sprite.spritecollide(boss,attack_group,True))!=0: 
            boss.life-=hero.attack    
            
    if skill_e_on==1:#判断q技能是否攻击到敌人
        k1,y1,b1,k2,y2,b2=e_collide()
        for nm in normalenemy_group:
            if abs((nm.rect.centerx*k1-nm.rect.centery+b1)/pow(k1**2+y1**2+10**-20,0.5))<=skill_e_image_height/2 and abs((nm.rect.centerx*k2-nm.rect.centery+b2)/pow(k2**2+y2**2+10**-20,0.5))<=skill_e_image_width:
                nm.life-=3   
        for rn in rangeenemy_group:
            if abs((rn.rect.centerx*k1-rn.rect.centery+b1)/pow(k1**2+y1**2+10**-20,0.5))<=skill_e_image_height/2 and abs((rn.rect.centerx*k2-rn.rect.centery+b2)/pow(k2**2+y2**2+10**-20,0.5))<=skill_e_image_width:
                rn.life-=3  
        for se in strongenemy_group:
            if abs((se.rect.centerx*k1-se.rect.centery+b1)/pow(k1**2+y1**2+10**-20,0.5))<=skill_e_image_height/2 and abs((se.rect.centerx*k2-se.rect.centery+b2)/pow(k2**2+y2**2+10**-20,0.5))<=skill_e_image_width:
                se.life-=3     
        if boss_on==1 and time()-last_hurt>=1:
            if abs((boss.rect.centerx*k1-boss.rect.centery+b1)/pow(k1**2+y1**2+10**-20,0.5))<=skill_e_image_height/2 and abs((boss.rect.centerx*k2-boss.rect.centery+b2)/pow(k2**2+y2**2+10**-20,0.5))<=skill_e_image_width:
                boss.life-=3   
                last_hurt=time()
        
    if skill_q_on==1 : #判断e技能是否攻击到敌人
        for nm in normalenemy_group:
            if ((nm.rect.centerx-skill_q.rect.centerx)**2+(nm.rect.centery-skill_q.rect.centery)**2)**0.5<=q_size/2:
                nm.life-=2
        for rn in rangeenemy_group:
            if ((rn.rect.centerx-skill_q.rect.centerx)**2+(rn.rect.centery-skill_q.rect.centery)**2)**0.5<=q_size/2:
                rn.life-=2     
        for se in strongenemy_group:
            if ((se.rect.centerx-skill_q.rect.centerx)**2+(se.rect.centery-skill_q.rect.centery)**2)**0.5<=q_size/2:
                se.life-=2     
        pygame.sprite.spritecollide(skill_q,rangeenemy_attack_group,True)
        if boss_on==1 and time()-last_hurt>=1:
            if ((boss.rect.centerx-skill_q.rect.centery)**2+(boss.rect.centerx-skill_q.rect.centery)**2)**0.5<=q_size/2:
                boss.life-=2  
                last_hurt=time()
                
    for nm in normalenemy_group:#判断敌人是否攻击到角色
        if pygame.sprite.collide_rect(hero,nm):
            hero.life-=nm.attack
            nm.life-=1
            hurt_sound.play()
            
    a=len(pygame.sprite.spritecollide(hero,rangeenemy_attack_group,True)) 
    if a!=0:
        hero.life-=rangeenemy_attack*a
        hurt_sound.play()
        
    for se in strongenemy_group:#判断敌人是否攻击到角色
        if pygame.sprite.collide_rect(hero,se) and time()-se.last_strongenemy_attack_time>strongenemy_attack_interval: 
            se.last_strongenemy_attack_time=time()
            hero.life-=se.attack    
            hurt_sound.play()
            
            
    #敌人死亡判断     
    for nm in normalenemy_group: 
        if nm.life<=0:
            normalenemy_group.remove(nm)
            score+=nornalenemy_score
            hero.charge+=nornalenemy_score*2
    for rn in rangeenemy_group: 
        if rn.life<=0:
            rangeenemy_group.remove(rn)
            score+=rangeenemy_score
            hero.charge+=rangeenemy_score*2
    for se in strongenemy_group: 
        if se.life<=0:
            strongenemy_group.remove(se)
            score+=strongenemy_score
            hero.charge+=strongenemy_score*2

    if boss_on==1 and boss.life<=0:#判断boss是否死亡
        score+=40
        hero.charge+=80
        boss.rect.top=800
        boss.rect.left=1400
        boss_on=0
        win=1
        last_win=time()
        win_sound.play()

        
    #分数，冷却,充能、时间更新
    if hero.charge>=100: 
        hero.charge=100    
    
    if skill_e_on==1:
        hero.charge=0
        
    q_cd=time()-q_start_time
    if q_cd>=q_duration+q_interval:
        q_cd=q_duration+q_interval
    shift_cd=time()-shift_start_time
    if shift_cd>=shift_interval+shift_duration:
        shift_cd=shift_interval+shift_duration
        
    time_str='%02d:'%int((time()-starttime)/60)+'%02d'%int((time()-starttime)%60)
    cd_str='            Q-charge:'+'%3d'%hero.charge+'    E-cd:'+str(int(q_duration+q_interval-q_cd))+'s    Shift-cd:'+str(int(shift_interval+shift_duration-shift_cd))+'s'
        
    str1='Life:'+'%2d'%hero.life+'        Score:'+'%03d'%score+'        Level:'+str(stage)+'              '+time_str+cd_str
    text_life = font.render(str1,True,[255,255,255],1) 


    refresh() #刷新屏幕
    
pygame.quit()
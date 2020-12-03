# -*- coding: utf-8 -*-
import pygame, random, math
from pygame.locals import *

pygame.mixer.pre_init(44100, -16, 1, 512) # changes sample rate and buffersize
pygame.init()

#사용할 색상초기화
white = (255, 255, 255, 50)
black = (0, 0, 0)
light_grey = Color('#606060')

grey_off = Color('#212121')
grey = Color('#424242')

green_off = Color('#417015')
green = Color('#81E029')

red_off = Color('#7F160F')
red = Color('#FE2C1E')

blue_off = Color('#006C5D')
blue = Color('#00D8B9')

yellow_off = Color('#7F8000')
yellow = Color('#FEFF00')

orange_off = Color('#804F00')
orange = Color('#FF9D00')

purple_off = Color('#480080')
purple = Color('#8F00FF')

bg = Color('#161616')
bg_sub = Color('#282828')

screen = pygame.display.set_mode((1300, 800))
clock = pygame.time.Clock()



#버튼 클래스
class button(pygame.sprite.Sprite):
    def __init__(self, text, x,y,w,h, pushed, color0, color1, border = 0, border_radius = 5):
        pygame.sprite.Sprite.__init__(self)
        self.x, self.y, self.w, self.h = x, y, w, h
        # x, y is coords of top left position of rectangle, and w, h, is width height of rect.
        self.pushed = pushed
        self.border = border  # if border = 0 then rectangle is filled, 1 is not filled
        self.color0 = color0  # unpushed color
        self.color1 = color1  # pushed color
        self.border_radius = border_radius
        self.coords = self.x, self.y
        Rect1 = (self.x, self.y, self.w, self.h)
        self.Return_rect = pygame.draw.rect(screen, (255, 0, 0), Rect1, self.border, self.border_radius)
        font = pygame.font.SysFont("arial", 14)
        width, height = font.size(text)
        self.txt = font.render(text, True, (0, 0, 0))
        xoffset = (self.w-width) // 2
        yoffset = (self.h-height) // 2
        self.coords = self.x + xoffset, self.y + yoffset
        
    def push(self):
        if self.pushed == False:
            self.pushed = True
        else:
            self.pushed = False
        self.draw(screen)
        
    def is_pushed(self):
        return self.pushed
        
    def button_rect(self): 
        return self.Return_rect

    def draw(self, screen):        
        Rect = (self.x, self.y, self.w, self.h)
        if self.pushed:
            pygame.draw.rect(screen, self.color1, Rect, self.border, self.border_radius)
            screen.blit(self.txt, self.coords)
        else:
            pygame.draw.rect(screen, self.color0, Rect, self.border, self.border_radius)
            screen.blit(self.txt, self.coords)

    def update(self):        
        Rect = (self.x, self.y, self.w, self.h)
        if self.pushed:
            pygame.draw.rect(screen, self.color1, Rect, self.border, self.border_radius)
            screen.blit(self.txt, self.coords)
        else:
            pygame.draw.rect(screen, self.color0, Rect, self.border, self.border_radius)
            screen.blit(self.txt, self.coords)


#텍스트 박스 클래스(텍스트 넣으면 중앙정렬해줌)
class CenteredText(object):

    def __init__(self, text, font_size, font_color, x,y,w,h, color, border = 0):
        self.x, self.y, self.w, self.h = x, y, w, h
        # x, y is coords of top left position of rectangle, and w, h, is width height of rect
        self.border = border  # if border = 0 then rectangle is filled, 1 is not filled
        self.color = color
        self.font_size = font_size
        self.font_color = font_color
        font = pygame.font.SysFont("arial", self.font_size)
        width, height = font.size(text)
        xoffset = (self.w-width) // 2
        yoffset = (self.h-height) // 2
        self.coords = self.x + xoffset, self.y + yoffset
        self.txt = font.render(text, True, self.font_color)
        
        
    def draw(self, screen):        
        Rect = (self.x, self.y, self.w, self.h)
        pygame.draw.rect(screen, self.color, Rect, self.border)
        screen.blit(self.txt, self.coords)
        
    def get_border_rect(self):
        Rect1 = (self.x, self.y, self.w, self.h)
        R = pygame.draw.rect(screen, (0, 0, 0), Rect1, self.border)
        return R
    
    def get_text(self):
        return self.text


#음악 샘플 클래스(음악 파일을 import 하고 재생)
class sample(object):
    '''sample class plays an audio file 
    '''
    def __init__(self, file):
        self.file = pygame.mixer.Sound(file)
    
    def play_sound(self):
        self.file.play()     


#그래픽 클래스
class Pulse(pygame.sprite.Sprite):
    def __init__(self, rect, color):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([rect.width, rect.height])
        self.rect = rect
        self.color = color
        self.radius = 0
        self.thickness = 1

        self.delta = 4

    def speedUp(self, delta):
        self.delta += delta

    def speedDown(self, delta):
        self.delta -= delta

    def changeColor(self, color):
        self.color = color

    def changeThickness(self, thickness):
        self.thickness = thickness

    def update(self):
        self.radius += self.delta
        pygame.draw.circle(screen, self.color, self.rect.center, self.radius, self.thickness)

        if(self.radius > 500):
            self.kill()

colorTypes = (red, blue, green, yellow, orange, purple)

#아이콘 클래스
class Icon(pygame.sprite.Sprite):
    def __init__(self, image, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.position = position

    def update(self):
        self.rect.center = self.position

#############
#버튼 생성 파트#

#각종 버튼 딕셔너리(생성한 버튼들을 넣어두고 gameloop이 돌때 꺼내 씀)
button_dict = {}
#시퀀서 돌때 버튼을 highlight해주는 버튼 딕셔너리
border_dict = {}

#악기별 버튼 번호 튜플로 초기화
def make_inst_tuple(n):
    inst = (n, n+6, n+12, n+18, n+24, n+30, n+36, n+42, n+48, n+54, n+60, n+66, n+72, n+78, n+84, n+90)
    return inst

inst1 = make_inst_tuple(0)
inst2 = make_inst_tuple(1)
inst3 = make_inst_tuple(2)
inst4 = make_inst_tuple(3)
inst5 = make_inst_tuple(4)
inst6 = make_inst_tuple(5)

#이중 for loop을 사용해 화면에 배치할 8*4 비트 버튼을 생성해서 버튼 딕셔너리에 삽입 
def draw_beat_button(start_btn_number, start_x, start_y):
    button_number = start_btn_number

    for x in range(start_x, start_x + 72*4, 72):
        for y in range(start_y, start_y + 44*6, 44):
            if button_number in inst1:
                off_color = green_off
                on_color = green
            elif button_number in inst2:
                off_color = red_off
                on_color = red
            elif button_number in inst3:
                off_color = blue_off
                on_color = blue
            elif button_number in inst4:
                off_color = yellow_off
                on_color = yellow
            elif button_number in inst5:
                off_color = orange_off
                on_color = orange
            elif button_number in inst6:
                off_color = purple_off
                on_color = purple
            else:
                off_color = grey_off
                on_color = grey

            button_dict['button%s' % button_number] = button('', x, y, 70, 40, False, off_color, on_color, 0)
            border_dict['border%s' % button_number] = button('', x, y, 70, 40, False, white, white, 2)
            button_number += 1

draw_beat_button(0, 104, 524)
draw_beat_button(24, 400, 524)
draw_beat_button(48, 696, 524)
draw_beat_button(72, 992, 524)

#각종 조작 버튼을 생성하고 딕셔너리에 삽입(start, clear, tempo 등등)
button_dict['start_button'] = button('RUN', 16, 464 - 44*0, 70, 40, False, grey_off, white, 0, 20)
button_dict['Clear'] = button('CLEAR', 16, 464 - 44*1, 70, 40, False, grey_off, white, 0, 20)
button_dict['4'] = button('1/4', 16, 464 - 44*2, 70, 40, False, grey_off, white, 0, 20)
button_dict['8'] = button('1/8', 16, 464 - 44*3, 70, 40, False, grey_off, white, 0, 20)
button_dict['16'] = button('1/16', 16, 464 - 44*4, 70, 40, False, grey_off, white, 0, 20)
button_dict['32'] = button('1/32', 16, 464 - 44*5, 70, 40, False, grey_off, white, 0, 20)

#버튼 생성 파트 끝#
#############


#############
#음악파일 생성 파트 시작#

#음악샘플 딕셔너리 생성
sample_dict = {}

#음악샘플 딕셔너리의 key를 비트 버튼 번호로 설정하고 해당 key에 음악파일 배정(예: button4에 sample0 배정)
#for loop을 사용해 inst1 -> sample0, inst2 -> sample1, inst3 -> sample2, inst4 -> sample3 배정
sample_num = 0
for s in range(0, 96):
    sample_dict['button%s' % s] = sample('sample%s.wav' % sample_num)
    sample_num += 1
    if sample_num > 5:
        sample_num = 0

#음악파일 생성 파트 끝#
#############


#############
#텍스트 라벨 파트 시작#

#cetered text 클래스 속성: text, font_size, font_color, x,y,w,h, color, border = 0
label_dict = {}
label_dict['KICK'] =  CenteredText('KICK', 14, green, 16, 524 + 44*0, 70, 40, bg_sub, 0)
label_dict['SNARE'] = CenteredText('SNARE', 14, red, 16, 524 + 44*1, 70, 40, bg_sub, 0)
label_dict['HIGH-HAT'] = CenteredText('HIGH-HAT', 14, blue, 16, 524 + 44*2, 70, 40, bg_sub, 0)
label_dict['CLAP'] = CenteredText('CLAP', 14, yellow, 16, 524 + 44*3, 70, 40, bg_sub, 0)
label_dict['SHAKE'] = CenteredText('SHAKE', 14, orange, 16, 524 + 44*4, 70, 40, bg_sub, 0)
label_dict['COW-BELL'] = CenteredText('COW-BELL', 14, purple, 16, 524 + 44*5, 70, 40, bg_sub, 0)

#텍스트 라벨 파트 끝#
#############

#화면 하단 조작바 rect 정의
beat_bar = (0, 512, 1300, 288)
control_bar = (0,0,104,512)

#메인 loop
def game_loop():
    
    screen.fill(black)
    #draw beat bar
    pygame.draw.rect(screen, bg, beat_bar)
    #draw control bar
    pygame.draw.rect(screen, light_grey, control_bar)
    
    #재생될 음악샘플이 들어오고 나가는 딕셔너리
    sound_queue_dict = {}

    pulses = pygame.sprite.Group()
    static_buttons = pygame.sprite.Group()
    activated_buttons = pygame.sprite.Group()
    deactivated_buttons = pygame.sprite.Group()
    played_buttons = pygame.sprite.Group()

    icons = [
        Icon('1.png', (52,544 + 44*0)),
        Icon('2.png', (52,544 + 44*1)), 
        Icon('3.png', (52,544 + 44*2)),
        Icon('4.png', (52,544 + 44*3)),
        Icon('5.png', (52,544 + 44*4)),
        Icon('6.png', (52,544 + 44*5))
    ]

    static_icons = pygame.sprite.RenderPlain(*icons)
    
    #딕셔너리에 저장된 모든 버튼을 그린다
    for k in button_dict:
         button_dict[k].draw(screen)

    #딕셔너리에 저장된 모든 텍스트 라벨을 그린다
    for k in label_dict:
        label_dict[k].draw(screen)

    static_icons.update()
    static_icons.draw(screen)
    
    button_counter_list = [0, 1, 2, 3, 4, 5]    
    button_dict['8'].push()
    button_dict['8'].draw(screen)
    sound_queue_dict['8'] = 0
    beats_per_bar_list =  ['4', '8', '16', '32']
    beats_per_bar_list_copy = ['4', '8', '16', '32']

    BPM = 120
    BPM_text = '128'
    BPM_text2 = ''
    change_timer = True   
    
    while True: # game loop
         
        #마우스 위치 추적 변수
        mouse_pos = pygame.mouse.get_pos()

        #4, 8, 16, 32박 버튼 중 눌린 것을 검사해서 타이머 설정(템포 조절하는 곳)
        if change_timer:
            for x in beats_per_bar_list:
                if button_dict[x].is_pushed():
                    x_int = int(x)
                    divisor = x_int // 4
                    BPM_in_milliseconds = 60000 // BPM
                    milliseconds_per_step = BPM_in_milliseconds // divisor
            pygame.time.set_timer(pygame.USEREVENT, milliseconds_per_step)
            change_timer = False
          
        #clear버튼이 눌렸을 때 0~31번 버튼 중 눌린 버튼을 검사하고 비활성화시킴. 재생할 음악샘플도 모두 삭제 
        if button_dict['Clear'].is_pushed():
            for q in range (0, 96):
                q_str = (str(q))
                if button_dict['button%s' % q_str].is_pushed():
                    button_dict['button%s' % q_str].push()
                    button_dict['button%s' % q_str].draw(screen)
                    if 'button%s' % q_str in sound_queue_dict:
                        del sound_queue_dict['button%s' % q_str]
            button_dict['Clear'].push()
            button_dict['Clear'].draw(screen)
            
        #각종 이벤트 발생 추적 loop
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:   #allows for user to quit
                pygame.quit()
                return  
            
            #타이머 이벤트
            if event.type == pygame.USEREVENT:  #timer
                
                for k in button_dict:
                    # button_dict[k].draw(screen)
                    static_buttons.add(button_dict[k])
                
                if button_dict['start_button'].is_pushed():
                    temp = pygame.sprite.Group()
                    for x in button_counter_list:
                        x_str = str(x)
                        # border_dict['border%s' % x_str].draw(screen) 
                        temp.add(border_dict['border%s' % x_str])  
                    played_buttons = temp

                    pushed = []                     
                    for w in button_counter_list:
                        w_str = str(w)
                        button_str = 'button' + w_str
                        if button_str in sound_queue_dict:
                            sample_dict[button_str].play_sound()
                        if button_dict[button_str].is_pushed():
                            pushed.append(w)

                    for i in pushed:
                        if i % 6 == 0:
                            pulses.add(Pulse(Rect(random.randint(170,1240),random.randint(60,450),0,0), red))
                        elif i % 6 == 1:
                            for pulse in pulses:
                                pulse.speedUp(random.randint(4,8))
                        elif i % 6 == 2:
                            for pulse in pulses:
                                pulse.speedDown(random.randint(4,8))
                        elif i % 6 == 3:
                            for pulse in pulses:
                                pulse.changeThickness(random.randint(1,10))
                        elif i % 6 == 4:
                            for pulse in pulses:
                                pulseColor = random.choice(colorTypes)
                                pulse.changeColor(pulseColor)
                        elif i % 6 == 5:
                            for pulse in pulses:
                                pulse.speedUp(random.randint(4,8))
                        

                    next_counter_list = []
                    for x in button_counter_list:
                         x += 6
                         next_counter_list.append(x)
                    button_counter_list = next_counter_list
                    if button_counter_list[0] > 95:
                         button_counter_list = [0, 1, 2, 3, 4, 5]   
                else:
                    button_counter_list = [0, 1, 2, 3, 4, 5]
            
            #마우스 이벤트
            if event.type == pygame.MOUSEBUTTONDOWN:
                #누른 버튼을 활성화/비활성화, sound 딕셔너리에도 추가/삭제
                for k in button_dict:
                    if button_dict[k].button_rect().collidepoint(mouse_pos):
                        button_dict[k].push()
                        # button_dict[k].draw(screen)
                        activated_buttons.add(button_dict[k])
                        if button_dict[k].is_pushed():
                            sound_queue_dict[k] = 0
                        else:
                            del sound_queue_dict[k]    

                #템포조절 버튼 4, 6, 16, 32 중 택1
                for i in beats_per_bar_list:
                    if button_dict[i].button_rect().collidepoint(mouse_pos):
                        beats_per_bar_list_copy.remove(i)
                        for l in beats_per_bar_list_copy:
                            if button_dict[l].is_pushed():
                                button_dict[l].push()
                                button_dict[l].draw(screen)
                        change_timer = True
                        beats_per_bar_list_copy = ['4', '8', '16', '32']

        screen.fill(black)
        pulses.update()
        static_icons.update()
        static_icons.draw(screen)
        static_buttons.update()
        activated_buttons.update()
        played_buttons.update()
        
        
        pygame.display.update()
        clock.tick(30)

game_loop()
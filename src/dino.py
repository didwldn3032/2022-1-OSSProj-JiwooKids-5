from src.setting import *

'''
dino.py : 게임 내 공룡 캐릭터와 관련한 특성 및 상태 구현
Dino Class
< 변수 >
- type (str) : 디노의 스킨 결정 (ORIGINAL, PINK, RED, ORANGE, YELLOW, GREEN)
- rect.bottom (float) : 화면의 가로 길이
- rect.left (float) : 화면의 세로 길이
- image : 디노의 이미지 
- index (int) : 
- counter (int) : 
- score (int) : 현재 디노가 획득한 점수
- isJumping (boolean) : 디노가 땅에 있는지, 점프해있는지
- isDead (boolean) : 디노가 죽었는지, 즉 게임이 끝났는지
- isDucking (boolean) : 디노가 수그렸는지
- isBlinking (boolean) : 디노가 깜빡이고있는지
- movement[int, int] : 디노의 움직임 [x, y]
- jumpSpeed (float) : 디노의 점프 속도
- superJumpSpeed (float) : 디노의 2단 점프 속도
- collision_immune (boolean) : 
- isSuper (boolean) :
- stand_pos_width : 디노가 서있을 때의 가로 길이
- duck_pos_width : 디노가 엎드려 있을 때의 가로 길이
< 함수 >
- draw() : 화면의 사각형 내에 디노의 이미지를 붙여넣음
- checkbounds() : 디노가 화면 범위 밖을 벗어났는지 확인하는 함수
- update() : 디노의 각종 상태(isJumping, isBlinking 등)에 따라 속성값(movement, index, counter 등)을 변경
'''

class Dino():
    def __init__(self, sizex=-1, sizey=-1,type = None):
        
        # 디노의 타입을 결정합니다. 
        self.type = type

        # 해당하는 디노의 스킨을 가져와서 적용
        if type == 'ORIGINAL':
            self.images, self.rect = load_sprite_sheet('dino_arrange.png', 11, 1, sizex, sizey, -1)
            # self.images, self.rect = load_sprite_sheet('pinkdino.png', 6, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('dino_ducking.png', 6, 1, 59, sizey, -1)
            # self.images1, self.rect1 = load_sprite_sheet('pinkdino_ducking.png', 2, 1, 59, sizey, -1)
        elif type == 'PINK':
            self.images, self.rect = load_sprite_sheet('dino_pink.png', 11, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('dino_pink_ducking.png', 6, 1, 59, sizey, -1)
        elif type == 'RED':
            self.images, self.rect = load_sprite_sheet('dino_red.png', 11, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('dino_red_ducking.png', 6, 1, 59, sizey, -1)    
        elif type == 'ORANGE':
            self.images, self.rect = load_sprite_sheet('dino_orange.png', 11, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('dino_orange_ducking.png', 6, 1, 59, sizey, -1) 
        elif type == 'YELLOW':
            self.images, self.rect = load_sprite_sheet('dino_yellow.png', 11, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('dino_yellow_ducking.png', 6, 1, 59, sizey, -1)
        elif type == 'GREEN':
            self.images, self.rect = load_sprite_sheet('dino_green.png', 11, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('dino_green_ducking.png', 6, 1, 59, sizey, -1)
        elif type == 'PURPLE':
            self.images, self.rect = load_sprite_sheet('dino_purple.png', 11, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('dino_purple_ducking.png', 6, 1, 59, sizey, -1)  
        elif type == 'BLACK':
            self.images, self.rect = load_sprite_sheet('dino_black.png', 11, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('dino_black_ducking.png', 6, 1, 59, sizey, -1)    
        else: 
            self.images, self.rect = load_sprite_sheet('dino_arrange.png', 11, 1, sizex, sizey, -1)
            self.images1, self.rect1 = load_sprite_sheet('dino_ducking.png', 6, 1, 59, sizey, -1)

        self.rect.bottom = int(0.9*height)
        self.rect.left = width/15
        self.image = self.images[0]
        self.index = 0
        self.counter = 0
        self.score = 0
        self.score2 = 0
        self.item_time = 0
        self.isJumping = False
        self.isDead = False
        self.isDucking = False
        self.isBlinking = False
        self.movement = [0, 0]
        self.jumpSpeed = 11.5
        self.superJumpSpeed = self.jumpSpeed * 1.3
        self.collision_immune = False
        self.isSuper = False

        # 아이템 사용 상태
        self.Superglass = False
        self.Sovel = False

        self.stand_pos_width = self.rect.width
        self.duck_pos_width = self.rect1.width

    def draw(self):
        screen.blit(self.image, self.rect)

    def checkbounds(self):
        if self.rect.bottom > int(0.9*height):
            self.rect.bottom = int(0.9*height)
            self.isJumping = False

    def update(self):
        # 1. movement y값 변경
        if self.isJumping: 
            self.movement[1] = self.movement[1] + gravity # 움직임의 y값에 gravity값을 더해 점프 높이를 적용

        # 2. Dino의 상황별 모션 구현
        if self.Superglass: # 안경쓰고 있을 때
            if self.isJumping: self.index = 5 # 뛰고있을 때
            # 걸어갈 때
            if self.isDucking: # 숙이고있으면
                if self.counter % 5 == 0: 
                    if self.index==2: self.index=3
                    elif self.index==3: self.index=2
                    else: self.index=2
            else: # 서있으면
                if self.counter % 5 == 0: 
                    if self.index == 6: self.index=7
                    elif self.index == 7: self.index=6
                    else: self.index = 6

        elif self.Sovel: # 삽들고 있을 때
            if self.isJumping: self.index = 8 # 뛰고있을 때
            # 걸어갈 때
            if not self.isDucking: # 서있으면
                if self.counter % 5 == 0:
                    if self.index==9: self.index=10
                    elif self.index==10: self.index=9
                    else: self.index=9
            else: # 숙이고있으면
                if self.counter % 5 == 0:
                    if self.index==4: self.index=5
                    elif self.index==5: self.index=4
                    else: self.index=4

        # elif self.isBlinking: # 눈 깜빡이기
        #     if self.index == 0:
        #         if self.counter % 400 == 399:
        #             self.index = 2
        #     else:
        #         if self.counter % 20 == 19:
        #             self.index = 2

        else: # 아무것도 안입고 있을 때
            if self.isJumping: self.index = 0 # 뛰고있을 때
             # 걸어갈 때
            if not self.isDucking: # 서있으면
                if self.counter % 5 == 0:
                    if self.index==2: self.index=3
                    elif self.index==3: self.index=2
                    else: self.index=2
            else: # 숙이고있으면
                if self.counter % 5 == 0:
                    if self.index==0: self.index=1
                    elif self.index==1: self.index=0
                    else: self.index=0

        if self.isDead: # 죽었을 경우
            self.index = 4

        if self.collision_immune:
            if self.counter % 10 == 0: self.index = 2

        # 숙이고 있는 모션 구현
        if not self.isDucking:
            if self.counter % 5 == 0:
                self.image = self.images[self.index]
            self.rect.width = self.stand_pos_width
        else:
            if self.counter % 5 == 0: 
                self.image = self.images1[self.index]
            if self.collision_immune is True:
                if self.counter % 5 == 0:
                    self.image = self.images[5]
            self.rect.width = self.duck_pos_width

        self.rect = self.rect.move(self.movement)
        self.checkbounds()

        if not self.isDead and self.counter % 7 == 6 and self.isBlinking == False:
            self.score += 1
            self.score2 += 1
            self.item_time += 1
            if self.score % 100 == 0 and self.score != 0:
                if pygame.mixer.get_init() != None:
                    checkPoint_sound.play()

        self.counter = (self.counter + 1)
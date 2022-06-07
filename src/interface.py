from src.setting import *

'''
interface.py : 게임 내 각종 환경 요소 객체
Ground(땅) class
< 변수 >
- image, rect : 그라운드의 이미지와 프레임 (기본, 장애물용)
- speed : 그라운드 이동 속도
< 함수 >
- draw() : 화면에 그라운드를 그려넣음
- update() : 화면 내 그라운드의 상태 업데이트
Cloud(구름) class
< 변수 >
- image, rect(left, top) : 구름의 이미지와 프레임(왼쪽끝, 최상단)
- speed : 구름 이동 속도
- movement : 구름의 이동
< 함수 >
- draw() : 화면에 구름을 그려넣음
- update() : 화면 내 구름의 상태 업데이트
Heart(체력량) class
< 변수 >
- image, rect(left, top) : 체력량의 이미지와 프레임(왼쪽끝, 최상단)
< 함수 >
- draw() : 화면에 체력량을 그려넣음
HeartIndicator(체력 개수) class
< 변수 >
- life : 잔여 체력 개수
- life_set : 잔여 체력 개수 시각화를 위한 리스트
< 함수 >
- draw() : 체력 개수만큼 그려넣음
- update() : 잔여 체력 개수 업데이트
Scoreboard(스코어보드) class
< 변수 >
- score : 시각화할 스코어
- tempimages, self.temprect : 스코어 이미지와 프레임 저장을 위한 변수
- image : 스코어보드 이미지
- rect(left, top) : 스코어의 프레임(왼쪽끝, 최상단)
< 함수 >
- draw() : 화면에 스코어보드를 그려넣음
- update() : 스코어값에 따라 스코어 이미지를 만들어서 그려넣음
'''

class Ground:
    def __init__(self, speed=-5):
        self.image, self.rect = load_image('Ground_extend.png', -1, -1, -1)
        self.image1, self.rect1 = load_image('Ground_extend.png', -1, -1, -1)
        self.rect.top = height - 50
        self.rect1.top = height - 50
        self.rect1.left = self.rect.right
        self.speed = speed

    def draw(self):
        screen.blit(self.image, self.rect)
        screen.blit(self.image1, self.rect1)

    def update(self):
        self.rect.left += self.speed
        self.rect1.left += self.speed

        if self.rect.right < 0:
            self.rect.left = self.rect1.right

        if self.rect1.right < 0:
            self.rect1.left = self.rect.right


class Cloud(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.image, self.rect = load_image('cloud.png', int(90*30/42), 30, -1)
        self.speed = 1
        self.rect.left = x
        self.rect.top = y
        self.movement = [-1*self.speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)
        if self.rect.right < 0: # 구름이 화면 밖을 벗어나면 객체를 없애버림
            self.kill()


class Heart:

    def __init__(self, sizex=-1, sizey=-1, x=-1, y=-1):
        self.images, self.rect = load_sprite_sheet("heart_life.png", 1, 1, sizex, sizey, -1)
        self.image = self.images[0]
        if x == -1:
            self.rect.left = width * 0.01
        else:
            self.rect.left = x

        if y == -1:
            self.rect.top = height * 0.01
        else:
            self.rect.top = y

    def draw(self):
        screen.blit(self.image, self.rect)


class HeartIndicator:

    def __init__(self, life):
        # self.heart_size = 40
        self.life = life
        self.life_set = []

    def draw(self):
        for life in self.life_set:
            life.draw()

    def update(self, life):
        self.life = life
        # self.life_set = [Heart(self.heart_size, self.heart_size, width * 0.01 + i * self.heart_size) for i in range(self.life)]
        self.life_set = [Heart(object_size[0], object_size[1], width * 0.01 + i * (object_size[0]-i)) for i in range(self.life)]


class boss_heart:
    def __init__(self, x=-1, y=-1):
        self.pos_x = 0
        self.pos_y = 0
        if x == -1:
            self.pos_x = width * 0.03
        else:
            self.pos_x = x
        if y == -1:
            self.pos_y = height * 0.15
        else:
            self.pos_y = y
    def draw(self):
        screen.blit(self.sc, self.sc_rect)

    def update(self, hp):
        self.sc = font.render(f'Boss X {hp}'.zfill(2), True, black)
        self.sc_rect = self.sc.get_rect()
        self.sc_rect.left = self.pos_x
        self.sc_rect.top = self.pos_y



class Scoreboard:
    def __init__(self, x=-1, y=-1):
        self.score = 0
        self.pos_x = 0
        self.pos_y = 0
        if x == -1:
            self.pos_x = width * 0.59
        else:
            self.pos_x = x
        if y == -1:
            self.pos_y = height * 0.05
        else:
            self.pos_y = y

    def draw(self):
        screen.blit(self.sc, self.sc_rect)

    def update(self, score, high_score):
        score_digits = extractDigits(score)

        # self.image.fill(background_col)
        self.sc = font.render(f'HIGH : {high_score} NOW : {score}'.zfill(5), True, black)
        self.sc_rect = self.sc.get_rect()
        self.sc_rect.left = self.pos_x
        self.sc_rect.top = self.pos_y


class Story_Scoreboard:
    def __init__(self, x=-1, y=-1):
        self.score = 0
        self.pos_x = 0
        self.pos_y = 0
        if x == -1:
            self.pos_x = width * 0.75
        else:
            self.pos_x = x
        if y == -1:
            self.pos_y = height * 0.05
        else:
            self.pos_y = y

    def draw(self):
        screen.blit(self.sc, self.sc_rect)

    def update(self, score):
        score_digits = extractDigits(score)

        # self.image.fill(background_col)
        self.sc = font.render(f'NOW : {score}'.zfill(5), True, black)
        self.sc_rect = self.sc.get_rect()
        self.sc_rect.left = self.pos_x
        self.sc_rect.top = self.pos_y



class Mask_time:
    def __init__(self, x=-1, y=-1):
        self.pos_x = 0
        self.pos_y = 0
        if x == -1:
            self.pos_x = width * 0.63
        else:
            self.pos_x = x
        if y == -1:
            self.pos_y = height * 0.15
        else:
            self.pos_y = y
    def draw(self):
        screen.blit(self.sc, self.sc_rect)

    def update(self, hp):
        self.sc = font.render(f'Mask Time : {100-hp}'.zfill(2), True, black)
        self.sc_rect = self.sc.get_rect()
        self.sc_rect.left = self.pos_x
        self.sc_rect.top = self.pos_y


from src.setting import *

'''
ShieldItem class

<변수>
- image,rect : 이미지, 위치, 크기 지정
- movement : 움직임(역방향)
- index : item 위치 설정
- counter : 

<함수>
- draw() : 화면에 쉴드아이템 이미지 삽입
- update() : 쉴드아이템 상태 업데이트(계속 왼쪽으로 이동하다 화면 밖 벗어나면 삭제)

LifeItem class

<변수>
- image,rect : 이미지, 위치, 크기 지정
- movement : 움직임(역방향)
- index : item 위치 설정
- counter : 

<함수>
- draw() : 화면에 생명(하트)이미지 삽입
- update() : 하트아이템 상태 업데이트(계속 왼쪽으로 이동하다 화면 밖 벗어나면 삭제)

SlowItem

<변수>
- image,rect : 이미지, 위치, 크기 지정
- movement : 움직임(역방향)
- index : item 위치 설정
- counter : 

<함수>
- draw() : 화면에 slow아이템 이미지 삽입
- update() : slow아이템 상태 업데이트(계속 왼쪽으로 이동하다 화면 밖 벗어나면 삭제)

obj class : 미사일 생성 클래스

<함수>
- put_img : 파일형태 확인후, 그에 맞게 이미지 load
- change_size : 미사일 크기 조정
- show : 화면에 이미지 삽입

'''


class ShieldItem(pygame.sprite.Sprite):

    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet('item.png', 2, 1, sizex, sizey, -1)
        self.item_height = [height*0.82, height*0.75, height*0.60]
        self.rect.centery = self.item_height[random.randrange(0, 3)]
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1 * speed, 0]
        self.index = 0
        self.counter = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index + 1) % 2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()


class LifeItem(pygame.sprite.Sprite):

    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet("heart.png", 2, 1, sizex, sizey, -1)
        self.heart_height = [height*0.82, height*0.75, height*0.60]
        self.rect.centery = self.heart_height[random.randrange(3)]
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1 * speed, 0]
        self.index = 0
        self.counter = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index + 1) % 2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()


class SlowItem(pygame.sprite.Sprite):

    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet("slow_pic.png", 2, 1, sizex, sizey, -1)
        self.slow_height = [height*0.82, height*0.75, height*0.60]
        self.rect.centery = self.slow_height[random.randrange(3)]
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1 * speed, 0]
        self.index = 0
        self.counter = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index + 1) % 2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()

### 미사일을 쉽게 만들기 위한 미사일 클래스 ###
class obj(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.x = 0
        self.y = 0
        self.move = 0
        self.xmove = 0
        self.ymove = 0
        self.movement = [0, 0]
        self.rect=None
    def put_img(self, address):
        if address[-3:] == "png":
            self.img = pygame.image.load(address).convert_alpha()
            self.rect = self.img.get_rect
        else :
            self.img = pygame.image.load(address)
        self.sx, self.sy = self.img.get_size() #이미지 크기를 튜플 형태로 반환
    def change_size(self, sx, sy):
        self.img = pygame.transform.scale(self.img, (sx, sy))
        self.sx, self.sy = self.img.get_size() 
    def show(self):
        screen.blit(self.img, (self.x,self.y))


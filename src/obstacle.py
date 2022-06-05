from src.setting import *

'''
Cactus class/fire_Cactus : 선인장 장애물
<변수>
- image,rect : 이미지, 위치, 크기 지정
- movement : 움직임(역방향)
<함수>
- draw() : 화면에 선인장 이미지 삽입
- update() : 선인장 상태 업데이트(계속 왼쪽으로 이동하다 화면 밖 벗어나면 삭제)
PteraKing class : 보스
<변수>
- image,rect : 이미지, 위치, 크기 지정
- movement : 움직임(역방향)
- pattern0/1/2_time : 지속 시간
- pattern2_bottommost_time : 보스가 내려가서 머무는 시간
- isAlive : 보스가 살아있는가
- pattern_idx : 보스 행동 패턴
- hp : 보스 생명 15
<함수>
- draw() : 화면에 보스 이미지 삽입
- pattern0() : 
	count 10주기로 보스가 위아래로 움직임
	count가 200이 되면 pattern 종료
	pattern0이 끝나면 pattern_idx =1 통해 다음번 보스는 pattern1
- pattern1():
	count 10주기로 보스가 위아래로 움직임
	left,right로 계속 이동하다 끝에 걸리면 반대로
	count가 200되면 pattern 종료
- pattern2(): 
	count 10주기로 보스가 위아래로 움직임
	보스가 내려가다 지정된 위치에서 stop
	stop상태에서 200이 지나면 goup
	보스가 올라가다 지정된 위치가 되면 pattern0
	
- update() : pattern_idx에 맞게 패턴 진행, 10번에 한번씩 보스 출현
Ptera class : 작은 보스
<변수>
- image,rect : 이미지, 위치, 크기 지정
- movement : 움직임(역방향)
- index : item 위치 설정
- counter : 
<함수>
- draw() : 화면에 작은 보스 이미지 삽입
- update() : 작은 보스 상태 업데이트(계속 왼쪽으로 이동하다 화면 밖 벗어나면 삭제)
Stone class : 돌 장애물
<변수>
- image,rect : 이미지, 위치, 크기 지정
- movement : 움직임(역방향)
<함수>
- draw() : 화면에 돌 이미지 삽입
- update() : 돌 상태 업데이트(계속 왼쪽으로 이동하다 화면 밖 벗어나면 삭제)
'''

class Hole(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1, left=0):
        pygame.sprite.Sprite.__init__(self,self.containers)
        rand_width = random.randrange(80, 150)
        self.images, self.rect = load_sprite_sheet('holes3.png', 1, 1, rand_width, 47, -1)
        self.rect.top = height *0.993
        self.rect.bottom = int(0.995*height)
        self.rect.left = width + self.rect.width + left
        self.image = self.images[0]
        self.movement = [-1*speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()

class Cactus(pygame.sprite.Sprite): #장애물 1.선인장
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers) #Sprite를 사용하면 이미지, 위치, 충돌 처리를 통합해서 처리
        self.images, self.rect = load_sprite_sheet('cacti-small.png', 3, 1, sizex, sizey, -1)
        self.rect.bottom = int(0.9*height)
        self.rect.left = width + self.rect.width
        self.image = self.images[random.randrange(0,3)] #0과 3 사이의 난수를 반환
        self.movement = [-1*speed, 0] #캐릭터에게 speed의 속도로 다가옴

    def draw(self): #self.image와 rect를 screen에 삽입
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()


class fire_Cactus(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images, self.rect = load_sprite_sheet('fire_cacti6.png', 3, 1, sizex, sizey, -1)
        self.rect.bottom = int(0.9*height)
        self.rect.left = width + self.rect.width
        self.image = self.images[random.randrange(0,3)]
        self.movement = [-1*speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()

# pteraking 클래스
class PteraKing(pygame.sprite.Sprite):
    
    def __init__(self, speed=0, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self)
        self.images, self.rect = load_sprite_sheet('pteraking.png', 2, 1, sizex, sizey, -1)
        # self.ptera_height = [height*0.82, height*0.75, height*0.60]
        self.ptera_height=height*0.3
        # self.rect.centery = self.ptera_height[random.randrange(0, 3)]
        self.rect.centery = self.ptera_height
        self.rect.left = width - self.rect.width -50
        self.image = self.images[0]
        self.movement = [-1*speed, 0]
        # 
        self.down_speed=2
        self.down_movement=[0,self.down_speed]
        self.up_speed=2
        self.up_movement=[0,-self.up_speed]

        self.stop_movement = [0,0]
        # 
        self.index = 0
        self.counter = 1
        # 새로운 정의.
        self.isAlive=True
        self.pattern_idx=0
        self.goleft=True
        self.reached_leftmost=False
        self.reached_rightmost=False
        self.pattern0_time=200
        self.pattern0_counter=0

        self.pattern1_time=200
        self.pattern1_counter=0
        self.pattern1_speed=15
        self.pattern1_lastmove=False

        self.pattern2_counter=0
        self.godown=True
        self.bottommost=height*0.6
        self.topmost = height * 0.3
        # 보스가 내려가서 머무르는 시간
        self.pattern2_bottommost_time = 200

        self.pattern3_time=200
        self.pattern3_counter=0
        self.pattern3_speed=15
        self.pattern3_lastmove=False

        self.stop=False

        self.goup=False
        self.topmost=height*0.3
        # 
        self.hp = 15

    def draw(self):
        screen.blit(self.image, self.rect)
        # 총알 그리기

    def pattern0(self):

        self.pattern1_lastmove=False
        self.pattern0_counter+=1
        self.movement[0]=0
        if self.counter %10==0:
            self.index = (self.index+1) % 2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        if self.pattern0_counter % self.pattern0_time == 0:
            self.pattern_idx = 1

    def pattern1(self):

        self.pattern1_counter+=1

        if self.counter % 10 == 0:
            self.index = (self.index+1) % 2
        self.image = self.images[self.index]

        if (self.goleft == True) and (self.reached_leftmost == False):
            self.movement[0] = -1 * self.pattern1_speed
            self.rect = self.rect.move(self.movement)

            if self.rect.left < 0:
                self.goleft = False
                self.reached_leftmost = True
                self.reached_rightmost = False
        
        else:
            self.movement[0] = self.pattern1_speed
            self.rect = self.rect.move(self.movement)

            if self.pattern1_lastmove:
                if self.rect.left > width - self.rect.width -50:
                        self.goleft = True
                        self.reached_rightmost = True
                        self.reached_leftmost = False

                        self.pattern_idx = 2
            else:
                if self.rect.left > width - self.rect.width -50:
                        self.goleft = True
                        self.reached_rightmost = True
                        self.reached_leftmost = False
            
            if self.pattern1_counter % self.pattern1_time == 0:
                self.pattern1_lastmove=True

        # 총알발사.

    def pattern2(self):

        if self.counter % 10 ==0:
            self.index = (self.index+1) % 2
        self.image = self.images[self.index]
        
        if self.godown:
            self.rect = self.rect.move(self.down_movement)
            if self.rect.centery > self.bottommost:
                self.godown = False
                self.goup =  False
                self.stop = True
        
        if self.stop:
            self.pattern2_counter +=1
            self.rect = self.rect.move(self.stop_movement)
            if self.pattern2_counter % self.pattern2_bottommost_time == 0:
                self.godown = False
                self.goup = True
                self.stop = False
        
        if self.goup:
            self.rect = self.rect.move(self.up_movement)
            if self.rect.centery < self.topmost:
                self.godown = True
                self.goup = False
                self.stop = False
                self.pattern_idx = 0


    def pattern3(self):

        self.pattern3_counter+=1

        if self.counter % 10 == 0:
            self.index = (self.index+1) % 2
        self.image = self.images[self.index]

        if (self.goleft == True) and (self.reached_leftmost == False):
            self.movement[0] = -1 * self.pattern1_speed
            self.rect = self.rect.move(self.movement)

            if self.rect.left < 0:
                self.goleft = False
                self.reached_leftmost = True
                self.reached_rightmost = False
        
        else:
            self.movement[0] = self.pattern1_speed
            self.rect = self.rect.move(self.movement)

            if self.pattern1_lastmove:
                if self.rect.left > width - self.rect.width -50:
                        self.goleft = True
                        self.reached_rightmost = True
                        self.reached_leftmost = False

                        self.pattern_idx = 2
            else:
                if self.rect.left > width - self.rect.width -50:
                        self.goleft = True
                        self.reached_rightmost = True
                        self.reached_leftmost = False
            
            if self.pattern1_counter % self.pattern1_time == 0:
                self.pattern1_lastmove=True

    


    

    def update(self):

        self.counter=self.counter+1
     
        # 패턴0
        if self.pattern_idx==0:
            # self.pattern0_counter=0
            self.pattern0()

        # 패턴1 
        elif self.pattern_idx==1:
            # self.pattern1_counter = 0
            self.pattern1()
           
        # 패턴2
        else: 
            # self.pattern2_counter = 0 
            self.pattern2()

# 



class Ptera(pygame.sprite.Sprite):

    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.images, self.rect = load_sprite_sheet('ptera.png', 2, 1, sizex, sizey, -1)
        self.ptera_height = [height*0.75, height*0.68, height*0.53]
        self.rect.centery = self.ptera_height[random.randrange(0, 3)]
        self.rect.left = width + self.rect.width
        self.image = self.images[0]
        self.movement = [-1*speed, 0]
        self.index = 0
        self.counter = 0

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        if self.counter % 10 == 0:
            self.index = (self.index+1) % 2
        self.image = self.images[self.index]
        self.rect = self.rect.move(self.movement)
        self.counter = (self.counter + 1)
        if self.rect.right < 0:
            self.kill()

class Stone(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images, self.rect = load_sprite_sheet('stone.png', 1, 1, sizex, sizey, -1)
        self.rect.top = height *0.87
        self.rect.bottom = int(0.9*height)
        self.rect.left = width + self.rect.width

        #self.ptera_height = height * 0.3
        ## self.rect.centery = self.ptera_height[random.randrange(0, 3)]
        #self.rect.centery = self.ptera_height
        #self.rect.left = width - self.rect.width - 50

        self.image = self.images[0]
        self.movement = [-1*speed, 0]

    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()


class Mask_item(pygame.sprite.Sprite):
    def __init__(self, speed=5, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self,self.containers)
        self.images, self.rect = load_sprite_sheet('mask_bubble.png', 1, 1, sizex, sizey, -1)
        self.rect.bottom = random.randrange(int(0.45*height), int(height*0.995))

        
        self.rect.left = width + self.rect.width
        self.image = self.images[0] #0과 3 사이의 난수를 반환
        self.movement = [-1*speed, 0] #캐릭터에게 speed의 속도로 다가옴
        
    def draw(self):
        screen.blit(self.image, self.rect)

    def update(self):
        self.rect = self.rect.move(self.movement)

        if self.rect.right < 0:
            self.kill()


class Human(pygame.sprite.Sprite):
    
    def __init__(self, speed=0, sizex=-1, sizey=-1):
        pygame.sprite.Sprite.__init__(self)
        self.images, self.rect = load_sprite_sheet('pteraking.png', 2, 1, sizex, sizey, -1)
        self.rect.bottom = int(0.9 * height)
        self.rect.left = width - 150

        self.image = self.images[0]
        self.movement = [0, 0]
        self.stop_movement = [0,0]

        self.index = 0
        self.counter = 1
        self.isAlive=True
        self.pattern_idx=0

        self.pattern0_time=1000
        self.pattern0_counter=0
        self.pattern1_time=1000
        self.pattern1_counter = 0
        self.pattern2_time=1000
        self.pattern2_counter = 0
        self.pattern3_time=1000
        self.pattern3_counter = 0


        self.isJumping=False
        self.jumpSpeed = 11.5
        self.hp = 15

    def draw(self):
        screen.blit(self.image, self.rect)

    def checkbounds(self):
        if self.rect.bottom > int(0.9*height):
            self.rect.bottom = int(0.9*height)
            self.isJumping = False

    def pattern0(self):
        self.pattern0_counter += 1
        self.movement[0] = 0
        self.image = self.images[1]
        if self.pattern0_counter % self.pattern0_time == 0: # 200초가 넘어간 경우
            self.pattern_idx = 1

    def pattern1(self):
        self.pattern1_counter += 1
        self.movement[0] = 0
        self.image = self.images[1]
        if self.isJumping: 
            self.movement[1] = self.movement[1] + gravity # 움직임의 y값에 gravity값을 더해 점프 높이를 적용
        
        if self.pattern1_counter % self.pattern1_time == 0: # 200초가 넘어간 경우
            self.pattern_idx = 2

    def pattern2(self):
        self.pattern2_counter += 1
        self.movement[0] = 0
        self.image = self.images[1]
        if self.pattern2_counter % self.pattern2_time == 0: # 200초가 넘어간 경우
            self.pattern_idx = 3

    def pattern3(self):
        self.pattern3_counter += 1
        self.movement[0] = 0
        self.image = self.images[1]
        if self.pattern3_counter % self.pattern3_time == 0: # 200초가 넘어간 경우
            self.pattern_idx = 0

    def update(self):
        self.counter=self.counter+1
        self.rect = self.rect.move(self.movement)
        self.checkbounds()


        if self.pattern_idx==0: self.pattern0()
        elif self.pattern_idx==1: self.pattern1()
        elif self.pattern_idx==2: self.pattern2()
        elif self.pattern_idx==3: self.pattern3()

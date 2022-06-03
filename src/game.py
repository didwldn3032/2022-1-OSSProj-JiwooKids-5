from src.dino import *
from src.obstacle import *
from src.item import *
from src.interface import *
from db.db_interface import InterfDB
from time import sleep

'''
game.py : src 하위 모듈에서 생성한 클래스를 가져와 화면과 게임 기능 구현
- 시작화면 : introscreen()
- 게임옵션화면 : option()
- 게임선택화면 : selectMode()
- 이지모드 : gameplay_easy()
- 하드모드 : gameplay_hard()
- 게임 룰 설명 : gamerule()
- 게임 중단 : pausing()
- 점수등록 : typescore(score)
- 크레딧 화면 : credit()
* while 문을 돌며 입력에 따른 기능 수행시키고 반복문을 빠져나오면 게임 종료
'''

db = InterfDB("db/score.db")






## 시작 화면 ##
def introscreen():
    global resized_screen

    # temp_dino를 전역변수로 설정합니다.
    global temp_dino
    global type_idx
    global dino_type
    dino_type = ['ORIGINAL','RED','ORANGE','YELLOW','GREEN','PURPLE','BLACK','PINK']
    type_idx = 0
    ALPHA_MOVE = 20
    click_count = 0
    #
    temp_dino = Dino(dino_size[0], dino_size[1])
    temp_dino.isBlinking = True
    gameStart = False

    ###이미지 로드###
    # 배경 이미지
    alpha_back, alpha_back_rect = alpha_image('earth_bg.png', width + ALPHA_MOVE, height)
    alpha_back_rect.left = -ALPHA_MOVE
    # 버튼 이미지
    r_btn_gamestart, r_btn_gamestart_rect = load_image(*resize('btn_start.png', 150, 50, -1))
    btn_gamestart, btn_gamestart_rect = load_image('btn_start.png', 150, 50, -1)
    r_btn_board, r_btn_board_rect = load_image(*resize('btn_board.png', 150, 50, -1))
    btn_board, btn_board_rect = load_image('btn_board.png', 150, 50, -1)
    r_btn_option, r_btn_option_rect = load_image(*resize('btn_option.png', 150, 50, -1))
    btn_option, btn_option_rect = load_image('btn_option.png', 150, 50, -1)
    # DINO IMAGE


    while not gameStart:
        if pygame.display.get_surface() == None:
            print("Couldn't load display surface")
            return True
        else:
            #for 문으로 동시에 일어나는 여러 이벤트를 event.get()통해 이벤트 감지, 이를 리스트에 저장하고 차례로 반환하며 처리
            for event in pygame.event.get():
                # 이두용이 작성1 시작:
                if event.type == pygame.VIDEORESIZE and not full_screen:
                    r_btn_gamestart, r_btn_gamestart_rect = load_image(*resize('btn_start.png', 150, 50, -1))
                    btn_gamestart, btn_gamestart_rect = load_image('btn_start.png', 150, 50, -1)
                    r_btn_board, r_btn_board_rect = load_image(*resize('btn_board.png', 150, 50, -1))
                    btn_board, btn_board_rect = load_image('btn_board.png', 150, 50, -1)
                    r_btn_option, r_btn_option_rect = load_image(*resize('btn_option.png', 150, 50, -1))
                    btn_option, btn_option_rect = load_image('btn_option.png', 150, 50, -1)

                    ###IMGPOS###
                    #BACKGROUND IMG POS
                    alpha_back_rect.bottomleft = (width*0, height)
                    #이두용이 작성1 끝.

                #이벤트 타입이 quit이면 while문 빠져나가며 게임종료
                if event.type == pygame.QUIT:
                    return True

                # 버튼 클릭했을 때 event
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        x, y = event.pos
                        #game button
                        if r_btn_gamestart_rect.collidepoint(x, y):
                            temp_dino.isJumping = True
                            temp_dino.isBlinking = False
                            temp_dino.movement[1] = -1 * temp_dino.jumpSpeed

                        #board button
                        if r_btn_board_rect.collidepoint(x, y):
                            board()
                        # option button
                        if r_btn_option_rect.collidepoint(x, y):
                            option()

                        # temp_dino를 누르는 경우: 
                        if temp_dino.rect.collidepoint(x, y):
                            click_count += 1 
                            type_idx = click_count % len(dino_type)
                            temp_dino = Dino(dino_size[0], dino_size[1],type = dino_type[type_idx])
                            temp_dino.isBlinking = True

        temp_dino.update()

        # interface draw
        if pygame.display.get_surface() != None:

            r_btn_gamestart_rect.centerx, r_btn_board_rect.centerx, r_btn_option_rect.centerx = resized_screen.get_width() * 0.72, resized_screen.get_width() * 0.72, resized_screen.get_width() * 0.72
            r_btn_gamestart_rect.centery, r_btn_board_rect.centery, r_btn_option_rect.centery = resized_screen.get_height() * 0.5, resized_screen.get_height() * (0.5+button_offset), resized_screen.get_height() * (0.5+2*button_offset)

            screen.blit(alpha_back, alpha_back_rect)
            disp_intro_buttons(btn_gamestart, btn_board, btn_option)

            temp_dino.draw()
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())), resized_screen_centerpos)

        pygame.display.update()

        #tick 통해 FPS 설정
        clock.tick(FPS)

        if temp_dino.isJumping == False and temp_dino.isBlinking == False:
            gameStart = True
            selectMode()

    #while문 빠져나가면 게임 종료
    pygame.quit()
    quit()


def option():
    global on_pushtime;
    global off_pushtime
    global bgm_on
    global high_score
    global resized_screen

    btnpush_interval = 500  # ms
    pygame.mixer.music.stop()
    done = False
    ALPHA_MOVE = 20
    db_init = False

    alpha_back, alpha_back_rect = alpha_image('option_bg.png', width + ALPHA_MOVE, height)
    alpha_back_rect.left = -ALPHA_MOVE
    btn_bgm_on, btn_bgm_on_rect = load_image('btn_bgm_on.png', 60, 60, -1);
    btn_bgm_off, btn_bgm_off_rect = load_image('btn_bgm_off.png', 60, 60, -1)
    r_btn_bgm_on, r_btn_bgm_on_rect = load_image(*resize('btn_bgm_on.png', 60, 60, -1))
    init_btn_image, init_btn_rect = load_image('scorereset.png', 60, 60, -1)
    r_init_btn_image, r_init_btn_rect = load_image(*resize('scorereset.png', 60, 60, -1))
    btn_gamerule, btn_gamerule_rect = load_image('btn_gamerule.png', 60, 60, -1)
    r_btn_gamerule, r_btn_gamerule_rect = load_image(*resize('btn_gamerule.png', 60, 60, -1))
    btn_home, btn_home_rect = load_image('main_button.png', 70, 62, -1)
    r_btn_home, r_btn_home_rect = load_image(*resize('main_button.png', 70, 62, -1))
    btn_credit, btn_credit_rect = load_image('btn_credit.png', 150, 50, -1)
    r_btn_credit, r_btn_credit_rect = load_image(*resize('btn_credit.png', 150, 50, -1))

    btn_bgm_on_rect.center = (width * 0.25, height * 0.5)
    init_btn_rect.center = (width * 0.5, height * 0.5)
    btn_gamerule_rect.center = (width * 0.75, height * 0.5)
    btn_home_rect.center = (width * 0.9, height * 0.15)
    btn_credit_rect.center = (width * 0.9, height * 0.85)

    while not done:
        for event in pygame.event.get():

            # CHANGE SIZE START
            if event.type == pygame.VIDEORESIZE and not full_screen:
                # r_btn_gamestart, r_btn_gamestart_rect = load_image(*resize('btn_start.png', 150, 50, -1))
                # btn_gamestart, btn_gamestart_rect = load_image('btn_start.png', 150, 50, -1)
                # r_btn_board, r_btn_board_rect = load_image(*resize('btn_board.png', 150, 50, -1))
                # btn_board, btn_board_rect = load_image('btn_board.png', 150, 50, -1)
                # r_btn_option, r_btn_option_rect = load_image(*resize('btn_option.png', 150, 50, -1))
                # btn_option, btn_option_rect = load_image('btn_option.png', 150, 50, -1)
                pass
                ###IMGPOS###
                #BACKGROUND IMG POS
                # Background_rect.bottomleft = (width*0, height)
            
            # CHANGE SIZE END

            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    x, y = event.pos
                    if r_btn_home_rect.collidepoint(x, y):
                        introscreen()

                    if r_btn_bgm_on_rect.collidepoint(x, y) and bgm_on:
                        off_pushtime = pygame.time.get_ticks()
                        if off_pushtime - on_pushtime > btnpush_interval:
                            bgm_on = False

                    if r_btn_bgm_on_rect.collidepoint(x, y) and not bgm_on:
                        on_pushtime = pygame.time.get_ticks()
                        if on_pushtime - off_pushtime > btnpush_interval:
                            bgm_on = True

                    if r_init_btn_rect.collidepoint(x, y):
                        db.query_db("delete from user;")
                        db.commit()
                        high_score = 0
                        db_init = True

                    if r_btn_gamerule_rect.collidepoint(x, y):
                        gamerule()

                    if r_btn_credit_rect.collidepoint(x, y):
                        credit()

            # if event.type == pygame.VIDEORESIZE:
            #     checkscrsize(event.w, event.h)

        r_init_btn_rect.centerx, r_init_btn_rect.centery = resized_screen.get_width() * 0.5, resized_screen.get_height() * 0.5
        r_btn_gamerule_rect.centerx, r_btn_gamerule_rect.centery = resized_screen.get_width() * 0.75, resized_screen.get_height() * 0.5
        r_btn_home_rect.centerx, r_btn_home_rect.centery = resized_screen.get_width() * 0.9, resized_screen.get_height() * 0.15
        r_btn_credit_rect.centerx, r_btn_credit_rect.centery = resized_screen.get_width() * 0.9, resized_screen.get_height() * 0.85

        #스크린에 색 채움
        screen.blit(alpha_back, alpha_back_rect)
        screen.blit(init_btn_image, init_btn_rect)
        screen.blit(btn_gamerule, btn_gamerule_rect)
        screen.blit(btn_home, btn_home_rect)
        screen.blit(btn_credit, btn_credit_rect)

        if bgm_on:
            screen.blit(btn_bgm_on, btn_bgm_on_rect)
            r_btn_bgm_on_rect.centerx, r_btn_bgm_on_rect.centery = resized_screen.get_width() * 0.25, resized_screen.get_height() * 0.5
        if not bgm_on:
            screen.blit(btn_bgm_off, btn_bgm_on_rect)
            r_btn_bgm_on_rect.centerx, r_btn_bgm_on_rect.centery = resized_screen.get_width() * 0.25, resized_screen.get_height() * 0.5
        if db_init:
            draw_text("Scoreboard cleared", font, screen, 400, 300, black)

        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_centerpos)
        pygame.display.update()

        clock.tick(FPS)
    pygame.quit()
    quit()



def selectMode():
    global resized_screen
    gameStart = False
    ALPHA_MOVE = 20
    btnpush_interval = 500

    # 버튼 이미지

    ##easy mode button
    easymode_btn_image, easymode_btn_rect = alpha_image('ranking.png', 200, 60, -1)
    r_easymode_btn_image, r_easy_btn_rect = alpha_image(*resize('ranking.png', 200, 60, -1))
    # hardmode button
    btn_hardmode, btn_hardmode_rect = alpha_image('story.png', 200, 60, -1)
    r_btn_hardmode, r_btn_hardmode_rect = alpha_image(*resize('story.png', 200, 60, -1))
    # 배경 이미지
    alpha_back, alpha_back_rect = alpha_image('earth_bg.png', width + ALPHA_MOVE, height)
    alpha_back_rect.left = -ALPHA_MOVE


    easymode_btn_rect.center = (width * 0.5, height * 0.5)
    btn_hardmode_rect.center = (width * 0.5, height * 0.75)


    while not gameStart:
        for event in pygame.event.get():
            
            if event.type == pygame.QUIT:
                gameStart = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    x, y = event.pos
                    if r_easy_btn_rect.collidepoint(x, y):
                        gameplay_rank()

                    if r_btn_hardmode_rect.collidepoint(x, y):
                        ItemSelectMode()

            if event.type == pygame.VIDEORESIZE:
                checkscrsize(event.w, event.h)

        r_easy_btn_rect.centerx, r_easy_btn_rect.centery = resized_screen.get_width() * 0.5, resized_screen.get_height() * 0.5
        r_btn_hardmode_rect.centerx, r_btn_hardmode_rect.centery = resized_screen.get_width() * 0.5, resized_screen.get_height() * (
                0.5 + button_offset)
        

        screen.blit(alpha_back, alpha_back_rect)
        screen.blit(easymode_btn_image, easymode_btn_rect)
        screen.blit(btn_hardmode, btn_hardmode_rect)


        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_centerpos)
        pygame.display.update()

        clock.tick(FPS)
    pygame.quit()
    quit()

#스토리모드별 아이템 변수
item_story1 = False
item_story2 = False
item_story3 = False
item_story4 = False
#아이템 체크 횟수
item_cnt=0

def ItemSelectMode():
    global item_story1
    global item_story2
    global item_story3
    global item_story4
    global item_cnt
    ALPHA_MOVE = 20
    width_offset = 0.2
    resized_screen_center = (0, 0)
    global resized_screen
    game_start = False

    # 배경 이미지
    # back_store, back_store_rect = load_image('intro_bg.png', width, height)
    alpha_back, alpha_back_rect = alpha_image('Earth_bg.png', width + ALPHA_MOVE, height)
    alpha_back_rect.left = -ALPHA_MOVE

    # 버튼 이미지
    sung_btn_image, sung_btn_rect = alpha_image('sunglass.png', 150, 150, -1)
    r_sung_btn_image, r_sung_btn_rect = alpha_image(*resize('sunglass.png', 150, 150, -1))
    shov_btn_image, shov_btn_rect = alpha_image('shovel.png', 150, 150, -1)
    r_shov_btn_image, r_shov_btn_rect = alpha_image(*resize('shovel.png', 150, 150, -1))
    umbr_btn_image, umbr_btn_rect = load_image('umbrella.png', 150, 150, -1)
    r_umbr_btn_image, r_umbr_btn_rect = load_image(*resize('umbrella.png', 150, 150, -1))
    mask_btn_image, mask_btn_rect = load_image('mask.png', 150, 150, -1)
    r_mask_btn_image, r_mask_btn_rect = load_image(*resize('mask.png', 150, 150, -1))
    


    item_story1 = False
    item_story2 = False
    item_story3 = False
    item_story4 = False

    lets_btn_image, lets_btn_rect = load_image('LetsGo.png', 100, 30, -1)
    r_lets_btn_image, r_lets_btn_rect = load_image(*resize('LetsGo.png', 100, 30, -1))
    option_btn_image, option_btn_rect = load_image('btn_option.png', 100, 30, -1)
    r_option_btn_image, r_option_btn_rect = load_image(*resize('btn_option.png', 100, 30, -1))

    while not game_start:
        for event in pygame.event.get():
            # if event.type == pygame.VIDEORESIZE and not full_screen:
            #     back_store_rect.bottomleft = (width * 0, height)
            if event.type == pygame.VIDEORESIZE:
                check_scr_size(event.w, event.h)
            if event.type == pygame.QUIT:
                game_start = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pressed() == (1, 0, 0):
                    x, y = pygame.mouse.get_pos()
                    if r_sung_btn_rect.collidepoint(x, y):
                        if item_story1==False:
                            if item_cnt>=2:
                                pass
                            else:
                                item_story1=True
                                item_cnt+=1
                        else:
                            item_story1=False
                            item_cnt-=1
                    if r_shov_btn_rect.collidepoint(x, y):
                        if item_story2==False:
                            if item_cnt>=2:
                                    pass
                            else:
                                item_story2=True
                                item_cnt+=1
                        else:
                            item_story2=False
                            item_cnt-=1
                    if r_umbr_btn_rect.collidepoint(x, y):
                        if item_story3==False:
                            if item_cnt>=2:
                                    pass
                            else:
                                item_story3=True
                                item_cnt+=1
                        else:
                            item_story3=False
                            item_cnt-=1
                    if r_mask_btn_rect.collidepoint(x, y):
                        if item_story4==False:
                            if item_cnt>=2:
                                    pass
                            else:
                                item_story4=True
                                item_cnt+=1
                        else:
                            item_story4=False
                            item_cnt-=1
                    if r_lets_btn_rect.collidepoint(x, y):
                        gameplay_story2()
                    # if r_start_btn_rect.collidepoint(x, y):
                    #     gameplay_story1()

        if item_story1 == False:
            sung_btn_image, sung_btn_rect = alpha_image('sunglass.png', 150, 150, -1)
            r_sung_btn_image, r_sung_btn_rect = alpha_image(*resize('sunglass.png', 150, 150, -1))
        else:
            sung_btn_image, sung_btn_rect = alpha_image('sunglasson.png', 150, 150, -1)
            r_sung_btn_image, r_sung_btn_rect = alpha_image(*resize('sunglasson.png', 150, 150, -1))
        
        if item_story2 == False:
            shov_btn_image, shov_btn_rect = alpha_image('shovel.png', 150, 150, -1)
            r_shov_btn_image, r_shov_btn_rect = alpha_image(*resize('shovel.png', 150, 150, -1))
        else:
            shov_btn_image, shov_btn_rect = alpha_image('shovelon.png', 150, 150, -1)
            r_shov_btn_image, r_shov_btn_rect = alpha_image(*resize('shovelon.png', 150, 150, -1))
        
        if item_story3 == False:
            umbr_btn_image, umbr_btn_rect = load_image('umbrella.png', 150, 150, -1)
            r_umbr_btn_image, r_umbr_btn_rect = load_image(*resize('umbrella.png', 150, 150, -1))
        else:
            umbr_btn_image, umbr_btn_rect = load_image('umbrellaon.png', 150, 150, -1)
            r_umbr_btn_image, r_umbr_btn_rect = load_image(*resize('umbrellaon.png', 150, 150, -1))
        
        if item_story4 == False:
            mask_btn_image, mask_btn_rect = load_image('mask.png', 150, 150, -1)
            r_mask_btn_image, r_mask_btn_rect = load_image(*resize('mask.png', 150, 150, -1))
        else:
            mask_btn_image, mask_btn_rect = load_image('maskon.png', 150, 150, -1)
            r_mask_btn_image, r_mask_btn_rect = load_image(*resize('maskon.png', 150, 150, -1))
        

        r_sung_btn_rect.centerx = resized_screen.get_width() * 0.2
        r_sung_btn_rect.centery = resized_screen.get_height() * 0.6
        r_shov_btn_rect.centerx = resized_screen.get_width() * (0.2 + width_offset)
        r_shov_btn_rect.centery = resized_screen.get_height() * 0.6
        r_umbr_btn_rect.centerx = resized_screen.get_width() * (0.2 + 2 * width_offset)
        r_umbr_btn_rect.centery = resized_screen.get_height() * 0.6
        r_mask_btn_rect.centerx = resized_screen.get_width() * (0.2 + 3 * width_offset)
        r_mask_btn_rect.centery = resized_screen.get_height() * 0.6
        r_lets_btn_rect.centerx = resized_screen.get_width() * 0.1
        r_lets_btn_rect.centery = resized_screen.get_height() * 0.1
        # r_start_btn_rect.centerx = resized_screen.get_width() * 0.1
        # r_start_btn_rect.centery = resized_screen.get_height() * 0.1
        # screen.blit(back_store, back_store_rect)
        screen.blit(alpha_back, alpha_back_rect)
        disp_store_buttons(sung_btn_image, shov_btn_image, umbr_btn_image, lets_btn_image, mask_btn_image)
        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_center)
        pygame.display.update()
        clock.tick(FPS)
    pygame.quit()
    quit()

## 게임 작동 ##



def gameplay_rank():
    global resized_screen
    global high_score
    
    result = db.query_db("select score from user order by score desc;", one=True)
    if result is not None:
        high_score = result['score']

    # HERE: REMOVE SOUND!!    
    # if bgm_on:
    #     pygame.mixer.music.play(-1)  # 배경음악 실행
    
    gamespeed = 4
    startMenu = False
    gameOver = False
    gameQuit = False
    ###
    life = 5
    ###
    paused = False
    
    # 디노 타입 때문에 변경된 부분
    playerDino = Dino(dino_size[0], dino_size[1], type = dino_type[type_idx])
    # 

    new_ground = Ground(-1 * gamespeed)
    scb = Scoreboard()
    heart = HeartIndicator(life)
    boss = boss_heart()
    counter = 0
    


    cacti = pygame.sprite.Group()
    fire_cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    stones = pygame.sprite.Group() #add stones
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()
    shield_items = pygame.sprite.Group()
    life_items = pygame.sprite.Group()
    slow_items = pygame.sprite.Group()


    Cactus.containers = cacti
    fire_Cactus.containers = fire_cacti
    Ptera.containers = pteras
    Cloud.containers = clouds
    ShieldItem.containers = shield_items
    LifeItem.containers = life_items
    SlowItem.containers = slow_items
    Stone.containers = stones # add stone containers

    # BUTTON IMG LOAD
    # retbutton_image, retbutton_rect = load_image('replay_button.png', 70, 62, -1)
    gameover_image, gameover_rect = load_image('game_over.png', 380, 22, -1)
    
    # 1. 미사일 발사.
    space_go=False
    m_list=[]
    bk=0
    # 익룡이 격추되었을때
    isDown=False
    boomCount=0
    #

    # 방향키 구현
    goLeft=False
    goRight=False
    #

    # 보스몬스터 변수설정
    isPkingTime=False
    isPkingAlive=True
    pking=PteraKing()
    pm_list = []
    pm_vector = []
    pm_pattern0_count = 0
    pm_pattern1_count = 0
    pking_appearance_score = 100
    #

    #
    jumpingx2 = False

    while not gameQuit:
        while startMenu:
            pass
        while not gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:  # 스페이스 누르는 시점에 공룡이 땅에 닿아있으면 점프한다.
                            if playerDino.rect.bottom == int(0.9 * height):
                                playerDino.isJumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if event.key == pygame.K_DOWN:  # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                        if event.key == pygame.K_LEFT:
                            # print("left")
                            goLeft=True

                        if event.key == pygame.K_RIGHT:
                            # print("right")
                            goRight=True

                        if event.key == pygame.K_ESCAPE:
                            paused = not paused
                            paused = pausing()

                        # jumping x2 ( press key s)
                        if event.key == pygame.K_s:
                            jumpingx2=True

                        # 2. a키를 누르면, 미사일이 나갑니다.
                        if event.key == pygame.K_a:
                            space_go=True
                            bk=0
                        #

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            playerDino.isDucking = False

                        # 3.a키에서 손을 떼면, 미사일이 발사 되지 않습니다.
                        if event.key == pygame.K_a:
                            space_go = False
                        #

                        # 방향키 추가
                        if event.key == pygame.K_LEFT:
                            goLeft=False

                        if event.key == pygame.K_RIGHT:
                            goRight=False
                        #

                        ## jumgpingx2
                        if event.key == pygame.K_s:
                            jumpingx2 = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed() == (1, 0, 0) and playerDino.rect.bottom == int(0.9 * height):
                            # (mouse left button, wheel button, mouse right button)
                            playerDino.isJumping = True
                            if pygame.mixer.get_init() != None:
                                jump_sound.play()
                            playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if pygame.mouse.get_pressed() == (0, 0, 1):
                            # (mouse left button, wheel button, mouse right button)
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                    if event.type == pygame.MOUSEBUTTONUP:
                        playerDino.isDucking = False

                    if event.type == pygame.VIDEORESIZE:
                        checkscrsize(event.w, event.h)

            if not paused:

                # [05.01 안도현] 하드 모드에서 화면 밖으로 이탈하는 프레임 아웃 문제 해결 
                if goLeft:
                    if playerDino.rect.left < 0:
                        playerDino.rect.left = 0
                    else:
                        playerDino.rect.left = playerDino.rect.left - gamespeed

                if goRight:
                    if playerDino.rect.right > width:
                        playerDino.rect.right = width
                    else:
                        playerDino.rect.left = playerDino.rect.left + gamespeed
                #

                # 4. space_go가 True이고, 일정 시간이 지나면, 미사일을 만들고, 이를 미사일 배열에 넣습니다.
                if (space_go==True) and (int(bk%100)==0):
                    # print(bk)
                    mm=obj()

                    # 디노의 종류에 따라 다른 총알이 나가도록 합니다.
                    if playerDino.type == 'RED':
                        mm.put_img("./sprites/black_bullet.png")
                        mm.change_size(15,15)
                    elif playerDino.type == 'YELLOW':
                        mm.put_img("./sprites/blue_bullet.png")
                        mm.change_size(15,15)
                    elif playerDino.type == 'ORANGE':
                        mm.put_img("./sprites/blue_bullet.png")
                        mm.change_size(15,15)
                    elif playerDino.type == 'PURPLE':
                        mm.put_img("./sprites/pink_bullet.png")
                        mm.change_size(15,15)
                    elif playerDino.type == 'PINK':
                        mm.put_img("./sprites/heart_bullet.png")
                        mm.change_size(15,15)
                    else:                    
                        mm.put_img("./sprites/red_bullet.png")
                        mm.change_size(15,15)
                    # 
                    
                    if playerDino.isDucking ==False:
                        mm.x = round(playerDino.rect.centerx)
                        mm.y = round(playerDino.rect.top*1.035)
                    if playerDino.isDucking ==True:
                        mm.x = round(playerDino.rect.centerx)
                        mm.y = round(playerDino.rect.centery*1.01)
                    mm.move = 15
                    m_list.append(mm)
                bk=bk+1
                d_list=[]

                #미사일 하나씩 꺼내옴
                for i in range(len(m_list)):
                    m=m_list[i]
                    m.x +=m.move
                    if m.x>width:
                        d_list.append(i)

                d_list.reverse()
                for d in d_list:
                    del m_list[d]
                #

                if jumpingx2 :
                    if  playerDino.rect.bottom == int(height * 0.9):
                        playerDino.isJumping = True
                        playerDino.movement[1] = -1 * playerDino.superJumpSpeed

                # 보스 몬스터 패턴0(위에서 가만히 있는 패턴): 보스 익룡이 쏘는 미사일.
                if (isPkingTime) and (pking.pattern_idx == 0) and (int(pm_pattern0_count % 20) == 0):
                    pm=obj()
                    pm.put_img("./sprites/pking bullet.png")
                    pm.change_size(15,15)
                    pm.x = round(pking.rect.centerx)
                    pm.y = round(pking.rect.centery)
                    pm.xmove = random.randint(0,15)
                    pm.ymove = random.randint(1,3)

                    pm_list.append(pm)
                pm_pattern0_count += 1
                pd_list = []

                for i in range(len(pm_list)):
                    pm = pm_list[i]
                    pm.x -= pm.xmove
                    pm.y += pm.ymove
                    if pm.y > height or pm.x < 0:
                        pd_list.append(i)
                pd_list.reverse()
                for d in pd_list:
                    del pm_list[d]


                #

                # 보스 몬스터 패턴1(좌우로 왔다갔다 하는 패턴): 보스 익룡이 쏘는 미사일.
                if (isPkingTime) and (pking.pattern_idx == 1) and (int(pm_pattern1_count % 20) == 0):
                    print(pm_list)
                    pm=obj()
                    pm.put_img("./sprites/pking bullet.png")
                    pm.change_size(15,15)
                    pm.x = round(pking.rect.centerx)
                    pm.y = round(pking.rect.centery)
                    pm.move = 3
                    pm_list.append(pm)
                pm_pattern1_count += 1
                pd_list = []

                for i in range(len(pm_list)):
                    pm=pm_list[i]
                    pm.y +=pm.move
                    if pm.y>height or pm.x < 0:
                        pd_list.append(i)

                pd_list.reverse()
                for d in pd_list:
                    del pm_list[d]
                #


                for c in cacti:
                    c.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, c):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False

                for f in fire_cacti:
                    f.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, f):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False

                for p in pteras:
                    p.movement[0] = -1 * gamespeed

                    # 7. 익룡이 미사일에 맞으면 익룡과 미사일 모두 사라집니다.

                    if (len(m_list)==0):
                        pass
                    else:
                        if (m.x>=p.rect.left)and(m.x<=p.rect.right)and(m.y>p.rect.top)and(m.y<p.rect.bottom):
                            print("격추 성공")
                            isDown=True
                            boom=obj()
                            boom.put_img("./sprites/boom.png")
                            boom.change_size(200,100)
                            boom.x=p.rect.centerx-round(p.rect.width)*2.5
                            boom.y=p.rect.centery-round(p.rect.height)*1.5
                            playerDino.score+=30
                            p.kill()
                            # 여기만 바꿈
                            m_list.remove(m)
                            #
                    #

                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, p):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False

                for s in stones:
                    s.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, s):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                if not playerDino.isSuper:
                    for s in shield_items:
                        s.movement[0] = -1 * gamespeed
                        if pygame.sprite.collide_mask(playerDino, s):
                            if pygame.mixer.get_init() is not None:
                                checkPoint_sound.play()
                            playerDino.collision_immune = True
                            playerDino.isSuper = True
                            s.kill()
                            item_time = pygame.time.get_ticks()
                        elif s.rect.right < 0:
                            s.kill()
                else:
                    for s in shield_items:
                        s.movement[0] = -1 * gamespeed
                        if pygame.sprite.collide_mask(playerDino, s):
                            if pygame.mixer.get_init() is not None:
                                checkPoint_sound.play()
                            playerDino.collision_immune = True
                            playerDino.isSuper = True
                            s.kill()
                            item_time = pygame.time.get_ticks()
                        elif s.rect.right < 0:
                            s.kill()

                    if pygame.time.get_ticks() - item_time > shield_time:
                        playerDino.collision_immune = False
                        playerDino.isSuper = False

                for l in life_items:
                    l.movement[0] = -1 * gamespeed
                    if pygame.sprite.collide_mask(playerDino, l):
                        if pygame.mixer.get_init() is not None:
                            checkPoint_sound.play()
                        life += 1
                        l.kill()
                    elif l.rect.right < 0:
                        l.kill()

                for k in slow_items:
                    k.movement[0] = -1 * gamespeed
                    if pygame.sprite.collide_mask(playerDino, k):
                        if pygame.mixer.get_init() is not None:
                            checkPoint_sound.play()
                        gamespeed -= 1
                        new_ground.speed += 1
                        k.kill()
                    elif k.rect.right < 0:
                        k.kill()


                STONE_INTERVAL = 100
                CACTUS_INTERVAL = 50
                # 익룡을 더 자주 등장시키기 위해 12로 수정했습니다. (원래값은 300)
                PTERA_INTERVAL = 12
                #
                CLOUD_INTERVAL = 300
                SHIELD_INTERVAL = 500
                LIFE_INTERVAL = 1000
                SLOW_INTERVAL = 1000

                OBJECT_REFRESH_LINE = width * 0.8
                MAGIC_NUM = 10

                # print(pking.hp)
                if (isPkingAlive)and(playerDino.score>pking_appearance_score):
                    isPkingTime=True
                else:
                    isPkingTime = False

                if isPkingTime:
                    if len(cacti) < 2:
                        if len(cacti) == 0:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))
                    else:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))

                    if len(fire_cacti) < 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL*5) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(fire_Cactus(gamespeed, object_size[0], object_size[1]))

                    if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                        Cloud(width, random.randrange(height / 5, height / 2))

                    if (len(m_list)==0):
                        pass
                    else:
                        if (m.x>=pking.rect.left)and(m.x<=pking.rect.right)and(m.y>pking.rect.top)and(m.y<pking.rect.bottom):
                            isDown=True
                            boom=obj()
                            boom.put_img("./sprites/boom.png")
                            boom.change_size(200,100)
                            boom.x=pking.rect.centerx-round(pking.rect.width)
                            boom.y=pking.rect.centery-round(pking.rect.height/2)
                            pking.hp -= 1
                            m_list.remove(m)

                            if pking.hp <= 0:
                                pking.kill()
                                isPkingAlive=False

                    #
                    if (len(pm_list)==0):
                        pass
                    else:
                        # print("x: ",pm.x,"y: ",pm.y)
                        for pm in pm_list:
                            if (pm.x>=playerDino.rect.left)and(pm.x<=playerDino.rect.right)and(pm.y>playerDino.rect.top)and(pm.y<playerDino.rect.bottom):
                                print("공격에 맞음.")
                                # if pygame.sprite.collide_mask(playerDino, pm):
                                playerDino.collision_immune = True
                                life -= 1
                                collision_time = pygame.time.get_ticks()
                                if life == 0:
                                    playerDino.isDead = True
                                pm_list.remove(pm)
                    #
                else:
                    if len(cacti) < 2:
                        if len(cacti) == 0:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))
                        else:
                            for l in last_obstacle:
                                if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL) == MAGIC_NUM:
                                    last_obstacle.empty()
                                    last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))

                    if len(fire_cacti) < 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL * 5) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(fire_Cactus(gamespeed, object_size[0], object_size[1]))

                    if len(stones) < 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(STONE_INTERVAL * 5) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Stone(gamespeed, object_size[0], object_size[1]))


                    if len(pteras) == 0 and random.randrange(PTERA_INTERVAL) == MAGIC_NUM and counter > PTERA_INTERVAL:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE:
                                last_obstacle.empty()
                                last_obstacle.add(Ptera(gamespeed, ptera_size[0], ptera_size[1]))

                    if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                        Cloud(width, random.randrange(height / 5, height / 2))

                    if len(shield_items) == 0 and random.randrange(
                            SHIELD_INTERVAL) == MAGIC_NUM and counter > SHIELD_INTERVAL:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE:
                                last_obstacle.empty()
                                last_obstacle.add(ShieldItem(gamespeed, object_size[0], object_size[1]))

                    if len(life_items) == 0 and random.randrange(
                            LIFE_INTERVAL) == MAGIC_NUM and counter > LIFE_INTERVAL * 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE:
                                last_obstacle.empty()
                                last_obstacle.add(LifeItem(gamespeed, object_size[0], object_size[1]))

                    if len(slow_items) == 0 and random.randrange(SLOW_INTERVAL) == MAGIC_NUM and counter > SLOW_INTERVAL:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE:
                                last_obstacle.empty()
                                last_obstacle.add(SlowItem(gamespeed, object_size[0], object_size[1]))

                playerDino.update()
                cacti.update()
                fire_cacti.update()
                stones.update()
                pteras.update()
                clouds.update()
                shield_items.update()
                life_items.update()

                new_ground.update()
                scb.update(playerDino.score,high_score)
                boss.update(pking.hp)
                heart.update(life)
                slow_items.update()

                # 보스몬스터 타임이면,
                if isPkingTime:
                    pking.update()
                #

                if pygame.display.get_surface() != None:
                    screen.fill(background_col)
                    new_ground.draw()
                    clouds.draw(screen)
                    scb.draw()
                    boss.draw()
                    heart.draw()
                    cacti.draw(screen)
                    fire_cacti.draw(screen)
                    stones.draw(screen)
                    pteras.draw(screen)
                    shield_items.draw(screen)
                    life_items.draw(screen)
                    slow_items.draw(screen)

                    # pkingtime이면, 보스몬스터를 보여줘라.
                    if isPkingTime:
                        # print(pking.pattern_idx)
                        pking.draw()
                        # 보스 익룡이 쏘는 미사일을 보여준다.
                        for pm in pm_list:
                            pm.show()
                    #

                   # 5. 미사일 배열에 저장된 미사일들을 게임 스크린에 그려줍니다.
                    for m in m_list:
                        m.show()
                        # print(type(mm.x))
                    if isDown :
                        boom.show()
                        boomCount+=1
                        # boomCount가 5가 될 때까지 boom이미지를 계속 보여준다.
                        if boomCount>10:
                            boomCount=0
                            isDown=False
                    #

                    playerDino.draw()
                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                        resized_screen_centerpos)
                    pygame.display.update()
                clock.tick(FPS)

                if playerDino.isDead:
                    gameOver = True
                    pygame.mixer.music.stop()  # 죽으면 배경음악 멈춤
                    if playerDino.score > high_score:
                        high_score = playerDino.score

                if counter % speed_up_limit_count == speed_up_limit_count - 1:
                    new_ground.speed -= 1
                    gamespeed += 1

                counter = (counter + 1)

        if gameQuit:
            break

        while gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            gameOver = False
                            gameQuit = True
                            typescore(playerDino.score)
                            if not db.is_limit_data(playerDino.score):
                                db.query_db(
                                    f"insert into user(username, score) values ('{gamername}', '{playerDino.score}');")
                                db.commit()
                                board()
                            else:
                                board()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        gameOver = False
                        gameQuit = True
                        typescore(playerDino.score)
                        if not db.is_limit_data(playerDino.score):
                            db.query_db(
                                f"insert into user(username, score) values ('{gamername}', '{playerDino.score}');")
                            db.commit()
                            board()
                        else:
                            board()

                    if event.type == pygame.VIDEORESIZE:
                        checkscrsize(event.w, event.h)

            scb.update(playerDino.score,high_score)
            boss.update(pking.hp)
            if pygame.display.get_surface() != None:
                disp_gameOver_msg(gameover_image)
                scb.draw()
                boss.draw()
                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_centerpos)
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()


Shovel = False #삽

## 미세먼지 ##
def gameplay_story1():
    global item_story1
    Sunglass = False #선글라스
    global resized_screen
    global high_score
    result = db.query_db("select score from user order by score desc;", one=True)
    if result is not None:
        high_score = result['score']
    #    if bgm_on:
    #       pygame.mixer.music.play(-1) # 배경음악 실행
    gamespeed = 4
    startMenu = False
    gameOver = False
    gameClear = False
    gameQuit = False
    ###
    life = 5
    ###
    paused = False

    #배경이미지
    back_image,back_rect = load_image('new_rock_2.png',800,400,-1)
    #먼지이미지
    dust_image,dust_rect = load_image('dust.png',800,400,-1)

    #불투명도
    dustnum=0
    dust_image.set_alpha(dustnum)

    playerDino = Dino(dino_size[0], dino_size[1], type=dino_type[type_idx])

    new_ground = Ground(-1 * gamespeed)
    s_scb = Story_Scoreboard()
    heart = HeartIndicator(life)
    counter = 0

    cacti = pygame.sprite.Group()
    fire_cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    # add stones
    stones = pygame.sprite.Group()

    last_obstacle = pygame.sprite.Group()
    shield_items = pygame.sprite.Group()
    life_items = pygame.sprite.Group()
    slow_items = pygame.sprite.Group()
    # highjump_items = pygame.sprite.Group()

    Stone.containers = stones

    Cactus.containers = cacti
    fire_Cactus.containers = fire_cacti
    Ptera.containers = pteras
    Cloud.containers = clouds
    ShieldItem.containers = shield_items
    LifeItem.containers = life_items
    SlowItem.containers = slow_items
    # HighJumpItem.containers = highjump_items

    # BUTTON IMG LOAD
    # retbutton_image, retbutton_rect = load_image('replay_button.png', 70, 62, -1)
    gameover_image, gameover_rect = load_image('game_over.png', 380, 22, -1)

    #방향키 구현
    goLeft=False
    goRight=False
    #2단 점프
    jumpingx2=False

    while not gameQuit:
        while startMenu:
            pass
        while not gameOver and not gameClear:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True


            else:
                screen.fill(background_col)
                screen.blit(back_image,back_rect)
                pygame.display.update()

                

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # 종료
                        gameQuit = True
                        gameOver = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:  # 스페이스 누르는 시점에 공룡이 땅에 닿아있으면 점프한다.
                            if playerDino.rect.bottom == int(0.9 * height):
                                playerDino.isJumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if event.key == pygame.K_DOWN:  # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                        if event.key == pygame.K_ESCAPE:
                            paused = not paused
                            paused = pausing()

                        if event.key == pygame.K_LEFT:
                            goLeft=True
                        
                        if event.key == pygame.K_RIGHT:
                            goRight=True
                        
                        if event.key == pygame.K_s:
                            jumpingx2=True

                        if event.key == pygame.K_d:
                            if item_story1 == True:
                                Sunglass=True

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            playerDino.isDucking = False

                        if event.key == pygame.K_LEFT:
                            goLeft=False
                        
                        if event.key == pygame.K_RIGHT:
                            goRight=False

                        if event.key == pygame.K_s:
                            jumpingx2=False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed() == (1, 0, 0) and playerDino.rect.bottom == int(0.9 * height):
                            # (mouse left button, wheel button, mouse right button)
                            playerDino.isJumping = True
                            if pygame.mixer.get_init() != None:
                                jump_sound.play()
                            playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if pygame.mouse.get_pressed() == (0, 0, 1):
                            # (mouse left button, wheel button, mouse right button)
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                    if event.type == pygame.MOUSEBUTTONUP:
                        playerDino.isDucking = False

                    if event.type == pygame.VIDEORESIZE:
                        checkscrsize(event.w, event.h)

                #미세먼지 등장

                if playerDino.score<50:
                    dust_image.set_alpha(dustnum)
                    screen.blit(dust_image,dust_rect)
                    pygame.display.update()
                elif 50<=playerDino.score<100:
                    dustnum=255
                    dust_image.set_alpha(dustnum)
                    screen.blit(dust_image,dust_rect)
                    pygame.display.update()
                elif 100<=playerDino.score<150:
                    dustnum=0
                    dust_image.set_alpha(dustnum)
                    screen.blit(dust_image,dust_rect)
                    pygame.display.update()
                elif 150<=playerDino.score<200:
                    dustnum=255
                    dust_image.set_alpha(dustnum)
                    screen.blit(dust_image,dust_rect)
                    pygame.display.update()
                elif 200<=playerDino.score<250:
                    dustnum=0
                    dust_image.set_alpha(dustnum)
                    screen.blit(dust_image,dust_rect)
                    pygame.display.update()
                elif 250<=playerDino.score<300:
                    dustnum=255
                    dust_image.set_alpha(dustnum)
                    screen.blit(dust_image,dust_rect)
                    pygame.display.update()
                elif 300<=playerDino.score<350:
                    dustnum=0
                    dust_image.set_alpha(dustnum)
                    screen.blit(dust_image,dust_rect)
                    pygame.display.update()
                elif 350<=playerDino.score<400:
                    dustnum=255
                    dust_image.set_alpha(dustnum)
                    screen.blit(dust_image,dust_rect)
                    pygame.display.update()
                elif 400<=playerDino.score<450:
                    dustnum=0
                    dust_image.set_alpha(dustnum)
                    screen.blit(dust_image,dust_rect)
                    pygame.display.update()
                else:
                    dustnum=255
                    dust_image.set_alpha(dustnum)
                    screen.blit(dust_image,dust_rect)
                    pygame.display.update()

            if not paused:

                if goLeft:
                    if playerDino.rect.left < 0:
                        playerDino.rect.left = 0
                    else:
                        playerDino.rect.left = playerDino.rect.left - gamespeed

                if goRight:
                    if playerDino.rect.right > width:
                        playerDino.rect.right = width
                    else:
                        playerDino.rect.left = playerDino.rect.left + gamespeed
                
                if jumpingx2 :
                    if  playerDino.rect.bottom == int(height * 0.9):
                        playerDino.isJumping = True
                        playerDino.movement[1] = -1 * playerDino.superJumpSpeed

                if item_story1==True:
                    if Sunglass == True:
                        if playerDino.score % 50 ==0:
                            Sunglass=False
                        for s in stones:
                            s.movement[0] = -1 * gamespeed
                            if not playerDino.collision_immune:
                                if pygame.sprite.collide_mask(playerDino, s):
                                    playerDino.collision_immune = True
                                    life -= 1
                                    collision_time = pygame.time.get_ticks()
                                    if life == 0:
                                        playerDino.isDead = True
                                    if pygame.mixer.get_init() is not None:
                                        die_sound.play()
                        for c in cacti:
                            c.movement[0] = -1 * gamespeed
                            if not playerDino.collision_immune:
                                if pygame.sprite.collide_mask(playerDino, c):
                                    playerDino.collision_immune = True
                                    life -= 1
                                    collision_time = pygame.time.get_ticks()
                                    if life == 0:
                                        playerDino.isDead = True
                                    if pygame.mixer.get_init() is not None:
                                        die_sound.play()

                            elif not playerDino.isSuper:
                                immune_time = pygame.time.get_ticks()
                                if immune_time - collision_time > collision_immune_time:
                                    playerDino.collision_immune = False
                        
                        for f in fire_cacti:
                            f.movement[0] = -1 * gamespeed
                            if not playerDino.collision_immune:
                                if pygame.sprite.collide_mask(playerDino, f):
                                    playerDino.collision_immune = True
                                    life -= 1
                                    collision_time = pygame.time.get_ticks()
                                    if life == 0:
                                        playerDino.isDead = True
                                    if pygame.mixer.get_init() is not None:
                                        die_sound.play()

                            elif not playerDino.isSuper:
                                immune_time = pygame.time.get_ticks()
                                if immune_time - collision_time > collision_immune_time:
                                    playerDino.collision_immune = False
                        
                        for p in pteras:
                            p.movement[0] = -1 * gamespeed
                            if not playerDino.collision_immune:
                                if pygame.sprite.collide_mask(playerDino, p):
                                    playerDino.collision_immune = True
                                    life -= 1
                                    collision_time = pygame.time.get_ticks()
                                    if life == 0:
                                        playerDino.isDead = True
                                    if pygame.mixer.get_init() is not None:
                                        die_sound.play()

                            elif not playerDino.isSuper:
                                immune_time = pygame.time.get_ticks()
                                if immune_time - collision_time > collision_immune_time:
                                    playerDino.collision_immune = False


                            elif not playerDino.isSuper:
                                immune_time = pygame.time.get_ticks()
                                if immune_time - collision_time > collision_immune_time:
                                    playerDino.collision_immune = False
                        if not playerDino.isSuper:
                            for s in shield_items:
                                s.movement[0] = -1 * gamespeed
                                if pygame.sprite.collide_mask(playerDino, s):
                                    if pygame.mixer.get_init() is not None:
                                        checkPoint_sound.play()
                                    playerDino.collision_immune = True
                                    playerDino.isSuper = True
                                    s.kill()
                                    item_time = pygame.time.get_ticks()
                                elif s.rect.right < 0:
                                    s.kill()
                    else:
                        for s in stones:
                            if playerDino.score<50:
                                s.image.set_alpha(255)
                            elif 50<=playerDino.score<100:
                                s.image.set_alpha(70)
                            elif 100<=playerDino.score<150:
                                s.image.set_alpha(255)
                            elif 150<=playerDino.score<200:
                                s.image.set_alpha(70)
                            elif 200<=playerDino.score<250:
                                s.image.set_alpha(255)
                            elif 250<=playerDino.score<300:
                                s.image.set_alpha(70)
                            elif 300<=playerDino.score<350:
                                s.image.set_alpha(255)
                            elif 350<=playerDino.score<400:
                                s.image.set_alpha(70)
                            elif 400<=playerDino.score<450:
                                s.image.set_alpha(255)
                            else:
                                s.image.set_alpha(70)
                            
                            s.movement[0] = -1 * gamespeed
                            if not playerDino.collision_immune:
                                if pygame.sprite.collide_mask(playerDino, s):
                                    playerDino.collision_immune = True
                                    life -= 1
                                    collision_time = pygame.time.get_ticks()
                                    if life == 0:
                                        playerDino.isDead = True
                                    if pygame.mixer.get_init() is not None:
                                        die_sound.play()

                        for c in cacti:
                            if playerDino.score<50:
                                c.image.set_alpha(255)
                            elif 50<=playerDino.score<100:
                                c.image.set_alpha(70)
                            elif 100<=playerDino.score<150:
                                c.image.set_alpha(255)
                            elif 150<=playerDino.score<200:
                                c.image.set_alpha(70)
                            elif 200<=playerDino.score<250:
                                c.image.set_alpha(255)
                            elif 250<=playerDino.score<300:
                                c.image.set_alpha(70)
                            elif 300<=playerDino.score<350:
                                c.image.set_alpha(255)
                            elif 350<=playerDino.score<400:
                                c.image.set_alpha(70)
                            elif 400<=playerDino.score<450:
                                c.image.set_alpha(255)
                            else:
                                c.image.set_alpha(70)
                            c.movement[0] = -1 * gamespeed
                            if not playerDino.collision_immune:
                                if pygame.sprite.collide_mask(playerDino, c):
                                    playerDino.collision_immune = True
                                    life -= 1
                                    collision_time = pygame.time.get_ticks()
                                    if life == 0:
                                        playerDino.isDead = True
                                    if pygame.mixer.get_init() is not None:
                                        die_sound.play()

                            elif not playerDino.isSuper:
                                immune_time = pygame.time.get_ticks()
                                if immune_time - collision_time > collision_immune_time:
                                    playerDino.collision_immune = False

                        for f in fire_cacti:
                            if playerDino.score<50:
                                f.image.set_alpha(255)
                            elif 50<=playerDino.score<100:
                                f.image.set_alpha(70)
                            elif 100<=playerDino.score<150:
                                f.image.set_alpha(255)
                            elif 150<=playerDino.score<200:
                                f.image.set_alpha(70)
                            elif 200<=playerDino.score<250:
                                f.image.set_alpha(255)
                            elif 250<=playerDino.score<300:
                                f.image.set_alpha(70)
                            elif 300<=playerDino.score<350:
                                f.image.set_alpha(255)
                            elif 350<=playerDino.score<400:
                                f.image.set_alpha(70)
                            elif 400<=playerDino.score<450:
                                f.image.set_alpha(255)
                            else:
                                f.image.set_alpha(70)
                            f.movement[0] = -1 * gamespeed
                            if not playerDino.collision_immune:
                                if pygame.sprite.collide_mask(playerDino, f):
                                    playerDino.collision_immune = True
                                    life -= 1
                                    collision_time = pygame.time.get_ticks()
                                    if life == 0:
                                        playerDino.isDead = True
                                    if pygame.mixer.get_init() is not None:
                                        die_sound.play()

                            elif not playerDino.isSuper:
                                immune_time = pygame.time.get_ticks()
                                if immune_time - collision_time > collision_immune_time:
                                    playerDino.collision_immune = False

                        for p in pteras:
                            if playerDino.score<50:
                                p.image.set_alpha(255)
                            elif 50<=playerDino.score<100:
                                p.image.set_alpha(70)
                            elif 100<=playerDino.score<150:
                                p.image.set_alpha(255)
                            elif 150<=playerDino.score<200:
                                p.image.set_alpha(70)
                            elif 200<=playerDino.score<250:
                                p.image.set_alpha(255)
                            elif 250<=playerDino.score<300:
                                p.image.set_alpha(70)
                            elif 300<=playerDino.score<350:
                                p.image.set_alpha(255)
                            elif 350<=playerDino.score<400:
                                p.image.set_alpha(70)
                            elif 400<=playerDino.score<450:
                                p.image.set_alpha(255)
                            else:
                                p.image.set_alpha(70)
                            p.movement[0] = -1 * gamespeed
                            if not playerDino.collision_immune:
                                if pygame.sprite.collide_mask(playerDino, p):
                                    playerDino.collision_immune = True
                                    life -= 1
                                    collision_time = pygame.time.get_ticks()
                                    if life == 0:
                                        playerDino.isDead = True
                                    if pygame.mixer.get_init() is not None:
                                        die_sound.play()

                            elif not playerDino.isSuper:
                                immune_time = pygame.time.get_ticks()
                                if immune_time - collision_time > collision_immune_time:
                                    playerDino.collision_immune = False


                            elif not playerDino.isSuper:
                                immune_time = pygame.time.get_ticks()
                                if immune_time - collision_time > collision_immune_time:
                                    playerDino.collision_immune = False

                        if not playerDino.isSuper:
                            for s in shield_items:
                                s.movement[0] = -1 * gamespeed
                                if pygame.sprite.collide_mask(playerDino, s):
                                    if pygame.mixer.get_init() is not None:
                                        checkPoint_sound.play()
                                    playerDino.collision_immune = True
                                    playerDino.isSuper = True
                                    s.kill()
                                    item_time = pygame.time.get_ticks()
                                elif s.rect.right < 0:
                                    s.kill()
                else:
                    for s in stones:
                        if playerDino.score<50:
                            s.image.set_alpha(255)
                        elif 50<=playerDino.score<100:
                            s.image.set_alpha(70)
                        elif 100<=playerDino.score<150:
                            s.image.set_alpha(255)
                        elif 150<=playerDino.score<200:
                            s.image.set_alpha(70)
                        elif 200<=playerDino.score<250:
                            s.image.set_alpha(255)
                        elif 250<=playerDino.score<300:
                            s.image.set_alpha(70)
                        elif 300<=playerDino.score<350:
                            s.image.set_alpha(255)
                        elif 350<=playerDino.score<400:
                            s.image.set_alpha(70)
                        elif 400<=playerDino.score<450:
                            s.image.set_alpha(255)
                        else:
                            s.image.set_alpha(70)
                        
                        s.movement[0] = -1 * gamespeed
                        if not playerDino.collision_immune:
                            if pygame.sprite.collide_mask(playerDino, s):
                                playerDino.collision_immune = True
                                life -= 1
                                collision_time = pygame.time.get_ticks()
                                if life == 0:
                                    playerDino.isDead = True
                                if pygame.mixer.get_init() is not None:
                                    die_sound.play()

                    for c in cacti:
                        if playerDino.score<50:
                            c.image.set_alpha(255)
                        elif 50<=playerDino.score<100:
                            c.image.set_alpha(70)
                        elif 100<=playerDino.score<150:
                            c.image.set_alpha(255)
                        elif 150<=playerDino.score<200:
                            c.image.set_alpha(70)
                        elif 200<=playerDino.score<250:
                            c.image.set_alpha(255)
                        elif 250<=playerDino.score<300:
                            c.image.set_alpha(70)
                        elif 300<=playerDino.score<350:
                            c.image.set_alpha(255)
                        elif 350<=playerDino.score<400:
                            c.image.set_alpha(70)
                        elif 400<=playerDino.score<450:
                            c.image.set_alpha(255)
                        else:
                            c.image.set_alpha(70)
                        c.movement[0] = -1 * gamespeed
                        if not playerDino.collision_immune:
                            if pygame.sprite.collide_mask(playerDino, c):
                                playerDino.collision_immune = True
                                life -= 1
                                collision_time = pygame.time.get_ticks()
                                if life == 0:
                                    playerDino.isDead = True
                                if pygame.mixer.get_init() is not None:
                                    die_sound.play()

                        elif not playerDino.isSuper:
                            immune_time = pygame.time.get_ticks()
                            if immune_time - collision_time > collision_immune_time:
                                playerDino.collision_immune = False

                    for f in fire_cacti:
                        if playerDino.score<50:
                            f.image.set_alpha(255)
                        elif 50<=playerDino.score<100:
                            f.image.set_alpha(70)
                        elif 100<=playerDino.score<150:
                            f.image.set_alpha(255)
                        elif 150<=playerDino.score<200:
                            f.image.set_alpha(70)
                        elif 200<=playerDino.score<250:
                            f.image.set_alpha(255)
                        elif 250<=playerDino.score<300:
                            f.image.set_alpha(70)
                        elif 300<=playerDino.score<350:
                            f.image.set_alpha(255)
                        elif 350<=playerDino.score<400:
                            f.image.set_alpha(70)
                        elif 400<=playerDino.score<450:
                            f.image.set_alpha(255)
                        else:
                            f.image.set_alpha(70)
                        f.movement[0] = -1 * gamespeed
                        if not playerDino.collision_immune:
                            if pygame.sprite.collide_mask(playerDino, f):
                                playerDino.collision_immune = True
                                life -= 1
                                collision_time = pygame.time.get_ticks()
                                if life == 0:
                                    playerDino.isDead = True
                                if pygame.mixer.get_init() is not None:
                                    die_sound.play()

                        elif not playerDino.isSuper:
                            immune_time = pygame.time.get_ticks()
                            if immune_time - collision_time > collision_immune_time:
                                playerDino.collision_immune = False

                    for p in pteras:
                        if playerDino.score<50:
                            p.image.set_alpha(255)
                        elif 50<=playerDino.score<100:
                            p.image.set_alpha(70)
                        elif 100<=playerDino.score<150:
                            p.image.set_alpha(255)
                        elif 150<=playerDino.score<200:
                            p.image.set_alpha(70)
                        elif 200<=playerDino.score<250:
                            p.image.set_alpha(255)
                        elif 250<=playerDino.score<300:
                            p.image.set_alpha(70)
                        elif 300<=playerDino.score<350:
                            p.image.set_alpha(255)
                        elif 350<=playerDino.score<400:
                            p.image.set_alpha(70)
                        elif 400<=playerDino.score<450:
                            p.image.set_alpha(255)
                        else:
                            p.image.set_alpha(70)
                        p.movement[0] = -1 * gamespeed
                        if not playerDino.collision_immune:
                            if pygame.sprite.collide_mask(playerDino, p):
                                playerDino.collision_immune = True
                                life -= 1
                                collision_time = pygame.time.get_ticks()
                                if life == 0:
                                    playerDino.isDead = True
                                if pygame.mixer.get_init() is not None:
                                    die_sound.play()

                        elif not playerDino.isSuper:
                            immune_time = pygame.time.get_ticks()
                            if immune_time - collision_time > collision_immune_time:
                                playerDino.collision_immune = False


                        elif not playerDino.isSuper:
                            immune_time = pygame.time.get_ticks()
                            if immune_time - collision_time > collision_immune_time:
                                playerDino.collision_immune = False

                        if not playerDino.isSuper:
                            for s in shield_items:
                                s.movement[0] = -1 * gamespeed
                                if pygame.sprite.collide_mask(playerDino, s):
                                    if pygame.mixer.get_init() is not None:
                                        checkPoint_sound.play()
                                    playerDino.collision_immune = True
                                    playerDino.isSuper = True
                                    s.kill()
                                    item_time = pygame.time.get_ticks()
                                elif s.rect.right < 0:
                                    s.kill()
                STONE_INTERVAL = 50

                CACTUS_INTERVAL = 50
                PTERA_INTERVAL = 300
                CLOUD_INTERVAL = 300
                SHIELD_INTERVAL = 500
                LIFE_INTERVAL = 1000
                SLOW_INTERVAL = 1000
                HIGHJUMP_INTERVAL = 300
                OBJECT_REFRESH_LINE = width * 0.8
                MAGIC_NUM = 10

                if len(cacti) < 2:
                    if len(cacti) == 0:
                        last_obstacle.empty()
                        last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))
                    else:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))

                if len(fire_cacti) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL * 5) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(fire_Cactus(gamespeed, object_size[0], object_size[1]))

                if len(stones) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(STONE_INTERVAL * 3) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(Stone(gamespeed, object_size[0], object_size[1]))

                if len(pteras) == 0 and random.randrange(PTERA_INTERVAL) == MAGIC_NUM and counter > PTERA_INTERVAL:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE:
                            last_obstacle.empty()
                            last_obstacle.add(Ptera(gamespeed, ptera_size[0], ptera_size[1]))

                if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                    Cloud(width, random.randrange(height / 5, height / 2))



                playerDino.update()
                cacti.update()
                fire_cacti.update()
                pteras.update()
                clouds.update()
                shield_items.update()
                life_items.update()
                # highjump_items.update()
                new_ground.update()
                s_scb.update(playerDino.score)
                heart.update(life)
                slow_items.update()

                stones.update()
                
                if pygame.display.get_surface() != None:
                    new_ground.draw()
                    clouds.draw(screen)
                    s_scb.draw()
                    heart.draw()
                    cacti.draw(screen)
                    stones.draw(screen)
                    fire_cacti.draw(screen)
                    pteras.draw(screen)
                    shield_items.draw(screen)
                    life_items.draw(screen)
                    slow_items.draw(screen)
                    # highjump_items.draw(screen)
                    playerDino.draw()
                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                        resized_screen_centerpos)
                    pygame.display.update()

                    


                clock.tick(FPS)

                if playerDino.isDead:
                    gameOver = True
                    pygame.mixer.music.stop()  # 죽으면 배경음악 멈춤
                    if playerDino.score > high_score:
                        high_score = playerDino.score

                if counter % speed_up_limit_count == speed_up_limit_count - 1:
                    new_ground.speed -= 1
                    gamespeed += 1

                counter = (counter + 1)

                if playerDino.score >= 500:
                    gameClear = True
                    break
                

        if gameQuit:
            break

        while gameClear:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_n:
                            gameplay_story2()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        gameplay_story2()
            break


        while gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            gameOver = False
                            gameQuit = True
                            introscreen()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        gameOver = False
                        gameQuit = True
                        introscreen()

                    if event.type == pygame.VIDEORESIZE:
                        checkscrsize(event.w, event.h)


            if pygame.display.get_surface() != None:
                disp_gameOver_msg(gameover_image)
                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_centerpos)
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()

def gameplay_story2(): # 지진모드
    global item_story2
    #아이템 관련 변수 설정
    Shovel = False #삽
    global resized_screen
    global high_score
    result = db.query_db("select score from user order by score desc;", one=True)
    if result is not None:
        high_score = result['score']
    #    if bgm_on:
    #       pygame.mixer.music.play(-1) # 배경음악 실행
    gamespeed = 4
    startMenu = False
    gameOver = False
    gameClear = False
    gameQuit = False
    life = 5

    paused = False

    playerDino = Dino(dino_size[0], dino_size[1], type=dino_type[type_idx])
    Background, Background_rect = load_image('new_rock_2.png', 800, 400, -1)
    
    new_ground = Ground(-1 * gamespeed)
    s_scb = Story_Scoreboard()
    heart = HeartIndicator(life)
    counter = 0

    cacti = pygame.sprite.Group()
    fire_cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()

    stones = pygame.sprite.Group()
    holes = pygame.sprite.Group()

    last_obstacle = pygame.sprite.Group()

    Stone.containers = stones
    Hole.containers = holes

    Cactus.containers = cacti
    fire_Cactus.containers = fire_cacti
    Ptera.containers = pteras
    Cloud.containers = clouds

    # BUTTON IMG LOAD
    # retbutton_image, retbutton_rect = load_image('replay_button.png', 70, 62, -1)
    
    gameover_image, gameover_rect = load_image('game_over.png', 380, 22, -1)
    clear_image, clear_rect = load_image('intro_bg.png', width, height, -1)

    # 방향키 구현
    goLeft=False
    goRight=False
    jumpingx2=False

    while not gameQuit:
        while startMenu:
            pass
        while not gameOver and not gameClear:
            
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True


            else:
                screen.fill(background_col)
                screen.blit(Background, Background_rect)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # 종료
                        gameQuit = True
                        gameOver = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:  # 스페이스 누르는 시점에 공룡이 땅에 닿아있으면 점프한다.
                            if playerDino.rect.bottom == int(0.9 * height):
                                playerDino.isJumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if event.key == pygame.K_DOWN:  # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                        if event.key == pygame.K_LEFT:
                            # print("left")
                            goLeft=True

                        if event.key == pygame.K_RIGHT:
                            # print("right")
                            goRight=True

                        # jumping x2 ( press key s)
                        if event.key == pygame.K_s:
                            jumpingx2=True

                        if event.key == pygame.K_d:
                            if item_story2 == True:
                                Shovel = True
                        
                        if event.key == pygame.K_ESCAPE:
                            paused = not paused
                            paused = pausing()

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            playerDino.isDucking = False

                        # 방향키 추가
                        if event.key == pygame.K_LEFT:
                            goLeft=False

                        if event.key == pygame.K_RIGHT:
                            goRight=False
                        #

                        ## jumgpingx2
                        if event.key == pygame.K_s:
                            jumpingx2 = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed() == (1, 0, 0) and playerDino.rect.bottom == int(0.9 * height):
                            # (mouse left button, wheel button, mouse right button)
                            playerDino.isJumping = True
                            if pygame.mixer.get_init() != None:
                                jump_sound.play()
                            playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if pygame.mouse.get_pressed() == (0, 0, 1):
                            # (mouse left button, wheel button, mouse right button)
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                    if event.type == pygame.MOUSEBUTTONUP:
                        playerDino.isDucking = False

                    if event.type == pygame.VIDEORESIZE:
                        checkscrsize(event.w, event.h)

            if not paused:
                
                if goLeft:
                    if playerDino.rect.left < 0:
                        playerDino.rect.left = 0
                    else:
                        playerDino.rect.left = playerDino.rect.left - gamespeed

                if goRight:
                    if playerDino.rect.right > width:
                        playerDino.rect.right = width
                    else:
                        playerDino.rect.left = playerDino.rect.left + gamespeed

                if jumpingx2 :
                    if  playerDino.rect.bottom == int(height * 0.9):
                        playerDino.isJumping = True
                        playerDino.movement[1] = -1 * playerDino.superJumpSpeed


                for h in holes:
                    h.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, h):
                            if Shovel==True:
                                h.image.set_alpha(0)                      
                            else:
                                playerDino.collision_immune = True
                                life -= 5
                                collision_time = pygame.time.get_ticks()
                                if life <= 0:
                                    playerDino.isDead = True
                                if pygame.mixer.get_init() is not None:
                                    die_sound.play()
                
                for s in stones:
                    s.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, s):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                for c in cacti:
                    c.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, c):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False

                for f in fire_cacti:
                    f.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, f):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False

                for p in pteras:
                    p.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, p):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False


                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False

                HOLE_INTERVAL = 50
                STONE_INTERVAL = 50
                CACTUS_INTERVAL = 50
                PTERA_INTERVAL = 340
                CLOUD_INTERVAL = 300
                OBJECT_REFRESH_LINE = width *0.95 
                MAGIC_NUM = 10

                if len(cacti) < 2:
                    if len(cacti) == 0 and playerDino.score <= 1:
                        last_obstacle.empty()
                        last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))
                    else:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))

                if len(fire_cacti) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL * 5) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(fire_Cactus(gamespeed, object_size[0], object_size[1]))

                if len(stones) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(STONE_INTERVAL) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(Stone(gamespeed, object_size[0], object_size[1]))
                if Shovel ==True:
                    pass
                else:
                    if len(holes) < 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(HOLE_INTERVAL) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Hole(gamespeed, object_size[0], object_size[1]))

                if len(pteras) == 0 and random.randrange(PTERA_INTERVAL) == MAGIC_NUM and counter > PTERA_INTERVAL:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE:
                            last_obstacle.empty()
                            last_obstacle.add(Ptera(gamespeed, ptera_size[0], ptera_size[1]))


                if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                    Cloud(width, random.randrange(height / 5, height / 2))

                playerDino.update()
                cacti.update()
                fire_cacti.update()
                pteras.update()
                clouds.update()
                new_ground.update()
                s_scb.update(playerDino.score)
                heart.update(life)

                stones.update()
                holes.update()

                if pygame.display.get_surface() != None:
                    new_ground.draw()
                    clouds.draw(screen)
                    s_scb.draw()
                    heart.draw()
                    cacti.draw(screen)
                    stones.draw(screen)
                    holes.draw(screen)
                    fire_cacti.draw(screen)
                    pteras.draw(screen)
                    playerDino.draw()
                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                        resized_screen_centerpos)
                    pygame.display.update()
                clock.tick(FPS)

                if playerDino.isDead:
                    gameOver = True
                    # pygame.mixer.music.stop()  # 죽으면 배경음악 멈춤
                    if playerDino.score > high_score:
                        high_score = playerDino.score

                if counter % speed_up_limit_count == speed_up_limit_count - 1:
                    new_ground.speed -= 1
                    gamespeed += 1

                counter = (counter + 1)

                if playerDino.score >= 500:
                    gameClear = True
                    break

        if gameQuit:
            break

        

        while gameClear:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_n:
                            gameplay_story3()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        gameplay_story3()
            break

        while gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            gameOver = False
                            gameQuit = True
                            introscreen()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        gameOver = False
                        gameQuit = True
                        introscreen()

                    if event.type == pygame.VIDEORESIZE:
                        checkscrsize(event.w, event.h)


            if pygame.display.get_surface() != None:
                disp_gameOver_msg(gameover_image)
                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_centerpos)
                pygame.display.update()
            clock.tick(FPS)


    pygame.quit()
    quit()

def gameplay_story3():
    global resized_screen
    global high_score
    global item_story3
    result = db.query_db("select score from user order by score desc;", one=True)
    if result is not None:
        high_score = result['score']
    #    if bgm_on:
    #       pygame.mixer.music.play(-1) # 배경음악 실행
    gamespeed = 4
    startMenu = False
    gameOver = False
    gameClear = False
    gameQuit = False
    Umbrella = False
    ###
    life = 5
    ###
    paused = False

    playerDino = Dino(dino_size[0], dino_size[1], type=dino_type[type_idx])

    new_ground = Ground(-1 * gamespeed)
    s_scb = Story_Scoreboard()
    heart = HeartIndicator(life)
    counter = 0

    cacti = pygame.sprite.Group()
    fire_cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    # add stones
    stones = pygame.sprite.Group()

    last_obstacle = pygame.sprite.Group()
    shield_items = pygame.sprite.Group()
    life_items = pygame.sprite.Group()
    slow_items = pygame.sprite.Group()
    # highjump_items = pygame.sprite.Group()

    Stone.containers = stones

    Cactus.containers = cacti
    fire_Cactus.containers = fire_cacti
    Ptera.containers = pteras
    Cloud.containers = clouds
    ShieldItem.containers = shield_items
    LifeItem.containers = life_items
    SlowItem.containers = slow_items
    # HighJumpItem.containers = highjump_items

    # BUTTON IMG LOAD
    # retbutton_image, retbutton_rect = load_image('replay_button.png', 70, 62, -1)
    gameover_image, gameover_rect = load_image('game_over.png', 380, 22, -1)

    #1. 미사일 발사.
    space_go=False
    m_list=[]
    a_list=[]
    bk=0

    #익룡이 격추되었을때
    isDown=False
    boomCount=0

    #방향키 구현
    goLeft=False
    goRight=False

    pm_list = []
    pm_pattern1_count=0
    #2단 점프
    jumpingx2=False

    back_image, back_rect = load_image("story3_background.png", 800, 400, -1)
    


    while not gameQuit:
        while startMenu:
            pass
        while not gameOver and not gameClear:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True


            else:
                screen.fill(background_col)
                screen.blit(back_image, back_rect)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # 종료
                        gameQuit = True
                        gameOver = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:  # 스페이스 누르는 시점에 공룡이 땅에 닿아있으면 점프한다.
                            if playerDino.rect.bottom == int(0.9 * height):
                                playerDino.isJumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if event.key == pygame.K_DOWN:  # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True
                        
                        if event.key == pygame.K_LEFT:
                            goLeft=True
                        
                        if event.key == pygame.K_RIGHT:
                            goRight=True

                        if event.key == pygame.K_ESCAPE:
                            paused = not paused
                            paused = pausing()

                        if event.key == pygame.K_s:
                            jumpingx2=True
                        
                        if event.key == pygame.K_a:
                            space_go=True
                            bk=0

                        if event.key == pygame.K_d:
                            if item_story3 == True:
                                Umbrella = True

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            playerDino.isDucking = False

                        if event.key == pygame.K_a:
                            space_go=False

                        if event.key == pygame.K_LEFT:
                            goLeft=False
                        
                        if event.key == pygame.K_RIGHT:
                            goRight=False

                        if event.key == pygame.K_s:
                            jumpingx2=False
                        

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed() == (1, 0, 0) and playerDino.rect.bottom == int(0.9 * height):
                            # (mouse left button, wheel button, mouse right button)
                            playerDino.isJumping = True
                            if pygame.mixer.get_init() != None:
                                jump_sound.play()
                            playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if pygame.mouse.get_pressed() == (0, 0, 1):
                            # (mouse left button, wheel button, mouse right button)
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                    if event.type == pygame.MOUSEBUTTONUP:
                        playerDino.isDucking = False

                    if event.type == pygame.VIDEORESIZE:
                        checkscrsize(event.w, event.h)

            if not paused:

                if goLeft:
                    if playerDino.rect.left < 0:
                        playerDino.rect.left = 0
                    else:
                        playerDino.rect.left = playerDino.rect.left - gamespeed

                if goRight:
                    if playerDino.rect.right > width:
                        playerDino.rect.right = width
                    else:
                        playerDino.rect.left = playerDino.rect.left + gamespeed

                if (space_go==True) and (int(bk%100)==0):
                    # print(bk)
                    mm=obj()

                    # 디노의 종류에 따라 다른 총알이 나가도록 합니다.
                    if playerDino.type == 'RED':
                        mm.put_img("./sprites/black_bullet.png")
                        mm.change_size(15,15)
                    elif playerDino.type == 'YELLOW':
                        mm.put_img("./sprites/blue_bullet.png")
                        mm.change_size(15,15)
                    elif playerDino.type == 'ORANGE':
                        mm.put_img("./sprites/blue_bullet.png")
                        mm.change_size(15,15)
                    elif playerDino.type == 'PURPLE':
                        mm.put_img("./sprites/pink_bullet.png")
                        mm.change_size(15,15)
                    elif playerDino.type == 'PINK':
                        mm.put_img("./sprites/heart_bullet.png")
                        mm.change_size(15,15)
                    else:                    
                        mm.put_img("./sprites/red_bullet.png")
                        mm.change_size(15,15)
                    # 
                    
                    if playerDino.isDucking ==False:
                        mm.x = round(playerDino.rect.centerx)
                        mm.y = round(playerDino.rect.top*1.035)
                    if playerDino.isDucking ==True:
                        mm.x = round(playerDino.rect.centerx)
                        mm.y = round(playerDino.rect.centery*1.01)
                    mm.move = 15
                    m_list.append(mm)
                bk=bk+1
                d_list=[]

                #미사일 하나씩 꺼내옴
                for i in range(len(m_list)):
                    m=m_list[i]
                    m.x +=m.move
                    if m.x>width:
                        d_list.append(i)

                d_list.reverse()
                for d in d_list:
                    del m_list[d]
                #

                if jumpingx2 :
                    if  playerDino.rect.bottom == int(height * 0.9):
                        playerDino.isJumping = True
                        playerDino.movement[1] = -1 * playerDino.superJumpSpeed

                if goLeft:
                    if playerDino.rect.left < 0:
                        playerDino.rect.left = 0
                    else:
                        playerDino.rect.left = playerDino.rect.left - gamespeed

                if goRight:
                    if playerDino.rect.right > width:
                        playerDino.rect.right = width
                    else:
                        playerDino.rect.left = playerDino.rect.left + gamespeed
               
                if  (int(pm_pattern1_count % 20) == 0):
                    pm=obj()
                    pm.put_img("./sprites/water_drop.png")
                    pm.change_size(40,40)
                    pm.x = random.randrange(40, 800-40)
                    pm.y = 10
                    pm.move = 3
                    pm_list.append(pm)
                pm_pattern1_count += 1
                pd_list = []

                for i in range(len(pm_list)):
                    pm=pm_list[i]
                    pm.y +=pm.move
                    if pm.y>height or pm.x < 0:
                        pd_list.append(i)

                pd_list.reverse()
                for d in pd_list:
                    del pm_list[d]
                #


                for s in stones:
                    s.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, s):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                for c in cacti:
                    c.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, c):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False

                for f in fire_cacti:
                    f.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, f):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False
                
                for p in pteras:
                    p.movement[0] = -1 * gamespeed

                    # 7. 익룡이 미사일에 맞으면 익룡과 미사일 모두 사라집니다.

                    if (len(m_list)==0):
                        pass
                    else:
                        if (m.x>=p.rect.left)and(m.x<=p.rect.right)and(m.y>p.rect.top)and(m.y<p.rect.bottom):
                            print("격추 성공")
                            isDown=True
                            boom=obj()
                            boom.put_img("./sprites/boom.png")
                            boom.change_size(200,100)
                            boom.x=p.rect.centerx-round(p.rect.width)*2.5
                            boom.y=p.rect.centery-round(p.rect.height)*1.5
                            playerDino.score+=30
                            p.kill()
                            # 여기만 바꿈
                            m_list.remove(m)
                            #
                    #

                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, p):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False


                if not playerDino.isSuper:
                    for s in shield_items:
                        s.movement[0] = -1 * gamespeed
                        if pygame.sprite.collide_mask(playerDino, s):
                            if pygame.mixer.get_init() is not None:
                                checkPoint_sound.play()
                            playerDino.collision_immune = True
                            playerDino.isSuper = True
                            s.kill()
                            item_time = pygame.time.get_ticks()
                        elif s.rect.right < 0:
                            s.kill()

                STONE_INTERVAL = 50

                CACTUS_INTERVAL = 50
                PTERA_INTERVAL = 300
                CLOUD_INTERVAL = 300
                SHIELD_INTERVAL = 500
                LIFE_INTERVAL = 1000
                SLOW_INTERVAL = 1000
                HIGHJUMP_INTERVAL = 300
                OBJECT_REFRESH_LINE = width * 0.8
                MAGIC_NUM = 10

                if Umbrella == True:
                    um=obj()
                    um.put_img("./sprites/umbrella_item.png")
                    um.change_size(70,70)
                    um.x = (playerDino.rect.left+playerDino.rect.right)/2-40
                    um.y = playerDino.rect.bottom - 70
                    um.move = 5

                    if (len(pm_list)==0):
                        pass
                    else:
                        # print("x: ",pm.x,"y: ",pm.y)
                        for pm in pm_list:
                            if (pm.y>=um.y)and(pm.x<=um.x+35)and(pm.x>=um.x-35):
                                pm.img.set_alpha(0)


                else:
                    if (len(pm_list)==0):
                        pass
                    else:
                        # print("x: ",pm.x,"y: ",pm.y)
                        for pm in pm_list:
                            if (pm.x>=playerDino.rect.left)and(pm.x<=playerDino.rect.right)and(pm.y>playerDino.rect.top)and(pm.y<playerDino.rect.bottom):
                                print("공격에 맞음.")
                                # if pygame.sprite.collide_mask(playerDino, pm):
                                playerDino.collision_immune = True
                                life -= 1
                                collision_time = pygame.time.get_ticks()
                                if life == 0:
                                    playerDino.isDead = True
                                pm_list.remove(pm)

                if len(cacti) < 2:
                    if len(cacti) == 0 and playerDino.score <= 1:
                        last_obstacle.empty()
                        last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))
                    else:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))

                if len(fire_cacti) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL * 5) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(fire_Cactus(gamespeed, object_size[0], object_size[1]))

                if len(stones) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(STONE_INTERVAL * 3) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(Stone(gamespeed, object_size[0], object_size[1]))

                

                if len(pteras) == 0 and random.randrange(PTERA_INTERVAL) == MAGIC_NUM and counter > PTERA_INTERVAL:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE:
                            last_obstacle.empty()
                            last_obstacle.add(Ptera(gamespeed, ptera_size[0], ptera_size[1]))

                if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                    Cloud(width, random.randrange(height / 5, height / 2))

                playerDino.update()
                cacti.update()
                fire_cacti.update()
                pteras.update()
                clouds.update()
                shield_items.update()
                life_items.update()
                # highjump_items.update()
                new_ground.update()
                s_scb.update(playerDino.score)
                heart.update(life)
                slow_items.update()

                stones.update()
                for a in a_list:
                    a.show()



                if pygame.display.get_surface() != None:
                    new_ground.draw()
                    clouds.draw(screen)
                    s_scb.draw()
                    heart.draw()
                    cacti.draw(screen)
                    stones.draw(screen)
                    fire_cacti.draw(screen)
                    pteras.draw(screen)
                    shield_items.draw(screen)
                    life_items.draw(screen)
                    slow_items.draw(screen)
                    # highjump_items.draw(screen)

                    for pm in pm_list:
                        pm.show()

                    if Umbrella == True:
                        um.show()

                    playerDino.draw()
                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                        resized_screen_centerpos)
                    pygame.display.update()
                clock.tick(FPS)


                if playerDino.isDead:
                    gameOver = True
                    pygame.mixer.music.stop()  # 죽으면 배경음악 멈춤
                    if playerDino.score > high_score:
                        high_score = playerDino.score

                if counter % speed_up_limit_count == speed_up_limit_count - 1:
                    new_ground.speed -= 1
                    gamespeed += 1

                counter = (counter + 1)

                if playerDino.score >= 50:
                    gameClear = True
                    break

        if gameQuit:
            break
        
        while gameClear:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_n:
                            gameplay_story4()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        gameplay_story4()
            break

        while gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            gameOver = False
                            gameQuit = True
                            introscreen()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        gameOver = False
                        gameQuit = True
                        introscreen()

                    if event.type == pygame.VIDEORESIZE:
                        checkscrsize(event.w, event.h)


            if pygame.display.get_surface() != None:
                disp_gameOver_msg(gameover_image)
                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_centerpos)
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()


def gameplay_story4():
    global resized_screen
    global high_score
    global item_story4
    result = db.query_db("select score from user order by score desc;", one=True)
    if result is not None:
        high_score = result['score']
    #    if bgm_on:
    #       pygame.mixer.music.play(-1) # 배경음악 실행
    gamespeed = 4
    startMenu = False
    gameOver = False
    gameClear = False
    gameQuit = False
    Maskplus = False
    ###
    life = 5
    ###
    paused = False

    playerDino = Dino(dino_size[0], dino_size[1], type=dino_type[type_idx])

    new_ground = Ground(-1 * gamespeed)
    s_scb = Story_Scoreboard()
    heart = HeartIndicator(life)
    m_time = Mask_time()
    counter = 0

    cacti = pygame.sprite.Group()
    fire_cacti = pygame.sprite.Group()
    pteras = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    # add stones
    stones = pygame.sprite.Group()
    mask_items = pygame.sprite.Group()

    last_obstacle = pygame.sprite.Group()
    shield_items = pygame.sprite.Group()
    life_items = pygame.sprite.Group()
    slow_items = pygame.sprite.Group()
    # highjump_items = pygame.sprite.Group()

    Stone.containers = stones

    Cactus.containers = cacti
    fire_Cactus.containers = fire_cacti
    Ptera.containers = pteras
    Cloud.containers = clouds
    ShieldItem.containers = shield_items
    LifeItem.containers = life_items
    SlowItem.containers = slow_items
    Mask_item.containers = mask_items
    # HighJumpItem.containers = highjump_items

    # BUTTON IMG LOAD
    # retbutton_image, retbutton_rect = load_image('replay_button.png', 70, 62, -1)
    gameover_image, gameover_rect = load_image('game_over.png', 380, 22, -1)

    #1. 미사일 발사.
    space_go=False
    m_list=[]
    a_list=[]
    bk=0

    #익룡이 격추되었을때
    isDown=False
    boomCount=0

    #방향키 구현
    goLeft=False
    goRight=False

    pm_list = []
    pm_pattern1_count=0
    #2단 점프
    jumpingx2=False

    back_image, back_rect = load_image("story3_background.png", 800, 400, -1)
    


    while not gameQuit:
        while startMenu:
            pass
        while not gameOver and playerDino.score <= 50:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True


            else:
                screen.fill(background_col)
                screen.blit(back_image, back_rect)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:  # 종료
                        gameQuit = True
                        gameOver = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:  # 스페이스 누르는 시점에 공룡이 땅에 닿아있으면 점프한다.
                            if playerDino.rect.bottom == int(0.9 * height):
                                playerDino.isJumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if event.key == pygame.K_DOWN:  # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True
                        
                        if event.key == pygame.K_LEFT:
                            goLeft=True
                        
                        if event.key == pygame.K_RIGHT:
                            goRight=True

                        if event.key == pygame.K_ESCAPE:
                            paused = not paused
                            paused = pausing()

                        if event.key == pygame.K_s:
                            jumpingx2=True
                        
                        if event.key == pygame.K_a:
                            space_go=True
                            bk=0

                        if event.key == pygame.K_d:
                            if item_story4 == True:
                                Maskplus = True

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            playerDino.isDucking = False

                        if event.key == pygame.K_a:
                            space_go=False

                        if event.key == pygame.K_LEFT:
                            goLeft=False
                        
                        if event.key == pygame.K_RIGHT:
                            goRight=False

                        if event.key == pygame.K_s:
                            jumpingx2=False
                        

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed() == (1, 0, 0) and playerDino.rect.bottom == int(0.9 * height):
                            # (mouse left button, wheel button, mouse right button)
                            playerDino.isJumping = True
                            if pygame.mixer.get_init() != None:
                                jump_sound.play()
                            playerDino.movement[1] = -1 * playerDino.jumpSpeed

                        if pygame.mouse.get_pressed() == (0, 0, 1):
                            # (mouse left button, wheel button, mouse right button)
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                    if event.type == pygame.MOUSEBUTTONUP:
                        playerDino.isDucking = False

                    if event.type == pygame.VIDEORESIZE:
                        checkscrsize(event.w, event.h)

            if not paused:

                if goLeft:
                    if playerDino.rect.left < 0:
                        playerDino.rect.left = 0
                    else:
                        playerDino.rect.left = playerDino.rect.left - gamespeed

                if goRight:
                    if playerDino.rect.right > width:
                        playerDino.rect.right = width
                    else:
                        playerDino.rect.left = playerDino.rect.left + gamespeed

                if (space_go==True) and (int(bk%100)==0):
                    # print(bk)
                    mm=obj()

                    # 디노의 종류에 따라 다른 총알이 나가도록 합니다.
                    if playerDino.type == 'RED':
                        mm.put_img("./sprites/black_bullet.png")
                        mm.change_size(15,15)
                    elif playerDino.type == 'YELLOW':
                        mm.put_img("./sprites/blue_bullet.png")
                        mm.change_size(15,15)
                    elif playerDino.type == 'ORANGE':
                        mm.put_img("./sprites/blue_bullet.png")
                        mm.change_size(15,15)
                    elif playerDino.type == 'PURPLE':
                        mm.put_img("./sprites/pink_bullet.png")
                        mm.change_size(15,15)
                    elif playerDino.type == 'PINK':
                        mm.put_img("./sprites/heart_bullet.png")
                        mm.change_size(15,15)
                    else:                    
                        mm.put_img("./sprites/red_bullet.png")
                        mm.change_size(15,15)
                    # 
                    
                    if playerDino.isDucking ==False:
                        mm.x = round(playerDino.rect.centerx)
                        mm.y = round(playerDino.rect.top*1.035)
                    if playerDino.isDucking ==True:
                        mm.x = round(playerDino.rect.centerx)
                        mm.y = round(playerDino.rect.centery*1.01)
                    mm.move = 15
                    m_list.append(mm)
                bk=bk+1
                d_list=[]

                #미사일 하나씩 꺼내옴
                for i in range(len(m_list)):
                    m=m_list[i]
                    m.x +=m.move
                    if m.x>width:
                        d_list.append(i)

                d_list.reverse()
                for d in d_list:
                    del m_list[d]
                #

                if jumpingx2 :
                    if  playerDino.rect.bottom == int(height * 0.9):
                        playerDino.isJumping = True
                        playerDino.movement[1] = -1 * playerDino.superJumpSpeed

                if goLeft:
                    if playerDino.rect.left < 0:
                        playerDino.rect.left = 0
                    else:
                        playerDino.rect.left = playerDino.rect.left - gamespeed

                if goRight:
                    if playerDino.rect.right > width:
                        playerDino.rect.right = width
                    else:
                        playerDino.rect.left = playerDino.rect.left + gamespeed
               


                for s in stones:
                    s.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, s):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                for c in cacti:
                    c.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, c):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False

                for f in fire_cacti:
                    f.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, f):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False
                
                
                for m in mask_items:
                    m.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, m):
                            playerDino.collision_immune = True
                            collision_time = pygame.time.get_ticks()
                            playerDino.score2 = 0
                            m.image.set_alpha(0)
                            
                            if pygame.mixer.get_init() is not None:
                                checkPoint_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False

                for p in pteras:
                    p.movement[0] = -1 * gamespeed

                    # 7. 익룡이 미사일에 맞으면 익룡과 미사일 모두 사라집니다.

                    if (len(m_list)==0):
                        pass
                    else:
                        if (m.x>=p.rect.left)and(m.x<=p.rect.right)and(m.y>p.rect.top)and(m.y<p.rect.bottom):
                            print("격추 성공")
                            isDown=True
                            boom=obj()
                            boom.put_img("./sprites/boom.png")
                            boom.change_size(200,100)
                            boom.x=p.rect.centerx-round(p.rect.width)*2.5
                            boom.y=p.rect.centery-round(p.rect.height)*1.5
                            playerDino.score+=30
                            p.kill()
                            # 여기만 바꿈
                            m_list.remove(m)
                            #
                    #

                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, p):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False


                if not playerDino.isSuper:
                    for s in shield_items:
                        s.movement[0] = -1 * gamespeed
                        if pygame.sprite.collide_mask(playerDino, s):
                            if pygame.mixer.get_init() is not None:
                                checkPoint_sound.play()
                            playerDino.collision_immune = True
                            playerDino.isSuper = True
                            s.kill()
                            item_time = pygame.time.get_ticks()
                        elif s.rect.right < 0:
                            s.kill()

                STONE_INTERVAL = 50

                CACTUS_INTERVAL = 50
                MASK_INTERVAL = 50
                PTERA_INTERVAL = 300
                CLOUD_INTERVAL = 300
                SHIELD_INTERVAL = 500
                LIFE_INTERVAL = 1000
                SLOW_INTERVAL = 1000
                HIGHJUMP_INTERVAL = 300
                OBJECT_REFRESH_LINE = width * 0.8
                MAGIC_NUM = 10

                
                if Maskplus == True: 
                    playerDino.score2 = 0
                    Maskplus = False


                if (len(pm_list)==0):
                    pass
                else:
                    # print("x: ",pm.x,"y: ",pm.y)
                    for pm in pm_list:
                        if (pm.x>=playerDino.rect.left)and(pm.x<=playerDino.rect.right)and(pm.y>playerDino.rect.top)and(pm.y<playerDino.rect.bottom):
                            print("공격에 맞음.")
                            # if pygame.sprite.collide_mask(playerDino, pm):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            pm_list.remove(pm)

                if len(cacti) < 2:
                    if len(cacti) == 0 and playerDino.score <= 1:
                        last_obstacle.empty()
                        last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))
                    else:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))

                if len(fire_cacti) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL * 5) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(fire_Cactus(gamespeed, object_size[0], object_size[1]))

                if len(stones) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(STONE_INTERVAL * 3) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(Stone(gamespeed, object_size[0], object_size[1]))

                
                if len(mask_items) < 2:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(MASK_INTERVAL) == MAGIC_NUM:
                            last_obstacle.empty()
                            last_obstacle.add(Mask_item(gamespeed, object_size[0], object_size[1]))


                if len(pteras) == 0 and random.randrange(PTERA_INTERVAL) == MAGIC_NUM and counter > PTERA_INTERVAL:
                    for l in last_obstacle:
                        if l.rect.right < OBJECT_REFRESH_LINE:
                            last_obstacle.empty()
                            last_obstacle.add(Ptera(gamespeed, ptera_size[0], ptera_size[1]))

                if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                    Cloud(width, random.randrange(height / 5, height / 2))

                playerDino.update()
                cacti.update()
                fire_cacti.update()
                mask_items.update()
                m_time.update(playerDino.score2)
                pteras.update()
                clouds.update()
                shield_items.update()
                life_items.update()
                new_ground.update()
                s_scb.update(playerDino.score)
                heart.update(life)
                slow_items.update()

                stones.update()
                for a in a_list:
                    a.show()



                if pygame.display.get_surface() != None:
                    new_ground.draw()
                    clouds.draw(screen)
                    s_scb.draw()
                    heart.draw()
                    cacti.draw(screen)
                    stones.draw(screen)
                    fire_cacti.draw(screen)
                    mask_items.draw(screen)
                    m_time.draw()
                    pteras.draw(screen)
                    shield_items.draw(screen)
                    life_items.draw(screen)
                    slow_items.draw(screen)
                    # highjump_items.draw(screen)

                    for pm in pm_list:
                        pm.show()


                    playerDino.draw()
                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                        resized_screen_centerpos)
                    pygame.display.update()
                clock.tick(FPS)

                
                if playerDino.score2 == 100:
                    playerDino.isDead = True

                if playerDino.isDead:
                    gameOver = True
                    pygame.mixer.music.stop()  # 죽으면 배경음악 멈춤
                    if playerDino.score > high_score:
                        high_score = playerDino.score

                if counter % speed_up_limit_count == speed_up_limit_count - 1:
                    new_ground.speed -= 1
                    gamespeed += 1

                counter = (counter + 1)

                if playerDino.score >= 50:
                    gameClear = True
                    break


        if gameQuit:
            break
        
        while gameClear:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_n:
                            gameplay_story5()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        gameplay_story5()
            break

        while gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False

            for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            gameOver = False
                            gameQuit = True
                            introscreen()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        gameOver = False
                        gameQuit = True
                        introscreen()

                    if event.type == pygame.VIDEORESIZE:
                        checkscrsize(event.w, event.h)


            if pygame.display.get_surface() != None:
                disp_gameOver_msg(gameover_image)
                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_centerpos)
                pygame.display.update()
            clock.tick(FPS)


    pygame.quit()
    quit()




def gameplay_story5():
    global resized_screen
    global high_score
    global item_story1
    global item_story2
    global item_story3
    global item_story4

    result = db.query_db("select score from user order by score desc;", one=True)
    if result is not None:
        high_score = result['score']
    
    dust_image, dust_rect = load_image('dust.png',800,400,-1)
    Background, Background_rect = load_image('new_rock_2.png', 800, 400, -1)

    dustnum=0
    dust_image.set_alpha(dustnum)

    gamespeed = 4
    startMenu = False
    gameOver = False
    gameQuit = False
    Umbrella = False
    Maskplus = False
    Itemtime = False

    life = 5
    paused = False
    playerDino = Dino(dino_size[0], dino_size[1], type = dino_type[type_idx])
    new_ground = Ground(-1 * gamespeed)
    scb = Scoreboard()
    heart = HeartIndicator(life)
    boss = boss_heart()
    m_time = Mask_time()
    counter = 0

    cacti = pygame.sprite.Group()
    fire_cacti = pygame.sprite.Group()
    clouds = pygame.sprite.Group()
    last_obstacle = pygame.sprite.Group()
    holes = pygame.sprite.Group()
    mask_items = pygame.sprite.Group()

    Cactus.containers = cacti
    Hole.containers = holes
    fire_Cactus.containers = fire_cacti
    Cloud.containers = clouds
    Mask_item.containers = mask_items

    gameover_image, gameover_rect = load_image('game_over.png', 380, 22, -1)
    
    # 1. 미사일 발사.
    space_go=False
    m_list=[]
    bk=0
    # 익룡이 격추되었을때
    isDown=False
    boomCount=0

    # 방향키 구현
    goLeft=False
    goRight=False

    # 보스몬스터 변수설정
    isHumanTime=False
    isHumanAlive=True
    human=Human()
    pm_list = [] # 보스의 총알 개수
    rm_list = []
    pm_pattern0_count = 0 # 패턴 0 시간
    pm_pattern1_count = 0 # 패턴 1 시간
    pm_pattern2_count = 0 # 패턴 2 시간
    pm_pattern3_count = 0 # 패턴 3 시간
    human_appearance_score = 100

    jumpingx2 = False

    while not gameQuit:
        while startMenu:
            pass
        while not gameOver:

            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = True
            else:
                screen.blit(Background, Background_rect)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = True

                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE or event.key == pygame.K_UP:  # 스페이스 누르는 시점에 공룡이 땅에 닿아있으면 점프한다.
                            if playerDino.rect.bottom == int(0.9 * height):
                                playerDino.isJumping = True
                                if pygame.mixer.get_init() != None:
                                    jump_sound.play()
                                playerDino.movement[1] = -1 * playerDino.jumpSpeed
                        if event.key == pygame.K_DOWN:  # 아래방향키를 누르는 시점에 공룡이 점프중이지 않으면 숙인다.
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True
                        if event.key == pygame.K_LEFT:
                            goLeft=True
                        if event.key == pygame.K_RIGHT:
                            goRight=True
                        if event.key == pygame.K_ESCAPE:
                            paused = not paused
                            paused = pausing()
                        if event.key == pygame.K_s:
                            jumpingx2=True
                        if event.key == pygame.K_a:
                            space_go=True
                            bk=0
                        if event.key == pygame.K_d:
                            Itemtime=True

                    if event.type == pygame.KEYUP:
                        if event.key == pygame.K_DOWN:
                            playerDino.isDucking = False
                        if event.key == pygame.K_a:
                            space_go = False
                        if event.key == pygame.K_LEFT:
                            goLeft=False
                        if event.key == pygame.K_RIGHT:
                            goRight=False
                        if event.key == pygame.K_s:
                            jumpingx2 = False

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if pygame.mouse.get_pressed() == (1, 0, 0) and playerDino.rect.bottom == int(0.9 * height):
                            # (mouse left button, wheel button, mouse right button)
                            playerDino.isJumping = True
                            if pygame.mixer.get_init() != None:
                                jump_sound.play()
                            playerDino.movement[1] = -1 * playerDino.jumpSpeed
                        if pygame.mouse.get_pressed() == (0, 0, 1):
                            # (mouse left button, wheel button, mouse right button)
                            if not (playerDino.isJumping and playerDino.isDead):
                                playerDino.isDucking = True

                    if event.type == pygame.MOUSEBUTTONUP:
                        playerDino.isDucking = False

                    if event.type == pygame.VIDEORESIZE:
                        checkscrsize(event.w, event.h)

            if not paused:
                if goLeft:
                    if playerDino.rect.left < 0:
                        playerDino.rect.left = 0
                    else:
                        playerDino.rect.left = playerDino.rect.left - gamespeed
                if goRight:
                    if playerDino.rect.right > width:
                        playerDino.rect.right = width
                    else:
                        playerDino.rect.left = playerDino.rect.left + gamespeed

                #### space_go가 True이고, 일정 시간이 지나면, 미사일을 만들고, 이를 미사일 배열에 넣습니다.
                if (space_go==True) and (int(bk%100)==0):
                    mm=obj()

                    if playerDino.type == 'RED':
                        mm.put_img("./sprites/black_bullet.png")
                        mm.change_size(15,15)
                    elif playerDino.type == 'YELLOW':
                        mm.put_img("./sprites/blue_bullet.png")
                        mm.change_size(15,15)
                    elif playerDino.type == 'ORANGE':
                        mm.put_img("./sprites/blue_bullet.png")
                        mm.change_size(15,15)
                    elif playerDino.type == 'PURPLE':
                        mm.put_img("./sprites/pink_bullet.png")
                        mm.change_size(15,15)
                    elif playerDino.type == 'PINK':
                        mm.put_img("./sprites/heart_bullet.png")
                        mm.change_size(15,15)
                    else:                    
                        mm.put_img("./sprites/red_bullet.png")
                        mm.change_size(15,15)
                    
                    if playerDino.isDucking ==False:
                        mm.x = round(playerDino.rect.centerx)
                        mm.y = round(playerDino.rect.top*1.035)
                    if playerDino.isDucking ==True:
                        mm.x = round(playerDino.rect.centerx)
                        mm.y = round(playerDino.rect.centery*1.01)
                    mm.move = 15
                    m_list.append(mm)
                bk = bk + 1
                d_list = []

                print(playerDino.score2)
                #### 다이노의 미사일 하나씩 꺼내옴
                for i in range(len(m_list)):
                    m = m_list[i]
                    m.x += m.move
                    if m.x > width:
                        d_list.append(i)
                d_list.reverse()
                for d in d_list:
                    del m_list[d]

                if jumpingx2 :
                    if  playerDino.rect.bottom == int(height * 0.9):
                        playerDino.isJumping = True
                        playerDino.movement[1] = -1 * playerDino.superJumpSpeed


                #### 보스 몬스터 패턴 0 - 미세먼지 모드
                if (isHumanTime) and (human.pattern_idx == 0):          
                    # 1. 배경 이미지 처리
                    # if (playerDino.score%100) < 50:
                    #     dust_image.set_alpha(dustnum)
                    #     screen.blit(dust_image, dust_rect)
                    #     pygame.display.update()
                    # elif 50 <= (playerDino.score%100) < 100:
                    #     dustnum=255
                    #     dust_image.set_alpha(dustnum)
                    #     screen.blit(dust_image, dust_rect)
                    #     pygame.display.update()

                    # 2. 장애물 이미지 처리 
                    for c in cacti:
                        if (playerDino.score%100) <50:
                            c.image.set_alpha(255)
                        elif 50<=(playerDino.score%100) < 100:
                            c.image.set_alpha(30)
                        c.movement[0] = -1 * gamespeed

                    for f in fire_cacti:
                        if (playerDino.score%100) <50:
                            c.image.set_alpha(255)
                        elif 50<=(playerDino.score%100) < 100:
                            f.image.set_alpha(30)
                        f.movement[0] = -1 * gamespeed
                    
                    # 3. 보스의 공격
                    if (int(pm_pattern0_count % 80) == 0):
                        pm = obj()
                        pm.put_img("./sprites/pking bullet.png")
                        pm.change_size(15, 15)
                        pm.x = round(human.rect.centerx)
                        pm.y = round(human.rect.bottom - 45)
                        pm.xmove = random.randint(10, 15)
                        pm_list.append(pm)

                pm_pattern0_count += 1
                pd_list = []

                for i in range(len(pm_list)):
                    pm = pm_list[i]
                    pm.x -= pm.xmove
                    if pm.x < 0:
                        pd_list.append(i)

                pd_list.reverse()
                for d in pd_list:
                    del pm_list[d]


                #### 보스 몬스터 패턴 1 - 지진 모드
                if (isHumanTime) and (human.pattern_idx == 1):
                    # 1. 보스의 임의 점프
                    JUMP_MAGIC = 50
                    print(str(human.rect.bottom) + " vs "+str(int(0.9 * height)))
                    if (random.randrange(0, 100) == JUMP_MAGIC):
                        print("구덩이 활성화")
                        if (human.rect.bottom == int(0.9 * height)):
                            
                            human.isJumping = True
                            human.movement[1] = -1 * human.jumpSpeed

                            for l in last_obstacle:
                                if l.rect.right > OBJECT_REFRESH_LINE: l.kill()

                            new_hole_right = human.rect.left - width
                            last_obstacle.add(Hole(gamespeed, object_size[0], object_size[1], new_hole_right))

                    
                    # 3. 보스의 공격

                    if (int(pm_pattern1_count % 80) == 0):
                        pm=obj()
                        pm.put_img("./sprites/pking bullet.png")
                        pm.change_size(15,15)
                        pm.x = round(human.rect.centerx)
                        pm.y = round(human.rect.bottom - 45)
                        pm.xmove = random.randint(10, 15)
                        pm_list.append(pm)
                    
                pm_pattern1_count += 1
                pd_list = []

                for i in range(len(pm_list)):
                    pm=pm_list[i]
                    pm.x -= pm.move
                    if pm.x < 0:
                        pd_list.append(i)

                pd_list.reverse()
                for d in pd_list:
                    del pm_list[d]

                #### 보스 몬스터 패턴 2 - 산성비 모드
                if (isHumanTime) and (human.pattern_idx == 2):
                    
                    # 1. 배경 이미지 처리
                    # if (playerDino.score%100) < 50:
                    #     dust_image.set_alpha(dustnum)
                    #     screen.blit(dust_image, dust_rect)
                    #     pygame.display.update()
                    # elif 50 <= (playerDino.score%100) < 100:
                    #     dustnum=255
                    #     dust_image.set_alpha(dustnum)
                    #     screen.blit(dust_image, dust_rect)
                    #     pygame.display.update()
                    
                    
                    # 3. 보스의 공격

                    if (int(pm_pattern2_count % 80) == 0):
                        pm = obj()
                        pm.put_img("./sprites/pking bullet.png")
                        pm.change_size(15, 15)
                        pm.x = round(human.rect.centerx)
                        pm.y = round(human.rect.bottom - 45)
                        pm.xmove = random.randint(10, 15)
                        pm_list.append(pm)


                    if (int(pm_pattern2_count % 30) == 0):
                        rm=obj()
                        rm.put_img("./sprites/water_drop.png")
                        rm.change_size(40,40)
                        rm.x = random.randrange(playerDino.rect.left, playerDino.rect.right)
                        rm.y = 10
                        rm.move = 3
                        rm_list.append(rm)
                    
                pm_pattern2_count += 1
                pd_list = []
                rd_list = []

                for i in range(len(pm_list)):
                    pm=pm_list[i]
                    pm.y +=pm.move
                    if pm.y>height or pm.x < 0:
                        pd_list.append(i)

                for i in range(len(rm_list)):
                    rm=rm_list[i]
                    rm.y +=rm.move
                    if rm.y>height or rm.x < 0:
                        rd_list.append(i)

                pd_list.reverse()
                for d in pd_list:
                    del pm_list[d]

                rd_list.reverse()
                for r in rd_list:
                    del rm_list[r]



                #### 보스 몬스터 패턴 3 - 바이러스 모드
                if (isHumanTime) and (human.pattern_idx == 3):
                    
                    # 1. 배경 이미지 처리
                    # if (playerDino.score%100) < 50:
                    #     dust_image.set_alpha(dustnum)
                    #     screen.blit(dust_image, dust_rect)
                    #     pygame.display.update()
                    # elif 50 <= (playerDino.score%100) < 100:
                    #     dustnum=255
                    #     dust_image.set_alpha(dustnum)
                    #     screen.blit(dust_image, dust_rect)
                    #     pygame.display.update()
                    
                    
                    # 3. 보스의 공격

                    if (int(pm_pattern3_count % 80) == 0):
                        pm = obj()
                        pm.put_img("./sprites/pking bullet.png")
                        pm.change_size(15, 15)
                        pm.x = round(human.rect.centerx)
                        pm.y = round(human.rect.bottom - 45)
                        pm.xmove = random.randint(10, 15)
                        pm_list.append(pm)
                    
                pm_pattern3_count += 1
                pd_list = []

                for i in range(len(pm_list)):
                    pm=pm_list[i]
                    pm.y +=pm.move
                    if pm.y>height or pm.x < 0:
                        pd_list.append(i)

                pd_list.reverse()
                for d in pd_list:
                    del pm_list[d]                    


                
                #### 장애물 충돌처리
                for c in cacti:
                    c.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, c):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False

                for f in fire_cacti:
                    f.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, f):
                            playerDino.collision_immune = True
                            life -= 1
                            collision_time = pygame.time.get_ticks()
                            if life == 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                    elif not playerDino.isSuper:
                        immune_time = pygame.time.get_ticks()
                        if immune_time - collision_time > collision_immune_time:
                            playerDino.collision_immune = False
                
                for h in holes:
                    h.movement[0] = -1 * gamespeed
                    if not playerDino.collision_immune:
                        if pygame.sprite.collide_mask(playerDino, h):
                            playerDino.collision_immune = True
                            life -= 5
                            collision_time = pygame.time.get_ticks()
                            if life <= 0:
                                playerDino.isDead = True
                            if pygame.mixer.get_init() is not None:
                                die_sound.play()

                if (isHumanTime) and (human.pattern_idx == 3):
                    for ma in mask_items:
                        ma.movement[0] = -1 * gamespeed
                        if not playerDino.collision_immune:
                            if pygame.sprite.collide_mask(playerDino, ma):
                                playerDino.collision_immune = True
                                collision_time = pygame.time.get_ticks()
                                playerDino.score2 = 0
                                ma.image.set_alpha(0)
                                
                                if pygame.mixer.get_init() is not None:
                                    checkPoint_sound.play()

                        elif not playerDino.isSuper:
                            immune_time = pygame.time.get_ticks()
                            if immune_time - collision_time > collision_immune_time:
                                playerDino.collision_immune = False

                CACTUS_INTERVAL = 50
                CLOUD_INTERVAL = 300
                OBJECT_REFRESH_LINE = width * 0.8
                MAGIC_NUM = 10
                MASK_INTERVAL = 50

                if (isHumanTime):
                    if (Itemtime == True) and (human.pattern_idx == 2) and (Umbrella == True):
                        um=obj()
                        um.put_img("./sprites/umbrella_item.png")
                        um.change_size(70,70)
                        um.x = (playerDino.rect.left+playerDino.rect.right)/2-40
                        um.y = playerDino.rect.bottom - 70
                        um.move = 5

                        if (len(pm_list)==0):
                            pass
                        else:
                            # print("x: ",pm.x,"y: ",pm.y)
                            for pm in pm_list:
                                if (pm.y>=um.y)and(pm.x<=um.x+35)and(pm.x>=um.x-35):
                                    pm.set_alpha(0)

                    else:
                        if (len(pm_list)==0): pass # 보스 공격 모션
                        else:
                            for pm in pm_list:
                                if (pm.x>=playerDino.rect.left)and(pm.x<=playerDino.rect.right)and(pm.y>playerDino.rect.top)and(pm.y<playerDino.rect.bottom):
                                    print("공격에 맞음.")
                                    playerDino.collision_immune = True
                                    life -= 1
                                    collision_time = pygame.time.get_ticks()
                                    if life == 0:
                                        playerDino.isDead = True
                                    pm_list.remove(pm)


                if (isHumanTime) and (Itemtime == True) and (human.pattern_idx == 3) and (Maskplus == True):
                    playerDino.score2 = 0
                    Maskplus = False

                if (isHumanAlive) and (playerDino.score> human_appearance_score):
                    isHumanTime = True
                else:
                    isHumanTime = False

                # 보스몬스터 타임 - 선인장, 불선인장만 나오도록
                if isHumanTime:
                    if len(cacti) < 2:
                        if len(cacti) == 0 and playerDino.score <= 1:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))
                        else:
                            for l in last_obstacle:
                                if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL) == MAGIC_NUM:
                                    last_obstacle.empty()
                                    last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))

                    if len(fire_cacti) < 2:
                        for l in last_obstacle:
                            if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL*5) == MAGIC_NUM:
                                last_obstacle.empty()
                                last_obstacle.add(fire_Cactus(gamespeed, object_size[0], object_size[1]))

                    if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                        Cloud(width, random.randrange(height / 5, height / 2))

                    if (len(m_list)==0): pass # 다이노 공격 모션
                    else:
                        if (m.x>=human.rect.left)and(m.x<=human.rect.right)and(m.y>human.rect.top)and(m.y<human.rect.bottom):
                            isDown=True
                            boom=obj()
                            boom.put_img("./sprites/boom.png")
                            boom.change_size(200,100)
                            boom.x=human.rect.centerx-round(human.rect.width)
                            boom.y=human.rect.centery-round(human.rect.height/2)
                            human.hp -= 1
                            m_list.remove(m)

                            if human.hp <= 0:
                                human.kill()
                                isHumanAlive=False


                    if (len(rm_list)==0): pass # 보스 공격 모션
                    else:
                        for rm in rm_list:
                            if (rm.x>=playerDino.rect.left)and(rm.x<=playerDino.rect.right)and(rm.y>playerDino.rect.top)and(rm.y<playerDino.rect.bottom):
                                print("공격에 맞음.")
                                playerDino.collision_immune = True
                                life -= 1
                                collision_time = pygame.time.get_ticks()
                                if life == 0:
                                    playerDino.isDead = True
                                rm_list.remove(rm)
                    if (isHumanTime) and (human.pattern_idx == 3):
                        if len(mask_items) < 2:
                            for l in last_obstacle:
                                if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(MASK_INTERVAL) == MAGIC_NUM:
                                    last_obstacle.empty()
                                    last_obstacle.add(Mask_item(gamespeed, object_size[0], object_size[1]))


                # 다이노 공격 타임 - 선인장만 나오도록
                else:
                    if len(cacti) < 2:
                        if len(cacti) == 0:
                            last_obstacle.empty()
                            last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))
                        else:
                            for l in last_obstacle:
                                if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(CACTUS_INTERVAL) == MAGIC_NUM:
                                    last_obstacle.empty()
                                    last_obstacle.add(Cactus(gamespeed, object_size[0], object_size[1]))

                    if len(clouds) < 5 and random.randrange(CLOUD_INTERVAL) == MAGIC_NUM:
                        Cloud(width, random.randrange(height / 5, height / 2))
                    if (isHumanTime) and (human.pattern_idx == 3):
                        if len(mask_items) < 2:
                            for l in last_obstacle:
                                if l.rect.right < OBJECT_REFRESH_LINE and random.randrange(MASK_INTERVAL) == MAGIC_NUM:
                                    last_obstacle.empty()
                                    last_obstacle.add(Mask_item(gamespeed, object_size[0], object_size[1]))


                playerDino.update()
                cacti.update()
                fire_cacti.update()
                clouds.update()
                holes.update()
                new_ground.update()
                scb.update(playerDino.score, high_score)
                boss.update(human.hp)
                heart.update(life)
                mask_items.update()
                m_time.update(playerDino.score2)
                if (human.pattern_idx != 3):
                    playerDino.score2 = 0

                # 보스몬스터 타임이면,
                if isHumanTime:
                    human.update()

                if pygame.display.get_surface() != None:
                    screen.fill(background_col)
                    screen.blit(Background, Background_rect)
                    new_ground.draw()
                    clouds.draw(screen)
                    scb.draw()
                    boss.draw()
                    heart.draw()
                    cacti.draw(screen)
                    holes.draw(screen)
                    fire_cacti.draw(screen)
                    if (isHumanTime) and (human.pattern_idx == 3):
                        mask_items.draw(screen)
                        m_time.draw()
                        

                    # pkingtime이면, 보스몬스터를 보여줘라.
                    if isHumanTime:
                        human.draw()
                        for pm in pm_list: pm.show()

                    if (isHumanTime) and (human.pattern_idx == 2):
                        human.draw()
                        for rm in rm_list: rm.show()

                   # 5. 미사일 배열에 저장된 미사일들을 게임 스크린에 그려줍니다.
                    for m in m_list:
                        m.show()
                        # print(type(mm.x))
                    if isDown :
                        boom.show()
                        boomCount+=1
                        # boomCount가 5가 될 때까지 boom이미지를 계속 보여준다.
                        if boomCount>10:
                            boomCount=0
                            isDown=False
                    #
                    if (isHumanTime):
                        if (Itemtime == True) and (human.pattern_idx == 2) and (Umbrella == True):
                            um.show()

                    playerDino.draw()
                    resized_screen.blit(
                        pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                        resized_screen_centerpos)
                    pygame.display.update()
                clock.tick(FPS)

                if playerDino.score2 == 100:
                    playerDino.isDead = True

                if playerDino.isDead:
                    gameOver = True
                    pygame.mixer.music.stop()  # 죽으면 배경음악 멈춤
                    if playerDino.score > high_score:
                        high_score = playerDino.score

                if counter % speed_up_limit_count == speed_up_limit_count - 1:
                    new_ground.speed -= 1
                    gamespeed += 1

                counter = (counter + 1)

        if gameQuit:
            break

        while gameOver:
            if pygame.display.get_surface() == None:
                print("Couldn't load display surface")
                gameQuit = True
                gameOver = False
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        gameQuit = True
                        gameOver = False
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            gameQuit = True
                            gameOver = False

                        if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                            gameOver = False
                            gameQuit = True
                            typescore(playerDino.score)
                            if not db.is_limit_data(playerDino.score):
                                db.query_db(
                                    f"insert into user(username, score) values ('{gamername}', '{playerDino.score}');")
                                db.commit()
                                board()
                            else:
                                board()

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        gameOver = False
                        gameQuit = True
                        typescore(playerDino.score)
                        if not db.is_limit_data(playerDino.score):
                            db.query_db(
                                f"insert into user(username, score) values ('{gamername}', '{playerDino.score}');")
                            db.commit()
                            board()
                        else:
                            board()

                    if event.type == pygame.VIDEORESIZE:
                        checkscrsize(event.w, event.h)

            scb.update(playerDino.score,high_score)
            boss.update(human.hp)
            if pygame.display.get_surface() != None:
                disp_gameOver_msg(gameover_image)
                scb.draw()
                boss.draw()
                resized_screen.blit(
                    pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                    resized_screen_centerpos)
                pygame.display.update()
            clock.tick(FPS)

    pygame.quit()
    quit()
    
def gamerule():
    global resized_screen
    gameQuit = False
    max_per_screen = 10
    screen_board_height = resized_screen.get_height()
    screen_board = pygame.surface.Surface((
        resized_screen.get_width(),
        screen_board_height
        ))

    gamerule_image, gamerule_rect= load_image("gamerule.png",800,300,-1)
    gamerule_rect.centerx=width*0.5
    gamerule_rect.centery=height*0.5

    while not gameQuit:
        if pygame.display.get_surface() is None:
            gameQuit = True
        else:
            screen_board.fill(background_col)
            screen_board.blit(gamerule_image,gamerule_rect)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameQuit = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                        gameQuit = True
                        # introscreen()
                        option()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        gameQuit = True
                        # introscreen()
                        option()
                if event.type == pygame.VIDEORESIZE:
                    checkscrsize(event.w, event.h)

            screen.blit(screen_board, (0,0))
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())), resized_screen_centerpos)
            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

def pausing():
    global resized_screen
    gameQuit = False
    pause_pic, pause_pic_rect = alpha_image('Paused.png', width, height, -1)

    pygame.mixer.music.pause()  # 일시정지상태가 되면 배경음악도 일시정지

    # BUTTON IMG LOAD
    retbutton_image, retbutton_rect = load_image('main_button.png', 70, 62, -1)
    resume_image, resume_rect = load_image('continue_button.png', 70, 62, -1)

    resized_retbutton_image, resized_retbutton_rect = load_image(*resize('main_button.png', 70, 62, -1))
    resized_resume_image, resized_resume_rect = load_image(*resize('continue_button.png', 70, 62, -1))

    # BUTTONPOS
    retbutton_rect.centerx = width * 0.4
    retbutton_rect.top = height * 0.52
    resume_rect.centerx = width * 0.6
    resume_rect.top = height * 0.52

    resized_retbutton_rect.centerx = resized_screen.get_width() * 0.4
    resized_retbutton_rect.top = resized_screen.get_height() * 0.52
    resized_resume_rect.centerx = resized_screen.get_width() * 0.6
    resized_resume_rect.top = resized_screen.get_height() * 0.52

    while not gameQuit:
        if pygame.display.get_surface() is None:
            print("Couldn't load display surface")
            gameQuit = True
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    gameQuit = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.mixer.music.unpause()  # pausing상태에서 다시 esc누르면 배경음악 일시정지 해제
                        return False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed() == (1, 0, 0):
                        x, y = event.pos
                        if resized_retbutton_rect.collidepoint(x, y):
                            introscreen()

                        if resized_resume_rect.collidepoint(x, y):
                            pygame.mixer.music.unpause()  # pausing상태에서 오른쪽의 아이콘 클릭하면 배경음악 일시정지 해제

                            return False

                if event.type == pygame.VIDEORESIZE:
                    checkscrsize(event.w, event.h)

            screen.fill(white)
            screen.blit(pause_pic, pause_pic_rect)
            screen.blit(retbutton_image, retbutton_rect)
            screen.blit(resume_image, resume_rect)
            resized_screen.blit(
                pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
                resized_screen_centerpos)
            pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()


def typescore(score):
    global resized_screen
    global gamername
    global width, height
    done = False
    active = True

    message_pos = (width * 0.25, height * 0.3)
    score_pos = (width * 0.35, height * 0.4)
    inputbox_pos = (width * 0.43, height * 0.5)
    typebox_size = 100
    letternum_restriction = 3
    input_box = pygame.Rect(inputbox_pos[0], inputbox_pos[1], 500, 50)
    color = pygame.Color('dodgerblue2')

    text = ''
    text2 = font.render("플레이어 이름을 입력해주세요", True, black)
    text3 = font.render(f"CURRENT SCORE: {score}", True, black)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                introscreen()
            if event.type == pygame.KEYDOWN:
                # if active:
                if event.key == pygame.K_RETURN:
                    gamername = text.upper()
                    done = True
                elif event.key == pygame.K_BACKSPACE:
                    text = text[:-1]
                else:
                    if event.unicode.isalpha() == True:
                        if len(text) < letternum_restriction:
                            text += event.unicode

            if event.type == pygame.VIDEORESIZE:
                checkscrsize(event.w, event.h)

        screen.fill(white)
        txt_surface = textsize(50).render(text.upper(), True, color)
        input_box.w = typebox_size
        screen.blit(txt_surface, (input_box.centerx - len(text) * 11 - 5, input_box.y))
        screen.blit(text2, message_pos)
        screen.blit(text3, score_pos)
        pygame.draw.rect(screen, color, input_box, 2)
        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_centerpos)

        #화면 업데이트 코드
        pygame.display.flip()
        clock.tick(FPS)


def credit():
    global resized_screen
    done = False
    creditimg, creditimg_rect = alpha_image('credit.png', width, height, -1)

    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
            if event.type == pygame.MOUSEBUTTONDOWN:
                return False
            if event.type == pygame.VIDEORESIZE:
                checkscrsize(event.w, event.h)
        screen.fill(white)
        screen.blit(creditimg, creditimg_rect)
        resized_screen.blit(
            pygame.transform.scale(screen, (resized_screen.get_width(), resized_screen.get_height())),
            resized_screen_centerpos)
        pygame.display.update()

        clock.tick(FPS)

    #게임 종료
    pygame.quit()
    quit()








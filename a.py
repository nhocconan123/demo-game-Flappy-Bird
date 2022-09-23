from bisect import bisect_right
from multiprocessing import Event
from os import access
# import Screen, sys
import pygame,sys, random
#tao ham cho tro choi
def draw_floor():
    screen.blit(floor,(floor_x_pos,650))
    screen.blit(floor,(floor_x_pos+432,690))

def create_pipe():
    radom_pipe_pos=random.choice(pipe_height)
    bottom_pipe = pipe_surface.get_rect(midtop=(600,radom_pipe_pos))
    top_pipe = pipe_surface.get_rect(midtop=(600,radom_pipe_pos-650))
    return bottom_pipe,top_pipe

#xu ly ong
def move_pipe(pipes):
    for pipe in pipes:
        pipe.centerx -=5
    return pipes
def draw_pipe(pipes):
    for pipe in pipes:
        if pipe.bottom >= 600:
            screen.blit(pipe_surface,pipe)
        else:
            flip_pipe= pygame.transform.flip(pipe_surface,False,True)
            screen.blit(flip_pipe,pipe)
#xu ly va cham
def check_collision(pipes):
    for pipe in pipes:
        if bird_rect.colliderect(pipe):
            print('va cham')
            return False
    if bird_rect.top <=-75 or bird_rect.bottom >=650:
        print('va cham')
        return False
    return True

#ham xoay chim
def rotate_bird(bird1):
    new_bird =pygame.transform.rotozoom(bird1,-bird_movement*3,1)
    return new_bird

#tao hieu ung dap canh cho chim
def bird_animation():
    new_bird=bird_list[bird_index]
    new_bird_rect=new_bird.get_rect(center=(100,bird_rect.centery))
    return new_bird,new_bird_rect
def score_display(game_state):
    if game_state=='main game':
        score_surface=game_font.render(str(int(score)),True,(255,255,255))
        scoree_rect= score_surface.get_rect(center=(216,100))
        screen.blit(score_surface,scoree_rect)
    if game_state=='game over':
        score_surface=game_font.render( f'Score :{int(score)}',True,(255,255,255))
        scoree_rect= score_surface.get_rect(center=(216,100))
        screen.blit(score_surface,scoree_rect)

        hight_score_surface=game_font.render( f'Hight Score: {int(high_score)}',True,(255,255,255))
        hight_score_rect= hight_score_surface.get_rect(center=(216,610))
        screen.blit(hight_score_surface,hight_score_rect)

def update_score(score,high_score):
    if score < high_score:
        high_score=score
    return high_score

pygame.init() #khoi tao

screen =pygame.display.set_mode((432,768))

clock= pygame.time.Clock()
game_font=pygame.font.SysFont('arial', 40)

# pygame.font.Font("myfont.ttf", size)

# tao cac bien cho tro choi



gravity= 0.25
bird_movement = 0
game_active= True
score=0
high_score=0
# game_active=False

#cho ham nay chay hien thi tren man hinh

#chen back ground
bg=pygame.image.load('assets/background-night.png')
bg=pygame.transform.scale2x(bg)

#chen san
floor =pygame.image.load('assets/floor.png')
floor=pygame.transform.scale2x(floor)
floor_x_pos=0
#tao chim
bird_dow=pygame.transform.scale2x(pygame.image.load('assets/yellowbird-downflap.png').convert_alpha())
bird_mid=pygame.transform.scale2x(pygame.image.load('assets/yellowbird-midflap.png').convert_alpha())
bird_up=pygame.transform.scale2x(pygame.image.load('assets/yellowbird-upflap.png').convert_alpha())
bird_list=[bird_dow,bird_mid,bird_up]
bird_index=0
# print(bird_index)
bird=bird_list[bird_index]
# bird = pygame.image.load('assets/yellowbird-midflap.png').convert_alpha()
# bird =pygame.transform.scale2x(bird)
bird_rect = bird.get_rect(center=(100,384))
#tạo timer cho bird
birdflap=pygame.USEREVENT+1
pygame.time.set_timer(birdflap,200)

#tao ong
pipe_surface = pygame.image.load('assets/pipe-green.png').convert()
pipe_surface =pygame.transform.scale2x(pipe_surface)
pipe_list=[]
#tao timer
spawnpipe = pygame.USEREVENT
pygame.time.set_timer(spawnpipe,1200)
pipe_height =[200,300,400]


# running=True
while True:
    #Screen.fill(GREY)
    #pygame.draw.rect(Screen,WHITE,(100,50,50,50))
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type==pygame.KEYDOWN:
            if event.key== pygame.K_SPACE:
                bird_movement =0
                bird_movement = -11
            #check cho nguoi dung choi lai game
            if event.key==pygame.K_SPACE and game_active==False:
                # print('chay  vao den day roi ne ahihi')
                game_active=True
                pipe_list.clear()
                bird_rect.center=(100,384)
                bird_movement=0
                score=0
        if event.type==spawnpipe:
            pipe_list.extend(create_pipe())
            print(create_pipe)

        if event.type==birdflap:
            if bird_index <2:
                bird_index +=1
            else:
                bird_index=0
            bird,bird_rect=bird_animation()

    screen.blit(bg,(0,0))  #khai bao de hien thi du lieu anh
    if game_active:
        #chim
        bird_movement += gravity #tạo trọng lực
        rotated_bird=rotate_bird(bird)#xoay hinh ảnh chim
        bird_rect.centery += bird_movement
        screen.blit(rotated_bird,bird_rect)

        # va cham
        game_active= check_collision(pipe_list)
        #ong
        pipe_list= move_pipe(pipe_list)
        draw_pipe(pipe_list)
        score +=0.01
        score_display('main game')#tinh diem
    else:
        high_score=update_score(score,high_score)
        score_display('game over')
    #san
    floor_x_pos -=1
    draw_floor()
    if floor_x_pos <= -432:
        floor_x_pos =0
    #screen.blit(floor,(floor_x_pos,600))  #khai bao de hien thi du lieu anh
    pygame.display.update()
    clock.tick(120)

pygame.quit()
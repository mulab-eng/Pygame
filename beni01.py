import pygame
import sys
import math
import random
import os

############################### ウィンドウの大きさ　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　　
WIDTH=1200
HEIGHT=670

########################### 画像ファイルを読み込む
img_weapon = pygame.image.load("./image/bullet.png")
img_weapon2 = pygame.image.load("./image/bullet2.png")
img_robot = pygame.image.load("./image/robot.png")
img_enemy = pygame.image.load("./image/enemy.png")
img_bakuhatsu= pygame.image.load("./image/bakuhatsu.png")
img_bakuhatsu2= pygame.image.load("./image/bakuhatsu2.png")
img_wall = pygame.image.load("./image/wall.png")
img_haikei=pygame.image.load("./image/haikei.png")
img_start=pygame.image.load("./image/start.png")
img_gameover=pygame.image.load("./image/gameover.png")
img_high=pygame.image.load("./image/high.png")

se_shot=None # 音声ファイル用変数
se_hit=None

############################### スコア
score=100

# count=0
ta=0

written=0
switch=0

scorefile=open('score01.txt','r')
zenkaiscore_str = scorefile.read()
if len(zenkaiscore_str) < 1:
    zenkaiscore_str='-100'
zenkaiscore = int(zenkaiscore_str)
scorefile.close()

scorefile=open('score01.txt','w')

############################### 地上局の弾の変数
e_msl_f=False
e_msl_x=300       # 弾のx座標
e_msl_y=300       # 弾のy座標
e_msl_theta=0   # 弾の角度

################################ 地上局の変数
emy_x=200
emy_y=200
emy_vx=-40
emy_vy=-30
emy_theta=(5/4)*math.pi
emy_v=0
emy_omega=0.0

############################## 人工衛星の変数
Radius=300  # 軌道の半径
R_theta=0  # 軌道の角度
R_Omega=0.1  # 軌道の角速度
xr=Radius  # 人工衛星のx座標
yr=0   # 人工衛星の y座標
vx= 40  # x方向の速度（初期値）
vy= 30  # y方向の速度
theta=0 # 人工衛星の角度の初期値[rad]
v=10   #[m/sec]  # 前進方向の速度
omega=-0.5 #[rad/sec]  # 回転の角速度

################################### 画面の更新
deltaT=1/30  # 画面更新の刻み時間 Δt
timer=0  # 時間を測る変数

# ゲームの開始，プレイ中，ゲームオーバーを管理する変数
idx=0  
########## ジョイスティック（ゲームパッド）の有無
Joys=0  #初期値は無し

######## 複数の弾を発射できるようにする ########
MISSILE_MAX = 100
msl_no = 0
msl_f = [False]*MISSILE_MAX
msl_x = [0]*MISSILE_MAX
msl_y = [0]*MISSILE_MAX
msl_theta=[0]*MISSILE_MAX  # 弾の角度
key_spc = 0
joy_b = 0

##############################################   画像化した文字を表示   ########################################################## 
def disp_str(screen, img, x, y, th, k):  # 画像を位置(x,y)，角度thで表示する関数．
                                        #  imgはファイル名，kは拡大縮小の倍率
    X= WIDTH*0.5 + x   # 座標変換
    Y= HEIGHT*0.5 - y # 座標変換
    th=th*180/math.pi # 座標変換
    TH=th # 座標変換
    img1 = pygame.transform.rotozoom(img, TH, k)  # 画像の回転と拡大縮小
    X = X - img1.get_width()/2    # 位置の微調整
    Y = Y - img1.get_height()/2   # 位置の微調整
    screen.blit(img1, [X, Y])     # 画像の表示
##############################################   画像表示   ########################################################## 
def disp_img(screen, img, x, y, th, k):  # 画像を位置(x,y)，角度thで表示する関数．
                                        #  imgはファイル名，kは拡大縮小の倍率
    X= WIDTH*0.5 + x   # 座標変換
    Y= HEIGHT*0.5 - y # 座標変換
    th=th*180/math.pi # 座標変換
    TH=th-90 # 座標変換
    img1 = pygame.transform.rotozoom(img, TH, k)  # 画像の回転と拡大縮小
    X = X - img1.get_width()/2    # 位置の微調整
    Y = Y - img1.get_height()/2   # 位置の微調整
    screen.blit(img1, [X, Y])     # 画像の表示

##############################################   弾   ########################################################## 
def set_missile(): # 弾の初期設定
    global xr, yr, vx, vy, theta, v, omega, deltaT, msl_no
    global msl_f, msl_x, msl_y, msl_theta
    if msl_f[msl_no] == False:  # 弾が存在しなければ
        msl_f[msl_no]= True     # 弾を存在させて
        msl_x[msl_no] = xr+20*math.cos(theta) # 弾の発射位置のx座標を計算（人工衛星の近く）
        msl_y[msl_no] = yr+20*math.sin(theta) # 弾の発射位置のy座標を計算（人工衛星の近く）
        msl_theta[msl_no]=theta  # 発射するときの弾の角度を人工衛星の角度と同じに設定
        msl_no = (msl_no+1)%MISSILE_MAX

def e_set_missile(): # 地上局の弾の初期設定
    global emy_x, emy_y, emy_vx, emy_vy, emy_theta, emy_v, emy_omega, deltaT 
    global e_msl_f, e_msl_x, e_msl_y, e_msl_theta
    if e_msl_f == False:  # 地上局の弾が存在しなければ
        e_msl_f= True     # 地上局の弾を存在させて
        e_msl_x = emy_x+20*math.cos(emy_theta) # 地上局の弾の発射位置のx座標を計算（人工衛星の近く）
        e_msl_y = emy_y+20*math.sin(emy_theta) # 地上局の弾の発射位置のy座標を計算（人工衛星の近く）
        e_msl_theta=emy_theta  # 発射するときの地上局の弾の角度を地上局の角度と同じに設定

def move_missile(screen):  # 弾を動かす関数
    global xr, yr, vx, vy, theta, v, omega, deltaT 
    global msl_f, msl_x, msl_y, msl_theta
    for i in range(MISSILE_MAX):
        if msl_f[i] == True:
            msl_x[i] = msl_x[i]  + 15*math.cos(msl_theta[i]) # 弾のx座標を更新
            msl_y[i] = msl_y[i]  + 15*math.sin(msl_theta[i]) # 弾のy座標を更新
            if math.fabs(msl_x[i]) > WIDTH*0.5: # 弾のx座標の絶対値がウィンドウの半分を超えたら
                msl_f[i]=False # 弾はウィンドウから出るので存在しない（False）とする
            if math.fabs(msl_y[i]) > HEIGHT*0.5: # 弾のy座標の絶対値がウィンドウの半分を超えたら
                msl_f[i]=False # 弾はウィンドウから出るので存在しない（False）とする
            disp_img(screen, img_weapon, msl_x[i], msl_y[i], msl_theta[i], 0.05) # 弾の画像を位置と角度を指定して表示

def e_move_missile(screen):  # 地上局の弾を動かす関数
    global emy_x, emy_y, emy_vx, emy_vy, emy_theta, emy_v, emy_omega, deltaT 
    global e_msl_f, e_msl_x, e_msl_y, e_msl_theta
    if e_msl_f == True:
        e_msl_x = e_msl_x  + 15*math.cos(e_msl_theta) # 弾のx座標を更新
        e_msl_y = e_msl_y  + 15*math.sin(e_msl_theta) # 弾のy座標を更新
        if math.fabs(e_msl_x) > WIDTH*0.5: # 弾のx座標の絶対値がウィンドウの半分を超えたら
            e_msl_f=False # 弾はウィンドウから出るので存在しない（False）とする
        if math.fabs(e_msl_y) > HEIGHT*0.5: # 弾のy座標の絶対値がウィンドウの半分を超えたら
            e_msl_f=False # 弾はウィンドウから出るので存在しない（False）とする
        disp_img(screen, img_weapon2, e_msl_x, e_msl_y, e_msl_theta, 0.15) # 弾の画像を位置と角度を指定して表示


##############################################   人工衛星   ########################################################## 
def move_robot(screen):  # 人工衛星を動かす関数
    global xr, yr, vx, vy, theta, v, omega, deltaT, score, R_Omega, R_theta
    # vx=v*math.cos(theta)   # 人工衛星のx方向の速度
    # vy=v*math.sin(theta)   # 人工衛星のy方向の速度
    vx=-Radius*R_Omega*math.sin(R_theta)   # 人工衛星のx方向の速度
    vy=Radius*R_Omega*math.cos(R_theta)   # 人工衛星のy方向の速度
    R_theta=R_theta+R_Omega*deltaT  # 軌道の角度を更新
    thetadot=omega         # 人工衛星の角速度
    xr = xr + vx * deltaT   # 人工衛星のx座標を更新
    yoyu=30
    if xr > WIDTH*0.5-yoyu:
        xr= WIDTH*0.5-yoyu
    if xr < -WIDTH*0.5+yoyu:
        xr= -WIDTH*0.5+yoyu
    yr = yr + vy * deltaT   # 人工衛星のy座標を更新
    if yr > HEIGHT*0.5-yoyu:
        yr= HEIGHT*0.5-yoyu
    if yr < -HEIGHT*0.5+yoyu:
        yr= -HEIGHT*0.5+yoyu
    theta = theta + thetadot * deltaT  # 人工衛星の角度を更新
    disp_img(screen, img_robot, xr, yr, theta, 0.3) # 人工衛星の画像を位置と角度を指定して表示
    kyori2=(xr-e_msl_x)*(xr-e_msl_x)+(yr-e_msl_y)*(yr-e_msl_y)
    kyori=math.sqrt(kyori2)
    if kyori < 40:
        #地上局の上に画像を表示
        disp_img(screen, img_bakuhatsu, xr, yr, theta, 0.25)
        # score = score-1
        # count = count +1
        
##############################################  地上局 ########################################################## 
def move_enemy(screen):  # 地上局を動かす関数
    global emy_x, emy_y, emy_vx, emy_vy, emy_theta, emy_v, emy_omega, deltaT, score, count
    emy_vx=emy_v*math.cos(emy_theta)   # 地上局のx方向の速度
    emy_vy=emy_v*math.sin(emy_theta)   # 地上局のy方向の速度
    # emy_thetadot=emy_omega         # 地上局の角速度
    emy_x = emy_x + emy_vx * deltaT   # 地上局のx座標を更新
    emy_y = emy_y + emy_vy * deltaT   # 地上局のy座標を更新
    # emy_theta = emy_theta + emy_thetadot * deltaT  # 地上局の角度を更新
    
    e_kyori2=(xr-emy_x)*(xr-emy_x)+(yr-emy_y)*(yr-emy_y)
    e_kyori=math.sqrt(e_kyori2)
    if e_kyori > 270:
        move = ["front","stop"]
        choice = random.choice(move)
        if timer%15==0:
            if choice=="front":
                emy_v=30
            if choice=="stop":
                emy_v=0
    if e_kyori < 270:
        emy_v=-40

    ahead_t= 2.2 # 予測時間(秒) 好みに応じて調整
    next_xr = xr + vx * ahead_t
    next_yr = yr + vy * ahead_t
    dx = next_xr - emy_x
    dy = next_yr - emy_y

    if emy_theta > 2*math.pi:
        emy_theta = emy_theta - 2*math.pi
    if emy_theta < 0:
        emy_theta = emy_theta + 2*math.pi
    r_thetarad=math.atan2(dy,dx)  # 地上局から人工衛星へ引いたベクトルのラジアンの角度
    if r_thetarad < 0:
        r_thetarad = r_thetarad + 2*math.pi

    e=(emy_theta-r_thetarad+math.pi)%(2*math.pi)-math.pi
    gain=-1.0
    emy_thetadot=gain*e
    emy_theta = emy_theta + emy_thetadot * deltaT

    disp_img(screen, img_enemy, emy_x, emy_y, emy_theta, 0.15) # 地上局の画像を位置と角度を指定して表示

    if emy_x > WIDTH*0.5:
        emy_x = WIDTH*0.5
    if emy_x < -WIDTH*0.5:
        emy_x = -WIDTH*0.5
    if emy_y > HEIGHT*0.5:
        emy_y = HEIGHT*0.5
    if emy_y < -HEIGHT*0.5:
        emy_y = -HEIGHT*0.5    

    for i in range(MISSILE_MAX):
        if msl_f[i] == True:
            kyori2=(emy_x-msl_x[i])*(emy_x-msl_x[i])+(emy_y-msl_y[i])*(emy_y-msl_y[i])
            kyori=math.sqrt(kyori2)
            if kyori < 40:
                # count = count +1
                se_hit.play()
                #地上局の上に画像を表示
                disp_img(screen, img_bakuhatsu2, emy_x, emy_y, emy_theta, 0.2)
                msl_f[i]=False
                kyori3 = (emy_x-xr)*(emy_x-xr)+(emy_y-yr)*(emy_y-yr) 
                kyori4 = math.sqrt(kyori3) 
                score=score + 1 

##############################################   メイン  ########################################################## 
def main():
    global xr, yr, vx, vy, theta, v, omega, deltaT, timer
    global idx, key_spc, joy_b, bgm, scorefile, score
    global se_shot, se_hit, written, zenkaiscore, switch
    pygame.init()
    pygame.joystick.init()
    pygame.display.set_caption("シューティングゲーム")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # ウィンドウのサイズ
    clock = pygame.time.Clock()  # 画面更新のためにクロックをつくっておく
    se_shot=pygame.mixer.Sound('./sound/shot.wav')
    se_hit=pygame.mixer.Sound('./sound/hit.wav')
    font = pygame.font.Font(None, 50) # 文字のフォントと大きさ
    font2 = pygame.font.Font(None, 140) # 文字のフォントと大きさ
    font3 = pygame.font.Font(None, 190) # 文字のフォントと大きさ
    pygame.mixer.music.load('./sound/bgm.wav')
    time_limit=30 #制限時間

    while True:
        for event in pygame.event.get():  
            if event.type == pygame.QUIT:  # ×が押されたら終了する
                pygame.quit()
                sys.exit()
        screen.fill((55, 55, 240))   # ウィンドウの内部に色を塗る
        try:
            joystick = pygame.joystick.Joystick(0)
            joystick.init()
            joy_lr = joystick.get_axis(0)
            joy_ud = joystick.get_axis(1)
            joyL_lr = joystick.get_axis(2)
            joyL_ud = joystick.get_axis(3)
            jbtn1 = joystick.get_button(0)+joystick.get_button(1)+joystick.get_button(2)+joystick.get_button(3)
            jbtn2 = joystick.get_button(2) # Xボタン
            jbtn3 = joystick.get_button(4) # LB
            jbtn4 = joystick.get_button(5) # RB
            jbtn5 = joystick.get_button(7) # START
            jbtn6 = joystick.get_button(6)  # BACK
            jbtn7 = joystick.get_button(3)  # 黄色
            Joys=1
        except:
            Joys=0
        key=pygame.key.get_pressed()  # キーボードが押されたらそのキーをkeyとして記憶

        if idx==0:  # スタート
            screen.blit(img_start, [0, 0])
            if Joys == 1:  ###ゲームパッド
                sur = font.render('Press START button', True, (120,120,40)) # 色を指定して文字str(tmr)を画像surに置き換える
                disp_str(screen, sur, 0, 250, 0, 1.0)
                # screen.blit(sur, [0, 0])  # 座標を指定して画像を表示する
                if (key[pygame.K_SPACE]==True) or (jbtn5 !=0):
                    idx=1
                    pygame.mixer.music.play(-1)
            else:  ###キーボード
                sur = font.render('Press SPACE key', True, (120,120,40)) # 色を指定して文字str(tmr)を画像surに置き換える
                disp_str(screen, sur, 0, 250, 0, 1.0)
                # screen.blit(sur, [0, 0])  # 座標を指定して画像を表示する
                if key[pygame.K_SPACE]==True:
                    idx=1
                    pygame.mixer.music.play(-1)

        if idx==1:   # ゲームプレイ中
            timer=timer+1
            screen.blit(img_haikei, [0, 0])

            # 地上局の弾の発射              
            if timer%10 ==1:
                e_set_missile() #弾の発射準備
            e_move_missile(screen) #発射された弾の移動と画像表示

            # #壁の移動
            # move_wall(screen,timer)
            # contact_wall()

            ##### 弾の発射 #######
            if Joys == 1:
                joy_b = (joy_b+1)*jbtn1
                key_spc = (key_spc+1)*key[pygame.K_SPACE]
            else:
                key_spc = (key_spc+1)*key[pygame.K_SPACE]
            if (joy_b%10 == 1 or key_spc%10 == 1):
                set_missile()
                se_shot.play()
            move_missile(screen) #発射された弾の移動と画像表示

            ####### 人工衛星の制御
            if Joys == 1:
                if jbtn4 != 0:  # RB
                    omega =  - 0.5
                if jbtn3 != 0:  # LB
                    omega =   0.5
                # if joy_ud < -0.01:
                #     v =  70
                #     # omega = 0
                # if joy_ud > 0.01:
                #     v = -70
                #     # omega = 0
                # if joyL_ud < -0.01:
                #     v =  70
                #     # omega = 0
                # if joyL_ud > 0.01:
                #     v = -70
                #     # omega = 0
                if joy_lr  > 0.01:
                    omega =  - 0.5
                if joy_lr < -0.01:
                    omega =   0.5
            #####  キーボード矢印キーでの操作
            if key[pygame.K_RIGHT]==True:
                    omega = - 1
            if key[pygame.K_LEFT]==True:
                    omega =   1
            # if key[pygame.K_UP]==True:
            #         v=  60
            #         omega=0
            # if key[pygame.K_DOWN]==True:
            #         v=- 60
            #         omega=0
            #### 人工衛星の停止       
            if Joys == 1:
                if (jbtn2 != 0) or (jbtn6 != 0): # ボタンXまたはBACKが押されたら
                    omega = 0
                    v=0
            if key[pygame.K_s]==True:  # キーボードでs
                    v=0
                    omega=0 
            move_robot(screen)  # 人工衛星の移動
            move_enemy(screen)  # 地上局の移動
            time=timer*deltaT
            time=math.floor(time) #小数点以下切り捨て
            sur = font.render('Timer: '+str(time_limit-time), True, (120,120,40)) # 色を指定して文字str(tmr)を画像surに置き換える
            screen.blit(sur, [0, 0])  # 座標を指定して画像を表示する
            sur = font.render('Score: '+str(score), True, (0,0,0)) # 色を指定して文字str(tmr)を画像surに置き換える
            screen.blit(sur, [0, 30])  # 座標を指定して画像を表示する
            if (time_limit-time) < 10:
                if switch == 0:
                    pygame.mixer.music.stop()
                    pygame.mixer.music.load('./sound/bgm.wav')
                    pygame.mixer.music.play(-1)
                    switch=1
            if (time_limit-time) < 0:
                idx=2

        if idx==2:   # GAMEOVER表示   
            pygame.mixer.music.stop()
            # 最終スコアの表示
            if zenkaiscore < score:
                screen.blit(img_high, [0, 0])
                sur = font3.render(str(score), True, (255,200,255)) # 色を指定して文字str(tmr)を画像surに置き換える
                disp_str(screen, sur, 10, -45, 0, 1.0)
                # screen.blit(sur, [350, 250])  # 座標を指定して画像を表示する
                if written == 0:
                    scorefile.write(str(score))
                    written=1
            else:
                screen.blit(img_gameover, [0, 0])
                sur = font2.render('Score: '+str(score), True, (255,200,255)) # 色を指定して文字str(tmr)を画像surに置き換える
                disp_str(screen, sur, 0, -45, 0, 1.0)
                # screen.blit(sur, [105, 300])  # 座標を指定して画像を表示する
                if written == 0:
                    scorefile.write(str(zenkaiscore))
                    written=1
            scorefile.close()

        pygame.display.update()  
        clock.tick(30)  # 1秒間に30回，画面を更新

if __name__ == '__main__':
    main()
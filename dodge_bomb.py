import os
import sys
import random
import pygame as pg


WIDTH, HEIGHT = 1600, 900
delta = {pg.K_UP:(0,-5), pg.K_DOWN:(0,5), pg.K_LEFT:(-5,0), pg.K_RIGHT:(5,0)}
accs = [a for a in range(1,11)]
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def check_bound(rct: pg.Rect) -> tuple[bool, bool]:
    yoko, tate = True, True
    if rct.left < 0 or WIDTH < rct.right:  # 横方向判定
        yoko = False
    if rct.top < 0 or HEIGHT < rct.bottom:  # 縦方向判定
        tate = False
    return yoko, tate

def main():
    pg.display.set_caption("逃げろ！こうかとん")
    screen = pg.display.set_mode((WIDTH, HEIGHT))
    bg_img = pg.image.load("fig/pg_bg.jpg")
    kk_img = pg.image.load("fig/3.png")
    kk_img_f = pg.transform.flip(kk_img, True, False)

    kk_img_l = pg.transform.rotozoom(kk_img, 0, 2.0)
    kk_img_r = pg.transform.rotozoom(kk_img_f, 0, 2.0)
    kk_img_ul = pg.transform.rotozoom(kk_img, -45, 2.0)
    kk_img_ur = pg.transform.rotozoom(kk_img_f, 45, 2.0)
    kk_img_dl = pg.transform.rotozoom(kk_img, 45, 2.0)
    kk_img_dr = pg.transform.rotozoom(kk_img_f, -45, 2.0)
    kk_img_u = pg.transform.rotozoom(kk_img_f, 90, 2.0)
    kk_img_d = pg.transform.rotozoom(kk_img, 90, 2.0)

    kk_dct = {(-5,0):kk_img_l,
              (-5,-5):kk_img_ul,
              (0,-5):kk_img_u,
              (5,-5):kk_img_ur,
              (5,0):kk_img_r,
              (5,5):kk_img_dr,
              (0,5):kk_img_d,
              (-5,5):kk_img_dl}
    
    shape = kk_dct[(-5,0)]

    kk_rct = kk_img.get_rect()
    kk_rct.center = 900, 400

    bm_sur = pg.Surface((20,20))
    bm_sur.set_colorkey((0,0,0))
    pg.draw.circle(bm_sur,(0, 0, 255), (10, 10), 10)
    bm_img = bm_sur.get_rect()
    bm_img.center = random.randint(0, WIDTH), random.randint(0, HEIGHT)
    vx, vy = +5, +5
    clock = pg.time.Clock()
    tmr = 0

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT: 
                return
            
        if kk_rct.colliderect(bm_img):
            return #gameover判定
        
        screen.blit(bg_img, [0, 0]) 

        key_lst = pg.key.get_pressed()
        sum_mv = [0, 0]
        for k, v in delta.items():
            if key_lst[k]:
                sum_mv[0] += v[0]
                sum_mv[1] += v[1]
        kk_rct.move_ip(sum_mv)

        for k,v in kk_dct.items():
            if tuple(sum_mv) == k:
                shape = v
                screen.blit(shape,kk_rct)
            else:
                screen.blit(shape,kk_rct)

        if check_bound(kk_rct) != (True, True):
            kk_rct.move_ip(-sum_mv[0], -sum_mv[1])

        bm_img.move_ip(vx, vy)
        yoko, tate = check_bound(bm_img)
        if not yoko:
            vx *= -1
        if not tate:
            vy *= -1
        screen.blit(bm_sur, bm_img)
        pg.display.update()
        tmr += 1
        clock.tick(50)


if __name__ == "__main__":
    pg.init()
    main()
    pg.quit()
    sys.exit()

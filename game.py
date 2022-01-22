import time

import pygame
from pygame import *
import random


class Background():
    def __init__(self, screen):
        self.screen = screen
        self.image1 = pygame.image.load('imgs/img_bg_level_2.jpg')
        self.image2 = pygame.image.load('imgs/img_bg_level_2.jpg')
        self.screen_rect = self.screen.get_rect()
        self.rect1 = self.image1.get_rect()
        self.rect2 = self.image2.get_rect()
        self.rect2.top = -self.screen_rect.height

        self.speed = 2

    def move(self):
        self.screen.blit(self.image1, self.rect1)
        self.screen.blit(self.image2, self.rect2)
        self.rect1.top += self.speed
        self.rect2.top += self.speed
        if self.rect1.top > self.screen_rect.height:
            self.rect1.top = -self.screen_rect.height
        if self.rect2.top > self.screen_rect.height:
            self.rect2.top = -self.screen_rect.height


class MyPlane(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(MyPlane, self).__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load('imgs/hero1.png')
        self.rect = self.image.get_rect()
        self.rect.midbottom = self.screen_rect.midbottom
        self.speed = 10
        self.bullets = pygame.sprite.Group()
        self.life = 3
        self.props = 0
        self.move_up = False
        self.move_down = False
        self.move_right = False
        self.move_left = False
        self.fire = False

    def key_ctrl(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_w or event.key == K_UP:
                self.move_up = True
            elif event.key == K_s or event.key == K_DOWN:
                self.move_down = True
            elif event.key == K_d or event.key == K_RIGHT:
                self.move_right = True
            elif event.key == K_a or event.key == K_LEFT:
                self.move_left = True
            elif event.key == K_SPACE:
                self.fire = True
        elif event.type == pygame.KEYUP:
            if event.key == K_w or event.key == K_UP:
                self.move_up = False
            elif event.key == K_s or event.key == K_DOWN:
                self.move_down = False
            elif event.key == K_d or event.key == K_RIGHT:
                self.move_right = False
            elif event.key == K_a or event.key == K_LEFT:
                self.move_left = False
            elif event.key == K_SPACE:
                self.fire = False

    def bullets_ctrl(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                self.bullets.add(Bullet(self.rect))
                # m=Music()
                # m.play_bullet_sound()
            # if event.key==K_p:
            #     self.props-=1

    def key_pressed_ctrl(self):
        key = pygame.key.get_pressed()
        # key2=pygame.key
        if key[K_w] or key[K_UP]:
            if self.rect.top > 0:
                self.rect.top -= self.speed
        elif key[K_s] or key[K_DOWN]:
            if self.rect.bottom < self.screen_rect.bottom:
                self.rect.bottom += self.speed
        elif key[K_d] or key[K_RIGHT]:
            if self.rect.right < self.screen_rect.right:
                self.rect.right += self.speed
        elif key[K_a] or key[K_LEFT]:
            if self.rect.left > 0:
                self.rect.left -= self.speed
        # elif key[K_SPACE]:
        #     self.bullets.add(Bullet(self.rect))

    def draw(self):
        self.screen.blit(self.image, self.rect)
        self.bullets.update()
        self.bullets.draw(self.screen)

    def update(self):
        self.key_pressed_ctrl()
        # if self.move_up and self.rect.top > self.screen_rect.top:
        #     self.rect.top -= self.speed
        # elif self.move_down and self.rect.bottom < self.screen_rect.bottom:
        #     self.rect.bottom += self.speed
        # elif self.move_right and self.rect.right < self.screen_rect.right:
        #     self.rect.right += self.speed
        # elif self.move_left and self.rect.left > self.screen_rect.left:
        #     self.rect.left -= self.speed
        # elif self.fire:
        #     self.bullets.add(Bullet(self.rect))

        self.draw()


class EnemyPlane(pygame.sprite.Sprite):
    def __init__(self):
        super(EnemyPlane, self).__init__()
        self.image = pygame.image.load('imgs/enemy1.png')
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, Manager.size[0] - self.rect.width)
        self.speed = 3

    def update(self):
        self.rect.top += self.speed


class Boss(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Boss, self).__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load('imgs/enemy2.png')
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, self.screen_rect.width - self.rect.width)
        self.speed = 10
        self.dirction_right = True
        self.bullets = pygame.sprite.Group()
        self.life = 50

    def move(self):
        if self.dirction_right:
            self.rect.right += self.speed
            if self.rect.right >= self.screen_rect.right:
                self.dirction_right = not self.dirction_right
        else:
            self.rect.left -= self.speed
            if self.rect.left <= 0:
                self.dirction_right = not self.dirction_right

    def auto_fire(self):
        if random.randint(0, 150) == 10:
            self.bullets.add(EnemyBullet(self.rect))

    def update(self):
        self.move()
        self.auto_fire()
        self.bullets.update()
        self.bullets.draw(self.screen)


class Bullet(pygame.sprite.Sprite):
    def __init__(self, plane_rect):
        super(Bullet, self).__init__()
        self.image = pygame.image.load('imgs/bullet.png')
        self.rect = self.image.get_rect()
        self.rect.center = plane_rect.center
        self.rect.top = plane_rect.top - self.rect.height
        self.speed = 5

    def update(self):
        self.rect.top -= self.speed
        if self.rect.top < 0:
            self.kill()


class EnemyBullet(Bullet):
    def __init__(self, enemy_plane_rect):
        super(EnemyBullet, self).__init__(enemy_plane_rect)
        self.image = pygame.image.load('imgs/bullet1.png')
        self.speed = 5
        self.rect.bottom = enemy_plane_rect.bottom + self.rect.height

    def update(self):
        self.rect.bottom += self.speed
        if self.rect.bottom > self.rect.bottom:
            self.kill()


class Music():
    def __init__(self):
        pygame.mixer.init()
        pygame.mixer.music.load('sound/bg.wav')
        pygame.mixer.music.set_volume(0.5)
        self.bomb = pygame.mixer.Sound('sound/bomb.wav')
        pygame.mixer.music.set_volume(1)
        self.get_props = pygame.mixer.Sound('sound/props_get.mp3')
        self.use_props = pygame.mixer.Sound('sound/props_use.wav')
        self.bullet_sound = pygame.mixer.Sound('sound/bullet.mp3')

    def play_background_music(self):
        pygame.mixer.music.play(-1)  # 无限循环播放背景音乐

    def play_bomb_sound(self):
        pygame.mixer.Sound.play(self.bomb)

    def play_props_get(self):
        pygame.mixer.Sound.play(self.get_props)

    def play_props_use(self):
        pygame.mixer.Sound.play(self.use_props)

    def play_bullet_sound(self):
        pygame.mixer.Sound.play(self.bullet_sound)


class Bomb():
    def __init__(self, screen, type):
        self.screen = screen
        if type == 'enemy':
            self.images = [pygame.image.load('imgs/enemy1_down{}.png'.format(n)) for n in range(1, 5)]
        elif type == 'boss':
            self.images = [pygame.image.load('imgs/enemy2_down{}.png'.format(n)) for n in range(1, 5)]
        elif type == 'player':
            self.images = [pygame.image.load('imgs/hero_blowup_n{}.png'.format(n)) for n in range(1, 5)]
        self.index = 0
        self.pos = [0, 0]
        self.is_bomb = False

    def action(self, rect):  # 判断是否执行判断，并获取位置
        self.pos = [rect.left, rect.top]
        self.is_bomb = True

    def show(self):
        if self.is_bomb == False:
            return
        else:
            self.screen.blit(self.images[self.index], self.pos)
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
                self.is_bomb = False


class Props(pygame.sprite.Sprite):
    def __init__(self, screen):
        super(Props, self).__init__()
        self.screen = screen
        self.screen_rect = self.screen.get_rect()
        self.image = pygame.image.load('imgs/prop_type_1.png')
        self.rect = self.image.get_rect()
        self.rect.left = random.randint(0, self.screen_rect.width - self.rect.width)
        self.speed = 3

    def auto_move(self):
        if self.rect.top > self.screen_rect.height:
            self.kill()
        self.rect.top += self.speed

    def draw(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        self.auto_move()
        self.draw()


class Score:
    def __init__(self):
        self.historical_score = 0
        self.current_score = 0
        self.historical_score_pos = (200, 400)
        self.current_score_pos = (200, 600)

    def get_score(self):
        with open('score.txt', 'r') as stream:
            self.historical_score = int(stream.readline().rstrip())

    def store_score(self):
        if self.current_score > self.historical_score:
            with open('score.txt', 'w') as wstream:
                wstream.write(str(self.current_score))


class Manager():
    size = (480, 768)

    def __init__(self):
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode(self.size)
        self.music = Music()
        self.players = pygame.sprite.Group()
        self.enemys = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()
        self.props = pygame.sprite.Group()
        self.props_num = 3
        # self.number = 0  # 用于记录主函数循环次数
        self.EVENT_ID_ENEMY = USEREVENT + 1
        self.EVENT_ID_BOSS = USEREVENT + 2
        self.EVENT_ID_PROP = USEREVENT + 3
        self.players_bomb = Bomb(self.screen, 'player')
        self.enemys_bomb = Bomb(self.screen, 'enemy')
        self.bosses_bomb = Bomb(self.screen, 'boss')
        self.score = Score()  # 记录得分
        self.props_used = False
        self.bullet_shoot = False

    def new_player(self):
        self.player = MyPlane(self.screen)
        self.players.add(self.player)

    def new_enemy_player(self):
        self.enemys.add(EnemyPlane())

    def new_boss(self):
        self.bosses.add(Boss(self.screen))

    def new_props(self):
        self.props.add(Props(self.screen))

    def draw_text(self, text, pos=(0, 100), text_height=30, font_color=(255, 0, 0), bg_color=None):
        font_obj = pygame.font.Font('baddf.ttf', text_height)
        text_obj = font_obj.render(text, True, font_color, bg_color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = pos
        self.screen.blit(text_obj, text_rect)

    def draw_props_num(self, text, pos=(200, 100), text_height=30, font_color=(255, 0, 0), bg_color=None):
        font_obj = pygame.font.Font('baddf.ttf', text_height)
        text_obj = font_obj.render(text, True, font_color, bg_color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = pos
        self.screen.blit(text_obj, text_rect)

    def draw_life_num(self, text, pos=(200, 400), text_height=30, font_color=(255, 0, 0), bg_color=None):
        font_obj = pygame.font.Font('baddf.ttf', text_height)
        text_obj = font_obj.render(text, True, font_color, bg_color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = pos
        self.screen.blit(text_obj, text_rect)

    def use_props(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_p:
                if self.props_num > 0:
                    self.props_num -= 1
                    self.props_used = True

    def shoot(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == K_SPACE:
                self.music.play_bullet_sound()


    def game_pause(self):
        pass

    def restart(self):
        pass

    def collide_handler(self):
        self.enemys_bomb.show()
        self.players_bomb.show()
        self.bosses_bomb.show()
        colloide_of_enemybullets_and_players = False
        if self.bosses:
            colloide_of_enemybullets_and_players = pygame.sprite.groupcollide(list(self.bosses)[0].bullets,
                                                                              self.players, True, False)
        colloide_of_players_and_enemys = pygame.sprite.groupcollide(self.enemys, self.players, True, False)
        colloide_of_bullets_and_enemys = pygame.sprite.groupcollide(self.enemys, list(self.players)[0].bullets,
                                                                    True, True)
        colloide_of_bullets_and_bosses = pygame.sprite.groupcollide(self.bosses, list(self.players)[0].bullets,
                                                                    False, True)
        colloide_of_players_and_props = pygame.sprite.groupcollide(self.props, self.players, True, False)

        if colloide_of_players_and_enemys:
            items = list(colloide_of_players_and_enemys.items())
            '''

            pygame.sprite.groupcollide(A，B，Ture，Ture)的返回值为一个字典
            键为A，值为B，两个布尔类型的参数决定对应的精灵是否被kill
            print(items)
            print(items[0])
            print(items[0][0].rect)
            print(items[0][0])
            '''
            enemy = items[0][0]
            player = items[0][1][0]
            player.life -= 1

            self.enemys_bomb.action(enemy.rect)

            self.music.play_bomb_sound()
            self.score.current_score += 100
            if player.life <= 0:
                self.players_bomb.action(player.rect)
                self.players_bomb.show()
                self.players_bomb.show()
                self.players_bomb.show()
                self.players_bomb.show()
                player.kill()
                # pygame.time.delay(500)
                self.game_over()
                '''生命值小于0时死亡，销毁敌机'''
        if colloide_of_bullets_and_enemys:
            items = list(colloide_of_bullets_and_enemys.items())
            enemy = items[0][0]
            self.enemys_bomb.action(enemy.rect)
            self.music.play_bomb_sound()
            self.score.current_score += 100
        if colloide_of_bullets_and_bosses:
            items = list(colloide_of_bullets_and_bosses.items())
            boss = items[0][0]
            boss.life -= 1
            if boss.life <= 0:
                self.bosses_bomb.action(boss.rect)
                # self.bosses_bomb.show()
                # self.bosses_bomb.show()
                # self.bosses_bomb.show()
                # self.bosses_bomb.show()
                # self.bosses_bomb.show()
                boss.kill()
                self.score.current_score += 2000
                self.music.play_bomb_sound()
        if colloide_of_players_and_props:
            if self.props_num < 3:
                self.props_num += 1
                self.music.play_props_get()
        if self.props_used:
            for enemy in list(self.enemys):
                self.enemys_bomb.action(enemy.rect)
                self.enemys_bomb.show()
                # self.music.play_bomb_sound()
                self.music.play_props_use()
                self.score.current_score += len(self.enemys) * 100
                enemy.kill()
            for boss in list(self.bosses):
                if boss.life <= 0:
                    self.bosses_bomb.action(boss.rect)
                    self.bosses_bomb.show()
                    boss.kill()
                boss.life -= 10

                self.props_used = False
        if colloide_of_enemybullets_and_players:
            items = list(colloide_of_enemybullets_and_players.items())
            player = items[0][1][0]
            player.life -= 1
            if player.life <= 0:
                self.players_bomb.action(player.rect)
                self.game_over()

    def game_over(self):
        image1 = pygame.image.load('imgs/gameover2.png')
        image2 = pygame.image.load('imgs/gameover.png')
        self.screen.blit(image1, self.screen.get_rect().topleft)
        pygame.display.update()
        pygame.time.delay(2000)
        self.screen.blit(image2, self.screen.get_rect().topleft)
        self.score.get_score()
        self.score.store_score()
        self.draw_text('{}'.format(self.score.historical_score), self.score.historical_score_pos)
        self.draw_text('{}'.format(self.score.current_score), self.score.current_score_pos)
        pygame.display.update()

        pygame.time.delay(2000)
        pygame.quit()
        exit()

    def main(self):
        pygame.init()
        bg = Background(self.screen)
        self.music.play_background_music()
        self.new_player()  # 修改飞机为单个精灵而非精灵组
        pygame.time.set_timer(self.EVENT_ID_ENEMY, 750)  # 设置定时器，每隔0.5秒生成一个敌机
        pygame.time.set_timer(self.EVENT_ID_BOSS, 60000)  # 一分钟生成一个boss
        pygame.time.set_timer(self.EVENT_ID_PROP, 20000)  # 20秒一个道具
        while 1:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                elif event.type == self.EVENT_ID_ENEMY:
                    self.new_enemy_player()
                elif event.type == self.EVENT_ID_BOSS:
                    self.new_boss()
                elif event.type == self.EVENT_ID_PROP:
                    self.new_props()
                self.use_props(event)
                self.shoot(event)
                list(self.players)[0].bullets_ctrl(event)
            bg.move()
            self.collide_handler()
            self.props.update()
            self.players.update()
            self.enemys.update()
            self.bosses.update()
            self.players.draw(self.screen)
            self.enemys.draw(self.screen)
            self.bosses.draw(self.screen)
            self.draw_text('得分：{}'.format(self.score.current_score))
            self.draw_props_num('剩余炸弹:' + str(self.props_num), (300, 100))
            self.draw_life_num('LIFE:' + str(list(self.players)[0].life), (350, 650))
            pygame.display.update()
            # self.number+=random.randint(0,100)
            self.clock.tick(60)


'''
    1增加碰撞类，死亡特效，音效，吃道具音效；
    2背景音乐
    3小飞机的间隔生成
    4得分，文件读写
    5游戏设置
    6道具类，清楚所有敌方精灵
    
    
    碰撞检测，给己方飞机定义3条命，三个炸弹，吃到道具回生命值，捡到炸弹数量+1，
    如果己方飞机与地方飞机或子弹碰撞，己方飞机生命值-1,获得无敌时间3秒，道具清空所有敌方单位
    学习：碰撞参数，是否kill精灵；定义时间按固定时间生成飞机，道具；
    杀死敌方得分，根据得分出boss，暂定小怪按匀速产生（避免小怪叠加）
    有必要的话调整飞机key_ctrl()防止子弹叠加。
    回顾代码，添加注释；


    
    增加道具类
    飞机死亡的安排
    按键控制的修改
    文件读写记录得分，及得分的显示

'''

if __name__ == '__main__':
    game = Manager()
    game.main()

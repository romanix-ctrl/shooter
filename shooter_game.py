
from pygame import *
from random import randint
lost = 0
killed = 0
class GameSprite(sprite.Sprite):
    def __init__(self, p_image, p_x, p_y, speed):
        super().__init__()
        self.image = transform.scale(image.load(p_image), (50, 50))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < 650:
            self.rect.x += self.speed
        GameSprite.reset(self)
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint(40, 650)
            self.rect.y = 0
            lost = lost + 1

window = display.set_mode((700, 500))
display.set_caption('шутер')
background = transform.scale(image.load('galaxy.jpg'), (700, 500))
#font
font.init()
font = font.SysFont('Arial', 70)

#music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
monsters = sprite.Group()
player = Player('rocket.png', 300, 430, 4)
for i in range(5):
    monster = Enemy('ufo.png', randint(0,700), 0, randint(1,2))
    monsters.add(monster)

bullets = sprite.Group()

#game base
FPS = 30
clock = time.Clock()

game = True
finish = False
#game cycle
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
           if e.key == K_SPACE:
               player.fire()
    if finish == False:
        sprites_list = sprite.groupcollide(monsters, bullets, True, True)
        for i in sprites_list:
            killed += 1
            monster = Enemy('ufo.png', randint(0,700), 0, randint(1,2))
            monsters.add(monster)

        text_lose = font.render('Пропущено:' + str(lost), 1, (255,255,255))
        text_count = font.render('Убито:' + str(killed), 1, (255,255,255))
        window.blit(background, (0, 0))    
        window.blit(text_lose, (10, 50))
        window.blit(text_count, (10, 100))
        player.reset()
        player.update()
        monsters.update()
        bullets.update()
        monsters.draw(window)
        bullets.draw(window)
        if lost >= 100:
            text_loose = font.render('lose', 1, (255,255,255))
            window.blit(text_loose, (200, 200))            
            finish = True
        if killed >= 5:
            text_win = font.render('Вы выиграли!', 1, (255,255,255))
            window.blit(text_win, (200, 200))
            finish = True        
        display.update()




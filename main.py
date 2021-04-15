import pygame.locals as gameGlobals
import pygame, sys
from random import randint
pygame.init()#?
#imports^

screen = pygame.display.set_mode((600,400))
#creates pygame window

class ball:#creats the ball class
  def __init__(self, x, y):#has x,y location and x,y velocity
    self.x = x
    self.y = y
    self.xDir = 5
    self.yDir = 5
  def draw(self):#draws the ball
    pygame.draw.circle(screen,(255,255,255),(self.x,self.y),12)
  def move(self, score):#the x and y increade by the velocity of the bvall
    self.x += self.xDir
    self.y += self.yDir
    pointtobe = self.bounce()#checks to see if the ball hits the op bottom or sides
    if pointtobe == 1:#p2 scores
      board.PLAYER2 += 1
      self.x = 300
      self.y = 200
      dead = 0
    elif pointtobe == 2:#p1 scores
      board.PLAYER1 += 1
      self.x = 300
      self.y = 200
      dead = 0
  def bounce(self):
    if self.x <= 6:#if it goes in player 1s net then give poingt to players 2
      return 1
    if self.x >= 594:#if it goes in player 2s net then give poingt to players 1
      return 2
    if self.y >= 388 or self.y <= 12:#hits top/bottom, inverss y vel to bnounce
      self.yDir = -self.yDir
    return 0#nothing happened
class paddle:#creats paddle class
  def __init__(self, x, y):#has x,y location and y vel
    self.x = x
    self.y = y
    self.yDir = 0
  def draw(self):#draws paddle
    pygame.draw.rect(screen,(255,255,255),(self.x,self.y, 20, 80))
  def move(self):#as long as it is inside the screen move it by its vel
    if self.y+self.yDir < 320 and self.y+self.yDir > 0:
      self.y += self.yDir
  def bounce(self, pong):#it ball collides then inverse its vel so it bounces
    if pong.x in range(self.x-5, self.x+25) and pong.y in range(self.y-10,self.y+90):
      pong.xDir = -pong.xDir
  def folow(self, y):#tracks ball, is a bit slower so you could ptoentially score but it is very ahrd, try using a powerup!
    if y > self.y:
      self.y += 5
    elif y < self.y:
      self.y -= 5
class bonus(paddle):#child class of paddle, bonus paddle, inhertis all the other traits
  def __init__(self, x, y):
    super().__init__(x, y)
  def draw(self):#draws bigger paddle
    pygame.draw.rect(screen,(255,255,255),(self.x,self.y, 20, 180))
  def bounce(self, pong):#it ball collides then inverse its vel so it bounces
    if pong.x in range(self.x-5, self.x+25) and pong.y in range(self.y-10,self.y+190):
      pong.xDir = -pong.xDir
class score:#creats the score baord
  def __init__(self, PLAYER1=0, PLAYER2=0):#points for eaqch side
    self.PLAYER1 = PLAYER1
    self.PLAYER2 = PLAYER2
  def draw(self):#draws the score baord in the middle
    fontName = pygame.font.match_font('arial')
    font = pygame.font.Font(fontName, 24)
    text = font.render(str(self.PLAYER1) + '  :SCORE:  ' + str(self.PLAYER2), True, (255,255,255))
    screen.blit(text, (225, 10))
class powerup:#creats a circle around the center, if the ball goes through it activeates a random powerup. 
  def __init__(self, x, y):#has x,y location and x,y velocity
    self.x = x
    self.y = y
  def draw(self):
    pygame.draw.circle(screen,(0,255,255),(self.x,self.y),15)
class setup:#creates pbjects user can click and will either put you into 1 or 2 player, has x,y location and txt attribbutes
  def __init__(self, x, y, txt):
    self.x = x
    self.y = y
    self.txt = txt
  def draw(self):#draws the setup optuions
    fontName = pygame.font.match_font('arial')
    font = pygame.font.Font(fontName, 64)
    text = font.render(self.txt, False, (255, 255, 255))
    screen.blit(text, (self.x, self.y))

#///////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////
#///////////////////////////////////////////////////////////////////////////////////////
#Run game:
plays = 0#^these set up the two game mode options, and a vairble to store what gamemode to play
while plays >= 0:
  tim = pygame.time.Clock()#sets yp time for the game
  player1 = setup(150,80,'1 PLAYER')
  player2 = setup(150,160, '2 PLAYER')
  while plays == 0:
    screen.fill((10,10,10))
    player1.draw()
    player2.draw()#creates background colour aprints two options

    for event in pygame.event.get():#if you click on either change plays to whichever gamemode the user picked, and ends this loop
      if event.type == gameGlobals.MOUSEBUTTONDOWN:
        mPos = pygame.mouse.get_pos()
        if mPos[0] in range(150, 450) and mPos[1] in range(80, 145):
          plays = 1
        if mPos[0] in range(150, 450) and mPos[1] in range(160, 225):
          plays = 2   

    tim.tick(30)#these run and update the window
    pygame.display.update()

  #///////////////////////////////////////////////////////////////////////////////////////
  #1P
  if plays == 1:#these set up ll the objects and vairbles for the game. for single player includes the ball, player1, opponetnt1 and scorebaord
    pong = ball(300,200)
    p1 = paddle(10, 150)
    o1 = paddle(570, 150)
    board = score()
    power = powerup(randint(250,350), randint(50,350))
    pwp = 0
    freeze = 0
    big = 0
    pongs = []
    pongs.append(pong)
    pPow = 0
  while plays == 1:
    screen.fill((10,10,10))#creates background

    if 0 < pong.xDir:#who hit it last
      lstht = 1
    else:
      lstht = 2

    for i in pongs:
      i.draw()
      i.move(board)
      p1.bounce(i)
      o1.bounce(i)
    p1.draw()
    o1.draw()
    if pPow == 2 and freeze >= 1:
      print('haha')
    else:
      pongy = pongs[0]
      for i in pongs:#the ai will track the nearest ball
        if i.x > pongy.x:
          pongy = i
      o1.folow(pongy.y)
    board.draw()
    #^^^these draw the ball/balls and both paddles, moves non playuer opponents, and checks if the ball should bounce, and draws scorebaord. also checks if  ai is frozen. mostly everything runs through here exdept player paddle movemnet
    
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if pPow == 1 and freeze >= 1:#if frozen you cant move
          print('haha')
        else:
          if event.key == pygame.K_UP:
            p1.yDir = -6
          if event.key == pygame.K_DOWN:
            p1.yDir = 6
          if event.key == ord('w'):
            p1.yDir = -6
          if event.key == ord('s'):
            p1.yDir = 6
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
          p1.yDir = 0
        if event.key == pygame.K_DOWN:
          p1.yDir = 0
        if event.key == ord('w'):
          p1.yDir = 0
        if event.key == ord('s'):
          p1.yDir = 0
    p1.move()
    #when player press up or w then paddle moves up, and when player presses down or s the paddle moves dowbn. the pygamegetevent gets what keys are pressed and released, so it can see if tyhe player wants to move, or when releasing a key stops the paddels movement

    if board.PLAYER1 >= 10 or board.PLAYER2 >= 10:#one player scored enough points to end the game
      plays = 3

    power.draw()#draws powerup
    for i in pongs:
      if i.x in range(power.x-25, power.x+25) and i.y in range(power.y-25,power.y+25):
        power.x, power.y = randint(250,350), randint(50,350)#if ball goes through powerup, give randompowerup
        pwp = randint(1,3)
        pPow = 0
        if pwp == 1:#freeze powerup
          print('freeze')
          freeze = 90
          if lstht == 1:
            pPow = 2
          else:
            pPow = 1
        elif pwp == 3:#bonus paddle size
          pPow = lstht
          big = 301#big paddle timer
          if pPow == 1:#one players paddle will become a bonus paddle until timer runs oout
            p1 = bonus(p1.x, p1.y)
          elif pPow == 2:
            o1 = bonus(o1.x, o1.y)
        elif pwp == 2:#multi ball
          pong = ball(300, 200)#creates a new ball instance for the game
          pongs.append(pong)
    
    if freeze >= 1:#freeze ages
      freeze -= 1
    if big == 1:#bonus ends
      p1 = paddle(p1.x, p1.y)#player paddle is converted back to normal paddle
      o1 = paddle(o1.x, o1.y)
    if big >= 1:#bonus ages
      big -= 1
      
    tim.tick(30)#these run and update the window
    pygame.display.update()

  #///////////////////////////////////////////////////////////////////////////////////////
  #2P
  if plays == 2:#these set up ll the objects and varibales for the game. for two player includes the ball, player1, player2 and scorebaord
    pong = ball(300,200)
    p1 = paddle(10, 150)
    p2 = paddle(570, 150)
    board = score()
    power = powerup(randint(250,350), randint(150,250))
    pwp = 0
    freeze = 0
    big = 0
    pongs = []
    pongs.append(pong)
    pPow = 0
  while plays == 2:
    screen.fill((10,10,10))#creates background

    if 0 < pong.xDir:#who hit it last
      lstht = 1
    else:
      lstht = 2

    for i in pongs:
      i.draw()
      i.move(board)
      p1.bounce(i)
      p2.bounce(i)
    p1.draw()
    p2.draw()
    board.draw()
    #^^^these draw the ball/balls and both paddles, moves non playuer opponents, and checks if the ball should bounce, and draws scorebaord. mostly everything runs through here exdept player paddle movemnet
    
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN:
        if pPow == 2 and freeze >= 1:
          print('haha')#player 2 is frozen, cant move
        else:
          if event.key == pygame.K_UP:
            p2.yDir = -6
          if event.key == pygame.K_DOWN:
            p2.yDir = 6
        if pPow == 1 and freeze >= 1:
          print('haha')#player 1 is frozen, cant move
        else:
          if event.key == ord('w'):
            p1.yDir = -6
          if event.key == ord('s'):
            p1.yDir = 6
      if event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
          p2.yDir = 0
        if event.key == pygame.K_DOWN:
          p2.yDir = 0
        if event.key == ord('w'):
          p1.yDir = 0
        if event.key == ord('s'):
          p1.yDir = 0
    p1.move()
    p2.move()
    #when player press up or w then paddle moves up, and when player presses down or s the paddle moves dowbn. the pygamegetevent gets what keys are pressed and released, so it can see if tyhe player wants to move, or when releasing a key stops the paddels movement
      
    if board.PLAYER1 >= 10 or board.PLAYER2 >= 10:#one player scored enough points to end the game
      plays = 3

    power.draw()#draws powerup
    for i in pongs:
      if i.x in range(power.x-25, power.x+25) and i.y in range(power.y-25,power.y+25):
        power.x, power.y = randint(250,350), randint(50,350)#if ball goes through powerup, give randompowerup
        pwp = randint(1,3)
        pPow = 0
        if pwp == 1:#freeze powerup
          print('freeze')
          freeze = 90#tiemr
          if lstht == 1:
            pPow = 2
          else:
            pPow = 1
        elif pwp == 3:#bonus paddle size
          pPow = lstht
          big = 301#tiemr
          if pPow == 1:
            p1 = bonus(p1.x, p1.y)#makes one of the players paddle into a bonus paddle until tiemr ends
          elif pPow == 2:
            p2 = bonus(p2.x, p2.y)
        elif pwp == 2:#multi ball
          pong = ball(300, 200)#creates new ball isnance for the gmae
          pongs.append(pong)

    if freeze >= 1:#freeze ages
      freeze -= 1
    if big == 1:#bonus ends
      p1 = paddle(p1.x, p1.y)#player paddle is converted back to a normal paddle thus loosing the bonus advantage
      p2 = paddle(p2.x, p2.y)
    if big >= 1:#bonus ages
      big -= 1
    
    tim.tick(30)#these run and update the window
    pygame.display.update()
  
  #///////////////////////////////////////////////////////////////////////////////////////
  #game over

  game = setup(110,100, 'GAME OVER')
  replay = setup(175,240, 'try again')
  while plays == 3:
    screen.fill((10,10,10))
    game.draw()
    replay.draw()#creates background colour aprints gameover and option to replay

    for event in pygame.event.get():#if click on replay or any up or down key then return to pick mode menu
      if event.type == gameGlobals.MOUSEBUTTONDOWN:
        mPos = pygame.mouse.get_pos()
        if mPos[0] in range(175, 415) and mPos[1] in range(240, 300):
          plays = 0
      if event.type == pygame.KEYDOWN:#any movement button will also but you into the replay menu
        if event.key == pygame.K_UP:
          plays = 0
        if event.key == pygame.K_DOWN:
          plays = 0
        if event.key == ord('w'):
          plays = 0
        if event.key == ord('s'):
          plays = 0

    tim.tick(30)#these run and update the window
    pygame.display.update()

#end///////////////////////////////////////////////////////////////////////////////////////

'''
Polymorphism
polymorhism is the ability to take on many forms. such as the paddle, if it goes through the big powerup then it chnages omto a diffrent form odf a bigger paddle, and then returns to its nsm,aller paddle version. This is an example becasue the paddle can take on either of these forms which are very simular. the bonus paddle inherits the properties and method of the normal paddle but draws and bounces diffrently. IOt is ther same vairbale, same paddle, but acts diffrent in each sernario. so when either class uses something from the other is an example of polymprhpism

inheritance
the bonus paddle size powerup has a parent and child class, so the bonus paddle inherits all the properties and mothods the nornmal paddle has, and can replace others. like the bonus paddle will bounce at a diffrent range ecasue he paddle is bigger, and it will draw diffrent becasu eit will look bigger, but the x,y,movemnet, and so on is all inherited so it is simualr but can act and look difrent in the ways I want'''
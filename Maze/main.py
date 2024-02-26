import pygame
import random, math
from path import *
from player import *
pygame.init()

screen = pygame.display.set_mode([800,600])

# Colors
WHITE = [255,255,255]
GREEN = [150,200,150]
BLACK = [0,0,0]

# fonts and clock
font = pygame.font.Font(None, 80)
font2 = pygame.font.Font(None, 50)
clock = pygame.time.Clock()

# game variables
gameOver = False
running = True
wallsize = 20
currentCell = [30,30]
recursiveCounter = 0
backtrackCounter = 1
startTime = pygame.time.get_ticks()
buttonColor = WHITE
timer = 0
f = open("HighScore.txt", "r")
HighScore = int(f.readline())
playerOffsety = 0
playerOffsetx = 0
recentKey = ""
player = Player(40,40)

# game lists
SpaceRectList = []
visitedCells = []
unvisitedCells = []
PathList = pygame.sprite.Group()

# Rendering text
EndScreen = font.render("Congrats!", True, [100,50,50])
EndScreen2 = font.render("You got the plant!", True, [100,50,50])
EndScreen3 = font.render("NEW HIGHSCORE!", True, [100,50,50])
HighScoreText = font2.render("High Score:", True, [255,255,255])
timerText = font.render("Time:", True, [255,255,255])
resetButton = font.render("Reset", True, [30,40,30])

ResetButton = pygame.Rect(600, 450, 170, 80)



# plant set up
plant = pygame.image.load("plant.png")
plant = pygame.transform.smoothscale(plant, [30,30])
Plant = pygame.sprite.Sprite()
Plant.image = plant
Plant.rect = Plant.image.get_rect()
Plant.rect.x = 40*14.5 - 40
Plant.rect.y = 40*14.5 - 40


visitedCells.append(currentCell)



# Set up initial grid
def initialGrid():
  global PathList
  for i in range(14):
    for j in range(14):
      rectx = j*40 + 30
      recty = i*40 + 30
      rectsize = wallsize
      SpaceRect = path(rectx, recty)
      PathList.add(SpaceRect)
initialGrid()

# Add paths between initial grid squares

def breakWalls(unvisitedCells):
  global currentCell
  #targetCell = random.choice(unvisitedCells)
  targetCellNum = random.randint(0,len(unvisitedCells)-1)
  targetCell = unvisitedCells[targetCellNum]
  rectx = (currentCell[0]+targetCell[0])/2
  recty = (currentCell[1]+targetCell[1])/2
  rectsize = wallsize
  SpaceRect = path(rectx, recty)
  PathList.add(SpaceRect)
  unvisitedCells.pop(targetCellNum)
  currentCell = targetCell
  visitedCells.append(currentCell)
  unvisitedCells = getUnvisitedCells(currentCell)
  while len(unvisitedCells)>0:
    unvisitedCells = getUnvisitedCells(currentCell)
    if len(unvisitedCells) > 0:
      breakWalls(unvisitedCells)
  
# Figure out which direction to move after placing a path

def getUnvisitedCells(currentCell):
  unvisitedCells = []
  if [currentCell[0], currentCell[1] - 40] not in visitedCells and currentCell[0] in range(0,590) and currentCell[1]-40 in range(0,590) :
    unvisitedCells.append([currentCell[0], currentCell[1] - 40])
  if [currentCell[0], currentCell[1] + 40] not in visitedCells and currentCell[0] in range(0,590) and currentCell[1]+40 in range(0,590) :
    unvisitedCells.append([currentCell[0], currentCell[1] + 40])
  if [currentCell[0] - 40, currentCell[1]] not in visitedCells and currentCell[0]-40 in range(0,590) and currentCell[1] in range(0,590) :
    unvisitedCells.append([currentCell[0] - 40, currentCell[1]])
  if [currentCell[0] + 40, currentCell[1]] not in visitedCells and currentCell[0] +40in range(0,590) and currentCell[1] in range(0,590) :
    unvisitedCells.append([currentCell[0] + 40, currentCell[1]])
  
  return unvisitedCells

# Main maze generating function that gets called recursively
def generateMaze():
  global recursiveCounter
  global currentCell
  global backtrackCounter
  
  if backtrackCounter > len(visitedCells) + 1:
    backtrackCounter = 1
  currentCell = visitedCells[len(visitedCells) - backtrackCounter]
  unvisitedCells = getUnvisitedCells(visitedCells[len(visitedCells) - backtrackCounter])
  while len(unvisitedCells)>0:
    if backtrackCounter > len(visitedCells) + 1:
      backtrackCounter = 1
    unvisitedCells = getUnvisitedCells(visitedCells[len(visitedCells) - backtrackCounter])
    currentCell = visitedCells[len(visitedCells) - backtrackCounter]
    if len(unvisitedCells) > 0:
      breakWalls(unvisitedCells)
    
  screen.fill([0,0,0])
  PathList.draw(screen)
  for i in range(len(SpaceRectList)):
    pygame.draw.rect(screen, WHITE, SpaceRectList[i])
  pygame.display.flip()
  if len(visitedCells) < 196:
    backtrackCounter += 1
    generateMaze()



generateMaze()

print("first maze done")




# screen that shows up after collecting plant
def endScreen():
  global HighScore
  screen.fill([10,210,110])
  screen.blit(EndScreen, [150, 200])
  screen.blit(EndScreen2, [30, 300])
  f = open("HighScore.txt", "r")
  HighScore = int(f.readline())
  
  if timer <= HighScore:
    HighScore = timer
    screen.blit(EndScreen3, [20,400])
    f = open("HighScore.txt", "w")
    f.write(str(timer))



def reset():
  global player, timer, gameOver, startTime, currentCell, backtrackCounter, PathList, unvisitedCells, visitedCells, spaceRectList
  player.rect.x = 40
  player.rect.y = 40
  timer = 0
  currentCell = [30,30]
  backtrackCounter = 1
  startTime = pygame.time.get_ticks()
  gameOver = False
  unvisitedCells = []
  visitedCells = []
  spaceRectList = []
  PathList.empty()
  visitedCells.append(currentCell)
  initialGrid()
  generateMaze()
  
  

while running:
  screen.fill([30,40,30])
  PathList.draw(screen)
  for event in pygame.event.get():
    if event.type == pygame.MOUSEBUTTONDOWN:
      if ResetButton.collidepoint(event.pos):
        reset()
    if event.type == pygame.MOUSEMOTION:
      if ResetButton.collidepoint(event.pos):
        buttonColor = GREEN
      else:
        buttonColor = WHITE
    if event.type == pygame.KEYDOWN:
      if event.key ==pygame.K_UP:
        player.changeY = -3
        player.rect.y -= 3
        playerOffsety = 3
        recentKey = "up"
      if event.key == pygame.K_DOWN:
        player.changeY = 3
        player.rect.y += 3
        playerOffsety = -3
        recentKey = "down"
      if event.key == pygame.K_LEFT:
        player.changeX = -3
        player.rect.x -= 6
        playerOffsetx = 6
        recentKey = "left"
      if event.key == pygame.K_RIGHT:
        player.changeX = 3
        player.rect.x += 6
        playerOffsetx = -6
        recentKey = "right"
    if event.type == pygame.KEYUP:
      if event.key == pygame.K_UP:
        player.changeY = 0
        player.rect.y += 3
      if event.key == pygame.K_DOWN:
        player.changeY = 0
        player.rect.y -= 3
      if event.key == pygame.K_LEFT:
        player.changeX = 0
        player.rect.x += 6
      if event.key == pygame.K_RIGHT:
        player.changeX = 0
        player.rect.x -= 6
  isColliding = pygame.sprite.spritecollide(player, PathList, False)
  
  if not isColliding:
    player.changeY = 0
    player.changeX = 0
    playerOffsetx = 0
    playerOffsety = 0
    if recentKey == "up":
      player.rect.y += 3
    if recentKey == "down":
      player.rect.y -= 3
    if recentKey == "left":
      player.rect.x += 6
    if recentKey == "right":
      player.rect.x -= 6 
  for i in range(len(SpaceRectList)):
    pygame.draw.rect(screen, WHITE, SpaceRectList[i])
  plantCollision = player.rect.colliderect(Plant.rect)
  
  if plantCollision:
    gameOver = True
    endScreen()

  # Blitting plant and player images
  screen.blit(plant, [40*14.5 - 40, 40*14.5 - 40])
  screen.blit(player.image, [player.rect.x-15, player.rect.y-15 + playerOffsety])
  player.update()
  pygame.draw.rect(screen, (200,0,0), player.rect, 2)

  # Incrementing Timer
  if not gameOver:
    timer = pygame.time.get_ticks()-startTime
  
  # Calculating timers
  minutes = math.floor(timer/60000)
  seconds = math.floor(timer/1000) -(60*minutes)
  miliseconds = timer - (minutes*60000)-(seconds*1000)

  hsminutes = math.floor(HighScore/60000)
  hsseconds = math.floor(HighScore/1000) -(60*hsminutes)
  hsmiliseconds = HighScore - (hsminutes*60000)-(hsseconds*1000)
  
  if seconds < 10:
    seconds = ("0"+str(seconds))
  
  # Timer/HighScore Text
  timerTextNum = font2.render((str(minutes)) + ":" + (str(seconds)) + ":" + (str(miliseconds)), True, [255,255,255])
  HighScoreTextNum = font2.render((str(hsminutes)) + ":" + (str(hsseconds)) + ":" + (str(hsmiliseconds)), True, [255,255,255])
  
  pygame.draw.rect(screen, buttonColor, ResetButton, 0, 7)
  
  # blitting text
  screen.blit(timerText, [600, 100])
  screen.blit(timerTextNum, [600, 150])
  screen.blit(HighScoreTextNum, [600,350])
  screen.blit(HighScoreText, [590, 300]) 
  screen.blit(resetButton, [610,460])
  
  pygame.display.flip()
  clock.tick(30)
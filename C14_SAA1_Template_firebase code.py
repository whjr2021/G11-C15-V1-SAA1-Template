import pygame
import time
from firebase import firebase

# Create a game screen and set its title 
screen = pygame.display.set_mode((600,600))
pygame.display.set_caption("Car Racing Game")

# Student Additional Activity 1- Step 1: Replace databse URL with the database created in TA1
db = firebase.FirebaseApplication('CAR RACING DATABASE LINK', None)

def db_get_data(count):
   all_player=[]
   for i in range(1,count+1):
       all_player.append(db.get("",i))
   return all_player
   
class Player:
    # Define the __init__ method with properties- self, name, xloc, yloc
    def __init__(self, num, name, xloc, yloc):
        pygame.init()
        self.name = name
        self.xloc = xloc
        self.yloc = yloc
        self.num=num
       
    def image_load(self, location, width, height):
        img = pygame.image.load(location).convert_alpha()
        img_scaled = pygame.transform.smoothscale(img,(width,height))
        return img_scaled
    
    def player_name(self, position):
        font = pygame.font.Font(None, 30)
        text = font.render(self.name, 1, (0, 255,255))
        screen.blit(text, position)
        
    def text_display(size,text,r,g,b,x,y):
        font = pygame.font.Font(None, size)
        text = font.render(text, 1, (r,g,b))
        screen.blit(text, (x,y))

    def move_up(self):
        self.yloc -= 10
        return self.yloc
    
    def move_down(self):
        self.yloc += 10
        return self.yloc
    
    def move_left(self):
        if self.xloc >= 50:                          
            self.xloc -= 10 
        return self.xloc
    
    def move_right(self):
        if self.xloc <= 320:                          
            self.xloc += 10
        return self.xloc  
    # Added time update function
    def time_update(self,time):
        self.time=time
    # function to update player data to db
    def db_update(self):
         data={"name":self.name,"x":self.xloc,"y":self.yloc,"time":self.time}
         db.put("",self.num,data)
    

player_count=db.get("","PlayerCount")
players=db_get_data(player_count)

print(player_count)
if player_count<3:
    player_count+=1
    db.put("","PlayerCount",player_count)
    carx = 140
    cary = 450
    bgy = 0
    counter = 0
    player = Player(player_count,"John", carx, cary)

    
    carryOn = True
    t1 = time.time()
    
    while carryOn:
        bgImg = pygame.image.load("road.png").convert_alpha()
        bgImg_scaled = pygame.transform.smoothscale(bgImg,(650,600))
        screen.blit(bgImg_scaled,(0,0))
        
        yellow_car = player.image_load("yellow_car.png", 230, 140)
        player.player_name((carx+90, cary+130))
       
        
        # Update player location
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                carryOn = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    cary = player.move_up()
                    bgy -= 10
                if event.key == pygame.K_DOWN:
                    cary = player.move_down()
                    bgy += 10
                if event.key==pygame.K_RIGHT:
                    carx = player.move_right()
                if event.key==pygame.K_LEFT:
                    carx = player.move_left()  
               
        
        if player.yloc <= 30:
            bgy = 0
            player.yloc = 450
            counter += 1
    
                
        t2 = time.time()
        game_time = t2-t1
        game_time = round(game_time, 2)
        '''updated time to object player here'''
        player.time_update(game_time)
        
        # Display game time elapsed
        '''using obj specific game time here'''
        Player.text_display(35,"TIME ELAPSED: " + str(player.time)+ "seconds",0, 255,255,130,15)
        
        
        # Display finish line after 5 iterations of game loop
        # Check if "counter" is equal to 5
        if counter == 2:
            # Create and draw the finish line white-colored rectangle at (x,y)=(95, 40) with width=400 and height=30
            finish_line = pygame.Rect(95,40,400,30)
            pygame.draw.rect(screen,(255,255,255),finish_line)
            Player.text_display(40, "----------FINISH----------", 255,0,0,160,45)
            pygame.display.flip()
            
            # End the game loop after displaying finish line
            pygame.time.wait(3000)
            screen.fill((0,100,200))  
            '''using obj specific game time here'''
            texty=100
            for i in players:
                Player.text_display(40, i["name"]+": "+str(round(i["time"],2))+ " seconds",255,255,255,140,texty)       
                texty+=100
                #Player.text_display(40,"Game Over, Good Luck Next Time!",255,255,255,80,250)       
                pygame.display.flip()
            pygame.time.wait(5000)
            # Break out of 'while' game loop
            break
        
        screen.blit(yellow_car, (player.xloc, player.yloc))
        player.db_update()
       #screen.blit(red_car, (red_carx, red_cary))
        #screen.blit(blue_car, (blue_carx, blue_cary))
    
        pygame.display.flip()
    pygame.quit()
else:
    print("LOBBY FULL!GAME CANNOT BE STARTED!")
    pygame.quit()
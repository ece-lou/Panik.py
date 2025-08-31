import pygame
from sys import exit
from random import randint 
from datetime import datetime
import datetime
import random
import time
from threading import Thread
import pygame.mixer
import string
import os
import shutil

def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surface = test_font.render(f" Time: {current_time}", False, "White")
    score_rectangle = score_surface.get_rect(center = (650,50))
    buffer.blit(score_surface, score_rectangle)
    
    return current_time

def obstacle_movement(obstacle_list, speed):
    if obstacle_list: 
        for obstacle_rect in obstacle_list:
            obstacle_rect.x -= speed

            if obstacle_rect.bottom == 300:
                screen.blit(bebek_surface,obstacle_rect)
            else:
                screen.blit(fly_surface,obstacle_rect)

        obstacle_list = [obstacle for obstacle in obstacle_list if obstacle.x > -100]    

        return obstacle_list
    
    else: 
        return []

blink_logs = []

def collisions(player,obstacles):

    if obstacles:
        for obstacle_rect in obstacles:
            if player.colliderect(obstacle_rect):
                return False
    return True

def blink_data():
    global thread_running
    print("----- Blink Counter -----")
    last_print_time = time.time()  
    while thread_running:  
        current_time = time.time()
        if current_time - last_print_time >= 10:  
            blink_count = random.randint(8, 13)  
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            log_line = f"Time: {timestamp}, Blink Count: {blink_count}"

            print(log_line, flush=True)
            blink_logs.append(log_line)

            last_print_time = current_time  
        time.sleep(1)

def invert_colors(surface):    
    array = pygame.surfarray.array3d(surface)  
    inverted_array = 255 - array  
    pygame.surfarray.blit_array(surface, inverted_array)  

def increase_music_intensity():
    current_volume = pygame.mixer.music.get_volume() 
    new_volume = min(current_volume + 0.3, 1.0)  
    pygame.mixer.music.set_volume(new_volume)  

def show_logo_intro():
    
    logo_image = pygame.image.load("Desktop/Panikfile/Graphix/rodentgiris.jpg").convert_alpha()
    logo_image = pygame.transform.scale(logo_image, (800, 400))
    logo_image = pygame.transform.rotozoom(logo_image,1,1)
    
    for alpha in range(0, 256, 3):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

        screen.fill((0, 0, 0))
        logo_image.set_alpha(alpha)
        screen.blit(logo_image, (0, 0))
        pygame.display.update()
        pygame.time.delay(20)

    pygame.time.delay(1000)

    screen.fill((0, 0, 0))

   
    gothic_font = pygame.font.Font("Desktop/Panikfile/Fontx/Gothicpixels.ttf", 28)

    line1 = gothic_font.render("Panik.py by Grim Rodent Studios", True, "#F2EBE3")
    line2 = gothic_font.render("Music by s4k4t4t", True, "#F2EBE3")
    line3 = gothic_font.render("Designed by Ece Altas", True, "#F2EBE3")

    screen.blit(line1, line1.get_rect(center=(400, 140)))
    screen.blit(line2, line2.get_rect(center=(400, 190)))
    screen.blit(line3, line3.get_rect(center=(400, 240)))

    pygame.display.update()
    pygame.time.delay(3000)  

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    waiting = False

        screen.fill((139, 0, 0))  #deep red
        press_font = pygame.font.Font("Desktop/Panikfile/Fontx/Gothicpixels.ttf", 32)
        message = press_font.render("Press SPACE to Start", True, "#F2EBE3")
        screen.blit(message, message.get_rect(center=(400, 200)))

        pygame.display.update()
        pygame.time.delay(50)

pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800,400))
pygame.display.set_caption("Panik.py")
clock = pygame.time.Clock()
test_font = pygame.font.Font("Desktop/Panikfile/Fontx/Gothicpixels.ttf", 30) 

pygame.mixer.music.load("Desktop/Panikfile/Musix/muzik1x.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.5) 

show_logo_intro()

giant_enemy_music = "Desktop/Panikfile/Musix/kocamanx.mp3"
giant_enemy_background = pygame.image.load("Desktop/Panikfile/Graphix/gigax.png").convert()
giant_enemy_phase = False

game_active = False
start_time = 0
score = 0
thread_running = True
blink_data_printed = False
obstacle_speed = 6
screen_flipped = False
colors_inverted = False
current_frequency = 44100
BSOD = False
final_screen_active = False

#DEATH COUNTER
death_counter = 0

test_surface = pygame.Surface((100,200)) 
sky_surface = pygame.image.load('Desktop/Panikfile/Graphix/yenix.png').convert()
ground_surface = pygame.image.load("Desktop/Panikfile/Graphix/ground2x.png").convert()

#OBSTACLES
bebek_surface = pygame.image.load("Desktop/Panikfile/Enemix/Bebek2x.png").convert_alpha()

fly_surface = pygame.image.load("Desktop/Panikfile/Enemix/Flyx.png").convert_alpha()
fly_surface = pygame.transform.rotozoom(fly_surface,0,3/2)

#FAKE POPUP
fake_popup_surface = pygame.image.load("Desktop/Panikfile/Graphix/korkux.png").convert_alpha()
fake_popup_surface = pygame.transform.rotozoom(fake_popup_surface,0,1.1)
fake_popup_rectangle = fake_popup_surface.get_rect(center = (400,200))

obstacle_rect_list = []

player_surface = pygame.image.load("Desktop/Panikfile/Playerx/kedi.png").convert_alpha()
player_rectangle = player_surface.get_rect(midbottom = (80,300)) 
player_gravity = 0
can_double_jump = True

#INTRO SCREEN
bebek_giris = pygame.image.load("Desktop/Panikfile/Enemix/Bebekx.png").convert_alpha()
bebek_giris = pygame.transform.rotozoom(bebek_giris,0,4/3) 
bebek_giris_rectangle = bebek_giris.get_rect(center = (400,200))

son = pygame.image.load("Desktop/Panikfile/Enemix/Sonx.png").convert_alpha()
son = pygame.transform.rotozoom(son,0,2)
son_rectangle = son.get_rect(center = (400,200))

game_name = test_font.render("I am the darkness of your soul", False , "#F2EBE3")
game_name_rect = game_name.get_rect(center = (400,80))
game_name2 = test_font.render("Failure !", False , "#F2EBE3")
game_name_rect2 = game_name2.get_rect(center = (400,80))

giant_enemy_surface = pygame.image.load("Desktop/Panikfile/Enemix/Flyx.png").convert_alpha()
giant_enemy_surface = pygame.transform.scale(giant_enemy_surface,(400, 200))  
giant_enemy_rect = giant_enemy_surface.get_rect(midbottom=(900, 300))  

game_message = test_font.render("Beat me if you can!",False,"#F2EBE3")
game_message_rect = game_message.get_rect(center = (400,320))

#TIMER
obstacle_timer = pygame.USEREVENT + 1
pygame.time.set_timer(obstacle_timer,1200) 

while True:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            thread_running = False
            exit() 

        if game_active:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if player_rectangle.collidepoint(event.pos) and player_rectangle.bottom >= 300:
                    player_gravity = -20
                    
                    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and player_rectangle.bottom >= 300:
                    player_gravity = -20
                    can_double_jump = True
                    
                elif can_double_jump: 
                    player_gravity = -20
                    can_double_jump = False
                                           
        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
            
                start_time = int(pygame.time.get_ticks() / 1000)

        if event.type == obstacle_timer and game_active:
            for enemy in range(2):
                if randint(0,2):
                    obstacle_rect_list.append(bebek_surface.get_rect(bottomright = (randint(900,1100),300)))
                else:
                     obstacle_rect_list.append(fly_surface.get_rect(bottomright = (randint(900,1100),150)))

    buffer = pygame.Surface((800,400))

    if game_active:

        if giant_enemy_phase:
            buffer.blit(giant_enemy_background, (0, 0))

        else: 
            buffer.blit(sky_surface, (0, 0))
        
        buffer.blit(ground_surface, (0, 300))

        score = display_score()

        #PLAYER
        player_gravity += 1
        player_rectangle.y += player_gravity

        if player_rectangle.bottom >= 300: 
            player_rectangle.bottom = 300
            can_double_jump = True


        buffer.blit(player_surface, player_rectangle)
        

        if giant_enemy_phase: 
            giant_enemy_rect.x -= obstacle_speed
            if giant_enemy_rect.x < -400:  
                giant_enemy_rect.midbottom = (900, 300)  

            buffer.blit(giant_enemy_surface, giant_enemy_rect)
            
            
            if giant_enemy_rect.colliderect(player_rectangle):
                game_active = False
                BSOD = True
                pygame.display.set_mode((0,0), pygame.FULLSCREEN)

        else:

        #OBSTACLE MOVEMENT
            obstacle_rect_list = obstacle_movement(obstacle_rect_list, obstacle_speed)
            for obstacle_rect in obstacle_rect_list:
                if obstacle_rect.bottom == 300:
                    buffer.blit(bebek_surface, obstacle_rect)
                else:
                    buffer.blit(fly_surface, obstacle_rect)

        # COLLISION
        if not collisions(player_rectangle,obstacle_rect_list):
            game_active = False
            death_counter +=1

    else:
        if BSOD:

            lucida_font = pygame.font.Font("Desktop/Panikfile/Fontx/LucidaGrande.ttc", 20)
            game_font = test_font 
            buffer = pygame.Surface((pygame.display.Info().current_w, pygame.display.Info().current_h))
            buffer.fill((0, 0, 255))  
            
            message_lines = [
                "Congratulations, you've reached the end of the game. But before you go, there's something you should know.",
                "",
                "This was not just a game, we've been watching you.",
                "",
                "Not in a way that you’d notice, but we've been... monitoring.",
                "Your every blink... every movement. Your camera was active the whole time.",
                "While dowloading 'the game' you allowed us access to everything :) ",
                "Reminder to be careful what you have downloaded from the internet",
                "You willingly allowed it. You consented." 
                "Access to your folders, your location, your desktop!",
                "",
                "Ps. Check your desktop to find two presents! One of them gives the exact times of your blinks during the game.",
                "How exciting!",
                ".",
                "What files did we look at? What information did we find? That’s a question you might want to think about...",
                "",
                "This 'might' have been a malicious file disguied as an innocent game. One that is more than just code.", 
                "Even if you think the game is over, the real consequences might just be beginning.",
                "",
                "Exit the game now with ESC, if you dare.",
                "",
            
            ] 

            x_start = 50  
            y_start = 100  
            line_spacing = 30  
            
            for line in message_lines:
                rendered_line = lucida_font.render(line, True, "White")
                buffer.blit(rendered_line, (x_start, y_start))
                y_start += line_spacing

            screen.blit(buffer, (0, 0))
            

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        BSOD = False
                        final_screen_active = True
                        pygame.display.update()
                        

                elif event.type == pygame.QUIT:
                    pygame.quit()
                    thread_running = False
                    exit()

        elif final_screen_active:
            pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
            buffer = pygame.Surface((pygame.display.Info().current_w, pygame.display.Info().current_h))
            buffer.fill((0, 0, 0))  

            final_message_text = "Do not Forget:  Exiting does not mean escaping."
            final_message = lucida_font.render(final_message_text, True, "White")
                        
        
            final_message_rect = final_message.get_rect(
                center=(pygame.display.Info().current_w // 2, pygame.display.Info().current_h // 2)
            )
            buffer.blit(final_message, final_message_rect)
            
            screen.blit(buffer, (0, 0))
            pygame.display.update()
            
            pygame.time.wait(3000)

            desktop = os.path.join(os.path.expanduser("~"), "Desktop")
            
            file_path = os.path.join(desktop, "blink_data.txt")
            with open(file_path, "w") as f:
                f.write("Camera Access Granted \n Real Time Blink Data:\n\n")
                for entry in blink_logs:
                    f.write(entry + "\n")  

            source_image = "Desktop/Panikfile/Graphix/grimgoodbye.jpg"
            target_image = os.path.join(desktop, "grimgoodbye.jpg")
            shutil.copyfile(source_image, target_image)

            pygame.quit()
            thread_running = False
            exit()
                

        else:    
            buffer.fill((139, 0, 0))
            buffer.blit(bebek_giris, bebek_giris_rectangle)
            obstacle_rect_list.clear()
            player_rectangle.midbottom = (80,300)
            player_gravity = 0

            score_message = test_font.render(f"Time spent on earth: {score}",False,"#F2EBE3")
            score_message_rect = score_message.get_rect(center = (400,330))

            if score == 0:
                buffer.blit(game_message, game_message_rect)
                buffer.blit(game_name, game_name_rect)
            else:
                buffer.blit(score_message, score_message_rect)
                buffer.blit(game_name2, game_name_rect2)

#DEATH COUNTER

            if death_counter == 1:
                buffer.blit(fake_popup_surface, fake_popup_rectangle)
                
            
            elif death_counter == 2 and not blink_data_printed:  
                obstacle_speed = 10 
                blink_data_printed = True
                blink_thread = Thread(target=blink_data, daemon=True)
                blink_thread.start()
                increase_music_intensity()

            elif death_counter == 3:
                obstacle_speed = 15
                increase_music_intensity()

            elif death_counter == 4 and not screen_flipped:
                obstacle_speed = 9
                screen_flipped = True
                increase_music_intensity()
            
            elif death_counter == 5:
                obstacle_speed = 20
                increase_music_intensity()
            
            elif death_counter == 6 and not colors_inverted:
                screen_flipped = False
                colors_inverted = True
                increase_music_intensity()
            
            elif death_counter == 7:
                colors_inverted = False
                obstacle_speed = 15
                increase_music_intensity()
            
            elif death_counter == 8:
                obstacle_speed = 20

                flicker = True
                flicker_start_time = pygame.time.get_ticks()  
                flicker_duration = 3000  
                flicker_font = pygame.font.Font("Desktop/Panikfile/Fontx/GothicPixels.ttf", 40) 

                buffer.fill((139, 0, 0))  
                buffer.blit(son, son_rectangle)
                obstacle_rect_list.clear()
                player_rectangle.midbottom = (80, 300)
                player_gravity = 0

                if pygame.time.get_ticks() - flicker_start_time < flicker_duration:
                    if random.randint(0, 10) > 7:  
                        flicker = not flicker

                    if flicker:
                        flicker_text = "The darkness awaits you."
                        rendered_text = flicker_font.render(flicker_text, True, (255, 0, 0))
                        flicker_text_rect = rendered_text.get_rect(center=(400, 80))
                        buffer.blit(rendered_text, flicker_text_rect)
                else:
                    
                    score_message = test_font.render(f"Time spent on earth: {score}", False, "#F2EBE3")
                    score_message_rect = score_message.get_rect(center=(400, 330))
                    buffer.blit(score_message, score_message_rect)
                      
            elif death_counter == 9 and not giant_enemy_phase:
                pygame.mixer.music.fadeout(2500)

                glitch_start_time = pygame.time.get_ticks()  
                glitch_duration = 3000  
                glitch_text = "Your time on Earth has ended."
                glitch_font = pygame.font.Font("Desktop/Panikfile/Fontx/GothicPixels.ttf",50) 
                color = (255, 0, 0)

                while pygame.time.get_ticks() - glitch_start_time < glitch_duration:
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            pygame.quit()
                            thread_running = False
                            exit()

                    buffer.fill((139, 0, 0))  
                    buffer.blit(bebek_giris, bebek_giris_rectangle)
                    player_rectangle.midbottom = (80, 300)
                    player_gravity = 0

                    glitch_display = ''.join(
                        random.choice(string.ascii_letters + " ") if random.random() > 0.9 else c
                        for c in glitch_text
                    )
                    rendered_text = glitch_font.render(glitch_display, True, color)
                    rendered_text_rect = rendered_text.get_rect(center=(400, 200))
                    buffer.blit(rendered_text, rendered_text_rect)

                    screen.blit(buffer, (0, 0))
                    pygame.display.flip()
                    clock.tick(15)
                 
                pygame.mixer.music.stop()
                giant_enemy_phase = True
                obstacle_rect_list.clear()
                giant_enemy_rect.midbottom = (900, 300)
                obstacle_speed = 2 

                pygame.mixer.music.load(giant_enemy_music)
                pygame.mixer.music.play(-1) 
                pygame.mixer.music.set_volume(0.7)
                        

    if screen_flipped:
        rotated_buffer = pygame.transform.rotate(buffer, 180)
        if colors_inverted:
            invert_colors(rotated_buffer)  
        screen.blit(rotated_buffer, (0, 0))
    else:
        if colors_inverted:
            invert_colors(buffer) 
        screen.blit(buffer, (0, 0))

    if BSOD and event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
        BSOD = False  
        game_active = False
        death_counter = 0  

        obstacle_speed = 6  
        start_time = 0
        pygame.display.set_mode((800, 400))  


    pygame.display.update()
    clock.tick(60) #frame rate 

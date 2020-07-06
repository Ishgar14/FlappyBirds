import random
import time
import pygame
pygame.init()
 
WIDTH  = 1000
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
FPS    = 60
clock  = pygame.time.Clock()


isAlive   = True
Paused    = False
Debug     = False
player    = pygame.Rect(10, HEIGHT // 2, 40, 40)
offx      = player.x
score     = 0
gravity   = 2
pipes     = []
next_pipe = None
hole_size = 200
pipe_time = time.time()
pipe_speed = 60

WHITE   = (255, 255, 255)
BLACK   = (0  ,   0,   0)
TEAL    = (0  , 180, 220)
GREEN   = (50 , 225, 100)
VIOLET  = (160,  30, 200)

def abs(x: int):
    return x if x >= 0 else -x

def display_score():
    font   = pygame.font.SysFont(None, 20)
    msg = font.render("Score: %d" % score, True, WHITE)
    screen.blit(msg, (0, 10))


def display_msg(message: str, x: int, y: int, size: int = 20, colour: tuple = WHITE):
    font = pygame.font.SysFont(None, size)
    msg  = font.render(message, True, colour)
    screen.blit(message, (x,y))


def spawn_pipes():
    global next_pipe
    x,y = random.randrange(WIDTH // 8, WIDTH // 2), random.randint(HEIGHT // 10, HEIGHT // 1.5)
    pipe_width = 40

    if len(pipes) > 0:
        x = pipes[-1][0].x + random.randint(player.width + 50, player.width + 150)
        y = abs(pipes[-1][0].y + random.randint(-player.y // 2, player.y))

    up_obstacle   = pygame.Rect(x, 0, pipe_width, y)
    down_obstacle = pygame.Rect(x, y + hole_size, pipe_width, HEIGHT)
    pipe = (up_obstacle, down_obstacle)
    pipes.append(pipe)

    if next_pipe is None: next_pipe = pipes[0]
    if Debug: print(next_pipe)


def main():
    global isAlive, Paused, Debug, score, offx, next_pipe, pipe_time

    screen.fill(BLACK)
    display_score()

    if pygame.event.poll().type == pygame.QUIT:
        print("Exiting...")
        pygame.quit()
        exit(0)

    pygame.draw.rect(screen, VIOLET, player)

    # movement control
    keys = pygame.key.get_pressed()
    x, y = player.x, player.y
    if keys[pygame.K_w]:
        y -= 10
    if keys[pygame.K_a]:
        x -= 4
    if keys[pygame.K_d]:
        x += 4
    if keys[pygame.K_s]:
        y += 2
    y += gravity

    # Press P for pause
    if keys[pygame.K_p]:
        Paused = not Paused
        print("Paused = ", Paused)
        if Paused: return
        x = player.x
        y = player.y
    player.x, player.y = x, y

    # Press G to enable debugging
    if keys[pygame.K_g]:
        Debug = not Debug
        if Debug:
            print("Enabled Debugging...")
        else:
            print("Disabled Debugging...")

    # ensure player is within screen
    if player.y < 0:
        player.y = 0
    if player.x < 0:
        player.x = 0
    
    if player.y + player.height > HEIGHT:
        player.y = HEIGHT - player.height

    while len(pipes) < 6 or next_pipe is None:
            spawn_pipes()

    for pipe in pipes:
        if pipe[0].x < player.x:
            next_pipe = pipe
        else:
            break

    if len(pipes) > 0 and player.x + player.width > next_pipe[0].x:
        if player.y > next_pipe[0].y + next_pipe[0].height and player.y < next_pipe[1].y:
            score += 1
            # print(score)
            spawn_pipes()
            current_index = pipes.index(next_pipe)
            del pipes[current_index]
            next_pipe = pipes[current_index]
        else:
            isAlive = False
            print("You collided with a pipe!")
            return
        next_pipe = None


    # remove pipes out of screen
    for pipe in pipes:
        if pipe[0].x + pipe[0].width < 0:
            if Debug:
                print("number of pipes = ", len(pipes))
                print("Removed pipe -> ", pipe[0], " ", pipe[1])
            pipes.remove(pipe)

    cooldown_done = time.time() - pipe_time > 1 / pipe_speed #0.05
    for pipe in pipes:
        up   = pipe[0]
        down = pipe[1]
        if cooldown_done:
            up.x   -= offx
            down.x -= offx

        pygame.draw.rect(screen, GREEN, up)
        pygame.draw.rect(screen, GREEN, down)

    if cooldown_done:
        pipe_time = time.time()


    clock.tick(FPS)
    pygame.display.flip()

if __name__ == "__main__":
    while isAlive:
        main()
    print("Your score was %d" % score)

import glfw
from OpenGL.GL import *
import math
import random

# Names and roll numbers of the group members:
# Annoor Sharara Akhand (Roll 09)
# Md. Sifat Hossain (Roll 17)


# Operation principles:
# This program creates a Ping Pong game where two players control paddles on either side of the screen.
# The objective is to hit the ball with the paddle to send it to the opponent's side. The player scores 
# a point if the opponent fails to return the ball. The game ends based on certain conditions such as 
# reaching a score limit.

# Paddle properties
paddle_width, paddle_height = 20, 150 
PADDLE_SPEED = 35

# Ball properties
ball_radius = 20
ball_speed = 2
ball_dx, ball_dy = ball_speed, ball_speed

# Window dimensions
WIDTH, HEIGHT = 800, 600

# Paddle positions
left_paddle_y = 0
right_paddle_y = 0

# Other game state variables
vertical_direction = 0
horizontal_direction = 0
game_started = False
last_key_press_time = 0

def bresenham_line(x0, y0, x1, y1):
    # Bresenham's line drawing algorithm
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while x0 != x1 or y0 != y1:
        glVertex2f(x0, y0)
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

def draw_lines():
    # Draw the center line
    glColor3f(1, 1, 1)  # White color for the axis
    glBegin(GL_POINTS)
    bresenham_line(0, -HEIGHT, 0, HEIGHT)
    glEnd()

def draw_circle_using_midpoint(x0, y0, radius):
    # Midpoint circle drawing algorithm
    x = radius
    y = 0
    p = 1 - radius  # Initial value of decision parameter

    glBegin(GL_POINTS)
    def plot_circle_points(x, y):
        glVertex2f(x0 + x, y0 + y)
        glVertex2f(x0 - x, y0 + y)
        glVertex2f(x0 + x, y0 - y)
        glVertex2f(x0 - x, y0 - y)
        glVertex2f(x0 + y, y0 + x)
        glVertex2f(x0 - y, y0 + x)
        glVertex2f(x0 + y, y0 - x)
        glVertex2f(x0 - y, y0 - x)

    plot_circle_points(x, y)

    while x > y:
        y += 1
        if p <= 0:
            p += 2 * y + 1
        else:
            x -= 1
            p += 2 * (y - x) + 1
        plot_circle_points(x, y)
    glEnd()

def draw_paddle(paddle_points):
    # Draw paddle using points and lines
    glBegin(GL_POINTS)
    start_y = paddle_points[0][1]
    end_y = paddle_points[1][1]
    start_x = paddle_points[0][0]
    end_x = paddle_points[3][0]
    
    y = start_y
    while y <= end_y:
        zone = get_zone(start_x, y, end_x, y)    
        x0, y0 = allZone_to_3(zone, start_x, y)      
        x1, y1 = allZone_to_3(zone, end_x, y)      

        glColor3ub(255,255,0)  # Yellow color for paddles

        draw_line_3(x0, y0, x1, y1, zone)
        y += 1
    
    glEnd()

def get_zone(x0, y0, x1, y1):
    # Determine the zone for Bresenham's algorithm
    dx = x1 - x0
    dy = y1 - y0

    if dx >= 0 and dy >= 0:
        if dx > dy:
            return 0
        return 1
    elif dx >= 0 and dy < 0:
        if dx > abs(dy):
            return 7
        return 6
    elif dx < 0 and dy >= 0:
        if abs(dx) > dy:
            return 3
        return 2
    else:
        if abs(dx) > abs(dy):
            return 4
        return 5

def return_back(zone, x, y):
    # Convert from zone 3 to the original zone
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x 
    elif zone == 3:
        return -x, y 
    elif zone == 4:
        return -x, -y 
    elif zone == 5:
        return -y, -x 
    elif zone == 6:
        return -y, x 
    else:
        return x, -y
    
def allZone_to_3(zone, x, y):
    # Convert from any zone to zone 3
    if zone == 0:
        return x, y
    elif zone == 1:
        return y, x
    elif zone == 2:
        return y, -x 
    elif zone == 3:
        return -x, y 
    elif zone == 4:
        return -x, -y 
    elif zone == 5:
        return -y, -x 
    elif zone == 6:
        return -y, x 
    else:
        return x, -y

def draw_pixel(x, y, zone):
    # Draw a pixel in the original zone
    x, y = return_back(zone, x, y)
    glVertex2f(x, y)

def draw_line_3(x0, y0, x1, y1, zone):
    # Draw a line in zone 3
    dx = x1 - x0
    dy = y1 - y0
    x = x0
    y = y0
    d = 2 * dy - dx
    del_e = 2 * dy
    del_ne = 2 * (dy - dx)
    draw_pixel(x, y, zone)
    while x < x1:
        if d <= 0:
            d += del_e
            x += 1
        else:
            d += del_ne
            x += 1
            y += 1
        draw_pixel(x, y, zone)

def draw_ball(x_center, y_center, num_circles, max_radius):
    # Draw the ball using midpoint circle algorithm
    glColor3f(1, 0, 0)  # Red color for the ball
    for i in range(1, num_circles + 1):
        radius = max_radius * (i / num_circles)
        draw_circle_using_midpoint(x_center, y_center, radius)

def key_callback(window, key, scancode, action, mods):
    # Handle key press events for paddle movement and game control
    global left_paddle_y, right_paddle_y, ball_x, ball_y, vertical_direction, horizontal_direction, game_started, last_key_press_time
    
    if action == glfw.PRESS or action == glfw.REPEAT:
        if key == glfw.KEY_W and left_paddle_y + paddle_height / 2 + PADDLE_SPEED <= HEIGHT / 2:
            left_paddle_y += PADDLE_SPEED
        elif key == glfw.KEY_S and left_paddle_y - paddle_height / 2 - PADDLE_SPEED >= -HEIGHT / 2:
            left_paddle_y -= PADDLE_SPEED
        elif key == glfw.KEY_UP and right_paddle_y + paddle_height / 2 + PADDLE_SPEED <= HEIGHT / 2:
            right_paddle_y += PADDLE_SPEED
        elif key == glfw.KEY_DOWN and right_paddle_y - paddle_height / 2 - PADDLE_SPEED >= -HEIGHT / 2:
            right_paddle_y -= PADDLE_SPEED
        elif key == glfw.KEY_ESCAPE:
            glfw.set_window_should_close(window, True)
    
    if key == glfw.KEY_ENTER and action == glfw.PRESS:
        if not game_started:
            ball_x = 0
            ball_y = 0
            vertical_direction = 1
            horizontal_direction = 1
            game_started = True

def reset_ball(scored_left):
    # Reset the ball to the center and set its direction
    global ball_x, ball_y, vertical_direction, horizontal_direction
    ball_x = 0
    ball_y = 0
    vertical_direction = 1 if random.choice([True, False]) else -1
    horizontal_direction = 1 if scored_left else -1

def main():
    # Main function to initialize the game and run the main loop
    global left_paddle_y, right_paddle_y, ball_x, ball_y, vertical_direction, horizontal_direction, game_started, last_key_press_time
    global WIDTH, HEIGHT
    
    if not glfw.init():
        return

    monitor = glfw.get_primary_monitor()
    video_mode = glfw.get_video_mode(monitor)
    WIDTH = video_mode.size.width
    HEIGHT = video_mode.size.height
    
    window = glfw.create_window(WIDTH, HEIGHT, "Ping Pong Game", monitor, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glOrtho(-WIDTH / 2, WIDTH / 2, -HEIGHT / 2, HEIGHT / 2, -1, 1)

    glfw.set_key_callback(window, key_callback)

    left_paddle_y = 0
    right_paddle_y = 0
    paddle_width = 20
    paddle_height = 150  # Increased paddle height
    ball_x = 0
    ball_y = 50
    ball_radius = 30
    speed = 4
    ball_number = 70
    vertical_direction = 1
    horizontal_direction = 1
    game_started = True

    left_score = 0
    right_score = 0

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT)
        glColor3f(1, 1, 1)

        draw_lines()
        
        draw_paddle([(-WIDTH / 2 + 50, left_paddle_y - paddle_height / 2), 
                     (-WIDTH / 2 + 50, left_paddle_y + paddle_height / 2), 
                     (-WIDTH / 2 + 50 + paddle_width, left_paddle_y + paddle_height / 2), 
                     (-WIDTH / 2 + 50 + paddle_width, left_paddle_y - paddle_height / 2)])  # Left paddle (yellow)

        draw_paddle([(WIDTH / 2 - 50 - paddle_width, right_paddle_y - paddle_height / 2), 
                     (WIDTH / 2 - 50 - paddle_width, right_paddle_y + paddle_height / 2), 
                     (WIDTH / 2 - 50, right_paddle_y + paddle_height / 2), 
                     (WIDTH / 2 - 50, right_paddle_y - paddle_height / 2)])  # Right paddle (yellow)
        
        if game_started:
            draw_ball(ball_x, ball_y, ball_number, ball_radius)
            
            ball_x += speed * horizontal_direction
            ball_y += speed * vertical_direction

            if ball_y + ball_radius > HEIGHT / 2 or ball_y - ball_radius < -HEIGHT / 2:
                vertical_direction *= -1

            # Handle collision with left paddle
            if ball_x - ball_radius < -WIDTH / 2 + 50 + paddle_width and \
               left_paddle_y - paddle_height / 2 < ball_y < left_paddle_y + paddle_height / 2:
                horizontal_direction *= -1
                ball_x = -WIDTH / 2 + 50 + paddle_width + ball_radius  # Adjust ball position to avoid sticking

            # Handle collision with right paddle
            if ball_x + ball_radius > WIDTH / 2 - 50 - paddle_width and \
               right_paddle_y - paddle_height / 2 < ball_y < right_paddle_y + paddle_height / 2:
                horizontal_direction *= -1
                ball_x = WIDTH / 2 - 50 - paddle_width - ball_radius  # Adjust ball position to avoid sticking

            # Check if ball went out of bounds (restart game and update score)
            if ball_x - ball_radius < -WIDTH / 2:
                right_score += 1
                print(f"Score: Left - {left_score}, Right - {right_score}")
                reset_ball(scored_left=False)

            if ball_x + ball_radius > WIDTH / 2:
                left_score += 1
                print(f"Score: Left - {left_score}, Right - {right_score}")
                reset_ball(scored_left=True)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()


# Ping Pong Game

This project is a recreation of the classic Ping Pong game using OpenGL and GLFW. The game is designed as part of the Computer Graphics Lab course (CSE 4169) at the University of Dhaka. 

## Team Members

- **Md. Sifat Hossain** (Roll 17)
  - Email: sifatb910@gmail.com
- **Annoor Sharara Akhand** (Roll 09)
  - Email: sharara99@gmail.com

## Objective

The objective of this project is to create a functional Ping Pong game where two players can control paddles on either side of the screen to hit a ball back and forth. The game is played using keyboard inputs.

## Features

1. **Input Handling**: 
   - Player 1 controls their paddle using the `W` (up) and `S` (down) keys.
   - Player 2 controls their paddle using the arrow keys (Up and Down).

2. **Game Logic**: 
   - Both paddles move according to the corresponding key presses.
   - The ball moves and bounces off the paddles and the screen edges.

3. **Collision Detection**: 
   - Accurate collision detection between the ball and the paddles.
   - The ball bounces back when it hits a paddle or the top/bottom screen edge.

4. **Scoring**: 
   - A point is awarded to the opponent if a player fails to hit the ball back.
   - Scores are printed in the terminal.

5. **Game Over and Restart**: 
   - The game continues indefinitely until manually stopped.
   - The game can be restarted by pressing the `Enter` key.

## Algorithms Used

- **Line Drawing**: Bresenham's line drawing algorithm.
- **Circle Drawing**: Midpoint circle drawing algorithm.
- **Collision Detection**: Bounding box collision detection for paddles and ball.
- **Input Handling**: GLFW key callbacks for paddle movement.

## How to Run

1. Ensure you have the necessary dependencies installed:
   - GLFW
   - PyOpenGL

   You can install them using pip:
   ```sh
   pip install glfw PyOpenGL
2. Clone the repository:
    git clone https://github.com/yourusername/ping-pong-game.git
    cd ping-pong-game
3. Run the game:
    python ping_pong_game.py

    
Controls

    Player 1: W (up), S (down)
    Player 2: Arrow keys (Up, Down)
    Start Game: Enter
    Exit Game: Escape

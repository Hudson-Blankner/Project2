import pygame
import sys
import random

# ============================================================
#                  ROCK PAPER SCISSORS
# ============================================================

def play_rps():
    print("\n--- ROCK PAPER SCISSORS ---")
    print("Type rock, paper, or scissors. Type 'quit' to exit.\n")

    choices = ["rock", "paper", "scissors"]
    player_history = []

    def ai_choice():
        if len(player_history) < 3:
            return random.choice(choices)
        last = player_history[-1]
        if last == "rock":
            return "paper"      # AI counters you
        elif last == "paper":
            return "scissors"
        else:
            return "rock"

    while True:
        player = input("Your choice: ").lower()
        if player == "quit":
            return
        if player not in choices:
            print("Invalid choice.")
            continue
        
        comp = ai_choice()
        player_history.append(player)

        print(f"AI picks: {comp}")

        if player == comp:
            print("Tie!")
        elif (
            (player == "rock" and comp == "scissors") or
            (player == "paper" and comp == "rock") or
            (player == "scissors" and comp == "paper")
        ):
            print("You win!")
        else:
            print("AI wins!")


# ============================================================
#                         TIC TAC TOE
# ============================================================

def print_board(board):
    print("\n")
    for i in range(0, 9, 3):
        print(board[i], board[i+1], board[i+2])
    print("\n")

def check_winner(board, mark):
    # all winning combos
    wins = [
        (0,1,2), (3,4,5), (6,7,8),
        (0,3,6), (1,4,7), (2,5,8),
        (0,4,8), (2,4,6)
    ]
    return any(board[a] == board[b] == board[c] == mark for a,b,c in wins)

def ai_move(board):
    # 1) AI tries to win
    for i in range(9):
        if board[i] == "-":
            board[i] = "O"
            if check_winner(board, "O"):
                return
            board[i] = "-"

    # 2) AI blocks X
    for i in range(9):
        if board[i] == "-":
            board[i] = "X"
            if check_winner(board, "X"):
                board[i] = "O"
                return
            board[i] = "-"

    # 3) Take center
    if board[4] == "-":
        board[4] = "O"
        return

    # 4) Otherwise random
    open_moves = [i for i, v in enumerate(board) if v == "-"]
    board[random.choice(open_moves)] = "O"


def play_ttt():
    board = ["-"] * 9

    print("\n--- TIC TAC TOE ---")
    print("You are X. AI is O.\n")

    while True:
        print_board(board)

        # Player turn
        move = input("Pick a spot (1-9): ")
        if not move.isdigit() or not (1 <= int(move) <= 9):
            print("Invalid move.")
            continue
        move = int(move) - 1

        if board[move] != "-":
            print("Spot taken.")
            continue

        board[move] = "X"

        # Player wins?
        if check_winner(board, "X"):
            print_board(board)
            print("You win!")
            return

        # Board full?
        if "-" not in board:
            print_board(board)
            print("Tie game.")
            return

        # AI turn
        ai_move(board)

        # AI wins?
        if check_winner(board, "O"):
            print_board(board)
            print("AI wins!")
            return

        if "-" not in board:
            print_board(board)
            print("Tie game.")
            return



# ============================================================
#                           PONG (AI)
# ============================================================

# Initialize pygame only once
pygame.init()

WIDTH, HEIGHT = 800, 600
WHITE = (255,255,255)
BLACK = (0,0,0)

PADDLE_WIDTH, PADDLE_HEIGHT = 10, 100
PLAYER_SPEED = 6
AI_SPEED = 5
BALL_SIZE = 20

def reset_pong(ball, left_paddle, right_paddle):
    ball.center = (WIDTH//2, HEIGHT//2)
    sx = random.choice([-5,5])
    sy = random.choice([-5,5])
    left_paddle.y = HEIGHT//2 - PADDLE_HEIGHT//2
    right_paddle.y = HEIGHT//2 - PADDLE_HEIGHT//2
    return sx, sy


def run_pong():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pong vs AI")

    left_paddle = pygame.Rect(30, HEIGHT//2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
    right_paddle = pygame.Rect(WIDTH-40, HEIGHT//2 - 50, PADDLE_WIDTH, PADDLE_HEIGHT)
    ball = pygame.Rect(WIDTH//2, HEIGHT//2, BALL_SIZE, BALL_SIZE)

    bx, by = reset_pong(ball, left_paddle, right_paddle)
    clock = pygame.time.Clock()

    p_score = 0
    ai_score = 0

    FONT = pygame.font.SysFont("Arial", 32)

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                return

        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and left_paddle.top > 0:
            left_paddle.y -= PLAYER_SPEED
        if keys[pygame.K_s] and left_paddle.bottom < HEIGHT:
            left_paddle.y += PLAYER_SPEED

        # AI movement
        if ball.centery < right_paddle.centery:
            right_paddle.y -= AI_SPEED
        elif ball.centery > right_paddle.centery:
            right_paddle.y += AI_SPEED

        # Ball movement
        ball.x += bx
        ball.y += by

        if ball.top <= 0 or ball.bottom >= HEIGHT:
            by *= -1

        if ball.colliderect(left_paddle) or ball.colliderect(right_paddle):
            bx *= -1

        # Scoring
        if ball.left <= 0:
            ai_score += 1
            bx, by = reset_pong(ball, left_paddle, right_paddle)

        if ball.right >= WIDTH:
            p_score += 1
            bx, by = reset_pong(ball, left_paddle, right_paddle)

        # Draw
        screen.fill(BLACK)
        pygame.draw.rect(screen, WHITE, left_paddle)
        pygame.draw.rect(screen, WHITE, right_paddle)
        pygame.draw.ellipse(screen, WHITE, ball)
        pygame.draw.aaline(screen, WHITE, (WIDTH//2,0), (WIDTH//2,HEIGHT))

        score_text = FONT.render(f"{p_score} | {ai_score}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - 40, 20))

        pygame.display.flip()
        clock.tick(60)



# ============================================================
#                     MAIN MENU (TEXT)
# ============================================================

def main():
    while True:
        print("\n===========================")
        print("      PYTHON AI GAMES")
        print("===========================")
        print("1. Rock Paper Scissors")
        print("2. Tic Tac Toe")
        print("3. Pong vs AI")
        print("4. Quit")
        
        choice = input("Choose a game: ")

        if choice == "1":
            play_rps()
        elif choice == "2":
            play_ttt()
        elif choice == "3":
            run_pong()
        elif choice == "4":
            print("Goodbye!")
            sys.exit()
        else:
            print("Invalid choice.\n")

# ============================================================
#                         RUN PROGRAM
# ============================================================

if __name__ == "__main__":
    main()

import curses
import random

def main(stdscr):
    # Setup
    curses.curs_set(0)  # Hide the cursor
    stdscr.nodelay(True)  # Don't wait for user input
    stdscr.timeout(100)   # Refresh every 100 ms

    # Get screen size
    sh, sw = stdscr.getmaxyx()
    box = [[3, 3], [sh - 3, sw - 3]]

    # Create a border
    for y in range(box[0][0], box[1][0]):
        stdscr.addstr(y, box[0][1], '│')
        stdscr.addstr(y, box[1][1], '│')
    for x in range(box[0][1], box[1][1]):
        stdscr.addstr(box[0][0], x, '─')
        stdscr.addstr(box[1][0], x, '─')

    stdscr.addstr(box[0][0], box[0][1], '┌')
    stdscr.addstr(box[0][0], box[1][1], '┐')
    stdscr.addstr(box[1][0], box[0][1], '└')
    stdscr.addstr(box[1][0], box[1][1], '┘')

    # Initial snake and food
    snake = [[sh//2, sw//2 + i] for i in range(3)]
    direction = curses.KEY_LEFT
    food = [random.randint(box[0][0] + 1, box[1][0] - 1),
            random.randint(box[0][1] + 1, box[1][1] - 1)]
    stdscr.addch(food[0], food[1], '🍎')

    # Game loop
    while True:
        key = stdscr.getch()
        if key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            direction = key

        head = snake[0]
        if direction == curses.KEY_UP:
            new_head = [head[0] - 1, head[1]]
        elif direction == curses.KEY_DOWN:
            new_head = [head[0] + 1, head[1]]
        elif direction == curses.KEY_LEFT:
            new_head = [head[0], head[1] - 2]
        elif direction == curses.KEY_RIGHT:
            new_head = [head[0], head[1] + 2]

        # Check collisions
        if (new_head in snake or
            new_head[0] in [box[0][0], box[1][0]] or
            new_head[1] in [box[0][1], box[1][1]]):
            msg = "GAME OVER"
            stdscr.addstr(sh//2, sw//2 - len(msg)//2, msg)
            stdscr.refresh()
            curses.napms(2000)
            break

        snake.insert(0, new_head)
        if new_head == food:
            food = None
            while food is None:
                nf = [random.randint(box[0][0]+1, box[1][0]-1),
                      random.randint(box[0][1]+1, box[1][1]-1)]
                if nf not in snake:
                    food = nf
            stdscr.addch(food[0], food[1], '🍎')
        else:
            tail = snake.pop()
            stdscr.addch(tail[0], tail[1], ' ')

        stdscr.addch(new_head[0], new_head[1], '█')

if __name__ == "__main__":
    curses.wrapper(main)

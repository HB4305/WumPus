# import tkinter as tk
# from environment import N, agent_pos, agent_dir, grid
# from inference_engine import knowledge

# CELL_SIZE = 60
# colors = {
#     'safe': 'lightgreen',
#     'maybe_pit': 'orange',
#     'maybe_wumpus': 'red',
#     'unknown': 'gray',
#     'visited': 'white'
# }

# def draw_grid(canvas, visited):
#     canvas.delete("all")
#     for x in range(N):
#         for y in range(N):
#             px = x * CELL_SIZE
#             py = (N - 1 - y) * CELL_SIZE
#             pos = (x, y)

#             # Màu nền ô
#             if pos == agent_pos:
#                 color = 'blue'
#             elif pos in visited:
#                 color = colors.get(knowledge.get(pos, 'visited'), 'white')
#             else:
#                 color = 'gray'

#             canvas.create_rectangle(px, py, px+CELL_SIZE, py+CELL_SIZE, fill=color)
#             canvas.create_text(px+CELL_SIZE//2, py+CELL_SIZE//2, text=f"{x},{y}", font=('Arial', 9))

#             # Hiển thị icon agent hướng N/E/S/W
#             if pos == agent_pos:
#                 canvas.create_text(px+CELL_SIZE//2, py+CELL_SIZE//2 + 20, text=agent_dir, fill='white', font=('Arial', 10, 'bold'))

# def show_gui(percept, action, visited):
#     window = tk.Tk()
#     window.title("Wumpus World")
#     canvas = tk.Canvas(window, width=N*CELL_SIZE, height=N*CELL_SIZE)
#     canvas.pack()

#     draw_grid(canvas, visited)

#     # Thông tin percept
#     info = tk.Label(window, text=f"Percept: {percept}\nAction: {action}", font=('Arial', 12))
#     info.pack()

#     window.after(1000, window.destroy)  # Tự động tắt sau 1 giây (hiệu ứng animation)
#     window.mainloop()
import tkinter as tk
import time

CELL = 60
DELAY = 500  # mili giây
root = None
canvas = None
step_callback = None
auto_running = False

def init_gui(n, on_step):
    global root, canvas, step_callback
    step_callback = on_step

    root = tk.Tk()
    root.title("Wumpus World GUI")

    canvas = tk.Canvas(root, width=n * CELL, height=n * CELL)
    canvas.pack()

    frame = tk.Frame(root)
    frame.pack()

    next_btn = tk.Button(frame, text="Next Step", command=next_step)
    next_btn.pack(side=tk.LEFT, padx=5)

    auto_btn = tk.Button(frame, text="Auto Run", command=start_auto)
    auto_btn.pack(side=tk.LEFT, padx=5)

def draw_grid(n, agent_pos, agent_dir, visited, grid, wumpus_alive, knowledge):
    canvas.delete("all")
    for x in range(n):
        for y in range(n):
            px = x * CELL
            py = (n - 1 - y) * CELL
            pos = (x, y)

            if pos == agent_pos:
                color = "blue"
            elif pos in visited:
                tag = knowledge.get(pos, '')
                if tag == 'safe':
                    color = 'lightgreen'
                elif tag == 'maybe_pit':
                    color = 'orange'
                elif tag == 'maybe_wumpus':
                    color = 'red'
                else:
                    color = 'white'
            else:
                color = 'gray'

            canvas.create_rectangle(px, py, px+CELL, py+CELL, fill=color, outline='black')
            canvas.create_text(px+CELL//2, py+CELL//2, text=f"{x},{y}", font=('Arial', 8))

            if grid[x][y]['gold']:
                canvas.create_text(px+30, py+15, text="G", fill="gold", font=('Arial', 10, 'bold'))

            if grid[x][y]['pit']:
                canvas.create_text(px+30, py+30, text="P", fill="black", font=('Arial', 10))

            if grid[x][y]['wumpus'] is not None and wumpus_alive[grid[x][y]['wumpus']]:
                canvas.create_text(px+30, py+45, text="W", fill="red", font=('Arial', 10))

            if pos == agent_pos:
                canvas.create_text(px+30, py+30, text=agent_dir, fill="white", font=('Arial', 12, 'bold'))

    root.update()

def next_step():
    if step_callback:
        done = step_callback()
        if done:
            stop_auto()

def start_auto():
    global auto_running
    auto_running = True
    auto_loop()

def stop_auto():
    global auto_running
    auto_running = False

def auto_loop():
    if auto_running:
        next_step()
        root.after(DELAY, auto_loop)

def start_gui():
    root.mainloop()

def draw_rect(canvas, x, y, width, height, fill):
    x2 = x + width
    y2 = y + height
    canvas.create_rectangle(x, y, x2, y2, fill=fill)

def fill_screen(canvas, fill):
    canvas.delete("all")
    canvas.create_rectangle(0, 0, canvas.width, canvas.height, fill=fill)

def draw_oval(canvas, x, y, width, height, fill):
    x2 = x + width
    y2 = y + height
    canvas.create_oval(x, y, x2, y2, fill=fill)

def draw_circle(canvas, x, y, radius, fill):
    canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=fill)

def draw_line(canvas, x1, y1, x2, y2, fill):
    canvas.create_line(x1, y1, x2, y2, fill=fill)
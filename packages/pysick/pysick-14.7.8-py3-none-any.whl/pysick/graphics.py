def draw_rect(canvass, x, y, width, height, fill):
    x2 = x + width
    y2 = y + height
    canvass.canvas.create_rectangle(x, y, x2, y2, fill=fill)

def fill_screen(canvass, fill):
    canvass.canvas.delete("all")
    canvass.canvas.create_rectangle(0, 0, canvass.width, canvass.height, fill=fill)

def draw_oval(canvass, x, y, width, height, fill):
    x2 = x + width
    y2 = y + height
    canvass.canvas.create_oval(x, y, x2, y2, fill=fill)

def draw_circle(canvass, x, y, radius, fill):
    canvass.canvas.create_oval(x - radius, y - radius, x + radius, y + radius, fill=fill)

def draw_line(canvass, x1, y1, x2, y2, fill):
    canvass.canvas.create_line(x1, y1, x2, y2, fill=fill)
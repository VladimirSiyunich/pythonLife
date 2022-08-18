# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
import time
import tkinter as tk
import threading
import random
from logic import *


class MainWindow(tk.Frame):
    __canvas_width = 1200
    __canvas_height = 680
    __x0 = 0
    __y0 = 0

    def __init__(self, root, **kwargs):
        super().__init__(root, **kwargs)
        self.root = root
        self.x = self.y = 0
        self.run = False
        self.set = False
        self.initUI()

    def initUI(self):
        opts = {'ipadx': 10, 'ipady': 10, 'sticky': 'nswe'}
        vldt_ifnum_cmd = (self.root.register(self.ValidateIfNum), '%P', '%W')
        self.lbl1 = tk.Label(self.root, text="Rows:")
        self.lbl1.grid(column=0, row=0, **opts)
        self.spn_rows = tk.Spinbox(self.root, from_=10, to=100, increment=10, validate='all', validatecommand=vldt_ifnum_cmd)
        self.spn_rows.grid(column=1, row=0, **opts)
        self.lbl2 = tk.Label(self.root, text="Columns:")
        self.lbl2.grid(column=0, row=1, **opts)
        self.spn_columns = tk.Spinbox(self.root, from_=10, to=100, increment=10, validate='all', validatecommand=vldt_ifnum_cmd)
        self.spn_columns.grid(column=1, row=1, **opts)
        self.btn = tk.Button(self.root, text="Set!", command=self.clicked)
        self.btn.grid(column=0, row=2, columnspan=3, **opts)
        self.canvas0 = tk.Canvas(self.root, width=self.__canvas_width, height=self.__canvas_height, cursor="cross")
        self.canvas1 = tk.Canvas(self.root, width=self.__canvas_width, height=self.__canvas_height, cursor="cross")

    def clicked(self):
        rows = int(self.spn_rows.get())
        columns = int(self.spn_columns.get())
        self.world = World(rows, columns)
        self.set = True
        self.draw_grid(rows, columns)
        self.canvas0.bind('<Button-1>', self.b1)
        opts = {'ipadx': 10, 'ipady': 10, 'sticky': 'nswe'}
        self.lbl4 = tk.Label(self.root, text="Cycle: 0")
        self.lbl4.grid(column=1, row=0, **opts)
        self.btn_go = tk.Button(self.root, text="Go!", command=self.clicked_go)
        self.btn_go.grid(column=2, row=0, **opts)
        self.btn_stop = tk.Button(self.root, text="Stop!", command=self.clicked_stop)
        self.btn_stop.grid(column=3, row=0, **opts)
        opts = {'ipadx': 10, 'ipady': 10, 'sticky': 'nwe'}
        self.btn_random = tk.Button(self.root, text="Random seed", command=self.clicked_random)
        self.btn_random.grid(column=2, row=1, columnspan=2, **opts)

    def clicked_random(self):
        for k in range(self.world.numRows * self.world.numColumns // 10):
            i = random.randint(0, self.world.numRows - 1)
            j = random.randint(0, self.world.numColumns - 1)
            if self.put_cell(i, j):
                color = '#0000ffff0000'
            else:
                color = '#ffffffffffff'
            self.fill_cell(self.canvas0, i, j, color)
            self.fill_cell(self.canvas1, i, j, color)

    def clicked_go(self):
        if not self.run:
            self.run = True
            self.x = threading.Thread(target=self.life_thread, daemon=True)
            self.x.start()

    def clicked_stop(self):
        if self.run:
            self.run = False
            print("thread: %s" % self.run)

    def life_thread(self):
        cycle = 0
        while True:
            if self.run:
                self.lbl4.config(text="Cycle: " + str(cycle))
                self.world.next_cycle()
                if len(self.world.change_list) == 0:
                    self.run = False
                    return
                if cycle % 2 == 0:
                    self.flip_canvas(self.canvas0, self.canvas1)
                else:
                    self.flip_canvas(self.canvas1, self.canvas0)
                time.sleep(0.2)
                cycle += 1
            else:
                return
            time.sleep(0.1)

    def flip_canvas(self, active_canvas, hidden_canvas):
        self.update_canvas(hidden_canvas, self.world.change_list)
        active_canvas.grid_remove()
        hidden_canvas.grid(column=1, row=1)
        self.update_canvas(active_canvas, self.world.change_list)

    def update_canvas(self, canvas, change_list):
        for k in range(len(change_list)):
            pair = change_list[k]
            i = pair[0]
            j = pair[1]
            age = self.world.matrix[i][j].age
            if age == -1:
                self.fill_cell(canvas, i, j, "#fffffffff")
            else:
                ng = 65535 - age * (65535 / Cell.maxAge)
                if ng < 0:
                    ng = 0
                color = "#%4.4x%4.4x%4.4x" % (0, int(ng), 0)
                self.fill_cell(canvas, i, j, color)

    def draw_grid(self, rows, columns):
        self.lbl1.grid_forget()
        self.lbl2.grid_forget()
        self.spn_rows.grid_forget()
        self.spn_columns.grid_forget()
        self.btn.grid_forget()
        self.canvas0.grid(column=1, row=1)
        self.rowHeight = self.__canvas_height / rows
        self.columnWidth = self.__canvas_width / columns
        self.canvas0.create_rectangle(self.__x0, self.__y0, self.__canvas_width, self.__canvas_height, fill='white')
        self.canvas1.create_rectangle(self.__x0, self.__y0, self.__canvas_width, self.__canvas_height, fill='white')
        self.grid = [[self.draw_cell(y, x, 'white') for x in range(columns)] for y in range(rows)]

    def b1(self, event):
        self.x = event.x
        self.y = event.y
        if self.set:
            row = self.get_row(self.y)
            column = self.get_column(self.x)
            if self.put_cell(row, column):
                color = '#0000ffff0000'
            else:
                color = '#ffffffffffff'
            self.fill_cell(self.canvas0, row, column, color)

    def get_row(self, y):
        return int((y - self.__y0) / self.rowHeight)

    def get_column(self, x):
        return int((x - self.__x0) / self.columnWidth)

    def put_cell(self, row, column):
        if self.world.matrix[row][column].age == -1:
            self.world.matrix[row][column].age = 1
            return True
        else:
            self.world.matrix[row][column].age = -1
            return False

    def draw_cell(self, row, column, color):
        x1 = self.__x0 + self.columnWidth * column
        x2 = x1 + self.columnWidth
        y1 = self.__y0 + self.rowHeight * row
        y2 = y1 + self.rowHeight
        rect = self.canvas0.create_rectangle(x1, y1, x2, y2, fill=color, outline='white')
        rect = self.canvas1.create_rectangle(x1, y1, x2, y2, fill=color, outline='white')
        return rect

    def fill_cell(self, canvas, row, column, color):
        canvas.itemconfig(self.grid[row][column], fill=color)


    def ValidateIfNum(self, user_input, widget_name):
        valid = True
        minval = int(self.root.nametowidget(widget_name).config('from')[4])
        maxval = int(self.root.nametowidget(widget_name).config('to')[4])
        if int(user_input) not in range (minval, maxval):
            valid = False
        return valid

def main():
    global window
    window = tk.Tk()
    window.title("Life game")
    window.geometry("1350x720+20+30")
    MainWindow(window)
    window.mainloop()


if __name__ == '__main__':
    main()

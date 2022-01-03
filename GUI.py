import checkers
import tkinter
from win32api import GetSystemMetrics


class MainFrame():
    val = 0
    game = []
    canvas = 0
    line_count = 0
    width_offset = 100
    height_offset = 100
    interval_width = 0
    interval_height = 0
    width = 0
    height = 0
    AI = True
    root =[]
    resigned = -1

    def __init__(self, root, game, line_count,AI):
        self.game = game
        self.AI = AI
        self.width = GetSystemMetrics(0) - 100
        self.height = GetSystemMetrics(1) - 100
        self.root = root
        canvas = tkinter.Canvas(root, height=self.height, width=self.width)
        canvas.pack()
        self.canvas = canvas
        self.line_count = line_count
        self.width_offset = 100
        self.height_offset = 100
        available_width = self.width - 2 * self.width_offset
        available_height = self.height - 2 * self.height_offset
        self.interval_width = available_width / (line_count - 1)
        self.interval_height = available_height / (line_count - 1)
        canvas.bind('<Button-1>', self.canvas_click_event)
        for i in range(0, line_count):
            self.canvas.create_line(self.width_offset + i * self.interval_width, self.height_offset,
                                    self.width_offset + i * self.interval_width, self.height - self.height_offset)
            self.canvas.create_line(self.width_offset, self.height_offset + i * self.interval_height,
                                    self.width - self.width_offset, self.height_offset + i * self.interval_height)
        btn = tkinter.Button(root, text='Pass turn', width=40,
                             height=5, bd='10', command=self.pass_turn_to)

        btn.place(x=self.width_offset, y=self.height - 80)
        btn2 = tkinter.Button(self.root, text='Resign', width=40,
                             height=5, bd='10', command=self.resign)
        btn2.place(x=self.width/2, y=self.height - 80)
        root.mainloop()

    def canvas_click_event(self, event):
        self.get_position_from_grid([event.x, event.y])
        if(self.AI):
            checkers.random_ai(self.game, 100)
            self.redraw_board()

    def pass_turn_to(self):
        checkers.pass_turn(self.game)
        if(self.AI):
            checkers.random_ai(self.game, 100)
        self.redraw_board()

    def get_position_from_grid(self, position):
        x_pos = position[0]
        x_cell = (x_pos - self.width_offset + self.interval_width / 2) // self.interval_width
        if x_cell >= self.line_count:
            x_cell = self.line_count - 1
        if x_cell < 0:
            x_cell = 0
        y_pos = position[1]
        y_cell = (y_pos - self.height_offset + self.interval_height / 2) // self.interval_height
        if y_cell >= self.line_count:
            y_cell = self.line_count - 1
        if y_cell < 0:
            y_cell = 0
        x_cell = int(x_cell)
        y_cell = int(y_cell)
        print(str(x_cell) + " " + str(y_cell))
        if checkers.move_piece(self.game, [x_cell, y_cell]):
            self.redraw_board()


    def draw_at_cell(self, position, piece,previousFlag):
        pos_x = self.width_offset + position[0] * self.interval_width
        pos_y = self.height_offset + position[1] * self.interval_height
        color = ""
        if (piece == 0):
            color = "#FFFFFF"
        else:
            color = "#000000"
        piece_size_width = self.interval_width/2.1
        piece_size_height = self.interval_height/2.1
        piece_size= min(piece_size_height,piece_size_width)

        self.canvas.create_oval(pos_x - piece_size, pos_y - piece_size, pos_x + piece_size, pos_y + piece_size,
                                fill=color)
        if (previousFlag):
            self.canvas.create_oval(pos_x - piece_size / 4, pos_y - piece_size / 4, pos_x + piece_size / 4,
                                    pos_y + piece_size / 4,
                                    fill="#0066FF")
    def resign(self):
        self.resigned = self.game.playerTurn
        self.end_screen()

    def redraw_board(self):
        self.canvas.delete("all")
        self.canvas.pack()
        if not checkers.is_final(self.game):
            for i in range(0, self.line_count):
                self.canvas.create_line(self.width_offset + i * self.interval_width, self.height_offset,
                                        self.width_offset + i * self.interval_width, self.height - self.height_offset)
                self.canvas.create_line(self.width_offset, self.height_offset + i * self.interval_height,
                                        self.width - self.width_offset, self.height_offset + i * self.interval_height)
            for i in range(0, len(self.game.board.Rows)):
                for j in range(0, len(self.game.board.Rows[0])):
                    if self.game.board.Rows[i][j] != -1:
                        previousFlag = False
                        if self.game.previousMove:
                            if i == self.game.previousMove[0] and j == self.game.previousMove[1]:
                                previousFlag = True
                        self.draw_at_cell([i, j], self.game.board.Rows[i][j],previousFlag)
            score = checkers.compute_scores(self.game)
            self.canvas.create_text(100, 25, text="BlackScore = " + str(score[0]), fill="black",
                                    font=('Helvetica 15 bold'))
            self.canvas.create_text(self.width / 2, 25, text="WhiteScore = " + str(score[1]), fill="black",
                                    font=('Helvetica 15 bold'))
        else:
            self.end_screen()

    def end_screen(self):
        score = checkers.compute_scores(self.game)
        self.canvas.create_text(100, 25, text="BlackScore = " + str(score[0]), fill="black",
                                font=('Helvetica 15 bold'))
        self.canvas.create_text(self.width / 2, 25, text="WhiteScore = " + str(score[1]), fill="black",
                                font='Helvetica 15 bold')
        winner = "Tie"
        if (self.resigned == -1):
            if score[0] > score[1]:
                winner = " Black won "
            elif score[0] < score[1]:
                winner = " White won "
        else:
            if self.resigned == 0:
                winner = "Black won"
            else:
                winner = "White won"

        self.canvas.create_text(self.width / 2 - 200, self.height / 2, text=winner, fill="black",
                                font=('Helvetica 30 bold'))
        btn = tkinter.Button(self.root, text='Restart', width=40,
                             height=5, bd='10', command=self.restart_game)
        btn.place(x=self.width - self.width_offset *2 , y=self.height - 80)

    def restart_game(self):
        self.root.destroy()
        mainScreen = MenuFrame()
        mainScreen.frame.mainloop()


class MenuFrame():
    game_size = 1
    AI = True
    frame = []
    variable = []
    inputtxt =[]
    def __init__(self):
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        root = tkinter.Tk()
        root.minsize(300, 300)
        self.frame = root
        sizes = ['7x7','9x9','11x11','13x13','19x19','Custom']
        self.variable = tkinter.StringVar()
        self.variable.set(sizes[3])
        dropdown = tkinter.OptionMenu(root,self.variable,
            *sizes,
            command=self.choose_game
        )
        dropdown.place(x=100,y=0)
        self.inputtxt = tkinter.Text(root,
                           height=3,
                           width=10)
        self.inputtxt.place(x=100, y=100)
        txt = tkinter.Label(root,text="Custom size")
        txt.place(x=100,y=80)
        printButton = tkinter.Button(root,
                                text="Submit",
                                command=self.proceed_to_main)
        printButton.place(x=100,y=150)
        self.AI = tkinter.IntVar()
        c = tkinter.Checkbutton(root, text="AI", variable=self.AI)
        c.place(x=100,y=60)

    def proceed_to_main(self):
        print("Here")

        print(self.game_size)
        self.start_game()

    def choose_game(self,choice):
        choice = self.variable.get()
        print(choice)
        if(choice != "Custom"):
            self.game_size = int(choice[0:choice.find('x')])
        else:
            self.game_size = int(self.inputtxt.get(1.0,"end-1c"))

    def start_game(self):
        width = GetSystemMetrics(0)
        height = GetSystemMetrics(1)
        root = tkinter.Tk()
        root.minsize(width - 100, height - 100)
        game = checkers.Game(self.game_size)
        self.frame.destroy()
        frame = MainFrame(root, game, len(game.board.Rows), self.AI.get())





print("Width =", GetSystemMetrics(0))
print("Height =", GetSystemMetrics(1))

game = checkers.Game(15)
mainScreen = MenuFrame()
mainScreen.frame.mainloop()
# for i in range(0, 100):
#     checkers.random_ai(game, 300)
# checkers.printGame(game)
# width = GetSystemMetrics(0)
# height = GetSystemMetrics(1)
# root = tkinter.Tk()
# root.minsize(width - 100, height - 100)
# frame = MainFrame(root, game, len(game.board.Rows),True)
# canvas = tkinter.Canvas(root,width = GetSystemMetrics(0),height= GetSystemMetrics(1))
# canvas.pack()

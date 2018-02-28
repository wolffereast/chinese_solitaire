import Tkinter
import gameboard

layout1 = []
layout1.append([-1, -1, 1, 1, 1, -1, -1])
layout1.append([-1, 1, 1, 1, 1, 1, -1])
layout1.append([1, 1, 1, 1, 1, 1, 1])
layout1.append([1, 1, 1, 0, 1, 1, 1])
layout1.append([1, 1, 1, 1, 1, 1, 1])
layout1.append([-1, 1, 1, 1, 1, 1, -1])
layout1.append([-1, -1, 1, 1, 1, -1, -1])

# bad layout here. Can't be empty.
layout2 = []

# Also a bad layout, Not a nested array.
layout3 = [0, 0, 0]

# Bad layout, rows are not the same length.
layout4 = []
layout4.append([0, 0, 0])
layout4.append([0, 0])
layout4.append([0, 0, 0])

# Bad layout, invalid indexes, must be -1, 0, or 1.
layout5 = []
layout5.append([0, 0, 0])
layout5.append([2, 0, 0])
layout5.append([1, 1, 1])

root = Tkinter.Tk()
root.title('Chinese Solitaire')
board = gameboard.Gameboard(layout1, root)
board.mainloop()
root.destroy()

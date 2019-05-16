"""
(to be re-named) Eisenhower.py
Author: Jon David Tannehill
"""

import functools
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

global tasks
tasks = {}

class Task():
    global tasks
    def __init__(self, todo, matrix):
        self.name = tk.StringVar()
        self.urgency = tk.IntVar()
        self.importance = tk.IntVar()
        self.name.set('task ' + str(len(tasks)))
        self.urgency.set(len(tasks))
        self.importance.set(len(tasks))

        self.unitL = tk.Frame(todo)
        self.itemL = tk.Entry(self.unitL, textvariable=self.name)
        self.itemL.grid(row=1, column=1, columnspan=3)

        self.unitL.grid(row=self.urgency.get()+2, column=1)

        self.unitR = tk.Frame(todo)
        self.itemR = tk.Entry(self.unitR, textvariable=self.name)
        self.itemR.grid(row=1, column=1, columnspan=3)
        self.increaseR = tk.Button(self.unitR, text='Raise', command=functools.partial(self.increase_importance, self.itemL, self.importance, self.unitR))
        self.increaseR.grid(row=2, column=1)
        self.decreaseR = tk.Button(self.unitR, text='Lower', command=functools.partial(self.decrease_importance, self.itemL, self.importance, self.unitR))
        self.decreaseR.grid(row=2, column=2)
        self.deleteR = tk.Button(self.unitR, text='Delete', command=functools.partial(self.delete_task, self.itemL, self.unitL, self.unitR))
        self.deleteR.grid(row=2, column=3)
        self.unitR.grid(row=self.importance.get()+2, column=2)

        self.increaseL = tk.Button(self.unitL, text='Raise', command=functools.partial(self.increase_urgency, self.itemL, self.urgency, self.unitL))
        self.increaseL.grid(row=2, column=1)
        self.decreaseL = tk.Button(self.unitL, text='Lower', command=functools.partial(self.decrease_urgency, self.itemL, self.urgency, self.unitL))
        self.decreaseL.grid(row=2, column=2)
        self.deleteL = tk.Button(self.unitL, text='Delete', command=functools.partial(self.delete_task, self.itemL, self.unitL, self.unitR))
        self.deleteL.grid(row=2, column=3)

        self.itemL.focus_set()
        tasks[self.itemL.get()] = [self.urgency.get(), self.importance.get()]

    def new_task():
        pass

    def delete_task(self, itemL, unitL, unitR):
        del tasks[itemL.get()]
        unitL.grid_forget()
        unitR.grid_forget()
        del self

#Problems with the following class methods:
#Why does the second if condition, on line 65 and corresponding lines in other functions, (sometimes) trigger when it seems that itemL's value never changes??
#Need to have a way to change the grid position of another class instance's unitL row number too. Not that the current one works or anything --> use todo.winfo_children() and matrix.winfo_children() ???

    def increase_urgency(self, itemL, urgency, unitL):
        global tasks
        if tasks[itemL.get()][0] != 0:
            print(tasks[itemL.get()][0])
            tasks[itemL.get()][0] -= 1
        for x in tasks.keys():
            if tasks[x][0] == tasks[itemL.get()][0]:
                tasks[x][0] += 1
        unitL.grid(row=self.urgency.get()+2, column=1)

    def increase_importance(self, itemL, importance, unitR):
        global tasks
        if tasks[itemL.get()][1] != 0:
            print(tasks[itemL.get()])
            tasks[itemL.get()][1] -= 1
        for x in tasks.keys():
            if tasks[x][1] == tasks[itemL.get()][1]:
                tasks[x][1] += 1
        unitR.grid(row=self.importance.get()+2, column=2)

    def decrease_urgency(self, itemL, urgency, unitL):
        global tasks
        print(tasks[itemL.get()])
        for x in tasks.keys():
            if tasks[x][0] > tasks[itemL.get()][0]:
                tasks[itemL.get()][0] += 1
                break
        for x in tasks.keys():
            if tasks[x][0] == tasks[itemL.get()][0]:
                tasks[x][0] -= 1
        unitL.grid(row=self.urgency.get()+2, column=1)

    def decrease_importance(self, itemL, importance, unitR):
        global tasks
        print(tasks[itemL.get()])
        for x in tasks.keys():
            if tasks[x][1] > tasks[itemL.get()][1]:
                tasks[itemL.get()][1] +=1
                break
        tasks[itemL.get()][1] += 1
        for x in tasks.keys():
            if tasks[x][1] == tasks[itemL.get()][1]:
                tasks[x][1] -= 1
        unitR.grid(row=self.importance.get()+2, column=2)

def generate():
    print(tasks)

def help():
    help = tk.Toplevel()
    help.title('Help Information')
    tk.Label(help, text='This box will contain useful information on the application and Eisenhower matrixes in general.').pack(ipadx=15, ipady=15)
    tk.Button(help, text='Ok', command=help.destroy).pack()
    help.mainloop()

root = tk.Tk()
root.title('Eisenhower Matrix')
widthR = str(int(root.winfo_screenwidth()))
heightR = str(int(root.winfo_screenheight()))
root.geometry(widthR + 'x' + heightR)

menu = tk.Frame(root, relief='ridge', borderwidth=2)
saveAs = tk.Button(menu, text='Save As', command=asksaveasfilename)
saveAs.pack(side='left')
save = tk.Button(menu, text='Save', command=None)
save.pack(side='left')
load = tk.Button(menu, text='Load', command=askopenfilename)
load.pack(side='left')
clearAll = tk.Button(menu, text='Clear All', command=None)
clearAll.pack(side='left')
help = tk.Button(menu, text='Help', command=help)
help.pack(side='left')
quit = tk.Button(menu, text='Quit', command=root.destroy)
quit.pack(side='left')
menu.pack(side='top', anchor='nw', fill='x')

todo = tk.Frame(root, relief='ridge', borderwidth=2)
tk.Label(todo, text='Urgency:').grid(row=1, column=1)
tk.Label(todo, text='Importance:').grid(row=1, column=2)
todo.pack(side='left', anchor='nw', fill='y')
new = tk.Button(todo, text='New Task', command=lambda: Task(todo, matrix))
new.grid(row=1002, column=1)
generate = tk.Button(todo, text='Generate Matrix', command=generate)
generate.grid(row=1002, column=2)

matrix = tk.Frame(root, relief='ridge', borderwidth=2)
matrix.pack(side='left', fill='x')
quadrants = tk.Canvas(matrix, bg='red', width=100, height=100)
quadrants.pack(fill='both')


if __name__ == '__main__':
    Task(todo, matrix)
    root.mainloop()
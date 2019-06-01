"""
Eisenhower.py

Creates and dynamically re-orders an Eisenhower Matrix out of a list of tasks based on their relative importance and urgency.
Still crude and a little ugly with several buttons in the top menu that don't do anything, but it basically works.

A work in progress by:
Jon David Tannehill
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import sys, functools, operator
#import PIL.ImageTk

global task_names, task_ids
task_names = {}
task_ids = ['task' + str(x) for x in range(100)]

class Task():
    def __init__(self, root, menu, todo, matrix):
        self.name = tk.StringVar(value='Task '+str(len(task_names)))
        self.urgency = tk.IntVar(value=len(task_names))
        self.importance = tk.IntVar(value=len(task_names))

        self.unitM = tk.Label(matrix, textvariable=self.name, font='Times 6 bold', height=2, width=8)

        self.unitU = tk.Frame(todo)
        self.unitI = tk.Frame(todo)
        self.unitU.grid(row=self.urgency.get()+1, column=1)
        self.unitI.grid(row=self.importance.get()+1, column=2)
        self.itemU = tk.Entry(self.unitU, textvariable=self.name)
        self.increaseU = tk.Button(self.unitU, text='Raise', command=functools.partial(self.increase_urgency, self.unitU, self.urgency))
        self.decreaseU = tk.Button(self.unitU, text='Lower', command=functools.partial(self.decrease_urgency, self.unitU, self.urgency))
        self.deleteU = tk.Button(self.unitU, text='Delete', command=functools.partial(self.delete_task, self.unitU, self.unitI, self.unitM))
        self.itemU.grid(row=1, column=1, columnspan=3)
        self.increaseU.grid(row=2, column=1)
        self.decreaseU.grid(row=2, column=2)
        self.deleteU.grid(row=2, column=3)

        self.itemI = tk.Entry(self.unitI, textvariable=self.name)
        self.increaseI = tk.Button(self.unitI, text='Raise', command=functools.partial(self.increase_importance, self.unitI, self.importance))
        self.decreaseI = tk.Button(self.unitI, text='Lower', command=functools.partial(self.decrease_importance, self.unitI, self.importance))
        self.deleteI = tk.Button(self.unitI, text='Delete', command=functools.partial(self.delete_task, self.unitU, self.unitI, self.unitM))
        self.itemI.grid(row=1, column=1, columnspan=3)
        self.increaseI.grid(row=2, column=1)
        self.decreaseI.grid(row=2, column=2)
        self.deleteI.grid(row=2, column=3)
        
        # debugging code below:
        print(self.name.get()+' initialized with', 'urgency '+str(self.urgency.get()), 'and importance '+str(self.importance.get()))
        print(task_names)


    def place(self, urgency, importance, unitM):
        global task_names
        base = 9 - ((len(task_names) // 2) + (len(task_names) % 2))
        rownum = base + importance.get()
        colnum = base + urgency.get()
        unitM.grid(row=rownum, column=colnum)

    def increase_urgency(self, unitU, urgency):
        if urgency.get() != 0:
            urgency.set(urgency.get()-1)
            for x in task_names.keys():
                if task_names[x].urgency.get() == urgency.get() and task_names[x] != self:
                    task_names[x].urgency.set(task_names[x].urgency.get()+1)
                    task_names[x].unitU.grid(row=task_names[x].urgency.get()+1, column=1)
                    unitU.grid(row=urgency.get()+1, column=1)
                    break
            for x in task_names.keys():
                task_names[x].place(task_names[x].urgency, task_names[x].importance, task_names[x].unitM)
        # for debugging:
        print()
        for x in task_names.keys():
            print(task_names[x].name.get(), ' urgency: ', task_names[x].urgency.get(), sep='')


    def increase_importance(self, unitI, importance):
        if importance.get() != 0:
            importance.set(importance.get()-1)
            for x in task_names.keys():
                if task_names[x].importance.get() == importance.get() and task_names[x] != self:
                    task_names[x].importance.set(task_names[x].importance.get()+1)
                    task_names[x].unitI.grid(row=task_names[x].importance.get()+1, column=2)
                    unitI.grid(row=importance.get()+1, column=2)
                    break
            for x in task_names.keys():
                task_names[x].place(task_names[x].urgency, task_names[x].importance, task_names[x].unitM)
        # for debugging:
        print()
        for x in task_names.keys():
            print(task_names[x].name.get(), ' importance: ', task_names[x].importance.get(), sep='')


    def decrease_urgency(self, unitU, urgency):
        for x in task_names.keys():
            if task_names[x].urgency.get() > urgency.get():
                urgency.set(urgency.get()+1)
                unitU.grid(row=urgency.get()+1, column=1)
                break
        for x in task_names.keys():
            if task_names[x].urgency.get() == urgency.get() and task_names[x] != self:
                task_names[x].urgency.set(task_names[x].urgency.get()-1)
                task_names[x].unitU.grid(row=task_names[x].urgency.get()+1, column=1)
                break
        for x in task_names.keys():
            task_names[x].place(task_names[x].urgency, task_names[x].importance, task_names[x].unitM)
        # for debugging: 
        print()
        for x in task_names.keys():
            print(task_names[x].name.get(), ' urgency: ', task_names[x].urgency.get(), sep='')


    def decrease_importance(self, unitI, importance):
        for x in task_names.keys():
            if task_names[x].importance.get() > importance.get():
                importance.set(importance.get()+1)
                unitI.grid(row=importance.get()+1, column=2)
                break
        for x in task_names.keys():
            if task_names[x].importance.get() == importance.get() and task_names[x] != self:
                task_names[x].importance.set(task_names[x].importance.get()-1)
                task_names[x].unitI.grid(row=task_names[x].importance.get()+1, column=2)
                break
        for x in task_names.keys():
            task_names[x].place(task_names[x].urgency, task_names[x].importance, task_names[x].unitM)
        # for debugging:
        print()
        for x in task_names.keys():
            print(task_names[x].name.get(), ' importance: ', task_names[x].importance.get(), sep='')


    def delete_task(self, unitU, unitI, unitM):
        global task_names, task_ids
        print('\nDELETING...')
        print('tasks:', task_names)
        unitU.grid_forget()
        unitI.grid_forget()
        unitM.grid_forget()
        for x in task_names.keys():
            if task_names[x] == self:
                task_ids.insert(0, x)
                del task_names[x]
                break
        print('\nReconfiguring...\n')
        
        try:
            urgency_vals = []
            urgency_slots = {}
            importance_vals = []
            importance_slots = {}
            for x in task_names.keys():
                urgency_vals.append([task_names[x].urgency, task_names[x].urgency.get()])
                importance_vals.append([task_names[x].importance, task_names[x].importance.get()])

            urgency_vals = sorted(urgency_vals, key=operator.itemgetter(1))
            importance_vals = sorted(importance_vals, key=operator.itemgetter(1))
            print('urgency_vals:', urgency_vals)
            print('importance_vals:', importance_vals)
            
            urgency_vals[0][1] = 0
            for x in range(len(urgency_vals)-1):
                if (urgency_vals[x+1][1] - urgency_vals[x][1]) > 1:
                    urgency_vals[x+1][1] -= ((urgency_vals[x+1][1] - urgency_vals[x][1]) - 1)
            for x in range(len(urgency_vals)):
                urgency_vals[x][0].set(urgency_vals[x][1])

            importance_vals[0][1] = 0
            for x in range(len(importance_vals)-1):
                if (importance_vals[x+1][1] - importance_vals[x][1]) > 1:
                    importance_vals[x+1][1] -= ((importance_vals[x+1][1] - importance_vals[x][1]) - 1)
            for x in range(len(importance_vals)):
                importance_vals[x][0].set(importance_vals[x][1])

            print('new urgency values:', urgency_vals)
            print('new importance values:', importance_vals)

            for x in task_names.keys():
                task_names[x].unitU.grid(row=task_names[x].urgency.get()+1, column=1)
                task_names[x].unitI.grid(row=task_names[x].importance.get()+1, column=2)
                task_names[x].place(task_names[x].urgency, task_names[x].importance, task_names[x].unitM)

        except:
            print(sys.exc_info())

        del self


class Gui():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Eisenhower Matrix')
        widthR = str(int(self.root.winfo_screenwidth()))
        heightR = str(int(self.root.winfo_screenheight()))
        self.root.geometry(widthR + 'x' + heightR)

        self.menu = tk.Frame(self.root)
        self.new_task = tk.Button(self.menu, text='New Task', command=self.make_task)
        self.new_task.pack(side='left')
        self.saveAs = tk.Button(self.menu, text='Save As', command=asksaveasfilename)
        self.saveAs.pack(side='left')
        self.save = tk.Button(self.menu, text='Save', command=self.save_tasks)
        self.save.pack(side='left')
        self.load = tk.Button(self.menu, text='Load', command=self.load_tasks)
        self.load.pack(side='left')
        self.clearAll = tk.Button(self.menu, text='Clear All', command=None)
        self.clearAll.pack(side='left')
        self.help = tk.Button(self.menu, text='Help', command=self.task_help)
        self.help.pack(side='left')
        self.quit = tk.Button(self.menu, text='Quit', command=self.root.destroy)
        self.quit.pack(side='left')
        self.menu.grid(row=1, column=1, columnspan=2)
        
        self.todo = tk.Frame(self.root)
        tk.Label(self.todo, text='Urgency').grid(row=0, column=1)
        tk.Label(self.todo, text='Importance').grid(row=0, column=2)
        to_scroll = tk.Scrollbar(self.todo)
        to_scroll.activate(index='slider')
        to_scroll.grid(row=1, column=3)
        self.todo.grid(row=2, column=1)
        
        self.matrix = tk.Frame(self.root)
        tk.Label(self.matrix, text='<----Increasing Urgency----<').grid(row=0, column=0, columnspan=17)
        tk.Label(self.matrix, text='^\n^\n^\n^\n^\n\n\nI\nn\nc\nr\ne\na\ns\ni\nn\ng\n \nI\nm\np\no\nr\nt\na\nn\nc\ne\n\n\n^\n^\n^\n^\n^').grid(row=1, column=0, rowspan=16)
        self.fire = tk.Frame(self.matrix, background='red', width=350, height=300)
        self.annoyance = tk.Frame(self.matrix, background='orange', width=350, height=300)
        self.value_creator = tk.Frame(self.matrix, background='green', width=350, height=300)
        self.leisure = tk.Frame(self.matrix, background='blue', width=350, height=300)
        self.fire.grid(row=1, column=1, rowspan=8, columnspan=8)
        self.annoyance.grid(row=9, column=1, rowspan=8, columnspan=8)
        self.value_creator.grid(row=1, column=9, rowspan=8, columnspan=8)
        self.leisure.grid(row=9, column=9, rowspan=8, columnspan=8)
        self.matrix.grid(row=2, column=2)
        """
        transparent = PIL.ImageTk.PhotoImage(file='Transparent.png')
        self.topmatrix = tk.Frame(self.root, bg=transparent)
        self.topmatrix.grid(row=2, column=2)
        """
        self.make_task()


    def make_task(self):
        global task_names, task_ids
        id = task_ids.pop(0)
        task_names[id] = Task(self.root, self.menu, self.todo, self.matrix)
        for x in task_names.keys():
            task_names[x].place(task_names[x].urgency, task_names[x].importance, task_names[x].unitM)

    def save_tasks(self):
        pass


    def load_tasks(self):
        pass


    def task_help(self):
        help = tk.Toplevel()
        help.title('Help Information')
        tk.Label(help, text='This box will contain useful information on the application and Eisenhower matrixes in general.').pack(ipadx=15, ipady=15)
        tk.Button(help, text='Ok', command=help.destroy).pack()
        help.mainloop()

"""
class Matrix(tk.Frame):
    def __init__(self):
"""

if __name__ == '__main__':
    window = Gui()
    window.root.mainloop()

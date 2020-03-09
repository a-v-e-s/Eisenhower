#!/usr/bin/env python3

"""
Eisenhower.py

Creates and dynamically re-orders an Eisenhower Matrix out of a list of tasks based on their relative importance and urgency.
Still crude and a little ugly, but it basically works.

A work in progress by:
Jon David Tannehill
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import functools, operator, pickle

global task_names, task_ids
task_names = {}
task_ids = ['task' + str(x) for x in range(100)]


class Task():
    def __init__(self, id, root, menu, todo, matrix, data=None):
        if data == None:
            self.name = tk.StringVar(value=id)
            self.urgency = tk.IntVar(value=len(task_names))
            self.importance = tk.IntVar(value=len(task_names))
        else:
            self.name = tk.StringVar(value=data[0])
            self.urgency = tk.IntVar(value=data[1])
            self.importance = tk.IntVar(value=data[2])

        self.unitM = tk.Label(matrix, textvariable=self.name, font='Times 10 bold', height=2, width=8, wraplength=62)

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


    def place(self, urgency, importance, unitM):
        base = 7 - ((len(task_names) // 2) + (len(task_names) % 2))
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


    def delete_task(self, unitU, unitI, unitM):
        global task_ids
        unitU.grid_forget()
        unitI.grid_forget()
        unitM.grid_forget()
        for x in task_names.keys():
            if task_names[x] == self:
                task_ids.insert(0, x)
                del task_names[x]
                break
        
        urgency_vals = []
        importance_vals = []
        for x in task_names.keys():
            urgency_vals.append([task_names[x].urgency, task_names[x].urgency.get()])
            importance_vals.append([task_names[x].importance, task_names[x].importance.get()])
        urgency_vals = sorted(urgency_vals, key=operator.itemgetter(1))
        importance_vals = sorted(importance_vals, key=operator.itemgetter(1))
        
        if urgency_vals:
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

            for x in task_names.keys():
                task_names[x].unitU.grid(row=task_names[x].urgency.get()+1, column=1)
                task_names[x].unitI.grid(row=task_names[x].importance.get()+1, column=2)
                task_names[x].place(task_names[x].urgency, task_names[x].importance, task_names[x].unitM)

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
        self.saveAs = tk.Button(self.menu, text='Save As', command=self.save_as)
        self.saveAs.pack(side='left')
        self.load = tk.Button(self.menu, text='Load', command=self.load_tasks)
        self.load.pack(side='left')
        self.help = tk.Button(self.menu, text='Help', command=self.task_help)
        self.help.pack(side='left')
        self.quit = tk.Button(self.menu, text='Quit', command=self.root.destroy)
        self.quit.pack(side='left')
        self.menu.grid(row=1, column=1, columnspan=2)
        
        self.todo = tk.Frame(self.root)
        tk.Label(self.todo, text='Urgency').grid(row=0, column=1)
        tk.Label(self.todo, text='Importance').grid(row=0, column=2)
        self.todo.grid(row=2, column=1)

        self.matrix = tk.Frame(self.root)
        tk.Label(self.matrix, text='<----Increasing Urgency----<').grid(row=0, column=1, columnspan=12)
        tk.Label(self.matrix, text='^\n^\n^\n^\n^\n\n\nI\nn\nc\nr\ne\na\ns\ni\nn\ng\n \nI\nm\np\no\nr\nt\na\nn\nc\ne\n\n\n^\n^\n^\n^\n^').grid(row=1, column=0, rowspan=12)
        self.fire = tk.Frame(self.matrix, background='red', width=400, height=300)
        self.annoyance = tk.Frame(self.matrix, background='orange', width=400, height=300)
        self.value_creator = tk.Frame(self.matrix, background='green', width=400, height=300)
        self.leisure = tk.Frame(self.matrix, background='blue', width=400, height=300)
        self.fire.grid(row=1, column=1, rowspan=6, columnspan=6)
        self.annoyance.grid(row=7, column=1, rowspan=6, columnspan=6)
        self.value_creator.grid(row=1, column=7, rowspan=6, columnspan=6)
        self.leisure.grid(row=7, column=7, rowspan=6, columnspan=6)
        self.matrix.grid(row=2, column=2)
        self.make_task()


    def make_task(self, task=None):
        global task_names
        id = task_ids.pop(0)
        if task == None:
            task_names[id] = Task(id, self.root, self.menu, self.todo, self.matrix)
            for x in task_names.keys():
                task_names[x].place(task_names[x].urgency, task_names[x].importance, task_names[x].unitM)
        else:
            task_names[id] = Task(id, self.root, self.menu, self.todo, self.matrix, task)


    def save_as(self):
        save_this = [[task_names[x].name.get(), task_names[x].urgency.get(), task_names[x].importance.get()] for x in task_names.keys()]
        with open(asksaveasfilename(), 'wb') as f:
            pickle.dump(save_this, f)


    def load_tasks(self):
        delete_this = []
        for x in task_names.keys():
            delete_this.append(task_names[x])
        while len(delete_this) != 0:
            delete_this[0].delete_task(delete_this[0].unitU, delete_this[0].unitI, delete_this[0].unitM)
            delete_this.pop(0)

        with open(askopenfilename(), 'rb') as f:
            load_this = pickle.load(f)
        for x in load_this:
            self.make_task(x)
        for x in task_names.keys():
            task_names[x].place(task_names[x].urgency, task_names[x].importance, task_names[x].unitM)


    def task_help(self):
        help = tk.Toplevel()
        help.title('Help Information')
        tk.Label(help, text=
            'This program creates dynamic Eisenhower matrixes from a\n'
            'set of tasks ranked by relative urgency and importance.\n'
            'Currently it supports a maximum of 12 different tasks.\n'
            'Save and Load functions, and support for greater numbers\n'
            'of tasks are currently in development.\n\n'

            'The "New Task" button creates a new task.\n'
            'The "Raise" and "Lower" buttons increase and decrease a \n'
            'task\'s relative urgency or importance ranking relative \n'
            'to other tasks.\n'
            'The Delete buttons will delete a task from both columns as\n'
            'well as from the matrix on the right-hand side.\n'
            'The Help button displays this information.\n'
            'The Quit button closes the program.\n'
            'You can change the name of a task in all three of the\n'
            'locations in which it is displayed by typing in either of\n'
            'its two text boxes on the left-hand side.\n\n'

            'The red quadrant contains tasks which are both relatively\n'
            'urgent and important. You can think of these as being like\n'
            'fires which need to be put out.\n'
            'The green quadrant contains tasks which are highly important,\n'
            'but which do not need to be completed quickly. It is believed\n'
            'to be ideal to strive to spend as much time on these tasks\n'
            'as possible.\n'
            'The yellow quadrant contains tasks which are urgent but\n'
            'relatively unimportant. They are essentially busy-work.\n'
            'The blue quadrant contains tasks which are neither urgent\n'
            'nor important relative to others. They can be done at your\n'
            'leisure.').pack(ipadx=15, ipady=15)
        tk.Button(help, text='Ok', command=help.destroy).pack()
        help.mainloop()


if __name__ == '__main__':
    window = Gui()
    window.root.mainloop()
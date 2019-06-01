"""
Eisenhower.py

Creates and dynamically re-orders an Eisenhower Matrix out of a list of tasks based on their relative importance and urgency.
Still crude and a little ugly with several buttons in the top menu that don't do anything, but it basically works.

A work in progress by:
Jon David Tannehill
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename, askdirectory
import os, sys, functools, operator, pickle, threading
#import PIL.ImageTk

global task_names
task_names = []


class Task():
    def __init__(self, root, menu, todo, matrix, data=None):
        if data == None:
            self.name = tk.StringVar(value='Task'+str(len(task_names)))
            self.urgency = tk.IntVar(value=len(task_names))
            self.importance = tk.IntVar(value=len(task_names))
        else:
            self.name = tk.StringVar(value=data[0])
            self.urgency = tk.IntVar(value=data[1])
            self.importance = tk.IntVar(value=data[2])

        self.unitM = tk.Label(matrix, textvariable=self.name, font='Times 10 bold', height=2, width=8)

        self.unitU = tk.Frame(todo)
        self.unitI = tk.Frame(todo)
        self.unitU.grid(row=self.urgency.get()+1, column=1)
        self.unitI.grid(row=self.importance.get()+1, column=2)
        self.itemU = tk.Entry(self.unitU, textvariable=self.name)
        self.increaseU = tk.Button(self.unitU, text='Raise', command=functools.partial(self.increase_urgency, self.unitU, self.urgency))
        self.decreaseU = tk.Button(self.unitU, text='Lower', command=functools.partial(self.decrease_urgency, self.unitU, self.urgency))
        self.deleteU = tk.Button(self.unitU, text='Delete', command=functools.partial(self.delete_task, self.name, self.urgency, self.importance, self.unitU, self.unitI, self.unitM))
        self.itemU.grid(row=1, column=1, columnspan=3)
        self.increaseU.grid(row=2, column=1)
        self.decreaseU.grid(row=2, column=2)
        self.deleteU.grid(row=2, column=3)

        self.itemI = tk.Entry(self.unitI, textvariable=self.name)
        self.increaseI = tk.Button(self.unitI, text='Raise', command=functools.partial(self.increase_importance, self.unitI, self.importance))
        self.decreaseI = tk.Button(self.unitI, text='Lower', command=functools.partial(self.decrease_importance, self.unitI, self.importance))
        self.deleteI = tk.Button(self.unitI, text='Delete', command=lambda: [threading.Thread(target=Gui.reconfigure), self.delete_task(self.name, self.urgency, self.importance, self.unitU, self.unitI, self.unitM)])
        self.itemI.grid(row=1, column=1, columnspan=3)
        self.increaseI.grid(row=2, column=1)
        self.decreaseI.grid(row=2, column=2)
        self.deleteI.grid(row=2, column=3)
        
        # debugging code below:
        print(self.name.get()+' initialized with', 'urgency '+str(self.urgency.get()), 'and importance '+str(self.importance.get()))
        print(task_names)


    def place(self, urgency, importance, unitM):
        base = 7 - ((len(task_names) // 2) + (len(task_names) % 2))
        rownum = base + importance.get()
        colnum = base + urgency.get()
        unitM.grid(row=rownum, column=colnum)


    def increase_urgency(self, unitU, urgency):
        if urgency.get() != 0:
            urgency.set(urgency.get()-1)
            for x in task_names:
                if x.urgency.get() == urgency.get() and x != self:
                    x.urgency.set(x.urgency.get()+1)
                    x.unitU.grid(row=x.urgency.get()+1, column=1)
                    unitU.grid(row=urgency.get()+1, column=1)
                    break
            for x in task_names:
                x.place(x.urgency, x.importance, x.unitM)
        # for debugging:
        print('\n', task_names)
        for x in task_names:
            print(x.name.get(), ' urgency: ', x.urgency.get(), sep='')


    def increase_importance(self, unitI, importance):
        if importance.get() != 0:
            importance.set(importance.get()-1)
            for x in task_names:
                if x.importance.get() == importance.get() and x != self:
                    x.importance.set(x.importance.get()+1)
                    x.unitI.grid(row=x.importance.get()+1, column=2)
                    unitI.grid(row=importance.get()+1, column=2)
                    break
            for x in task_names:
                x.place(x.urgency, x.importance, x.unitM)
        # for debugging:
        print('\n', task_names)
        for x in task_names:
            print(x.name.get(), ' importance: ', x.importance.get(), sep='')


    def decrease_urgency(self, unitU, urgency):
        for x in task_names:
            if x.urgency.get() > urgency.get():
                urgency.set(urgency.get()+1)
                unitU.grid(row=urgency.get()+1, column=1)
                break
        for x in task_names:
            if x.urgency.get() == urgency.get() and x != self:
                x.urgency.set(x.urgency.get()-1)
                x.unitU.grid(row=x.urgency.get()+1, column=1)
                break
        for x in task_names:
            x.place(x.urgency, x.importance, x.unitM)
        # for debugging: 
        print('\n', task_names)
        for x in task_names:
            print(x.name.get(), ' urgency: ', x.urgency.get(), sep='')


    def decrease_importance(self, unitI, importance):
        for x in task_names:
            if x.importance.get() > importance.get():
                importance.set(importance.get()+1)
                unitI.grid(row=importance.get()+1, column=2)
                break
        for x in task_names:
            if x.importance.get() == importance.get() and x != self:
                x.importance.set(x.importance.get()-1)
                x.unitI.grid(row=x.importance.get()+1, column=2)
                break
        for x in task_names:
            x.place(x.urgency, x.importance, x.unitM)
        # for debugging:
        print('\n', task_names)
        for x in task_names:
            print(x.name.get(), ' importance: ', x.importance.get(), sep='')


    def delete_task(self, name, urgency, importance, unitU, unitI, unitM):
        print('\nDELETING...')
        print('tasks:', task_names)
        for item in unitU.grid_slaves():
            item.grid_forget()
            del item
        for item in unitI.grid_slaves():
            item.grid_forget()
            del item
        unitU.grid_forget()
        unitI.grid_forget()
        unitM.grid_forget()
        del unitU, unitI, unitM
        del name, urgency, importance
        del self
        
        print('\nReconfiguring...\n')
        
        urgency_vals = []
        importance_vals = []
        for x in task_names:
            if x != self:
                urgency_vals.append([x.urgency, x.urgency.get()])
                importance_vals.append([x.importance, x.importance.get()])
        urgency_vals = sorted(urgency_vals, key=operator.itemgetter(1))
        importance_vals = sorted(importance_vals, key=operator.itemgetter(1))
        print('urgency_vals:', urgency_vals)
        print('importance_vals:', importance_vals)
        
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

            print('new urgency values:', urgency_vals)
            print('new importance values:', importance_vals)

            for x in task_names:
                if x != self:
                    x.unitU.grid(row=x.urgency.get()+1, column=1)
                    x.unitI.grid(row=x.importance.get()+1, column=2)
                    x.place(x.urgency, x.importance, x.unitM)

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
        to_scroll = tk.Scrollbar(self.todo)
        to_scroll.activate(index='slider')
        to_scroll.grid(row=1, column=3)
        self.todo.grid(row=2, column=1)
        
        # Why doesn't this work?
        # setting rowspan and columnspan values to span pushes task unitMs to bottom-right
        #if len(task_names) > 1:
        #    span = len(task_names) // 2 + 1
        #else:
        #    span = 1
        #start_point2 = span + 1
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
        if task == None:
            task_names.append(Task(self.root, self.menu, self.todo, self.matrix))
            for x in task_names:
                x.place(x.urgency, x.importance, x.unitM)
        else:
            task_names.append(Task(self.root, self.menu, self.todo, self.matrix, task))
            for x in task_names:
                x.place(x.urgency, x.importance, x.unitM)


    def save_as(self):
        save_this = [[x.name.get(), x.urgency.get(), x.importance.get()] for x in task_names]
        with open(asksaveasfilename(), 'wb') as f:
            pickle.dump(save_this, f)


    def load_tasks(self):
        delete_this = []
        for x in task_names:
            delete_this.append(x)
        while len(delete_this) != 0:
            delete_this[0].delete_task(x.name, x.urgency, x.importance, x.unitU, x.unitI, x.unitM)
            delete_this.pop(0)

        with open(askopenfilename(), 'rb') as f:
            load_this = pickle.load(f)
        for x in load_this:
            self.make_task(x)


    def task_help(self):
        help = tk.Toplevel()
        help.title('Help Information')
        tk.Label(help, text='This box will contain useful information on the application and Eisenhower matrixes in general.').pack(ipadx=15, ipady=15)
        tk.Button(help, text='Ok', command=help.destroy).pack()
        help.mainloop()


    def reconfigure():
        time.sleep(0.05)
        print('\nReconfiguring...\n')
        urgency_vals = []
        importance_vals = []
        for x in task_names:
                urgency_vals.append([x.urgency, x.urgency.get()])
                importance_vals.append([x.importance, x.importance.get()])
        urgency_vals = sorted(urgency_vals, key=operator.itemgetter(1))
        importance_vals = sorted(importance_vals, key=operator.itemgetter(1))
        print('urgency_vals:', urgency_vals)
        print('importance_vals:', importance_vals)
        
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

            print('new urgency values:', urgency_vals)
            print('new importance values:', importance_vals)

            for x in task_names:
                    x.unitU.grid(row=x.urgency.get()+1, column=1)
                    x.unitI.grid(row=x.importance.get()+1, column=2)
                    x.place(x.urgency, x.importance, x.unitM)


if __name__ == '__main__':
    window = Gui()
    window.root.mainloop()
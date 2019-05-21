import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import functools, sys

global task_names
task_names = {}

class Task():
    def __init__(self, root, menu, todo, matrix):
        self.name = tk.StringVar(value='Task '+str(len(task_names)))
        self.urgency = tk.IntVar(value=len(task_names))
        self.importance = tk.IntVar(value=len(task_names))

        #placement = categorize(self.urgency, self.importance)
        self.unitU = tk.Frame(todo)
        self.unitI = tk.Frame(todo)
        self.unitM = tk.Frame()
        self.unitU.grid(row=self.urgency.get()+1, column=1)
        self.unitI.grid(row=self.importance.get()+1, column=2)
        self.itemU = tk.Entry(self.unitU, textvariable=self.name)
        self.increaseU = tk.Button(self.unitU, text='Raise', command=functools.partial(self.increase_urgency, self.unitU, self.urgency))
        self.decreaseU = tk.Button(self.unitU, text='Lower', command=functools.partial(self.decrease_urgency, self.unitU, self.urgency))
        self.deleteU = tk.Button(self.unitU, text='Delete', command=functools.partial(self.delete_task, self.unitU, self.unitI, self.itemU))
        self.itemU.grid(row=1, column=1, columnspan=3)
        self.increaseU.grid(row=2, column=1)
        self.decreaseU.grid(row=2, column=2)
        self.deleteU.grid(row=2, column=3)

        self.itemI = tk.Entry(self.unitI, textvariable=self.name)
        self.increaseI = tk.Button(self.unitI, text='Raise', command=functools.partial(self.increase_importance, self.unitI, self.importance))
        self.decreaseI = tk.Button(self.unitI, text='Lower', command=functools.partial(self.decrease_importance, self.unitI, self.importance))
        self.deleteI = tk.Button(self.unitI, text='Delete', command=functools.partial(self.delete_task, self.unitU, self.unitI, self.itemI))
        self.itemI.grid(row=1, column=1, columnspan=3)
        self.increaseI.grid(row=2, column=1)
        self.decreaseI.grid(row=2, column=2)
        self.deleteI.grid(row=2, column=3)
        # debugging code below:
        print(self.name.get()+' initialized with', 'urgency '+str(self.urgency.get()), 'and importance '+str(self.importance.get()))
        print(task_names)

    def categorize(self, urgency, importance):
        pass

    def increase_urgency(self, unitU, urgency):
        if urgency.get() != 0:
            urgency.set(urgency.get()-1)
            for x in task_names.keys():
                if task_names[x].urgency.get() == urgency.get() and task_names[x] != self:
                    task_names[x].urgency.set(task_names[x].urgency.get()+1)
                    task_names[x].unitU.grid(row=task_names[x].urgency.get()+1, column=1)
                    unitU.grid(row=urgency.get()+1, column=1)
                    break
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
        # for debugging:
        print()
        for x in task_names.keys():
            print(task_names[x].name.get(), ' importance: ', task_names[x].importance.get(), sep='')

    def delete_task(self, unitU, unitI, item):
        unitU.grid_forget()
        unitI.grid_forget()
        for x in task_names.keys():
            if task_names[x] == self:
                del task_names[x]
                break
        print('\nDELETING...')
        print('tasks:', task_names)
        # need code to rearrange items in grids...
        del self
        
    def reconfigure(self):
        pass


class Gui():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Eisenhower Matrix')
        widthR = str(int(self.root.winfo_screenwidth()))
        heightR = str(int(self.root.winfo_screenheight()))
        self.root.geometry(widthR + 'x' + heightR)

        self.task_ids = ['task' + str(x) for x in range(100)]

        self.menu = tk.Frame(self.root)
        self.new_task = tk.Button(self.menu, text='New Task', command=functools.partial(self.make_task, self.task_ids))
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
        self.menu.pack(side='top') # grid? something else?
        
        self.todo = tk.Frame(self.root)
        self.todo.pack(side='left', expand='False') # grid? something else?
        
        self.matrix = tk.Frame(self.root)
        self.fires = tk.Frame(self.matrix, background='red', width=400, height=300)
        self.annoyances = tk.Frame(self.matrix, background='orange', width=400, height=300)
        self.value_creators = tk.Frame(self.matrix, background='green', width=400, height=300)
        self.leisures = tk.Frame(self.matrix, background='blue', width=400, height=300)
        self.fires.grid(row=1, column=1)
        self.annoyances.grid(row=2, column=1)
        self.value_creators.grid(row=1, column=2)
        self.leisures.grid(row=2, column=2)
        self.matrix.pack(side='right', expand='True', fill='both') # grid? something else?

        self.make_task(self.task_ids)

    def make_task(self, task_ids):
        global task_names
        task_names[task_ids.pop(0)] = Task(self.root, self.menu, self.todo, self.matrix)

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


if __name__ == '__main__':
    window = Gui()
    window.root.mainloop()

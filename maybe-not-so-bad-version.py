import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import functools

global tasks, task_ids
tasks = {}
task_ids = ['task' + str(x) for x in range(100)]

class Task():
    def __init__(self, root, menu, todo, matrix):
        global tasks
        self.name = tk.StringVar(value='Task '+str(len(tasks)))
        self.urgency = tk.IntVar(value=len(tasks))
        self.importance = tk.IntVar(value=len(tasks))
        tasks[self] = [self.name, self.urgency, self.importance]

        self.unitU = tk.Frame(todo)
        self.unitI = tk.Frame(todo)
        self.unitU.grid(row=self.urgency.get()+1, column=1)
        self.unitI.grid(row=self.importance.get()+1, column=2)
        self.itemU = tk.Entry(self.unitU, textvariable=self.name)
        self.increaseU = tk.Button(self.unitU, text='Raise', command=functools.partial(self.increase_urgency, self.unitU, self.unitI))
        self.decreaseU = tk.Button(self.unitU, text='Lower', command=functools.partial(self.decrease_urgency, self.unitU, self.unitI))
        self.deleteU = tk.Button(self.unitU, text='Delete', command=functools.partial(self.delete_task, self.unitU, self.unitI, self.itemU))
        self.itemU.grid(row=1, column=1, columnspan=3)
        self.increaseU.grid(row=2, column=1)
        self.decreaseU.grid(row=2, column=2)
        self.deleteU.grid(row=2, column=3)

        self.itemI = tk.Entry(self.unitI, textvariable=self.name)
        self.increaseI = tk.Button(self.unitI, text='Raise', command=functools.partial(self.increase_urgency, self.unitU, self.unitI))
        self.decreaseI = tk.Button(self.unitI, text='Lower', command=functools.partial(self.decrease_urgency, self.unitU, self.unitI))
        self.deleteI = tk.Button(self.unitI, text='Delete', command=functools.partial(self.delete_task, self.unitU, self.unitI, self.itemI))
        self.itemI.grid(row=1, column=1, columnspan=3)
        self.increaseI.grid(row=2, column=1)
        self.decreaseI.grid(row=2, column=2)
        self.deleteI.grid(row=2, column=3)
        # debugging code below:
        print(self.name.get()+' initialized with', 'urgency '+str(self.urgency.get()), 'and importance '+str(self.importance.get()))
        print('Tasks: ', tasks)

    def increase_urgency(self, unitU, unitI):
        if self.urgency.get() != 0:
            self.urgency.set(self.urgency.get()-1)
        for x in tasks:
            if list(tasks[x])[1].get() == self.urgency.get():
                list(tasks[x])[1].set(list(tasks[x])[1].get()+1)
                unitU.grid(row=self.urgency.get()+1, column=1)
                tasks[x].unitU.grid(row=list(tasks[x])[1].get()+1, column=1)
    
    def increase_importance(self, unitU, unitI):
        pass
    
    def decrease_urgency(self, unitU, unitI):
        pass
    
    def decrease_importance(self, unitU, unitI):
        pass

    def delete_task(self, unitU, unitI, item):
        # this part works
        unitU.grid_forget()
        unitI.grid_forget()
        # this part doesn't
        for x in tasks:
            if x == self:
                del tasks[x]
                del x
        print(tasks)
    
    def reconfigure(self):
        pass


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
        self.menu.pack(side='top') # grid? something else?
        
        self.todo = tk.Frame(self.root)
        self.todo.pack(side='left', expand='False') # grid? something else?
        
        self.matrix = tk.Frame(self.root)
        self.matrix.pack(side='right', expand='True', fill='both') # grid? something else?

        self.make_task()

    def make_task(self):
        global tasks, task_ids
        tasks[task_ids.pop(0)] = Task(self.root, self.menu, self.todo, self.matrix)
        """
        else:
            local_ids = task_ids
            for x in tasks.keys():
                #print(x)
                print(x.name.get())
                if x.name.get() in local_ids:
                    local_ids.remove(x.name.get())
            tasks[local_ids[0]] = Task(self.root, self.menu, self.todo, self.matrix)
        """

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

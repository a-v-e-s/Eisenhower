import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
import functools, sys

global task_names, task_ids
task_names = {}
task_ids = ['task' + str(x) for x in range(100)]

class Task():
    def __init__(self, root, menu, todo, matrix):
        self.name = tk.StringVar(value='Task '+str(len(task_names)))
        self.urgency = tk.IntVar(value=len(task_names))
        self.importance = tk.IntVar(value=len(task_names))

        self.unitU = tk.Frame(todo)
        self.unitI = tk.Frame(todo)
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

        category, rownum, colnum = self.categorize(self.urgency, self.importance)
        self.unitM = tk.Frame(matrix, width=100, height=50)
        self.itemM = tk.Entry(self.unitM, textvariable=self.name)
        self.unitM.grid(row=rownum, column=colnum)

        # debugging code below:
        print(self.name.get()+' initialized with', 'urgency '+str(self.urgency.get()), 'and importance '+str(self.importance.get()))
        print(task_names)

    def categorize(self, urgency, importance):
        global task_names
        category = 1
        rownum = 1
        colnum = 1
        if len(task_names) % 4 == 1:
            category = 'leisure'
            rownum = 1
            colnum = 1
        return category, rownum, colnum

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
        global task_names, task_ids
        unitU.grid_forget()
        unitI.grid_forget()
        for x in task_names.keys():
            if task_names[x] == self:
                task_ids.insert(0, x)
                del task_names[x]
                break
        self.reconfigure()
        del self
        # debugging information:
        print('\nDELETING...')
        print('tasks:', task_names)
        print('\nReconfiguring...\n')
        
    def reconfigure(self):
        global task_names
        urgency_slots = []
        urgency_slots1 = []
        importance_slots = []
        importance_slots1 = []
        for x in task_names.keys():
            urgency_slots.append(task_names[x].urgency)
            importance_slots.append(task_names[x].importance)
        
        for x in importance_slots:
            importance_slots1.append(x.get())
        importance_slots1.sort()
        for x in range(len(importance_slots1)-1):
            if importance_slots1[x] == importance_slots1[x+1] - 2:
                importance_slots1[x+1] -= 1
        print('importance_slots:\n', importance_slots1)

        for x in urgency_slots:
            urgency_slots1.append(x.get())
        urgency_slots1.sort()
        for x in range(len(urgency_slots1)-1):
            if urgency_slots1[x] == urgency_slots1[x+1] -2:
                urgency_slots1[x+1] -= 1
        print('urgency_slots:\n', urgency_slots1)

        for x in task_names.keys():
            task_names[x].unitU.grid(row=task_names[x].urgency.get()+1, column=1)
            task_names[x].unitI.grid(row=task_names[x].importance.get()+1, column=2)


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
        self.todo.grid(row=2, column=1)
        
        self.matrix = tk.Frame(self.root)
        tk.Label(self.matrix, text='<----Increasing Urgency----<').grid(row=0, column=0, columnspan=3)
        tk.Label(self.matrix, text='^\n^\n^\n^\n^\n\n\nI\nn\nc\nr\ne\na\ns\ni\nn\ng\n \nI\nm\np\no\nr\nt\na\nn\nc\ne\n\n\n^\n^\n^\n^\n^').grid(row=1, column=0, rowspan=2)
        self.fire = tk.Frame(self.matrix, background='red', width=400, height=300)
        self.annoyance = tk.Frame(self.matrix, background='orange', width=400, height=300)
        self.value_creator = tk.Frame(self.matrix, background='green', width=400, height=300)
        self.leisure = tk.Frame(self.matrix, background='blue', width=400, height=300)
        self.fire.grid(row=1, column=1)
        self.annoyance.grid(row=2, column=1)
        self.value_creator.grid(row=1, column=2)
        self.leisure.grid(row=2, column=2)
        self.matrix.grid(row=2, column=2)
        """
        self.transparent = tk.PhotoImage(file='Transparent.png')
        self.topmatrix = tk.Canvas(self.root, )
        self.topmatrix.grid(row=2, column=2)
        """
        self.make_task()

    def make_task(self):
        global task_names, task_ids
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

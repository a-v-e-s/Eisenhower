"""
Eisenhower.py

Creates and dynamically re-orders an Eisenhower Matrix out of a list of tasks based on their relative importance and urgency.
Still crude and a little ugly, but it basically works.

A work in progress by:
Jon David Tannehill
"""

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksave_asfilename
import functools, operator, pickle

global tasks, task_ids
tasks = {}
task_ids = ['task' + str(x) for x in range(100)]


class Task():
    def __init__(self, id, root, menu, todo, matrix, data=None):
        if data == None:
            self.name = tk.StringVar(value=id)
            self.urgency = tk.IntVar(value=len(tasks))
            self.importance = tk.IntVar(value=len(tasks))
        else:
            self.name = tk.StringVar(value=data[0])
            self.urgency = tk.IntVar(value=data[1])
            self.importance = tk.IntVar(value=data[2])

        self.mtrx_label = tk.Label(matrix, textvariable=self.name, font='Times 10 bold', height=2, width=8, wraplength=62)

        self.frm_urgency = tk.Frame(todo)
        self.frm_importance = tk.Frame(todo)
        self.frm_urgency.grid(row=self.urgency.get()+1, column=1)
        self.frm_importance.grid(row=self.importance.get()+1, column=2)
        self.ent_urgency = tk.Entry(self.frm_urgency, textvariable=self.name)
        self.urg_raise = tk.Button(self.frm_urgency, text='Raise', command=functools.partial(self.increase_urgency, self.frm_urgency, self.urgency))
        self.urg_lower = tk.Button(self.frm_urgency, text='Lower', command=functools.partial(self.decrease_urgency, self.frm_urgency, self.urgency))
        self.urg_del = tk.Button(self.frm_urgency, text='Delete', command=functools.partial(self.delete_task, self.frm_urgency, self.frm_importance, self.mtrx_label))
        self.ent_urgency.grid(row=1, column=1, columnspan=3)
        self.urg_raise.grid(row=2, column=1)
        self.urg_lower.grid(row=2, column=2)
        self.urg_del.grid(row=2, column=3)

        self.ent_importance = tk.Entry(self.frm_importance, textvariable=self.name)
        self.imp_raise = tk.Button(self.frm_importance, text='Raise', command=functools.partial(self.increase_importance, self.frm_importance, self.importance))
        self.imp_lower = tk.Button(self.frm_importance, text='Lower', command=functools.partial(self.decrease_importance, self.frm_importance, self.importance))
        self.imp_del = tk.Button(self.frm_importance, text='Delete', command=functools.partial(self.delete_task, self.frm_urgency, self.frm_importance, self.mtrx_label))
        self.ent_importance.grid(row=1, column=1, columnspan=3)
        self.imp_raise.grid(row=2, column=1)
        self.imp_lower.grid(row=2, column=2)
        self.imp_del.grid(row=2, column=3)


    def place(self, urgency, importance, mtrx_label):
        base = 7 - ((len(tasks) // 2) + (len(tasks) % 2))
        rownum = base + importance.get()
        colnum = base + urgency.get()
        mtrx_label.grid(row=rownum, column=colnum)


    def increase_urgency(self, frm_urgency, urgency):
        if urgency.get() != 0:
            urgency.set(urgency.get()-1)
            for x in tasks.keys():
                if tasks[x].urgency.get() == urgency.get() and tasks[x] != self:
                    tasks[x].urgency.set(tasks[x].urgency.get()+1)
                    tasks[x].frm_urgency.grid(row=tasks[x].urgency.get()+1, column=1)
                    frm_urgency.grid(row=urgency.get()+1, column=1)
                    break
            for x in tasks.keys():
                tasks[x].place(tasks[x].urgency, tasks[x].importance, tasks[x].mtrx_label)


    def increase_importance(self, frm_importance, importance):
        if importance.get() != 0:
            importance.set(importance.get()-1)
            for x in tasks.keys():
                if tasks[x].importance.get() == importance.get() and tasks[x] != self:
                    tasks[x].importance.set(tasks[x].importance.get()+1)
                    tasks[x].frm_importance.grid(row=tasks[x].importance.get()+1, column=2)
                    frm_importance.grid(row=importance.get()+1, column=2)
                    break
            for x in tasks.keys():
                tasks[x].place(tasks[x].urgency, tasks[x].importance, tasks[x].mtrx_label)


    def decrease_urgency(self, frm_urgency, urgency):
        for x in tasks.keys():
            if tasks[x].urgency.get() > urgency.get():
                urgency.set(urgency.get()+1)
                frm_urgency.grid(row=urgency.get()+1, column=1)
                break
        for x in tasks.keys():
            if tasks[x].urgency.get() == urgency.get() and tasks[x] != self:
                tasks[x].urgency.set(tasks[x].urgency.get()-1)
                tasks[x].frm_urgency.grid(row=tasks[x].urgency.get()+1, column=1)
                break
        for x in tasks.keys():
            tasks[x].place(tasks[x].urgency, tasks[x].importance, tasks[x].mtrx_label)


    def decrease_importance(self, frm_importance, importance):
        for x in tasks.keys():
            if tasks[x].importance.get() > importance.get():
                importance.set(importance.get()+1)
                frm_importance.grid(row=importance.get()+1, column=2)
                break
        for x in tasks.keys():
            if tasks[x].importance.get() == importance.get() and tasks[x] != self:
                tasks[x].importance.set(tasks[x].importance.get()-1)
                tasks[x].frm_importance.grid(row=tasks[x].importance.get()+1, column=2)
                break
        for x in tasks.keys():
            tasks[x].place(tasks[x].urgency, tasks[x].importance, tasks[x].mtrx_label)


    def delete_task(self, frm_urgency, frm_importance, mtrx_label):
        global task_ids
        frm_urgency.grid_forget()
        frm_importance.grid_forget()
        mtrx_label.grid_forget()
        for x in tasks.keys():
            if tasks[x] == self:
                task_ids.insert(0, x)
                del tasks[x]
                break
        
        urgency_vals = []
        importance_vals = []
        for x in tasks.keys():
            urgency_vals.append([tasks[x].urgency, tasks[x].urgency.get()])
            importance_vals.append([tasks[x].importance, tasks[x].importance.get()])
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

            for x in tasks.keys():
                tasks[x].frm_urgency.grid(row=tasks[x].urgency.get()+1, column=1)
                tasks[x].frm_importance.grid(row=tasks[x].importance.get()+1, column=2)
                tasks[x].place(tasks[x].urgency, tasks[x].importance, tasks[x].mtrx_label)

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
        self.save_as = tk.Button(self.menu, text='Save As', command=self.save_as)
        self.save_as.pack(side='left')
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
        self.busy_work = tk.Frame(self.matrix, background='orange', width=400, height=300)
        self.value_creator = tk.Frame(self.matrix, background='green', width=400, height=300)
        self.leisure = tk.Frame(self.matrix, background='blue', width=400, height=300)
        self.fire.grid(row=1, column=1, rowspan=6, columnspan=6)
        self.busy_work.grid(row=7, column=1, rowspan=6, columnspan=6)
        self.value_creator.grid(row=1, column=7, rowspan=6, columnspan=6)
        self.leisure.grid(row=7, column=7, rowspan=6, columnspan=6)
        self.matrix.grid(row=2, column=2)
        
        self.make_task()


    def make_task(self, task=None):
        global tasks
        id = task_ids.pop(0)
        if task == None:
            tasks[id] = Task(id, self.root, self.menu, self.todo, self.matrix)
            for x in tasks.keys():
                tasks[x].place(tasks[x].urgency, tasks[x].importance, tasks[x].mtrx_label)
        else:
            tasks[id] = Task(id, self.root, self.menu, self.todo, self.matrix, task)


    def save_as(self):
        save_this = [[tasks[x].name.get(), tasks[x].urgency.get(), tasks[x].importance.get()] for x in tasks.keys()]
        with open(asksave_asfilename(), 'wb') as f:
            pickle.dump(save_this, f)


    def load_tasks(self):
        delete_this = []
        for x in tasks.keys():
            delete_this.append(tasks[x])
        while len(delete_this) != 0:
            delete_this[0].delete_task(delete_this[0].frm_urgency, delete_this[0].frm_importance, delete_this[0].mtrx_label)
            delete_this.pop(0)

        with open(askopenfilename(), 'rb') as f:
            load_this = pickle.load(f)
        for x in load_this:
            self.make_task(x)
        for x in tasks.keys():
            tasks[x].place(tasks[x].urgency, tasks[x].importance, tasks[x].mtrx_label)


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
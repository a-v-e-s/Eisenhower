"""
eisenhower.py

Author: Jon David Tannehill
"""

from task import Task
import cfg
import tkinter as tk
import pickle
from tkinter.filedialog import askopenfilename, asksaveasfilename


class Gui():
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Eisenhower Matrix')
        root_width = str(int(self.root.winfo_screenwidth()))
        root_height = str(int(self.root.winfo_screenheight()))
        self.root.geometry(root_width + 'x' + root_height)

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
        id = cfg.task_ids.pop(0)
        if task == None:
            cfg.tasks[id] = Task(id, self.root, self.menu, self.todo, self.matrix)
            for x in cfg.tasks.keys():
                cfg.tasks[x].place(cfg.tasks[x].urgency, cfg.tasks[x].importance, cfg.tasks[x].mtrx_label)
        else:
            cfg.tasks[id] = Task(id, self.root, self.menu, self.todo, self.matrix, task)


    def save_as(self):
        save_this = [[cfg.tasks[x].name.get(), cfg.tasks[x].urgency.get(), cfg.tasks[x].importance.get()] for x in cfg.tasks.keys()]
        with open(asksaveasfilename(), 'wb') as f:
            pickle.dump(save_this, f)


    def load_tasks(self):
        delete_this = []
        for x in cfg.tasks.keys():
            delete_this.append(cfg.tasks[x])
        while len(delete_this) != 0:
            delete_this[0].delete_task(delete_this[0].frm_urgency, delete_this[0].frm_importance, delete_this[0].mtrx_label)
            delete_this.pop(0)

        with open(askopenfilename(), 'rb') as f:
            load_this = pickle.load(f)
        for x in load_this:
            self.make_task(x)
        for x in cfg.tasks.keys():
            cfg.tasks[x].place(cfg.tasks[x].urgency, cfg.tasks[x].importance, cfg.tasks[x].mtrx_label)


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
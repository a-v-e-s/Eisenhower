"""
task.py

Author: Jon David Tannehill
"""

import tkinter as tk
import functools, operator
import cfg


class Task():
    def __init__(self, id, root, menu, todo, matrix, data=None):
        if data == None:
            self.name = tk.StringVar(value=id)
            self.urgency = tk.IntVar(value=len(cfg.tasks))
            self.importance = tk.IntVar(value=len(cfg.tasks))
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
        base = 7 - ((len(cfg.tasks) // 2) + (len(cfg.tasks) % 2))
        rownum = base + importance.get()
        colnum = base + urgency.get()
        mtrx_label.grid(row=rownum, column=colnum)


    def increase_urgency(self, frm_urgency, urgency):
        if urgency.get() != 0:
            urgency.set(urgency.get()-1)
            for x in cfg.tasks.keys():
                if cfg.tasks[x].urgency.get() == urgency.get() and cfg.tasks[x] != self:
                    cfg.tasks[x].urgency.set(cfg.tasks[x].urgency.get()+1)
                    cfg.tasks[x].frm_urgency.grid(row=cfg.tasks[x].urgency.get()+1, column=1)
                    frm_urgency.grid(row=urgency.get()+1, column=1)
                    break
            for x in cfg.tasks.keys():
                cfg.tasks[x].place(cfg.tasks[x].urgency, cfg.tasks[x].importance, cfg.tasks[x].mtrx_label)


    def increase_importance(self, frm_importance, importance):
        if importance.get() != 0:
            importance.set(importance.get()-1)
            for x in cfg.tasks.keys():
                if cfg.tasks[x].importance.get() == importance.get() and cfg.tasks[x] != self:
                    cfg.tasks[x].importance.set(cfg.tasks[x].importance.get()+1)
                    cfg.tasks[x].frm_importance.grid(row=cfg.tasks[x].importance.get()+1, column=2)
                    frm_importance.grid(row=importance.get()+1, column=2)
                    break
            for x in cfg.tasks.keys():
                cfg.tasks[x].place(cfg.tasks[x].urgency, cfg.tasks[x].importance, cfg.tasks[x].mtrx_label)


    def decrease_urgency(self, frm_urgency, urgency):
        for x in cfg.tasks.keys():
            if cfg.tasks[x].urgency.get() > urgency.get():
                urgency.set(urgency.get()+1)
                frm_urgency.grid(row=urgency.get()+1, column=1)
                break
        for x in cfg.tasks.keys():
            if cfg.tasks[x].urgency.get() == urgency.get() and cfg.tasks[x] != self:
                cfg.tasks[x].urgency.set(cfg.tasks[x].urgency.get()-1)
                cfg.tasks[x].frm_urgency.grid(row=cfg.tasks[x].urgency.get()+1, column=1)
                break
        for x in cfg.tasks.keys():
            cfg.tasks[x].place(cfg.tasks[x].urgency, cfg.tasks[x].importance, cfg.tasks[x].mtrx_label)


    def decrease_importance(self, frm_importance, importance):
        for x in cfg.tasks.keys():
            if cfg.tasks[x].importance.get() > importance.get():
                importance.set(importance.get()+1)
                frm_importance.grid(row=importance.get()+1, column=2)
                break
        for x in cfg.tasks.keys():
            if cfg.tasks[x].importance.get() == importance.get() and cfg.tasks[x] != self:
                cfg.tasks[x].importance.set(cfg.tasks[x].importance.get()-1)
                cfg.tasks[x].frm_importance.grid(row=cfg.tasks[x].importance.get()+1, column=2)
                break
        for x in cfg.tasks.keys():
            cfg.tasks[x].place(cfg.tasks[x].urgency, cfg.tasks[x].importance, cfg.tasks[x].mtrx_label)


    def delete_task(self, frm_urgency, frm_importance, mtrx_label):
        frm_urgency.grid_forget()
        frm_importance.grid_forget()
        mtrx_label.grid_forget()
        for x in cfg.tasks.keys():
            if cfg.tasks[x] == self:
                cfg.task_ids.insert(0, x)
                del cfg.tasks[x]
                break
        
        urgency_vals = []
        importance_vals = []
        for x in cfg.tasks.keys():
            urgency_vals.append([cfg.tasks[x].urgency, cfg.tasks[x].urgency.get()])
            importance_vals.append([cfg.tasks[x].importance, cfg.tasks[x].importance.get()])
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

            for x in cfg.tasks.keys():
                cfg.tasks[x].frm_urgency.grid(row=cfg.tasks[x].urgency.get()+1, column=1)
                cfg.tasks[x].frm_importance.grid(row=cfg.tasks[x].importance.get()+1, column=2)
                cfg.tasks[x].place(cfg.tasks[x].urgency, cfg.tasks[x].importance, cfg.tasks[x].mtrx_label)

        del self
import os
import time
import graphviz
import threading
import tkinter as tk
from tkinter import ttk
from tkinter import PhotoImage
from Node import Node

class Visualizer:
    """Tkinter interface for visualizing Global States and Distributed Snapshots of processes and their tasks."""

    msg_colors = {"request":"maroon", "token":"gold", "election":"blue", "coordinator":"purple"}
    format = "png"


    def __init__(self, img_folder="default", autocapture=False):
        # autocapture permits to capture tree when system state change (token move, leader election, ...)
        # but it's not good for showing events that are happening at the same time
        self.img_folder = 'tree_img/'+img_folder
        self.clear_img_folder()
        self.nb_img = 0
        self.autocapture = autocapture
        self.nodes = []
        self.edges = []         # format: [(node1, node2)]      -> represents channels betweeen processes
        self.edges_msg = {}     # format: {(sender_node, receiver_node): message_type}
        self.nodeWithToken = None
        self.nodeLeader = None
        self.request_queues = {}
        self._create_interface()
    
    def setNodes(self, nodes:[Node]):
        self.nodes = nodes


    def setEdges(self, edges:[[Node, Node]]):
        self.edges = []
        self.edges_msg = {}
        for node1,node2 in edges:
            self.edges.append((node1, node2))


    def moveToken(self, node:Node):
        self.nodeWithToken = node
        if self.autocapture: self.capture()
    

    def setLeader(self, node:Node):
        self.nodeLeader = node
        if self.autocapture: self.capture()
    

    def messageTransit(self, sender:Node, receiver:Node, msg_type:str):
        self.edges_msg[(sender, receiver)] = msg_type
    
    
    def clearTransit(self):
        self.edges_msg = {}
    

    def capture(self):
        # Build tree processes system and save as SVG
        tree = graphviz.Digraph(filename=str(self.nb_img), format=Visualizer.format)
        
        for node in self.nodes:
            border_color = "red" if node == self.nodeLeader else "black"
            if node == self.nodeWithToken:
                tree.node(str(node.id), color=border_color, style='filled', fillcolor='yellow')
            else:
                tree.node(str(node.id), color=border_color, style='solid')
        
        for node1, node2 in self.edges:
            if (node1,node2) in self.edges_msg:
                # message transits from father to son -> display directed link to the son
                msg_type = self.edges_msg[(node1,node2)]
                color = Visualizer.msg_colors[msg_type] if msg_type in Visualizer.msg_colors else "black"
                tree.edge(str(node1.id), str(node2.id), color=color, dir='forward')
            
            elif (node2,node1) in self.edges_msg:
                # message transits from son to father -> display directed link to the father
                msg_type = self.edges_msg[(node2,node1)]
                color = Visualizer.msg_colors[msg_type] if msg_type in Visualizer.msg_colors else "black"
                tree.edge(str(node1.id), str(node2.id), color=color, dir='back')    # trick to keep same tree structure with edge from father to son but inversed arrow
            
            else:
                # no message transits -> display simple link to represent channel between processes
                tree.edge(str(node1.id), str(node2.id), color="black", dir='none')
        
            # Save request queues of processes
            self.request_queues[self.nb_img] = {node.id: list(map(lambda x: str(x), node.request_queue)) for node in self.nodes}

        self.nb_img += 1
        return tree.render(directory=self.img_folder)


    def clear_img_folder(self):
        if os.path.isdir(self.img_folder):
            for file in os.listdir(self.img_folder):
                try: os.remove(self.img_folder+'/'+file)
                except: continue
    

    def _create_interface(self):
        self.root = tk.Tk()
        self.root.title("Raymond's Algorithm & Leader Election")
        tk.Label(self.root, text="Raymond's Algorithm & Leader Election", font="Arial 20").pack()
        
        # Control buttons
        controls = tk.Frame(self.root)
        controls.pack(pady=20)
        self.btn_autoplay = tk.Button(controls, text="▶", command=self._play_stop, fg="blue", font='Arial 20 bold')
        self.btn_back = tk.Button(controls, text="⏮", command=self._back, fg="blue", font='Arial 20 bold')
        self.btn_forward = tk.Button(controls, text="⏭", command=self._forward, fg="blue", font='Arial 18 bold')
        self.progress_bar = ttk.Progressbar(controls, length=400)
        self.btn_back.grid(row=0, column=0, padx=30)
        self.btn_autoplay.grid(row=0, column=1, padx=30)
        self.btn_forward.grid(row=0, column=2, padx=30)
        self.progress_bar.grid(row=1, column=0, columnspan=3, pady=10)

        # Tree System & Table of Request Queues
        system_infos = tk.Frame(self.root)
        system_infos.pack(padx=20, pady=20)
        self.tree_system = tk.Label(system_infos)
        self.tree_system.grid(row=0, column=0, padx=30)
        self.fifo_req_table = tk.Frame(system_infos)
        self.fifo_req_table.grid(row=0, column=1, padx=30)
        tk.Label(self.fifo_req_table, bg="white", font='Arial 14 bold', text="Process", relief="groove", width=7).grid(row=0, column=0)
        tk.Label(self.fifo_req_table, bg="white", font='Arial 14 bold', text="Requests Queue", relief="groove", width=20).grid(row=0, column=1)

        # Legend
        legend = tk.Frame(self.root, bg="white")
        legend.pack(padx=20, pady=10)
        tk.Label(legend, bg="yellow", font='Arial 12 bold', text="Token holder").grid(row=0, column=0, padx=15, pady=5)
        frame = tk.Frame(legend, background="red")
        frame.grid(row=0, column=1, padx=17, pady=5)
        tk.Label(frame, bg="white", font='Arial 12 bold', text="Leader").pack(padx=2, pady=2)
        tk.Label(legend, bg="white", font='Arial 12 bold', text="→ Request", fg=Visualizer.msg_colors['request']).grid(row=0, column=2, padx=15, pady=5)
        tk.Label(legend, bg="white", font='Arial 12 bold', text="→ Token", fg=Visualizer.msg_colors['token']).grid(row=0, column=3, padx=15, pady=5)
        tk.Label(legend, bg="white", font='Arial 12 bold', text="→ Election", fg=Visualizer.msg_colors['election']).grid(row=0, column=4, padx=15, pady=5)
        tk.Label(legend, bg="white", font='Arial 12 bold', text="→ Coordinator", fg=Visualizer.msg_colors['coordinator']).grid(row=0, column=5, padx=15, pady=5)
    

    def _back(self):
        self.step = max(self.step - 1, 0)
        self._update_system()
    

    def _forward(self):
        self.step = min(self.step + 1, self.nb_img-1)
        self._update_system()
    

    def _play_stop(self):
        if self.thread_autoplaying == None:
            self.thread_autoplaying = threading.Thread(target=self._autoplay)
            self.thread_autoplaying.start()
            self.btn_autoplay.configure(text="⏸")
        else:
            self.thread_autoplaying = None
            self.btn_autoplay.configure(text="▶")
    

    def _autoplay(self):
        while self.step < self.nb_img-1:
            time.sleep(2)
            if self.thread_autoplaying != None:
                self._forward()
            else: return
        self.thread_autoplaying = None
        self.btn_autoplay.configure(text="▶")
    

    def _update_system(self):
        try:
            self.progress_bar.config(value= self.step/(self.nb_img-1)*100)   # percentage of progression
            # update image
            image = PhotoImage(file=self.img_folder+'/'+str(self.step)+"."+Visualizer.format)
            self.tree_system.configure(image=image)
            self.tree_system.image = image
            # update table
            for node in self.nodes:
                queue = ", ".join(self.request_queues[self.step][node.id])
                self.req_queue_vars[node.id].set(queue)
        except Exception as e: print(e)


    def show(self):
        self.step = 0
        self.thread_autoplaying = None
        self.req_queue_vars = {}

        # init table
        for n in range(len(self.nodes)):
            node_id = self.nodes[n].id
            var = tk.StringVar()
            self.req_queue_vars[node_id] = var
            tk.Label(self.fifo_req_table, bg="white", width=7, font='Arial 14 bold', relief="groove", text=str(node_id)).grid(row=n+1, column=0)
            tk.Label(self.fifo_req_table, bg="white", width=20, font='Arial 14 bold', relief="groove", textvariable=var).grid(row=n+1, column=1)
        
        self._update_system()
        self.root.mainloop()

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import messagebox

from coffee_machine_client import get_dict_of_available_beverages, order_n, get_stats, stop_server

class Window:
    def __init__(self, main):
        self.main = main
        
        self.WIDTH = 400
        self.HEIGHT = 300
        self.main.title("Coffee Machine Manager")
        self.main.geometry(f"{self.WIDTH}x{self.HEIGHT}+300+400")
        self.main.minsize(self.WIDTH, self.HEIGHT)
        self.main.maxsize(self.WIDTH, self.HEIGHT)
            
        self.bev_buttons = []

        self.refresh_b = tk.Button(master=self.main, text="Refresh data", fg="green", font=("Helvetica",16), 
                                                    command=self.refresh)
        self.refresh_b.place(width=150, height=50, x=25, y=10)

        self.stats_b = tk.Button(master=self.main, text="Statistics", fg="black", font=("Helvetica",16), 
                                                    command=self.stats)
        self.stats_b.place(width=150, height=50, x=self.WIDTH-175, y=10)

        self.state_label = tk.Label(master=self.main, text="", font=("Helvetica",14))
        self.state_label.place(x=70, y=70)

    def order(self, i, event):
        """Sends order number i to server."""

        button = event.widget
        if button["state"] == "disabled":  return

        button["bg"] = "#ff7518"         # mark pressed button

        try:
            order_n(i)
        except ConnectionRefusedError:
            self.state_label["text"] = "Connection error. Sorry, try again later."
            for b in self.bev_buttons:
                b.destroy()
            self.bev_buttons.clear()
    
            return
            
        for b in self.bev_buttons:
            b["state"] = "disabled"
        
        self.state_label["text"] = "Go get your coffee, cowboy!"

    def refresh(self):
        """Gets dictionary of available beverages, then creates and places a button for each."""

        import math
        
        try:
            bevs = get_dict_of_available_beverages()
        except ConnectionRefusedError:
            self.state_label["text"] = "Connection error. Sorry, try again later."  
            for b in self.bev_buttons:
                b.destroy()
            self.bev_buttons.clear()
            return

        for b in self.bev_buttons:
                b.destroy()
        self.bev_buttons.clear()

        self.state_label["text"] = ""

        b_width  = (self.WIDTH - 40) / 3
        b_height = (self.HEIGHT - 100) / math.ceil(len(bevs) / 3)
        start_width  = 10
        start_height = 95

        count = 0
        for i, bev in bevs.items():
            b = tk.Button(master=self.main, text=str(bev), fg="white", bg="#b5651d",
                          font=("Helvetica",10))
            b.bind("<Button-1>", lambda event, bev_i=i: self.order(bev_i, event)) 

            b.place(width=b_width, height=b_height,
                    x=start_width + (b_width + 10) * (count % 3), y=start_height + b_height * (count // 3))

            count += 1
            self.bev_buttons.append(b)
        
    def stats(self):
        try:
            statistics = get_stats()
        except ConnectionRefusedError:
            statistics = "Connection error. Sorry, try again later."
            
        tk.messagebox.showinfo("Statistics", statistics)
    
    
if __name__ == "__main__":
    
    main = tk.Tk()
    win = Window(main)
    
    main.mainloop()
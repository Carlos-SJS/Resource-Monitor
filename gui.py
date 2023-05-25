import customtkinter
import back_end
from qbstyles import mpl_style
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.ticker as mtick

mpl_style(dark=True)

customtkinter.set_appearance_mode("Dark") 
customtkinter.set_default_color_theme("blue")

class App(customtkinter.CTk):
    default_bg_color = "#383838"
    
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Resource\nMonitor.py")
        self.geometry(f"{1200}x{600}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=120, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Resource Monitor", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 50))

        # Graphs frame
        self.graph_frame = customtkinter.CTkScrollableFrame(self, label_text="Resources")
        self.graph_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), rowspan = 2, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)
        self.graphs = []

        self.cpu_f = Figure(figsize=(5,5), dpi=100)
        self.cpu_plot = self.cpu_f.add_subplot(111)
        self.cpu_graph = FigureCanvasTkAgg(self.cpu_f, self.graph_frame)
        self.cpu_graph.get_tk_widget().grid(row=0, column=0, padx=(0, 0), pady=(20, 0), sticky="nsew")
        self.cpu_plot.plot([])
        self.cpu_plot.set_title("CPU Usage                                         00%")
        self.cpu_plot.autoscale(enable=False)
        self.cpu_plot.set_ylim(0,100)

        self.mem_f = Figure(figsize=(5,5), dpi=100)
        self.mem_plot = self.mem_f.add_subplot(111)
        self.mem_graph = FigureCanvasTkAgg(self.mem_f, self.graph_frame)
        self.mem_graph.get_tk_widget().grid(row=1, column=0, padx=(0, 0), pady=(20, 0), sticky="nsew")
        self.mem_plot.plot([])
        self.mem_plot.set_title("Memory Usage                                      00%")
        self.mem_plot.set_ylim([0,100])

        self.disk_f = Figure(figsize=(5,5), dpi=100)
        self.disk_plot = self.disk_f.add_subplot(111)
        self.disk_graph = FigureCanvasTkAgg(self.disk_f, self.graph_frame)
        self.disk_graph.get_tk_widget().grid(row=2, column=0, padx=(0, 0), pady=(20, 0), sticky="nsew")
        lb = 'Unnused space', 'Used space'
        self.disk_plot.pie([25, 75], labels=lb, explode=(0, 0.05), autopct='%1.1f%%')
        self.disk_plot.set_title("Disk Usage                                        75%")        

        # Process frame
        self.processes_frame = customtkinter.CTkScrollableFrame(self, label_text="Processes")
        self.processes_frame.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.processes_frame.grid_columnconfigure(0, weight=1)
        self.process_labels = []
        self.process_f = []
        
        
        self.filter_frame = customtkinter.CTkFrame(self, fg_color='transparent', height=30, width=300)
        #self.filter_frame.grid_propagate(False)
        self.filter_frame.grid(row=1, column = 2, sticky="EW", padx=(0,0))
        
        
        self.cpu_button = customtkinter.CTkButton(self.filter_frame, text="CPU", height=25, width=70)
        self.cpu_button.grid_propagate(False)
        self.cpu_button.place(relx=.56, y=5)
        
        self.memory_button = customtkinter.CTkButton(self.filter_frame, text="Memory", height=25, width=70)
        self.memory_button.grid_propagate(False)
        self.memory_button.place(relx=.73, y=5)
        
        self.cpu_button.configure(state="disabled")
        self.appearance_mode_optionemenu.set("Dark")

        self.bind("<Configure>", self.on_resize)
        self.update_data()


    prev_w = 0
    def on_resize(self, event):
        if self.prev_w == self.processes_frame.winfo_width():
            return
        
        self.prev_w = self.processes_frame.winfo_width()

        fwd = self.processes_frame.winfo_width()*.9
        for p in self.process_labels:
            p[0].configure(width=fwd*.6)
            p[1].configure(width=fwd*.2)
            p[2].configure(width=fwd*.2)
    
        for f in self.process_f:
            f.configure(width=fwd, require_redraw=True)

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        if new_appearance_mode == "Dark":
            mpl_style(dark=True)
            if self.default_bg_color != "#383838":
                self.default_bg_color = "#383838"
                for f in self.process_f:
                    f.configure(fg_color=self.default_bg_color)
                
        elif new_appearance_mode == "Light":
            mpl_style(dark=False)
            if self.default_bg_color != "#AFAFAF":
                self.default_bg_color = "#AFAFAF"
                for f in self.process_f:
                    f.configure(fg_color=self.default_bg_color)

        self.re_plot()

        customtkinter.set_appearance_mode(new_appearance_mode)

    def re_plot(self):
        self.cpu_f = Figure(figsize=(5,5), dpi=100)
        self.cpu_plot = self.cpu_f.add_subplot(111)
        self.cpu_graph = FigureCanvasTkAgg(self.cpu_f, self.graph_frame)
        self.cpu_graph.get_tk_widget().grid(row=0, column=0, padx=(0, 0), pady=(20, 0), sticky="nsew")
        self.cpu_plot.plot(self.cpudata)
        self.cpu_plot.set_title("CPU Usage                                         00%")
        self.cpu_plot.autoscale(enable=False)
        self.cpu_plot.set_ylim([0,100])
        self.cpu_plot.set_xlim([0,100])
        


        self.mem_f = Figure(figsize=(5,5), dpi=100)
        self.mem_plot = self.mem_f.add_subplot(111)
        self.mem_graph = FigureCanvasTkAgg(self.mem_f, self.graph_frame)
        self.mem_graph.get_tk_widget().grid(row=1, column=0, padx=(0, 0), pady=(20, 0), sticky="nsew")
        self.mem_plot.plot(self.memdata)
        self.mem_plot.set_title("Memory Usage                                 00%")
        #self.mem_plot.autoscale(enable=False)
        self.mem_plot.set_ylim([0,100])
        #self.mem_plot.set_xlim(0,100)
        

        self.disk_f = Figure(figsize=(5,5), dpi=100)
        self.disk_plot = self.disk_f.add_subplot(111)
        self.disk_graph = FigureCanvasTkAgg(self.disk_f, self.graph_frame)
        self.disk_graph.get_tk_widget().grid(row=2, column=0, padx=(0, 0), pady=(20, 0), sticky="nsew")
        lb = 'Unnused space', 'Used space'
        self.disk_plot.pie([25, 75], labels=lb, explode=(0, 0.05), autopct='%1.1f%%')
        self.disk_plot.set_title("Disk Usage                                    75%")  

    def plot_update(self):
        self.cpu_plot.clear()
        self.cpu_plot.plot(self.cpudata)
        self.cpu_plot.set_title(f"CPU Usage                                         {round(self.cpudata[-1], 2)}%")
        self.cpu_plot.set_ylim([0,100])
        self.cpu_plot.margins(0)

        #x_fill = np.linspace(0, len(self.cpudata)-1, 1000)
        #self.cpu_plot.fill_between(x_fill, 2*x_fill, alpha=0.5)
        self.cpu_plot.axes.get_xaxis().set_visible(False)
        self.cpu_plot.axes.get_yaxis().set_major_formatter(mtick.PercentFormatter())
        self.cpu_graph.draw_idle()

        self.mem_plot.clear()
        self.mem_plot.plot(self.memdata)
        self.mem_plot.set_title(f"Memory Usage                                 {round(self.memdata[-1], 2)}%")
        self.mem_plot.set_ylim([0,100])
        self.mem_plot.margins(0)
        
        self.mem_plot.axes.get_xaxis().set_visible(False)
        self.mem_plot.axes.get_yaxis().set_major_formatter(mtick.PercentFormatter())
        self.mem_graph.draw_idle()

        lb = 'Unnused space', 'Used space'
        self.disk_plot.clear()
        self.disk_plot.pie(self.diskdata, labels=lb, explode=(0, 0.05), autopct='%1.1f%%')
        self.disk_plot.set_title(f"Disk Usage                                   {self.diskpercent}%")    
        
        self.disk_graph.draw_idle()
        
    def processes_update(self):
        plist = back_end.get_processes()
        
        for i in range(min(len(plist), len(self.process_f))):
            self.process_labels[i][0].configure(text=plist[i]['name'])
            self.process_labels[i][1].configure(text=str(plist[i]['cpu_percent']) + "%")
            self.process_labels[i][2].configure(text=str(plist[i]['memory_percent']) + "%")
            
            self.process_f[i].configure(require_redraw=True)

        if len(plist) > len(self.process_f):
            fwdt = self.processes_frame.winfo_width()*.9
            k = len(plist)-len(self.process_f)
            for i in range(k):
                f = customtkinter.CTkFrame(master=self.processes_frame, fg_color=self.default_bg_color, height=30, width=fwdt)
                f.grid_propagate(False)
                f.grid(row=len(self.process_f), column=0, padx=0, pady=2) 
                
                l1  = customtkinter.CTkLabel(text=plist[i]['name'], master=f, bg_color="transparent", width=fwdt*.6, anchor="w")
                l1.grid(row=0, column=0, padx = (fwdt*.02, 0))
                l2  = customtkinter.CTkLabel(text=str(plist[i]['cpu_percent'])+"%", master=f, bg_color="transparent", width=fwdt*.2, anchor="w")
                l2.grid(row=0, column=1)
                l3  = customtkinter.CTkLabel(text=str(plist[i]['memory_percent'])+"%", master=f, bg_color="transparent", width=fwdt*.2, anchor="w")
                l3.grid(row=0, column=2)
            
                self.process_f.append(f)
                self.process_labels.append([l1,l2,l3])
        elif len(plist) < len(self.process_f):
            for i in range(len(self.process_f)-len(plist)):
                self.process_f[-1].destroy()
                self.process_f.pop()
                self.process_labels.pop()
        
    upd_ct = 18
    def update_data(self):
        #print(psutil.cpu_percent())
        self.cpudata = back_end.get_cpu()
        #print(self.cpudata)
        self.memdata = back_end.get_memory()

        self.diskdata, self.diskpercent = back_end.get_disk ()

        self.plot_update()
        if self.upd_ct == 20:
            self.processes_update()
            self.upd_ct = 0
            
        self.after(1000, self.update_data)
        self.upd_ct += 1

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()
    
    back_end.run_thread = False
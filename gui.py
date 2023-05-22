import tkinter
import tkinter.messagebox
import customtkinter
import matplotlib

from qbstyles import mpl_style

mpl_style(dark=True)

matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

customtkinter.set_appearance_mode("System") 
customtkinter.set_default_color_theme("blue")


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # configure window
        self.title("Resource Monitor.py")
        self.geometry(f"{1100}x{580}")

        # configure grid layout (4x4)
        self.grid_columnconfigure((1, 2), weight=1)

        # create sidebar frame with widgets
        self.sidebar_frame = customtkinter.CTkFrame(self, width=140, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, rowspan=4, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(4, weight=1)
        self.logo_label = customtkinter.CTkLabel(self.sidebar_frame, text="Better resource\nmonitor than\nErwin's\nresource monitor :D", font=customtkinter.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))
        self.sidebar_button_1 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_1.grid(row=1, column=0, padx=20, pady=10)
        self.sidebar_button_2 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_2.grid(row=2, column=0, padx=20, pady=10)
        self.sidebar_button_3 = customtkinter.CTkButton(self.sidebar_frame, command=self.sidebar_button_event)
        self.sidebar_button_3.grid(row=3, column=0, padx=20, pady=10)
        self.appearance_mode_label = customtkinter.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                                       command=self.change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.scaling_label = customtkinter.CTkLabel(self.sidebar_frame, text="UI Scaling:", anchor="w")
        self.scaling_label.grid(row=7, column=0, padx=20, pady=(10, 0))
        self.scaling_optionemenu = customtkinter.CTkOptionMenu(self.sidebar_frame, values=["80%", "90%", "100%", "110%", "120%"],
                                                               command=self.change_scaling_event)
        self.scaling_optionemenu.grid(row=8, column=0, padx=20, pady=(10, 20))

        # create textbox
        #self.textbox = customtkinter.CTkTextbox(self, width=250)
        #self.textbox.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")

        self.graph_frame = customtkinter.CTkScrollableFrame(self, label_text="Resources")
        self.graph_frame.grid(row=0, column=1, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.graph_frame.grid_columnconfigure(0, weight=1)
        self.graphs = []

        #for i in range(100):
        #    switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
        #    switch.grid(row=i, column=0, padx=10, pady=(0, 20))
        #    self.scrollable_frame_switches.append(switch)

        cpu_f = Figure(figsize=(5,5), dpi=100)
        cpu_plot = cpu_f.add_subplot(111)
        cpu_graph = FigureCanvasTkAgg(cpu_f, self.graph_frame)
        cpu_graph.get_tk_widget().grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        cpu_plot.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        cpu_plot.set_title("CPU Usage                                                00%")

        mem_f = Figure(figsize=(5,5), dpi=100)
        mem_plot = mem_f.add_subplot(111)
        mem_graph = FigureCanvasTkAgg(mem_f, self.graph_frame)
        mem_graph.get_tk_widget().grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        mem_plot.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        mem_plot.set_title("Memory Usage                                             00%")

        disk_f = Figure(figsize=(5,5), dpi=100)
        disk_plot = disk_f.add_subplot(111)
        disk_graph = FigureCanvasTkAgg(disk_f, self.graph_frame)
        disk_graph.get_tk_widget().grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        lb = 'Used space', 'Unnused space'
        disk_plot.pie([75, 25], labels=lb)
        disk_plot.set_title("Disk Usage                                               75%")        

        self.graphs.append(cpu_plot)
        self.graphs.append(mem_plot)
        self.graphs.append(cpu_plot)

        # create scrollable frame
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self, label_text="Processes")
        self.scrollable_frame.grid(row=0, column=2, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.scrollable_frame.grid_columnconfigure(0, weight=1)
        self.scrollable_frame_switches = []
        for i in range(100):
            switch = customtkinter.CTkSwitch(master=self.scrollable_frame, text=f"CTkSwitch {i}")
            switch.grid(row=i, column=0, padx=10, pady=(0, 20))
            self.scrollable_frame_switches.append(switch)

        # set default values
        self.sidebar_button_3.configure(state="disabled", text="Disabled CTkButton")
        self.scrollable_frame_switches[0].select()
        self.scrollable_frame_switches[4].select()
        self.appearance_mode_optionemenu.set("Dark")
        self.scaling_optionemenu.set("100%")

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        customtkinter.set_appearance_mode(new_appearance_mode)

    def change_scaling_event(self, new_scaling: str):
        new_scaling_float = int(new_scaling.replace("%", "")) / 100
        customtkinter.set_widget_scaling(new_scaling_float)

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()
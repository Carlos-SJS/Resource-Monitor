import tkinter
import tkinter.messagebox
import customtkinter
import matplotlib

from qbstyles import mpl_style

mpl_style(dark=True)

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
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 50))

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

        self.cpu_f = Figure(figsize=(5,5), dpi=100)
        self.cpu_plot = self.cpu_f.add_subplot(111)
        self.cpu_graph = FigureCanvasTkAgg(self.cpu_f, self.graph_frame)
        self.cpu_graph.get_tk_widget().grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.cpu_plot.plot([5,6,1,3,8,9,3,5])
        self.cpu_plot.set_title("CPU Usage                                                00%")

        self.mem_f = Figure(figsize=(5,5), dpi=100)
        self.mem_plot = self.mem_f.add_subplot(111)
        self.mem_graph = FigureCanvasTkAgg(self.mem_f, self.graph_frame)
        self.mem_graph.get_tk_widget().grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.mem_plot.plot([5,6,1,3,8,9,3,5])
        self.mem_plot.set_title("Memory Usage                                             00%")

        self.disk_f = Figure(figsize=(5,5), dpi=100)
        self.disk_plot = self.disk_f.add_subplot(111)
        self.disk_graph = FigureCanvasTkAgg(self.disk_f, self.graph_frame)
        self.disk_graph.get_tk_widget().grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        lb = 'Unnused space', 'Used space'
        self.disk_plot.pie([25, 75], labels=lb, explode=(0, 0.05), autopct='%1.1f%%')
        self.disk_plot.set_title("Disk Usage                                               75%")        

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

    def open_input_dialog_event(self):
        dialog = customtkinter.CTkInputDialog(text="Type in a number:", title="CTkInputDialog")
        print("CTkInputDialog:", dialog.get_input())

    def change_appearance_mode_event(self, new_appearance_mode: str):
        if new_appearance_mode == "Dark":
            mpl_style(dark=True)
        elif new_appearance_mode == "Light":
            mpl_style(dark=False)

        self.re_plot()

        customtkinter.set_appearance_mode(new_appearance_mode)

    def re_plot(self):
        self.cpu_f = Figure(figsize=(5,5), dpi=100)
        self.cpu_plot = self.cpu_f.add_subplot(111)
        self.cpu_graph = FigureCanvasTkAgg(self.cpu_f, self.graph_frame)
        self.cpu_graph.get_tk_widget().grid(row=0, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.cpu_plot.plot([5,6,1,3,8,9,3,5])
        self.cpu_plot.set_title("CPU Usage                                                00%")

        self.mem_f = Figure(figsize=(5,5), dpi=100)
        self.mem_plot = self.mem_f.add_subplot(111)
        self.mem_graph = FigureCanvasTkAgg(self.mem_f, self.graph_frame)
        self.mem_graph.get_tk_widget().grid(row=1, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        self.mem_plot.plot([5,6,1,3,8,9,3,5])
        self.mem_plot.set_title("Memory Usage                                             00%")

        self.disk_f = Figure(figsize=(5,5), dpi=100)
        self.disk_plot = self.disk_f.add_subplot(111)
        self.disk_graph = FigureCanvasTkAgg(self.disk_f, self.graph_frame)
        self.disk_graph.get_tk_widget().grid(row=2, column=0, padx=(20, 0), pady=(20, 0), sticky="nsew")
        lb = 'Unnused space', 'Used space'
        self.disk_plot.pie([25, 75], labels=lb, explode=(0, 0.05), autopct='%1.1f%%')
        self.disk_plot.set_title("Disk Usage                                               75%")         

    def sidebar_button_event(self):
        print("sidebar_button click")


if __name__ == "__main__":
    app = App()
    app.mainloop()
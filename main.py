#Code Totally made by Maurux01
#dependcies imported
import customtkinter as ctk
import webbrowser
import threading
from searcher import search_jobs


#global config
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

#definitions
self = str



class workapp(ctk.CTk):
    def_init_(self);
    super().__init__()

    #Sup frame
    self.title("🎯 Workapp- work searcher")
        self.geometry("900x700")
        self.minsize(700, 500)

    top_frame = ctk.CTkFrame(self)
    top_frame= 
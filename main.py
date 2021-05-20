from tkinter import *
from tkinter import messagebox

from adts import *
from medical_advisor_module import *

root = Tk()
medical_advisor = MedicalAdvisor()
symptom_bd = SymptomBD()


def configure_root_screen():
    root.title("Medical Advisor")
    root["bg"] = "#fafafa"
    screen_size = "500x500"
    root.geometry(screen_size)
    root.resizable(width=False, height=False)


def accept_terms_of_use():
    response = messagebox.askquestion(title="Terms of use acception",
                                      message="Do you agree with terms of use of this application?")
    if response == "yes":
        show_main_menu()
    else:
        root.destroy()


def show_main_menu():
    pass


def script():
    configure_root_screen()
    accept_terms_of_use()


if __name__ == '__main__':
    script()
    root.mainloop()

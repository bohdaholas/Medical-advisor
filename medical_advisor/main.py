from tkinter import *
from tkinter import messagebox
from medical_advisor.adts import *
from medical_advisor_module import *


def configure_root_screen():
    root.title("Medical Advisor")
    root["bg"] = "#fafafa"
    screen_size = "1200x900"
    root.geometry(screen_size)
    root.resizable(width=False, height=False)


def clear_screen():
    for el in root.winfo_children():
        el.destroy()


def run_app():
    response = messagebox.askquestion(title="Terms of use",
                                      message="Do you agree with terms of use of this application?")
    if response == "yes":
        display_app_menu()
    else:
        root.destroy()


def display_app_menu():
    clear_screen()
    header = Label(root, text="Medical Advisor", fg="#2F2B2B", bg=white_color, font="Helvetica 42 bold")
    menu = Frame(root, bg=white_color)
    set_default_values(menu)
    add_symptom(menu)
    analyze(menu)
    next_steps(menu)
    header.pack(pady=(10, 10))
    menu.pack(pady=(0, 30))


def set_default_values(header):
    is_default = BooleanVar()
    is_default.set(True)
    default_values = Checkbutton(header, text=f"Use default value for features not provided: {is_default.get()}",
                                 command=lambda: change_default_values_state(default_values, is_default),
                                 bg=white_color)
    default_values.grid(row=0, column=0, padx=(10, 10))
    medical_advisor.set_use_of_default_values(is_default.get())


def change_default_values_state(default_values, is_default):
    new_state = not is_default.get()
    is_default.set(new_state)
    default_values["text"] = f"Use default value for features not provided: {new_state}"


def add_symptom(header):
    add_symptom_btn = Button(header, text="Add symptom", command=lambda: add_symptom_popup())
    add_symptom_btn.grid(row=0, column=1, padx=(10, 10))


def add_symptom_popup():
    display_app_menu()
    symptom_frame = Frame(root, bg=white_color)
    lst_box_frame = Frame(symptom_frame, bg=white_color)
    scrollbar = Scrollbar(lst_box_frame, orient=VERTICAL)
    symptom_list_box = Listbox(lst_box_frame, yscrollcommand=scrollbar.set, width=100)
    list_symptoms("", symptom_list_box)

    scrollbar.config(command=symptom_list_box.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    search_field_value = StringVar()
    search_field_value.trace("w", lambda name, index, mode, lst_box=symptom_list_box,
                                         str_var=search_field_value: list_symptoms(str_var.get(), lst_box))
    symptom_search_field = Entry(symptom_frame, textvariable=search_field_value, width=102)
    selected_symptom_btn = Button(symptom_frame, text="Add", command=lambda: answer(symptom_frame, symptom_list_box),
                                  width=12)

    symptom_search_field.pack(pady=(0, 30))
    symptom_list_box.pack(padx=40)
    lst_box_frame.pack(pady=(0, 20))
    selected_symptom_btn.pack()
    symptom_frame.pack()


def list_symptoms(str_val, lst_box):
    lst_box.delete(0, "end")
    for symptom in symptom_bd.symptoms_data:
        question_sentence = symptom.question.question_sentence
        if str_val in question_sentence:
            lst_box.insert(END, question_sentence)


def confirm_symptom(symptom, value):
    patient.patient_symptoms.push((symptom.symptom_name, value.get()))
    display_app_menu()
    add_symptom_popup()


def answer(frame, lst_box):
    frame.pack_forget()
    selected_symptom_question = lst_box.get(ANCHOR)
    for symptom in symptom_bd.symptoms_data:
        if selected_symptom_question == symptom.question.question_sentence:
            display_answer_section(symptom)
            break


def display_answer_section(symptom):
    if symptom.question.answers.choices:
        answers_frame = Frame(root, bg=white_color)
        question = Label(answers_frame, text=symptom.question.question_sentence, fg=black_color,
                         bg=white_color, font='Helvetica 12 bold', wraplength=500)
        question.pack(pady=(0, 20))
        radio_value = IntVar()
        choices = symptom.question.answers.choices
        for choice in choices:
            choice_radio_btn = Radiobutton(answers_frame, text=choice, variable=radio_value,
                                           value=choices[choice], bg=white_color)
            choice_radio_btn.pack()
        answers_frame.pack(pady=(0, 20))

        confirm_btn = Button(root, text="Confirm", command=lambda: confirm_symptom(symptom, radio_value))
        confirm_btn.pack()
    else:
        print(symptom.question.answers.min_value, symptom.question.answers.max_value)


def analyze(header):
    min_symptoms_num = 3
    if len(patient.patient_symptoms) >= min_symptoms_num:
        analyze_btn = Button(header, text="Analyze", state=ACTIVE, command=analysis_results)
    else:
        analyze_btn = Button(header, text="Analyze", state=DISABLED)
    analyze_btn.grid(row=0, column=2, padx=(10, 10))


def analysis_results():
    patient.was_analyzed = True
    display_app_menu()
    medical_advisor.init_session()
    medical_advisor.accept_terms_of_use()
    for patient_symptom in patient.patient_symptoms:
        medical_advisor.add_symptom(patient_symptom[0], patient_symptom[1])
    number_of_results = 6
    diagnoses = medical_advisor.analyze(number_of_results)
    diagnoses_frame = Frame(root, bg=white_color)
    diagnoses_label = Label(diagnoses_frame, text="5 Possible diagnoses:", fg=red_color,
                            bg=white_color, font='Helvetica 18 bold')
    diagnoses_label.pack(pady=(0, 20))
    one_less = False
    for diagnose in diagnoses:
        if diagnose == "Patient in immediate life-threatening condition":
            one_less = True
            continue
        if not one_less and diagnose == diagnoses[-1]:
            break
        result_label = Label(diagnoses_frame, text=diagnose, bg=white_color)
        result_label.pack()
    diagnoses_frame.pack()


def next_steps(header):
    if not patient.was_analyzed:
        next_steps_btn = Button(header, text="Next Steps", state=DISABLED)
    else:
        next_steps_btn = Button(header, text="Next Steps", state=ACTIVE, command=show_specializations)
    next_steps_btn.grid(row=0, column=3, padx=(10, 10))


def show_specializations():
    display_app_menu()
    number_of_results = 5
    specializations = medical_advisor.get_suggested_specializations(number_of_results)
    specializations_frame = Frame(root, bg=white_color)
    specialization_label = Label(specializations_frame, text="Recommended specialists:", fg=green_color,
                                 bg=white_color, font='Helvetica 18 bold')
    specialization_label.pack(pady=(0, 20))
    for specialization in specializations:
        specialization_label = Label(specializations_frame, text=specialization, bg=white_color)
        specialization_label.pack()
    specializations_frame.pack()


if __name__ == '__main__':
    white_color = "#fafafa"
    black_color = "#2F2B2B"
    red_color = "#D21010"
    green_color = "#76E414"

    medical_advisor = MedicalAdvisor()
    symptom_bd = SymptomBD()
    patient = Patient()

    root = Tk()
    configure_root_screen()
    run_app()
    root.mainloop()

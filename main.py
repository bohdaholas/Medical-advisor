from tkinter import *
from tkinter import messagebox
from adts import *
from medical_advisor_module import *


def configure_root_screen():
    root.title("Medical Advisor")
    root["bg"] = "#fafafa"
    screen_size = "500x500"
    root.geometry(screen_size)
    root.resizable(width=False, height=False)


def run_app():
    response = messagebox.askquestion(title="Terms of use",
                                      message="Do you agree with terms of use of this application?")
    if response == "yes":
        # medical_advisor.init_session()
        # medical_advisor.accept_terms_of_use()
        display_app_menu()
    else:
        root.destroy()


def change_default_state(default_values, is_default):
    new_state = not is_default.get()
    is_default.set(new_state)
    default_values["text"] = f"Use default value for features not provided: {new_state}"


def use_default_values():
    is_default = BooleanVar()
    is_default.set(True)
    default_values = Checkbutton(root, text=f"Use default value for features not provided: {is_default.get()}",
                                 command=lambda: change_default_state(default_values, is_default))
    default_values.pack()


def add_symptom():
    add_symptom_btn = Button(root, text="Add symptom", command=lambda: add_symptom_popup(add_symptom_btn))
    add_symptom_btn.pack()


def list_symptoms(str_val, lst_box):
    lst_box.delete(0, "end")
    for symptom in symptom_bd.symptoms_data:
        question_sentence = symptom.question.question_sentence
        if str_val.get() in question_sentence:
            lst_box.insert(END, question_sentence)


def confirm_symptom(symptom, value):
    patient.patient_symptoms.push((symptom.symptom_name, value.get()))
    for el in root.winfo_children():
        el.destroy()
    display_app_menu()


def display_answer_section(frame, symptom):
    if symptom.question.answers.choices:
        answers_frame = Frame(root)
        radio_value = IntVar()
        choices = symptom.question.answers.choices
        for choice in choices:
            choice_radio_btn = Radiobutton(answers_frame, text=choice, variable=radio_value, value=choices[choice])
            choice_radio_btn.pack()
        answers_frame.pack()

        confirm_btn = Button(root, text="Confirm", command=lambda: confirm_symptom(symptom, radio_value))
        confirm_btn.pack()
    else:
        print(symptom.question.answers.min_value, symptom.question.answers.max_value)


def answer(frame, lst_box):
    frame.pack_forget()
    selected_symptom_question = lst_box.get(ANCHOR)
    for symptom in symptom_bd.symptoms_data:
        if selected_symptom_question == symptom.question.question_sentence:
            display_answer_section(frame, symptom)


def add_symptom_popup(add_symptom_btn):
    body_frame = Frame(root)
    lst_box_frame = Frame(body_frame)
    scrollbar = Scrollbar(lst_box_frame, orient=VERTICAL)
    symptom_list_box = Listbox(lst_box_frame, yscrollcommand=scrollbar.set)

    scrollbar.config(command=symptom_list_box.yview)
    scrollbar.pack(side=RIGHT, fill=Y)

    search_field_value = StringVar()
    search_field_value.trace("w", lambda name, index, mode, lst_box=symptom_list_box,
                                         str_var=search_field_value: list_symptoms(str_var, lst_box))
    symptom_search_field = Entry(body_frame, textvariable=search_field_value)
    selected_symptom_btn = Button(body_frame, text="Add", command=lambda: answer(body_frame, symptom_list_box))

    for el in (symptom_search_field, symptom_list_box, lst_box_frame, selected_symptom_btn, body_frame):
        el.pack()


def analysis_results():
    results_frame = Frame(root)
    medical_advisor.init_session()
    medical_advisor.accept_terms_of_use()
    for patient_symptom in patient.patient_symptoms:
        medical_advisor.add_symptom(patient_symptom[0], patient_symptom[1])
    number_of_results = 5
    results = medical_advisor.analyze(number_of_results)


def analyze():
    min_symptoms_num = 3
    if len(patient.patient_symptoms) >= min_symptoms_num:
        analyze_btn = Button(root, text="Analyze", state=ACTIVE)
        analysis_results()
    else:
        analyze_btn = Button(root, text="Analyze", state=DISABLED)
    analyze_btn.pack()


def next_steps():
    next_steps_btn = Button(root, text="Next Steps", state=DISABLED)
    next_steps_btn.pack()


def display_app_menu():
    use_default_values()
    add_symptom()
    analyze()
    next_steps()


def script():
    configure_root_screen()
    run_app()


if __name__ == '__main__':
    root = Tk()
    medical_advisor = MedicalAdvisor()
    symptom_bd = SymptomBD()
    patient = Patient()
    script()
    root.mainloop()

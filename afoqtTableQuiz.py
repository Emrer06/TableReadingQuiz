import customtkinter as ctk
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import time

import random


class Quiz:
    def __init__(self, num_question, time, root, main_window):
        self.root = root  # Root window for placing UI elements
        self.questions = num_question  # Number of questions for the quiz
        self.quiz_time = time  # Time for the quiz
        self.current_question_number = 1  # Tracker for the current question number
        self.q_num_label = None  # Label to display the current question number
        self.radio_buttons = []  # List to hold the radio buttons for choices
        self.setup_ui_elements()  # Call to setup the UI elements when an object is created
        self.question_answers = []  # initialize the question_answers list

        self.start_time = None  # To track the start time of the quiz
        self.time_remaining = time * 60  # Convert minutes to seconds
        self.timer_label = None  # Label to display the timer
        self.timer_running = False  # Flag to indicate if the timer is running

        self.start_timer()
        self.main_window = main_window

    def start_timer(self):
        self.start_time = time.time()
        self.timer_running = True
        self.timer_label = ctk.CTkLabel(self.root, text="Time Left: " + str(self.time_remaining) + "s", font=("Times New Roman", 20))
        self.timer_label.place(relx=0.5, rely=0.1, anchor="center")
        self.update_timer()

    def update_timer(self):
        if self.timer_running:
            elapsed_time = time.time() - self.start_time
            self.time_remaining = int(self.quiz_time * 60 - elapsed_time)
            if self.time_remaining > 0:
                self.timer_label.configure(text="Time Left: " + str(self.time_remaining) + "s")
                self.root.after(1000, self.update_timer)  # Update every second
            else:
                self.end_quiz()

    def setup_ui_elements(self):
        # Defining various fonts to be used in the UI
        question_font = ("Times New Roman", 50)
        answer_font = ("Times New Roman", 23)
        coordinate_font = ("Times New Roman", 40)

        # Creating and placing frames to hold other UI elements
        frame = ctk.CTkFrame(self.root, fg_color="white")
        frame.place(relx=0.5, rely=0.3, anchor="center")
        q_frame = ctk.CTkFrame(self.root, fg_color="white")
        q_frame.place(x=frame.winfo_x() + 10, y=frame.winfo_y() + 10)
        self.q_num_label = ctk.CTkLabel(q_frame, text=str(self.current_question_number) + ".", font=question_font)
        self.q_num_label.pack()

        # Setup other UI elements
        self.setup_radio_buttons(frame, answer_font)
        self.setup_labels_and_grid(frame, question_font, coordinate_font)
        self.setup_next_question_button()

    # Function to set up the next question button
    def setup_next_question_button(self):
        button_font = ctk.CTkFont(family='Bahnschrift SemiBold Condensed', size=20)
        self.next_question_button = ctk.CTkButton(self.root, text="Next Question", font=button_font, corner_radius=25, command=self.next_question)
        self.next_question_button.place(relx=0.95, rely=0.95, anchor="se")

    # Function to move to the next question
    def next_question(self):
        if self.radio_var.get() == 0:
            messagebox.showwarning("No Selection", "You must select an answer before proceeding.")
            return

        self.check_answer()

        # Increment the question number
        self.current_question_number += 1

        # Check if it's the last question
        if self.current_question_number == self.questions:
            self.next_question_button.configure(text="Submit", command=self.submit_quiz)
            # Update the UI for the next question
            self.update_for_next_question()
        elif self.current_question_number > self.questions:
            # If it's beyond the last question, submit the quiz
            self.submit_quiz()
        else:
            # Update the UI for the next question
            self.update_for_next_question()

    def update_for_next_question(self):
        # Update the UI elements for the next question
        self.q_num_label.configure(text=str(self.current_question_number) + ".")
        self.calculate_random_numbers_and_answer()
        self.update_radio_buttons()
        self.radio_var.set(0)
        self.update_coordinates()



    def check_answer(self): 
         # print the values to check what they are
        print(f"Selected answer: {self.radio_var.get()}, Correct answer: {self.answer}")

        is_correct = self.radio_var.get() == self.answer
        result = f"Question {self.current_question_number} {'Correct' if is_correct else 'Incorrect'}"
        self.question_answers.append(result)
        print(self.question_answers)

    # Function to update the x and y coordinates displayed
    def update_coordinates(self):
        self.x_coordinate.configure(text=str(self.random_numberX))
        self.y_coordinate.configure(text=str(self.random_numberY))

    def setup_radio_buttons(self, frame, answer_font):
        # Create a frame for radio buttons and set its position
        radio_frame = ctk.CTkFrame(self.root, fg_color="white")
        self.radio_var = tk.IntVar()
        # Calculate random numbers and answers for the question
        self.calculate_random_numbers_and_answer()
        # Generate choices for the radio buttons
        choices = self.generate_choices()
        # Position the radio frame in relation to the main frame
        radio_frame.place(x=frame.winfo_x() + 160, y=frame.winfo_y() + frame.winfo_height() + 220)
        style = ttk.Style()
        style.configure("TRadiobutton", font=answer_font)
        for i, choice in enumerate(choices):
            # Create a radio button with a choice and add it to the radio frame
            rb = ttk.Radiobutton(radio_frame, text=f"{choice}", value=choice, variable=self.radio_var, style="TRadiobutton")
            rb.pack(pady=6)  # Align radio buttons with padding
            self.radio_buttons.append(rb)  # Add the radio button to the list

    # Function to update the choices in the radio buttons for the next question
    def update_radio_buttons(self):
         choices = self.generate_choices()
         for i, button in enumerate(self.radio_buttons):
             button.configure(text=str(choices[i]), value=choices[i])

    # Function to calculate random numbers and the answer for the question
    def calculate_random_numbers_and_answer(self):
        # Generate two random numbers between -20 and 20
        self.random_numberX, self.random_numberY = random.randint(-20, 20), random.randint(-20, 20)
        # Calculate the answer based on the random numbers
        self.answer = 90 + self.random_numberX - self.random_numberY

    # Function to generate choices for the question
    def generate_choices(self):
        # Generate a list of offsets to create incorrect choices
        offsets = random.sample([-3, -2, -1, 1, 2, 3], 4)
        # Add offsets to the answer to create choices
        choices = [self.answer + offset for offset in offsets]
        # Randomly insert the correct answer in the choices list
        choices.insert(random.randint(0, 4), self.answer)
        return choices  # Return the list of choices

    # Function to setup labels and grid for displaying the question
    def setup_labels_and_grid(self, frame, question_font, coordinate_font):
        # Configure columns and rows for the grid in frame
        frame.columnconfigure((0, 1), weight=1)
        frame.rowconfigure((0, 1), weight=1)
        # Create and position the label for 'X'
        self.question_label_x = ctk.CTkLabel(frame, text="X", font=question_font)
        self.question_label_x.grid(row=0, column=0, padx=20)
        # Create and position the label for 'Y'
        self.question_label_y = ctk.CTkLabel(frame, text="Y", font=question_font)
        self.question_label_y.grid(row=0, column=1, padx=20)
        # Create and position the label for displaying the value of 'X'
        self.x_coordinate = ctk.CTkLabel(frame, text=str(self.random_numberX), font=coordinate_font)
        self.x_coordinate.grid(row=1, column=0, padx=20)
        # Create and position the label for displaying the value of 'Y'
        self.y_coordinate = ctk.CTkLabel(frame, text=str(self.random_numberY), font=coordinate_font)
        self.y_coordinate.grid(row=1, column=1, padx=20)
        
    def calculate_results(self):
        correct_answers = sum('Correct' in answer for answer in self.question_answers)
        incorrect_answers = sum('Incorrect' in answer for answer in self.question_answers)
        unanswered_questions = sum('Not Answered' in answer for answer in self.question_answers)
        time_taken = self.quiz_time * 60 - self.time_remaining
        avg_time_per_question = time_taken / len(self.question_answers) if len(self.question_answers) > 0 else 0

        messagebox.showinfo("Quiz Results", 
                            f"Correct answers: {correct_answers}\n"
                            f"Incorrect answers: {incorrect_answers}\n"
                            f"Unanswered questions: {unanswered_questions}\n"
                            f"Time taken: {time_taken} seconds\n"
                            f"Average time per question: {avg_time_per_question:.2f} seconds")


    def submit_quiz(self):
        self.timer_running = False

        # Check and record the answer of the current question before submitting if it's not the first question
        if self.current_question_number > 1 and self.radio_var.get() != 0:
            self.check_answer()

        self.calculate_results()

        # Clear the quiz window
        for widget in self.root.winfo_children():
            widget.destroy()

        # Show the main menu
        self.main_window.show_main_menu()


    def end_quiz(self):
        self.timer_running = False
        while self.current_question_number <= self.questions:
            self.question_answers.append(f"Question {self.current_question_number} Not Answered")
            self.current_question_number += 1
        messagebox.showinfo("Time's up!", "Time's up! The quiz will now end.")
        self.submit_quiz()
        
class MainWindow:
    def __init__(self):
        # Create the main window as an instance of ctk.CTk
        self.root = ctk.CTk(fg_color='white')
        self.root.title('AFQOT Table Reading Quiz')
        # Height and Width of window 
        self.root_width = 700
        self.root_height = 500

        # Calculate screen dimensions
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()

        # Centers window
        x = (self.screen_width / 2) - (self.root_width / 2)
        y = (self.screen_height / 2) - (self.root_height / 2)
        self.root.geometry(f'{self.root_width}x{self.root_height}+{int(x)}+{int(y)}')
        self.root.resizable(False, False)

        self.root.columnconfigure(0, weight=1)  # Leftmost column
        self.root.columnconfigure(1, weight=1)  # Central column (where your frame will be)
        self.root.columnconfigure(2, weight=1)  # Rightmost column

        self.root.rowconfigure(0, weight=1)  # Topmost row
        self.root.rowconfigure(1, weight=1)  # Central row (where your frame will be)
        self.root.rowconfigure(2, weight=1)  # Bottommost row

        # Create the central frame
        self.central_frame = ctk.CTkFrame(self.root, fg_color='white')
        self.central_frame.grid(row=1, column=1)

        label_font = ctk.CTkFont(family= 'Bahnschrift SemiBold Condensed', size = 40)
        button_font = ctk.CTkFont(family= 'Bahnschrift SemiBold Condensed', size = 20)

        button_width = 200
        button_height = 50

        # Now, place all your widgets in this central frame
        self.label = ctk.CTkLabel(self.central_frame, text='AFQOT Table Reading Quiz', font = label_font)
        self.label.grid(row=0, column=0, sticky='nsew', pady=10)
       
        self.full_test = ctk.CTkButton(self.central_frame, text="Full Test (7 Minutes)", command=self.start_full_test, corner_radius=25, font = button_font, width=button_width, height=button_height)
        self.full_test.grid(row=1, column=0, sticky='ns', pady=10)

        self.half_test = ctk.CTkButton(self.central_frame, text="Half Test (3.5 Minutes)", command=self.start_half_test, corner_radius=25, font = button_font, width=button_width, height=button_height)
        self.half_test.grid(row=2, column=0, sticky='ns', pady=10)

        self.quick_run = ctk.CTkButton(self.central_frame, text="Quick Run (1 Minute)", command=self.start_quick_run, corner_radius=25, font = button_font, width=button_width, height=button_height)
        self.quick_run.grid(row=3, column=0, sticky='ns', pady=10)

        self.root.mainloop()

    def show_main_menu(self):
        # Recreate the central frame
        self.central_frame = ctk.CTkFrame(self.root, fg_color='white')
        self.central_frame.grid(row=1, column=1)

        # Add back the main menu buttons and label
        label_font = ctk.CTkFont(family='Bahnschrift SemiBold Condensed', size=40)
        button_font = ctk.CTkFont(family='Bahnschrift SemiBold Condensed', size=20)
        button_width = 200
        button_height = 50

        self.label = ctk.CTkLabel(self.central_frame, text='AFQOT Table Reading Quiz', font=label_font)
        self.label.grid(row=0, column=0, sticky='nsew', pady=10)

        self.full_test = ctk.CTkButton(self.central_frame, text="Full Test (7 Minutes)", command=self.start_full_test, corner_radius=25, font=button_font, width=button_width, height=button_height)
        self.full_test.grid(row=1, column=0, sticky='ns', pady=10)

        self.half_test = ctk.CTkButton(self.central_frame, text="Half Test (3.5 Minutes)", command=self.start_half_test, corner_radius=25, font=button_font, width=button_width, height=button_height)
        self.half_test.grid(row=2, column=0, sticky='ns', pady=10)

        self.quick_run = ctk.CTkButton(self.central_frame, text="Quick Run (1 Minute)", command=self.start_quick_run, corner_radius=25, font=button_font, width=button_width, height=button_height)
        self.quick_run.grid(row=3, column=0, sticky='ns', pady=10)

    def clear_widgets(self):
        for widget in self.central_frame.winfo_children():
            widget.destroy()
        self.central_frame.destroy()

    def start_full_test(self):
        self.clear_widgets()
        quiz = Quiz(num_question=40, time=7, root=self.root, main_window=self)

    def start_half_test(self):
        self.clear_widgets()
        quiz = Quiz(num_question=20, time=3.5, root=self.root, main_window=self)

    def start_quick_run(self):
        self.clear_widgets()
        quiz = Quiz(num_question=7, time=1, root=self.root, main_window=self)

        

# Instantiate the class to create the GUI
if __name__ == '__main__':
    app = MainWindow()
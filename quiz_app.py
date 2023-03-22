import customtkinter
from tkinter import messagebox
from tkinter import PhotoImage
import mysql.connector as mysql
import random
from datetime import datetime
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, DatetimeTickFormatter
from bokeh.io import curdoc



def get_data_from_db(mysql_user, my_sql_password, db_name, db_table):
    category_one_questions = []
    category_two_questions = []
    category_three_questions = []
    myDB = mysql.connect(host="localhost", user=mysql_user, passwd=my_sql_password, database=db_name)
    mycursor = myDB.cursor(buffered=True)
    sql = f"SELECT ID FROM {db_table} WHERE category='1'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for question in myresult:
        category_one_questions.append(int(question[0]))
    sql = f"SELECT ID FROM {db_table} WHERE category='2'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for question in myresult:
        category_two_questions.append(int(question[0]))
    sql = f"SELECT ID FROM {db_table} WHERE category='3'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for question in myresult:
        category_three_questions.append(int(question[0]))
    return category_one_questions, category_two_questions, category_three_questions


def show_questions(selected_ids, index, mysql_user, my_sql_password, db_name, db_table):
    myDB = mysql.connect(host="localhost", user=mysql_user, passwd=my_sql_password, database=db_name)
    mycursor = myDB.cursor(buffered=True)
    sql = f"SELECT question, optiona, optionb, optionc, optiond, answer FROM {db_table} WHERE ID='{selected_ids[index]}'"
    mycursor.execute(sql)
    myresults = mycursor.fetchall()
    for item in myresults:
        question = item[0]
        options = [item[1], item[2], item[3], item[4]]
        answer = item[5]
        random.shuffle(options)
    return question, options, answer


class App():
    def __init__(self, mysql_user, my_sql_password, db_name, db_table, db_results_table):
        self.mysql_user = mysql_user
        self.my_sql_password = my_sql_password
        self.db_name = db_name
        self.db_table = db_table
        self.db_results_table = db_results_table
        customtkinter.set_appearance_mode("system")
        customtkinter.set_default_color_theme("green")
        self.main_window = customtkinter.CTk()
        self.main_window.configure(fg_color="#1e1e1e")
        self.width = self.main_window.winfo_screenwidth()
        self.height = self.main_window.winfo_screenheight()
        self.main_window.geometry(f"{self.width}x{self.height}+0+0")
        self.main_window.resizable(True, True)
        app_logo = PhotoImage(file=r"C:\Users\georg\PycharmProjects\emagapp\app_logo_2.png")
        self.main_frame = customtkinter.CTkFrame(self.main_window, fg_color="#1e1e1e")
        self.main_frame.pack()
        self.start_junior_btn = customtkinter.CTkButton(self.main_frame, text=" Junior Quiz ",
                                                        font=("Calibri", 20), command=self.junior_quiz)
        self.start_medior_btn = customtkinter.CTkButton(self.main_frame, text=" Medior Quiz ",
                                                        font=("Calibri", 20), command=self.medior_quiz)
        self.start_senior_btn = customtkinter.CTkButton(self.main_frame, text=" Senior Quiz ",
                                                        font=("Calibri", 20), command=self.senior_quiz)
        self.exit_btn = customtkinter.CTkButton(self.main_frame, text="     Exit    ",
                                                command=lambda: self.exit_func(),
                                                fg_color="#391306", font=("Calibri", 20))
        self.insert_btn = customtkinter.CTkButton(self.main_frame, text="   Insert    ", fg_color="#B35504",
                                                  font=("Calibri", 20), command=self.insert_page)
        self.delete_btn = customtkinter.CTkButton(self.main_frame, text="   Delete    ",fg_color="#B35504",
                                                  font=("Calibri", 20), command=self.delete_page)
        self.results_history_btn = customtkinter.CTkButton(self.main_frame, text="Previous Results", fg_color="#B35504",
                                                  font=("Calibri", 20), command=self.history_page)
        self.start_junior_btn.grid(column=0, row=0, padx=10, pady=5)
        self.start_medior_btn.grid(column=1, row=0, padx=10, pady=5)
        self.start_senior_btn.grid(column=2, row=0, padx=10, pady=5)
        self.exit_btn.grid(column=1, row=2, padx=10, pady=5)
        self.insert_btn.grid(column=0, row=1, padx=10, pady=15)
        self.delete_btn.grid(column=1, row=1, padx=10, pady=15)
        self.results_history_btn.grid(column=2, row=1, padx=10, pady=15)
        self.logo = customtkinter.CTkLabel(self.main_window, image=app_logo, text=" ")
        self.logo.pack(pady=100)
        self.main_window.mainloop()

    def exit_func(self):
        if messagebox.askyesno(title="Exit?", message="Are you sure you want to exit?"):
            self.main_window.quit()

    def junior_quiz(self):
        self.quiztype = "junior"
        # Get all questions from DB together with corresponding category
        category_one, category_two, category_three = get_data_from_db(self.mysql_user, self.my_sql_password,
                                                                      self.db_name, self.db_table)
        self.selected_ids = []
        # Generate 25 random questions for Junior Quiz
        i = 1
        while i <= 25:
            if i < 20:
                id = random.choice(category_one)
                self.selected_ids.append(id)
                category_one.remove(id)
                i += 1
            elif i < 23:
                id = random.choice(category_two)
                self.selected_ids.append(id)
                category_two.remove(id)
                i += 1
            else:
                id = random.choice(category_three)
                self.selected_ids.append(id)
                category_three.remove(id)
                i += 1
        # Shuffle selected questions
        random.shuffle(self.selected_ids)
        # Start quiz
        self.score = 0
        self.question = iter(range(0, 26))
        self.quiz(int(next(self.question)))

    # Start Quiz
    def quiz(self, index):
        self.index = index
        question, options, self.answer = show_questions(self.selected_ids, self.index, self.mysql_user,
                                                        self.my_sql_password,
                                                        self.db_name, self.db_table)
        self.quiz_frame = customtkinter.CTkFrame(self.main_window, fg_color="#1e1e1e", height=self.height, width=self.width)
        self.quiz_frame.place(x=0, y=0)
        self.back_button = customtkinter.CTkButton(self.quiz_frame, text="<--Back to main menu", font=("Calibri", 20),
                                                   command=lambda: self.quiz_frame.destroy(), fg_color="#391306")
        self.back_button.place(x=800, y=60)
        # Display question
        self.question_label = customtkinter.CTkLabel(self.quiz_frame, text=f"{index + 1}. {question}", fg_color="#1e1e1e",
                                               font=("Serif", 20))
        self.question_label.place(x=40, y=100)
        # Display answer options
        self.var = customtkinter.StringVar()
        self.radio_btn1 = customtkinter.CTkRadioButton(self.quiz_frame, text=options[0],
                                                       fg_color="#1e1e1e", font=("Serif", 20), variable=self.var,
                                                       value=options[0])
        self.radio_btn2 = customtkinter.CTkRadioButton(self.quiz_frame, text=options[1],
                                                       fg_color="#1e1e1e", font=("Serif", 20), variable=self.var,
                                                       value=options[1])
        self.radio_btn3 = customtkinter.CTkRadioButton(self.quiz_frame, text=options[2],
                                                       fg_color="#1e1e1e", font=("Serif", 20), variable=self.var,
                                                       value=options[2])
        self.radio_btn4 = customtkinter.CTkRadioButton(self.quiz_frame, text=options[3],
                                                       fg_color="#1e1e1e", font=("Serif", 20), variable=self.var,
                                                       value=options[3])
        self.submit_button = customtkinter.CTkButton(self.quiz_frame, text="Submit answer", font=("Calibri", 20))
        # Submit answer
        self.submit_button.bind("<ButtonRelease-1>", self.check_answer)
        self.submit_button.place(x=80, y=400)
        self.radio_btn1.place(x=40, y=150)
        self.radio_btn2.place(x=40, y=200)
        self.radio_btn3.place(x=40, y=250)
        self.radio_btn4.place(x=40, y=300)

    def check_answer(self, event):
        if self.var.get() == self.answer:
            try:
                # Correct answer scenario
                self.score += 4
                messagebox.showinfo("Congrats", "Your answer is correct.")
                self.quiz_frame.destroy()
                self.quiz(int(next(self.question)))
                print(1+1)
            except IndexError:
                # End of quiz scenario
                messagebox.showinfo("Completed", f"Your score is {self.score}.")
                date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                myDB = mysql.connect(host="localhost", user=self.mysql_user, passwd=self.my_sql_password,
                                     database=self.db_name)
                mycursor = myDB.cursor(buffered=True)
                sql = f"INSERT INTO {self.db_results_table} (quiz_type, score, date_time) VALUES (%s, %s, %s)"
                val = (self.quiztype, self.score, date_time)
                mycursor.execute(sql, val)
                myDB.commit()
        else:
            try:
                # Incorrect answer scenario
                messagebox.showinfo("Sorry", f"Your answer is incorrect. Correct answer: {self.answer}.")
                self.quiz_frame.destroy()
                self.quiz(int(next(self.question)))
            except IndexError:
                # End of quiz scenario
                messagebox.showinfo("Completed", f"Your score is {self.score}.")
                date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                myDB = mysql.connect(host="localhost", user=self.mysql_user, passwd=self.my_sql_password,
                                     database=self.db_name)
                mycursor = myDB.cursor(buffered=True)
                sql = f"INSERT INTO {self.db_results_table} (quiz_type, score, date_time) VALUES (%s, %s, %s)"
                val = (self.quiztype, self.score, date_time)
                mycursor.execute(sql, val)
                myDB.commit()

    def medior_quiz(self):
        self.quiztype = "medior"
        category_one, category_two, category_three = get_data_from_db(self.mysql_user, self.my_sql_password,
                                                                      self.db_name, self.db_table)
        self.selected_ids = []
        i = 1
        while i < 26:
            if i < 6:
                id = random.choice(category_one)
                self.selected_ids.append(id)
                category_one.remove(id)
                i += 1
            elif i < 21:
                id = random.choice(category_two)
                self.selected_ids.append(id)
                category_two.remove(id)
                i += 1
            else:
                id = random.choice(category_three)
                self.selected_ids.append(id)
                category_three.remove(id)
                i += 1
        random.shuffle(self.selected_ids)
        self.score = 0
        self.question = iter(range(0, 26))
        self.quiz(int(next(self.question)))

    def senior_quiz(self):
        self.quiztype = "senior"
        category_one, category_two, category_three = get_data_from_db(self.mysql_user, self.my_sql_password,
                                                                      self.db_name, self.db_table)
        self.selected_ids = []
        i = 1
        while i < 26:
            if i < 11:
                id = random.choice(category_two)
                self.selected_ids.append(id)
                category_two.remove(id)
                i += 1
            else:
                id = random.choice(category_three)
                self.selected_ids.append(id)
                category_three.remove(id)
                i += 1
        random.shuffle(self.selected_ids)
        self.score = 0
        self.question = iter(range(0, 26))
        self.quiz(int(next(self.question)))

    def insert_page(self):
        self.add_frame = customtkinter.CTkFrame(self.main_window, fg_color="#1e1e1e", height=self.height, width=self.width)
        self.add_frame.place(x=0, y=0)
        self.category = customtkinter.CTkLabel(self.add_frame, text="Category:", fg_color="#1e1e1e", font=("Serif", 20))
        self.category_box = customtkinter.CTkEntry(self.add_frame, width=400, font=("Serif", 20))
        self.question_label = customtkinter.CTkLabel(self.add_frame, text="Question:", fg_color="#1e1e1e", font=("Serif", 20))
        self.question_box = customtkinter.CTkEntry(self.add_frame, width=400, font=("Serif", 20))
        self.option1 = customtkinter.CTkLabel(self.add_frame, text="Option 1: ", fg_color="#1e1e1e", font=("Serif", 20))
        self.option1_box = customtkinter.CTkEntry(self.add_frame, width=400, font=("Serif", 20))
        self.option2 = customtkinter.CTkLabel(self.add_frame, text="Option 2: ", fg_color="#1e1e1e", font=("Serif", 20))
        self.option2_box = customtkinter.CTkEntry(self.add_frame, width=400, font=("Serif", 20))
        self.option3 = customtkinter.CTkLabel(self.add_frame, text="Option 3: ", fg_color="#1e1e1e", font=("Serif", 20))
        self.option3_box = customtkinter.CTkEntry(self.add_frame, width=400, font=("Serif", 20))
        self.option4 = customtkinter.CTkLabel(self.add_frame, text="Option 4: ", fg_color="#1e1e1e", font=("Serif", 20))
        self.option4_box = customtkinter.CTkEntry(self.add_frame, width=400, font=("Serif", 20))
        self.answer = customtkinter.CTkLabel(self.add_frame, text="Correct: ", fg_color="#1e1e1e", font=("Serif", 20))
        self.answer_box = customtkinter.CTkEntry(self.add_frame, width=400, font=("Serif", 20))
        self.insert_question = customtkinter.CTkButton(self.add_frame, text="--> Submit   ", font=("Calibri", 20))
        self.insert_question.bind("<ButtonRelease-1>", self.add_to_db)
        self.category.place(x=40, y=100)
        self.category_box.place(x=150, y=100)
        self.question_label.place(x=40, y=150)
        self.question_box.place(x=150, y=150)
        self.option1.place(x=40, y=200)
        self.option1_box.place(x=150, y=200)
        self.option2.place(x=40, y=250)
        self.option2_box.place(x=150, y=250)
        self.option3.place(x=40, y=300)
        self.option3_box.place(x=150, y=300)
        self.option4.place(x=40, y=350)
        self.option4_box.place(x=150, y=350)
        self.answer.place(x=40, y=400)
        self.answer_box.place(x=150, y=400)
        self.insert_question.place(x=800, y=200)
        self.back_button = customtkinter.CTkButton(self.add_frame, text="<--Back to main menu", font=("Calibri", 20),
                                                   command=lambda: self.add_frame.destroy(), fg_color="#391306")
        self.back_button.place(x=800, y=60)

    def add_to_db(self, event):
        _category = int(self.category_box.get())
        _question = self.question_box.get()
        _option1 = self.option1_box.get()
        _option2 = self.option2_box.get()
        _option3 = self.option3_box.get()
        _option4 = self.option4_box.get()
        _answer = self.answer_box.get()
        try:
            myDB = mysql.connect(host="localhost", user=self.mysql_user, passwd=self.my_sql_password,
                                 database=self.db_name)
            mycursor = myDB.cursor(buffered=True)
            sql = f"INSERT INTO {self.db_table} (category, question, optiona, optionb, optionc, optiond, answer) " \
                  f"VALUES(%s, " \
                  "%s, %s, %s, %s, %s, %s) "
            val = (_category, _question, _option1, _option2, _option3, _option4, _answer)
            mycursor.execute(sql, val)
            myDB.commit()
            messagebox.showinfo("Success", "New question added")
            mycursor.close()
            myDB.close()
            for box in [self.category_box, self.question_box, self.option1_box, self.option2_box, self.option3_box,
                        self.option4_box, self.answer_box]:
                box.delete(0, customtkinter.END)
        except:
            messagebox.showinfo("Error", "Please contact developer")

    def delete_page(self):
        myDB = mysql.connect(host="localhost", user=self.mysql_user, passwd=self.my_sql_password,
                                 database=self.db_name)
        mycursor = myDB.cursor(buffered=True)
        mycursor.execute(f"SELECT question, ID  FROM {self.db_table}")
        results = mycursor.fetchall()
        self.question_details = []
        for result in results:
            self.question_details.append(list(result))
        mycursor.close()
        myDB.close()
        questions = [item[0] for item in self.question_details]
        self.add_frame = customtkinter.CTkFrame(self.main_window, fg_color="#1e1e1e", height=self.height, width=self.width)
        self.add_frame.place(x=0, y=0)
        self.back_button = customtkinter.CTkButton(self.add_frame, text="<--Back to main menu", font=("Calibri", 20),
                                                   command=lambda: self.add_frame.destroy(), fg_color="#391306")
        self.back_button.place(x=800, y=60)
        self.read_intro = customtkinter.CTkLabel(self.add_frame, text="Current questions:",
                                                 fg_color="#1e1e1e", font=("Calibri", 20, "bold"))
        self.read_intro.place(x=40, y=60)
        self.clicked = customtkinter.StringVar()
        self.clicked.set("Select question...")
        drop = customtkinter.CTkOptionMenu(self.add_frame, variable=self.clicked, values=questions,
                                           font=("Calibri", 20))
        drop.place(x=40, y=150)
        self.delete_selected_button = customtkinter.CTkButton(self.add_frame, text="--> Delete", font=("Calibri", 20))
        self.delete_selected_button.bind("<ButtonRelease-1>", self.delete_from_db)
        self.delete_selected_button.place(x=800, y=400)

    def delete_from_db(self, event):
        choice = self.clicked.get()
        try:
            myDB = mysql.connect(host="localhost", user=self.mysql_user, passwd=self.my_sql_password,
                                 database=self.db_name)
            mycursor = myDB.cursor(buffered=True)
            sql = f"DELETE FROM {self.db_table} WHERE question = '{choice}'"
            mycursor.execute(sql)
            myDB.commit()
            messagebox.showinfo("Success", "Question deleted")
            self.add_frame.destroy()
            mycursor.close()
            myDB.close()
            self.delete_page()
        except:
            messagebox.showinfo("Error", "Please contact developer")

    def history_page(self):
        myDB = mysql.connect(host="localhost", user=self.mysql_user, passwd=self.my_sql_password,
                                 database=self.db_name)
        mycursor = myDB.cursor(buffered=True)
        mycursor.execute(f"SELECT quiz_type, score, date_time FROM {self.db_results_table}")
        myresult = mycursor.fetchall()
        data = []
        for item in myresult:
            data.append((item[1], item[2], item[0]))
        df = pd.DataFrame(data, columns=["Score", "Date", "Quiz_type"])
        curdoc().theme = "dark_minimal"
        tooltips = HoverTool(tooltips=[
            ("index", "$index"),
            ("Date", "$x{%F}"), ("Quiz_type", "@Quiz_type"), ("Score", "@Score"),
        ], formatters={"$x": "datetime"})
        p = figure(title="Historical data", x_axis_label="Date", x_axis_type="datetime", y_axis_label="Score",
                   tools=[tooltips], width=self.width - 50,
                   height=self.height - 120)
        p.circle("Date", "Score", size=10, source=df)
        p.line(source=df, x="Date", y="Score", color="red", line_width=1)
        p.xaxis[0].formatter = DatetimeTickFormatter(months="%Y-%m-%d")
        show(p)
        mycursor.close()
        myDB.close()


if __name__ == "__main__":
    app = App(mysql_user="", my_sql_password="", db_name="z", db_table="",
              db_results_table="")

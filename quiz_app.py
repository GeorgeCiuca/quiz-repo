import tkinter as tk
from tkinter import messagebox
import mysql.connector as mysql
import random
from datetime import datetime
import pandas as pd
from bokeh.plotting import figure, show
from bokeh.models import HoverTool, DatetimeTickFormatter
from bokeh.io import curdoc


def get_questions_from_db():
    myDB = mysql.connect(host="localhost", user="root",
                         passwd="mysqlPassword@", database="pythonquiz")
    mycursor = myDB.cursor(buffered=True)
    mycursor.execute("SELECT question, ID  FROM questions")
    results = mycursor.fetchall()
    data = []
    for result in results:
        data.append(list(result))
    mycursor.close()
    myDB.close()
    return data


def get_data_from_db():
    category_one = []
    category_two = []
    category_three = []
    myDB = mysql.connect(host="localhost", user="root",
                         passwd="mysqlPassword@", database="pythonquiz")
    mycursor = myDB.cursor(buffered=True)
    sql = "SELECT ID FROM questions WHERE category='1'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for id in myresult:
        category_one.append(int(id[0]))
    sql = "SELECT ID FROM questions WHERE category='2'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for id in myresult:
        category_two.append(int(id[0]))
    sql = "SELECT ID FROM questions WHERE category='3'"
    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    for id in myresult:
        category_three.append(int(id[0]))
    return category_one, category_two, category_three


def show_questions(selected_ids, index):
    myDB = mysql.connect(host="localhost", user="root",
                         passwd="mysqlPassword@", database="pythonquiz")
    mycursor = myDB.cursor(buffered=True)
    sql = f"SELECT question, optiona, optionb, optionc, optiond, answer FROM questions WHERE ID='{selected_ids[index]}'"
    mycursor.execute(sql)
    myresults = mycursor.fetchall()
    for item in myresults:
        question = item[0]
        options = [item[1], item[2], item[3], item[4]]
        answer = item[5]
        random.shuffle(options)
    return question, options, answer


class App():
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Python Quiz --> Test your knowledge")
        self.width = self.window.winfo_screenwidth()
        self.height = self.window.winfo_screenheight()
        self.window.geometry("%dx%d" % (self.width, self.height))
        self.window.state('zoomed')
        self.window.resizable(True, True)
        self.window.configure(bg="#2B4D59")
        cat_icon = tk.PhotoImage(
            file=r"C:\Users\georg\PycharmProjects\pythonquiz\cat.png")
        app_logo = tk.PhotoImage(
            file=r"C:\Users\georg\PycharmProjects\pythonquiz\app_logo_2.png")
        self.window.iconphoto(False, cat_icon)
        self.menu = tk.Menu(self.window)
        self.menu.config(bg="green")
        self.startmenu = tk.Menu(self.menu, font=(
            "Calibri", 14), bg="#31473A", fg="#EDF4F2")
        self.menu.add_cascade(label="Start", menu=self.startmenu)
        self.startmenu.add_command(
            label="Level --> Junior", command=self.junior_quiz)
        self.startmenu.add_command(
            label="Level --> Medior", command=self.medior_quiz)
        self.startmenu.add_command(
            label="Level --> Senior", command=self.senior_quiz)
        self.resultsmenu = tk.Menu(self.window, font=(
            "Calibri", 14), bg="#31473A", fg="#EDF4F2")
        self.menu.add_cascade(label="Options", menu=self.resultsmenu)
        self.resultsmenu.add_command(
            label="See previous results", command=self.graph_from_db)
        self.resultsmenu.add_separator()
        self.resultsmenu.add_separator()
        self.resultsmenu.add_command(
            label="Add new question", command=self.insert_page)
        self.resultsmenu.add_command(
            label="Delete question", command=self.delete_page)
        self.windowmenu = tk.Menu(self.menu, font=(
            "Calibri", 14), bg="#31473A", fg="#EDF4F2")
        self.menu.add_cascade(label="Window", menu=self.windowmenu)
        self.windowmenu.add_command(
            label="Minimize", command=self.window.iconify)
        self.windowmenu.add_command(label="Exit", command=self.exit_func)
        self.start_junior_btn = tk.Button(self.window, text=" Junior Quiz ", bg="#31473A", fg="#EDF4F2",
                                          font=("Calibri", 14), command=self.junior_quiz)
        self.start_medior_btn = tk.Button(self.window, text=" Medior Quiz ", bg="#39998E", fg="#EDF4F2",
                                          font=("Calibri", 14), command=self.medior_quiz)
        self.start_senior_btn = tk.Button(self.window, text=" Senior Quiz ", bg="#DA674A", fg="#EDF4F2",
                                          font=("Calibri", 14), command=self.senior_quiz)
        self.get_history_btn = tk.Button(self.window, text="   History   ", bg="#39998E", fg="#EDF4F2",
                                         font=("Calibri", 14))
        self.get_history_btn.bind("<ButtonRelease-1>", self.delete_page)
        self.exit_btn = tk.Button(self.window, text="     Exit    ", command=lambda: self.exit_func(), bg="#2B4D59",
                                  fg="#EDF4F2", font=("Calibri", 14))
        self.start_junior_btn.place(x=650, y=60)
        self.start_medior_btn.place(x=800, y=60)
        self.start_senior_btn.place(x=950, y=60)
        self.image_frame = tk.Label(self.window, image=app_logo, bg="#2B4D59")
        self.image_frame.place(x=575, y=200)
        self.window.config(menu=self.menu)
        self.window.mainloop()

    def exit_func(self):
        if messagebox.askyesno(title="Exit?", message="Are you sure you want to exit?"):
            self.window.quit()

    def junior_quiz(self):
        self.quiztype = "junior"
        category_one, category_two, category_three = get_data_from_db()
        self.selected_ids = []
        i = 1
        while i < 26:
            if i < 16:
                id = random.choice(category_one)
                self.selected_ids.append(id)
                category_one.remove(id)
                i += 1
            else:
                id = random.choice(category_two)
                self.selected_ids.append(id)
                category_two.remove(id)
                i += 1
        random.shuffle(self.selected_ids)
        self.score = 0
        self.iterable = iter(range(0, 26))
        self.quiz(int(next(self.iterable)))

    def quiz(self, index):
        self.index = index
        question, options, self.answer = show_questions(
            self.selected_ids, self.index)
        self.quiz_frame = tk.Frame(self.window, bg="#2B4D59")
        self.quiz_frame.place(x=0, y=0, height=self.height, width=self.width)
        self.back_button = tk.Button(self.quiz_frame, text="<--Back to main menu", font=("Calibri", 15),
                                     command=lambda: self.quiz_frame.destroy(), bg="#2B4D59", fg="#EDF4F2")
        self.back_button.place(x=800, y=60)
        self.question = tk.Label(self.quiz_frame, text=f"{index + 1}. {question}", fg="#EDF4F2", bg="#2B4D59",
                                 font=("Serif", 15))
        self.question.place(x=40, y=100)
        self.var = tk.StringVar()
        self.radio_btn1 = tk.Radiobutton(self.quiz_frame, text=options[0], selectcolor="black", fg="#EDF4F2",
                                         bg="#2B4D59", font=("Serif", 14), variable=self.var, value=options[0])
        self.radio_btn2 = tk.Radiobutton(self.quiz_frame, text=options[1], selectcolor="black", fg="#EDF4F2",
                                         bg="#2B4D59", font=("Serif", 14), variable=self.var, value=options[1])
        self.radio_btn3 = tk.Radiobutton(self.quiz_frame, text=options[2], selectcolor="black", fg="#EDF4F2",
                                         bg="#2B4D59", font=("Serif", 14), variable=self.var, value=options[2])
        self.radio_btn4 = tk.Radiobutton(self.quiz_frame, text=options[3], selectcolor="black", fg="#EDF4F2",
                                         bg="#2B4D59", font=("Serif", 14), variable=self.var, value=options[3])
        self.submit_button = tk.Button(self.quiz_frame, text="Submit answer", font=("Calibri", 15),
                                       command=lambda: self.quiz_frame.destroy(), bg="#7C8363", fg="#EDF4F2")
        self.submit_button.bind("<ButtonRelease-1>", self.check_answer)
        self.submit_button.place(x=80, y=400)
        self.radio_btn1.place(x=40, y=150)
        self.radio_btn2.place(x=40, y=200)
        self.radio_btn3.place(x=40, y=250)
        self.radio_btn4.place(x=40, y=300)

    def check_answer(self, event):
        if self.var.get() == self.answer:
            try:
                self.score += 4
                messagebox.showinfo("Congrats", "Your answer is correct.")
                self.quiz_frame.destroy()
                self.quiz(int(next(self.iterable)))
            except IndexError:
                messagebox.showinfo(
                    "Completed", f"Your score is {self.score}.")
                date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                myDB = mysql.connect(
                    host="localhost", user="root", passwd="mysqlPassword@", database="pythonquiz")
                mycursor = myDB.cursor(buffered=True)
                sql = "INSERT INTO results (quiz_type, score, date_time) VALUES (%s, %s, %s)"
                val = (self.quiztype, self.score, date_time)
                mycursor.execute(sql, val)
                myDB.commit()
        else:
            try:
                messagebox.showinfo("Sorry", "Your answer is incorrect.")
                self.quiz_frame.destroy()
                self.quiz(int(next(self.iterable)))
            except IndexError:
                messagebox.showinfo(
                    "Completed", f"Your score is {self.score}.")
                date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                myDB = mysql.connect(
                    host="localhost", user="root", passwd="mysqlPassword@", database="pythonquiz")
                mycursor = myDB.cursor(buffered=True)
                sql = "INSERT INTO results (quiz_type, score, date_time) VALUES (%s, %s, %s)"
                val = (self.quiztype, self.score, date_time)
                mycursor.execute(sql, val)
                myDB.commit()

    def medior_quiz(self):
        self.quiztype = "medior"
        category_one, category_two, category_three = get_data_from_db()
        self.selected_ids = []
        i = 1
        while i < 26:
            if i < 6:
                id = random.choice(category_one)
                self.selected_ids.append(id)
                category_one.remove(id)
                i += 1
            else:
                id = random.choice(category_two)
                self.selected_ids.append(id)
                category_two.remove(id)
                i += 1
        random.shuffle(self.selected_ids)
        self.score = 0
        self.iterable = iter(range(0, 26))
        self.quiz(int(next(self.iterable)))

    def senior_quiz(self):
        self.quiztype = "senior"
        category_one, category_two, category_three = get_data_from_db()
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
        self.iterable = iter(range(0, 26))
        self.quiz(int(next(self.iterable)))

    def insert_page(self):
        self.add_frame = tk.Frame(self.window, bg="#2B4D59")
        self.add_frame.place(x=0, y=0, height=self.height, width=self.width)
        self.category = tk.Label(
            self.add_frame, text="Category:", bg="#2B4D59", fg="white", font=("Serif", 15))
        self.category_box = tk.Entry(
            self.add_frame, width=50, font=("Serif", 15))
        self.question = tk.Label(
            self.add_frame, text="Question:", bg="#2B4D59", fg="white", font=("Serif", 15))
        self.question_box = tk.Entry(
            self.add_frame, width=50, font=("Serif", 15))
        self.option1 = tk.Label(
            self.add_frame, text="Option 1: ", bg="#2B4D59", fg="white", font=("Serif", 15))
        self.option1_box = tk.Entry(
            self.add_frame, width=50, font=("Serif", 15))
        self.option2 = tk.Label(
            self.add_frame, text="Option 2: ", bg="#2B4D59", fg="white", font=("Serif", 15))
        self.option2_box = tk.Entry(
            self.add_frame, width=50, font=("Serif", 15))
        self.option3 = tk.Label(
            self.add_frame, text="Option 3: ", bg="#2B4D59", fg="white", font=("Serif", 15))
        self.option3_box = tk.Entry(
            self.add_frame, width=50, font=("Serif", 15))
        self.option4 = tk.Label(
            self.add_frame, text="Option 4: ", bg="#2B4D59", fg="white", font=("Serif", 15))
        self.option4_box = tk.Entry(
            self.add_frame, width=50, font=("Serif", 15))
        self.answer = tk.Label(
            self.add_frame, text="Correct: ", bg="#2B4D59", fg="white", font=("Serif", 15))
        self.answer_box = tk.Entry(
            self.add_frame, width=50, font=("Serif", 15))
        self.insert_question = tk.Button(self.add_frame, text="--> Submit   ", font=("Calibri", 15), bg="#7C8363",
                                         fg="#EDF4F2")
        self.insert_question.bind("<ButtonRelease-1>", self.add_to_db)
        self.category.place(x=40, y=100)
        self.category_box.place(x=150, y=100)
        self.question.place(x=40, y=150)
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
        self.back_button = tk.Button(self.add_frame, text="<--Back to main menu", font=("Calibri", 15),
                                     command=lambda: self.add_frame.destroy(), bg="#2B4D59", fg="#EDF4F2")
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
            myDB = mysql.connect(host="localhost", user="root",
                                 passwd="mysqlPassword@", database="pythonquiz")
            mycursor = myDB.cursor(buffered=True)
            sql = "INSERT INTO questions(category, question, optiona, optionb, optionc, optiond, answer) VALUES(%s, " \
                  "%s, %s, %s, %s, %s, %s) "
            val = (_category, _question, _option1,
                   _option2, _option3, _option4, _answer)
            mycursor.execute(sql, val)
            myDB.commit()
            messagebox.showinfo("Success", "New question added")
            mycursor.close()
            myDB.close()
            for box in [self.category_box, self.question_box, self.option1_box, self.option2_box, self.option3_box,
                        self.option4_box, self.answer_box]:
                box.delete(0, tk.END)
        except:
            messagebox.showinfo("Error", "Please contact developer")

    def delete_page(self):
        self.question_details = get_questions_from_db()
        questions = [item[0] for item in self.question_details]
        self.add_frame = tk.Frame(self.window, bg="#2B4D59")
        self.add_frame.place(x=0, y=0, height=self.height, width=self.width)
        self.back_button = tk.Button(self.add_frame, text="<--Back to main menu", font=("Calibri", 15),
                                     command=lambda: self.add_frame.destroy(), bg="#2B4D59", fg="#EDF4F2")
        self.back_button.place(x=800, y=60)
        self.read_intro = tk.Label(self.add_frame, text="Current questions:",
                                   fg="white", bg="#31473A",
                                   font=("Calibri", 15, "bold"))
        self.read_intro.place(x=40, y=60)
        self.clicked = tk.StringVar()
        self.clicked.set("Select question...")
        drop = tk.OptionMenu(self.add_frame, self.clicked, *questions)
        drop.config(font=("Calibri", 15))
        drop.place(x=40, y=150)
        self.delete_selected_button = tk.Button(self.add_frame, text="--> Delete", font=("Calibri", 15), bg="#A36A00",
                                                fg="#EDF4F2")
        self.delete_selected_button.bind(
            "<ButtonRelease-1>", self.delete_from_db)
        self.delete_selected_button.place(x=800, y=400)

    def delete_from_db(self, event):
        choice = self.clicked.get()
        try:
            myDB = mysql.connect(host="localhost", user="root",
                                 passwd="mysqlPassword@", database="pythonquiz")
            mycursor = myDB.cursor(buffered=True)
            sql = f"DELETE FROM questions WHERE question = '{choice}'"
            mycursor.execute(sql)
            myDB.commit()
            messagebox.showinfo("Success", "Question deleted")
            self.add_frame.destroy()
            mycursor.close()
            myDB.close()
            self.delete_page()
        except:
            messagebox.showinfo("Error", "Please contact developer")

    def graph_from_db(self):
        myDB = mysql.connect(host="localhost", user="root",
                             passwd="mysqlPassword@", database="pythonquiz")
        mycursor = myDB.cursor(buffered=True)
        mycursor.execute("SELECT quiz_type, score, date_time FROM results")
        myresult = mycursor.fetchall()
        data = []
        for item in myresult:
            data.append((item[1], item[2], item[0]))
        df = pd.DataFrame(data, columns=["Score", "Date", "Quiz_type"])
        curdoc().theme = "dark_minimal"
        tooltips = HoverTool(tooltips=[
            ("index", "$index"),
            ("Date", "$x{%F}"), ("Quiz_type",
                                 "@Quiz_type"), ("Score", "@Score"),
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


if __name__ == '__main__':
    app = App()

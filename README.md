# Python Quiz App

App is designed in order to improve Python knowledge for various areas/modules/libraries. GUI is handled through Tkinter.
It works based on questions and 4 potential answers from which one is correct.
All questions, potential answers and correct answers will be stored in a local MySQL database.
Each question has a category (1,2 and 3) which stands for complexity (increasing).
There are 3 levels inside the app (junior, medior and senior), and a specific number of questions will be randomly selected from the Database based on the category.
Each quiz will represent 25 questions and in the end a score will be registered (4 points / question).
Scores will be registered in another database and will be visible in a chart inside the app. Chart is represented via Bokeh module.


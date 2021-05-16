import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from ttkthemes import ThemedTk
import calendar
import datetime
import math
import requests
import json
import webbrowser


class Resources(ttk.Frame):
    def __init__(self, parent, app):
        ttk.Frame.__init__(self, parent)

        self.app = app
        self.parent = parent

        ttk.Label(self, text="This app is meant to help keep track of your mental health throughout\na long period of time and allow you to further understand trends in\nyour daily moods. If you noticed long periods of negative days, don’t forget\nto reach out and remember that there are resources there out for you.", padding=10).pack(side = tk.TOP)
        ttk.Label(self, text="Mental Health Websites:", padding=10).pack(side = tk.TOP) 
        ttk.Label(self, text="Mental Health Hotlines:\nNational Suicide Prevention Hotline: (800) 273-TALK (8255)\n24/7 Crisis Hotline: Call: (512) 472-HELP (4357) & TTY: (512) 703-1395 TTY\n\nSexual Assault Hotline: 1-800-656-4673\nCrisis Text Line: Text “BRAVE” to 741741", padding=10).pack(side = tk.BOTTOM)
        ttk.Button(self, text="Active Minds: https://www.activeminds.org/", command=self.active, width='44').pack(side=tk.BOTTOM)
        ttk.Button(self, text="MHFA: https://www.mentalhealthfirstaid.org/", command=self.suicide, width='44').pack(side=tk.BOTTOM)
    
    def active(self):
        webbrowser.open("https://www.activeminds.org/")
    
    def suicide(self):
        webbrowser.open("https://www.mentalhealthfirstaid.org/")

class CalendarPage(ttk.Frame):
    def __init__(self, parent, app):
        ttk.Frame.__init__(self, parent)

        self.app = app
        self.parent = parent

        
        self.calendarInit()
    
    def calendarInit(self):
        date = datetime.datetime.now()
        year = date.year
        month = date.month
        cal_content = calendar.TextCalendar(firstweekday=0).itermonthdays(year, month)
        c = 0
        r = 1
        for i in range(7):
            if (i == 0):
                day = 'MON'
            if (i == 1):
                day = 'TUE'
            if (i == 2):
                day = 'WED'
            if (i == 3):
                day = 'THU'
            if (i == 4):
                day = 'FRI'
            if (i == 5):
                day = 'SAT'
            if (i == 6):
                day = 'SUN'
            button = ttk.Button(self, text=day, command=self.nothing, width='7')
            button.grid(column=i, row=0)

        for x in cal_content:
            #Add days
            #Make empty days empty
            if (x == 0):
                button = ttk.Button(self, text='', command=self.launch, width='7')
            else:
                #Get each color
                f = open('calendardata.json')
                storage = json.load(f)
                
                try:
                    bg = storage[str(x)]["color"]
                except:
                    bg = 'grey'
                
                f.close()

                button = tk.Button(self, text=x, command=self.launch, width='7', bg=bg)

            #Gridding
            #Columns increase until reaches 6
            button.grid(column=c, row=r)
            c += 1

            if (c > 6):
                c = 0
                r += 1

    def nothing(self):
        pass

    def launch(self):
        pass

class Feedback(ttk.Frame):
    def __init__(self, parent, app):
        ttk.Frame.__init__(self, parent)

        self.app = app
        self.parent = parent

        self.dayInit()
    
    def dayInit(self):
        #Date
        day = datetime.datetime.now().strftime("%b %d")
        date = ttk.Label(self, text=day, font=("Courier New Bold", 60), borderwidth=2, relief="solid", padding=10)
        date.pack(side = tk.TOP)

        #Entry
        button = ttk.Button(self, text="Add Entry", command=self.entry, width='10')
        button.pack(side = tk.BOTTOM)

        #Quote
        response = requests.get("https://quotes.rest/qod?language=en")
        json_resp = response.json()
        quote = json_resp["contents"]["quotes"][0]["quote"]
        author = json_resp["contents"]["quotes"][0]["author"]
        fullQuote = quote + " - " + author
        ttk.Label(self, text= fullQuote, font=("Garamond", 14), padding=10).pack(side = tk.BOTTOM)
    
    def entry(self):
        ConfigWindow(self, self.app)    

class ConfigWindow(tk.Toplevel):
    def __init__(self, parent, app):
        tk.Toplevel.__init__(self, parent)

        self.parent = parent
        self.app = app
        self.questions = ["I was frequently frustrated/agitated today", "I couldn’t seem to experience any positive feeling today", "I found it difficult to work up the initiative to do my work","I was frequently worried/stressed today", "I felt that I had nothing to look forward to", "I felt down-hearted today", "I was unable to be enthusiastic about anything", "I did not feel very much self-worth today", "I found it difficult to relax today", "I had little motivation today"]
        self.i = 0
        self.total = 0
        self.buttonInit()
        self.answer = tk.IntVar()
    
    def buttonInit(self):
        instructions = "How much often did these statement apply to you today (1-5)?\n5 - Never\n4 - Sometimes\n3 - Often\n2 - Almost Always\n1 - Always"
        self.label = ttk.Label(self, text=instructions, font=("Courier New Bold", 12), width='60')
        self.label.grid(row=0, columnspan=5, rowspan=5)

        ttk.Button(self, text="Next", command=self.question, width='94').grid(row=7, columnspan=5)

    def question(self):
        
        self.total += self.answer.get()

        self.one = ttk.Radiobutton(self, value=1, variable=self.answer, text="1", width='14').grid(column=0, row=6)
        self.two = ttk.Radiobutton(self, value=2, variable=self.answer, text="2", width='14').grid(column=1, row=6)
        self.three = ttk.Radiobutton(self, value=3, variable=self.answer, text="3", width='14').grid(column=2, row=6)
        self.four = ttk.Radiobutton(self, value=4, variable=self.answer, text="4", width='14').grid(column=3, row=6)
        self.five = ttk.Radiobutton(self, value=5, variable=self.answer, text="5", width='14').grid(column=4, row=6)



        if (self.i == len(self.questions)):
            self.commit()
            return

        self.label.configure(text=self.questions[self.i] + "\n\n\n\n\n")

        self.i += 1

    def commit(self):
        average = self.total / len(self.questions)
        color = self.assignColors(average)
        day = datetime.datetime.now().strftime("%d")

        #Commit to json
        storage = {}        
        storage[day] = {'color': color, 'average': average}
        with open('calendardata.json', 'r+') as file:
            data = json.load(file)
            data.update(storage)
            file.seek(0)
            json.dump(data, file, indent=4)
        
        #Close window
        self.destroy()
        self.update()

        #Update calendar
        self.app.updateCalendar()

    
    def assignColors(self, findAverage):
        if findAverage >= 1 and findAverage <= 1.8:
            return("#CC0000")
        elif findAverage > 1.8 and findAverage <= 2.6:
            return("#FF8000")
        elif findAverage > 2.6 and findAverage <= 3.4:
            return("#ffff00")
        elif findAverage > 3.4 and findAverage <= 4.2:
            return("#33cc33")
        elif findAverage > 4.2 and findAverage <= 5:
            return("#1F51FF")

class App(ThemedTk):
    def __init__(self):
        super().__init__()
        self.title("MentalHealthTracker")
        self.configure(theme='equilux')
        
        self.nb = self.create_notebook()
    
    def create_notebook(self):
        tabs = ttk.Notebook(self)
        
        main = Feedback(tabs, self)
        tabs.add(main, text="Main")
        self.calendar = CalendarPage(tabs, self)
        tabs.add(self.calendar, text="Calendar")
        resource = Resources(tabs, self)
        tabs.add(resource, text="Resources")
        
        tabs.pack()
        return tabs
    
    def updateCalendar(self):
        self.calendar.destroy()
        self.calendar = CalendarPage(self.nb, self)
        self.nb.add(self.calendar, text="Calendar")

app = App()
app.mainloop()

import tkinter as tk
from tkcalendar import Calendar, DateEntry
import datetime
import time
import calendar
from PIL import Image, ImageTk
import database as db
from tkinter import messagebox 
from functools import partial

time1 = ''
my_date = datetime.date.today()
stall = db.stalls()

class ntufoods(tk.Tk):

    def __init__(self, *args, **kwargs):
        
        tk.Tk.__init__(self, *args, **kwargs)
        self.container = tk.Frame(self)
        self.container.pack(side="top", fill="both", expand = True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        self.today = datetime.date.today().weekday()
        self.selectedDay = datetime.date.today().weekday()
        
        self.title("NTUfoods")
        self.geometry("400x600")
        self.resizable(width=False, height=False)
        self.iconbitmap("images\\meal.ico")

        self.create_frame(HomePage)
 
        self.show_frame(HomePage)

    # show frame function to raise frame called
    def show_frame(self, cont): 
        frame = self.frames[cont]
        frame.tkraise()    
    # function to call frame class
    def create_frame(self, pagename):
        frame = pagename(self.container, self)
        self.frames[pagename] = frame
        frame.grid(row=0, column=0, sticky='nsew')
    def _on_press(self):
        self.configure(relief="sunken")

    def getwaitingtime(self, db, storename, count):#calculator function
        num_person = count.get()#get string from entrybox

        # try and except can be used as well
        # try: 
        #     num_person = int(num_person) #get rid of input with alphabets
        #     num_person = str(num_person)
        # except:
        #     messagebox.showinfo("", "Invalid info, try again")
        # else:
        #     if num_person.isdigit(): #get rid of underscore "1_2"
        #         num_person = int(num_person)
        #         if num_person > 0:
        #             waitingtime_person = stall.database[storename]["average waiting time"]
        #             total_waitingtime = num_person * waitingtime_person
        #             messagebox.showinfo("","estimated waiting time: " + str(total_waitingtime) + " min")
        #         else:
        #             messagebox.showinfo("", "Invalid info, try again")

        if num_person.isdigit():#exception where int(1_2) is read as 12
            num_person = int(num_person)
            if num_person > 0:
                waitingtime_person = stall.database[storename]["average waiting time"]
                total_waitingtime = num_person * waitingtime_person
                messagebox.showinfo("","estimated waiting time: " + str(total_waitingtime) + " min")
            else:
                messagebox.showinfo("", "Invalid info, try again")
        else:
            messagebox.showinfo("", "Invalid info, try again")
    

class HomePage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        def tick():#program's clock
            global time1
            time2 = time.strftime('%H:%M:%S')
            if time2 != time1:
                time1 = time2
                clock.config(text=time2)
            clock.after(200, tick)
        
        def viewtoday():#called when view today button is pressed
            canvas.destroy()
            
            mylist = time1.split(":")
            hour_now = mylist[0]#today's hour
            min_now = mylist[1]#today's minutes
            global today_time_new
            today_time_new = int(hour_now + min_now)#today's time used for comparison

            app.selectedDay = datetime.date.today().weekday()# 0 represents Monday, 6 represents Sunday

            app.create_frame(StallPage)        
            app.show_frame(StallPage)

        def viewotherdays():#called when view other days button is pressed
            canvas.destroy()
            app.create_frame(SelectDatePage)
            app.show_frame(SelectDatePage)    

        def viewoperatinghours():#called when view operating hours button is pressed
            canvas.destroy()
            app.create_frame(Operatinghourpage)
            app.show_frame(Operatinghourpage) 

        canvas = tk.Canvas(
                    self, 
                    width = 400, 
                    height = 600,
                    bg='black')
        canvas.pack()

        img = Image.open("images\\restaurant.jpg")
        newimgsize = (410,600)
        resizedImg = img.resize(newimgsize)
        self.backgroundimg = ImageTk.PhotoImage(resizedImg)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.backgroundimg)

        canvas.create_text(205, 150, font=("Courier", 20, "bold"), text='Welcome to NTUfoods!', fill="black")

        button = tk.Button(text="View Today's Stores", font=("Courier", 11), command=lambda: viewtoday())
        button.bind("<Button-1>", lambda e: app._on_press())
        button.bind("<ButtonRelease-1>")
        canvas.create_window(270, 480, window=button, height=43, width=266)

        button = tk.Button(text="View Stores By Other Dates", font=("Courier", 11), command=lambda: viewotherdays())
        button.bind("<Button-1>", lambda e: app._on_press())
        button.bind("<ButtonRelease-1>")
        canvas.create_window(270, 523, window=button, height=43, width=266)

        button = tk.Button(text="View Operating Hours", font=("Courier", 11), command=lambda: viewoperatinghours())
        button.bind("<Button-1>", lambda e: app._on_press())
        button.bind("<ButtonRelease-1>")
        canvas.create_window(270, 566, window=button, height=43, width=266)

        dayanddate = tk.Label(font=('times', 20, 'bold'), bg='papaya whip', text=str(datetime.date.today())+'\n'+calendar.day_name[my_date.weekday()])
        canvas.create_window(70, 494, window=dayanddate, height=86, width=133)
        clock = tk.Label(font=('times', 20, 'bold'), bg='papaya whip')
        canvas.create_window(70, 550, window=clock, height=50, width=133)

        tick()

class StallPage(tk.Frame):
 
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self,parent)
        def goback():
            canvas.destroy()
            app.create_frame(HomePage)
            app.show_frame(HomePage)
        def gostore(storepage):
            canvas.destroy()
            app.show_frame(storepage)   
 
        stallnames = {#to call the classes
                    "Cantonese roast duck store": Roastduckstore,
                    "Chicken rice store": Chickenricestore,
                    "Handmade Noodle Store": Handmadenoodlestore,
                    "Indian Cuisine Store": Indiancuisinestore,
                    "Mini Wok Store": Miniwokstore,
                    "Soup Delight Store": Soupdelightstore,
                    "Western Food Store": Westernfoodstore,
                    "Yong Tau Foo Store": Yongtaufoostore,
                    }
        openstalls = []
        count = 0
        ypos = 150
        canvas = tk.Canvas(
                    self, 
                    width = 400, 
                    height = 600,
                    bg='black')
        canvas.pack()
        img = Image.open("images\\restaurant.jpg")
        newimgsize = (410,600)
        resizedImg = img.resize(newimgsize)
        self.backgroundimg = ImageTk.PhotoImage(resizedImg)
        canvas.create_image(0, 0, anchor=tk.NW, image=self.backgroundimg)

        canvas.create_text(205, 50, font=("Purisa", 20), text='Choose a stall', fill="black")
        
        for i in stall.database:
                if app.selectedDay in stall.database[i]["date"] and stall.database[i]["opening time"] <= today_time_new <= stall.database[i]["closing time"]:#editedbycy
                    openstalls.append(i)  #Find open stalls based on time
        self.storeimg = {}                
        for x in openstalls:            
            app.create_frame(stallnames[x]) #instance of class is created
            img = Image.open(stall.database[x]['storeimg'])
            newimgsize = (150,150)
            resizedImg = img.resize(newimgsize)
            self.storeimg[x] = ImageTk.PhotoImage(resizedImg)
            button = tk.Button(text=x, command=partial(gostore,stallnames[x]), image=self.storeimg[x])
            button.bind("<Button-1>", lambda e: app._on_press())
            button.bind("<ButtonRelease-1>")
            if (count % 2) == 0:
                canvas.create_window(100, ypos, window=button, height=100, width=150)
                count +=1
                ypos += 50
            elif (count % 2) == 1:
                canvas.create_window(300, ypos, window=button, height=100, width=150)
                count += 1
                ypos += 50
           
        if openstalls == []:
            canvas.create_text(200, 300, font=("Purisa", 20), text='No stalls are open at this time \n Please try again at another time', fill="black")

        backbutton = tk.Button(self, text="Back", command=lambda: goback())
        backbutton.bind("<Button-1>", lambda e: app._on_press())
        backbutton.bind("<ButtonRelease-1>")
        canvas.create_window(200, 550, window=backbutton)

class SelectDatePage(tk.Frame):
 
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self,parent)
        label = tk.Label(self, text="Confirm a time and date", font=("Verdana",12))
        label.pack(pady=10,padx=10)
        today = datetime.date.today()
        def goback():
            app.create_frame(HomePage)
            app.show_frame(HomePage)
 
        # what to do after date and time confirmed.
        def confirmation():
            app.selectedDay = cal.selection_get().weekday()
            hour = int(var_hr.get())
            minute = var_min.get()            
            ampm = var_am_pm.get()
            if hour != 12 and ampm == 'PM':
                hour += 12
            elif hour == 12 and ampm == 'AM':
                hour = str(0)
            selected_time = int(str(hour) + minute)#edited by cy
            global today_time_new
            # creating stall page
            today_time_new = selected_time
            app.create_frame(StallPage) 
            app.show_frame(StallPage)

        mindate = today
        maxdate = today + datetime.timedelta(days=90)
 
        cal = Calendar(self, font="Arial 14", selectmode='day', locale='en_US',cursor="hand1")
        cal.pack(fill="both")
        
        # ADD clock dropdown here
        OPTIONS_HR = ["01","02","03","04","05","06","07","08","09","10","11","12"]
        OPTIONS_MIN = ["00","30"]
        OPTIONS_AM_PM = ["AM","PM"]
 
        var_min = tk.StringVar(self)
        var_min.set(OPTIONS_MIN[0]) # default value
 
        var_hr = tk.StringVar(self)
        var_hr.set(OPTIONS_HR[0]) # default value
 
        var_am_pm = tk.StringVar(self)
        var_am_pm.set(OPTIONS_AM_PM[0])
 
        opt = tk.OptionMenu(self, var_hr, *OPTIONS_HR)
        opt.place(rely=0.5, relx = 0.15, width = 80)
        opt1 = tk.OptionMenu(self, var_min, *OPTIONS_MIN)
        opt1.place(rely=0.5, relx = 0.415, width = 80)
        opt2 = tk.OptionMenu(self, var_am_pm, *OPTIONS_AM_PM)
        opt2.place(rely=0.5, relx = 0.67, width = 80)

        img = Image.open("images\\clock.PNG")
        newimgsize = (200,200)
        resizedImg = img.resize(newimgsize)
        self.clockimg = ImageTk.PhotoImage(resizedImg)
        panel = tk.Label(self, image = self.clockimg)
        panel.place(rely=0.6, relx= 0.23)
 
        confirm = tk.Button(self, text="Confirm", command=lambda: confirmation()).place(rely = 0.55, relx = 0.23, width = 100)
            
        backbutton = tk.Button(self, text="Back", command=lambda: goback()).place(rely = 0.55, relx = 0.5, width = 100)

class Operatinghourpage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self,parent)

        def goback():
            app.create_frame(HomePage)
            app.show_frame(HomePage)

        def get_openingdays(mylistofdaysopenforstore):
            templist = []
            daysopened = {
                0 : "Monday",
                1 : "Tuesday",
                2 : "Wednesday",
                3 : "Thursday",
                4 : "Friday",
                5 : "Saturday",
                6 : "Sunday",
            }
            for x in mylistofdaysopenforstore:
                templist.append(daysopened[x])
            return templist

        mylistofstalls = []
        mylistofopeninghours = []
        mylistofclosinghours = []
        mylistofdaysopen = []
        for x in stall.database:
            mylistofstalls.append(x)
            mylistofopeninghours.append(stall.database[x]["opening time"])
            mylistofclosinghours.append(stall.database[x]["closing time"])
            mylistofdaysopen.append(stall.database[x]["date"])

        label = tk.Label(self, text="Operatinghourpage", font=("Verdana",12))
        label.pack(pady=10,padx=10)
        counter = 0
        for x in mylistofstalls:
            label_stall = tk.Label(self, text = x).pack()#store name
            
            templist = get_openingdays(mylistofdaysopen[counter])#opening days for respective store
            str_openingdays = " ,".join(templist)
            label_openingdays = tk.Label(self, text = str_openingdays).pack()

            str_operatingtime = "operating hours: " + str(mylistofopeninghours[counter]) + " - " + str(mylistofclosinghours[counter])#stringoperation
            label_operatingtime = tk.Label(self, text = str_operatingtime).pack()
            counter += 1
        backbutton = tk.Button(self, text="Back", command=lambda: goback()).pack()

class Roastduckstore(tk.Frame):#1 

    def __init__(self, parent, controller): 
        tk.Frame.__init__(self,parent)

        def goback():
            app.create_frame(StallPage)
            app.show_frame(StallPage)
        
        canvas = tk.Canvas(
                    self, 
                    width = 400, 
                    height = 600,
                    bg= 'light yellow'
        )
        canvas.pack()

        img = Image.open("food button\\Cantonese Duck.jpg")
        newimgsize = (410,200)
        resizedImg = img.resize(newimgsize)
        self.backgroundimg = ImageTk.PhotoImage(resizedImg)

        canvas.create_text(205, 50, font=("Purisa", 20), text='Cantonese Roast Duck Store', fill="black")
        canvas.create_text(205, 100, font=("Purisa", 12), text=stall.database["Cantonese roast duck store"]["description"], fill="black")

        foodnames = []
        foodprices = []
        
        if today_time_new < stall.database["Cantonese roast duck store"]["breakfast end"]:
            stall.fooditems(self, stall.database, "Cantonese roast duck store", "breakfast_menu", foodnames)
            ypos = 150
            for foodname in foodnames:
                canvas.create_text(150, ypos, font=("Purisa", 10), text=foodname, fill="black")
                ypos += 20
            stall.foodprices(self, stall.database, "Cantonese roast duck store", "breakfast_menu", foodprices)
            ypos = 150
            for foodprice in foodprices:
                canvas.create_text(300, ypos, font=("Purisa", 10), text=foodprice, fill="black")
                ypos += 20
        else:
            stall.fooditems(self, stall.database, "Cantonese roast duck store", "menu", foodnames)
            ypos = 150
            for foodname in foodnames:
                canvas.create_text(150, ypos, font=("Purisa", 10), text=foodname, fill="black")
                ypos += 20
            stall.foodprices(self, stall.database, "Cantonese roast duck store", "menu", foodprices)
            ypos = 150
            for foodprice in foodprices:
                canvas.create_text(300, ypos, font=("Purisa", 10), text=foodprice, fill="black")
                ypos += 20  
        canvas.create_image(0, ypos+60, anchor=tk.NW, image=self.backgroundimg)    

        canvas.create_text(100, ypos+40, font=("Purisa", 10), text='Enter no. of pax queuing', fill="black")

        count = tk.Entry(self)
        canvas.create_window(250, ypos+40, window=count)

        btn_calculate = tk.Button(self, text = "Calculate", bg = "green", command=lambda: app.getwaitingtime(db, "Cantonese roast duck store", count))
        btn_calculate.bind("<Button-1>", lambda e: app._on_press())
        btn_calculate.bind("<ButtonRelease-1>")
        canvas.create_window(350, ypos+40, window=btn_calculate)

        backbutton = tk.Button(self, text="Back", command=lambda: goback())
        backbutton.bind("<Button-1>", lambda e: app._on_press())
        backbutton.bind("<ButtonRelease-1>")
        canvas.create_window(200, 550, window=backbutton) 

class Chickenricestore(tk.Frame):#2

    def __init__(self, parent, controller): 
        tk.Frame.__init__(self,parent)
        def goback():
            app.create_frame(StallPage)
            app.show_frame(StallPage)
        canvas = tk.Canvas(
                    self, 
                    width = 400, 
                    height = 600,
                    bg= 'light yellow'
        )
        canvas.pack()

        img = Image.open("images\\chicken rice.jpg")
        newimgsize = (410,200)
        resizedImg = img.resize(newimgsize)
        self.backgroundimg = ImageTk.PhotoImage(resizedImg)

        canvas.create_text(205, 50, font=("Purisa", 20), text='Chicken rice store', fill="black")
        canvas.create_text(205, 100, font=("Purisa", 12), text=stall.database["Chicken rice store"]["description"], fill="black")
        
        foodnames = []
        foodprices = []

        is_odd = app.selectedDay % 2
        
        if is_odd == 1:
            stall.fooditems(self, stall.database, "Chicken rice store", "menu_odd", foodnames)
            ypos = 150
            for foodname in foodnames:
                canvas.create_text(150, ypos, font=("Purisa", 10), text=foodname, fill="black")
                ypos += 20
            stall.foodprices(self, stall.database, "Chicken rice store", "menu_odd", foodprices)
            ypos = 150
            for foodprice in foodprices:
                canvas.create_text(300, ypos, font=("Purisa", 10), text=foodprice, fill="black")
                ypos += 20
        else:
            stall.fooditems(self, stall.database, "Chicken rice store", "menu_even", foodnames)
            ypos = 150
            for foodname in foodnames:
                canvas.create_text(150, ypos, font=("Purisa", 10), text=foodname, fill="black")
                ypos += 20
            stall.foodprices(self, stall.database, "Chicken rice store", "menu_even", foodprices)
            ypos = 150
            for foodprice in foodprices:
                canvas.create_text(300, ypos, font=("Purisa", 10), text=foodprice, fill="black")
                ypos += 20

        canvas.create_image(0, ypos+60, anchor=tk.NW, image=self.backgroundimg)
        
        canvas.create_text(100, ypos+40, font=("Purisa", 10), text='Enter no. of pax queuing', fill="black")

        count = tk.Entry(self)
        canvas.create_window(250, ypos+40, window=count)

        btn_calculate = tk.Button(self, text = "Calculate", bg = "green", command=lambda: app.getwaitingtime(db, "Chicken rice store", count))
        btn_calculate.bind("<Button-1>", lambda e: app._on_press())
        btn_calculate.bind("<ButtonRelease-1>")
        canvas.create_window(350, ypos+40, window=btn_calculate)
 
        backbutton = tk.Button(self, text="Back", command=lambda: goback())
        backbutton.bind("<Button-1>", lambda e: app._on_press())
        backbutton.bind("<ButtonRelease-1>")
        canvas.create_window(200, 550, window=backbutton) 

class Handmadenoodlestore(tk.Frame):#3
 
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self,parent)
        def goback():
            canvas.destroy()
            app.create_frame(StallPage)
            app.show_frame(StallPage)
        canvas = tk.Canvas(
                    self, 
                    width = 400, 
                    height = 600,
                    bg= 'light yellow'
        )
        canvas.pack()

        foodnames = []
        foodprices = []

        img = Image.open("images\\noodles.jpg")
        newimgsize = (410,200)
        resizedImg = img.resize(newimgsize)
        self.backgroundimg = ImageTk.PhotoImage(resizedImg)

        canvas.create_text(205, 50, font=("Purisa", 20), text='Handmade Noodle Store', fill="black")
        canvas.create_text(205, 100, font=("Purisa", 12), text=stall.database["Handmade Noodle Store"]["description"], fill="black")
        
        stall.fooditems(self, stall.database, "Handmade Noodle Store", "menu", foodnames)
        ypos = 150
        for foodname in foodnames:
            canvas.create_text(100, ypos, font=("Purisa", 10), text=foodname, fill="black")
            ypos += 20
            
        stall.foodprices(self, stall.database, "Handmade Noodle Store", "menu", foodprices)
        ypos = 150
        for foodprice in foodprices:
            canvas.create_text(300, ypos, font=("Purisa", 10), text=foodprice, fill="black")
            ypos += 20

        canvas.create_image(0, ypos+60, anchor=tk.NW, image=self.backgroundimg)

        canvas.create_text(100, ypos+15, font=("Purisa", 10), text='Enter no. of pax queuing', fill="black")

        count = tk.Entry(self)
        canvas.create_window(250, ypos+15, window=count)

        btn_calculate = tk.Button(self, text = "Calculate", bg = "green", command=lambda: app.getwaitingtime(db, "Handmade Noodle Store", count))
        btn_calculate.bind("<Button-1>", lambda e: app._on_press())
        btn_calculate.bind("<ButtonRelease-1>")
        canvas.create_window(350, ypos+15, window=btn_calculate)

        backbutton = tk.Button(self, text="Back", command=lambda: goback())
        backbutton.bind("<Button-1>", lambda e: app._on_press())
        backbutton.bind("<ButtonRelease-1>")
        canvas.create_window(200, ypos+80, window=backbutton) 

class Indiancuisinestore(tk.Frame):#4
 
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self,parent)
        def goback():
            canvas.destroy()
            app.create_frame(StallPage)
            app.show_frame(StallPage)
        canvas = tk.Canvas(
                    self, 
                    width = 400, 
                    height = 600,
                    bg= 'light yellow',
                    scrollregion=(0,0,0,650)
        )
        vbar=tk.Scrollbar(self,orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT,fill=tk.Y)
        vbar.config(command=canvas.yview)
        canvas.config(width=400,height=600)
        canvas.config(yscrollcommand=vbar.set)
        canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)

        foodnames = []
        foodprices = []

        img = Image.open("images\\indian cuisine.jpg")
        newimgsize = (410,200)
        resizedImg = img.resize(newimgsize)
        self.backgroundimg = ImageTk.PhotoImage(resizedImg)

        canvas.create_text(205, 50, font=("Purisa", 20), text='Indian Cuisine Store', fill="black")
        canvas.create_text(205, 100, font=("Purisa", 12), text=stall.database["Indian Cuisine Store"]["description"], fill="black")
        
        stall.fooditems(self, stall.database, "Indian Cuisine Store", "menu", foodnames)
        ypos = 150
        for foodname in foodnames:
            canvas.create_text(100, ypos, font=("Purisa", 10), text=foodname, fill="black")
            ypos += 20
            
        stall.foodprices(self, stall.database, "Indian Cuisine Store", "menu", foodprices)
        ypos = 150
        for foodprice in foodprices:
            canvas.create_text(300, ypos, font=("Purisa", 10), text=foodprice, fill="black")
            ypos += 20
        canvas.create_image(0, ypos+50, anchor=tk.NW, image=self.backgroundimg)

        canvas.create_text(100, ypos+20, font=("Purisa", 10), text='Enter no. of pax queuing', fill="black")

        count = tk.Entry(self)
        canvas.create_window(250, ypos+20, window=count)

        btn_calculate = tk.Button(self, text = "Calculate", bg = "green", command=lambda: app.getwaitingtime(db, "Indian Cuisine Store", count))
        btn_calculate.bind("<Button-1>", lambda e: app._on_press())
        btn_calculate.bind("<ButtonRelease-1>")
        canvas.create_window(350, ypos+20, window=btn_calculate)

        backbutton = tk.Button(self, text="Back", command=lambda: goback())
        backbutton.bind("<Button-1>", lambda e: app._on_press())
        backbutton.bind("<ButtonRelease-1>")
        canvas.create_window(200, ypos+70, window=backbutton) 

class Miniwokstore(tk.Frame):#5
 
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self,parent)
        def goback():
            canvas.destroy()
            app.create_frame(StallPage)
            app.show_frame(StallPage)
        canvas = tk.Canvas(
                    self, 
                    width = 400, 
                    height = 600,
                    bg= 'light yellow',
                    scrollregion=(0,0,0,700)
        )
        vbar=tk.Scrollbar(self,orient=tk.VERTICAL)
        vbar.pack(side=tk.RIGHT,fill=tk.Y)
        vbar.config(command=canvas.yview)
        canvas.config(width=400,height=600)
        canvas.config(yscrollcommand=vbar.set)
        canvas.pack(side=tk.LEFT,expand=True,fill=tk.BOTH)
        
        foodnames = []
        foodprices = []

        img = Image.open("images\\wok.jpg")
        newimgsize = (410,200)
        resizedImg = img.resize(newimgsize)
        self.backgroundimg = ImageTk.PhotoImage(resizedImg)

        canvas.create_text(205, 50, font=("Purisa", 20), text='Mini Wok Store', fill="black")
        canvas.create_text(205, 100, font=("Purisa", 12), text=stall.database["Mini Wok Store"]["description"], fill="black")
        
        stall.fooditems(self, stall.database, "Mini Wok Store", "menu", foodnames)
        ypos = 150
        for foodname in foodnames:
            canvas.create_text(100, ypos, font=("Purisa", 10), text=foodname, fill="black")
            ypos += 20
            
        stall.foodprices(self, stall.database, "Mini Wok Store", "menu", foodprices)
        ypos = 150
        for foodprice in foodprices:
            canvas.create_text(300, ypos, font=("Purisa", 10), text=foodprice, fill="black")
            ypos += 20

        canvas.create_text(100, ypos+40, font=("Purisa", 10), text='Enter no. of pax queuing', fill="black")
        canvas.create_image(0, ypos+60, anchor=tk.NW, image=self.backgroundimg)

        count = tk.Entry(self)
        canvas.create_window(250, ypos+40, window=count)

        btn_calculate = tk.Button(self, text = "Calculate", bg = "green", command=lambda: app.getwaitingtime(db, "Mini Wok Store", count))
        btn_calculate.bind("<Button-1>", lambda e: app._on_press())
        btn_calculate.bind("<ButtonRelease-1>")
        canvas.create_window(350, ypos+40, window=btn_calculate)

        backbutton = tk.Button(self, text="Back", command=lambda: goback())
        backbutton.bind("<Button-1>", lambda e: app._on_press())
        backbutton.bind("<ButtonRelease-1>")
        canvas.create_window(200, ypos+80, window=backbutton) 

class Soupdelightstore(tk.Frame):#6
 
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self,parent)
        def goback():
            canvas.destroy()
            app.create_frame(StallPage)
            app.show_frame(StallPage)
        canvas = tk.Canvas(
                    self, 
                    width = 400, 
                    height = 600,
                    bg= 'light yellow'
        )
        canvas.pack()
        foodnames = []
        foodprices = []

        img = Image.open("images\\soup.jpg")
        newimgsize = (410,200)
        resizedImg = img.resize(newimgsize)
        self.backgroundimg = ImageTk.PhotoImage(resizedImg)

        canvas.create_text(205, 50, font=("Purisa", 20), text='Soup Delight Store', fill="black")
        canvas.create_text(205, 100, font=("Purisa", 12), text=stall.database["Soup Delight Store"]["description"], fill="black")
        
        stall.fooditems(self, stall.database, "Soup Delight Store", "menu", foodnames)
        ypos = 150
        for foodname in foodnames:
            canvas.create_text(100, ypos, font=("Purisa", 10), text=foodname, fill="black")
            ypos += 20
            
        stall.foodprices(self, stall.database, "Soup Delight Store", "menu", foodprices)
        ypos = 150
        for foodprice in foodprices:
            canvas.create_text(300, ypos, font=("Purisa", 10), text=foodprice, fill="black")
            ypos += 20

        canvas.create_text(100, ypos+40, font=("Purisa", 10), text='Enter no. of pax queuing', fill="black")

        canvas.create_image(0, ypos+60, anchor=tk.NW, image=self.backgroundimg)

        count = tk.Entry(self)
        canvas.create_window(250, ypos+40, window=count)

        btn_calculate = tk.Button(self, text = "Calculate", bg = "green", command=lambda: app.getwaitingtime(db, "Soup Delight Store", count))
        btn_calculate.bind("<Button-1>", lambda e: app._on_press())
        btn_calculate.bind("<ButtonRelease-1>")
        canvas.create_window(350, ypos+40, window=btn_calculate)

        backbutton = tk.Button(self, text="Back", command=lambda: goback())
        backbutton.bind("<Button-1>", lambda e: app._on_press())
        backbutton.bind("<ButtonRelease-1>")
        canvas.create_window(200, ypos+80, window=backbutton) 
        
class Westernfoodstore(tk.Frame):#7
 
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self,parent)
        
        def goback():
            canvas.destroy()
            app.create_frame(StallPage)
            app.show_frame(StallPage)
        canvas = tk.Canvas(
                    self, 
                    width = 400, 
                    height = 600,
                    bg= 'light yellow',
                    )
        canvas.pack()
        
        foodnames = []
        foodprices = []

        img = Image.open("images\\western.jpg")
        newimgsize = (410,200)
        resizedImg = img.resize(newimgsize)
        self.backgroundimg = ImageTk.PhotoImage(resizedImg)

        canvas.create_text(205, 50, font=("Purisa", 20), text="Western Food Store", fill="black")
        canvas.create_text(205, 100, font=("Purisa", 12), text=stall.database["Western Food Store"]["description"], fill="black")
        
        stall.fooditems(self, stall.database, "Western Food Store", "menu", foodnames)
        ypos = 150
        for foodname in foodnames:
            canvas.create_text(100, ypos, font=("Purisa", 10), text=foodname, fill="black")
            ypos += 20
            
        stall.foodprices(self, stall.database, "Western Food Store", "menu", foodprices)
        ypos = 150
        for foodprice in foodprices:
            canvas.create_text(300, ypos, font=("Purisa", 10), text=foodprice, fill="black")
            ypos += 20
        
        canvas.create_text(100, ypos+40, font=("Purisa", 10), text='Enter no. of pax queuing', fill="black")
        canvas.create_image(0, ypos+60, anchor=tk.NW, image=self.backgroundimg)

        count = tk.Entry(self)
        canvas.create_window(250, ypos+40, window=count)

        btn_calculate = tk.Button(self, text = "Calculate", bg = "green", command=lambda: app.getwaitingtime(db, "Western Food Store", count))
        btn_calculate.bind("<Button-1>", lambda e: app._on_press())
        btn_calculate.bind("<ButtonRelease-1>")
        canvas.create_window(350, ypos+40, window=btn_calculate)
 
        backbutton = tk.Button(self, text="Back", command=lambda: goback())
        backbutton.bind("<Button-1>", lambda e: app._on_press())
        backbutton.bind("<ButtonRelease-1>")
        canvas.create_window(200, ypos+80, window=backbutton)  

class Yongtaufoostore(tk.Frame):#8
 
    def __init__(self, parent, controller): 
        tk.Frame.__init__(self,parent)
        def goback():
            canvas.destroy()
            app.create_frame(StallPage)
            app.show_frame(StallPage)
        
        canvas = tk.Canvas(
                    self, 
                    width = 400, 
                    height = 600,
                    bg= 'light yellow'
        )
        canvas.pack()
        foodnames = []
        foodprices = []

        img = Image.open("images\\food.jpg")
        newimgsize = (410,200)
        resizedImg = img.resize(newimgsize)
        self.backgroundimg = ImageTk.PhotoImage(resizedImg)

        canvas.create_text(205, 50, font=("Purisa", 20), text='Yong Tau Foo', fill="black")
        canvas.create_text(205, 100, font=("Purisa", 12), text=stall.database["Yong Tau Foo Store"]["description"], fill="black")
        
        stall.fooditems(self, stall.database, "Yong Tau Foo Store", "menu", foodnames)
        ypos = 150
        for foodname in foodnames:
            canvas.create_text(100, ypos, font=("Purisa", 10), text=foodname, fill="black")
            ypos += 20
            
        stall.foodprices(self, stall.database, "Yong Tau Foo Store", "menu", foodprices)
        ypos = 150
        for foodprice in foodprices:
            canvas.create_text(300, ypos, font=("Purisa", 10), text=foodprice, fill="black")
            ypos += 20

        canvas.create_text(100, ypos+40, font=("Purisa", 10), text='Enter no. of pax queuing', fill="black")
        canvas.create_image(0, ypos+60, anchor=tk.NW, image=self.backgroundimg)

        count = tk.Entry(self)
        canvas.create_window(250, ypos+40, window=count)

        btn_calculate = tk.Button(self, text = "Calculate", bg = "green", command=lambda: app.getwaitingtime(db, "Yong Tau Foo Store", count))
        btn_calculate.bind("<Button-1>", lambda e: app._on_press())
        btn_calculate.bind("<ButtonRelease-1>")
        canvas.create_window(350, ypos+40, window=btn_calculate)

        backbutton = tk.Button(self, text="Back", command=lambda: goback())
        backbutton.bind("<Button-1>", lambda e: app._on_press())
        backbutton.bind("<ButtonRelease-1>")
        canvas.create_window(200, 500, window=backbutton)    

app = ntufoods()
app.mainloop()
import tkinter as tk
import time
from playsound import playsound
from tkinter import messagebox

class App():
    def __init__(self):
        #set time 
        self.timeToShowTodo = '25:00'
        self.timeToShowRest = '05:00'
        self.basicTodoTimer = 25 * 60
        self.basicRestTimer = 5 * 60
        self.mainTimer = self.basicTodoTimer

        self.started = False
        self.todos = dict()
        self.reset = False
        self.restingFinished = False
        self.mainFont = '#f2f2f2' # super light gray
        self.back = '#F23535'
        self.secondFont = '#011526' # black
        self.thirdFont = '#F2505D' # red
        
        # root staff
        self.root = tk.Tk()
        self.root.title('pomodoro')
        self.root.geometry('600x700')
        self.root.configure(bg = self.mainFont)

        # scroll bar frame
        self.initScrollBar()
        
        # timer label, container for timer buttons,  buttons for timer 
        self.initTimerThings()
        
        # label for input, input task
        self.initInputTaskThings()

        # submit input btn
        self.initSubmitTask()
        
        # tasks
        self.initTasksContainer() 
        
        #  render
        self.frame.mainloop()

    
    def initScrollBar(self):
        self.canvas = tk.Canvas(self.root, borderwidth = 0, background = self.mainFont)
        self.frame = tk.Frame(self.canvas, background= self.mainFont)
        self.vsb = tk.Scrollbar(self.root, orient="vertical", command = self.canvas.yview)
        self.canvas.configure(yscrollcommand = self.vsb.set,
            highlightbackground = self.mainFont, bd = 0,
            highlightcolor = self.mainFont, highlightthickness = 0)
        
        
        self.vsb.pack(side = "right", fill = "y")
        self.canvas.pack(fill = 'y', expand = True)
        self.canvas.create_window((192,300), window = self.frame, anchor = 'center')
        
        self.frame.bind("<Configure>", lambda event, canvas = self.canvas: self.onFrameConfigure(canvas))

    def initTimerThings(self):
        # label for timer
        self.label = tk.Label(self.frame,text=self.timeToShowTodo)
        self.label.configure(font='helvetica 30 bold',fg = self.secondFont, bg = self.mainFont)
        self.label.pack(pady = (30,20))
        

        # container for timer buttons
        self.containerBtn = tk.Frame(self.frame,width = 300 , height = 100, bg = self.mainFont) 
        self.containerBtn.pack()

 
        # buttons for timer 
        self.startStopBtn = tk.Button(self.containerBtn, text = 'start', command = self.btnFunc)
        self.startStopBtn.configure( bg = self.thirdFont, fg = self.mainFont, 
            font = 'helvetica 13 bold',width = 7, bd = 0)
        self.startStopBtn.pack(pady = (14,30), padx = (30), side=tk.LEFT)
        self.resetBtn = tk.Button(self.containerBtn,text = 'reset' , command = self.manageResets)
        self.resetBtn.configure( bg = self.thirdFont, fg = self.mainFont, font='helvetica 13 bold',width = 7, bd = 0)
        self.resetBtn.pack(pady = (14,30),padx = (30), side=tk.RIGHT)
    
    def initInputTaskThings(self):
        # label for input
        self.inputLabel = tk.Label(self.frame,text= 'Write your task here',
            bd = 0, bg = self.mainFont,
            fg =self.secondFont, 
            font = 'helvetica 10 bold')

        self.inputLabel.pack(pady = (0,5))
        
        # input task
        self.input = tk.Entry(self.frame,width = 35,
            bd = 0, bg = self.mainFont, 
            highlightbackground = self.secondFont, highlightcolor = self.secondFont, 
            highlightthickness = 3)

        self.input.pack(pady = (10,15), ipady = 5)

        self.inputNumLabel = tk.Label(self.frame,text= 'Write number of pomodoros',
            bd = 0, bg = self.mainFont, fg = self.secondFont,
            font = 'helvetica 10 bold')

        self.inputNumLabel.pack(pady = (10,10))

        self.numberofPom = tk.Entry(self.frame,
            width = 5, bd = 0,bg = self.mainFont, highlightbackground = self.secondFont,
            highlightcolor = self.secondFont, highlightthickness= 3)

        self.numberofPom.pack(ipady = 5)

    def initSubmitTask(self):
        # submit input btn
        self.errorLabel = tk.Label(self.frame, text = '')

        self.submBtn = tk.Button(self.frame, text = 'add', command = self.submitInput)
        self.submBtn.configure(bg = self.thirdFont, fg = self.mainFont,
            font='helvetica 13 bold',width = 22, bd = 0)

        self.submBtn.pack(pady = (25,5))
        self.errorLabel.pack(pady= (2,10)) 


    def initTasksContainer(self):
        # label for tasks container
        self.labelForContainer = tk.Label(self.frame, text = 'Tasks To Do',
            bd = 0, bg = self.mainFont, 
            fg = self.secondFont , font = 'helvetica 14 bold')
        self.labelCompletedTasks = tk.Label(self.frame,text = 'Completed Tasks',
            bd = 0, bg = self.mainFont,
            fg = self.secondFont, font = 'helvetica 14 bold')
            
        # frame for tasks
        self.containerForAllTasks = tk.Frame(self.frame)
        self.containerForCompletedTasks = tk.Frame(self.frame)
        self.labelForContainer.pack()
        self.containerForAllTasks.pack(pady = (6,20))
        self.labelCompletedTasks.pack()
        self.containerForCompletedTasks.pack(pady = (10,40))

    
    def updateClock(self):
        if self.started ==  True:
            now = self.timerGet()
            self.startStopBtn.configure(text = 'stop')
            
            self.label.configure(text=now)

            if now == '00:00':

                # play system notification
                self.root.bell()

                if self.restingFinished == False:
                    self.deleteAsFull()

                self.resetBtnFoo()

                return 
            
            self.frame.after(1000, self.updateClock)
            self.mainTimer -=1
            
    def btnFunc(self):
        if self.started == False:
            self.started = True
            self.updateClock()
        else:
            self.stopPressed()
            self.started = False
        
    def timerGet(self):
        t = self.mainTimer
        mins, secs = divmod(t, 60) 
        timer = f'{mins:02d}:{secs:02d}'

        return timer

    def stopPressed(self):
        self.startStopBtn.configure(text = 'proceed')

    def submitInput(self):
        task = self.input.get()

        try:
            pomodoros =  int(self.numberofPom.get())
        except:
            self.errorLabel.configure(text = 'Write a number')
            tk.messagebox.showerror(title = 'pomodoro',message='Write number please')
            return
        
        if pomodoros == None or pomodoros == 0:
            pomodoros = 1

        if task in self.todos:
            self.errorLabel.configure(text = 'This task already exists')
            tk.messagebox.showerror(title = 'pomodoro',message='This task already exists')

            return
        
        self.errorLabel.configure(text = '')
        taskContainer = tk.Frame(self.containerForAllTasks, height = 100, width = 100,
        highlightbackground=self.secondFont, highlightthickness= 3)
        todo = tk.Label(taskContainer, text = f'{task}')
        todo.configure(font = 'helvetica 10 ', width = 20,
            pady = 1,justify = 'left', 
            bg = self.mainFont,  fg = self.secondFont)
            
        progress = tk.Label(taskContainer, text = f'0/{pomodoros}', 
            pady = 1, padx = 5, 
            font = 'helvetica 10 ', bg = self.mainFont,  fg = self.secondFont)
        deleteBtn = tk.Button(taskContainer, font = 'helvetica 10 ',  text = 'DEL', 
            command = lambda : self.deleteTodo(taskContainer,task),
            relief="solid", bd = 0, pady=3 ,  fg = self.mainFont, bg = self.thirdFont)
        
        todoObj = Todo(0,pomodoros,taskContainer,progress)

        self.todos[task] =  todoObj
    	
        taskContainer.pack(pady = 4)
        
        todo.pack(side=tk.LEFT)
        deleteBtn.pack(side = tk.RIGHT, padx = (1,0))
        progress.pack(side=tk.RIGHT)
        

        self.input.delete(0, 'end')
        self.numberofPom.delete(0, 'end')

    def deleteTodo(self,x,task):
        x.destroy()
        del self.todos[task]

    def deleteAsFull(self):
        i = 0
        for key in self.todos.keys():
            if i == 0:
                todo = self.todos[key]
                todo.currState = todo.currState + 1
                maxCount = todo.pomodoros
                ourCount = todo.currState
               
                if ourCount == maxCount:
                    taskContainer = tk.Frame(self.containerForCompletedTasks, height = 100, width = 100,  
                        highlightbackground=self.secondFont, highlightthickness= 3)
                    
                    completedTodo = tk.Label(taskContainer, text = f'{key}',font = 'helvetica 10 ', 
                        width = 25,pady = 3,justify = 'left', 
                        bg = self.mainFont,  fg = self.secondFont)
                    
                    progress = tk.Label(taskContainer, text = f'{todo.currState}/{todo.pomodoros}', pady = 3, padx = 5, 
                    font = 'helvetica 10 ', bg = self.mainFont,  fg = self.secondFont)
                    taskContainer.pack(pady = (7))
                    completedTodo.pack(side=tk.LEFT)
                    progress.pack(side=tk.RIGHT)
                    
                    self.deleteTodo(todo.taskContainer ,key)
                else:
                    label = todo.progress
                    label.configure(text = f'{todo.currState}/{todo.pomodoros}')
                    label.update()
    
            break

    def resetBtnFoo(self):
        if self.restingFinished == True:
            self.mainTimer = self.basicTodoTimer
            timeToShow = self.timeToShowTodo
            nameofStart = 'start'
            self.resetBtn.configure(text = 'reset')
            self.restingFinished = False

        else:
            self.mainTimer = self.basicRestTimer
            timeToShow =  self.timeToShowRest
            nameofStart = 'rest'
            self.resetBtn.configure(text = 'skip')
            self.restingFinished = True
        
        self.resetBtn.update()
            
        if self.started == True:
            self.stopPressed()
            self.started = False

        self.startStopBtn.configure(text = nameofStart)
        self.label.configure(text = timeToShow)
        self.label.update()
        self.startStopBtn.update()

    def resetClassic(self):
        self.mainTimer = self.basicTodoTimer
        timeToShow = self.timeToShowTodo
        nameofStart = 'start'
        
        self.resetBtn.configure(text = 'reset')
        self.resetBtn.update()

        if self.started == True:
            self.stopPressed()
            self.started = False

        self.startStopBtn.configure(text = nameofStart)
        self.label.configure(text = timeToShow)
        self.label.update()
        self.startStopBtn.update()

    def manageResets(self):
            a = self.resetBtn.config('text')[-1]
            if a == 'reset':
                self.resetClassic()
            else:
                self.resetBtnFoo()

    def onFrameConfigure(self,canvas):
        canvas.configure(scrollregion=canvas.bbox("all"))



class Todo:
    def __init__ (self, currState, pomodoros, taskContainer, progress):
        self.currState = currState
        self.pomodoros = pomodoros
        self.taskContainer = taskContainer
        self.progress = progress


app=App()
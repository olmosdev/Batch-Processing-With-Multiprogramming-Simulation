# Importing essential modules
import math
import time
import random
import threading
from io import open
from copy import copy
from tkinter import *
from tkinter import messagebox as MessageBox

# To center the window on the screen (This is a little Mixin)
class CenterWidgetMixin:
    def center(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int((ws/2) - (w/2))
        y = int((hs/2) - (h/2))
        self.geometry(f"{w}x{h}+{x}+{y}")  

# Generating the main screen
class MainWidow(Tk, CenterWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title("Program 2 - Batch Processing and Multiprogramming")
        self.resizable(0, 0) 
        self.geometry("640x480")
        self.config(relief="sunken", bd=10)
        self.center()
        self.Build()

    # Creating interfaces
    def Build(self):
        # To contain other widgets
        mainFrame = Frame(self)
        mainFrame.grid(row=0, column=0)

        # Input frame
        inputFrame = Frame(mainFrame)
        inputFrame.grid(row=0, column=0)
        inputFrame.config(padx=5, pady=5)

        processLabel = Label(inputFrame, text="# Process")
        processLabel.grid(row=0, column=0)
        processLabel.config(padx=5, pady=5)

        self.processEntry = Entry(inputFrame)
        self.processEntry.config(justify="center", width=11)
        self.processEntry.grid(row=0, column=1, padx=5, pady=5)

        self.processButton = Button(inputFrame, text="Generate", command=self.Generate)
        self.processButton.grid(row=0, column=2, padx=5, pady=5)

        # Space
        spaceFrame = Frame(mainFrame)
        spaceFrame.grid(row=0, column=1, padx=110)

        # Clock frame
        clockFrame = Frame(mainFrame)
        clockFrame.grid(row=0, column=2)

        clockLabel = Label(clockFrame, text="Global clock:")
        clockLabel.config(padx=5)
        clockLabel.grid(row=0, column=0)
    
        self.clockLabel2 = Label(clockFrame, text="00:00:00")
        self.clockLabel2.config(justify="center", width=10)
        self.clockLabel2.grid(row=0, column=1)

        # Work frame
        workFrame = Frame(mainFrame)
        workFrame.config(pady=15, padx=35)
        workFrame.grid(row=1, column=0, columnspan=3)

        # On hold frame
        onHolfFrame = Frame(workFrame)
        onHolfFrame.grid(row=0, column=0, padx=10)

        onHoldLabel = Label(onHolfFrame, text="On hold")
        onHoldLabel.config(justify="center")
        onHoldLabel.grid(row=0, column=0, columnspan=2, pady=3)

        self.onHoldText = Text(onHolfFrame)
        self.onHoldText.config(width=20, height=20)
        self.onHoldText.grid(row=1, column=0, columnspan=2, pady=3)

        onHoldLabel2 = Label(onHolfFrame, text="# of outstanding lots: ")
        onHoldLabel2.grid(row=2, column=0, pady=3)

        self.onHoldLabel3 = Label(onHolfFrame, text="00")
        self.onHoldLabel3.grid(row=2, column=1, pady=3)

        # Execution frame
        executionFrame = Frame(workFrame)
        executionFrame.grid(row=0, column=1, padx=10)

        executionLabel = Label(executionFrame, text="Execution")
        executionLabel.config(justify="center")
        executionLabel.grid(row=0, column=0, pady=2)

        self.executionText = Text(executionFrame)
        self.executionText.config(width=20, height=10)
        self.executionText.grid(row=1, column=0, pady=3)

        self.interruptButton = Button(executionFrame, text="Interrupt", command=self.ActivateInterrupt)
        self.interruptButton.grid(row=2, column=0, pady=5, sticky="ew")

        self.errorButton = Button(executionFrame, text="Error", command=self.ActivateError)
        self.errorButton.grid(row=3, column=0, pady=5, sticky="ew")

        # Finished frame
        finishedFrame = Frame(workFrame)
        finishedFrame.grid(row=0, column=2, padx=10)

        finishedLabel = Label(finishedFrame, text="Finished")
        finishedLabel.config(justify="center")
        finishedLabel.grid(row=0, column=0, pady=3)

        self.finishedText = Text(finishedFrame)
        self.finishedText.config(width=20, height=20)
        self.finishedText.grid(row=1, column=0, pady=3)

        self.finishedButton = Button(finishedFrame, text="Get results", command=self.SaveProcessResult)
        self.finishedButton.config(state=DISABLED)
        self.finishedButton.grid(row=2, column=0, sticky="nsew", pady=3)

    def ActivateInterrupt(self):
        self.interruptStatus = 1

    def ActivateError(self):
        self.errorStatus = 1

    def Generate(self):
        # Essential data to create processes
        self.batch = []
        self.listOfBatches = []
        self.resultOfBatches = []
        self.people = ["Celeste", "Marisol", "Carlos", "Diego", "Edgar"]
        self.operators = ["+", "-", "*", "/"]
        counter = 1
        batch = 1

        # Blocking the processEntry to protect the program
        self.processEntry.config(state=DISABLED)
        self.processButton.config(state=DISABLED)

        # Doing validations
        try:
            self.numberOfProcess = int(self.processEntry.get())
            if self.numberOfProcess <= 0:
                raise ValueError()
        except:
            MessageBox.showwarning("ERROR", "You must write a valid number.")
            self.processEntry.config(state=NORMAL)
            self.processButton.config(state=NORMAL)
            return

        # Generating processes
        for p in range(self.numberOfProcess):
            if counter > 5:
                batch += 1
                counter = 1
                self.listOfBatches.append(self.batch)
                self.batch = []

            process = {
                "BATCH": batch,
                "ID": p+1,
                "PROGRAMMER": self.people[random.randrange(0,5)],
                "OPERATION": str(random.randrange(1,11)) + " " + self.operators[random.randrange(0, 4)] + " " + str(random.randrange(1,11)),
                "TIME": random.randrange(4, 14),
                "INTERRUPTSTATE": False,
                "EXECUTEDTIME": 0,
                "TIMELEFT": 0
            }
            self.batch.append(process)

            counter += 1
        self.listOfBatches.append(self.batch)

        # Saving data
        with open("processes.txt", "w") as textFile:
            batches = set() # To handle batch separation
            for batch in self.listOfBatches:
                for p in batch:
                    if p["BATCH"] not in batches:
                        batches.add(p["BATCH"])
                        textFile.write("BATCH: " + str(p["BATCH"]) + "\n")

                    for key, value in p.items():
                        if (key != "BATCH") and (key != "INTERRUPTSTATE") and (key != "EXECUTEDTIME") and (key != "TIMELEFT"):
                            textFile.write(f"\t{key}: {value}\n")
                    textFile.write("\n")

        # Starting the timer (Creating thread of execution to work with parallel programming)
        initialTime = time.time()
        self.timerStatus = True
        self.threadingTimer = threading.Thread(target=self.Timer, args=(initialTime,))
        self.threadingTimer.start()

        self.copyOfListOfBatches = copy(self.listOfBatches) # To protect original processes data
        
        # Starting to work all the processes
        self.Processor()


    def Processor(self):
        # Extracting a batch from the batch list
        while len(self.copyOfListOfBatches) > 0:
            batch = self.copyOfListOfBatches.pop(0)

            while len(batch) > 0:
                # Deleting the last records
                self.executionText.config(state=NORMAL)
                self.executionText.delete(1.0, 'end')
                self.executionText.config(state=DISABLED)
                self.onHoldText.config(state=NORMAL)
                self.onHoldText.delete(1.0, 'end')
                self.onHoldText.config(state=DISABLED)

                # Extracting a process from the list of processes that belongs to the batch
                process = batch.pop(0)

                self.MonitorRunningBatches(process, batch)

        self.timerStatus = False

    # To count the time
    def Timer(self, initialTimePa): # This needs an initial time to get the difference (elpased time)
        while self.timerStatus:
            time.sleep(1)
            endTime = time.time()
            totalTime = round(endTime-initialTimePa, 0)
            
            self.clockLabel2["text"] = math.trunc(totalTime)
            self.clockLabel2.update()
        
        # Unlocking the program
        self.finishedButton.config(state=NORMAL)
    
    def MonitorBatchesOnHold(self, batchPa):
        # Taking information from a waiting process 
        if len(batchPa) > 0:
            waitingProcess = batchPa[0]
        else:
            try:
                # If there is nothing inside the current batch, extract the first process from the next batch
                waitingProcess = self.copyOfListOfBatches[0][0]
            except:
                # If it gives an error, it means that there is nothing else to check
                return

        # Extracting process information
        self.onHoldText.config(state=NORMAL)
        self.onHoldText.delete(1.0, 'end')

        processInformation = ""
        processInformation += "ID: " + str(waitingProcess["ID"]) + "\n"
        processInformation += "PROGRAMMER: " + waitingProcess["PROGRAMMER"] + "\n"
        processInformation += "OPERATION: " + str(waitingProcess["OPERATION"]) + "\n"
        # TIME refers to the Estimated Maximum Time (EMT or TME if we speak in Spanish)
        processInformation += "TIME: " + str(waitingProcess["TIME"]) + "\n"

        if waitingProcess["INTERRUPTSTATE"]:
            processInformation += "TIMELEFT: " + str(waitingProcess["TIMELEFT"]) + "\n"

        # To know how many batches after the current one are pending
        batchCounter = len(self.copyOfListOfBatches)

        # To know how many processes are pending based on the current batch
        if len(batchPa) == 0:
            processInformation += f"\n\n{len(self.copyOfListOfBatches[0]) - 1} pending processes"
            batchCounter = len(self.copyOfListOfBatches) - 1
        else:
            processInformation += f"\n\n{len(batchPa) - 1} pending processes"
            
        # Displaying the current process information
        self.onHoldText.insert('insert', processInformation)
        self.onHoldText.config(state=DISABLED)
        self.onHoldLabel3["text"] = str(batchCounter)
        self.onHoldLabel3.update()
        

    def MonitorRunningBatches(self, processPa, batchPa):
        self.MonitorBatchesOnHold(batchPa)
        self.interruptStatus = 0
        self.errorStatus = 0

        actualProcess = processPa # Taking the first process in the list

        # To know the execution time of the process
        if actualProcess["INTERRUPTSTATE"]:    
            executionTime = int(actualProcess["TIMELEFT"])
        else:
            executionTime = int(actualProcess["TIME"])
        
        # To solve the mathematical operation
        operation = actualProcess["OPERATION"]
        operationResult = eval(operation)
            
        # Updating the received process time
        for t in range(executionTime, 0, -1):
            self.executionText.config(state=NORMAL)
            self.executionText.delete(1.0, 'end')

            processInformation = ""
            processInformation += "ID: " + str(actualProcess["ID"]) + "\n"
            processInformation += "PROGRAMMER: " + actualProcess["PROGRAMMER"] + "\n"
            processInformation += "OPERATION: " + str(actualProcess["OPERATION"]) + "\n"
            processInformation += "TIME: " + str(actualProcess["TIME"]) + "\n"
            processInformation += "EXECUTEDTIME: " + str(actualProcess["EXECUTEDTIME"]) + "\n"
            processInformation += "TIMELEFT: " + str(t) + "\n"
            self.executionText.insert('insert', processInformation)
            self.executionText.update()
            self.executionText.config(state=DISABLED)

            if self.interruptStatus:
                # Changing some process attributes
                actualProcess["EXECUTEDTIME"] = actualProcess["TIME"] - t
                actualProcess["TIMELEFT"] = t
                actualProcess["INTERRUPTSTATE"] = True
                batchPa.append(actualProcess)
                self.interruptStatus = 0
                return
            elif self.errorStatus:
                actualProcess["OPERATION"] = f"{operation} = ERROR"
                self.resultOfBatches.append(actualProcess)
                self.MonitorExecutedBatches(actualProcess)
                self.errorStatus = 0
                return

            time.sleep(1)

        actualProcess["OPERATION"] = f"{operation} = {operationResult}"
        self.resultOfBatches.append(actualProcess)

        self.MonitorExecutedBatches(actualProcess)

    def MonitorExecutedBatches(self, processExecutedPa):
        processExecuted = processExecutedPa

        self.finishedText.config(state=NORMAL)
        self.finishedText.delete(1.0, 'end')

        processInformation = ""
        processInformation += "ID: " + str(processExecuted["ID"]) + "\n"
        processInformation += "PROGRAMMER: " + processExecuted["PROGRAMMER"] + "\n"
        processInformation += "OPERATION: " + str(processExecuted["OPERATION"]) + "\n"
        
        self.finishedText.insert('insert', processInformation)
        self.finishedText.config(state=DISABLED)

        # Deleting the last record
        self.executionText.config(state=NORMAL)
        self.executionText.delete(1.0, 'end')
        self.executionText.config(state=DISABLED)

    def SaveProcessResult(self):
        with open("processesResult.txt", "w") as textFile:
            batches = set() # To handle batch separation

            for p in self.resultOfBatches:
                if p["BATCH"] not in batches:
                    batches.add(p["BATCH"])
                    textFile.write("BATCH: " + str(p["BATCH"]) + "\n")

                for key, value in p.items():
                    if (key != "BATCH") and (key != "TIME") and (key != "INTERRUPTSTATE") and (key != "EXECUTEDTIME") and (key != "TIMELEFT"):
                        textFile.write(f"\t{key}: {value}\n")
                textFile.write("\n")
        MessageBox.showinfo("RESULTS", "The results have already been written.")

        # Cleaning screens unlocking program
        self.processEntry.config(state=NORMAL)
        self.processEntry.delete(0, END)
        self.finishedText.config(state=NORMAL)
        self.finishedText.delete(1.0, END)
        self.processButton.config(state=NORMAL)
        self.finishedButton.config(state=DISABLED)

if __name__ == "__main__":
    app = MainWidow()
    app.mainloop()

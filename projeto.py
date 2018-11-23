# -*-encoding:utf-8-*-
#imports
import copy
# imports

#variables
days = ["domingo","segunda","terça","quarta","quinta","sexta","sábado"]
validDays = [day for day in days if not day in ["domingo","sábado"]]
# variables

# classes
#decorator
def undo(func):
    def func_wrapper(*args,**kwargs):    
        args[0].stateHistory.push({"reference":args[0],"savedState":copy.deepcopy(args[0])})
        res = func(*args,**kwargs)
        return res
    return func_wrapper
#decorator

class calendar:
    def __init__(self,weekday="domingo",timeRange = 60):
        self.day = 1
        self.month = 1
        self.months = timeRange/30
        self.partialMonth = timeRange%30
        self.daysLeft = timeRange-1
        self.monthDays = range(timeRange)

    def currMonthWorkdays(self):
        if(abs(self.month-self.months)>=1):
            monthRange = range(self.month*30)
        else:
            monthRange = range(self.partialMonth)
        return [day for day in monthRange if days[day%7] in validDays]

    def currDay(self):
        return self.day

    def currWeekDay(self):
        return validDays[self.day%7]

    def isWorkDay(self):
        return days[self.currWeekDay()] in validDays

    def nextSDay(self):
        if(self.day==31):
            self.day=1
            self.month+=1
        else:
            self.day+=1

    def lastWorkDay(self):
        return self.currMonthWorkdays()[-1]

    def nextSFriday(self):
        currDay = self.day
        while(days[currDay%7]!="sexta"):
            currDay+=1
        return currDay

class payroll:
    def __init__(self,employees):
        self.employees = employees
        self.lastId = 0
        self.stateHistory = stateHistory()
        self.calendar = calendar()
        if(self.employees):
            for empl in self.employees:
                empl.stateHistory = self.stateHistory
    @undo
    def pay(self):
        paid = 0
        for emplo in self.employees:
            if(emplo.payday[0]==self.calendar.day):
                paid+=1
                emplo.pay()
        return {"paid":paid}

    @undo
    def add(self,name,address,kind,sallary):
        id = self.lastId+1
        self.lastId+=1
        newEmployee = employee(name,address,sallary,kind,self.calendar,self.stateHistory)
        return({"Added":newEmployee})

    @undo
    def remove(self,id):
        for emplo in self.employees:
            if(emplo.id == id):
                self.employees.remove(emplo)
                break
        return({"Removed":emplo})


    def undo(self):
        prev = self.stateHistory.pop()
        self.stateHistory.pushFuture({"reference":prev["reference"],"savedState":copy.deepcopy(prev["reference"])})
        if(prev["reference"] and isinstance(prev["savedState"],prev["reference"].__class__)):
            prev["reference"].__dict__ = prev["savedState"].__dict__
        prev["reference"].stateHistory = self.stateHistory

    def redo(self):        
        nextS = self.stateHistory.popFuture()
        self.stateHistory.push({"reference":nextS["reference"],"savedState":copy.deepcopy(nextS["reference"])})
        if(nextS["reference"] and isinstance(nextS["savedState"],nextS["reference"].__class__)):
            nextS["reference"].__dict__ = nextS["savedState"].__dict__
        nextS["reference"].stateHistory = self.stateHistory

class stateHistory:
    def __init__(self):
        self.past = []
        self.future = []

    def pop(self):
        if(len(self.past)):
            popped = self.past[-1]
            self.past = self.past[:-1]
        else:
            popped = None
        return popped

    def popFuture(self):
        if(len(self.future)):
            popped = self.future[-1]
            self.future = self.future[:-1]
        else:
            popped = None
        return popped

    def push(self,comm):
        self.past.append(comm)

    def pushFuture(self,comm):
        self.future.append(comm)

class employee:
    def __init__(self,name="",address="",id=0,sallary=0,kind="monthly",calendar=None,stateHistory = None,rate = 1,comissionRate = 0.2):
        self.name = name
        self.address = address
        self.id = id
        self.baseSallary = sallary
        self.kind = kind
        self.payday = 0
        self.lastPay = -1
        self.calendar = calendar
        self.stateHistory = stateHistory
        self.syndicate = False
        self.tax = 0
        if(kind=="monthly"):
            self.rate = rate
            self.payday = [self.calendar.lastWorkDay()]
            self.sallary = self.baseSallary*self.rate
        elif(kind=="comissioned"):
            self.rate = 0.5
            self.payday = [self.calendar.nextSFriday(),self.calendar.nextSFriday+14]
            self.sallary = self.baseSallary*self.rate
            self.comissionRate = comissionRate
        elif(kind=="hourly"):
            self.rate = 20/8 #20 dias úteis divididos por 8 horas = fração do salário ganho por hora
            self.payday = [day for day in self.calendar.currMonthWorkdays() if days[day%7] == "sexta"]
            self.sallary = 0

    def makeSyndicate(self,syndicate,tax = 0.1):
        self.syndicate = syndicate
        self.tax = tax
        syndicate.add(self)

    @undo
    def update(self,sallary,kind,comissioned,payday,syndicate):
        self.sallary = sallary
        self.kind = kind
        self.comissioned = comissioned
        self.payday = payday
        self.syndicate = syndicate
        return {"sallary":sallary,"kind":kind,"comissioned":comissioned,"payday":payday,"syndicated":syndicate}

    @undo
    def punchOut(self,hours):
        if(hours>8):
            self.sallary+=8*(self.baseSallary*self.rate)
            self.sallary+=(hours-8)*(self.baseSallary*(1.5*self.rate))

    @undo
    def addSale(self,sale):
        if(sale.keys() != ["valor","data"]):
            return None
        else:
            self.sallary+=sale["valor"]*self.comissionRate
            return sale
    @undo
    def pay(self):
        self.lastPay = self.calendar.currDay()
        if(self.syndicate):
            self.sallary-=self.tax

        if(self.kind=="monthly"):
            self.payday = []
            dev = {"paid":self.sallary,"day":self.lastPay,"month":self.calendar.month}
            self.sallary = self.baseSallary*self.rate
            return dev

        elif(self.kind=="comissioned"):
            if(len(self.payday)>1):
                self.lastPay=self.payday[0]
                self.payday = self.payday[1:]
            else:
                self.lastPay = self.payday[0]
                self.payday = []
            dev = {"paid":self.sallary,"day":self.lastPay,"month":self.calendar.month}
            self.sallary = self.baseSallary*self.rate
            return dev

        elif(self.kind == "hourly"):
            if(len(self.payday)>1):
                self.lastPay=self.payday[0]
                self.payday = self.payday[1:]
            else:
                self.lastPay = self.payday[0]
                self.payday = []
            dev = {"paid":self.sallary,"day":self.lastPay,"month":self.calendar.month}
            self.sallary = 0
            return dev
# classes

# functions

# functions

# main
def main():
    return None
# main

if __name__ == "__main__":
    main()

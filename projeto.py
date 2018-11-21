#imports
import copy
# imports

#variables
days = ["domingo","segunda","terça","quarta","quinta","sexta","sábado"]
validDays = [day for day in days if not day in ["domingo","sábado"]]
# variables
def time_all_class_methods(Cls):
    class NewCls(object):
        def __init__(self,*args,**kwargs):
            self.oInstance = Cls(*args,**kwargs)
        def __getattribute__(self,s):
            """
            this is called whenever any attribute of a NewCls object is accessed. This function first tries to
            get the attribute off NewCls. If it fails then it tries to fetch the attribute from self.oInstance (an
            instance of the decorated class). If it manages to fetch the attribute from self.oInstance, and
            the attribute is an instance method then `time_this` is applied.
            """
            try:
                x = super(NewCls,self).__getattribute__(s)
            except AttributeError:
                pass
            else:
                return x
            x = self.oInstance.__getattribute__(s)
            if type(x) == type(self.__init__): # it is an instance method
                print(copy.deepcopy(x))                 # this is equivalent of just decorating the method with time_this
            else:
                return x
    return NewCls
# classes
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

    def nextDay(self):
        if(self.day==31):
            self.day=1
            self.month+=1
        else:
            self.day+=1

    def lastWorkDay(self):
        return self.currMonthWorkdays()[-1]

    def nextFriday(self):
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

    def pay(self):
        for employee in self.employees:
            if(employee.payday[0]==self.calendar.day):
                employee.pay()

class stateHistory:
    def __init__(self):
        self.stack = []
        self.size = 0
    def pop(self):
        popped = self.stack[-1]
        self.stack = self.stack[:-1]
        return popped
    def push(self,comm):
        self.stack.append(comm)
@time_all_class_methods
class employee:
    def __init__(self,name="",address="",id=0,sallary=0,kind="monthly",comissioned = False,comissionShare=0.2,syndicated=False,serviceTax=0,calendar=None):
        self.name = name
        self.address = address
        self.id = id
        self.sallary = sallary
        self.comission = 0
        self.comissionShare = comissionShare
        self.kind = kind
        self.syndicated = syndicated
        self.serviceTax = serviceTax
        self.payday = 0
        self.lastPay = -1
        self.calendar = calendar
        if(kind=="monthly"):
            self.payday = [self.calendar.lastWorkDay()]
        elif(kind=="comissioned"):
            self.payday = [self.calendar.nextFriday(),self.calendar.nextFriday+14]
        elif(kind=="hourly"):
            self.payday = [day for day in self.calendar.currMonthWorkdays() if days[day%7] == "sexta"]

    def update(self,sallary,kind,comissioned,payday,syndicated):
        self.sallary = sallary
        self.kind = kind
        self.comissioned = comissioned
        self.payday = payday
        self.syndicated = syndicated
    def pay(self):
        self.lastPay = self.calendar.currDay()
        if(self.syndicated):
            self.sallary-=self.serviceTax

        if(self.kind=="monthly"):
            self.payday = []
            dev =  "pagos {} reais no dia {} do mês {}".format(self.sallary,self.lastPay,self.calendar.month)
            self.sallary = 0
            return dev

        elif(self.kind=="comissioned"):
            if(len(self.payday)>1):
                self.lastPay=self.payday[0]
                self.payday = self.payday[1:]
            else:
                self.lastPay = self.payday[0]
                self.payday = []
            dev =  "pagos {} reais no dia {} do mês {}".format(self.sallary/2,self.lastPay,self.calendar.month)
            return dev

        elif(self.kind == "hourly"):
            if(len(self.payday)>1):
                self.lastPay=self.payday[0]
                self.payday = self.payday[1:]
            else:
                self.lastPay = self.payday[0]
                self.payday = []
            dev =  "pagos {} reais no dia {} do mês {}".format(self.sallary,self.lastPay,self.calendar.month)
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

#-*- encoding: utf-8 -*-
#imports
import engine
#imports

#variables
mainMenu = '''
 _______   ______    __       __    __       ___          _______   _______                        
|   ____| /  __  \\  |  |     |  |  |  |     /   \\        |       \\ |   ____|                       
|  |__   |  |  |  | |  |     |  |__|  |    /  ^  \\       |  .--.  ||  |__                          
|   __|  |  |  |  | |  |     |   __   |   /  /_\\  \\      |  |  |  ||   __|                         
|  |     |  `--'  | |  `----.|  |  |  |  /  _____  \\     |  '--'  ||  |____                        
|__|      \\______/  |_______||__|  |__| /__/     \\__\\    |_______/ |_______|                       
                                                                                                   
.______      ___       _______      ___      .___  ___.  _______ .__   __. .___________.  ______   
|   _  \\    /   \\     /  _____|    /   \\     |   \\/   | |   ____||  \\ |  | |           | /  __  \\  
|  |_)  |  /  ^  \\   |  |  __     /  ^  \\    |  \\  /  | |  |__   |   \\|  | `---|  |----`|  |  |  | 
|   ___/  /  /_\\  \\  |  | |_ |   /  /_\\  \\   |  |\\/|  | |   __|  |  . `  |     |  |     |  |  |  | 
|  |     /  _____  \\ |  |__| |  /  _____  \\  |  |  |  | |  |____ |  |\\   |     |  |     |  `--'  | 
| _|    /__/     \\__\\ \\______| /__/     \\__\\ |__|  |__| |_______||__| \\__|     |__|      \\______/ 

Bem vindo! O que deseja fazer hoje?(0-10)
0.  Adicionar um empregado
1.  Remover um empregado
2.  Lancar um resultado de venda
3.  Lancar um cartao de ponto
4.  Lancar uma taxa de servico
5.  Alterar detalhes de um empregado
6.  Rodar a folha de pagamento para hoje
7.  Desfazer
8.  Refazer
9.  Rodar folhas de pagamento no intervalo
E.  Sair
'''
#variables

#classes

#classes

#functions
def showPayroll(payroll):
    for e in payroll.employees:
        for i in e.__dict__:
            print("{}\t = \t{}".format(i,e.__dict__[i]))
        print("\n")

def parseInput(text,iType):
    text = text.split(",")
    if(iType == "empregado"):
        if(len(text)==4):
            try:
                int(text[3])
            except:
                return None
            res = text
        else:
            return None
    elif(iType == "id"):
        if(len(text)==1):
            try:
                int(text[0])
            except:
                return None
            res = [int(text[0])]
    elif(iType == "salesCard"):
        if(len(text)==3):
            try:
                int(text[0])
                int(text[1])
            except:
                return None
            res = (text[0],{"valor":text[0],"data":text[1]})
    elif(iType == "tax"):
        if(len(text)==2):
            try:
                float(text[0])
                int(text[1])
            except:
                return None
            res = text
    return res
#functions

#main
def main():
    payroll = engine.payroll()
    syndicate = engine.syndicate()
    currCode = "0"
    Output = ""
    print(mainMenu)
    while(currCode.lower() != "e"):
        print(mainMenu)
        currCode = input(Output)
        if(currCode == "0"):
            new =  parseInput(input("Informe nome, endereco, tipo(mensal,comissao,hora), salario base(O valor que seria recebido se o tipo do empregado cumprir com o tempo requerido dele.) separados por virgula: "),"empregado")
            if(new):
                payroll.add(new[0],new[1],new[2],int(new[3]))
                print("{} recebeu o id {}".format(payroll.employees[-1].name,payroll.employees[-1].id))
            else:
                print("Entrada inválida, tente novamente")
        elif(currCode == "1"):
            rem = parseInput(input("Informe o id do funcionário a ser removido: "),"id")
            if(rem):
                payroll.remove(*rem)
            else:
                print("Entrada inválida, tente novamente.")
        elif(currCode == "2"):
            rem = parseInput(input("Informe o id do empregado, o valor sem sifrao e a data da venda, separados por virgula: "),"salesCard")
            if(rem):
                emplo = payroll.find(rem[0])
                if(emplo):
                    if(emplo.kind == "comissao"):
                        emplo.addSale(rem[1])
                    else:
                        print("Empregado nao comissionado.")
                else:
                    print("Empregado nao encontrado")
            else:
                print("Entrada invalida")
        elif(currCode == "3"):
            rem = parseInput(input("Informe o id do funcionario para bater o ponto: "),"id")
            if(rem):
                emplo = payroll.find(rem[0])
                if(emplo):
                    if(emplo.kind == "hora"):
                        time = input("Informe quantas horas foram trabalhadas hoje: ")
                        emplo.punchOut(time)
                    else:
                        print("Funcionario nao e horista")
                else:
                    print("Funcionario nao encontrado")
            else:
                print("Entrada invalida")
        elif(currCode == "4"):
            rem = parseInput(input("Informe a nova taxa do sindicado"),"tax")
            if(rem):
                syndicate.applyTax(float(rem[0]),int(rem[1]))
        elif(currCode == "5"):
            rem = parseInput(input("Informe o id do funcionario a ser atualizado"),"id")
            if(rem):
                emplo = payroll.find(rem[0])
                if(emplo):
                    new = input("Nesta ordem, separados por vírgulas, informe os campos a serem atualizados, se for para manter o mesmo, ponha -1 no lugar:\nsalario,tipo,dia do pagamento,se faz parte do sindicato(s/n)")
                    res = emplo.update(*new.split(","))
                    if(res["syndicated"]):
                        syndicate.add(emplo)
                else:
                    print("Empregado nao encontrado")
            else:
                print("Entrada invalida")
        elif(currCode == "6"):
            payroll.pay()
        elif(currCode == "7"):
            payroll.undo()
        elif(currCode == "8"):
            payroll.redo()
        elif(currCode == "9"):
            intervalo = input("Informe quantos dias devem ser contemplados pelo programa, ele rodará de hoje até o dia informado.")
        input("Aperte enter para continuar.")
    return None
#main

if __name__=="__main__":
    main()

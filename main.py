import random
from datetime import datetime, timedelta

class Bank:
    __accountsCounter=0
    __customerDatabase=[]
    def createAccount(customerDetails):
        if Bank.__is_existing(customerDetails):
            return False
        else:
            return Bank.__put_data(customerDetails,Bank.__accountNumberGeneration())
    def get_data():
        return Bank.__customerDatabase
    def update_balance(accountNumber,accountHolderName,amount):
        for accountData in Bank.__customerDatabase:
            if accountNumber==accountData['accountNumber'] and accountHolderName==accountData['accountHolder']:
                accountData['accountBalance']+=amount
                return True
        return False
    def __put_data(customerDetails,accountNumber):
        Bank.__customerDatabase.append({"accountNumber":accountNumber,
                                        "accountHolder":customerDetails['customerName'],
                                        "mobileNumber":customerDetails['mobileNumber'],
                                        "aadharNumber":customerDetails['aadharNumber'],
                                        "panCardNumber":customerDetails['panCardNumber'],
                                        "accountBalance":0})
        return {"accountNumber":accountNumber,
                "accountHolder":customerDetails['customerName'],
                "mobileNumber":customerDetails['mobileNumber']}
    def __accountNumberGeneration():
        Bank.__accountsCounter+=1
        accountNumber= "SBI"+str(Bank.__accountsCounter).zfill(12)
        return accountNumber
    def __is_existing(customerDetails):
        for customer in Bank.__customerDatabase:
            if customer['panCardNumber']==customerDetails['panCardNumber'] and customer['aadharNumber']==customerDetails['aadharNumber']:
                return True
        return False

class Rupay:
    __rupayDatabase=[]
    __issuedDebitCards=[] # Only store debit cards
    # def get_debit_cards():
    #     print(Rupay.__issuedDebitCards)
    def generateDebitCard(accountData):
        is_found=False
        for rupayData in Rupay.__rupayDatabase:
            if accountData['accountNumber']==rupayData['accountNumber']:
                is_found=True
                break
        if is_found:
            for debitCard in Rupay.__rupayDatabase:
                if debitCard['accountNumber']==accountData['accountNumber']:
                    return "Debit card "+str(debitCard['debitCardNumber'])+ " already exists for the account number "+accountData['accountNumber']
        else:
            while True:
                debitCardNumber=random.randint(100000000001,999999999999)
                if debitCardNumber not in Rupay.__issuedDebitCards:
                    # BankOperations.cash_withdrawl(bankOperation,accountData["accountNumber"],accountData["accountHolder"],500)
                    Rupay.__issuedDebitCards.append(debitCardNumber)
                    time=datetime.now()+timedelta(days=1095)
                    expiry=(str(time.month)+"/"+str(time.year)[2::])
                    rupayData={ "accountNumber":accountData['accountNumber'],
                                "accountHolderName":accountData['accountHolder'],
                                "mobileNumber":accountData['mobileNumber'],
                                "debitCardNumber":debitCardNumber,
                                "cvv_Number":random.randint(101,999),
                                "Expiry":expiry}
                    Rupay.__rupayDatabase.append(rupayData)
                    Bank.update_balance(accountData["accountNumber"],accountData["accountHolder"],-500)
                    print("debit card created and returned")
                    return {"debitCardNumber":debitCardNumber,
                            "cvv_Number":rupayData['cvv_Number'],
                            "Expiry":rupayData["Expiry"]}
           
class Customer:
    def __init__(self):
        self.customerName=input("Enter your name: ")
        self.mobileNumber=int(input("Enter your Mobile number : "))
        self.motherName=input("Enter Mother name: ")
        self.fatherName=input("Enter Father name: ")
        self.aadharNumber=int(input("Enter Aadhar: "))
        self.panCardNumber=input("Enter your Pan card number: ")
    def get_data(self):
        return {
            "customerName":self.customerName,
            "mobileNumber":self.mobileNumber,
            "motherName":self.motherName,
            "fatherName":self.fatherName,
            "aadharNumber":self.aadharNumber,
            "panCardNumber":self.panCardNumber
        }

class BankOperations:
    def account_creation(self,customerDetails):
        createStatus = Bank.createAccount(customerDetails)
        if createStatus == False:
            print("Account already Exists ")
        else:
            print("Your passBook: ",createStatus)
            wantDebitCard=input("Do you want debit card(y/n): ").lower()
            if wantDebitCard=="y":
                print("you need to deposit minimum ₹500 to get debit card")
                print("******* deposit ********")
                accountNumber=input("Enter account number: ")
                accountHolderName=input("Enter account holder name: ")
                amount=int(input("Enter amount: "))
                if self.deposit(accountNumber,accountHolderName,amount):
                    print(f"{amount} deposited into your account") # Account verified and deposited amount
                    if self.check_balance(accountNumber)>=500:
                        print("your debit card",self.issue_debit_card(accountNumber))
                    else:
                        print("Insufficient Balance to get debit card! Try to deposit minimum Amount of ₹500")
                else:
                    print("Account details miss-matched")
    def cash_withdrawl(self,accountNumber,accountHolderName,amount):
        for accountData in Bank.get_data():
            if accountData['accountNumber']==accountNumber and accountData['accountHolder']==accountHolderName: 
                if accountData['accountBalance']>=amount:
                    Bank.update_balance(accountNumber,accountHolderName,-amount)
                    return f"{amount} Withdrawn from your account"
                else:
                    return False
        else:
            return None
    def deposit(self,accountNumber,accountHolderName,amount):
        return Bank.update_balance(accountNumber,accountHolderName,amount)
    def check_balance(self,accountNumber):
        for accountData in Bank.get_data():
            if (accountData['accountNumber']==accountNumber):
                return accountData['accountBalance']
        else:
            return None
    def transfer_money(self,senderAccountNumber,senderAccountHolderName,receiverAccountNumber,receiverAccountHolderName,amount):
        count=0
        for accountData in Bank.get_data():
            if ((senderAccountNumber==accountData['accountNumber'] and senderAccountHolderName==accountData['accountHolder']) or 
            (receiverAccountNumber==accountData['accountNumber'] and receiverAccountHolderName==accountData['accountHolder'])):
                count+=1
                if count == 2:
                    senderBalance = self.check_balance(senderAccountNumber)
                    if senderBalance >= amount:
                        Bank.update_balance(senderAccountNumber,senderAccountHolderName,-amount)
                        Bank.update_balance(receiverAccountNumber,receiverAccountHolderName,amount)
                        print(f"{amount} transferred to {receiverAccountNumber}")
                    else:
                        print("Low balance in sender's account")
                    return None
        else:
            print("Account details miss-matched")
    def issue_debit_card(self,accountNumber):
        for accountData in Bank.get_data():
            if (accountData['accountNumber']==accountNumber):
                return Rupay.generateDebitCard(accountData)

operation=BankOperations()
while True:
    # print('''\t1.Offline (Visiting Bank)
        # 2.Online (Through Phone Pay)''')
    print('''\t1.Create account
        2.cash withdrawl
        3.Deposit
        4.check balance
        5.Transfer money
        6.Get debit card
        7.Exit''')

    option=int(input("Enter an option: "))
    match(option):
        case 1:
            print("******* Account Creation ******")
            operation.account_creation(Customer().get_data())
        case 2:
            print("******** cash withdrawl ********")
            accountNumber=input("Enter your account number: ")
            accountHolderName=input("Enter Account Holder name: ")
            amount=int(input("Enter Amount to withdraw: "))
            result=operation.cash_withdrawl(accountNumber,accountHolderName,amount)
            if result==None:
                print("Account details Miss-matched, try entering details again")
            elif result==False:
                print("Low balance !")
            else:
                print(result)
        case 3:
            print("******** Deposit *********")
            accountNumber=input("Enter your account number: ")
            accountHolderName=input("Enter Account Holder name: ")
            amount=int(input("Enter Amount to deposit: "))
            print(f"{amount} deposited into your account" if operation.deposit(accountNumber,accountHolderName,amount) else "Account details miss-matched, Try entering the valid details")
        case 4:
            print("******* check balance ********")
            accountNumber=input("Enter your Account number: ")
            result=operation.check_balance(accountNumber)
            if result==None:
                print("No Account Found !")
            else:
                print("Your balance is:",result)
        case 5:
            print("********* Transfer money *********")
            senderAccountNumber=input("Enter sender account number: ")
            senderAccountHolderName=input("Enter sender account holder name: ")
            receiverAccountNumber=input("Enter receiver account number: ")
            receiverAccountHolderName=input("Enter receiver account holder name: ")
            amount=int(input("Enter amount to transfer: "))
            operation.transfer_money(senderAccountNumber,senderAccountHolderName,receiverAccountNumber,receiverAccountHolderName,amount)
        case 6:
            print("********* Get debit card **********")
            accountNumber=input("Enter Account Number: ")
            result=operation.check_balance(accountNumber)
            if result==None:
                print("No Account Found !")
            elif result>=500:
                res=operation.issue_debit_card(accountNumber)
                if isinstance(res,dict):
                    # print("your debit card",operation.issue_debit_card(accountNumber))
                    print("your debit card",res)
                else:
                    print(res)
            else:
                print(f'Your balance is {result}')
                print("Your minimum balance must be ₹500 to get debit card")
        case 7:
            print("Exited")
            # print(Bank.get_data())
            break
        # case __:
        #     Rupay.get_debit_cards()
            print("Invalid option please select options from below")
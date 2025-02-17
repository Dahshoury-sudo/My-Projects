import random

class Bankaccount:
    number_of_customers = 0
    def __init__(self,name,initial_amount = 0):
        self.initial_amount = initial_amount
        self.name = name
        self.card_number = random.randint(100000000000000,999999999999999)
        self.balance = initial_amount
        Bankaccount.number_of_customers += 1
        



    def deposit(self):
        amount = int(input(f"{self.name}, How Much Money Do u want to deposit: "))
        self.amount_to_add = amount
        self.balance += self.amount_to_add
        print("Transaction Completed ✅ ✅ ")





    def withdraw(self):
        amount = int(input(f"{self.name}, How Much Money Do u want to withdraw: "))
        self.amount_to_withdraw = amount
        if amount > self.balance:
            print("Transaction Failed ❌ ❌ ")
            print(f"{self.name}, Sorry You Don't Have Enough Cash To Withdraw.. Your Balance is {self.balance}")

        else:
            print("Transaction Completed ✅ ✅ ")
            self.balance -= amount



    
    def transfer(self,to):
        amount = int(input(f"How much ? : "))
        if amount > self.balance:
            print("Transaction Failed ❌ ❌ ")
            print(f"{self.name}, Sorry You Don't Have Enough Cash To Withdraw.. Your Balance is {self.balance}")   
        else:

            self.balance -= amount
            to.balance += amount



    def validate(self):
        name = input("Who Do u want to transfer money to ? : ").capitalize()
        pass


        

    def get_balance(self):
        print(f"{self.name}, Your Balance Is: {self.balance:,}")


class InterestRewardAcct(Bankaccount):
    def __init__(self,name,initial_amount):
        super().__init__(name)
        self.balance = initial_amount * 1.05




Mohamed = Bankaccount("Mohamed",1500)
Nada = Bankaccount("Nada",1200)
Ahmed = Bankaccount("Ahmed",1000)
Fouad = InterestRewardAcct("Fouad",234000)

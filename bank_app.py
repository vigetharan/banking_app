#importing datetime for get date and time for transaction history
from datetime import datetime

#create a Text file as users.txt for keeping Default Username and password
try:
    with open('users.txt','x') as file:
        file.write('Admin::user:admin,pass:1234\n')
except FileExistsError:
    pass

#create a Text file as defaults.txt for keeping upcoming Customer Id and Account Number
try:
    with open('defaults.txt','x') as file:
        file.write('C0001,100001')
except FileExistsError:
    pass

#function for a welcome note
def welcome():
    print(f'{'=*'*27}\nWELCOME TO ABCD BANK\n{'=*'*27}')

# function for getting a file into dictioanary
def getFileAsDic(file):
    dic={}
    with open(file,'r') as file:
        for line in file:
            key,value= line.strip().split('::')
            sub_dic={}
            for item in value.split(','):
                sub_key,sub_value =item.split(':') 
                sub_dic[sub_key]=sub_value
            dic[key] = sub_dic
        return dic

# function for getting a dictioanary into a file 
def writeDicToFile(dic,to_file):
    data=""
    for key,value in dic.items():
        sub_data=""
        for i,(subkey, subvalue) in enumerate(value.items()):
            if i>0:
                sub_data +=','
            sub_data += f'{subkey}:{subvalue}'
        data +=f'{key}::{sub_data}\n'
    with open(to_file,'w') as file:
        file.write(data)

# for Get a valid amount
def get_amount(type):
    if type == 'Initial':
        note='To open an account enter the Amount for initial deposit : '
    elif type == "Withdraw":
        note = 'Enter the amount to Withdraw : '
    elif type == 'Deposit':
        note = 'Enter the amount to Deposit : '
    while True:
        try:
            amount = float(input(print(note)))
            if amount>0: return f'{amount}'  
            else:
                print('The amount must be greater than zero...!')
                continue
        except ValueError:
            print("Amount must be in digits only")

def get_acc_no_as_input():
    accounts=getFileAsDic('accounts.txt')
    while True:
        try:
            acc_num = input("Please Enter account number for get balance : ")
            for key in accounts:
                if key == acc_num:
                    return acc_num
            print('Account number not available\nContact bank for get an account number...\n')
        except ValueError:
            print('Account number must be numbers and contains only 6 Digits.\n')
            continue

# function for Deposit
def deposit(customer_id, deposit_type='Deposit'):
    date_time=datetime.today().replace(microsecond=0)
    if deposit_type == 'Initial_Deposit':
        with open('defaults.txt','r+') as file:
            default =file.readline().split(',')
            account_no =int(default[1])
        new_balance = amount = get_amount('Initial')
        with open('accounts.txt','a') as file:
            file.write(f'{account_no}::cus_id:{customer_id},balance:{amount}\n')
    elif deposit_type == 'Deposit':
        customers = getFileAsDic('customers.txt')
        account_no = customers[customer_id]['accountNo']
        amount = get_amount('Deposit')
        accounts = getFileAsDic('accounts.txt')
        accounts[account_no]['balance'] = float(accounts[account_no]['balance']) + amount
        writeDicToFile(accounts,'accounts.txt')
    with open('transactions.txt','a') as file:
            file.write(f'{date_time}::cus_id:{customer_id},acc_no:{account_no},type:{deposit_type},amount:{amount},balance:{new_balance}\n')
#function for ger customer information
def get_customer():
    customer_details={}
    while True:
        name = input("Enter new Customer's name : ")
        if not name.isalpha():
            print("name must be in letters only... please re enter")
            continue
        else:
            customer_details['Name']=name
            break
    while True:
        try:
            age = int(input("Enter new Customer's Age : "))
            if int(age) <18 or int(age)>100:
                print('Age must between 18 t0 100...\nPlease ReEnter age.')
                continue
            else:
                customer_details['Age']=age
                break
        except ValueError: 
            print('age must be a number...!\n Please ReEnter Correct age')
        continue
    address = input("Enter new Customer's address : ")
    customer_details['Address'] = address
    username = input("Enter new Customer's username : ")
    password = input(f"Enter password for username of {username}: ")
    return customer_details, username, password

# function for create a customer
def create_customer():
    with open('defaults.txt','r+') as file:
        default=file.readline().split(',')
        customer_id = default[0]
        account_no =int(default[1])
    custome_details,username,password =get_customer()
    toWriteDetails={customer_id:custome_details}
    toWriteDetails[customer_id]['Account_no'] = account_no
    writeDicToFile(toWriteDetails,'customers.txt')
    print(f'Customer with customer id:- {customer_id} created successfully....!!!\n')
    with open('users.txt','a') as file:
        file.write(f'{customer_id}::user:{username},pass:{password}\n')
        deposit(customer_id, 'Initial_Deposit')
    print('Account opened successfully...!!!\n')
#write to file upcoming account number and customer id for next creation
    next_account_no = account_no +1
    num_partOf_customer_id = int(customer_id[1:])
    next_customer_id = (f'C{(num_partOf_customer_id + 1):04}')
    with open('defaults.txt','w') as file:
        file.write(f'{next_customer_id},{next_account_no}')

#FUNCTION FOR WITHDRAWAL
def withdrawal(customer_id):
    date_time=datetime.today().replace(microsecond=0)
    customers = getFileAsDic('customers.txt')
    account_no = customers[customer_id]['accountNo']
    print('withdraw success')
    amount = get_amount('Withdraw')
    accounts = getFileAsDic('accounts.txt')
    if account_no in accounts.keys:
        accounts[account_no]['balance'] += amount
        new_balance = accounts[account_no]['balance']
        writeDicToFile(accounts,'accounts.txt')
        with open('transactions.txt','a') as file:
            file.write(f'{date_time}::cus_id:{customer_id},acc_no:{account_no},type:Withdrawal,amount:{amount},balance:{new_balance}\n')
    else:
        print("account number not found\nPlease Retry with a correct one")
#fUNCTION FOR BALANCE CHECK
def check_balance(accountNo):
    a=getFileAsDic('accounts.txt')
    for key in a:
        if key == accountNo:
            balance = float(a[key]['balance'])
    print(f'Current Account balance of {accountNo} is : {balance:,.2f}')
#getting Account Transaction history   
def get_transaction_history_by_acc_no(account_no):
    print(f"{'*'*36}\nTRANSACTION HISTORY OF {account_no}\n{'*'*36}")
    print(f"date\t\t\ttype of transaction\t\tamount\t\tbalance\n{'='*50}")
    transactions=getFileAsDic('transactions.txt')
    str=""
    for key,value in transactions.items():
            if int(value['acc_no']) == account_no:
                print(f'{key}\t{transactions[key]['type']},\t\t\t,{transactions[key]['amount']},\t\t,{transactions[key]['balance']}\n')

def get_transaction_history_by_date(date):
    print(f"TRANSACTION HISTORY OF {date}\n{'*'*25}")
    print("Account No.\t\t\ttype of transaction\t\tamount\t\tbalance")
    transactions=getFileAsDic('transactions.txt')
    str =""
    for key in transactions:
        if key.startswith(date):
            str += (f'{transactions[key]['acc_no']}\t\t\t{transactions[key]['amount']}\t\t{transactions[key]['balance']}\n')
        print(f'{key}\t{str}')


def change_pw(c_id,username):
    users=getFileAsDic('users.txt')
    for key in users:
        if key == c_id:
            username=users[c_id]['user']
    new_pw = input(f"Enter new password for username of({username}) :")
    users[c_id]['pass'] = new_pw
    writeDicToFile(users,'users.txt')
    print('Password changed successfully.!\nPlease login again :')
    main_menu()             #after password change, call main_menu() for relogin

#MENU FOR PROCESS AS ADMIN, if admin logged in successful.
def admin_menu():
    while True:
        print('WELCOME TO ABCD BANK as an ADMIN...!!!!')
        print('1. create a customer')
        print('2. create an account')
        print("3. view a customer's details")
        print('4. check transaction history of a account')
        print("5. view an account's balance")
        print("6. change admin's password")
        print("7. change a user's password")
        print('8. Logout')
        print('9. Exit')
        try:
            choice=int(input('As a admin please chose a choice'))
            if choice in [1,2,3,4,5,6,7,8]:
                return choice
            elif choice ==9:
                exit()
            else:
                print('invalid choice....!\nPlease choose a correct one between 1-9')
                continue
        except ValueError:
            print('Invalid input please enter a valid number between 1-9')
            continue
#MENU FOR PROCESS AS USER, if user logged in successful.
def user_menu():
   while True:
        print('WELCOME TO ABCD BANK as an USER...!!!!')
        print('1. Check Balance of an account/')
        print('2. Deposit to your account.')
        print('3. Withdrawal from your account.')
        print('4. Transaction History of your account.')
        print('5. change your login password.')
        print('6. Logout.')
        print('7. Exit.')
        try:
            choice=int(input('As a admin please chose a choice'))
            if choice in [1,2,3,4,5,6]:
                return choice
            elif choice ==7:
                    exit()
            else:
                print('invalid choice....!\nPlease choose a correct one between 1-9')
                continue
        except ValueError:
            print('Invalid input please enter a valid number between 1-9')
            continue
# Main menu for execution of main program.
def main_menu():
    username=input('Enter your username : ').strip()
    password=input('Enter your password  : ').strip()
    users=getFileAsDic('users.txt')
    for key in users:
        if username == users[key]['user']:
            customer_id = key               
            if username=='admin' and password == users[key]['pass']:
                print('login as admin successfully:')
                while True:
                    select = admin_menu()
                    if select ==1:      create_customer()
                    elif select ==2:    create_account(customer_id)
                    elif select ==3:    get_transaction_history_by_date(input('Enter date for get transaction history : '))
                    elif select ==4:    get_transaction_history_by_acc_no(get_acc_no_as_input())
                    elif select ==5:    check_balance(get_acc_no_as_input())
                    elif select ==6:    change_pw(customer_id,username)
                    elif select ==7:    change_pw(input("Enter the USER's Customer ID for change password : "))
                    elif select ==8:    main_menu()
                    elif select ==9:    exit()
            elif password==users[key]['pass']:
                print('Welcome as user!!!')
                select = user_menu()
                if select ==1:
                    check_balance()
                    break
                elif select ==2:
                    deposit(customer_id, 'Deposit')
                elif select ==3:
                    withdrawal(customer_id)
                elif select ==4:
                    get_transaction_history()
                elif select ==5:
                    print()
                    change_pw(customer_id,username)
                elif select ==6:
                    main_menu()
                    break
            else:
                print('Password is incorrect.! Please retry...!')
    else:
        print('Access Denied...!\nUsername not exists...\n Contact admin for register username and password!')

welcome()           
main_menu()

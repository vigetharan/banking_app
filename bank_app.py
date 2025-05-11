#importing datetime for get date and time for transaction history.
from datetime import datetime

import getpass
#create a Text file as users.txt for keeping Default Username and password
try:
    with open('users.txt','x') as file:
        file.write('Admin::user:admin,pass:1234\n')
except FileExistsError:
    pass

#create a Text file as defaults.txt for keeping upcoming Customer Id and Account Number.......
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
    elif type == "Transfer":
        note = 'Enter the amount for Transfer : '
    while True:
        try:
            amount = float(input(note))
            if amount>0: return amount
            else:
                print('The amount must be greater than zero...!')
                continue
        except ValueError:
            print("Amount must be in digits only")
#check account number available in accounts details
def get_acc_no_as_input():
    accounts=getFileAsDic('accounts.txt')
    while True:
        try:
            acc_num = input("Please Enter account number : ")
            for key in accounts:
                if key == acc_num:
                    return acc_num
            print('Account number not available\nEnter the correct one OR Contact bank for create an account...\n')
        except ValueError:
            print('Account number must be numbers and contains only 6 Digits.\n')
            continue

# function for Deposit
def deposit(customer_id, deposit_type):
    try:
        date_time=datetime.today().replace(microsecond=0)
        if deposit_type == 'Initial_Deposit':
            with open('defaults.txt','r+') as file:
                default =file.readline().split(',')
                account_no =int(default[1])
            new_balance = amount = get_amount('Initial')
            with open('accounts.txt','a') as file:
                file.write(f'{account_no}::cus_id:{customer_id},balance:{amount}\n')
            print(f"Initial deposit of {amount:,.2f} is depositted to your account successfully...!\nCurrent BALANCE is :{new_balance:,.2f} ")
        elif deposit_type == 'Deposit':
            try:
                customers = getFileAsDic('customers.txt')
                account_no = customers[customer_id]['Account_no']
                amount = get_amount('Deposit')
                accounts = getFileAsDic('accounts.txt')
                accounts[account_no]['balance'] = float(accounts[account_no]['balance']) + amount
                new_balance =  accounts[account_no]['balance']
                writeDicToFile(accounts,'accounts.txt')
            except KeyError:
                print("Sorry 😒 Deposit was not successful...!")
                pass
        with open('transactions.txt','a') as file:
            file.write(f'{date_time}::cus_id:{customer_id},acc_no:{account_no},type:{deposit_type},amount:{amount},balance:{new_balance}\n')
            print(f'Your {deposit_type} of {amount:,.2f} is depositted to your account successfully...!\nCurrent BALANCE is :{new_balance:,.2f} ')
    except UnboundLocalError:
        print(f"\t{'X'*45}\n\t\tCustomer id is invalid, please retry again\n")
        pass
# For get age, DOB, sex from NIC Number
def get_Nic():
    mon=[31,29,31,30,31,30,31,31,30,31,30,31]
    while True:
        nic_no=input("nic no").strip()
        if(len(nic_no)==12):
            year = int(nic_no[:4])
            day_part = int(nic_no[4:7])
        elif len(nic_no)==10:
            day_part = int(nic_no[2:5])
            if int(nic_no[:2])>10:
                year = int('19'+nic_no[:2]) # for born before 2000, not works for born before year of 1910
            else:   year = int('20'+nic_no[:2]) #for born after 2000
        else:
            print("Invalid NIC number...!💔\tNIC must be (12 digits)/(9 digits with an letter)\nPlease Re-enter correct number.\n")
            continue
        age = int(datetime.now().year)-int(year)
        if day_part<366:
            days=day_part
            sex = "MALE"
            break
        elif (day_part-500)<366:
            days=day_part-500
            sex = "FEMALE"
            break
        else:
            print('🤢NIC Number you entered is not valid....\n Please Re-Enter your correct NIC Number.')
    #checking for get day and month with [month]
    sum=0
    for i in range (12):
        sum=sum+mon[i]
        if sum>days:
            month = i+1
            b_day = days-sum+(mon[i])
            break
        elif sum == days:
            month = i+1
            b_day = (mon[i])
            break
        i=i+1
    details=[nic_no,sex,age,year,month,b_day]
    return details

#function for ger customer information
def get_customer():
    customer_details={}
    while True:
        name = input("Enter new Customer's name : ")
        if not name.isalpha():
            print("NAME must be in letters only... please re enter")
            continue
        else:
            break
    nic_details=get_Nic()
    nic_no = nic_details[0]
    sex = nic_details[1]    
    age = nic_details[2]    
    dob = f'{nic_details[3]}-{nic_details[4]}-{nic_details[5]}'
    address = input("Enter new Customer's address : ")
    username = input("Enter new Customer's username : ")
    password = input(f"Enter password for username of {username}: ")
    customer_details =[name, address, nic_no, age, sex, dob, username, password]
    return customer_details

# function for create a customer
def create_customer():
    with open('defaults.txt','r+') as file:
        default=file.readline().split(',')
        customer_id = default[0]
        account_no =int(default[1])
    details=get_customer()
    with open('customers.txt','a') as file:
        file.write(f"{customer_id}::Name:{details[0]},Address:{details[1]},NIC:{details[2]},Age:{details[3]},sex:{details[4]},dob:{details[5]},Account_no:{account_no}\n")
    print(f'Customer with customer id:- {customer_id} created successfully....!!!\n')
    with open('users.txt','a') as file:
        file.write(f'{customer_id}::user:{details[6]},pass:{details[7]}\n')
        deposit(customer_id, 'Initial_Deposit')
    print('Account opened successfully...!!!\nInitial Deposit Done....!!!\n')
#write to file next account number and customer id for next creation
    next_account_no = account_no +1
    num_partOf_customer_id = int(customer_id[1:])
    next_customer_id = (f'C{(num_partOf_customer_id + 1):04}')
    with open('defaults.txt','w') as file:
        file.write(f'{next_customer_id},{next_account_no}')

#FUNCTION FOR WITHDRAWAL
def withdrawal(customer_id):
    accounts = getFileAsDic('accounts.txt')
    date_time=datetime.today().replace(microsecond=0)
    customers = getFileAsDic('customers.txt')
    account_no = customers[customer_id]['Account_no']
    while True:
        amount = get_amount('Withdraw')
        if amount > float(accounts[account_no]['balance']):
            print('Amount must be lower than account balance...\nPlease re-Try..\n')
            continue
        else: break
    accounts[account_no]['balance'] = float(accounts[account_no]['balance']) - amount
    new_balance = accounts[account_no]['balance']
    writeDicToFile(accounts,'accounts.txt')
    with open('transactions.txt','a') as file:
        file.write(f'{date_time}::cus_id:{customer_id},acc_no:{account_no},type:Withdrawal,amount:{amount},balance:{new_balance}\n')
    print(f'Withdraw of {amount:,.2f} from your account is succcessful !!!\n')

#fUNCTION FOR BALANCE CHECK
def check_balance(accountNo):
    accounts=getFileAsDic('accounts.txt')
    for key in accounts:
        if int(key) == int(accountNo):
            balance = float(accounts[key]['balance'])
    print(f'Current Account balance of {accountNo} is : {balance:,.2f}')
#getting Account Transaction history   
def get_transaction_history_by_acc_no(account_no):
    print(f"{'*'*36}\nTRANSACTION HISTORY OF {account_no}\n{'*'*36}")
    print(f"{'date':<25}{'type of transaction':<25}{'amount':>20}{'balance':>20}\n{'='*50}")
    transactions=getFileAsDic('transactions.txt')
    for key,value in transactions.items():
        if str(value['acc_no']) == str(account_no):
            print(f"{key:<25}{value['type']:<25}{float(value['amount']):>20,.2f}{float(value['balance']):>20,.2f}\n")


def get_transaction_history_by_date(date):
    print(f"TRANSACTION HISTORY FOR {date}\n{'*'*81}")
    print(f"{'Account No.':<15}{'type of transaction':<25}{'amount':>20}{'balance':>20}")
    transactions=getFileAsDic('transactions.txt')
    found = True
    for key in transactions:
        if key.startswith(date):
            print(f"{transactions[key]['acc_no']:<15}{transactions[key]['type']:<25}{float(transactions[key]['amount']):>20,.2f}{float(transactions[key]['balance']):>20,.2f}\n")
    # if not found:
    #     print("No transactions found in given date.\n")
#function for inter bank account transfers
def transfer_between_accounts(customer_id):
    date_time=datetime.today().replace(microsecond=0)
    accounts = getFileAsDic('accounts.txt')
    customers = getFileAsDic('customers.txt')
    print("Transfer Money to another account\n")
    to_Acc = get_acc_no_as_input()
    print("To Transfer Money to another account\n")
    account_no = customers[customer_id]['Account_no']
    while True:
        amount = get_amount("Transfer")
        if amount > float(accounts[account_no]['balance']):
            print('Amount must be lower than account balance...\nPlease re-Try..\n')
            continue
        else: break
    if account_no in accounts:
        accounts[account_no]['balance'] = float(accounts[account_no]['balance']) - amount
        new_balance = accounts[account_no]['balance']
        writeDicToFile(accounts,'accounts.txt')
        with open('transactions.txt','a') as file:
            file.write(f'{date_time}::cus_id:{customer_id},acc_no:{account_no},type:Transfer Debit,amount:{amount},balance:{new_balance}\n')
        print(f'Transfer of {amount:,.2f} from your account is succcessful !!!\n')
    accounts[to_Acc]['balance'] = float(accounts[to_Acc]['balance']) + amount
    new_balance =  accounts[to_Acc]['balance']
    writeDicToFile(accounts,'accounts.txt')
    date_time1=datetime.today().replace(microsecond=0)
    with open('transactions.txt','a') as file:
        file.write(f'{date_time1}::cus_id:{customer_id},acc_no:{to_Acc},type:Transfer credit,amount:{amount},balance:{new_balance}\n')

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
        print(f"WELCOME TO ABCD BANK as an ADMIN...!!!!\n{'=-'*63}")
        print('\t\t1. create a customer')
        print('\t\t2. Deposit to an account')
        print("\t\t3. view a customer's details")
        print('\t\t4. check transaction history of a account')
        print('\t\t5. check transaction history by a date.')
        print("\t\t6. view an account's balance")
        print("\t\t7. change admin's password")
        print("\t\t8. change a user's password")
        print('\t\t9. Logout')
        print('\t\t0. Exit\n')
        try:
            choice=int(input('As a admin please chose a choice'))
            if choice in [1,2,3,4,5,6,7,8,9]:
                return choice
            elif choice ==0:
                exit()
            else:
                print('invalid choice....!\nPlease choose a correct one between 1-9')
                continue
        except ValueError:
            print('Invalid input please enter a valid number between 1-9\n')
            continue
#MENU FOR PROCESS AS USER, if user logged in successful.
def user_menu():
   while True:
        print(f"WELCOME TO ABCD BANK AS AN USER...!!!!\n{'=-'*63}")
        print('\t\t1. Check Balance of an account')
        print('\t\t2. Deposit to your account.')
        print('\t\t3. Withdrawal from your account.')
        print('\t\t4. To Transfer money to Another Account.')
        print('\t\t5. Transaction History of your account.')
        print('\t\t6. change your login password.')
        print('\t\t7. Logout.')
        print('\t\t8. Exit.\n')
        try:
            choice=int(input('As a user please chose a choice'))
            if choice in [1,2,3,4,5,6,7]:
                return choice
            elif choice ==8:
                exit()
            else:
                print('invalid choice....!\nPlease choose a correct one between 1-9')
                continue
        except ValueError:
            print('Invalid input please enter a valid number between 1-9')
            continue
#function for get account no from user
def get_acc_no(customer_id):
    customers=getFileAsDic('customers.txt')
    account_num = customers[customer_id]['Account_no']
    return int(account_num)

# Main menu for execution of main program.
def main_menu():
    username=input('Enter your username : ').strip()
    password=getpass.getpass('Password, you typing is not display, please type password and HIT ENTER KEY!!!\nEnter your password  : ').strip()
    print("PASSWORD Entered......!\n")
    users=getFileAsDic('users.txt')
    for key in users:
        if username == users[key]['user']:
            customer_id = key               
            if username=='admin' and password == users[key]['pass']:
                print('logged in as admin successfully.....!!!!')
                while True:
                    select = admin_menu()
                    if select ==1:      create_customer()
                    elif select ==2:    deposit(input("Enter Customer's ID for Details : "), "Deposit")
                    elif select ==3:    view_customer_details(input("Enter Customer's ID for Details : " ))
                    elif select ==4:    get_transaction_history_by_acc_no(get_acc_no_as_input())
                    elif select ==5:    get_transaction_history_by_date(input("Please Enter date for transaction history as YYYY-MM-DD"))
                    elif select ==6:    check_balance(get_acc_no_as_input())
                    elif select ==7:    change_pw(customer_id,username)
                    elif select ==8:    change_pw(input("Enter the USER's Customer ID for change password : "))
                    elif select ==9:    main_menu()
            elif password==users[key]['pass']:
                print('logged in as admin successfully....!!!!')
                while True:
                    select = user_menu()
                    if select ==1:      check_balance(int(get_acc_no(customer_id)))
                    elif select ==2:    deposit(customer_id, 'Deposit')
                    elif select ==3:    withdrawal(customer_id)
                    elif select ==4:    transfer_between_accounts(customer_id)
                    elif select ==5:    get_transaction_history_by_acc_no(get_acc_no(customer_id))
                    elif select ==6:    change_pw(customer_id,username)
                    elif select ==7:
                        main_menu()
                        break
            else:
                print('Password is incorrect.! Please retry...!')
                main_menu()
    else:
        print('Access Denied...!\nUsername not exists...\n Contact admin for register username and password!')

welcome()           
main_menu()

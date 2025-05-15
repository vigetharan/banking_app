from datetime import datetime                   #importing datetime for get date and time for transaction history.
import getpass
import os                                         
#create a Text file as users.txt for keeping Default Username and password
try:
    with open('users.txt','x') as file:
        file.write('Admin::user:admin,pass:1234\n')
except FileExistsError:
    pass

try:                                            #create a Text file as defaults.txt for keeping upcoming Customer Id and Account Number.......
    with open('defaults.txt','x') as file:
        file.write('C0001,100001')
except FileExistsError:
    pass

def welcome():                                                   #function for a welcome note
    note = f"\033[1m{'WELCOME TO ABCD BANK'}\033[0m"                                         
    print(f"{'=*'*63}\n\t\t\t\t{note}\n{'=*'*63}")

def getFileAsDic(file):                                 # function for getting a text file into a dictioanary
    dic={}
    try:
        with open(file,'r') as file:
            for line in file:
                key,value= line.strip().split('::')
                sub_dic={}
                for item in value.split(','):
                    sub_key,sub_value =item.split(':') 
                    sub_dic[sub_key]=sub_value
                dic[key] = sub_dic
            return dic
    except FileNotFoundError:
        print("✖️✖️✖️file not created yet, First create a customer with an account and TRY again....!")
        pass
 
def writeDicToFile(dic,to_file):                        # function for getting a dictioanary into a file
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

def get_amount(type):                                       # for Get a valid amount
    while type:
        if type == 'Initial':       note='To open an account enter the Amount for initial deposit : '
        elif type == "Withdraw":    note = 'Enter the amount to Withdraw : '
        elif type == 'Deposit':     note = 'Enter the amount to Deposit : '
        elif type == "Transfer":    note = 'Enter the amount for Transfer : '
        while True:
            try:
                amount = float(input(note))
                if amount>0: return amount
                else:
                    print('The amount must be greater than zero...!')
                    continue
            except ValueError:
                print("Amount must be in digits only")
                continue

def get_acc_no(customer_id):                            #function for get account by customer id
    customers=getFileAsDic('customers.txt')
    account_num = customers[customer_id]['Account_no']
    return int(account_num)

def get_acc_no_as_input():
    try:                              #check account number available in accounts details
        accounts=getFileAsDic('accounts.txt')
        while True:
            try:
                acc_num = input("Please Enter account number : ")
                for key in accounts:
                    if key == acc_num:
                        return acc_num
                print('\tAccount number is not available or not valid\nEnter the correct one OR Contact bank for create an account...\n')
            except (KeyError, ValueError):
                print('Account number must be numbers and contains only 6 Digits.\n')
                continue
    except (FileNotFoundError, TypeError):
        print("Account number you entered is not created yet....!")

# function for Deposit by passing account number or customer id.
def deposit(number, deposit_type):
    try:
        date_time=datetime.today().replace(microsecond=0)
        if deposit_type == 'Initial_Deposit':
            customer_id = number
            with open('defaults.txt','r+') as file:                 #take last used account number for new creation
                default =file.readline().split(',')
                account_no =int(default[1])
            new_balance = amount = get_amount('Initial')
            with open('accounts.txt','a') as file:
                file.write(f'{account_no}::cus_id:{number},balance:{amount}\n')
        elif deposit_type == 'Deposit':
            if number.upper().startswith('C'):
                customers = getFileAsDic('customers.txt')
                customer_id = number
                account_no = customers[customer_id]['Account_no']
            else:
                account_no = number
                accounts=getFileAsDic('accounts.txt') 
                customer_id = accounts[account_no]['cus_id']              
            amount = get_amount('Deposit')
            accounts = getFileAsDic('accounts.txt')
            accounts[account_no]['balance'] = float(accounts[account_no]['balance']) + amount
            new_balance =  accounts[account_no]['balance']
            writeDicToFile(accounts,'accounts.txt')
        with open('transactions.txt','a') as file:
            file.write(f'{date_time}::cus_id:{customer_id},acc_no:{account_no},type:{deposit_type},amount:{amount},balance:{new_balance}\n')
        print(f'Your {deposit_type} of {amount:,.2f} is depositted to your account successfully...!\n\tCurrent BALANCE is \t:{new_balance:,.2f}\n')
    except (UnboundLocalError,KeyError, FileNotFoundError):
        print(f"\t❌❌❌\tCustomer id or Account Number is invalid or not registered, please RE-Try again or contact bank for further details\n\t\t{'X'*45}\n")
        pass

def withdrawal(customer_id):                                #FUNCTION FOR WITHDRAWAL
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
    print(f'Withdraw of {amount:,.2f} from your account is succcessful !!!\nThe new balance is \t: {new_balance}')

 # function For get age, DOB, sex from NIC Number
def get_Nic():                                     
    mon=[31,29,31,30,31,30,31,31,30,31,30,31]       #assign days in 12 months for check date_part is which day of the year
    while True:
        try:        
            nic_no=input(f"{'Enter your NIC Number  ':<50}:").strip()
            if os.path.exists('customers.txt'): 
                customers = getFileAsDic('customers.txt')
                for key, value in customers.items():
                    if nic_no == value['NIC']:
                        print(f"⚠️NIC number you entered is already exist with customer id of : {key} and name of : {value['Name']}") 
                        get_Nic()
            else: pass
            if(len(nic_no)==12) and nic_no.isdigit():
                year = int(nic_no[:4])
                day_part = int(nic_no[4:7])
            elif len(nic_no)==10:
                day_part = int(nic_no[2:5])
                if int(nic_no[:2])>10:
                    year = int('19'+nic_no[:2])         # for born before 2000, not works for born before year of 1910
                else:   year = int('20'+nic_no[:2])     #for born after 2000
            else:                                       # user input doesn't meet requirement of 10 or 12 digits.
                print("\t\tInvalid NIC number...!\tNIC must be (12 digits)/(9 digits with an letter)\nPlease Re-enter correct number.\n")
                continue
            age = int(datetime.now().year)-year
            if day_part<366:
                days=day_part
                sex = "MALE"
            elif day_part>500 and (day_part-500)<366:           #checks for female and also for valid nic number
                days=day_part-500
                sex = "FEMALE"
            else:
                print('\t\t💥NIC Number you entered is not valid....\n\t Please Re-Enter your correct NIC Number.')
                continue
            sum=0                                                           #checking for get day and month with [month]
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
        except (ValueError, TypeError, AttributeError):
            print("\t💥Invalid NIC number...!💔\tNIC must be (12 digits)/(9 digits with an letter)\nPlease Re-enter correct number.\n")
            continue

def get_customer_details():                                 #function for ger customer information
    customer_details={}
    while True:
        name = input(f"{"Enter new Customer's name in full : ":<50}:").strip().title()
        space_removed_name = name.replace(' ','')
        if len(name) < 3:
            print("\t💥NAME must be in letters only and minimum 3 letters... please re enter a valid name")
            continue
        elif not  space_removed_name.isalpha():
            print("\t💥NAME must be in letters only and minimum 3 letters... please re enter a valid name")
            continue
        else:
            break
    nic_details=get_Nic()
    nic_no = nic_details[0]
    sex = nic_details[1]    
    age = nic_details[2]    
    dob = f'{nic_details[3]}-{nic_details[4]}-{nic_details[5]}'
    address = input(f"{"Enter new Customer's address":<50}:")
    users = getFileAsDic('users.txt')
    while True:                                                         #checking for username already exists in system.
        username = input(f"{"Enter new Customer's username ":<50}:")
        for key,value in users.items():
            if username == users[key]['user']:
                print('\t\t😔😔😔\t User name already exists please Retry with another one')
                break
        else:   break
    print('Password, you typing is INVISIBLE, please type a password and HIT ENTER KEY!!!')
    password = getpass.getpass(f"{'   Enter password for username of {username}':<50}")
    customer_details =[name, address, nic_no, age, sex, dob, username, password]
    return customer_details

# function for create a customer
def create_customer():
    with open('defaults.txt','r+') as file:
        default=file.readline().split(',')
        customer_id = default[0]
        account_no =int(default[1])
    details=get_customer_details()
    with open('customers.txt','a') as file:
        file.write(f"{customer_id}::Name:{details[0]},Address:{details[1]},NIC:{details[2]},Age:{details[3]},sex:{details[4]},dob:{details[5]},Account_no:{account_no}\n")
    print(f'\n\t🆗\tCustomer with customer id:- {customer_id} created successfully....!!!\n')
    with open('users.txt','a') as file:
        file.write(f'{customer_id}::user:{details[6]},pass:{details[7]}\n')
        deposit(customer_id, 'Initial_Deposit')
    print(f'\t🆗\tAccount opened successfully...!!!\n\t\t{'#'*36}\n')
# To write file next account number and customer id for next creation with an increment.
    next_account_no = account_no +1
    num_partOf_customer_id = int(customer_id[1:])
    next_customer_id = (f'C{(num_partOf_customer_id + 1):04}')
    with open('defaults.txt','w') as file:
        file.write(f'{next_customer_id},{next_account_no}')

def check_balance(accountNo):                                     #fUNCTION FOR BALANCE CHECK
    try:
        account_no = accountNo
        accounts=getFileAsDic('accounts.txt')
        if account_no in accounts:
            for key in accounts:
                if int(key) == int(accountNo):
                    balance = float(accounts[key]['balance'])
            print(f'Current Account balance of {accountNo} is : {balance:,.2f}\n')
        else:
            print("❌❌❌Account number you entered is not in our system,\n\tplease Try again....!")
    except (UnboundLocalError, KeyError, FileNotFoundError, TypeError):
        print(f"\t❌❌❌\tAccount Number is invalid or not registered, please RE-Try again or contact bank for further details\n\t\t{'X'*45}\n")
        pass
def login_history():
    log = getFileAsDic('login_history.txt')
    print(f"\t\t\t\t{'*'*36}\n\t\t\t\tLOGIN HISTORY OF THIS BANKING SYSTEM\n\t\t\t\t{'*'*36}")
    print(f"\t{'No.':<5}{'DATE':<25}{'CUSTOMER ID':<25}{'LOGGED USER NAME'}\n")
    order_no = 0
    for key in log:
        print(f"\t{order_no:<5}{key:<25}{log[key]['c_id']:<25}{log[key]['user']}")
        order_no +=1


def get_transaction_history_by_acc_no(account_no): 
    try:                             #getting Transaction history for a given Account Number 
        print(f"{'*'*36}\nTRANSACTION HISTORY OF {account_no}\n{'*'*36}")
        print(f"\t{'No.':<5}{'date':<25}{'type of transaction':<25}{'amount':>20}{'balance':>20}\n\t{'='*2:<5}{'='*10:<25}{'='*18:<35}{'='*10:<20}{'='*10:<20}")
        transactions=getFileAsDic('transactions.txt')
        order_no = 0
        for key,value in transactions.items():
            if str(value['acc_no']) == str(account_no):
                order_no +=1
                print(f"\t{order_no:<5}{key:<25}{value['type']:<25}{float(value['amount']):>20,.2f}{float(value['balance']):>20,.2f}\n")
        if order_no == 0:
            print("❌❌❌No transactions found for given sccount number.\n")
    except (UnboundLocalError, KeyError, FileNotFoundError):
        print(f"\t❌❌❌\tAccount Number is invalid or not registered, please RE-Try again or contact bank for further details\n\t\t{'X'*45}\n")
        pass
#getting transaction history by date
def get_transaction_history_by_date(date):
    print(f"TRANSACTION HISTORY FOR {date}\n{'*'*81}")
    print(f"\t{'No.':<5}{'Account No.':<15}{'type of transaction':<25}{'amount':>20}{'balance':>20}")
    transactions=getFileAsDic('transactions.txt')
    order_no = 0
    for key in transactions:
        if key.startswith(date):
            order_no +=1
            print(f"\t{order_no:<5}{transactions[key]['acc_no']:<15}{transactions[key]['type']:<25}{float(transactions[key]['amount']):>20,.2f}{float(transactions[key]['balance']):>20,.2f}\n")
    if order_no == 0:
        print("\t❌❌❌No transactions found in given date.\n")

#function for inter bank account transfers
def transfer_between_accounts(customer_id):
    date_time=datetime.today().replace(microsecond=0)
    accounts = getFileAsDic('accounts.txt')
    customers = getFileAsDic('customers.txt')
    account_no = customers[customer_id]['Account_no']
    if account_no in accounts:
        balance = float(accounts[account_no]['balance'])
        print(f"Your current BALANCE is : {balance}\nTransfer Money to another account, ", end=" * ")
        to_Acc = get_acc_no_as_input()
        print("\nTo Transfer Money to another account")
        while True:
            amount = get_amount("Transfer")
            if amount > balance :
                print('\t🚫\tAmount Exceeded account balance...\n \tAmount must be lower than account balance...\n')
                continue
            else: break
        accounts[account_no]['balance'] = float(accounts[account_no]['balance']) - amount
        new_balance = accounts[account_no]['balance']
        writeDicToFile(accounts,'accounts.txt')
        with open('transactions.txt','a') as file:
            file.write(f'{date_time}::cus_id:{customer_id},acc_no:{account_no},type:Transfer Debit,amount:{amount},balance:{new_balance}\n')
        print(f'Transfer of {amount:,.2f} from your account to account : {to_Acc} is succcessful !!!\nAnd the money was debitted form your account.\n\t\t your current balance is : {new_balance}')
        accounts[to_Acc]['balance'] = float(accounts[to_Acc]['balance']) + amount
        new_balance =  accounts[to_Acc]['balance']
        writeDicToFile(accounts,'accounts.txt')
        date_time1=datetime.today().replace(microsecond=0)
        with open('transactions.txt','a') as file:
            file.write(f'{date_time1}::cus_id:{customer_id},acc_no:{to_Acc},type:Transfer credit,amount:{amount},balance:{new_balance}\n')
    else:
        print(f"\t👎\tInvalid Customer id OR Account not created yet.\n\t\t\tPlease contact bank for further assistants.")
def change_pw(c_id,username):
    users=getFileAsDic('users.txt')
    for key in users:
        if key == c_id:
            username=users[c_id]['user']
    new_pw = input(f"Enter new password for username of({username}) :")
    users[c_id]['pass'] = new_pw
    writeDicToFile(users,'users.txt')
    print('Password changed successfully.!\nPlease login again with your new password :\n')
    main_menu()                                                                                 #after password change, call main_menu() for relogin

def view_customer_details(c_id):
    customer_details = getFileAsDic('customers.txt')
    while True:
        try:
            print(f"\tCUSTOMER DETAILS OF :{c_id}\n{'⁙'*63}")
            print(f"{'NAME ':<15}:{customer_details[c_id]['Name']:<30}{'NIC No.':<20}{customer_details[c_id]['NIC']}\n")
            print(f"{'GENDER ':<15}:{customer_details[c_id]['sex']:<30}{'DATE OF BIRTH : ':<20}{customer_details[c_id]['dob']}\n")
            print(f"{'AGE : ':<15}{customer_details[c_id]['Age']:<30}{'ACCOUNT NUMBER : ':<20}{customer_details[c_id]['Account_no']:<20}\n")
            print(f"{'ADDRESS ':<15}:{customer_details[c_id]['Address']}\n")
            break  
        except KeyError:
            print("\tCUSTOMER ID is not valid\n\tPlease Enter as format of (C****) \n")
            if input("type 'exit' for out from system.... OR Press ENTER for continue. : ").strip().lower() == 'exit':
                exit()
            else:
                c_id = input("Enter customer id for get details : ")
def delete_customer(customer_id):
    customers = getFileAsDic('customers.txt')
    transactions = getFileAsDic('transactions.txt')
    transactions1=transactions.copy()
    accounts = getFileAsDic('accounts.txt')
    users = getFileAsDic('users.txt')
    login_history = getFileAsDic('login_history.txt')
    login_history1 = login_history.copy()
    account_no = customers[customer_id]['Account_no']
    try:
        for key in customers:
            if key == customer_id:
                if input('Please Confirm the customer ID for delete : ') == customer_id:
                    if input('Are You Sure About Deletion ?\nEnter Y/N for confirm : ').upper() == 'Y':
                        customers.pop(customer_id)
                        del users[customer_id]
                        print('Customer deleted from customers and users successfully')
                        break
                    else:
                        print("THANK YOU for your confirmation as 'NO' .")
                        return
        else:
                print('Customer ID is not found, please RE-Try with the correct one. ')
        for key, value in accounts.items():
            if value['cus_id'] == customer_id:
                del accounts[key]
                print('Customer deleted from accounts successfully')
                break
        else: print('No accounts found for given Customer ID\n')
        no_of_transactions = 0
        for key, value in transactions1.items():
            if value['cus_id'] == customer_id:
                transactions.pop(key)
                no_of_transactions += 1
        print(f'{no_of_transactions} Customer Transactions were deleted from Transactions History successfully')
        if no_of_transactions == 0:
            print('No Transactions found for given Customer ID\n')
        no_of_login = 0
        for key, value in login_history1.items():
            if value['c_id'] == customer_id:
                login_history.pop(key)
                no_of_login += 1
        print(f'{no_of_login} Customer Logins were deleted from login_history History successfully\n')
        if no_of_login == 0:
            print('No Logins found for given Customer ID\n')
        writeDicToFile(users, 'users.txt')
        writeDicToFile(customers, 'customers.txt')
        writeDicToFile(accounts, 'accounts.txt')
        writeDicToFile(transactions, 'transactions.txt')
        writeDicToFile(login_history, 'login_history.txt')
    except KeyError:
        print('Something going wrong, please retry with correct customer-ID')
        pass

#MENU FOR PROCESS AS ADMIN, if admin logged in successful.
def admin_menu():
    print(f"{'=-'*63}\n\t\t\tWELCOME TO ABCD BANK as an ADMIN...!!!!\n{'=-'*63}")
    while True:
        print('\t1. Create a customer')
        print('\t11. Delete Customer')
        print('\t2. Deposit to an account')
        print("\t3. View a customer's details")
        print('\t4. Check transaction history of a account')
        print('\t5. Check transaction history by a date.')
        print("\t6. view an account's balance")
        print("\t7. View Login History")
        print("\t8. Change password")
        print('\t9. Logout')
        print('\t0. Exit\n')
        try:
            choice=int(input('As a admin please chose a choice : '))
            if choice in [1,2,3,4,5,6,7,8,9,11]:
                return choice
            elif choice ==0:
                exit()
            else:
                print('invalid choice....!\nPlease choose a correct one between 1-9\n')
                continue
        except ValueError:
            print('Invalid input please enter a valid number between 1-9\n')
            continue
#MENU FOR PROCESS AS USER, if user logged in successful.
def user_menu():
    print(f"{'=-'*63}\n\t\t\tWELCOME TO ABCD BANK AS AN USER...!!!!\n{'=-'*63}")
    while True:
        print('\t1. Check Balance of your account')
        print('\t2. Deposit to your account.')
        print('\t3. Withdrawal from your account.')
        print('\t4. To Transfer money to Another Account from your account.')
        print('\t5. Transaction History of your account.')
        print('\t6. change your login password.')
        print('\t7. Logout.')
        print('\t8. Exit.\n')
        try:
            choice=int(input('As a user please chose a choice : '))
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

# Main menu for execution of main program.
attempt = 3
def main_menu():
    global attempt
    welcome()
    username=input('\tEnter your username : ').strip()
    password=getpass.getpass('Password, you typing is INVISIBLE, please type correct password and HIT ENTER KEY!!!\n\tEnter your password  : ').strip()
    print("\t\t\t✔✔✔✔✔\tPASSWORD Entered......!\t✔✔✔✔✔")
    users=getFileAsDic('users.txt')
    for key in users:
        if username == users[key]['user']:
            customer_id = key               
            if username=='admin' and password == users[key]['pass']:
                print(f"Logged in as ADMIN successfully.....!!!!\n{' ⚜ '*40}")
                date_time2 = datetime.today().replace(microsecond=0)
                with open('login_history.txt','a') as file:
                    file.write(f"{date_time2}::c_id:{customer_id},user:{username}\n")
                while True:
                    select = admin_menu()
                    if select ==1:      create_customer()
                    if select ==11:
                        del_cus_id = input('Enter the Customer -ID for delete : ')
                        delete_customer(del_cus_id)
                    elif select ==2:    deposit(input("Enter Customer's ID or Account number for Deposit : "), "Deposit")
                    elif select ==3:    view_customer_details(input("Enter Customer's ID for Details : " ))
                    elif select ==4:    get_transaction_history_by_acc_no(get_acc_no_as_input())
                    elif select ==5:    get_transaction_history_by_date(input("Please Enter date for transaction history as YYYY-MM-DD : "))
                    elif select ==6:    check_balance(get_acc_no_as_input())
                    elif select ==7:    login_history()
                    elif select ==8:
                        a = input("1.\tFor change ADMIN password:-\t PRESS-- 1\n\tFor change a USER's password:-\t PRESS--2")
                        if a == '1':  change_pw(customer_id, username)
                        elif a== '2':   change_pw(input("Enter the USER's Customer ID for change password : "),input("Enter the USER's username for change password : "))
                        else:
                            print("invalid choice....!!!\n Please retry....!!!")
                            continue
                    elif select == 9:
                        print(f"Thank you ..........\n{'✈ 🛩 🚀 '*10}")
                        main_menu()        
            elif password==users[key]['pass']:
                print(f"Logged in as USER successfully....!!!!\n{' ✔ '*40}")
                date_time3 = datetime.today().replace(microsecond=0)
                with open('login_history.txt','a') as file:
                    file.write(f"{date_time3}::c_id:{customer_id},user:{username}\n")
                while True:
                    select = user_menu()
                    if select ==1:      check_balance(int(get_acc_no(customer_id)))
                    elif select ==2:    deposit(customer_id, 'Deposit')
                    elif select ==3:    withdrawal(customer_id)
                    elif select ==4:    transfer_between_accounts(customer_id)
                    elif select ==5:    get_transaction_history_by_acc_no(get_acc_no(customer_id))
                    elif select ==6:    change_pw(customer_id,username)
                    elif select ==7:
                        print(f"Thank you ..........\n{'✈ 🛩 🚀 '*10}")
                        main_menu()
            else:
                print('\tPassword is incorrect.! Please retry...!')
                attempt -=1
                if attempt ==0:
                    print("You exceeded maximum attempt of login try allowed...!")
                    exit()
                else:
                    print(f"\n\t\t\tYou have ⚠️ {attempt} ⚠️ more chances for try login.\n")
                    main_menu()
    else:
        print('\t⛔⛔⛔Access Denied...!\n\tUsername is not exists in our system...\n \tContact admin for register username and password!')
        attempt -=1
        if attempt ==0:
            print("You exceeded maximum attempt of login try allowed...!")
            exit()
        else:
            print(f"\n\t\t\tYou have ⚠️ {attempt} ⚠️ more chances for try login.\n")
            main_menu()
        main_menu()        
main_menu()
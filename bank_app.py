#create a Text file as user.txt for keeping Default Username and password
try:
    with open('user.txt','x') as file:
        file.write('Admin::admin:1234\n')
except FileExistsError:
    pass
#create a Text file as defaults.txt for keeping upcoming Customer Id and Account Number
try:
    with open('defaults.txt','x') as file:
        file.write('101,10001')
except FileExistsError:
    pass
#importing datetime for get date and time for transaction history
from datetime import datetime

# Just a function for a welcome note
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
# function for Deposit
def deposit(customer_id,account_no,amount,deposit_type='Deposit'):
    if deposit_type == 'Initial_Deposit':
        balance = amount
        print(account_no)
        print(balance)
        with open('accounts.txt','a') as file:
            file.write(f'{account_no}::cus_id:{customer_id},balance:{amount}\n')
        with open('transactions.txt','a') as file:
            file.write(f'{datetime.today().replace(microsecond=0)}::cus_id:{customer_id},acc_no:{account_no},type:{deposit_type},amount:{amount},balance:{balance}\n')
    else:
        exit()
    # else:
    #     with open('accounts.txt','a') as file:
    #         for line in file:
    #             key,value = line.strip().split('::')
    #             if key == account_no:

def create_customer():
    with open('defaults.txt','r+') as file:
        default=file.readline().split(',')
        print(default)
        customer_id =int(default[0])
        account_no =int(default[1])
        print(customer_id,account_no)
    name = input("Enter Your name : ")
    age = input("Enter Your Age : ")
    address = input("Enter Your address : ")
    username = input("Enter Customer's username : ")
    password = input("Enter Customer's password : ")
    with open('customers.txt','a') as file:
        file.write(f'{customer_id}::name:{name},Age:{age},Adress:{address},AccountNo:{account_no}\n')
    print('customer created successfully')
    with open('user.txt','a') as file:
        file.write(f'{customer_id}::{username}:{password}\n')
    try:
        amount=int(input(print('To open an account enter the amount for initial deposit:')))
        deposit(customer_id,account_no,amount,'Initial_Deposit')
    except ValueError:
        print('amount must be in numbers only')
        pass
    account_no +=1
    customer_id +=1
    with open('defaults.txt','w') as file:
        file.write(f'{customer_id},{account_no}')

def create_account():
    print('account created')




def withdrawal(customer_id,account_no,amount):
    print('withdraw success')
    a = getFileAsDic('accounts.txt')
    if account_no in a.keys:
        a[account_no]['balance'] += amount
        new_balance = a[account_no]['balance']
        writeDicToFile(a,'accounts.txt')
        with open('transactions.txt','a') as file:
            file.write(f'{datetime.today().replace(microsecond=0)}::cus_id:{customer_id},acc_no:{account_no},type:Withdrawal,amount:{amount},balance:{new_balance}\n')
    else:
        print("account number not found\nPlease Retry with a correct one")
def check_balance(account_no):
    a=getFileAsDic('accounts.txt')
    if account_no in a:
        balance = a[account_no]['balance']
        print(f'account balance for{account_no} is : {balance}')
    else:
        print("account number not found\nPlease Retry with a correct one")
    
def transaction_history(account_no):
    a = getFileAsDic('transactions.txt')
    # for key,value in a.items():
    #     str = ""
    #     for sub_key,Sub_value in value.items():
    #         srt += (f'{}') 


        
    print('transaction history of ')

def getCustomerDetails(customer_id):
    print('customer details of ')

def getAccountDetails(account_No):
    print('account details of ')

def change_pw(c_id,username):
    new_pw = input(f"Enter new password for username of({username}) :")
    a=getFileAsDic('user.txt')
    a[c_id][username] = new_pw
    writeDicToFile(a,'user.txt')
    print('Password changed successfully.! Please login again :')
    main_menu()




#MENU FOR PROCESS AS ADMIN, if admin logged in successful..!
def admin_menu():
        print('1. create a customer')
        print('2. create an account')
        print('3. view/change/upgrade a customer details')
        print('4. check transactions of a account')
        print('5. view customer details')
        print('6. view account details')
        print('7. change admin password')
        print('8. Logout')
        print('9. Exit')
        try:
            choice=int(input('As a admin please chose a choice'))
            if choice in [1,2,3,4,5,6,7,8]:
                return choice
            elif choice ==9:
                    exit()
        except ValueError:
            print('Invalid input please enter a valid number between 1-8')
#MENU FOR PROCESS AS USER, if user logged in successful..!
def user_menu():
    print('welcome user')
    print('1. Check Balance')
    print('2. Deposit')
    print('3. Withdrawal')
    print('4. Transaction History')
    print('5. view customer details')
    print('6. view account details')
    print('7. change your password')
    print('8. Logout')
    print('9. Exit')
    selection = int(input('Enter your choice : '))
    return selection
# Main menu for execution of main program.
def main_menu():
    username=input('\ntype "exit" for EXIT from here\nEnter your username : ').strip()
    if username =='exit' :
        exit()
    password=input('Enter your password  : ').strip()
    a=getFileAsDic('user.txt')
    for item in a.items():
        if username in item[1]:
            customer_id = item[0]               
            if username=='admin' and password==item[1][username]:
                print('login as admin successfully:')
                while True:
                    select = admin_menu()
                    if select ==1:
                        create_customer()
                    elif select ==2:
                        create_account()
                    elif select ==3:
                        getCustomerDetails()
                    elif select ==4:
                        transaction_history()
                    elif select ==5:
                        getCustomerDetails()
                    elif select ==6:
                        getAccountDetails()
                    elif select == 7:
                        change_pw(customer_id,username)
                    elif select == 8:
                        welcome()
                        main_menu()
                    elif select == 9:
                        exit()
            elif password==item[1][username]:
                print('Welcome as user!!!')
                select = user_menu()
                b = getFileAsDic('customers.txt')
                account_no = b[customer_id]['AccountNo']
                if select ==1:
                    check_balance(customer_id)
                    break
                elif select ==2:
                    deposit()
                elif select ==3:
                    amount = float(input("Please Enter amount for withdraw : "))
                    withdrawal(customer_id, acc_no, amount)
                elif select ==4:
                    transaction_history()
                elif select ==5:
                    getCustomerDetails()
                elif select ==6:
                    getAccountDetails()
                elif select == 7:
                    print()
                    change_pw(customer_id,username)
                elif select == 8:
                    break
            else:
                print('Password is incorrect.! Please retry...!')
    else:
        print('Access Denied...!\nUsername not exists...\n Contact admin for register username and password!')

welcome()           
main_menu()

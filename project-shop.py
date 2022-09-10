from datetime import datetime
import sqlite3
cnt=sqlite3.connect('C:/store.db')
islogin=False
isadmin=False
userid=""
mark=0
########################################## create user table
# cnt.execute(''' CREATE TABLE users
# (ID INTEGER PRIMARY KEY,
#   fname CHAR(20),
#   lname CHAR(20),
#   addr CHAR(50),
#   grade INT(10),
#   username CHAR(15),
#   password CHAR(15),
#   edate CHAR(10),
#   ncode CHAR(15),
#   reserve1 CHAR(10))''')
# print('done')
# cnt.close()

############################################ create product table

# cnt.execute(''' CREATE TABLE products
# (ID INTEGER PRIMARY KEY,
#   pname CHAR(20),
#   quantity INT(30),
#   bprice INT(20),
#   sprice INT(20),
#   edate CHAR(15),
#   brand CHAR(40),
#   reserve1 CHAR(20))''')
# print('done')
# cnt.close()

######################################### create transactions table

# cnt.execute(''' CREATE TABLE transactions
# (ID INTEGER PRIMARY KEY,
#   uid INT(15),
#   pid INT(15),
#   bdate CHAR(15),
#   qnt INT(5),
#   comment CHAR(50),
#   reserve CHAR(30))''')
# print('done')
# cnt.close()
# transactios
############################################ main program


def validation(fname,lname,addr,username,password,cpassword,ncode):
    global cnt
    errorlist=[]
    if(fname=="" or lname=="" or addr=="" or username=="" or password=="" or cpassword=="" or ncode==""):
        msg='please fill all of blanks'
        errorlist.append(msg)
    if(len(password)<8):
        msg='pass lenght must be at least 8'
        errorlist.append(msg)
    if(password!=cpassword):
        msg='pass and confirm missmatch'
        errorlist.append(msg)
        
    if(not(ncode.isnumeric())):
        msg='national code should be numeric'
        errorlist.append(msg)
    
    sql='SELECT * FROM users WHERE username=? '
    cursor=cnt.execute(sql,(username,))
    rows=cursor.fetchall()
    if(len(rows)!=0):
        msg='username already exist'
        errorlist.append(msg)
        
    return errorlist



def submit():
    
    fname=input('please enter your name:  ')
    lname=input('please enter your last name:  ')
    addr=input('please enter your address:  ')
    grade=0
    edate=datetime.today().strftime('%y-%m-%d')
    username=input('please enter your username:  ')
    password=input('please enter your password:  ')
    cpassword=input('please enter your password confirmation:  ')
    ncode=input('please enter your national code:  ')
    result=validation(fname,lname,addr,username,password,cpassword,ncode)
    if(len(result)!=0):
        for err_msg in result:
            print(err_msg)
        return
    sql=''' INSERT INTO users(fname,lname,addr,grade,username,password,edate,ncode)
    VALUES(?,?,?,?,?,?,?,?)'''
    cnt.execute(sql,(fname,lname,addr,grade,username,password,edate,ncode))
    cnt.commit()
    print('submit done successfully')


    
def login():
    global islogin,isadmin,userid
    if(islogin):
        print('you are already logged in')
        return
    user=input('please enter username:  ')
    passw=input('please enter password:  ')
    sql=''' SELECT username,id FROM users WHERE  (username=? AND password=?)'''
    cursor=cnt.execute(sql,(user,passw))
    row=cursor.fetchone()
    if(not(row)):
        print('wrong user or pass')
        return
    print('welcome to your account')
    userid=row[1]
        
    islogin=True
    if user=='admin':
        isadmin=True



def logout():
    global islogin,isadmin,userid,mark
    if(not(islogin)):
        print('you are already logged out')
        return
    islogin=False
    isadmin=False
    userid=""
    print('you are logged out now')
    mark=0



def mproducts():
    global islogin,isadmin
    if(islogin==False or isadmin==False):
        print('you are not allowed for this action')
        return
    
    Products_name=input('please enter product name:  ')
    quantity=input('please enter quantity  ')
    buy_price=input('please enter buy price:  ')
    sell_price=input('please enter buy sell price:  ')
    ex_date=""
    brand=input('please enter brand name:  ')
    ###############
    sql="SELECT pname FROM products WHERE pname=? "
    cursor=cnt.execute(sql,(Products_name,))
    rows=cursor.fetchall()
    if(len(rows)>0):
        print('product name already exist')
        return
    ###############
    sql=''' INSERT INTO products(pname,quantity,bprice,sprice,edate,brand)
    VALUES(?,?,?,?,?,?)'''
    cnt.execute(sql,(Products_name,quantity,buy_price,sell_price,ex_date,brand))
    cnt.commit()
    print('data inserted successfully')



def buy():
    global islogin,userid
    if(islogin==False):
        print('first you must login')
        return
    bdate=datetime.today().strftime('%y-%m-%d')
    pname=input('enter a product name you want to buy:  ')
    sql="SELECT * FROM products WHERE pname=?"
    cursor=cnt.execute(sql,(pname,))
    row=cursor.fetchone()
    if(not(row)): 
        print('wrong product name')
        return
    print('product:',row[1],'Q:',row[2],' brand:',row[6],' price:',row[4])
    num=int(input('number of products? '))
    if(num<=0):
        print('wrong number')
        return
    if(num>row[2]):
        print('not enough number of products')
        return
    print('total cost ',num*row[4])
    confirm=input('are you sure? [yes/no]: ')
    if(confirm!='yes'):
        print('canceled by user')
        return
    newquant=int(row[2])-num
    sql="UPDATE products SET quantity=? WHERE pname=?"
    cnt.execute(sql,(newquant,pname))
    print('thanks for your shopping')
    cnt.commit()
    
    sql='''INSERT INTO transactions (uid,pid,bdate,qnt)
           VALUES(?,?,?,?)'''
    cnt.execute(sql,(userid,row[0],bdate,num))
    cnt.commit()
    


def plist():
    sql=" SELECT pname,quantity FROM products WHERE quantity>0 "
    cursor=cnt.execute(sql)
    rows=cursor.fetchall()
    for row in rows:
        print('product name:',row[0],'  Quantity:',row[1])
    


def alltrc():
    global islogin,isadmin
    if(not(isadmin)):
        print('you are not allowed for this action')
        return
    if(not(islogin)):
        print('you are not logged in')
        return
    
    sql='''SELECT users.lname,products.pname,transactions.qnt,transactions.bdate FROM transactions INNER JOIN users
    ON transactions.uid=users.id
    INNER JOIN products
    ON transactions.pid=products.id'''
    cursor=cnt.execute(sql)
    for row in cursor:
        print('user: ',row[0],"products: ",row[1],"qnt: ",row[2],"date: ",row[3])



def uedit():
    global islogin,isadmin,mark
    if(not(isadmin)):
        print('you are not allowed for this action,you must login as admin')
        return
    if(not(islogin)):
        print('you are not logged in')
        return
    ############ showing user id and usernames
    sql='''SELECT id,username FROM users '''
    cursor=cnt.execute(sql)
    row=cursor.fetchone()
    while(row):
        print('user id:',row[0],' username:',row[1])
        row=cursor.fetchone()
    ############ username validation
    user=input('please enter username you want to edit: ')
    if(user=='admin'):
        mark=1
    sql="SELECT * FROM users WHERE username=?"
    cursor=cnt.execute(sql,(user,))
    row=cursor.fetchone()
    if(not(row)): 
        print('wrong username,please type username correctly')
        return
    ############ showing users info
    sql='''SELECT fname,lname,addr,grade,username,password,ncode FROM users WHERE username=? '''
    cursor=cnt.execute(sql,(user,))
    row=cursor.fetchone()
    while(row):
        print('firstname:',row[0],' lastname:',row[1],' address:',row[2],' grade:',row[3],' username:',row[4],' password:',row[5],' national code:',row[6])
        row=cursor.fetchone()
    ############
    print('type[firstname/lastname/address/grade/username/password/national code/exit]')
    while(True):
        choose=input('please enter a specification you want to edit: ')
        if(choose=='firstname'):
            select=input('please enter new firstname: ')
            confirm=input('are you sure? [type yes/no]: ')
            if(confirm=='yes'):
                edate=datetime.today().strftime('%y-%m-%d')
                sql='''UPDATE users SET fname=? , edate=? WHERE username=? '''
                cnt.execute(sql,(select,edate,user))
                cnt.commit()
                print('firstname edited successfully')
            else:
                print('opration canceled')
                return
            
        elif(choose=='lastname'):
            select=input('please enter new lastname: ')
            confirm=input('are you sure? [type yes/no]: ')
            if(confirm=='yes'):
                edate=datetime.today().strftime('%y-%m-%d')
                sql='''UPDATE users SET lname=? , edate=? WHERE username=? '''
                cnt.execute(sql,(select,edate,user))
                cnt.commit()
                print('lastname edited successfully')
            else:
                print('opration canceled')
                return
            
        elif(choose=='address'):
            select=input('please enter new address: ')
            confirm=input('are you sure? [type yes/no]: ')
            if(confirm=='yes'):
                edate=datetime.today().strftime('%y-%m-%d')
                sql='''UPDATE users SET addr=? , edate=? WHERE username=? '''
                cnt.execute(sql,(select,edate,user))
                cnt.commit()
                print('address edited successfully')
            else:
                print('opration canceled')
                return
            
        elif(choose=='grade'):
            select=int(input('please enter new grade: '))
            confirm=input('are you sure? [type yes/no]: ')
            if(confirm=='yes'):
                edate=datetime.today().strftime('%y-%m-%d')
                sql='''UPDATE users SET grade=? , edate=? WHERE username=? '''
                cnt.execute(sql,(select,edate,user))
                cnt.commit()
                print('grade edited successfully')
            else:
                print('opration canceled')
                return
            
        elif(choose=='username'):
            if(mark==1):
                print("you cant change admin's username")
                return
            select=input('please enter new username: ')
            confirm=input('are you sure? [type yes/no]: ')
            if(confirm=='yes'):
                edate=datetime.today().strftime('%y-%m-%d')
                sql='''UPDATE users SET username=? , edate=? WHERE username=? '''
                cnt.execute(sql,(select,edate,user))
                user=select
                cnt.commit()
                print('username edited successfully')
                
            else:
                print('opration canceled')
                return
            
        elif(choose=='password'):
            select=input('please enter new password: ')
            select_confirm=input(('enter new password again: '))
            if(len(select)<8):
                print('password lenght must be at least 8')
                
            if(select_confirm==select):
                confirm=input('are you sure? [type yes/no]: ')
                if(confirm=='yes'):
                    edate=datetime.today().strftime('%y-%m-%d')
                    sql='''UPDATE users SET password=? , edate=? WHERE username=? '''
                    cnt.execute(sql,(select,edate,user))
                    cnt.commit()
                    print('password edited successfully')
                    if(mark==1):
                        logout()
                        print('please login with new password')
                        return
                else:
                    print('opration canceled')
                    return
            else:
                print('pass and confirm missmatch')
                
            
            
        elif(choose=='national code'):
            select=input('please enter new national code: ')
            confirm=input('are you sure? [type yes/no]: ')
            if(confirm=='yes'):
                sql='''UPDATE users SET ncode=? WHERE username=? '''
                cnt.execute(sql,(select,user))
                cnt.commit()
                print('national code edited successfully')
            else:
                print('opration canceled')
                return
    
        elif(choose=='exit'):
            return
        else:
            print('wrong input')
    
    
    
    


def pedit():
    global islogin,isadmin
    if(not(isadmin)):
        print('you are not allowed for this action,you must log in as admin')
        return
    if(not(islogin)):
        print('you are not logged in')
        return
    ############ showing product id and product names
    sql='''SELECT id,pname FROM products '''
    cursor=cnt.execute(sql)
    row=cursor.fetchone()
    while(row):
        print('products id:',row[0],' product name:',row[1])
        row=cursor.fetchone()
    ############ product name validation
    product=input('please enter product name you want to edit: ')
    sql="SELECT * FROM products WHERE pname=?"
    cursor=cnt.execute(sql,(product,))
    row=cursor.fetchone()
    if(not(row)): 
        print('wrong product name,please type product name correctly')
        return
    ############ showing products info
    
    sql='''SELECT pname,quantity,bprice,sprice,edate,brand FROM products WHERE pname=? '''
    cursor=cnt.execute(sql,(product,))
    row=cursor.fetchone()
    while(row):
        print('product name:',row[0],' quantity:',row[1],' buy price:',row[2],' sell price:',row[3],' expire date:',row[4],' brand:',row[5])
        row=cursor.fetchone()
    ############
    print('type[product name/quantity/buy price/sell price/expire date/brand/exit]')
    while(True):
        choose=input('please enter a specification you want to edit: ')
        if(choose=='product name'):
            select=input('please enter new product name: ')
            confirm=input('are you sure? [type yes/no]: ')
            if(confirm=='yes'):
                sql='''UPDATE products SET pname=?  WHERE pname=? '''
                cnt.execute(sql,(select,product))
                cnt.commit()
                product=select
                print('product name edited successfully')
            else:
                print('opration canceled')
                return
        
        elif(choose=='quantity'):
            select=int(input('please enter new quantity: '))
            confirm=input('are you sure? [type yes/no]: ')
            if(confirm=='yes'):
                sql='''UPDATE products SET quantity=? WHERE pname=? '''
                cnt.execute(sql,(select,product))
                cnt.commit()
                print('quantity edited successfully')
            else:
                print('opration canceled')
                return
            
        elif(choose=='buy price'):
            select=int(input('please enter new buy price: '))
            confirm=input('are you sure? [type yes/no]: ')
            if(confirm=='yes'):
                sql='''UPDATE products SET bprice=? WHERE pname=? '''
                cnt.execute(sql,(select,product))
                cnt.commit()
                print('buy price edited successfully')
            else:
                print('opration canceled')
                return
        
        elif(choose=='sell price'):
            select=int(input('please enter new sell price: '))
            confirm=input('are you sure? [type yes/no]: ')
            if(confirm=='yes'):
                sql='''UPDATE products SET sprice=? WHERE pname=? '''
                cnt.execute(sql,(select,product))
                cnt.commit()
                print('sell price edited successfully')
            else:
                print('opration canceled')
                return
        
        elif(choose=='expire date'):
            select=input('please enter new expire date: ')
            confirm=input('are you sure? [type yes/no]: ')
            if(confirm=='yes'):
                sql='''UPDATE products SET edate=? WHERE pname=? '''
                cnt.execute(sql,(select,product))
                cnt.commit()
                print('expire date edited successfully')
            else:
                print('opration canceled')
                return
            
        elif(choose=='brand'):
            select=input('please enter new brand name: ')
            confirm=input('are you sure? [type yes/no]: ')
            if(confirm=='yes'):
                sql='''UPDATE products SET brand=? WHERE pname=? '''
                cnt.execute(sql,(select,product))
                cnt.commit()
                print('brand edited successfully')
            else:
                print('opration canceled')
                return
        elif(choose=='exit'):
            return
        else:
            print('wrong input')
    

def delete():
    global islogin,isadmin,mark
    if(not(isadmin)):
        print('you are not allowed for this action,you must login as admin')
        return
    if(not(islogin)):
        print('you are not logged in')
        return
    ############ showing user id and usernames
    sql='''SELECT id,username FROM users '''
    cursor=cnt.execute(sql)
    row=cursor.fetchone()
    while(row):
        print('user id:',row[0],' username:',row[1])
        row=cursor.fetchone()
    ############ username validation
    user=input('please enter username you want to delete: ')
    if(user=='admin'):
        mark=1
    sql="SELECT * FROM users WHERE username=?"
    cursor=cnt.execute(sql,(user,))
    row=cursor.fetchone()
    if(not(row)): 
        print('wrong username,please type username correctly')
        return
    ############
    confirm=input('are you sure to delete this account? [type yes/no]: ')
    if(confirm=='yes'):
        sql='''DELETE  FROM users WHERE username=? '''
        cnt.execute(sql,(user,))
        cnt.commit()
        print('account deleted successfully')
        if(mark==1):
            logout()
            print('please create new admin account immediately')
            return
    else:
        print('opration canceled')
    

def searchprice():
    global islogin
    if(islogin==False):
        print('first you must login')
        return
    price=input('enter a price you want to see the products below the price: ')
    if(not(price.isnumeric())):
        print('price must be numeric')
        return
    sql='''SELECT pname,quantity,bprice FROM products WHERE bprice<? '''
    cursor=cnt.execute(sql,(price,))
    row=cursor.fetchall()
    if(len(row)==0):
        print('found nothing')
    else:
        for item in row:
            print('product name:',item[0],' quantity:',item[1],' buy price:',item[2])


def searchprice2():
    price1=input('enter a max buy price you want to search:  ')
    price2=input('enter a min buy price you want to search:  ')
    if(not(price1.isnumeric())):
        print('price must be numeric')
        return
    if(not(price2.isnumeric())):
        print('price must be numeric')
        return
    
    sql='''SELECT pname,quantity,bprice FROM products WHERE bprice<? and bprice>? '''
    cursor=cnt.execute(sql,(price1,price2))
    row=cursor.fetchall()
    if(len(row)==0):
        print('found nothing')
    else:
        for item in row:
            print('product name:',item[0],' quantity:',item[1],' buy price:',item[2])



print('''plans:\n 1.submit(here you can sign up)\n 2.login\n 3.logout
 4.manage products(here admin can add products info)\n 5.buy\n 6.products list
 7.all transactions(here admin can see all transactions)\n 8.edit users(admin only)\n 9.edit products(admin only)
 10.delete accounts(admin only)
 11.search price(show all products below the amount you entered)
 12.search price2(show all products between 2 amounts you entered)\n 13.exit ''')
while(True):
    plan=int(input('please choose your plan by entering the number:  '))
    if(plan==1):
        submit()
    elif(plan==2):
        login()
    elif(plan==3):
        logout()
    elif(plan==4):
        mproducts()
    elif(plan==5):
        buy()
    elif(plan==6):
        plist()
    elif(plan==7):
        alltrc()
    elif(plan==8):
        uedit()
    elif(plan==9):
        pedit()
    elif(plan==10):
        delete()
    elif(plan==11):
        searchprice()
    elif(plan==12):
        searchprice2()
    elif(plan==13):
        break
    else:
        print('wrong input')











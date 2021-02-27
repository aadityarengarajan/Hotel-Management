import random
from os import remove,rename
from datetime import datetime, timedelta
import mysql.connector

conn=mysql.connector.connect(host='localhost', user='root', passwd='toor', database='avantikaa')
curs=conn.cursor()

ones = ["", "one ","two ","three ","four ", "five ", "six ","seven ","eight ","nine ","ten ","eleven ","twelve ", "thirteen ", "fourteen ", "fifteen ","sixteen ","seventeen ", "eighteen ","nineteen "] 
twenties = ["","","twenty ","thirty ","forty ", "fifty ","sixty ","seventy ","eighty ","ninety "] 
thousands = ["","thousand ","million ", "billion ", "trillion ", "quadrillion ", "quintillion ", "sextillion ", "septillion ","octillion ", "nonillion ", "decillion ", "undecillion ", "duodecillion ", "tredecillion ", "quattuordecillion ", "quindecillion", "sexdecillion ", "septendecillion ", "octodecillion ", "novemdecillion ", "vigintillion "] 
def num999(n): 
    c = n % 10
    b = ((n % 100) - c) / 10
    a = ((n % 1000) - (b * 10) - c) / 100
    t = "" 
    h = "" 
    if a != 0 and b == 0 and c == 0: 
        t = ones[a] + "hundred " 
    elif a != 0: 
        t = ones[a] + "hundred and " 
    if b <= 1: 
        h = ones[n%100] 
    elif b > 1: 
        h = twenties[b] + ones[c] 
    st = t + h 
    return st 
def num2word(num): 
    if num == 0: return 'zero';
    i = 3
    n = str(num) 
    word = "" 
    k = 0 
    while(i == 3): 
        nw = n[-i:] 
        n = n[:-i] 
        if int(nw) == 0: 
            word = num999(int(nw)) + thousands[int(nw)] + word 
        else: 
            word = num999(int(nw)) + thousands[k] + word 
        if n == '': 
            i = i+1 
        k += 1 
    return word[:-1] 

def createtable():
    curs.reset()
    curs.execute('drop table if exists hotel;')
    curs.execute('''create table hotel (
name varchar(20),
address varchar(50),
phoneno int,
checkin date,
checkout date,
duration int,
roomtype varchar(20),
roomcost int,
servicecost int,
roomno int,
paid int,
service varchar(500)
);''')
    print('Table: hotel created')
   

def book():
   curs.reset() 
   with open('guests.dat','ab') as f:
    name=input("Name (str) : ")
    while True:
        try:
            phone=int(input("Phone No. (int) : "))
        except:
            continue
        break
    address=input("address (str) : ")
    while True:
        try:
            checkin=datetime.strptime(input("Check In (DD/MM/YYYY) : "), "%d/%m/%Y")
        except:
            continue
        break
    while True:
        try:
            duration=int(input("Staying for _ days (int) : "))
        except:
            continue
        break
    roomtypevalidation=False
    while roomtypevalidation==False:
        try:
            roomtype=int(input('''
Room Type :-

NO.    TYPE          COST
 1   Single DX      Rs.1200
 2   Double DX      Rs.1700
 3   Single AC      Rs.1000
 4   Double AC      Rs.1300
 5   Single NAC     Rs.600


Room Type (int) :'''))
            if roomtype>=1 and roomtype<=5:
                roomtypevalidation=True
        except:
            continue
    checkout=(checkin + timedelta(days=duration)).strftime("%d/%M/%Y")
    checkin=checkin.strftime("%d/%M/%Y")
    roomno=random.randint(0,100)
    if roomtype==1:
        roomcost=1200
        roomtype="Single DX"

    elif roomtype==2:
        roomcost=1700
        roomtype="Double DX"

    elif roomtype==3:
        roomcost=1000
        roomtype="Single AC"

    elif roomtype==4:
        roomcost=1300
        roomtype="Double AC"

    elif roomtype==5:
        roomcost=600
        roomtype="Single NAC"

    elif roomtype==6:
        roomcost=850
        roomtype="Double NAC"
    while True:
        try:
            paid=float(input("Amount Received (float) : "))
        except:
            continue
        break
    
           
    guest={
    'name':name,
    'address':address,
    'phone no':phone,
    'check in':checkin,
    'check out':checkout,
    'duration':duration,
    'room type':roomtype,
    'room cost':roomcost,
    'service cost':0,
    'room no':roomno,
    'paid':paid,
    'services':[]
    }
    sql=f'insert into hotel values ("{name}","{address}",{phone},{checkin},{checkout},{duration},"{roomtype}",{roomcost},0,{roomno},{paid},NULL)'
    print(sql)
    curs.execute(sql)
    conn.commit() 
    details='''
Name '''+name+'''
address '''+address+'''
Phone No. '''+str(phone)+'''


Checked In / Checking In On '''+str(checkin)+'''
Staying For '''+str(duration)+''' Days
Checked Out / Checking Out On '''+str(checkout)+'''
Room Number '''+str(roomno)+'''
Room Type '''+str(roomtype)+'''
Room Cost '''+str(roomcost)+'''

Added to hotel database.
'''
    print(details)


def info(room):
   curs.reset()
   curs.execute('select * from hotel')
   data = curs.fetchall()
   for i in data:
    flag=0
    keys = ['name','address','phone no','check in','check out','duration','room type','room cost','service cost','room no','paid','services']
    guest = dict(zip(keys, i))
    roomno=guest['room no']
    if room==roomno:
        flag=1
        roomcost=guest['room cost']
        name=guest['name']
        address=guest['address']
        phone=guest['phone no']
        checkin=guest['check in']
        duration=guest['duration']
        checkout=guest['check out']
        roomtype=guest['room type']
        servicecost=guest['service cost']
        paid=guest['paid']
        services=str(guest['services']).replace("'",'').split(',')
        details='''
GUEST INFO

GUEST NAME '''+name+''' | ROOM NUMBER '''+str(roomno)+'''

Name '''+name+'''
address '''+address+'''
Phone No. '''+str(phone)+'''


Checked In / Checking In On '''+str(checkin)+'''
Staying For '''+str(duration)+''' Days
Checked Out / Checking Out On '''+str(checkout)+'''
Room Number '''+str(roomno)+'''
Room Type '''+roomtype+'''
Room Cost Rs.'''+str(roomcost)+'''
Service Cost Rs.'''+str(servicecost)+'''

Amount Received Rs.'''+str(paid)+'''
'''
        print(details)

def delete(room):
    curs.reset()
    print("Are you sure you want to remove the following customer from database?")
    print()
    info(room)
    choice=input("(Y/N) : ")
    if choice=='y' or choice=='Y':
        curs.execute(f"delete from hotel where roomno={room}")
        conn.commit()

def roomservice(room):
    curs.reset()
    ops='''
PERFORM ROOM SERVICE

NO.             SERVICE                  COST         
1               Washing                 Rs.500
2              Coffee/Tea               Rs.50
3             Medical Aid               Rs.250
4              Beautician               Rs.2000
5   Food served in the room /restaurant Rs.1500
6           Telephone Calls             Rs.160

'''
    while 1:
        try:
            print(ops)
            choice=int(input("Choice : "))
        except:
            continue
        break
    costs={1:500,2:50,3:250,4:2000,5:1500,6:750}
    srv={1:'Washing',2:'Coffee/Tea',3:'Medical Aid',4:'Beautician',5:'Food served in the room /restaurant',6:'Telephone Call'}
    curs.execute(f'select * from hotel where roomno={room}')
    guest=curs.fetchall()[0]
    keys = ['name','address','phone no','check in','check out','duration','room type','room cost','service cost','room no','paid','services']
    guest = dict(zip(keys, guest))
    roomno=guest['room no']
    roomcost=guest['room cost']
    name=guest['name']
    address=guest['address']
    phone=guest['phone no']
    checkin=guest['check in']
    duration=guest['duration']
    checkout=guest['check out']
    roomtype=guest['room type']
    paid=guest['paid']
    services=str(guest['services']).replace("'",'').split(',')
    servicecost=float(guest['service cost'])
    services.append(srv[choice])
    servicecost+=costs[choice]
    curs.execute(f"delete from hotel where roomno={room}")
    conn.commit()
    sql=f'insert into hotel values ("{name}","{address}",{phone},{checkin},{checkout},{duration},"{roomtype}",{roomcost},{servicecost},{roomno},{paid},"{(str(services).replace("[","").replace("]",""))}")'.replace('None','NULL')
    curs.execute(sql)
    conn.commit()


def updatedata(room):
    curs.reset()
    print(info(room))
    print()
    ops='''
CHANGE GUEST DATA

NO.             UPDATE     
1                Name
2               address
3              Phone No.
4            Check In Date
5              Duration
6            Check Out Date 
7              Room Type
8             Service Cost
9               Room No.
10             Room Cost
11            Amount Paid

'''
    while 1:
        try:
            print(ops)
            choice=int(input("Choice : "))
        except:
            continue
        break

    if choice==1:
        name=input('Name (str) : ')
        curs.execute(f'update hotel set name={name} where roomno={room}')
        print("Guest Details Updated.")
    elif choice==2:
        address=input('address (str) : ')
        curs.execute(f'update hotel set address={address} where roomno={room}')
        print("Guest Details Updated.")
    elif choice==3:
        while True:
            try:
                phone=int(input("Phone No. (int) : "))
            except:
                continue
            break
        curs.execute(f'update hotel set phoneno={phone} where roomno={room}')
        print("Guest Details Updated.")
    elif choice==4:
        while True:
            try:
                checkin=datetime.strptime(input("Check In (DD/MM/YYYY) : "), "%d/%m/%Y")
            except:
                continue
            break
        curs.execute(f'update hotel set checkin={checkin} where roomno={room}')
        print("Guest Details Updated.")    
    elif choice==5:
        duration=int(input("Staying for _ days (int) : "))
        curs.execute(f'update hotel set duration={duration} where roomno={room}')
        print("Guest Details Updated.")
    elif choice==6:
        while True:
            try:
                checkout=datetime.strptime(input("Check Out (DD/MM/YYYY) : "), "%d/%m/%Y")
            except:
                continue
            break
        curs.execute(f'update hotel set checkout={checkout} where roomno={room}')
        print("Guest Details Updated.")    
    elif choice==7:
        roomtypevalidation=False
        while roomtypevalidation==False:
            try:
                roomtype=int(input('''
Room Type :-

NO.    TYPE          COST
1   Single DX      Rs.1200
2   Double DX      Rs.1700
3   Single AC      Rs.1000
4   Double AC      Rs.1300
5   Single NAC     Rs.600


Room Type (int) :'''))
                if roomtype>=1 and roomtype<=5:
                    roomtypevalidation=True
            except:
                continue
        if roomtype==1:
            roomcost=1200
            roomtype="Single DX"

        elif roomtype==2:
            roomcost=1700
            roomtype="Double DX"

        elif roomtype==3:
            roomcost=1000
            roomtype="Single AC"

        elif roomtype==4:
            roomcost=1300
            roomtype="Double AC"

        elif roomtype==5:
            roomcost=600
            roomtype="Single NAC"

        elif roomtype==6:
            roomcost=850
            roomtype="Double NAC"
        curs.execute(f'update hotel set roomtype={roomtype} where roomno={room}')
        curs.execute(f'update hotel set roomcost={roomcost} where roomno={room}')
        print("Guest Details Updated.")    
    elif choice==8:
        while True:
            try:
                servicecost=int(input("Service Cost (int) : "))
            except:
                continue
            break
        curs.execute(f'update hotel set servicecost={servicecost} where roomno={room}')
        print("Guest Details Updated.")
    elif choice==9:
        while True:
            try:
                servicecost=int(input("Room No. (int) : "))
            except:
                continue
            break
        curs.execute(f'select * from hotel where roomno={room}')
        print("Guest Details Updated.")
        guest=curs.fetchall()[0]
        keys = ['name','address','phone no','check in','check out','duration','room type','room cost','service cost','room no','paid','services']
        guest = dict(zip(keys, guest))
        curs.execute(f'update hotel set roomno={servicecost} where phoneno={guest["phone no"]}')
        print("Guest Details Updated.")
    elif choice==10:
        while True:
            try:
                servicecost=int(input("Room Cost (int) : "))
            except:
                continue
            break
        curs.execute(f'update hotel set servicecost={servicecost} where roomno={room}')
        print("Guest Details Updated.")
    elif choice==11:
        while True:
            try:
                paid=int(input("Amount Paid (int) : "))
            except:
                continue
            break
        curs.execute(f'update hotel set paid={paid} where roomno={room}')
        print("Guest Details Updated.")

def bills(room):
    curs.reset()
    curs.execute(f'select * from hotel where roomno={room}')
    guest=curs.fetchall()[0]
    keys = ['name','address','phone no','check in','check out','duration','room type','room cost','service cost','room no','paid','services']
    guest = dict(zip(keys, guest))
    roomno=guest['room no']
    roomcost=guest['room cost']
    name=guest['name']
    address=guest['address']
    phone=guest['phone no']
    checkin=guest['check in']
    duration=guest['duration']
    checkout=guest['check out']
    roomtype=guest['room type']
    servicecost=guest['service cost']
    paid=guest['paid']
    total=str(1.15*(roomcost+servicecost))
    sales=str(0.15*(roomcost+servicecost))
    billno=str(random.randint(64325543,32544123314))
    details=f'''
ROOM BILL
GUEST NAME {name} | ROOM NUMBER {str(name)}

Name {name}
address {address}
Phone No. {str(phone)}
Bill No. {billno}

Checked In on {str(checkin)}
Stayed For {str(duration)} Days
Checked Out on {str(checkout)}
Room Number {str(roomno)}



Room Rent Rs.{str(roomcost)}
Service Cost Rs.{str(servicecost)}
Sales Tax (15%) Rs.{sales}

Total Rs. {total}

Amount Received Rs.{str(paid)}'''
    print(details)

def servicereport(room):
    curs.reset()
    curs.execute(f'select * from hotel where roomno={room}')
    guest=curs.fetchall()[0]
    keys = ['name','address','phone no','check in','check out','duration','room type','room cost','service cost','room no','paid','services']
    guest = dict(zip(keys, guest))
    roomno=guest['room no']
    roomcost=guest['room cost']
    name=guest['name']
    address=guest['address']
    phone=guest['phone no']
    checkin=guest['check in']
    duration=guest['duration']
    checkout=guest['check out']
    roomtype=guest['room type']
    servicecost=guest['service cost']
    paid=guest['paid']
    services=str(guest['services']).replace("'",'').split(',')
    details='''
SERVICE CHARGE REPORT
GUEST NAME '''+name+''' | ROOM NUMBER '''+str(roomno)+'''

Name '''+name+'''
address '''+address+'''
Phone No. '''+str(phone)+'''
Bill No. '''+str(random.randint(64325543,32544123314))
    print()
    print(details)
    print()
    costs={1:500,2:50,3:250,4:2000,5:1500,6:750}
    srv={
    'Washing':500,
    'Coffee/Tea':50,
    'MedicalAid':250,
    'Beautician':2000,
    'Foodservedintheroom/restaurant':1500,
    'TelephoneCall':750}

    for i in services:
        if i!='NULL':
            print(i,str(' | Rs.'+str(srv[i.replace(" ",'')])))
    print('Total Rs. ',servicecost)
    print('Total (In Words) Rs. ',num2word(servicecost),'Only')

def totalincomereport():
    curs.reset()
    curs.execute(f'select * from hotel')
    guests=curs.fetchall()
    totalcost=0
    tax=0
    received=0
    print('ROOM NO. | ROOM COST | SERVICE COST | AMOUNT RECEIVED | 15% TAX')
    for guestt in guests:
        keys = ['name','address','phone no','check in','check out','duration','room type','room cost','service cost','room no','paid','services']
        guest = dict(zip(keys, guestt))
        roomno=guest['room no']
        roomcost=guest['room cost']
        servicecost=guest['service cost']
        paid=guest['paid']
        print(str(roomno),' | ',str(roomcost),' | ',str(servicecost),' | ',str(paid),' | ',str(0.15*(roomcost+servicecost)))
        totalcost+=roomcost
        totalcost+=servicecost
        tax+=(0.15*(roomcost+servicecost))
        received+=paid
    print()
    print()
    print('Total Income Rs.',totalcost)
    print('Total Tax Rs.',tax)
    print('Total Received Rs.',received)
    print('Total Profit Rs.',totalcost-tax)
    print('Current Profit Rs.',received-tax)


def occupiedroomnos():
    curs.reset()
    print('LIST OF OCCUPIED ROOM NUMBERS')
    curs.execute(f'select * from hotel')
    for i in curs.fetchall():
        keys = ['name','address','phone no','check in','check out','duration','room type','room cost','service cost','room no','paid','services']
        guest = dict(zip(keys, i))
        roomno=guest['room no']
        print(roomno)

menu='''
HOTEL MANAGEMENT PROJECT

1.Booking
2.Cancellation
3.Room Information
4.Room Service
5.Update Customer Data
6.Room Bills
7.Room Service Charges Detailed Report
8.Hotel Total Income Report
9.Occupied Room Numbers
10.Exit
'''
exit=False

while exit==False:
    while 1:
        try:
            print(menu)
            choice=int(input("Choice : "))
        except:
            continue
        break
    if choice==1:
        book()
    elif choice==2:
        while True:
            try:
                room=int(input("Room No. (int) : "))
            except:
                continue
            break
        delete(room)
    elif choice==3:
        while True:
            try:
                room=int(input("Room No. (int) : "))
            except:
                continue
            break
        info(room)
    elif choice==4:
        while True:
            try:
                room=int(input("Room No. (int) : "))
            except:
                continue
            break
        roomservice(room)
    elif choice==5:
        while True:
            try:
                room=int(input("Room No. (int) : "))
            except:
                continue
            break
        updatedata(room)
    elif choice==6:
        while True:
            try:
                room=int(input("Room No. (int) : "))
            except:
                continue
            break
        bills(room)
    elif choice==7:
        while True:
            try:
                room=int(input("Room No. (int) : "))
            except:
                continue
            break
        servicereport(room)
    elif choice==8:
        totalincomereport()
    elif choice==9:
        occupiedroomnos()
    elif choice==10:
        exit=True

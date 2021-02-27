import random
from os import remove,rename
from datetime import datetime, timedelta
import MySQLDB

conn=MySQLDB.connect(host='localhost', user='username', passwd='password', database='SCHOOLPROJECT')
curs=conn.cursor()

def book_room():
   with open('guests.dat','ab') as f:
    while 1:
        try:
            name=input("Name (str) : ")
        except:
            continue
        break
    while 1:
        try:
            phone=int(input("Phone No. (int) : "))
        except:
            continue
        break
    while 1:
        try:
            address=input("address (str) : ")
        except:
            continue
        break
    while 1:
        try:
            checkin=datetime.strptime(input("Check In (DD/MM/YYYY) : "), "%d/%m/%Y")
        except:
            continue
        break
    while 1:
        try:
            duration=int(input("Staying for _ days (int) : "))
        except:
            continue
        break
    while 1:
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
        except:
            continue
        break

    checkout=(checkin + timedelta(days=duration)).strftime("%d/%M/%Y")
    checkin=checkin.strftime("%d/%M/%Y")

    curs.execute(f'select * from hotel')
    rooms = ['EXISTS']
    for i in curs.fetchall():
        rooms.append(str(guest[-3]))
    roomnumber = 'EXISTS'

    while roomnumber in rooms:
        roomnumber=str(random.randint(0,100))

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

    while 1:
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
    'room no':roomnumber,
    'paid':paid,
    'services':[]
    }

    curs.execute(f'insert into hotel values ("{name}","{address}",{phone},{checkin},{checkout},{duration},"{roomtype}",{roomcost},0,{roomnumber},{paid},NULL)')
    conn.commit() 

    details='''
Name '''+name+'''
address '''+address+'''
Phone No. '''+str(phone)+'''


Checked In / Checking In On '''+str(checkin)+'''
Staying For '''+str(duration)+''' Days
Checked Out / Checking Out On '''+str(checkout)+'''
Room Number '''+str(roomnumber)+'''
Room Type '''+str(roomtype)+'''
Room Cost '''+str(roomcost)+'''

Added to hotel database.
'''
    print(details)


def room_information(room):
   curs.execute('select * from hotel')
   data = curs.fetchall()
   for i in data:
    flag=0
    guest = i
    roomnumber=guest[-3]
    if room==roomnumber:
        flag=1
        roomcost=guest[7]
        name=guest[0]
        address=guest[1]
        phone=guest[2]
        checkin=guest[3]
        duration=guest[5]
        checkout=guest[4]
        roomtype=guest[6]
        servicecost=guest[-4]
        paid=guest[-2]
        services=str(guest[-1]).replace("'",'').split(',')
        details='''
GUEST INFO

GUEST NAME '''+name+''' | ROOM NUMBER '''+str(roomnumber)+'''

Name '''+name+'''
address '''+address+'''
Phone No. '''+str(phone)+'''


Checked In / Checking In On '''+str(checkin)+'''
Staying For '''+str(duration)+''' Days
Checked Out / Checking Out On '''+str(checkout)+'''
Room Number '''+str(roomnumber)+'''
Room Type '''+roomtype+'''
Room Cost Rs.'''+str(roomcost)+'''
Service Cost Rs.'''+str(servicecost)+'''

Amount Received Rs.'''+str(paid)+'''
'''
        print(details)

def delete_booking(room):
    print("Are you sure you want to remove the following customer from database?")
    print()
    info(room)
    choice=input("(Y/N) : ")
    if choice in 'Yy':
        curs.execute(f"delete from hotel where roomnumber={room}")
        conn.commit()

def room_service(room):
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
    curs.execute(f'select * from hotel where roomnumber={room}')
    guest=curs.fetchall()[0]
    roomnumber=guest[-3]
    roomcost=guest[7]
    name=guest[0]
    address=guest[1]
    phone=guest[2]
    checkin=guest[3]
    duration=guest[5]
    checkout=guest[4]
    roomtype=guest[6]
    paid=guest[-2]
    services=str(guest[-1]).replace("'",'').split(',')
    servicecost=float(guest[-4])
    services.append(srv[choice])
    servicecost+=costs[choice]
    curs.execute(f"delete from hotel where roomnumber={room}")
    conn.commit()
    curs.execute(f'insert into hotel values ("{name}","{address}",{phone},{checkin},{checkout},{duration},"{roomtype}",{roomcost},{servicecost},{roomnumber},{paid},"{(str(services).replace("[","").replace("]",""))}")'.replace('None','NULL'))
    conn.commit()


def update_customer_data(room):
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
        curs.execute(f'update hotel set name={name} where roomnumber={room}')
        print("Guest Details Updated.")
    elif choice==2:
        address=input('address (str) : ')
        curs.execute(f'update hotel set address={address} where roomnumber={room}')
        print("Guest Details Updated.")
    elif choice==3:
        while 1:
            try:
                phone=int(input("Phone No. (int) : "))
            except:
                continue
            break
        curs.execute(f'update hotel set phoneno={phone} where roomnumber={room}')
        print("Guest Details Updated.")
    elif choice==4:
        while 1:
            try:
                checkin=datetime.strptime(input("Check In (DD/MM/YYYY) : "), "%d/%m/%Y")
            except:
                continue
            break
        curs.execute(f'update hotel set checkin={checkin} where roomnumber={room}')
        print("Guest Details Updated.")    
    elif choice==5:
        duration=int(input("Staying for _ days (int) : "))
        curs.execute(f'update hotel set duration={duration} where roomnumber={room}')
        print("Guest Details Updated.")
    elif choice==6:
        while 1:
            try:
                checkout=datetime.strptime(input("Check Out (DD/MM/YYYY) : "), "%d/%m/%Y")
            except:
                continue
            break
        curs.execute(f'update hotel set checkout={checkout} where roomnumber={room}')
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
        curs.execute(f'update hotel set roomtype={roomtype} where roomnumber={room}')
        curs.execute(f'update hotel set roomcost={roomcost} where roomnumber={room}')
        print("Guest Details Updated.")    
    elif choice==8:
        while 1:
            try:
                servicecost=int(input("Service Cost (int) : "))
            except:
                continue
            break
        curs.execute(f'update hotel set servicecost={servicecost} where roomnumber={room}')
        print("Guest Details Updated.")
    elif choice==9:
        while 1:
            try:
                servicecost=int(input("Room No. (int) : "))
            except:
                continue
            break
        curs.execute(f'select * from hotel where roomnumber={room}')
        print("Guest Details Updated.")
        guest=curs.fetchall()[0]
        curs.execute(f'update hotel set roomnumber={servicecost} where phoneno={guest[2]}')
        print("Guest Details Updated.")
    elif choice==10:
        while 1:
            try:
                servicecost=int(input("Room Cost (int) : "))
            except:
                continue
            break
        curs.execute(f'update hotel set servicecost={servicecost} where roomnumber={room}')
        print("Guest Details Updated.")
    elif choice==11:
        while 1:
            try:
                paid=int(input("Amount Paid (int) : "))
            except:
                continue
            break
        curs.execute(f'update hotel set paid={paid} where roomnumber={room}')
        print("Guest Details Updated.")

def room_bills(room):
    curs.execute(f'select * from hotel where roomnumber={room}')
    guest=curs.fetchall()[0]

    roomnumber=guest[-3]
    roomcost=guest[7]
    name=guest[0]
    address=guest[1]
    phone=guest[2]
    checkin=guest[3]
    duration=guest[5]
    checkout=guest[4]
    roomtype=guest[6]
    servicecost=guest[-4]
    paid=guest[-2]

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
Room Number {str(roomnumber)}



Room Rent Rs.{str(roomcost)}
Service Cost Rs.{str(servicecost)}
Sales Tax (15%) Rs.{sales}

Total Rs. {total}

Amount Received Rs.{str(paid)}'''
    print(details)

def room_servicecharge_report(room):
    curs.reset()
    curs.execute(f'select * from hotel where roomnumber={room}')
    guest=curs.fetchall()[0]

    roomnumber=guest[-3]
    roomcost=guest[7]
    name=guest[0]
    address=guest[1]
    phone=guest[2]
    checkin=guest[3]
    duration=guest[5]
    checkout=guest[4]
    roomtype=guest[6]
    servicecost=guest[-4]
    paid=guest[-2]
    services=str(guest[-1]).replace("'",'').split(',')

    details='''
SERVICE CHARGE REPORT
GUEST NAME '''+name+''' | ROOM NUMBER '''+str(roomnumber)+'''

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

def total_income_report():
    curs.reset()
    curs.execute(f'select * from hotel')
    guests=curs.fetchall()
    totalcost=0
    tax=0
    received=0
    print('ROOM NO. | ROOM COST | SERVICE COST | AMOUNT RECEIVED | 15% TAX')
    for guestt in guests:

        roomnumber=guest[-3]
        roomcost=guest[7]
        servicecost=guest[-4]
        paid=guest[-2]
        print(str(roomnumber),' | ',str(roomcost),' | ',str(servicecost),' | ',str(paid),' | ',str(0.15*(roomcost+servicecost)))
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


def occupied_room_numbers():
    curs.reset()
    print('LIST OF OCCUPIED ROOM NUMBERS')
    curs.execute(f'select * from hotel')
    for i in curs.fetchall():
        roomnumber=guest[-3]
        print(roomnumber)

menu='''
HOTEL MANAGEMENT PROJECT

1. New Booking
2. Booking Cancellation
3. View Room Information
4. Add Room Service Charges
5. Update Customer Data
6. View Room Bills
7. View Room Service Charges Detailed Report
8. View Hotel Total Income Report
9. View Occupied Room Numbers
10.Exit
'''

while 1:
    while 1:
        try:
            print(menu)
            choice=int(input("Choice : "))
        except:
            continue
        break
    if choice==1:
        book_room()
    elif choice==2:
        while 1:
            try:
                room=int(input("Room No. (int) : "))
            except:
                continue
            break
        delete_booking(room)
    elif choice==3:
        while 1:
            try:
                room=int(input("Room No. (int) : "))
            except:
                continue
            break
        room_information(room)
    elif choice==4:
        while 1:
            try:
                room=int(input("Room No. (int) : "))
            except:
                continue
            break
        room_service(room)
    elif choice==5:
        while 1:
            try:
                room=int(input("Room No. (int) : "))
            except:
                continue
            break
        update_customer_data(room)
    elif choice==6:
        while 1:
            try:
                room=int(input("Room No. (int) : "))
            except:
                continue
            break
        room_bills(room)
    elif choice==7:
        while 1:
            try:
                room=int(input("Room No. (int) : "))
            except:
                continue
            break
        room_servicecharge_report(room)
    elif choice==8:
        total_income_report()
    elif choice==9:
        occupied_room_numbers()
    elif choice==10:
        break

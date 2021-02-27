import csv
import os
import random
from datetime import datetime
from datetime import timedelta

def customers():
    with open('customer.csv','r') as details:
        data=csv.reader(details)
        c=0
        customers=[]
        roomnos=[]
        for rec in data:
            if c==0:
                c+=1
                pass
            else:
                customers.append(rec)
                roomnos.append(rec[8])
        return [customers,roomnos]

def customerdetails(rnumber):
    for i in customers()[0]:
        name=i[0]
        address=i[1]
        tele=i[2]
        mobile=i[3]
        checkin=i[4]
        stays=i[5]
        checkout=i[6]
        roomtype=i[7]
        roomno=i[8]
        charges=i[9]
        servcharges=i[10]
        if roomno==rnumber:
            print(f'''
===============INTERNATIONAL INN, SIMLA | CUSTOMER DETAILS=============

Name : {name:10s}   |   Telephone : {tele:10s}
Address : {address:10s} |   Mobile : {mobile:10s}

=======================================================================

Checked In : {checkin} | # of Stay Days : {stays:3s} | Check Out : {checkout}
Room # : {roomno}                           Room Type : {roomtype}
Charges : {charges}
Service Charges : {servcharges}

=======================================================================''')

def customerlist():
    print('===============INTERNATIONAL INN, SIMLA | CUSTOMER LIST================')
    for i in customers()[0]:
        try:
            name=i[0]
            address=i[1]
            tele=i[2]
            mobile=i[3]
            checkin=i[4]
            stays=i[5]
            checkout=i[6]
            roomtype=i[7]
            roomno=i[8]
            charges=i[9]
            servcharges=i[10]
            print(f'''

Name : {name:10s}   |   Telephone : {tele:10s}
Address : {address:10s} |   Mobile : {mobile:10s}

=======================================================================

Checked In : {checkin} | # of Stay Days : {stays:3s} | Check Out : {checkout}
Room # : {roomno}                           Room Type : {roomtype}
Charges : {charges}
Service Charges : {servcharges}

=======================================================================

''')
        except:
            pass

def booking():
    name=input("Customer Name : ")
    address=0
    address=input("Customer Address : ")
    address=address.replace(',','-')
    while 1:
        try:
            telephone=int(input("Customer Telephone # : "))
        except:
            continue
        break

    while 1:
        try:
            mobile=int(input("Customer Mobile # : "))
        except:
            continue
        break
    while 1:
        try:
            checkin=input("Check In Date (DD/MM/YYYY): ")
            checkin=datetime.strptime(checkin, "%d/%m/%Y")
        except Exception as e:
            print(e)
            continue
        break
    stays=0
    while 1:
        try:
            stays=int(input("# of days of stay : "))
        except:
            continue
        break
        
    checkout=(checkin + timedelta(days=stays)).strftime("%d/%M/%Y")
    checkin=checkin.strftime("%d/%M/%Y")
    while 1:
        try:
            roomtype=int(input("Room Type (1-Single DX, 2-Double DX, 3-Single AC, 4-Double AC, 5-Single NAC, 6-Double NAC): "))
        except:
            continue
        break
    roomno=random.randint(1,263)
    if roomtype==1:
        charges=1200
    elif roomtype==2:
        charges=1700
    elif roomtype==3:
        charges=1000
    elif roomtype==4:
        charges=1300
    elif roomtype==5:
        charges=600
    elif roomtype==6:
        charges=850
    rec=[str(name),str(address),str(telephone),str(mobile),str(checkin),str(stays),str(checkout),str(roomtype),str(roomno),str(charges),'0']
    customrs = customers()[0]
    with open('customer.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['CustName','CustAddress','Tele','Mob','CheckIn','Stays','CheckOut','RoomType','RoomNo','Charges','RoomService'])
        writer.writerows(customrs)
        writer.writerow(rec)
    print()
    print("Succesfuly booked room for customer!\n")
    print(f'''
===============INTERNATIONAL INN, SIMLA | CUSTOMER DETAILS=============

Name : {str(name):10s}   |   Telephone : {str(telephone):10s}
Address : {str(address):10s} |   Mobile : {str(mobile):10s}

=======================================================================

Checked In : {str(checkin)} | # of Stay Days : {str(stays):3s} | Check Out : {str(checkout)}
Room # : {str(roomno)}                           Room Type : {str(roomtype)}
Charges : {str(charges)}

=======================================================================''')
    print()

def cancelling(rnumber):
    print("Are you sure you want to cancel the booking of : \n\n")
    customerdetails(rnumber)
    print()
    opn=input("(Y/N) : ")
    if opn in  'Yy':
        towrite=[]
        for i in customers()[0]:
            roomno=i[8]
            if roomno==rnumber:
                pass
            else:
                towrite.append(i)
        with open('customer.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['CustName','CustAddress','Tele','Mob','CheckIn','Stays','CheckOut','RoomType','RoomNo','Charges','RoomService'])
            writer.writerows(towrite)

def roomservice(room):
    opns='''1.Washing
2.Coffee/Tea
3.Medical aid
4.Beautician
5.Food served in the room /restaurant
6.Telephone Calls'''
    while 1:
        try:
            print(opns)
            print()
            opn=int(input("Option : "))
        except:
            continue
        opn=str(opn)
        break
    rates={'1':'500','2':'50','3':'250','4':'2000','5':'1500','6':'750'}
    for i in customers()[0]:
        name=i[0]
        address=i[1]
        tele=i[2]
        mobile=i[3]
        checkin=i[4]
        stays=i[5]
        checkout=i[6]
        roomtype=i[7]
        charges=i[9]
        roomno=i[8]
        if roomno==room:
            servcharges=int(i[10])
            servcharges+=int(rates[str(opn)])
            servcharges=str(servcharges)
            rec=[name,address,tele,mobile,checkin,stays,checkout,str(roomtype),str(roomno),str(charges),servcharges]
            customrs=customers()[0]
            with open('customer.csv', 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(['CustName','CustAddress','Tele','Mob','CheckIn','Stays','CheckOut','RoomType','RoomNo','Charges','RoomService'])
                writer.writerow(rec)
                for i in customrs:
                    roomno=i[8]
                    if roomno==room:
                        pass
                    else:
                        writer.writerow(i)

def occrooms():
    print("Room #   |   Customer")
    roomnos = customers()[1]
    for i in range(len(customers()[0])):
        try:
            print(f"{roomnos[i]}   |  {customers()[0][i][0]}")
        except:
            pass
    print()

def income():
    totinc=0
    for i in customers()[0]:
        try:
            print(f'{i[0]} : Rs. {int(i[9])+int(i[10])}')
            totinc=totinc+int(i[9])+int(i[10])
        except:
            pass
    print()
    print(f"Total Income : Rs. {totinc}")

def servcharges():
    totinc=0
    for i in customers()[0]:
        try:
            print(f'{i[0]} : Rs. {int(i[10])}')
            totinc=totinc+int(i[10])
        except:
            pass
    print()
    print(f"Total Service Charges Income : Rs. {totinc}")


menu='''
===============INTERNATIONAL INN, SIMLA | CUSTOMER SERVICE=============

1.Booking
2.Cancelling
3.Room Service
4.Bill Printing
5.Get All Customers Details
6.Total Income
7.Service Charges Report
8.Occupied Room Numbers
0.Quit

=======================================================================
'''

while 1:
    print(menu)
    opn=int(input('Option : '))
    if opn==1:
        booking()
    elif opn==2:
        room=input("Room # : ")
        cancelling(room)
    elif opn==3:
        room=input("Room # : ")
        roomservice(room)
    elif opn==4:
        room=input("Room # : ")
        customerdetails(room)
    elif opn==5:
        customerlist()
    elif opn==6:
        income()
    elif opn==7:
        servcharges()
    elif opn==8:
        occrooms()
    else:
        quit()
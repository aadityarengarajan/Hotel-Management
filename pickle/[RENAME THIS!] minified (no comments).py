import pickle
import random
from datetime import datetime
from datetime import timedelta
THE_FILE='accounts.dat'
def guestdetails(roomno):
    f=open(THE_FILE,'rb')
    found=0
    while True:
        try:
            rec=pickle.load(f)
            roomnumber=rec[8]
            servicecharges=rec[10]
            if roomno==roomnumber:
                found=1
                roomcharges=rec[9]
                name=rec[0]
                addr=rec[1]
                tel=rec[2]
                mob=rec[3]
                checkindate=rec[4]
                staydays=rec[5]
                checkoutdate=rec[6]
                roomtype=rec[7]
                f.close() 
                return str('''
-guest details-

Name : '''+str(name)+'''
Telephone : '''+str(tel)+'''
Address : '''+str(addr)+'''
Mobile : '''+str(mob)+'''

-stay details-

Check In Date : '''+str(checkindate)+'''
# of Days of Stay : '''+str(staydays)+'''
Check Out : '''+str(checkoutdate)+'''
Room # : '''+str(roomnumber)+'''
Room Type : '''+str(roomtype)+'''
Charges : '''+str(roomcharges)+'''
Service Charges : '''+str(servicecharges)+'''

''')
        except:
            break
    if found==0:
        return str('Guest Not Found ; Sorry :-(')

def newguest():
    f=open(THE_FILE,'ab')
    name=input("Guest Name:")
    while 1:
        try:
            tel=int(input("Guest Tel. # : "))
        except:
            print()
            print("Invalid Entry, Try Again.")
            print()
            continue
        break
    while 1:
        try:
            mob=int(input("Guest Mob. # : "))
        except:
            print()
            print("Invalid Entry, Try Again.")
            print()
            continue
        break
    addr=input("Guest Address : ")
    while 1:
        try:
            checkindate=datetime.strptime(input("Check In Date : "), "%d/%m/%Y")
        except:
            print()
            print("Invalid Entry, Try Again.")
            print()
            continue
        break
    while 1:
        try:
            staydays=int(input("# of Days of Stay : "))
        except:
            print()
            print("Invalid Entry, Try Again.")
            print()
            continue
        break
    while 1:
        try:
            roomtype=int(input("Room Type (1-Single DX, 2-Double DX, 3-Single AC, 4-Double AC, 5-Single NAC, 6-Double NAC) : "))
        except:
            print()
            print("Invalid Entry, Try Again.")
            print()
            continue
        break
    checkoutdate=(checkindate + timedelta(days=staydays)).strftime("%d/%M/%Y")
    checkindate=checkindate.strftime("%d/%M/%Y")
    roomnumber=random.randint(0,100)
    if roomtype==1:
        roomcharges=1200
        roomtype="Single DX"
    elif roomtype==2:
        roomcharges=1700
        roomtype="Double DX"
    elif roomtype==3:
        roomcharges=1000
        roomtype="Single AC"
    elif roomtype==4:
        roomcharges=1300
        roomtype="Double AC"
    elif roomtype==5:
        roomcharges=600
        roomtype="Single NAC"
    elif roomtype==6:
        roomcharges=850
        roomtype="Double NAC"
    servicecharges=0
    rec=[name,addr,tel,mob,checkindate,staydays,checkoutdate,roomtype,roomnumber,roomcharges,servicecharges]
    pickle.dump(rec,f)
    print(rec)
    f.close()
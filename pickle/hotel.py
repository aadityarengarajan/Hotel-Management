#Name, Address, Telephone, Mobile, Check In, Stays, Check Out, Room Type, Room Number, Room Charges, Service Charges

import pickle   #the module for handling binary files a.k.a '.dat' files
import random   #a module for generating a random hotel room number
from datetime import datetime   #a function off a module for handling dates and times
from datetime import timedelta  #a function off a module for calculating dates and times

THE_FILE='accounts.dat'  #a constant referring to the file

def guestdetails(roomno):  #to diplay the info of a customer
    f=open(THE_FILE,'rb') #opening the file to read new data
    found=0 #a variable/flag to check if the guest exists or not
    while True: #forever ; an infinite loop
        try: #to prevent the end of file error while reading the binary file
            rec=pickle.load(f) #reading recordwise
            roomnumber=rec[8]
            servicecharges=rec[10]
            if roomno==roomnumber: #if this record is the desired guest's information
                found=1 #setting the flag so it doesn't return "guest not found"
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
    f=open(THE_FILE,'ab') #opening the file to append new data
    #inputting data
    name=input("Guest Name:")
    while 1: #in an infinite loop for data validation
        try:
            tel=int(input("Guest Tel. # : "))
        except:
            print()
            print("Invalid Entry, Try Again.")
            print()
            continue
        break

    while 1: #in an infinite loop for data validation
        try:
            mob=int(input("Guest Mob. # : "))
        except:
            print()
            print("Invalid Entry, Try Again.")
            print()
            continue
        break
    
    addr=input("Guest Address : ")

    while 1: #in an infinite loop for data validation
        try:
            checkindate=datetime.strptime(input("Check In Date : "), "%d/%m/%Y")
        except:
            print()
            print("Invalid Entry, Try Again.")
            print()
            continue
        break
    
    while 1: #in an infinite loop for data validation
        try:
            staydays=int(input("# of Days of Stay : "))
        except:
            print()
            print("Invalid Entry, Try Again.")
            print()
            continue
        break
    
    while 1: #in an infinite loop for data validation
        try:
            roomtype=int(input("Room Type (1-Single DX, 2-Double DX, 3-Single AC, 4-Double AC, 5-Single NAC, 6-Double NAC) : "))
        except:
            print()
            print("Invalid Entry, Try Again.")
            print()
            continue
        break

    checkoutdate=(checkindate + timedelta(days=staydays)).strftime("%d/%M/%Y") #calculating the checkout date based on stay duration, 'strftime' converts it into a string from a datetime object which it was because we were using that module
    checkindate=checkindate.strftime("%d/%M/%Y") #converting the check in date to a string from a datetime object which it was because we were using that module
    roomnumber=random.randint(0,100) #random room number from random module
    #now we decide charges based on room type
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
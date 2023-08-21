# This is a sample Python script.

# Press Maj+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

import time
import hashlib
import os
import sys
from multiprocessing import Process

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


def PrintElaspedTime(elapsed):
    response=""
    day=int(elapsed / (60*60*24))
    remain=elapsed-day*60*60*24
    hour=int(remain/(60*60))
    remain = remain-hour*60*60
    minut=int(remain/60)
    remain = remain-minut*60
    #print ("*** DEBUG *** day="+str(day)+" ; h="+str(hour)+" ; min="+str(minut)+"; s="+str(remain))
    if day>0: response=response+str(day)+" day(s)"
    if hour>0: response = response + " "+ str(hour) + " h"
    if minut > 0: response = response + " "+ str(minut) + " mn"
    if remain > 0: response = response + " "+ str(round(remain)) + " s"
    return response


def getPourcent(base, current):
    return str(round(current*100/base))

def getElaspedTime(_start, _end):
    #return "Elapsed time (s) : "+str(round(_end - _start, 1))
    return "Elapsed time : " + PrintElaspedTime(_end-_start)

# *************************
# *** streamHash(fname) ***
# *************************
def streamHash(fname,_count,_total):
    fileSize=getFileSize(fname)
    print("Hashing file {}/{} : ".format(_count,_total)+fname + " (" + printFileSize(fname) + ") ")
    Count=1
    sha = hashlib.sha256()
    with open(fname, 'rb') as r_file:
        file_buffer = r_file.read(BLOCKSIZE)
        while len(file_buffer) > 0:
            sha.update(file_buffer)
            if fileSize > THRESOLD:
                print(getPourcent(fileSize/BLOCKSIZE,Count)+" %",end="")
                sys.stdout.write('\b\b\b\b\b')
                Count=Count+1
                #print("DEBUG Count=" + str(Count))
            file_buffer = r_file.read(BLOCKSIZE)
    if fileSize > THRESOLD:
        sys.stdout.write('\b\b\b\b\b')
    return sha.hexdigest()


# ***********************
# *** fileSize(fname) ***
# ***********************
def getFileSize(fname):
    return os.stat(fname).st_size

def printFileSize(fname):
    size=getFileSize(fname)
    s_unit="Bytes"
    if size>1024:
        size=size / 1024
        s_unit = "ko"
    if size>1024:
        size=size / 1024
        s_unit = "mo"
    if size>1024:
        size=size / 1024
        s_unit = "go"
    #return f'{}'  round(size,1) + " " + s_unit
    return f'{round(size, 1)} ' + s_unit


# **************************
# *** check_dir(dirname) ***
# **************************
def list_dirContent(dirname):
    print("Listing Content of "+dirname)
    for file_path in os.listdir(dirname):
        full_filename=os.path.join(dirname,file_path)
        if os.path.isfile(full_filename):
            if file_path not in exclude_list:
                fileList.append(full_filename)
        if os.path.isdir(full_filename) and recursive_flag:
            list_dirContent(full_filename)
            

def showCorrectSyntax():
    print('SYNTAX ERROR - correct syntax is : mail.py {-a} {-r} [directory_name]')
    print('[] = mandatory ; {} = optional - order not important')
    print('-a = append outputfile if it exists (it will be created if not exist) - if output file exists and append option if off then the program will exit with error msg')
    print('-r = recursive')


def fillFileListFromOutputFile(outfname):
    file1 = open(outfname, 'r',encoding="utf-8")
    Lines = file1.readlines()
    # Strips the newline character
    for line in Lines:
        lineSplit=line.split(";")
        alreadyDoneList.append(lineSplit[0])


################
## les variables
################
BLOCKSIZE = 65536
start=time.time()
THRESOLD=1024*1024*350 #350 mo
fileList=[]
alreadyDoneList=[]
exclude_list=["Thumbs.db"]
recursive_flag=False
append_flag=False
ouput_filename=os.path.join(os.path.dirname(sys.argv[0]),"sha256_output.txt")
_dirname=""

#if __name__ == '__main__':
if len(sys.argv) < 2:
    showCorrectSyntax()
    exit(1)

i=1
while i < len(sys.argv):
    if os.path.isdir(sys.argv[i]):
        _dirname=sys.argv[i]
    if sys.argv[i] == '-a':
        append_flag = True
    if sys.argv[i] == '-r':
        recursive_flag = True
    i=i+1

if not os.path.isdir(_dirname):
    showCorrectSyntax()
    exit(2)

if os.path.isfile(ouput_filename):
   if append_flag:
       fillFileListFromOutputFile(ouput_filename)
       ouput_file = open(ouput_filename, 'a', encoding="utf-8")
   else:
       print ("ERROR - append option is false and outputfile exists : ",ouput_filename)
       exit (0)
else:
    ouput_file=open(ouput_filename,'w',encoding="utf-8")


#print ('recursive_flag =  ',recursive_flag)
#print ('append_flag =  ',append_Flag)
#print ('_dirname =  ',_dirname)


list_dirContent(_dirname)
count=0
total=len(fileList)

for fname in fileList:
    count+=1
    if fname not in alreadyDoneList:
        fhash=streamHash(fname,count,total)
        print(fname+";"+fhash,file=ouput_file)
        #print("     ")
    else:
        print (fname+" already done")


ouput_file.close()

print ('Total Files : ',len(fileList))
print ('recursive_flag =  ',recursive_flag)
print ('append_flag    =  ',append_flag)
print ("Output file is "+ouput_filename)
print (getElaspedTime(start, time.time()))



# Press the green button in the gutter to run the script.
#if __name__ == '__main__':
#    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/

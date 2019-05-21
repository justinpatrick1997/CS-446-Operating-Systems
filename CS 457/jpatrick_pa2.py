"""
Author: Justin Patrick
Class: CS 457
Project: Database v2
Date: 3/14/2019
"""

import os
from shutil import rmtree
import re

scopeDir = ""
wrkDir = ""

#Function createDB creates the user specified database and error checks as necessary
def createDB(qb):
    #creating database dir if not already created
    try:
        #storing string that comes after 'create database'
        dir = qb.split("CREATE DATABASE ")[1]
        #checking if specified database exist
        if os.path.exists(dir):
            print "!Failed to create database " + dir + " because it already exists."
        else:
            #creating specified database
            os.makedirs(dir)
            print "Database " + dir + " created."
    except IndexError:
            print "!No database name specified"

#Function dropDB deletes the user specified database and error checks
def dropDB(qb):
    #deleting database dir unless it does not exist
    try:
        #storing string that comes after 'drop database'
        dir = qb.split("DROP DATABASE ")[1]
        #ensure specified database exists
        if os.path.exists(dir):
             rmtree(dir)
             print "Database " + dir + " deleted."
        else:
             print "!Failed to delete database " + dir + " because it does not exist."
    except IndexError:
        print "!No database name specified"

#Function createDB creates the user specified table and error checks
def createTB(qb):
    try:
        #check if we are in correct dir
        correctDB()
        #getting string after create table
        subDir = qb.split("CREATE TABLE ")[1]
        #parsing for passed
        subDir = subDir.split(" (")[0].lower()
        psFile = os.path.join(wrkDir, subDir)
        #print [subDir, psFile, wrkDir]

        if not os.path.isfile(psFile):
            #to create table this will use files which act as tables
            with open(psFile, "w") as TB:
                print "Table " + subDir + " created."
                #start of arg
                if "(" in qb:
                    #creating oList to load & send to file
                    oList = []
                    #remove the (
                    data = qb.split("(",1)[1]
                    #remove the )
                    data = data[:-1]
                    #in data replace the , with |
                    data = data.replace(", " , " | ")
                    #writing user specified data in to user created table
                    TB.write(data)
        else:
            raise ValueError("!Failed to create table " + subDir + " because it already exists.")
    except IndexError:
        print "!Failed to remove table because no table name is specified"
    except ValueError as err:
        print err.args[0]

#Function dropTB deletes the user specified table and error checks as necessary
def dropTB(qb):
    try:
        #check if we are in correct dir
        correctDB()
        #getting string after DROP TABLE
        subDir = qb.split("DROP TABLE ")[1]
        #finding table
        userTB = os.path.join(wrkDir, subDir)
        #checking if table is correct
        if os.path.isfile(userTB):
            #removing table
            os.remove(userTB)
            print "Table " + subDir + " deleted."
        else:
            raise ValueError("!Failed to delete table " + subDir + " because it does not exist.")
    except IndexError:
        print "!Failed to remove table because no table name specified"
    except ValueError as err:
        print err.args[0]

#Funtion insertDt allows users to insert data in to the database
def insertDt(qb):
    try:
        correctDB()
        usrTB = qb.split(" ")[2].lower()
        usrFL = os.path.join(wrkDir, usrTB)
        if os.path.isfile(usrFL):
            if "values" in qb:
                with open(usrFL, "a") as table:
                    out = []
                    dt = qb.split("(", 1)[1]
                    dt = dt[:-1]
                    counter = dt.count(",")
                    for x in range(counter + 1):
                        out.append(dt.split(",")[x].lstrip())
                        if "\"" == out[x][0] or "\'" == out[x][0]:
                            out[x] = out[x][1:-1]
                    table.write("\n")
                    table.write(" | ".join(out))
                    print "1 new record inserted."
            else:
                print "!Failed to insert into " + usrTB + " because there were no specified arguments"
        else:
            print "!Failed to alter table " + usrTB + " because it does not exist"
    except IndexError:
        print "!Failed to insert into table becasue no table name is specified"
    except ValueError as err:
        print err.args[0]

#Function alterTB alters the user table specified and error checks as necessary
def alterTB(qb):
    try:
        #check if we are in correct dir
        correctDB()
        #getting string after ALTER TABLE
        userTB = qb.split("ALTER TABLE ")[1]
        userTB = userTB.split(" ")[0]
        myFile = os.path.join(wrkDir, userTB)
        #checking if myFile is file
        if os.path.isfile(myFile):
            #checking for add
            if "ADD" in qb:
                #using a to append to end of file
                with open(myFile, "a") as TB:
                    newStr = qb.split("ADD ")[1]
                    #write new data to table
                    TB.write(", " + newStr)
                    print "Table " + userTB + " modified."
        else:
            raise ValueError("!Failed to alter table " + userTB + " because it does not exist.")
    except IndexError:
        print "!Failed to remoe table because no table name specified"
    except ValueError as err:
        print err.args[0]


#Function selectStar will query the user specified table and error check as necessary
def selectStar(qb, qbPD):
    try:
        #check if we are in correct dir
        correctDB()
        #stringing user specified table
        usrTB = re.split("FROM ", qb, flags=re.IGNORECASE)[1].lower()
        if "WHERE" in qbPD:
            usrTB = re.split("WHERE", usrTB, flags=re.IGNORECASE)[0]
            if " " in usrTB:
                usrTB = usrTB.split(" ")[0]
        usrFL = os.path.join(wrkDir, usrTB)
        output = ""
        if os.path.isfile(usrFL):
            with open(usrFL, "r+") as table:
                if "WHERE" in qbPD:
                    srchD = re.split("WHERE ", qb, flags=re.IGNORECASE)[1]
                    dt = table.readlines()
                    counter, output = where(srchD, "select", dt)
                    #for line in output:

                if "SELECT *" in qbPD:
                    if not output == "":
                        for line in output:
                            print line
                    else:
                        output += table.read()
                        print output
                else:
                    myArgs = re.split("SELECT", qb, flags=re.IGNORECASE)[1]
                    attributes = re.split("FROM", myArgs, flags=re.IGNORECASE)[0]
                    attributes = attributes.split(",")
                    if not output == "":
                        lines = output
                    else:
                        lines = table.readlines()
                        dt = lines
                    for line in lines:
                        out = []

                        for attribute in attributes:
                            attribute = attribute.strip()
                            colIndice = getCol(dt)
                            if attribute in colIndice:
                                detachLine = detach(line)
                                out.append(detachLine[colIndice.index(attribute)])
                        print " | ".join(out)
        else:
            print "!Failed to query table " + usrTB + " because it does not exist"
    except IndexError:
        print "!Failed to select because no table name is specified"
    except ValueError as err:
        print err.args[0]

#Function updateFrom allows for user updates
def updateFrom(qb):
    try:
        correctDB()
        myTB = re.split("UPDATE ", qb, flags=re.IGNORECASE)[1]
        myTB = re.split("SET", myTB, flags=re.IGNORECASE)[0].lower().strip()
        myFL = os.path.join(wrkDir, myTB)
        if os.path.isfile(myFL):
            with open(myFL, "r+") as table:
                dt = table.readlines()
                usrUP = re.split("WHERE ", qb, flags=re.IGNORECASE)[1]
                num = re.split("SET ", qb, flags=re.IGNORECASE)[1]
                num = re.split("WHERE ", num, flags=re.IGNORECASE)[0]
                counter, out = where(usrUP, "update", dt, num)
                table.seek(0)
                table.truncate()
                for line in out:
                    if not "\n" in line:
                        line += "\n"
                    table.write(line)
                if counter > 0:
                    print counter, " records modified."
                elif counter == 1:
                    print counter, " record modified."
                else:
                    print "No records modified."
        else:
            print "!Failed to update table " + myTB + " because it does not exist"
    except IndexError:
        print "!Failed to update table because no table name is specified"
    except ValueError as err:
        print err.args[0]

#Function useMe will use the user specified database and error checks as necessary
def useMe(qb):
    try:
        global scopeDir
        #placing database in userDB
        scopeDir = qb.split("USE ")[1]
        #as long as database userDB exists we are now using userDB
        if os.path.exists(scopeDir):
            print "Using database " + scopeDir + " ."
        else:
            raise ValueError("!Failed to use database because it does not exist.")
    except IndexError:
        print "!No database name specified"
    except ValueError:
        print err.args[0]

#Function getCol will find the column being referenced
def getCol(dt):
    colIndice =  dt[0].split(" | ")
    for x in range(len(colIndice)):
        colIndice[x] = colIndice[x].split(" ")[0]
    return colIndice

#Function detach will separate desired columns
def detach(line):
    lineT = line.split(" | ")
    for x in range(len(lineT)):
        lineT[x] = lineT[x].split(" ")[0]
    return lineT

#Function correctDB ensuring the we are in the correct dir
def correctDB():
    if scopeDir is "":
        raise ValueError("!No database selected")
    else:
        global wrkDir
        wrkDir = os.path.join(os.getcwd(), scopeDir)

#Function where function to select specific fields of data from the database
def where(findArg, choice, dt, upVal = ""):
    counter = 0
    colIndice = getCol(dt)
    nwName = colIndice
    passD = list(dt)
    out = []
    flag = 0
    if "=" in findArg:
        if "!=" in findArg:
            riCol = findArg.split(" !=")[0]
            flag = 1
        else:
            riCol = findArg.split(" =")[0]

        findArg = findArg.split("= ")[1]
        if "\"" in findArg or "\'" in findArg:
            findArg = findArg[1:-1]
        for line in dt:
            lineT = detach(line)
            if findArg in lineT:
                colIndice = nwName.index(riCol)
                lineIndice = lineT.index(findArg)
                if lineIndice == colIndice:
                    if choice == "delete":
                        del passD[passD.index(line)]
                        out = passD
                        counter += 1
                    if choice == "select":
                        out.append(passD[passD.index(line)])
                    if choice == "update":
                        attribute, field = upVal.split(" = ")
                        if attribute in nwName:
                            nwLine = detach(line)
                            nwLine[nwName.index(attribute)] = field.strip().strip("'")
                            passD[passD.index(line)] = ' | '.join(nwLine)
                            out = passD
                            counter += 1
    elif ">" in findArg:
        riCol = findArg.split(" >")[0]
        findArg = findArg.split("> ")[1]
        for line in dt:
            lineT = line.split(" | ")
            for x in range(len(lineT)):
                lineT[x] = lineT[x].split(" ")[0]
                try:
                    lineT[x] = float(lineT[x])
                    if lineT[x] > float(findArg):
                        tCol = colIndice.index(riCol)
                        if x == tCol:
                            if choice == "delete":
                                del passD[passD.index(line)]
                                out = passD
                                counter += 1
                            if choice == "select":
                                out.append(passD[passD.index(line)])
                            if choice == "update":
                                print " "
                except ValueError:
                    continue
    if flag:
        out = list(set(dt) - set(out))
    return counter, out

#Function deleteFrom allows for specific entry deletion
def deleteFrom(qb):
    try:
        correctDB()
        myTbl = re.split("DELETE FROM ", qb, flags=re.IGNORECASE)[1]
        myTbl = myTbl.split(" ")[0].lower()
        myFile = os.path.join(wrkDir, myTbl)
        if os.path.isfile(myFile):
            with open(myFile, "r+") as table:
                dt = table.readlines()
                toDel = re.split("WHERE ", qb, flags = re.IGNORECASE)[1]
                counter, out = where(toDel, "delete", dt)
                table.seek(0)
                table.truncate()
                for line in out:
                    table.write(line)
                if counter > 1:
                    print counter, " records deleted."
                elif counter == 1:
                    print counter, " record deleted."
                else:
                    print "No records deleted."
        else:
            print "!Failed to delete table " + myTbl + " because it does not exist"
    except IndexError:
        print "!Failedd to delete table because no table name is specified"
    except ValueError as err:
        print err.args[0]

#Main function running a simple interface for creating user specified databases
def main():
    try:
        #per instructions
        print "\n"
        while True:
            cmd = ""

            #per instructions dont parse lines with --
            while not ";" in cmd and not "--" in cmd:
                cmd += raw_input()

            #parsing command from test file
            cmd = cmd.split(";")[0]
            cmdStr = str(cmd)
            cmdStr = cmdStr.upper()

            #pass lines with --
            if "--" in cmd:
                pass
            #call createDB if CREATE DATABASE is found
            elif "CREATE DATABASE" in cmdStr:
                createDB(cmd)
            #call dropDB if DELETE DATABASE is found
            elif "DROP DATABASE" in cmdStr:
                dropDB(cmd)
            #call createTB if CREATE TABLE is found
            elif "CREATE TABLE" in cmdStr:
                createTB(cmd)
            #call dropTB if DELETE TABLE is found
            elif "DROP TABLE" in cmdStr:
                dropTB(cmd)
            #call alterTB if ALTER TABLE is found
            elif "ALTER TABLE" in cmdStr:
                alterTB(cmd)
            #call selectStar if SELECT * is found
            elif "SELECT" in cmdStr:
                selectStar(cmd, cmdStr)
            #call useMe if USE is found
            elif "USE" in cmdStr:
                useMe(cmd)
            #call updateFrom if UPDATE is found
            elif "UPDATE" in cmdStr:
                updateFrom(cmd)
            #call inserDt if INSERT INTO is found
            elif "INSERT INTO" in cmdStr:
                insertDt(cmd)
            #call deleteFrom if DELETE FROM is found
            elif "DELETE FROM" in cmdStr:
                deleteFrom(cmd)
            #exit if .EXIT is found
            elif ".EXIT" in cmdStr:
                print "All done."
                exit()


    except (EOFError, KeyboardInterrupt) as e:
        print "All done.\n"
        exit()

if __name__ == '__main__':
    main()

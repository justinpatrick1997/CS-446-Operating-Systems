"""
Author: Justin Patrick
Class: CS 457
Project: database v4
Date: 5/2/19
"""

import os, re
from contextlib import contextmanager
from shutil import rmtree
scopeDir = ""
wrkDir = ""

# called so multiple files can be managed
@contextmanager
# Function fileMngr opens multiple files and closes them all
def fileMngr(files, mode='rt'):
    files = [open(file, mode) for file in files]
    yield files
    for file in files:
        file.close()

# Function correctDB ensuring the we are in the correct dir
def correctDB():
    if scopeDir is "":
        raise ValueError("!No database selected")
    else:
        global wrkDir
        wrkDir = os.path.join(os.getcwd(), scopeDir)

# Function getCol will find the column being referenced
def getCol(dt):
    colIndice = dt.split(" | ")
    for x in range(len(colIndice)):
        colIndice[x] = colIndice[x].split(" ")[0]
    return colIndice

# Function detach will separate desired columns
def detach(line):
    lineT = line.split(" | ")
    for x in range(len(lineT)):
        lineT[x] = lineT[x].split(" ")[0]
    return lineT

# Function joinWhere implements join functionality for user passed tables
def joinWhere(findArg, tbVars, dtArr, joinType = 'inner'):
    counter = 0
    out = []
    flag = 0
    num_tables = len(dtArr)
    tinder = []
    emptyCols = ""

    #Collect column dt in array and see if it matches
    if "=" in findArg:  #Operator evaluation
        if "!=" in findArg:
            r_col = findArg.split(" !=")[0]
        else:
            searchL = findArg.split(" =")[0]
            searchL = searchL.split(".")[1]
            searchR = findArg.split("= ")[1]
            searchR = searchR.split(".")[1]
    if num_tables == 2:
        tbL = dtArr[0]
        tbR = dtArr[1]
    else:
        print "!join only accepts two tables"
        return -1, -1

    dtL = []
    dtR = []
    colL = getCol(tbL[0])
    colR = getCol(tbR[0])

    for line in tbL:

        lineSplit = detach(line)
        dtL.append(lineSplit[colL.index(searchL)])
    for line in tbR:
        lineSplit = detach(line)
        dtR.append(lineSplit[colR.index(searchR)])

    for x in range(len(dtL)):
        for y in range(len(dtR)):
            if dtL[x] == dtR[y]:
                tbR[y] = tbR[y].strip('\n')
                tbL[x] = tbL[x].strip('\n')
                out.append(tbL[x] + ' | ' + tbR[y])
                counter += 1
                if joinType == 'left':
                    tinder.append(tbL[x])

    if joinType == 'left':
        nums = len(colR)
        for x in range(nums):
            emptyCols += ' | '
        for x in range(len(dtL)):
            if not colL[0] in tbL[x]:
                if not tbL[x] in tinder:
                    out.append(tbL[x].strip('\n') + emptyCols )
                    counter += 1
    return counter, out


# Function alterTB alters the user table specified and error checks as necessary
def alterTB(qb):
    try:
        # check if we are in correct dir
        correctDB()
        # getting string after ALTER TABLE
        userTB = qb.split("ALTER TABLE ")[1]
        userTB = userTB.split(" ")[0].lower()
        myFile = os.path.join(wrkDir, userTB)
        # checking if myFile is file
        if os.path.isfile(myFile):
            # checking for add
            if "ADD" in qb:
                # using a to append to end of file
                with open(myFile, "a") as table:
                    newStr = qb.split("ADD ")[1]
                    # write new data to table
                    table.write("|" + newStr)
                    print "Table " + userTB + " modified."
        else:
            raise ValueError("!Failed to alter table " + userTB + " because it does not exist.")
    except IndexError:
        print "!Failed to remoe table because no table name specified"
    except ValueError as err:
        print err.args[0]


# Function createDB creates the user specified database and error checks as necessary
def createDB(qb):
    # creating database dir if not already created
    try:
        # storing string that comes after 'create database'
        dir = qb.split("CREATE DATABASE ")[1]
        # checking if specified database exist
        if os.path.exists(dir):
            print "!Failed to create database " + dir + " because it already exists."
        else:
            # creating specified database
            os.makedirs(dir)
            print "Database " + dir + " created."
    except IndexError:
        print "!No database name specified"


# Function createDB creates the user specified table and error checks
def createTB(qb):
    try:
        # check if we are in correct dir
        correctDB()
        # getting string after create table
        # parsing for passed
        subDir = " ".join(qb.split(" ")[2:])
        subDir = subDir.split("(", 1)[0]
        psFile = os.path.join(wrkDir, subDir)
        # print [subDir, psFile, wrkDir]

        if not os.path.isfile(psFile):
            # to create table this will use files which act as tables
            with open(psFile, "w") as table:
                print "Table " + subDir + " created."
                # start of arg
                if "(" in qb:
                    out = []
                    data = qb.split("(", 1)[1]
                    data = data[:-1]
                    counter = data.count(",")
                    for x in range(counter + 1):
                        out.append(data.split(", ")[x])
                    table.write(" | ".join(out))
        else:
            raise ValueError("!Failed to create table " + subDir + " because it already exists.")
    except IndexError:
        print "!Failed to remove table because no table name is specified"
    except ValueError as err:
        print err.args[0]

# Function deleteFrom allows for specific entry deletion
def deleteFrom(qb):
    try:
        correctDB()
        myTbl = re.split("DELETE FROM ", qb, flags=re.IGNORECASE)[1]
        myTbl = myTbl.split(" ")[0].lower()
        myFile = os.path.join(wrkDir, myTbl)
        if os.path.isfile(myFile):
            with open(myFile, "r+") as table:
                dt = table.readlines()
                toDel = re.split("WHERE ", qb, flags=re.IGNORECASE)[1]
                counter, out = where(toDel, "delete", dt)
                table.seek(0)
                table.truncate()
                for line in out:
                    table.write(line)
                if counter > 0:
                    print counter, " records deleted."
                else:
                    print "No records deleted."
        else:
            print "!Failed to delete table " + myTbl + " because it does not exist"
    except IndexError:
        print "!Failedd to delete table because no table name is specified"
    except ValueError as err:
        print err.args[0]

# Function dropDB deletes the user specified database and error checks
def dropDB(qb):
    # deleting database dir unless it does not exist
    try:
        # storing string that comes after 'drop database'
        dir = qb.split("DROP DATABASE ")[1]
        # ensure specified database exists
        if os.path.exists(dir):
            from shutil import rmtree
            rmtree(dir)
            print "Database " + dir + " deleted."
        else:
            print "!Failed to delete database " + dir + " because it does not exist."
    except IndexError:
        print "!No database name specified"

# Function dropTB deletes the user specified table and error checks as necessary
def dropTB(qb):
    try:
        # check if we are in correct dir
        correctDB()
        # getting string after DROP TABLE
        subDir = " ".join(qb.split(" ")[2:])
        subDir = subDir.split("(", 1)[0]
        # finding table
        userTB = os.path.join(wrkDir, subDir)
        # checking if table is correct
        if os.path.isfile(userTB):
            # removing table
            os.remove(userTB)
            print "Table " + subDir + " deleted."
        else:
            raise ValueError("!Failed to delete table " + subDir + " because it does not exist.")
    except IndexError:
        print "!Failed to remove table because no table name specified"
    except ValueError as err:
        print err.args[0]

# Function joinOn assists with join functionality
def joinOn(qb,qbPD):
    toJoinOn = re.split("on", qb, flags=re.IGNORECASE)[1]

    if "INNER" in qbPD:
        return joinWhere(searchItem, tbVars, dtArr)

    if "OUTTER" in qbPD:
        if "LEFT" in qbPD:
            counter, out = where(toJoinOn, "SELECT", dt)
            for line in data:
                for tinder in out:
                    print " "
        elif "RIGHT" in qbPD:
            counter, out = where(toJoinOn, "SELECT", dt)

# Function updateFrom allows for user updates
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
                else:
                    print "No records modified."
        else:
            print "!Failed to update table " + myTB + " because it does not exist"
    except IndexError:
        print "!Failed to update table because no table name is specified"
    except ValueError as err:
        print err.args[0]

# Function useMe will use the user specified database and error checks as necessary
def useMe(qb):
    try:
        global scopeDir
        # placing database in userDB
        scopeDir = qb.split("USE ")[1]
        # as long as database userDB exists we are now using userDB
        if os.path.exists(scopeDir):
            print "Using database " + scopeDir + " ."
        else:
            raise ValueError("!Failed to use database because it does not exist.")
    except IndexError:
        print "!No database name specified"
    except ValueError as err:
        print err.args[0]

#Function where assists with where table parsing functionality
def where(findArg, choice, dt, upVal=""):
    counter = 0
    colIndex =getCol(dt)
    attr_name = colIndex
    inputdt = list(dt)
    out = []
    flag = 0
    if "=" in findArg:  #Figure out the operator for splitting up the input
        if "!=" in findArg:
            r_col = findArg.split(" !=")[0]
            flag = 1
        else:
            r_col = findArg.split(" =")[0]

            findArg = findArg.split("= ")[1]
        if "\"" in findArg or "\'" in findArg: #Cleanup var
            findArg = findArg[1:-1]
        for line in dt:
            line_test = detach(line)
            if findArg in line_test:
                colIndex = attr_name.index(r_col)
                line_index = line_test.index(findArg)
                if line_index == colIndex:
                    if choice == "delete":
                        del inputdt[inputdt.index(line)]
                        out = inputdt
                        counter += 1
                    if choice == "select":
                        out.append(inputdt[inputdt.index(line)])
                    if choice == "update":
                        attribute, field = upVal.split(" = ")
                        if attribute in attr_name:
                            sep_line = detach(line)
                            sep_line[attr_name.index(attribute)] = field.strip().strip("'")
                            inputdt[inputdt.index(line)] = ' | '.join(sep_line)
                            out = inputdt
                            counter += 1

    elif ">" in findArg:  # Evaluate operator
        r_col = findArg.split(" >")[0]
        findArg = findArg.split("> ")[1]
        for line in dt:
            line_test = line.split(" | ")
            for x in range(len(line_test)):  #Evaluate each column item
                line_test[x] = line_test[x].split(" ")[0]
                try:
                    line_test[x] = float(line_test[x])  #Check value
                    if line_test[x] > float(findArg):
                        temp_col = colIndex.index(r_col)
                        if x == temp_col:  # Check for column
                            if choice == "delete":
                                del inputdt[inputdt.index(line)]  #Remove matching field
                                out = inputdt
                                counter += 1
                            if choice == "select":
                                out.append(inputdt[inputdt.index(line)])
                            if choice == "update":
                                print "hi"
                except ValueError:
                    continue
    if flag:
        out = list(set(dt) - set(out))
    return counter, out


# Funtion insertDt allows users to insert data in to the database
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

# Function selectStar will allow users to query tables and manage files
def selectStar(qb, qbPD):
    try:
        tbVars = []
        files = []
        joinType = ""
        correctDB()
        (files, tbVars, joinType) = selectFuncs(files, tbVars, joinType, qbPD, qb);
        result = ""

        with fileMngr(files, "r+") as tables:
            dt = []
            dtArr = []
            if "JOIN" in qbPD:
                for table in tables:
                    dt = table.readlines()
                    dtArr.append(dt)
                toJoinOn = re.split("on", qb, flags=re.IGNORECASE)[1]
                counter, result = joinWhere(toJoinOn, tbVars, dtArr, joinType)
            # Using the WHERE to find the matches with all attributes
            elif "WHERE" in qbPD:
                searchItem = re.split("WHERE ", qb, flags=re.IGNORECASE)[1]
                counter = 0
                if len(tables) == 1:  # Typical where behavior
                    dt = tables[0].readlines()
                    counter, result = where(searchItem, "select", dt)
                else:  # Implicit inner join
                    for table in tables:
                        dt = table.readlines()
                        dtArr.append(dt)
                        counter += 1
                    counter, result = joinWhere(searchItem, tbVars, dtArr)

            if "SELECT *" in qbPD:
                print dtArr[0][0].strip('\n') + " | " + dt[0].strip('\n')
                # Checks if the result is allocated from WHERE
                if not result == "":
                    for line in result:
                        print line
                # If there is no restriction from WHERE print all
                else:
                    for table in tables:
                        result += table.read()
                    print result

            # If doesnt want all attributes, trim down result
            else:
                arguments = re.split("SELECT", qb, flags=re.IGNORECASE)[1]
                attributes = re.split("FROM", arguments, flags=re.IGNORECASE)[0]
                attributes = attributes.split(",")
                if not result == "":  # Checks if the result is allocated
                    lines = result
                else:
                    lines = table.readlines()
                    dt = lines
                for line in lines:
                    out = []
                    for attribute in attributes:
                        attribute = attribute.strip()
                        colIndice = getCol(dt)
                        if attribute in colIndice:
                            separatedLine = detach(line)
                            out.append(separatedLine[colIndice.index(attribute)].strip())
                    print "|".join(out)
    #    print "!Failed to query table " + tableName + " because it does not exist"
    except IndexError as e:
        print "!Failed to select because no table name is specified"
    except ValueError as err:
        print err.args[0]

# Function selectFuncs provides additional functionality for selectStar
def selectFuncs(files, tbVars, joinType, qb, cmd):
    tbArr = []
    tbFind = {}
    tables = []

    if "JOIN" in qb:
        outcut = re.split("FROM ", cmd, flags=re.IGNORECASE)[1]
        if "LEFT" in qb:
            tableL = re.split("LEFT", outcut, flags=re.IGNORECASE)[0].lower()
            tableR = re.split("JOIN ", outcut, flags=re.IGNORECASE)[1].lower()
            tableR = re.split("ON", tableR, flags=re.IGNORECASE)[0].strip()
            tableL = re.split(" ", tableL, flags=re.IGNORECASE)[0].strip()
            tableR = re.split(" ", tableR, flags=re.IGNORECASE)[0].strip()
            tbArr.append(tableL)
            tbArr.append(tableR)
            joinType = 'left'
        elif "INNER" in qb:
            tableL = re.split("INNER", outcut, flags=re.IGNORECASE)[0].lower()
            tableR = re.split("JOIN ", outcut, flags=re.IGNORECASE)[1].lower()
            tableR = re.split("ON", tableR, flags=re.IGNORECASE)[0].strip()
            tableL = re.split(" ", tableL, flags=re.IGNORECASE)[0].strip()
            tableR = re.split(" ", tableR, flags=re.IGNORECASE)[0].strip()
            tbArr.append(tableL)
            joinType = 'inner'
            tbArr.append(tableR)
        elif "RIGHT" in qb:
            tbArr = re.split("RIGHT", outcut, flags=re.IGNORECASE)[0].lower()
            tbArr = re.split("JOIN", outcut, flags=re.IGNORECASE)[1].lower()
            joinType = 'right'
    elif "WHERE" in qb:
        tables = re.split("FROM ", cmd, flags=re.IGNORECASE)[1].lower()
        tables = re.split("WHERE", tables, flags=re.IGNORECASE)[0]

    else:
        tables = re.split("FROM ", cmd, flags=re.IGNORECASE)[1].lower()
        if "," in tables:
            for table in re.split(", ", tables):
                tbArr.append(table)
        else:
            tbArr.append(tables)

    if " " in tables:
        tables = tables.strip("\r")
        tables = tables.strip()
    if "," in tables:
        for table in re.split(", ", tables):
            table, tableVariable = re.split(" ", table, flags=re.IGNORECASE)
            tbFind[tableVariable] = table
            tbArr.append(table)
            tbVars.append(tableVariable)
    for tableName in tbArr:
        if tableName:
            files.append(os.path.join(wrkDir, tableName))

    return files, tbVars, joinType

def transact(lkArr, lkFlag):
    try:
        myFile = ""
        fileArr = []
        correctDB()

        while True:
            cmd = ""

            while not ";" in cmd and not "--" in cmd:
                cmd += raw_input().strip('\r')

            if "commit;" in cmd:
                break

            cmd = cmd.split(";")[0]
            inputStr = str(cmd)
            lkArr.append(inputStr)

            if "UPDATE" in inputStr.upper():
                myTB = re.split("UPDATE ", lkArr[1], flags=re.IGNORECASE)[1]
                myTB = re.split("SET", myTB, flags=re.IGNORECASE)[0].lower().strip()
                myFile = myTB = ".lock"
                fileArr = os.listdir("./locks")
                lockArr[0] = myFile
                path = "./locks/" + fileName
                fIn = open(path, "w")
                fIn.close()
                lkFlag = 1

        if myFile in fileArr:
            print "Error: table", myFile, "is locked."
            return ["table"], 0
        return lkArr, lkFlag

    except IndexError:
        print "!Transaction error"
    except ValueErorr as err:
        print err.args[0]

# Main function running a simple interface for creating user specified databases
def main():
    lkArr = ["table"]
    lkFlag = 0
    lkIndex = 1

    try:
        if not os.path.exists("./locks"):
            os.makedirs("./locks")
        # per instructions
        print "\n"
        while True:
            cmd = ""
            if lkFlag is 1:
                if lkIndex is not len(lkArr):
                    cmd = lkArr[lkIndex]
                    lkIndex += 1
                else:
                    rm = "./locks/" + lockArray[0]
                    if os.path.isfile(rm):
                        os.remove(rm)
                    lkArr = ["table"]
                    lkIndex = 1
                    lkFlag = 0
            if lkFlag is not 1:
                # per instructions dont parse lines with --
                while not ";" in cmd and not "--" in cmd:
                    cmd += raw_input().strip('\r')

            # parsing command from test file
            cmd = cmd.split(";")[0]
            cmdStr = str(cmd)
            cmdStr = cmdStr.upper()

            # pass lines with --
            if "--" in cmd:
                pass
            # call to
            elif "BEGIN TRANSACTION" in cmdStr:
                lkArr, lkFlag = transact(lkArr, lkFlag)
            # call createDB if CREATE DATABASE is found
            elif "CREATE DATABASE" in cmdStr:
                createDB(cmd)
            # call dropDB if DELETE DATABASE is found
            elif "DROP DATABASE" in cmdStr:
                dropDB(cmd)
            # call createTB if CREATE TABLE is found
            elif "CREATE TABLE" in cmdStr:
                createTB(cmd)
            # call dropTB if DELETE TABLE is found
            elif "DROP TABLE" in cmdStr:
                dropTB(cmd)
            # call alterTB if ALTER TABLE is found
            elif "ALTER TABLE" in cmdStr:
                alterTB(cmd)
            # call selectStar if SELECT * is found
            elif "SELECT" in cmdStr:
                selectStar(cmd, cmdStr)
            # call useMe if USE is found
            elif "USE" in cmdStr:
                useMe(cmd)
            # call updateFrom if UPDATE is found
            elif "UPDATE" in cmdStr:
                updateFrom(cmd)
            # call inserDt if INSERT INTO is found
            elif "INSERT INTO" in cmdStr:
                insertDt(cmd)
            # call deleteFrom if DELETE FROM is found
            elif "DELETE FROM" in cmdStr:
                deleteFrom(cmd)
            # exit if .EXIT is found
            elif ".EXIT" in cmdStr:
                print "All done."
                exit()



    except (EOFError, KeyboardInterrupt) as e:
        print "All done.\n"
        exit()


if __name__ == '__main__':
    main()

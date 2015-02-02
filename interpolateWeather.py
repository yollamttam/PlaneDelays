import os
import numpy as np

origin = 'PHL'

sqlsettings={'usr':'matt', 'dba':'matts_stuff', 'outfile':'OriginData.txt','origin':origin}
os.system("""mysql -u {usr} {dba} -e "SELECT flightyear, flightmonth, dayofmonth, deptime, depdelay FROM flights WHERE origin = '{origin}';" > {outfile}""".format(**sqlsettings))

# sqlsettings={'usr':'matt', 'dba':'matts_stuff', 'outfile':'OriginData.txt'}
# os.system('mysql -u {usr} {dba} -e "SELECT originstate, AVG(depdelay15bool) FROM flights GROUP BY originstate;" > {outfile}'.format(**sqlsettings))



continueBool = 1
if continueBool:

    infile = open(sqlsettings['outfile'])
    infile.readline() # skip the header

    for line in infile.readlines():
    
        year, month, day, deptime, depdelay = line.strip().split('\t')
        year = float(year)
        month = float(month)
        day = float(day)
        deptime = float(deptime)
        depdelay = float(depdelay)

        minutes = deptime % 100
        hours = np.floor(deptime/100)
        totalminutes = hours*60.0 + minutes

        # reconstruct scheduled departure time
        if (depdelay >= 0):
            # subtract departure depdelay from deptime
            # careful though because this is a time format
            
            totalminutes = totalminutes - depdelay
            hours = np.floor(totalminutes/60)
            minutes = totalminute % 60

        # create sql query to get temporally-neighboring weather data
        sqlsettings={'usr':'matt', 'dba':'matts_stuff', 'outfile':'OriginData.txt','origin':origin,'hours':hours,'minutes':minutes,'year':year,'month':month,'day':day,'totalm':totalminutes}

        cmd = """mysql -u {usr} {dba} -e "SELECT HOUR(DATES), MINUTE(DATES) FROM weather WHERE YEAR(DATES)={year} AND MONTH(DATES)={month} AND DAY(DATES)={day} ORDER BY ABS(60*HOUR(DATES)+MINUTE(DATES)-{totalm}) limit 6;" > {outfile}""".format(**sqlsettings)
        print cmd

        os.system(cmd)

        input('press return to end, this is just a test')
        

    infile.close()

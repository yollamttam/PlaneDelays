import os
import glob

sqlsettings={'usr':'matt', 'dba':'matts_stuff', 'outfile':'airportWeatherStations.txt'} 

# drop weather table if it exists already
print "dropping flights table if it exists already..."
os.system("""mysql -u {usr} {dba} -e "drop table if exists flights;" """.format(**sqlsettings))
# Create the weather table that you're going to load all the weather data into
print "creating our own flight table, with hookers and delay data..."
os.system("""mysql -u {usr} {dba} -e "CREATE TABLE flights (flightyear SMALLINT, flightmonth SMALLINT, dayofmonth SMALLINT, dayofweek SMALLINT, flightdate DATE, carrierID VARCHAR(10), flightnumber MEDIUMINT, originairport MEDIUMINT, origincityMID MEDIUMINT, origin VARCHAR(10), origincitystate VARCHAR(255) ENCLOSED BY '"', originstate VARCHAR(10), destairport MEDIUMINT, destcityMID MEDIUMINT, destination VARCHAR(10), destcitystate VARCHAR(255), deststate VARCHAR(10), deptime MEDIUMINT, depdelay FLOAT, depdelay15bool TINYINT, arrtime MEDIUMINT,arrdelay FLOAT, arrdelay15bool TINYINT, cancelledbool TINYINT, cancelcode VARCHAR(255), distance FLOAT, carrierdelay FLOAT, weatherdelay FLOAT, nasdelay FLOAT, securitydelay FLOAT, lateaircraftdelay FLOAT);" """.format(**sqlsettings))

continueBool = 0
# ok, so we probably want to just glob through all the files in the /tmp/FlightStatus directory...
filelist = glob.glob('/tmp/FlightData/*.csv')
nfiles = len(filelist)
for i in range(nfiles):
    filename = filelist[i]
    sqlsettings={'usr':'matt', 'dba':'matts_stuff', 'outfile':filename}
    os.system("""mysql -u {usr} {dba} -e "load data infile '{outfile}' into table
flights fields terminated by ',' ignore 1 lines (flightyear, flightmonth, dayofmonth, dayofweek, flightdate, carrierID, flightnumber, originairport, origincityMID, origin, origincitystate, originstate, destairport, destcityMID, destination, destcitystate, deststate, deptime, depdelay, depdelay15bool, arrtime,arrdelay, arrdelay15bool, cancelledbool, cancelcode, distance, carrierdelay, weatherdelay, nasdelay, securitydelay, lateaircraftdelay);" """.format(**sqlsettings))
    
    if (continueBool != 999):
        print "enter anything to continue, but:"
        continueBool = input('Enter 999 to continue to process all files...')
    


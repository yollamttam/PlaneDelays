import os

sqlsettings={'usr':'matt', 'dba':'matts_stuff', 'outfile':'airportWeatherStations.txt'} 

#os.system('mysql -u {usr} -p{pwd} {dba} -e "select * from (select StartTerminal as term, startdate as date, -1 as count from bikeshare Union All select EndTerminal as term, enddate as date, 1 as count from bikeshare ) as a order by a.date;" > {outfile}'.format(**sqlsettings))

# Take data from your stations database and export it to a file
os.system("""mysql -u {usr} {dba} -e "select USAF, WBAN, ICAO, STATION from stations where ICAO != '' and STATION like '% AIR%';" > {outfile}""".format(**sqlsettings))

# drop weather table if it exists already
print "dropping weather table if it exists already..."
os.system("""mysql -u {usr} {dba} -e "drop table if exists weather;" """.format(**sqlsettings))
# Create the weather table that you're going to load all the weather data into
print "creating our own weather table, with hookers and hourly precipitation data..."
os.system("""mysql -u {usr} {dba} -e "CREATE TABLE weather (USAF MEDIUMINT, WBAN MEDIUMINT, DATES DATETIME,
WINDDIR MEDIUMINT, WINDSPEED FLOAT, WINDGUST FLOAT, CLOUDCEIL
VARCHAR(10), SKYCOVER VARCHAR(10), L VARCHAR(10), M VARCHAR(10), H
VARCHAR(10), VISIBILITY FLOAT, MW VARCHAR(5), MWW VARCHAR(5), MWWW
VARCHAR(5), MWWWW VARCHAR(5), AW VARCHAR(5), AWW VARCHAR(5), AWWW
VARCHAR(5), AWWWW VARCHAR(5), W VARCHAR(5), TEMP FLOAT DEFAULT -999,
DEWPOINT FLOAT DEFAULT -999, SEAPRESSURE FLOAT DEFAULT -999, ALTIMITER
FLOAT, STATIONPRESSURE FLOAT DEFAULT -999, MAXTEMPT FLOAT DEFAULT
-999, MINTEMPT FLOAT DEFAULT -999, HOURLYPREC FLOAT, SIXHOURPREC
FLOAT, DAILYPREC FLOAT, THREEHOURPREC FLOAT, SNOWDEPTH FLOAT);" """.format(**sqlsettings))



# ok, so we want to iterate through this list 
# each row is an airport, we want to take USAF, WBAN
# numbers to get the FTP address for the data set

# Let's start with the year 2014
YEAR = 2014
contBool = 0

infile = open(sqlsettings['outfile'])
infile.readline() # skip the header

# create folder for data: WeatherData
folderName = "/tmp/WeatherData"
folderExists = os.path.exists(folderName)
if (folderExists == 0):
    os.system("mkdir %s" % (folderName))
    
for line in infile.readlines():
    # term, date, count = line.split('\t')
    USAF, WBAN, ICAO, STATION = line.split('\t')
    USAF = int(USAF)
    WBAN = int(WBAN)
    fileBase = "%06d-%05d-%d" % (USAF,WBAN,YEAR)
    filestring = "%06d-%05d-%d.gz" % (USAF,WBAN,YEAR)
    basevalue = "ftp://ftp.ncdc.noaa.gov/pub/data/noaa/2014/"
    filename = filestring
    filestring = basevalue + filestring
    print filestring
    os.system("wget %s" % (filestring))

    # perform check that file was downloaded. 
    successfulDownload = os.path.isfile(filename)
    if successfulDownload:
        print "%s successfully downloaded..." % (filename)
        os.system("gunzip %s" % (filename))
        os.system("java -classpath . ishJava %s %s.out" % (fileBase,fileBase))
        os.system("rm %s" % (fileBase))
        
        loadfile = "/tmp/WeatherData/%s.out" % (fileBase)
        sedshit = 1
        if sedshit:
            os.system("sed -i 's/\s\+/,/g' %s.out" % (fileBase))
            os.system("sed -i 's/*//g' %s.out" % (fileBase))
        os.system("mv %s.out %s/" % (fileBase,folderName))            
        sqlsettings={'usr':'matt', 'dba':'matts_stuff', 'outfile':loadfile}
        os.system("""mysql -u {usr} {dba} -e "load data infile '{outfile}' into table
weather fields terminated by ',' ignore 1 lines (USAF, WBAN, @DATES,
WINDDIR, WINDSPEED, WINDGUST, CLOUDCEIL, SKYCOVER, L, M, H,
VISIBILITY, MW, MWW, MWWW, MWWWW, AW, AWW, AWWW, AWWWW, W, TEMP,
DEWPOINT, SEAPRESSURE, ALTIMITER, STATIONPRESSURE, MAXTEMPT, MINTEMPT,
HOURLYPREC, SIXHOURPREC, DAILYPREC, THREEHOURPREC, SNOWDEPTH) SET
DATES = STR_TO_DATE(@DATES, '%Y%m%d%H%i');" """.format(**sqlsettings))

        os.system("rm %s" % (loadfile))
    else:
        print "looks like %s does not exist, moving on..." % (filename)
        os.system("""echo "%s" >> unsuccessfulFiles.txt""" % (filename))

    if (contBool != 999):
        contBool = input('Enter something to continue on to next file, enter 999 to get all...')

    


infile.close()

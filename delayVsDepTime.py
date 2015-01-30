import os
import numpy as np
import matplotlib.pyplot as plt

sqlsettings={'usr':'matt', 'dba':'matts_stuff', 'outfile':'USdata.txt'}


#os.system('mysql -u {usr} {dba} -e "SELECT originstate, AVG(depdelay15bool) FROM flights GROUP BY originstate;" > {outfile}'.format(**sqlsettings))

os.system('mysql -u {usr} {dba} -e "SELECT deptime, AVG(depdelay15bool) FROM flights GROUP BY deptime;" > {outfile}'.format(**sqlsettings))

infile = open(sqlsettings['outfile'])
infile.readline() # skip the header

# shades of blue
# colorlist = ["#011f4b", "#03396c", "#005b96", "#6497b1", "#b3cde0"]  
# shades of green
# colorlist = ["#4d7f17", "#6bb120", "#8ae429", "#9afe2e", "#aefe57"]
# shades of purple
# colorlist = ["#660066", "#800080", "#be29ec", "#d896ff", "#efbbff"]
# shades of turquoise 
# colorlist = ["#3bd6c6", "#40e0d0", "#43e8d8", "#89ecda", "#b3ecec"]
# colorlist.reverse()

flightcounts = np.array(())
deptimes = np.array(())
statedict = {}
colordict = {}
for line in infile.readlines():
    
    deptime,avgdelay = line.strip().split('\t')
    avgdelay = float(avgdelay)          
    deptime = float(deptime)
    flightcounts = np.hstack((flightcounts,avgdelay))
    deptimes = np.hstack((deptimes,deptime))

infile.close()

plt.plot(deptimes,flightcounts,'x')
plt.title('Percentage of Flights Delayed Vs. Departure Time')
plt.ylabel('Percentage of Flights Delayd')
plt.xlabel('Departure Time')
plt.show(block=False)
input('Press return to end program...')


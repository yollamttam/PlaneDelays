import os
import numpy as np
import matplotlib.pyplot as plt

sqlsettings={'usr':'matt', 'dba':'matts_stuff', 'outfile':'USdata.txt'}


#os.system('mysql -u {usr} {dba} -e "SELECT originstate, AVG(depdelay15bool) FROM flights GROUP BY originstate;" > {outfile}'.format(**sqlsettings))

os.system('mysql -u {usr} {dba} -e "SELECT destairport, AVG(depdelay15bool) FROM flights GROUP BY destairport;" > {outfile}'.format(**sqlsettings))

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
statedict = {}
colordict = {}
for line in infile.readlines():
    
    origin,count = line.strip().split('\t')
    count = float(count)          
    flightcounts = np.hstack((flightcounts,count))
    

infile.close()

plt.hist(flightcounts,30)
plt.xlabel('Percentage of Flights Delayed')
plt.ylabel('Frequency')
plt.title('Distribution of Percentage of Flights Delayed (>15 min) by Dest. Airport')
plt.show(block=False)
input('Press return to end program...')


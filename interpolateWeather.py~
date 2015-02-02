import os
import numpy as np


sqlsettings={'usr':'matt', 'dba':'matts_stuff', 'outfile':'USdata.txt'}


os.system('mysql -u {usr} {dba} -e "SELECT originstate, AVG(depdelay15bool) FROM flights GROUP BY originstate;" > {outfile}'.format(**sqlsettings))


infile = open(sqlsettings['outfile'])
infile.readline() # skip the header

# shades of blue
colorlist = ["#011f4b", "#03396c", "#005b96", "#6497b1", "#b3cde0"]  
# shades of green
# colorlist = ["#4d7f17", "#6bb120", "#8ae429", "#9afe2e", "#aefe57"]
# shades of purple
# colorlist = ["#660066", "#800080", "#be29ec", "#d896ff", "#efbbff"]
# shades of turquoise 
# colorlist = ["#3bd6c6", "#40e0d0", "#43e8d8", "#89ecda", "#b3ecec"]
colorlist.reverse()

flightcounts = np.array(())
statedict = {}
colordict = {}
for line in infile.readlines():
    
    depstate, count = line.strip().split('\t')
    count = float(count)          
    flightcounts = np.hstack((flightcounts,count))
    statedict[depstate] = count

infile.close()

flightcounts = np.sort(flightcounts)
print flightcounts


flightcounts1 = np.percentile(flightcounts,20)
flightcounts2 = np.percentile(flightcounts,40)
flightcounts3 = np.percentile(flightcounts,60)
flightcounts4 = np.percentile(flightcounts,80)

print flightcounts1,flightcounts2,flightcounts3,flightcounts4


infile = open(sqlsettings['outfile'])
infile.readline() # skip the header
for line in infile.readlines():
    depstate, count = line.strip().split('\t')
    count = float(count)
    if (count <= flightcounts1):
        colorchoice = colorlist[0]
    elif ((count <= flightcounts2)&(count>=flightcounts1)):
        colorchoice = colorlist[1]
    elif ((count <= flightcounts3)&(count>=flightcounts2)):
        colorchoice = colorlist[2]
    elif ((count <= flightcounts4)*(count>=flightcounts3)):
        colorchoice = colorlist[3]
    elif (count > flightcounts4):
        colorchoice = colorlist[4]

    colordict[depstate] = """style="fill:%s" """ % (colorchoice)


print colordict.items()          
          
colordict["DC"] = """style="fill:#b3cde0" """
colordict["AS"] = """style="fill:#b3cde0" """
colordict["GU"] = """style="fill:#b3cde0" """
colordict["MP"] = """style="fill:#b3cde0" """
colordict["PR"] = """style="fill:#b3cde0" """
infile = open('Blank_US_Map.svg')
svg = infile.read()
outfile = open('output.svg','w')
outfile.write(svg.format(**colordict))
outfile.close()

infile.close()

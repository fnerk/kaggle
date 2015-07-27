import csv as csv
import numpy as numpy

path = '/Users/damiencouch/kaggle'

print ('Hello')
csv_file_object = csv.reader(open(path+'/data/tit.csv','rb'))
header = csv_file_object.next()
data=[]
for row in csv_file_object:
	data.append(row)
data = numpy.array(data)

#print data
## print first row
#print data[0]
## print last row
#print data[-1]
## print thrid column first row
#print data[0,3]
## print 4th column
#print data[0::,3] 

num_passengers = numpy.size(data[0::,1].astype(numpy.float))
num_survived = numpy.sum(data[0::,1].astype(numpy.float))
print num_passengers
print num_survived

proportion_survivors = num_survived/num_passengers
print proportion_survivors

women_only_stats = data[0::,4] == "female"
men_only_stats = data[0::,4] != "female"

women_onboard = data[women_only_stats,1].astype(numpy.float)
men_onboard = data[men_only_stats,1].astype(numpy.float)

proportion_women_survived = numpy.sum(women_onboard) / numpy.size(women_onboard)

proportion_men_survived = numpy.sum(men_onboard) / numpy.size(men_onboard)

print 'women survived is %s' % proportion_women_survived
print 'men survived is %s' % proportion_men_survived



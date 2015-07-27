import csv as csv
import numpy as np

data_path = '/Users/damiencouch/kaggle/data'

input_file = open(data_path + '/tit.csv','rb')
input_file_object = csv.reader(input_file)

output_file = open(data_path + '/predictions.csv','wb')
output_file_object = csv.writer(output_file)

header = input_file_object.next()
data=[]
for row in input_file_object:
	data.append(row)
data = np.array(data)

fare_ceiling = 40

data[ data[0::,9].astype(np.float) >= fare_ceiling, 9 ] = fare_ceiling - 1.0

fare_bracket_size = 10

num_price_buckets = fare_ceiling / fare_bracket_size

num_classes = len(np.unique(data[0::,2]))

survival_table = np.zeros((2, num_classes, num_price_buckets))

#print survival_table

for i in xrange(num_classes):
	for j in xrange(num_price_buckets):
		women_only_stats = data[                         \
   		                   		(data[0::,4] == "female")  \
                       		&(data[0::,2].astype(np.float) \
                             	== i+1) \
                       &(data[0::,9].astype(np.float)  \
                            >= j*fare_bracket_size)   \
                       &(data[0::,9].astype(np.float)  \
                            < (j+1)*fare_bracket_size)\
                          , 1]                        

		men_only_stats = data[                         \
   		                   		(data[0::,4] != "female")  \
                       		&(data[0::,2].astype(np.float) \
                             	== i+1) \
                       &(data[0::,9].astype(np.float)  \
                            >= j*fare_bracket_size)   \
                       &(data[0::,9].astype(np.float)  \
                            < (j+1) * fare_bracket_size) \
                          , 1]

		survival_table[0,i,j] = np.mean(women_only_stats.astype(np.float))
		survival_table[1,i,j] = np.mean(men_only_stats.astype(np.float)) 

survival_table[ survival_table != survival_table ] = 0

survival_table [ survival_table <  0.5 ] = 0
survival_table [ survival_table >= 0.5 ] = 1

#### writing output, predictions based on survival table #####
####
output_file_object.writerow(["PassengerID", "survived"])


input_file.seek(0)
header = input_file_object.next()

for row in input_file_object:
	for j in xrange(num_price_buckets):
		try:
			row[8] = float(row[8])
		except:
			bin_fare = 3 - float(row[1])
			break
		if row[8] > fare_ceiling:
			bin_fare = num_price_buckets - 1
			break
		if row[8] >= j* fare_bracket_size and row[8] < (j+1) * fare_bracket_size:
			bin_fare = j
			break
	if row[3] == 'female' :
	#??print row[4]
		output_file_object.writerow([row[0],"%d" % int(survival_table[0, float(row[1])-1, bin_fare])])
	else:
		output_file_object.writerow([row[0],"%d" % int(survival_table[1, float(row[1])-1, bin_fare])])

input_file.close()
output_file.close()


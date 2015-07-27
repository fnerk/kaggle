import csv as csv
import numpy as numpy

data_path = '/Users/damiencouch/kaggle/data'

input_file = open(data_path + '/tit.csv','rb')

input_file_object = csv.reader(input_file)

output_file = open(data_path + '/genderbasemodel.csv','wb')
output_file_object = csv.writer(output_file)

output_file_object.writerow(["PassengerID", "survived"])

for row in input_file_object:
	#print row[4]
	if row[4] == 'female':
		output_file_object.writerow([row[0],'1'])
	else:
		output_file_object.writerow([row[0],'0'])
input_file.close()
output_file.close()


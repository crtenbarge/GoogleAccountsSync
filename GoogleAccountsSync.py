##Requires CSV or XLS File with the following columns

## Row 0 = Firstname
## Row 1 = Lastname
## Row 2 = Email
## Row 3 = Password
## Row 4 = School 
## Row 5 = Grade
## Row 6 = Enrolled (A or I)
## Row 7 = Date Enrolled
## Row 8 = Date Unenrolled
## Row 9 = On Restriction (Y or N)

import time
currentTime = int(time.time());
week = 604800;
month = 2592000;
threeMonth = 7776000;
year = 31800000;

##How far back to go with added students. See variables above. Recommendation is "week".
timeMark = week;
x=0;

import csv
import os

##Remove stray files
bashCommandX = 'rm '+dirpath+'/skyward.csv '+dirpath+'/skyward.xls '+dirpath+'/skyward.xml'
os.system(bashCommandX)

##Only necessary when converting from XLS to CSV. Requires LibreOffice and OS X
bashcommandZ = 'mv '+dirpath+'/*skyread*.xls '+dirpath+'/skyward.xls'
os.system(bashcommandZ)
bashCommandA = '/Applications/LibreOffice.app/Contents/MacOS/soffice --headless --convert-to xml '+dirpath+'/skyward.xls'
os.system(bashCommandA)
bashCommandB = '/Applications/LibreOffice.app/Contents/MacOS/soffice -headless --convert-to csv '+dirpath+'/skyward.xml'
os.system(bashCommandB)
bashCommandY = 'mv '+dirpath+'/skyward.csv '+dirpath+'/skyward.csv'
os.system(bashCommandY)



with open('skyward.csv', 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
    	x = x+1;
    	if x==1:
    		print 'lets get this party started!'
    	else:
			date_time = row[7]
			pattern = '%m/%d/%Y'
			pastTime = int(time.mktime(time.strptime(date_time, pattern)));
			diff = currentTime - pastTime;
    	if row[6] == 'I':
			bashCommand = "~/gam/gam.py update user %s suspended on" % (row[2])
			os.system(bashCommand)
			print 'Done: %s %s was suspended' % (row[0], row[1])
    	elif row[6] == 'A':
			if row[9] == 'Y':
				if diff < timeMark:
					bashCommand1 = 'python ~/gam/gam.py create user %s firstname "%s" lastname "%s" password %s000 suspended off changepassword off org "Students/%s/%sR"' % (row[2],row[0],row[1],row[3],row[4],row[5], )
					os.system(bashCommand1)
				bashCommand2 = 'python ~/gam/gam.py update user %s firstname "%s" lastname "%s" suspended off changepassword off org "Students/%s/%sR"' % (row[2],row[0],row[1],row[4],row[5], )
				os.system(bashCommand2)
				print 'Done: %s %s was added or updated and restricted' % (row[0], row[1])
			elif row[9] == 'N':
				if diff < timeMark:
					bashCommand1 = 'python ~/gam/gam.py create user %s firstname "%s" lastname "%s" password %s000 suspended off changepassword off org "Students/%s/%s"' % (row[2],row[0],row[1],row[3],row[4],row[5], )
					os.system(bashCommand1)
				bashCommand2 = 'python ~/gam/gam.py update user %s firstname "%s" lastname "%s" suspended off changepassword off org "Students/%s/%s"' % (row[2],row[0],row[1],row[4],row[5], )
				os.system(bashCommand2)
				print 'Done: %s %s was added or updated and privilaged' % (row[0], row[1])
    print 'Sync complete'

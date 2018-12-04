from text_alignment import build_table
import string
import random

alphabet=list(string.ascii_uppercase)

for i in range(30):
	t1=[random.choice(string.ascii_uppercase) for x in range(random.randint(1,27))]
	t2=[random.choice(string.ascii_uppercase) for x in range(random.randint(1,27))]
	pgap=random.randint(1,5)*(-1)
	pxy=random.randint(2,4)*(-1)
	print('Test number',i,':')
	print ('T1=',t1)
	print ('T2=',t2)
	print ('pgap=',pgap,'\tpxy=',pxy,'\nResult:')	
	try:
		build_table(t1,t2,pgap,pxy)
	except Exception as e:
		print(e)
	print ('\n')
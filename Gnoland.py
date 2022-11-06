import os
import sys
import pexpect
import time
import sqlite3
import datetime
from subprocess import Popen,PIPE
import json
import argparse



def get_balance():
	pwd=os.getcwd()
	db_pwd=pwd+"/Gnoland.db"
	print(db_pwd)
	conn =sqlite3.connect(db_pwd)
	c=conn.cursor()	
	c.execute('SELECT addr FROM Gnoland;')
	rows=c.fetchall()
	for i in rows:
		try:
			addr=i[0]
			result=Popen("gnokey query auth/accounts/{addr} --remote test3.gno.land:36657".format(addr=addr),shell=True,stdout=PIPE)
			balance=result.stdout.read().decode('utf-8')
			result=json.loads(balance.split("data")[1][2:])
			coins=result["BaseAccount"]["coins"]
			c.execute("UPDATE Gnoland SET balance = '%s' where addr=='%s';"%(coins,addr))
			conn.commit()
			print("**************")
			print("addr: "+addr)
			print("balance: "+coins)
			print("##############")
			#js=json.loads(result)
			#print (js)
		except TypeError:
			c.execute("UPDATE Gnoland SET balance = '0' where addr=='%s';"%(addr))
			conn.commit()
			print("**************")
			print("addr: "+addr)
			print("balance: "+"0ugnot")
			print("##############")
	conn.close()


def get_Gnoland():
	pwd=os.getcwd()
	db_pwd=pwd+"/Gnoland.db"
	print(db_pwd)
	conn =sqlite3.connect(db_pwd)
	c=conn.cursor()
	for i in range(1000000):
		tampletime=time.time()
		current=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(tampletime))
		name=str(int(tampletime*1000))
		child=pexpect.spawn('gnokey add %s'%(name))
		child.expect([pexpect.TIMEOUT,'Enter a passphrase to encrypt your key to disk'])
		child.sendline('abcd1234') 
		child.expect([pexpect.TIMEOUT,'Repeat the passphrase:'])
		child.sendline('abcd1234') 
		output=child.read()
		result=output.decode('utf-8')
		addr=result.split(':')[1].split(' ')[1]
		pub=result.split(':')[2].split(' ')[1].split(",")[0]
		key=result.split('\r\n\r\n')[3]
		print("********************")
		print("time: "+current)
		print("name: "+name)
		print("addr: "+addr)
		print("pub: "+pub)
		print("key: "+key)
		c.execute("INSERT INTO Gnoland (bjtime,name,addr,pub,key)\
				VALUES('%s','%s','%s','%s','%s')"\
				%(current,name,addr,pub,key))
		conn.commit()
		c.execute("SELECT COUNT(*) FROM Gnoland;")
		rows=c.fetchall()
		row=str(rows[0][0])
		print ("addr total: "+row)
		print("####################")


	conn.close()
def  main(num):
	if num==1:
		get_Gnoland()
	elif num==2:
		get_balance()

if __name__ == '__main__':
	parse = argparse.ArgumentParser()
	parse.add_argument('number', type=int, help='A number')
	args = parse.parse_args()
	main(args.number)

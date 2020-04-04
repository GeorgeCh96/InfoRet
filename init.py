import os
import subprocess 
import sys

def move(filelist, dest_name, b) :
	for file in filelist:
		source = os.path.join(b, file)
		dest = os.path.join(b, dest_name, file)
		os.replace(source, dest)	
	return 0

def IndexMod(dlist, ba) :
	inp = open("IndriBuildIndex.parameter.file.EXAMPLE", "r") #BasicIndri
	output = open("new", "w") #newIndri
	for line in inp:
		if '<path>' in line:	
			for doc in dlist :
				output.write('   <path>' + os.path.join(ba, 'collection', doc) + '</path>\n')
				break
		elif '<index>' in line:
			output.write(' <index>' + os.path.join(ba, 'index') + '</index>\n')
		else:
			output.write(line)
	inp.close()
	output.close()
	return 0

def QIndexMod(ba):
	inp = open("IndriRunQuery.queries.file.301-450-titles-only.EXAMPLE", "r") #BasicIndri
	output = open("newQ", "w") #newIndri
	for line in inp:
		if '<index>' in line:
			output.write(' <index>' + os.path.join(ba, 'index') + '</index>\n')
		else:
			output.write(line)
	inp.close()
	output.close()
	return 0	


print("Is initialization needed? [y/n] ")
init = input("Enter value: ")

if init == 'y' :
	base = os.getcwd()

	qf = open("qrels.301-450.trec.adhoc", "w")
	subprocess.call(["cat", "qrels.301-350.trec6.adhoc", "qrels.351-400.trec7.adhoc", "qrels.401-450.trec8.adhoc"], stdout=qf)
	qf.close()
	
	tf = open("topics.301-450.trec", "w")
	subprocess.call(["cat", "topics.301-350.trec6", "topics.351-400.trec7", "topics.401-450.trec8"], stdout=tf)
	tf.close()

	q_list = ["qrels.301-350.trec6.adhoc", "qrels.351-400.trec7.adhoc", "qrels.401-450.trec8.adhoc"] #, "qrels.301-450.trec.adhoc"
	t_list = ["topics.301-350.trec6", "topics.351-400.trec7", "topics.401-450.trec8"] #, "topics.301-450.trec"
	d_list = ['fbis', 'fr94', 'ft', 'latimes']

	os.mkdir(os.path.join(base, 'qrels'))
	os.mkdir(os.path.join(base, 'topics'))
	os.mkdir(os.path.join(base, 'collection'))
	os.mkdir(os.path.join(base, 'index')) #indribuildindex

	move(q_list, 'qrels', base)
	move(t_list, 'topics', base)
	move(d_list, 'collection', base)

	IndexMod(d_list, base)
	subprocess.call(["mv", "new", "IndriBuildIndex.parameter.file.EXAMPLE"])

	QIndexMod(base)
	subprocess.call(["mv", "newQ", "IndriRunQuery.queries.file.301-450-titles-only.EXAMPLE"])	

	print('Building Index')
	subprocess.call(["IndriBuildIndex", "IndriBuildIndex.parameter.file.EXAMPLE"])



elif init != 'n' :
	print("Type proper character [y or n]")
	sys.exit()

subprocess.call(["python3", "cr_query.py"])

res = open("results.trec", "w")
subprocess.call(["IndriRunQuery", "IndriRunQuery.queries.file.301-450.EXAMPLE"], stdout=res)
res.close()

#find / -name trec_eval 2> /dev/null
t_eval = os.system("find / -name trec_eval 2> /dev/null")
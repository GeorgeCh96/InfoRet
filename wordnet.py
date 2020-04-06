from nltk.corpus import wordnet as wn
from random import randrange

punct = [".", ',', '!', ';', '?', '(', ')', ':', '"']
p_space = ["'", '/', '   ', '  ', '_',  '-'] # 
qnum = 301

inp = open("IndriRunQuery.queries.file.301-450.EXAMPLE", "r")
out = open("IndriRunQuery.synonims.301-450.EXAMPLE", "w")


def remove_duplicates(list):
	newlist = []
	list = [x.lower() for x in list]
	for i in list:
		if i not in newlist:
			newlist.append(i)	
	return newlist	

def punct_rem(line2b):
	for sym in punct:
		if line2b.find(sym) != -1 :
			line2b = line2b.replace(sym,'')

	for sym in p_space:
		if line2b.find(sym) != -1 :
			line2b = line2b.replace(sym,' ')

	if line2b.find('&') != -1 :
		line2b = line2b.replace('&',' and ')	
	line2b = line2b.strip()
	return line2b	

#returns list of strings/synonims for every word in a line
def syn_gen(text):
	syns = []
	for word in text:
		s_set = wn.synsets(word)
		sense = {} 
		
		if not s_set:
			continue
		#For every synset in s_set find with which one of the rest has the highest similarity 
		for i in range(len(s_set)):
			mx = 0
			idx = []
			for j in range(len(s_set)) :
				score = s_set[i].wup_similarity(s_set[j])
				#creation of dict only in the first iteration
				if i == 0:
					sense[j] = 0
				#a kind of normalisation for cases where score cannot be provided
				if score == None:
					idx = [0] #randrange(len(s_set)): choose by luck or zero: choose the first one
					continue
				elif score != 1 :
					if score > mx:
						mx = score
						idx = [j]
					#if we have ties for the highest score be fair 	
					elif score == mx:
						idx.append(j)
			
			for index in idx:
				sense[index] = sense[index] + 1

		key = max(sense, key=sense.get)

		#Take the synset which occures the most
		new_syns = s_set[key].lemma_names() 

		if len(new_syns) > 2 :
			syns.extend(new_syns[0:2]) 
		else:
			syns.extend(new_syns)
	return syns


for line in inp:
	if '<query>' not in line:
		out.write(line)
		continue
	
	#filtering query to text	
	txt = line.rpartition('<text>')[-1].rpartition('</text>')[0]
	txt = txt.split(' ')

	#synonyms generate
	syns = syn_gen(txt)

	#enchance initial text with syns	
	txt.extend(syns)

	#normalisation
	txt = ' '.join(txt)	
	txt = punct_rem(txt)
	txt = txt.split(' ')
	txt = remove_duplicates(txt)
	txt = ' '.join(txt)

	out.write('<query> <type>indri</type> <number>%d</number> <text>%s</text> </query>\n' %(qnum,txt))
	qnum += 1
	
inp.close()
out.close()
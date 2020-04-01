f1 = open("IndriRunQuery.queries.file.301-450-titles-only.EXAMPLE", "r") #BasicIndriQuery
f2 = open("topics.301-450.trec", "r") #topics
out = open("IndriRunQuery.queries.file.301-450.EXAMPLE", "w") #newIndriQuery

flag = False
flag2 = False

punct = [".", ',', '!', ';', '?', '(', ')', ':', '"'] # , "'", '/', '-' space?
p_space = ["'", '/', '   ', '  '] # '-', 

def dashed(line3b, count2): #applies to multiple spaces as well 
	dash = 0
	while count2 > 1 :
		dash = line3b.find('-',dash)
		if line3b[dash + 1] == '-' :
			line3b = line3b[:dash +1] + line3b[dash + 2 :]
						
		else : 
			dash += 1 
		count2 -= 1
	line3b = line3b.strip()
	if line3b.find('-') == 0 :
		line3b = line3b.replace('-', '', 1)
	line3b = line3b.replace(' -', '-')
	line3b = line3b.replace('- ', '-')
	return line3b

def punct_rem(line2b):
	for sym in punct:
		if line2b.find(sym) != -1 :
			line2b = line2b.replace(sym,'')

	for sym in p_space:
		if line2b.find(sym) != -1 :
			line2b = line2b.replace(sym,' ')

	if line2b.find('&') != -1 :
		line2b = line2b.replace('&',' and ')	

	c = line2b.count('-')
	if  c > 0 :
		line2b = dashed(line2b, c)
	line2b = line2b.strip()
	return line2b		

print("1: Titles only 2: Titles and Descriptions 3: Titles, Descriptions and Narratives ")
s = int(input("Enter value: "))

if s == 1:
	out.write(f1.read())
	print("IndriRunQuery.queries.file.301-450.EXAMPLE has been created. [Titles Only]")
	
elif s == 2 or s == 3:

	for line in f1:
		end = line.find("</text>")
		flag = False;
		flag2 = False;

		if end == -1 :
			out.write(line)
		else:
			out.write(line[0 : end])
			#out.write(' ')
			for line2 in f2:
				start = line2.find("<desc>")
				if start == 0: 
					flag = True
					line2 = next(f2)

				if flag:
					if line2.strip() and not line2.count("<narr>"):
						line2 = punct_rem(line2)
						out.write(' ' + line2.rstrip('\n'))
					else :	
						if s == 3 :
							for line2 in f2:
								start2 = line2.find("<narr>")
								if start2 == 0: 
									flag2 = True
									line2 = next(f2)

								if flag2:
									if line2.strip():
										if line2.rstrip('\n') != '</top>' :
											line2 = punct_rem(line2)
											out.write(' ' + line2.rstrip('\n'))
										else: 
											out.write("</text> </query> \n")								 
											break
							break				
						elif line2.count('<narr>') : 
							line2 = next(f2)
							out.write("</text> </query> \n") 
							break
	if s == 2:							
		print("IndriRunQuery.queries.file.301-450.EXAMPLE has been created. [Titles and Descriptions]")
	else :
		print("IndriRunQuery.queries.file.301-450.EXAMPLE has been created. [Titles, Descriptions and Narratives]")	
else:
	print("Enter Proper Value")

f1.close()
f2.close()
out.close()

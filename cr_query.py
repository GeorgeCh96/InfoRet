f1 = open("IndriRunQuery.queries.file.301-450-titles-only.EXAMPLE", "r") #BasicIndriQuery
f2 = open("topics.301-450.trec", "r") #topics
out = open("IndriRunQuery.queries.file.301-450.EXAMPLE", "w") #newIndriQuery
flag = False
flag2 = False
whitespace = ' '
punct=[".", ',', '!', ';', '?', '(', ')', ':',"'", '"', '/', '-']

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
			out.write(whitespace)
			for line2 in f2:
				start = line2.find("<desc>")
				if start == 0: 
					flag = True
					line2 = next(f2)

				if flag:
					if line2.strip():
						
						for sym in punct:
							if line2.find(sym) != -1 :
								line2 = line2.replace(sym,whitespace)

						if line2.find('&') != -1 :
							line2 = line2.replace('&',' and ')

						out.write(line2.rstrip('\n') + whitespace)
					else :	
						if s ==3 :
							for line2 in f2:
								start2 = line2.find("<narr>")
								if start2 == 0: 
									flag2 = True
									line2 = next(f2)

								if flag2:
									if line2.strip():
										
										for sym in punct:
											if line2.find(sym) != -1 :
												line2 = line2.replace(sym,whitespace)

										if line2.find('&') != -1 :
											line2 = line2.replace('&',' and ')
										
										out.write(line2.rstrip('\n') + whitespace)
									else:
										line2 = next(f2)
										out.write("</text> </query> \n") 
										break
							break				
						else:
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

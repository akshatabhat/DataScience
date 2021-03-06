import os.path

file_ids = list(range(1,110))+list(range(200,310))+list(range(400,510))

for i in file_ids:
	filename = str(i) + ".txt"
	if (os.path.isfile(filename)) :
		f = open(filename, 'r')
		data = f.readlines()
		f.close()
		newdata = ''
		for lines in data:
			if "EU" in lines:
				lines = lines.split(' ')
				for word in lines:
					if "EU" == word:
						newdata += " <loc>EU</loc>"
					elif "EU," == word:
						print(word)
						newdata += " <loc>EU,</loc>"
					elif "EU's" == word:
						print(word)
						newdata += " <loc>EU's</loc>"
					elif "EU." == word:
						newdata += " <loc>EU.</loc>"
					elif "EU:" == word:
						newdata += " <loc>EU:</loc>"
					elif "EU." == word:
						newdata += " <loc>EU.</loc>"
					elif "(EU)" == word:
						newdata += " <loc>(EU)</loc>"
					else :
						newdata += " " + word
			else:
				newdata += lines
		f = open(filename, 'w')
		f.writelines(newdata)	 
		f.close() 


for i in file_ids:
	filename = str(i) + ".txt"
	if (os.path.isfile(filename)) :
		f = open(filename, 'r')
		data = f.readlines()
		f.close()
		newdata = ''
		for lines in data:
			if "European Union" in lines:
				lines = lines.split(' ')
				prevWord = ''
				for word in lines:
					if "European" == word:
						prevWord = "European"
					elif "Union" == word:
						if (prevWord == "European") :
							newdata += " <loc>European Union</loc>"
							prevWord = word
						else :
							newdata += " " + word
					elif "Union," == word:
						if (prevWord == "European") :
							newdata += " <loc>European Union,</loc>"
							prevWord = word
						else :
							newdata += " " + word
					elif "Union." == word:
						if (prevWord == "European") :
							newdata += " <loc>European Union.</loc>"
							prevWord = word
						else :
							newdata += " " + word
					elif "Union's" == word:
						if (prevWord == "European") :
							newdata += " <loc>European Union's</loc>"
							prevWord = word
						else :
							newdata += " " + word
					elif "Union-" == word:
						if (prevWord == "European") :
							newdata += " <loc>European Union-</loc>"
							prevWord = word
						else :
							newdata += " " + word
					else :
						if (prevWord == "European") :
							newdata += " " + prevWord
						prevWord = word
						newdata += " " + word
			else:
				newdata += lines
		f = open(filename, 'w')
		f.writelines(newdata)	 
		f.close() 
import string
import shutil, errno
import sys
import subprocess
import os

def copyFolder(src, dst):
    try:
        shutil.copytree(src, dst)
    except OSError as exc: # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst)
        else: raise



def convertVrienden():
	## read file
	with open("vrienden.html") as f:
	    content = f.readlines()


	## check for links
	## from  'vrienden/1.html' to  '#/app/vrienden/1'
	for line in content:         
		if ".html" in line:
			index = content.index(line)
			start = line.index('href')
			end  = line.index('.html') 
			vriend = line[end-1:end]
			line = string.replace(line, line[start:end+6], 'href="#/app/vrienden/' + vriend + '"')
			content[index] = line

	## write to file
	fo = open("vrienden.html1", "wb")
	for line in content:         
		fo.write(line)


	fo.close()


##convertVrienden()
for group in sys.argv:

	index = sys.argv.index(group)
	if index > 0:
	#	copyFolder("myfriendbook", sys.argv[1] + "/myfriendbook")
	# os.chdir(sys.argv[1] + "/myfriendbook")
	# subprocess.call(["ionic", "build"])
		print group


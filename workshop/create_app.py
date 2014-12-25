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

def createVrienden(group):

	template = """<ion-view title="Mijn vrienden">
  	<ion-nav-buttons side="left">
  	  <button menu-toggle="left" class="button button-icon icon ion-navicon"></button>
  		</ion-nav-buttons>
  		<ion-content class="has-header">
    		{{ion-list}}
  		</ion-content>
	</ion-view>
  	"""


	with open(group + "/vrienden.html") as f:
	    content = f.readlines()

	## check for links
	## from  'vrienden/1.html' to  '#/app/vrienden/1'
	items = "<ion-list>\n"

	for line in content:         
		if ".html" in line:
			index = content.index(line)
			start = line.index('href')
			end  = line.index('.html') 
			vriend = line[end-1:end]
			line = string.replace(line, line[start:end+6], 'href="#/app/vrienden/' + vriend + '"')
			line = string.replace(line, '<a class="item"', "<ion-item")
			line = string.replace(line, '</a>', "</ion-item>")
			items = items + line + "\n"
	items = items + "\n</ion-list>"		
	template = string.replace(template, '{{ion-list}}', items)

	## write to file
	fo = open("out/" + group + "/myfriendbook/www/templates/vrienden.html", "wb")
	fo.write(template)
	fo.close()
	



##convertVrienden()
for group in sys.argv:

	index = sys.argv.index(group)
	if index > 0:
		print "*** " + group + " ***"
		print "remove old folder"
		shutil.rmtree("out/" + group )
		print "copy folder"
		copyFolder(sys.argv[index], "out/" + group )
		print "copy ionic folder"
		copyFolder("myfriendbook", "out/" + group + "/myfriendbook")

		createVrienden(group)

		os.chdir("out/" + group + "/myfriendbook")
		# subprocess.call(["ionic", "build"])
		


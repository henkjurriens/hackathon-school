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


def createFriends(group):

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

def createFriend(group, friend):

	template = """<ion-view title="Vriend">
  	<ion-nav-buttons side="left">
      <button menu-toggle="left" class="button button-icon icon ion-navicon"></button>
 	</ion-nav-buttons>
	  	{{ion-content}}
	</ion-view>"""

	with open(group + "/vrienden/" + friend) as f:
	    content =  f.readlines()

	content = '\n'.join(content)
	start = content.index('<ion-content>')
	end = content.index('</ion-content>')
	
	content = content[start + 13:end]
	content = "<ion-content class=\"has-header\">" + content + "</ion-content>"
	template = string.replace(template,"{{ion-content}}", content)

	## write to file
	fo = open("out/" + group + "/myfriendbook/www/templates/vrienden/" + friend, "wb")
	fo.write(template)
	fo.close()




	

for group in sys.argv:

	index = sys.argv.index(group)
	if index > 0:
		print "*** " + group + " ***"
		print "remove old folder"

		try:
			shutil.rmtree("out/" + group )
		except:
			print "folder bestaat niet"	

		print "copy folder"
		copyFolder(sys.argv[index], "out/" + group )
		print "copy ionic folder"
		copyFolder("myfriendbook", "out/" + group + "/myfriendbook")

		print "create vrienden.html"
		createFriends(group)

		

		for subdir, dirs, files in os.walk("out/" + group + "/vrienden"):
			print "create friend"
    		for file in files:
    			if ".html" in file :
	    			print "create vrienden/" + file
	        		createFriend(group, file)


		os.chdir("out/" + group + "/myfriendbook")
		subprocess.call(["ionic", "build"])
		os.chdir("..");
		os.chdir("..");
		os.chdir("..");
		subprocess.call(["pwd",])

		


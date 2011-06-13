# -*- coding: utf-8 -*-
# This file has absolutely no copyright or licence at all.
# This file may be written by Virgo Pihlapuu.
#
# This script should make HTML table describing the folder structure and
# files with extensions like: py, cpp and h.
# It also should read some main header rows as a file description, 
# takes optional first argument as search word to filer files with this inside, 
# takes optional second argument as folder name where to search and 
# replaces some weird characters in final resutl string with HTML code.

import sys,os,fnmatch
from sys import argv

print 'Script started\r'
print '* Use extra arguments like: [search_word] [folder_path]' 
print '  to list files wtih specific word inside or search from other folder.'

patterns = ['*.cpp', '*.py', '*.h']
char_pairs = [
['ö','&ouml;'], ['ä','&auml;'], ['ü','&uuml;'], ['õ','&otilde;'], 
['Ö','&Ouml;'], ['Ä','&Auml;'], ['Ü','&Uuml;'], ['Õ','&Otilde;']
]

final_str = '<table border=1 cellpadding=2 width="1100"><tr><th>Index</th><th>File</th><th>Header</th><th>Size (kb)</th></tr>'
f_name = 'dir_sum.html'
size = 0

search_this = ''
if len(argv) > 1:
	search_this = argv[1]
	print '* Searching files with text \"'+ search_this +'\" iside them.'
else:
	print '* No search text argument - will list files without this filter'

path = '.'
if len(argv) > 2:
	path = argv[2]
	print '* Searching in folder: '+ path
else: print '* No path argument - will use default folder'

# Takes path and returns recusiv list of files
def list_files(p):
	res = []
	sub_list = []
	
	for item in os.listdir(p):
		if os.path.isdir(os.path.join(p, item)) == False:
			for pat in patterns:
				if fnmatch.fnmatch(item, pat):
					new_file = os.path.join(p, item)
					if look_in_file(new_file):
						res.append(new_file)
		else:
			sub_list.append(os.path.join(p, item))
			
	for sub in sub_list:
		res.extend(list_files(sub))
		
	return res

# returns some lines from the file as list
def doc_from_file(l):
	f = open(l,'r')
	f_str = ''
	f_str = ''
	line_list = []
	line_str = f.readline()
	line = 0
	while ((len(line_str) > 15) and (line < 5)):
		if(len(line_str) > 70): line_list.append(line_str[:70] +'...')
		else: line_list.append(line_str)
		line_str = f.readline()
		line += 1
	f.close()
	
	return line_list

# if there is search word, it will return true, if this word is in file
def look_in_file(p):
	if len(search_this) != 0:
		f = open(p,'r')
		s = f.read()
		n = s.rfind(search_this)
		f.close()
	else: n = 1
	return n != -1

# retruns string with weird characters replaced if it is enabled
def fix_characters(s,L):
	new_s = s
	for l_item in L:
		new_s = new_s.replace(l_item[0],l_item[1])
		#print 'replacing: "'+ l_item[0] +'" with "'+ l_item[1] +'"'
	return new_s
	
row_color = '"#ddffdd"'

i = 0;
for fp in list_files(path):
	i += 1
	f_sz = os.path.getsize(fp)
	size += f_sz
	final_str += '<tr bgcolor='+ row_color +'><td>'+ str(i) +'</td><td><a href="file:///'+ os.path.abspath(fp) +'">'+ fp +'</a></td><td>'+'<br>'.join(doc_from_file(fp)) +'</td><td>'+ str(int(f_sz / 1000)) +'</td></tr>\n'
	if row_color == '"#ddffdd"':
		row_color = '"#ddddff"'
	else: row_color = '"#ddffdd"'

final_str = '<html><head></head><body>'+ str(i) +' files in '+ os.path.abspath(path) +' with inside text: \"'+ search_this +'\" and filename pattern: '+ ', '.join(patterns) +'.<br>Total size: '+ str(int(size / 1000)) +' kb<br>'+ final_str +'</table></body></html>'
f = open(f_name, 'w')
final_str = fix_characters(final_str,char_pairs)
f.write(final_str)
f.close()

print '* found '+ str(i) +' files with pattern:'+ ', '.join(patterns)
print '* Output file:'+ f_name

#!/usr/bin/python
# -*- coding: utf-8 -*-

import textgen, cStringIO, cgi, re, Image

FONT_FILE="Play-Bold.ttf"
#FONT_FILE="FranklinGothicMediumC.otf"
IMAGE_WIDTH=185
IMAGE_HEIGHT=64



def unescape(s):
	return re.sub('&#([0-9]+);', lambda m: unichr(int(m.group(1))), s)


form = cgi.FieldStorage()
buttonText = unescape(unicode(form.getfirst("text", ""),"utf-8"))

tas = textgen.TextAutoSize(buttonText,IMAGE_WIDTH,IMAGE_HEIGHT,FONT_FILE, linePadding=0)
result=tas.drawOptimalText(textOffsetPercent=0.25)


if result!=None:

	fh=cStringIO.StringIO()
	result.save(fh, "PNG")
	
	print "Content-Type: image/png"
	print "Content-Disposition: attachment; filename=button.png"
	print  
	print fh.getvalue()
else:
	print "Content-Type: image/png"
	print
	print "Error"

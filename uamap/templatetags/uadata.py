from django import template



register = template.Library()

@register.simple_tag
def readdataone():
	processedFile=open("/var/www/html/uamap/uamap/templates/data1.js")
	processedData=processedFile.read()
	return processedData

@register.simple_tag
def readdataoneA():
	processedFile=open("/var/www/html/uamap/uamap/templates/data1A.js")
	processedData=processedFile.read()
	return processedData

@register.simple_tag
def readdata():
	processedFile=open("/var/www/html/uamap/uamap/templates/data.js")
	processedData=processedFile.read()
	return processedData
@register.simple_tag
def readdatatwoA():
	processedFile=open("/var/www/html/uamap/uamap/templates/data2A.js")
	processedData=processedFile.read()
	return processedData 

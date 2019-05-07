from django.shortcuts import render, redirect, render_to_response, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
import textwrap
from django.conf import settings
from django.http import HttpResponse
from django.http import HttpResponseForbidden
from django.views.generic.base import View
from subprocess import Popen, PIPE
import random
from django.http import JsonResponse
#class HomePageView(View):
from django.views.decorators.cache import cache_page

import pymongo
import time
import datetime

import sendgrid
import os
from sendgrid.helpers.mail import *
import sys, re

import uamapfunctions   as uf
from bson.code import Code

def dispatch(request, *args, **kwargs):
        response_text = textwrap.dedent('''\
            <html>
            <head>
                <title>Greetings to the world</title>
            </head>
            <body>
                <h1>Greetings to the world</h1>
                <p>Hello, world!</p>
            </body>
            </html>
        ''')
        return HttpResponse(response_text)


def addmycontent(request):
	data="<form><h1>Add my content</h1>"
	data=data+"<h2>Net id</h2><input type=text id='netid' name=netid><br>"
	data=data+"<h2>URL represent research (one url per line)</h2>"
	data=data+ "<textarea rows=10 cols=60 id=urls></textarea>"
	data=data+"<h2>Papers represent my research (pdf)</h2>"
	data=data+'  <div class="upload-area"  id="uploadfile"> <h2 id="droptxt">Drag and Drop file here<br/>Or<br/>Click to select file</h2>  </div>'
	data=data+"<h2>Grant proposals represent my research(pdf)</h2></form>"

	return render(request, 'addmycontent.html', {'data':''})

def contentsubmit(request):
    netid=request.POST['netid']
    urls=request.POST['urls']
    category=request.POST['category']

    f=request.FILES['file']

    name=f.name
    if name[-4:].lower()!=".pdf":
        data={'name':'error','size':0,'src':''}
        return JsonResponse(data)

    data={'name':name,'size':f.size,'src':'', 'category':category}
    name=f.name.replace(" ","_")
    name=netid + "_" +  category + "_" +name
    handle_uploaded_file(f,name)

    uf.savecontent_info_to_db(netid,name, f.size,category, urls)

    return JsonResponse(data)



def handle_uploaded_file(f,name):
    if not os.path.exists("/pdfs"):
        os.makedirs("/pdfs")
    destination = open('/pdfs/' + name, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return name



def getedgeinfo(request, n1, n2, network):

	financial_group, created = Group.objects.get_or_create(name=settings.FINANCIAL_DATA_ACCESS_GROUP_NAME)
	if request.user.groups.filter(name=settings.FINANCIAL_DATA_ACCESS_GROUP_NAME).exists() or request.user.is_staff or request.user.is_superuser:
		pass
	else:
		return HttpResponse("To access edge data, please login at <a target='_blank' href=/admin>here</a>")
	data=uf.getedgeinfo( n1, n2 )
	return HttpResponse(data)

def getuinfo(request, gsuid,datatype):
	return HttpResponse(uf.getuinfo( gsuid , datatype))

def search(request):
	return render(request, 'search.html', {'data':''})

def addstopwords(request):
#	txt2=request.POST.get('txt', '')
#	f = open('/home/hossain/processor3/lucene/stopwords.txt', 'a')
#	f.write(txt2+",")  # python will convert \n to os.linesep
#	f.close()

	return HttpResponse("done")


def universityregion(request,rid):
	return HttpResponse(uf.universityregion(rid))






def search3(request):
	return render(request, 'search3.html', {'data':''})

def addstopwords3(request):
	txt2=request.POST.get('txt', '')
	f = open(uf.peopleserachbasedlocation+ 'stopwords.txt', 'a')
	f.write(txt2+",")
	f.close()

	return HttpResponse("done")


def savefeedback(request):
	quid=request.POST.get('quid', '')
	txt=request.POST.get('txt', '')
	db = uf.getDBConnection()
	t2={ "$set":{  'feedback':txt}}
	db.searchQuery.update({'quid':quid},t2)
	return HttpResponse("Saved!")


def sendemail(request):


	return HttpResponse("")


def peoplesearchV4(request):

	if request.POST.get('url', '') !="":
		url=request.POST.get('url', '')
		qid, txt=uf.geturlcontent(url)
		qid=str(int(qid))
	else:
		txt2=request.POST.get('txt', 'add text')
		ts = time.time()
		qid = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
		db = uf.getDBConnection()
		t2={ 'quid': qid, 'query':txt2, 'url':'xxx'}
		db.searchQuery.insert(t2)
	cmd="java -cp \""+uf.peopleserachbasedlocation+":"+uf.peopleserachbasedlocation+"*\"  LuceneQueryV4 " + str(qid)
	print(cmd)
	proc = Popen(cmd  , stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
	data, map_err = proc.communicate()
	return HttpResponse(data + map_err)




def peoplesearch3(request):

	if request.POST.get('url', '') !="":
		url=request.POST.get('url', '')
		qid, txt=uf.geturlcontent(url)
		qid=str(int(qid))
	else:
		txt2=request.POST.get('txt', 'add text')
		ts = time.time()
		qid = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
		db = uf.getDBConnection()
		t2={ 'quid': qid, 'query':txt2, 'url':'xxx'}
		db.searchQuery.insert(t2)
	cmd="java -cp \""+uf.peopleserachbasedlocation+":"+uf.peopleserachbasedlocation+"*\"  LuceneQuery " + str(qid)
	print(cmd)
	proc = Popen(cmd  , stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
	data, map_err = proc.communicate()
	return HttpResponse(data + map_err)



def docresearchtopics(request, url):
	qid, txt=uf.geturlcontent(url)
	f = open(uf.peopleserachbasedlocation+'query.txt', 'wb')
	f.write(txt)
	f.close()
	cmd="java -cp \""+uf.peopleserachbasedlocation+":"+uf.peopleserachbasedlocation+"*\"  DocResearchTopics " + str(qid)

#	proc = Popen("java -cp \"/home/hossain/processor3/search3/:/home/hossain/processor3/search3/*\" DocResearchTopics "   , stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
	proc = Popen(cmd  , stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)

	data, map_err = proc.communicate()
	return HttpResponse(data + map_err)








def searchV4(request):
	return render(request, 'searchV4.html', {'data':''})



def search4(request):




	return render(request, 'search4.html', {'data':''})

def addstopwords2(request):
#	txt2=request.POST.get('txt', '')
#	f = open('/home/hossain/processor3/lucene2/stopwords.txt', 'a')
#	f.write(txt2+",")
#	f.close()

	return HttpResponse("done")


def peoplesearch2(request):
#	if request.POST.get('url', '') !="":
#		url=request.POST.get('url', '')
#		proc = Popen("python3 /home/hossain/processor3/lucene2/geturlcontent.py  " + url , stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
#		data, map_err = proc.communicate()
#		txt2=data + map_err
#		f = open('/home/hossain/processor3/lucene2/query.txt', 'wb')
#
#	else:
#		txt2=request.POST.get('txt', 'add text')
#		f = open('/home/hossain/processor3/lucene2/query.txt', 'w')
#
#	f.write(txt2)
#	f.close()
#
#	proc = Popen("java -cp \"/home/hossain/processor3/lucene2/:/home/hossain/processor3/lucene2/*\" LuceneQuery "   , stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
#		dot_out, map_err = proc.communicate(input = removeNonAscii(map_string))
#	data, map_err = proc.communicate()
	return HttpResponse("data + map_err")





def getFederalFund(request,university,sponsor, yearfrom,yearto):
	data=""
	db = uf.getDBConnection()

	map=Code(' function() { var txt = this.topics; if(txt){ txt = txt.split(",");  for (var i = txt.length - 1; i >= 0; i--)  if (txt[i])  emit(txt[i], 1);  }}')
	reduce=Code(' function( key, values ) {     var count = 0;     values.forEach(function(v) {   count +=v; });  return count; }')
	query={}
	query["ORGANIZATION_NAME"] = university.upper()
	if  sponsor!="" :
		query["DEPARTMENT"]=sponsor.upper()



	result = db.federalfund.map_reduce(map, reduce, "tmpTopicsFundCount", query=query )
	data="var federaltopics={"
	res=result.find().sort("value",-1)
	for doc in res:
		data = data+ "'" + doc["_id"] + "'"   +":"+ str(doc["value"])+", "
	data=data+"}"
	return HttpResponse(data )








def peoplesearch(request):
#
#	if request.POST.get('url', '') !="":
#		url=request.POST.get('url', '')
#		proc = Popen("python3 /home/hossain/processor3/lucene/geturlcontent.py  " + url , stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
#		data, map_err = proc.communicate()
#		txt2=data + map_err
#		f = open('/home/hossain/processor3/lucene/query.txt', 'wb')
#
#	else:
#		txt2=request.POST.get('txt', 'add text')
#		f = open('/home/hossain/processor3/lucene/query.txt', 'w')
#
#	f.write(txt2)
#	f.close()
#
#	proc = Popen("java -cp \"/home/hossain/processor3/lucene/:/home/hossain/processor3/lucene/*\" LuceneQuery "   , stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
#		dot_out, map_err = proc.communicate(input = removeNonAscii(map_string))
#	data, map_err = proc.communicate()
	return HttpResponse("data + map_err")

def getexternaledgeinfo(request, dummyid):
	return HttpResponse(uf.getexternaledgeinfo(dummyid))

def getfundinfo(request, gsuid):
	return HttpResponse(uf.getfundinfo(gsuid))

def searchuniversity(request, txt):
	return HttpResponse(uf.searchuniversity(txt) )

def getfunOranizationList(request, txt, department):
	namelist=""
	db = uf.getDBConnection()
	'''
	db.federalfund.distinct("ORGANIZATION_NAME").forEach(function(doc){
	 db.federalfundOrganizations.insert({name:doc})
	}
	)
	db.federalfundOrganizations.createIndex({name:1})
	'''


	x=re.compile(txt, re.IGNORECASE)
	c=db.federalfundOrganizations.find({"name": x, "department":department, "fundcount":{"$gt":3} }).limit(20)

	for u in c:
		namelist = namelist + '<a href="#" onclick=\'getFederalFund("' + u["name"] + '", "NIH")\'>' + u["name"] + '</a><br>'

	 #getFederalFund("University of Arizona","NIH","NSF","")
	return HttpResponse(namelist )


def selecteddepartments(request, txt):

	db = uf.getDBConnection()
	txt=txt.split(",") #["Medicine","Health Promotion Sciences"]
	cursor=db.currentfacuty.find({"dept":{"$in":txt}})
	userid=[];
	for doc in cursor:
		userid.append(doc["userid"])


	cursor=db.networkv2Nodes.find({"userid":{"$in":userid}})
	selectedIds=""
	for doc in cursor:
		selectedIds=selectedIds+str(doc["dummyid"])+","

	return HttpResponse(selectedIds)


def selectedbuilding(request, txt):

	selectedIds="var selected=["
	db = uf.getDBConnection()
	cursor=db.emplbuilding.find({"buildingid":txt})

	for doc in cursor:
		selectedIds= selectedIds + str( doc["dummyid"] )+ ","
	selectedIds= selectedIds +"]"
	return HttpResponse(selectedIds)





def searchdept(request, txt):
	return HttpResponse(uf.searchdept(txt))



def searchfundsource(request, txt):

	financial_group, created = Group.objects.get_or_create(name=settings.FINANCIAL_DATA_ACCESS_GROUP_NAME)
	if request.user.groups.filter(name=settings.FINANCIAL_DATA_ACCESS_GROUP_NAME).exists() or request.user.is_staff or request.user.is_superuser:
		pass
	else:
		return HttpResponse("To access financial data, please login at <a target='_blank' href=/admin>here</a>")

# HttpResponseForbidden('User must be authenticated and be in the "%s" group.' % settings.FINANCIAL_DATA_ACCESS_GROUP_NAME)

	return HttpResponse(uf.searchfundsource(txt))


def topics(request,submap):

#	financial_group, created = Group.objects.get_or_create(name=settings.FINANCIAL_DATA_ACCESS_GROUP_NAME)
#	if request.user.groups.filter(name=settings.FINANCIAL_DATA_ACCESS_GROUP_NAME).exists() or request.user.is_staff or request.user.is_superuser:
#		pass
#	else:
#		return HttpResponse("To access the application, please login at <a target='_blank' href=/admin>here</a>")
	#return HttpResponse("request.user.is_staff")

	return topicsCache(request,submap)


@cache_page(60 * 15)
def topicsCache(request,submap):
	obj={}
	print("request")
#	submap = submap #request.POST.get('submap', 'graph')
	if submap=="":
		submap="world"

	topmap = request.POST.get('topmap', 'cmap')
	obj["submap"]=submap
	obj["txtsize"]=request.POST.get('txtsize', 'degree')
	overalys=request.POST.getlist('overlayvalue')

	obj["Clustering"]=""
	obj["Citation"]=""
	obj["Fund"]=""
	obj["Connections"]=""
	print(overalys)
	for ov in overalys:
		obj[ov]="Yes"

	print("Connections",obj["Connections"])

	return render(request, 'topics2.html', {'data':obj})



def topicsnetwork(request):

	return render(request, 'worldtopicsnetwork.html')

def index(request):
    data="""<h1>UofA Collaborative Map</h1>


    <h3> <a href="#">  Map by considering  publications and research project proposals (v4)</a></h3>



  <h1>GRAM: Global Research Activity Map</h1>


  <table class="table table-hover" id="mapsubtype"> <tbody>
  <tr><td><h3> <a href="/topics">Research Topics Map</h3></td></tr>
  <tr><td><h4> <a href="#">GRAM: DataSet</h4></td></tr>
  <tr><td><h4> <a href="#">GRAM: Gallery </h4></td></tr>
  </tbody></table>

  <h1>Expert Matching</h1>


    <table class="table table-hover" id="mapsubtype"> <tbody>
    <tr><td> <h3> <a href="/searchV4">REMatch: Research Expert Matching System (V4)</h3></td></tr>
    <tr><td> <h3> <a href="https://www.youtube.com/watch?v=P35ss7MMVwA">Video</a></h3></td></tr>
    </tbody></table>"""

    return render(request, 'index.html', {'data':data})




def contributors(request):
	data="""
      <h1>Main Contributors</h1>
<div class="uaqs-person-row">
    <article class="node-236 node node-uaqs-person node-teaser clearfix" about="https://cs.arizona.edu/~hossain" typeof="sioc:Item foaf:Document">

     <header>
               <span property="dc:title" content="Md Iqbal Hossain" class="rdf-meta element-hidden"></span>

          </header>

  <div class="row border-separator"><div class="col-md-3">
  <a href="https://cs.arizona.edu/~hossain">
  <img typeof="foaf:Image" src="http://www2.cs.arizona.edu/~hossain/iqbal.png" width="188" height="188" alt=""></a>
  </div><div class="col-md-5">
  <h4><a href="https://cs.arizona.edu/~hossain">Md Iqbal Hossain</a></h4>

Md Iqbal Hossain  is a Research Scientist  of Computer Science at the University of Arizona. He works on information visualization, natural language processing and machine learning.
</div>
</div></div>

<div class="uaqs-person-row">
    <article class="node-236 node node-uaqs-person node-teaser clearfix" about="https://www2.cs.arizona.edu/~kobourov/" typeof="sioc:Item foaf:Document">

     <header>
               <span property="dc:title" content="Stephen Kobourov" class="rdf-meta element-hidden"></span>

          </header>

  <div class="row border-separator"><div class="col-md-3">
  <a href="https://www2.cs.arizona.edu/~kobourov/">
  <img typeof="foaf:Image" src="https://www2.cs.arizona.edu/~kobourov/kobourov_picture2016.jpg" width="188" height="188" alt=""></a>
  </div><div class="col-md-5">
  <h4><a href="https://www2.cs.arizona.edu/~kobourov/">Stephen Kobourov</a></h4>

Stephen Kobourov  is a Professor of Computer Science at the University of Arizona. He works on graph drawing and information visualization, geometric algorithms and data structures, human computer interaction, and pervasive computing.
</div>
</div></div>

<h1>Other Contributors</h1>

<div class="uaqs-person-row">
    <article class="node-236 node node-uaqs-person node-teaser clearfix" about="#" typeof="sioc:Item foaf:Document">

     <header>
               <span property="dc:title" content="Kimberly A Espy" class="rdf-meta element-hidden"></span>

          </header>

  <div class="row border-separator"><div class="col-md-3">
  <a href="#">
  <img typeof="foaf:Image" src="https://www.utsa.edu/today/2018/images/KimberlyEspy340.jpg" width="188" height="188" alt=""></a>
  </div><div class="col-md-5">
  <h4><a href="#">Kimberly A Espy</a></h4>

Kimberly Andrews Espy is the Provost and Vice President for Academic Affairs, University of Texas at San Antonio (UTSA)
</div>
</div></div>


<div class="uaqs-person-row">
    <article class="node-236 node node-uaqs-person node-teaser clearfix" about="#" typeof="sioc:Item foaf:Document">

     <header>
               <span property="dc:title" content="Randy Burd" class="rdf-meta element-hidden"></span>

          </header>

  <div class="row border-separator"><div class="col-md-3">
  <a href="#">
  <img typeof="foaf:Image" src="http://uacc.arizona.edu/sites/default/files/styles/medium/public/burd.jpg?itok=G0GaMlt5" width="188" height="188" alt=""></a>
  </div><div class="col-md-5">
  <h4><a href="#">Randy Burd</a></h4>

Randy Burd is the Senior VP for Academic Affairs, Long Island University
</div>
</div></div>


<div class="uaqs-person-row">
    <article class="node-236 node node-uaqs-person node-teaser clearfix" about="#" typeof="sioc:Item foaf:Document">

     <header>
               <span property="dc:title" content="Nirav Merchant" class="rdf-meta element-hidden"></span>

          </header>

  <div class="row border-separator"><div class="col-md-3">
  <a href="#">
  <img typeof="foaf:Image" src="https://datascience.arizona.edu/sites/default/files/styles/large/public/images/people/nirav_0_0.png?itok=DcYPOxZ3" width="188" height="188" alt=""></a>
  </div><div class="col-md-5">
  <h4><a href="#">Nirav Merchant</a></h4>

Nirav Merchant is the Director, UA Data Science Institute (Data7), The University of Arizona.
</div>
</div></div>


<div class="uaqs-person-row">
    <article class="node-236 node node-uaqs-person node-teaser clearfix" about="#" typeof="sioc:Item foaf:Document">

     <header>
               <span property="dc:title" content="Helen Purchase" class="rdf-meta element-hidden"></span>

          </header>

  <div class="row border-separator"><div class="col-md-3">
  <a href="#">
  <img typeof="foaf:Image" src="http://www.dcs.gla.ac.uk/~hcp/images/hcp.jpg" width="188" height="188" alt=""></a>
  </div><div class="col-md-5">
  <h4><a href="http://www.dcs.gla.ac.uk/~hcp/">Helen Purchase</a></h4>

Helen Purchase a Senior Lecturer, School of Computing Science, University of Glasgow.
</div>
</div></div>


<div class="uaqs-person-row">
    <article class="node-236 node node-uaqs-person node-teaser clearfix" about="#" typeof="sioc:Item foaf:Document">

     <header>
               <span property="dc:title" content="Mihai Surdeanu" class="rdf-meta element-hidden"></span>

          </header>

  <div class="row border-separator"><div class="col-md-3">
  <a href="#">
  <img typeof="foaf:Image" src="http://www.surdeanu.info/mihai/website/mihai/Surdeanu5-small.jpg" width="188" height="188" alt=""></a>
  </div><div class="col-md-5">
  <h4><a href="http://www.surdeanu.info/mihai/">Mihai Surdeanu</a></h4>

Mihai Surdeanu an Associate Professor, Computer Science at the University of Arizona.
</div>
</div></div>


"""

	return render(request, 'index.html', {'data':data})


def publications(request):
	data="""
      <h1>Publications</h1>
<table class="table table-hover" id="mapsubtype"> <tbody>
<tr><td>Randy Burd, Kimberly Andrews Espy, Md Iqbal Hossain, Stephen Kobourov, Nirav Merchant, and Helen Purchase. 2018. <a href="https://dl.acm.org/citation.cfm?id=3206531"><br>GRAM: global research activity map.</b></a> In Proceedings of the 2018 International Conference on Advanced Visual Interfaces (AVI '18). DOI: https://doi.org/10.1145/3206505.3206531 </td><td><a href="/static/papers/gram_AVI_2018.pdf">pdf</a></td></tr>
<tr><td>Md Iqbal Hossain, Stephen Kobourov, Helen Purchase, Mihai Surdeanu. 2018.
<a href="#"><br>REMatch: Research Expert Matching System.</b></a> In Proceedings of the  International Symposium on Big Data Visual and Immersive Analytics (BDVA '18). DOI:   </td><td><a href="/static/papers/REMatch_BDVA_2018.pdf">pdf</a> | <a href="/static/papers/rematch.key"> Presentation</a></td></tr>

<tr><td><a href="https://arxiv.org/abs/1706.04979">Research Topics Map: rtopmap</a></td><td><a href="/static/papers/research_topics_map.pdf">pdf</a></td></tr>
</tbody></table>


 <h1>Videos</h1>
<h3> <a href="https://www.youtube.com/watch?v=P35ss7MMVwA">Video</a></h3>
"""

	return render(request, 'index.html', {'data':data})


def vis(request,word):
	obj={}

	obj["Clustering"]=""
	obj["Citation"]=""
	obj["Fund"]=""
	obj["Connections"]=""
#	proc = Popen("python /home/hossain/processor3/webrequest/wordsource.py \"" + word + "\"" , stdout=PIPE, stdin=PIPE, stderr=PIPE, shell=True)
#	data, map_err = proc.communicate()
	data=uf.wordsource( word  )
	obj["data"]=data
	obj["r"]=random.random()
	return render(request, 'vis.html', {'data':obj})




def uamapX(request):
	obj={}
	print("request")
	submap = request.POST.get('submap', 'graph')
	topmap = request.POST.get('topmap', 'cmap')
	obj["submap"]=submap
	obj["txtsize"]=request.POST.get('txtsize', 'degree')
	overalys=request.POST.getlist('overlayvalue')
	obj["Clustering"]=""
	obj["Citation"]=""
	obj["Fund"]=""
	obj["Connections"]=""
	print(overalys)
	for ov in overalys:
		obj[ov]="Yes"
	print("Connections",obj["Connections"])


	if topmap=="cmap":
		return render(request, 'uamap5.html', {'data':obj})
	if topmap=="tmap":
		return render(request, 'topics1.html', {'data':obj})


def uamap(request, submap):
	obj={}
	print("request")
#	submap = request.POST.get('submap', 'graph')
	topmap = request.POST.get('topmap', 'cmap')

	#file = open('uamap/data/'+submap+'.js', 'r')
	#obj["data"]= file.read()



	obj["submap"]=submap

#	print(len(obj["data"]))

	print ("topmap", topmap)
	return render(request, 'uamap5.html', {'data':obj})



def cnetworkV4(request):
	obj={}
#	submap = request.POST.get('submap', 'graph')
	topmap = request.POST.get('topmap', 'cmap')

	#file = open('uamap/data/'+submap+'.js', 'r')
	#obj["data"]= file.read()



	obj["submap"]="graph"

#	print(len(obj["data"]))

	print ("topmap", topmap)
	return render(request, 'cnetworkV4.html', {'data':obj})





def cnetwork(request):
	obj={}
#	submap = request.POST.get('submap', 'graph')
	topmap = request.POST.get('topmap', 'cmap')

	#file = open('uamap/data/'+submap+'.js', 'r')
	#obj["data"]= file.read()



	obj["submap"]="graph"

#	print(len(obj["data"]))

	print ("topmap", topmap)
	return render(request, 'cnetwork.html', {'data':obj})


def lab(request):
	obj={}
	topmap = request.POST.get('topmap', 'cmap')
	obj["submap"]="graph"
	return render(request, 'lab.html', {'data':obj})

#see UAMAP-license.txt
#!/usr/bin/python

import pymongo
import sys, re

from array import *
from bson.code import Code



import urllib.request
from bs4 import BeautifulSoup
import time
import datetime




import mongoauth
client =mongoauth.auth(pymongo)
db = client.uamap

peopleserachbasedlocation="/home/hossain/processor4/matching/query/"
#uamapversion="V4"
uamapversion=""
def getDBConnection():
	return db

def getexternaledgeinfo(dummyid):

	networkVXdummyWithExternalConnection= eval('db.network'+uamapversion+'dummyWithExternalConnection')
	c=networkVXdummyWithExternalConnection.find({"dummyid": int(dummyid) })
	data=""
#	print(c)
#	print(dummyid)
	for u in c:
		data=data+u["jsstr"]


#	print(data)
	return data
	
def savecontent_info_to_db(netid, name,size, type,urls):
	t={'netid': netid, 'filename':name, 'filesize': size, 'category': type,'urls':urls}
	db.pdfs.insert(t)

def geturlcontent(url):

	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
	headers = { 'User-Agent' : user_agent }
	req= urllib.request.Request(url)
	#req = urllib.request(url)
	req.add_header('Referer', 'http://www.google.com/')
	req.add_header('User-Agent','Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
	req.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8')
	r = urllib.request.urlopen(req)
	html=r.read()
	soup = BeautifulSoup(html,  "html.parser")
	texts = soup.findAll(text=True)

	def visible(element):
		if element.parent.name in ['style', 'script', '[document]', 'head', 'title']:
		    return False
		elif re.match('<!--.*-->', str(element)):
		    return False
		return True

	visible_texts = list(filter(visible, texts))

	txt  = ''.join(visible_texts)
	txt=txt.replace("\n", " ")
	ts = time.time()
	qid = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d%H%M%S')
	t2={ 'quid': qid, 'query':txt, 'url':url}
	db.searchQuery.insert(t2)
	return qid, txt


def wordsource(phrase):

#	phrase=sys.argv[1]


	#c=db.unameid.find({'uname':x }).limit(10)
	#c=db.unameid.find({"uname": {'$regex': ".*" + txt + ".*"}})
	#c=db.unameid.find({"uname": x, "gsuid": {'$ne':"error"} }).limit(10)

	c=db.GSResearchPhrase.find({"stemmedPhrase":phrase})
	data="var nodes  = new vis.DataSet(["
	data=data+"  {id: 1, label: '"+phrase+"', level:0,  shape: 'circle' },"
	edgedata= "var edges = new vis.DataSet([  "

	i=1;
	for u in c:
		i=i+1;
	#	print ('<a href="#" onclick=\'getUniversitydata("' + u["gsuid"] + '", "' + u["uname"] + '")\'>' + u["uname"] + '</a>' )
		data=data+"  {id: "+ str(i ) +", label: '"+u["_id"] +" (" + str(int(u["value"])) +")"+"', level:1},"
		edgedata=edgedata + "{from: 1, to: " + str(i) + ",  arrows:'from' }, "
		text="," + u["_id"]+","
		text=re.escape(text)
	#	x=re.compile(text , re.IGNORECASE)
	#	regex2 = re.compile('.*({}).*'.format(text))
		x=re.compile('(%s)'%text,  re.IGNORECASE)

		d=db.gtopics.find({"phrases":x}).limit( 5 )
		j=i
		for r in d:
			i=i+1
			ph=r["phrases"][1:-1]
			data=data+"  {id: "+ str(i ) +",  shape: 'box' , label: '"+ph+"', level:2, url: 'https://scholar.google.com/citations?user="+ r["auid"] +"&hl=en'},"
			edgedata=edgedata + "{from: "+str(j)+", to: " + str(i) + ", arrows:'from' }, "




	data=data+"  ]);"
	edgedata=edgedata+"  ]);"



	data=data+ edgedata + "  var container = document.getElementById(\'mynetwork\');" + "  var data = {    nodes: nodes,    edges: edges  };"  + "  var options = {physics:true, layout: {          hierarchical: {         direction:'LR',   nodeSpacing: 100 , levelSeparation:500  }        },};"  + " var network = new vis.Network(container, data, options);";




	data=data+ " network.on('selectNode', function (params) {        if (params.nodes.length === 1) {            var node = nodes.get(params.nodes[0]);            window.open(node.url, '_blank');        }    });"


	f = open('./uamap/static/vis/data.js', 'wb')
	f.write(data.encode('utf-8'))
	f.close()
	return data


def searchfundsource(txt):
	x=re.compile(txt, re.IGNORECASE)
	proposalsmoneysourceid=eval('db.proposalsmoneysourceid'+ uamapversion)

	c=proposalsmoneysourceid.find({"source": x}).limit(10)
	returntext = ""
	for u in c:
		returntext = returntext+'<a href="#" onclick=\'getFundSourceData("' + u["code"] + '", "' + u["source"] + '")\'>' + u["source"] + '</a>'
	return returntext


def searchdept(txt):
	txt=" " +  txt.strip()+" "

	x=re.compile(txt, re.IGNORECASE)

	map = Code("function() {      var txt = this.refinedStemmedPhrases; txt = txt.split(\",\");          for (var i = txt.length - 1; i >= 0; i--) {           if (txt[i])  emit(txt[i], 1);          } }")
	reduce = Code("function( key, values ) {      var count = 0;        values.forEach(function(v) {     count +=v;        });    return count;}")

	result = db.gtopics.map_reduce(map, reduce,  "tmpdepartment", query={"university":x} )
	#result=db.tmpdepartment.find( )


	i=0
	z="var dept={"
	for u in result.find():
		z=z+   "\""+ u["_id"] + "\": "+ str( int(u["value"]) )+ ", "
	z=z+"}"

	z=''.join([i if ord(i) < 128 else ' ' for i in z])

	return z




def searchuniversity(txt):

	x=re.compile(txt, re.IGNORECASE)
	c=db.unameid.find({"uname": x, "gsuid": {'$ne':"error"} }).limit(10)
	returntext=""
	for u in c:
		returntext = returntext+ '<a href="#" onclick=\'getUniversitydata("' + u["gsuid"] + '", "' + u["uname"] + '")\'>' + u["uname"] + '</a>'
	return returntext


def getfundinfo(code):


	if code=="0":
		cond={"$match":{}}
	else:
		cond={"$match":{"code":code}}
	proposalsmoney=eval('db.proposalsmoney'+ uamapversion)

	cursor= proposalsmoney.aggregate([  cond ,{"$lookup": {            "from": "networkv3"+uamapversion+"dummy",            "localField": "userid",            "foreignField": "userid",            "as": "dummy"}} ,
	 { "$group": { "_id": {"userid":"$userid", "index":"$dummy.dummyid"}, "total": {    "$sum": "$amount"         }     } }
	] )

	d=""
	for doc in cursor:
		index=doc["_id"]["index"]
		money=doc["total"]
		if len(index)!=0:
			d=d+ "d["+ str(index[0]) + "]="+ str(money) + ";"

	returntext="var d={}\n"
	returntext= returntext+ d
	return returntext





def universityregion(regionid):

#	regionid=sys.argv[1]
	c=db.universityregion.find({'region':int(regionid)})
	d=''.join([i if ord(i) < 128 else ' ' for i in c[0]["topicscount"]])
	returntext= " "+ d + "; "
	returntext=   returntext+ "var peoplecount="+ str(int(c[0]["peoplecount"]))
	return returntext


def getuinfo(gsuid,overlaytype):
#	gsuid=sys.argv[1]
#	overlaytype=sys.argv[2]


	c=db.allUniversity.find({'gsuid':gsuid})
	d=''.join([i if ord(i) < 128 else ' ' for i in c[0][overlaytype]])
	returntext="var "+ d + ";\n"
	returntext=returntext+"var peoplecount="+ str(int(c[0]["peoplecount"]))
	return returntext


def getedgeinfo(n1, n2):

	returntext=""
	cur1=""
	cur2=""
	u1=""
	u2=""
	condition=""
	#print network
	networkVxNodes=eval('db.networkv3'+ ""+ 'dummy')
	network =eval('db.networkv3'+ uamapversion )

	cur1= networkVxNodes.find({"dummyid": int(n1) })
	cur2= networkVxNodes.find({"dummyid": int(n2) })

	for doc in cur1:
		u1=doc["userid"]
	for doc in cur2:
		u2=doc["userid"]
	condition={"userid":u1, "usertwoid":u2}
	condition2={"usertwoid":u1, "userid":u2}
	#print (condition)
	currentempl=eval('db.currentempl'+ "")
	cur=currentempl.find({'$or':[{"userid":u1}, {"userid":u2}]})
	i=0
	names= []

	for doc in cur:
		names.append(str(doc["shortname"]))
		i=i+1
	returntext=returntext+ "<b>" + names[0] + "</b> and <b>" + names[1] + "</b><br>"

	cur=network.find({'$or':[condition,condition2]} ).sort([('year',-1)]).limit( 10 )
	j=0
	for doc in cur:
		returntext=returntext+ str(doc["title"] ) + ", " + str( int(doc["year"]) ) + "<br>"
		j=j+1

	if j==10:
		returntext=returntext+"[...]"
	return returntext


def getedgeinfoV4(n1, n2):

	returntext=""
	cur1=""
	cur2=""
	u1=""
	u2=""
	condition=""
	#print network
	networkVxNodes=eval('db.network'+ uamapversion+ 'dummy')
	network =eval('db.network'+ uamapversion )

	cur1= networkVxNodes.find({"dummyid": int(n1) })
	cur2= networkVxNodes.find({"dummyid": int(n2) })

	for doc in cur1:
		u1=doc["userid"]
	for doc in cur2:
		u2=doc["userid"]
	condition={"userid":u1, "usertwoid":u2}
	condition2={"usertwoid":u1, "userid":u2}
	#print (condition)
	currentempl=eval('db.currentempl'+ uamapversion)
	cur=currentempl.find({'$or':[{"userid":u1}, {"userid":u2}]})
	i=0
	names= []

	for doc in cur:
		names.append(str(doc["shortname"]))
		i=i+1
	returntext=returntext+ "<b>" + names[0] + "</b> and <b>" + names[1] + "</b><br>"

	cur=network.find({'$or':[condition,condition2]} ).sort([('year',-1)]).limit( 10 )
	j=0
	for doc in cur:
		returntext=returntext+ str(doc["title"] ) + ", " + str( int(doc["year"]) ) + "<br>"
		j=j+1

	if j==10:
		returntext=returntext+"[...]"
	return returntext

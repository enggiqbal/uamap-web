isDown = false;
isDown3 = false;
isDown2 = false;

is_infodiv_down= false;
is_popupdiv_down=false;
is_graphdiv_down=false
function closethis(v)
{
	var x=document.getElementById(v)
x.style.display=""

} 
 



//Windowspreparation3(document.getElementById('infodiv2'), document.getElementById('infodiv1'), is_infodiv_down)
//Windowspreparation3(document.getElementById('graphdiv2'), document.getElementById('graphdiv1'), is_graphdiv_down)
//Windowspreparation3(document.getElementById('popupdiv2'), document.getElementById('popupdiv1'))


function Windowspreparation3(div, div2)
{
div2.addEventListener('mousedown', function(e) {
    is_popupdiv_down = true;
    offset = [
        div.offsetLeft - e.clientX,
        div.offsetTop - e.clientY
    ];
}, true);

document.addEventListener('mouseup', function() {
    is_popupdiv_down = false;
}, true);

document.addEventListener('mousemove', function(event) {
    event.preventDefault();
    if (is_popupdiv_down) {
        mousePosition = {
    
            x : event.clientX,
            y : event.clientY
    
        };
        div.style.left = (mousePosition.x + offset[0]) + 'px';
        div.style.top  = (mousePosition.y + offset[1]) + 'px';
    }
}, true);


}




function Windowspreparation2()
{

var div2=document.getElementById('infodiv2')

var div=document.getElementById('infodiv1')
div2.addEventListener('mousedown', function(e) {
    isDown2 = true;
    offset = [
        div.offsetLeft - e.clientX,
        div.offsetTop - e.clientY
    ];
}, true);

document.addEventListener('mouseup', function() {
    isDown2 = false;
}, true);

document.addEventListener('mousemove', function(event) {
    event.preventDefault();
    if (isDown2) {
        mousePosition = {
    
            x : event.clientX,
            y : event.clientY
    
        };
        div.style.left = (mousePosition.x + offset[0]) + 'px';
        div.style.top  = (mousePosition.y + offset[1]) + 'px';
    }
}, true);


}

function Windowspreparation()
{

var div2=document.getElementById('graphdiv2')

var div=document.getElementById('graphdiv1')
div2.addEventListener('mousedown', function(e) {
    isDown = true;
    offset = [
        div.offsetLeft - e.clientX,
        div.offsetTop - e.clientY
    ];
}, true);

document.addEventListener('mouseup', function() {
    isDown = false;
}, true);

document.addEventListener('mousemove', function(event) {
    event.preventDefault();
    if (isDown) {
        mousePosition = {
    
            x : event.clientX,
            y : event.clientY
    
        };
        div.style.left = (mousePosition.x + offset[0]) + 'px';
        div.style.top  = (mousePosition.y + offset[1]) + 'px';
    }
}, true);


}

function showmyedges(nodeindex) {
 
Windowspreparation();

document.getElementById("graphdiv").innerHTML="";


var edges={};
  var gnodes={};
var weight={};
	for (i = 0; i < E; i++) {
	if (topicsNode[nodeindex].i==edgesdata[i].i || topicsNode[nodeindex].i==edgesdata[i].j )
	{
//	edges["'"+topicsNode[edgesdata[i].i].n+"'"]=topicsNode[edgesdata[i].j].n;
	gnodes[  topicsNode[edgesdata[i].i].n  ]=1;
		gnodes[  topicsNode[edgesdata[i].j].n  ]=1;
 weight[ topicsNode[edgesdata[i].i].n ]= topicsNode[edgesdata[i].i].w
 weight[ topicsNode[edgesdata[i].j].n ]= topicsNode[edgesdata[i].j].w

	}
}

var nodelist=Object.keys(gnodes);
var nodevalue={}
 var n="";
	var i=0;
	for (var i=0; i< nodelist.length;i++)
	{
nodevalue[nodelist[i]]=i;

var w=weight[nodelist[i]]/100;
if (w<2 ) w=2;
if (w> 10) w=10;


if (nodelist[i]==topicsNode[nodeindex].n)
	n=n+'{"id": "'+ nodelist[i] +'",  "c":0, "w": "'+w+'"},';
else
	n=n+'{"id": "'+ nodelist[i] +'",  "c":1, "w": "'+w+'"},';

	} 
n=n.substring(0,n.length-1);
var l="";


	for (var i=0; i< nodelist.length;i++)
	{
	if(nodevalue[ topicsNode[nodeindex].n ] !=  nodevalue[nodelist[i]] )
	l=l+'{"source":  '+ nodevalue[ topicsNode[nodeindex].n ] +', "target": '+ nodevalue[nodelist[i]] +', "value": "1"},';

	} 
 

l=l.substring(0,l.length-1);

var nodetext='{"nodes": ['+ n+ '],';
var edgetext='"links": ['+ l+ ']}';

 var graph=nodetext + edgetext;

var data=JSON.parse(graph);
//console.log(data);
//console.log(nodeindex);
vis1(data);
var x=document.getElementById('graphdiv1')
x.style.display="block"
 

      }






function vis1(json, g=0.1, el=200,l=true)
{


//d3.select("svg").remove();
document.getElementById('graphdiv').innerHTML=""; 
var  color=["#ff77b4","#1f77b4"];


var width = 600,
    height = 600;
//var width = screen.availWidth,
//    height = screen.availHeight;

var svg = d3.select("#graphdiv").append("svg")
    .attr("width", width)
    .attr("height", height);

var force = d3.layout.force()
    .gravity(g)
    .distance(el)
    .charge(-100)
    .size([width, height]);


  force
      .nodes(json.nodes)
      .links(json.links)
      .start();

  var link = svg.selectAll(".link")
      .data(json.links)
    .enter().append("line")
      .attr("class", "link");// function(d){ return d.value;}); 
  var node = svg.selectAll(".node")
      .data(json.nodes)
    .enter().append("g") 
      .attr("class", "node")
      .call(force.drag);

 
 node.append("circle")
     .attr("r", function(d) { return d.w * 2;  })
      .attr("fill", function(d) { return color[d.c] });

if (l){
  node.append("text")
        .attr("x", -8)
      .attr("y", -8)
      .text(function(d) { return d.id });
}
  force.on("tick", function() {
    link.attr("x1", function(d) { return d.source.x; })
        .attr("y1", function(d) { return d.source.y; })
        .attr("x2", function(d) { return d.target.x; })
        .attr("y2", function(d) { return d.target.y; });

    node.attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
  });
 
}

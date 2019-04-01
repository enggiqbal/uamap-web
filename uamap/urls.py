"""
see UAMAP_license.txt for more details
"""
"""uamap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.views.generic import TemplateView
#from django.conf.urls import patterns, url
from uamap import  views

#urlpatterns = [
#	url(r'^$',  TemplateView.as_view(template_name='index.html')),
#	url(r'^uamap$',  TemplateView.as_view(template_name='uamap3.html')),
#	url(r'^admin/', admin.site.urls),
#	url(r'^getedgeinfo/(\d*)/(\d*)/(\d*)$', views.getedgeinfo, name='getedgeinfo'),
#]

urlpatterns = [
    url(r'^$',  views.index, name='index'),
    url(r'^publications/$', views.publications, name='publications'),
    url(r'^contributors/$', views.contributors, name='contributors'),
    url(r'^topics/(.*)$', views.topics, name='topics'),
    url(r'^peoplesearch/$', views.peoplesearch, name='peoplesearch'),
    url(r'^peoplesearch2/$', views.peoplesearch2, name='peoplesearch2'),
    url(r'^addstopwords/$', views.addstopwords, name='addstopwords'),
    url(r'^addstopwords2/$', views.addstopwords2, name='addstopwords2'),
    url(r'^peoplesearch3/$', views.peoplesearch3, name='peoplesearch3'),
    url(r'^docresearchtopics/(.*)$', views.docresearchtopics, name='docresearchtopics'),
    url(r'^addstopwords3/$', views.addstopwords3, name='addstopwords3'),
    url(r'^search$', views.search, name='search'),
    url(r'^search4$', views.search4, name='search4'),
    url(r'^search3$', views.search3, name='search3'),
    url(r'^cnetwork$', views.cnetwork, name='cnetwork'),
    url(r'^lab$', views.lab, name='lab'),
    url(r'^admin/', admin.site.urls),
    url(r'^getexternaledgeinfo/(\d*)$', views.getexternaledgeinfo, name='getexternaledgeinfo'),
    url(r'^getedgeinfo/(\d*)/(\d*)/(\d*)$', views.getedgeinfo, name='getedgeinfo'),
    url(r'^getuinfo/(.*)/(.*)$', views.getuinfo, name='getuinfo'),
    url(r'^universityregion/(\d*)$', views.universityregion, name='universityregion'),
    url(r'^getfundinfo/(\d*)$', views.getfundinfo, name='getfundinfo'),
    url(r'^searchuniversity/(.*)$', views.searchuniversity, name='searchuniversity'),
    url(r'^getfunOranizationList/(.*)/(.*)$', views.getfunOranizationList, name='getfunOranizationList'),
    url(r'^searchdept/(.*)$', views.searchdept, name='searchdept'),
    url(r'^selecteddepartments/(.*)$', views.selecteddepartments, name='selecteddepartments'),
    url(r'^selectedbuilding/(.*)$', views.selectedbuilding, name='selectedbuilding'),
    url(r'^searchfundsource/(.*)$', views.searchfundsource, name='searchfundsource'),
    url(r'^vis/(.*)$', views.vis, name='vis'),
    url(r'^topicsnetwork/', views.topicsnetwork, name='topicsnetwork'),
    url(r'^savefeedback', views.savefeedback, name='savefeedback'),
	url(r'^sendemail', views.sendemail, name='sendemail'),
	url(r'^getFederalFund/(.*)/(.*)/(.*)/(.*)', views.getFederalFund, name='getFederalFund'),


    url(r'^cnetworkV4$', views.cnetworkV4, name='cnetworkV4'),
    url(r'^peoplesearchV4/$', views.peoplesearchV4, name='peoplesearchV4'),
    url(r'^searchV4$', views.searchV4, name='searchV4'),

]

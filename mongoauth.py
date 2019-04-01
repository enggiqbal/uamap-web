#see UAMAP-license.txt
import os
print(os.environ['mogoconnection'])

def auth(pymongo):
   return pymongo.MongoClient('mongodb://hossain:myMPassForDocker819@mongodb_container:27017/')

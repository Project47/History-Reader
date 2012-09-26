from sqlalchemy import create_engine, Column, MetaData, Table
from sqlalchemy import Integer, String, Text
from sqlalchemy.orm import mapper, sessionmaker
import fnmatch
import os


class HistoryReader(object):
    pass

 
def loadSession():
    dbPath = '/home/anuj/.mozilla/firefox/7g7j3x4g.default/places.sqlite'
    matches = []
    for root, dirnames, filenames in os.walk('/home'):
      for filename in fnmatch.filter(filenames, 'places.sqlite'):
          matches.append(os.path.join(root, filename))
    print len(matches)
    for u in matches:
	print u
    dbPath=matches[0]
    engine = create_engine('sqlite:///%s' % dbPath, echo=True)
 
    metadata = MetaData(engine)    
    moz_places = Table('moz_places', metadata, 
                          Column('id', Integer, primary_key=True),
                          Column('url', String),
                          )
 
    mapper(HistoryReader, moz_places)
 
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
 
if __name__ == "__main__":
    session = loadSession()
    records = session.query(HistoryReader).all()
    char_list=[]
    website_name=""
    name_list=[]
    count_list=[]
    list_count=0

    for i in range (0,len(records)):  
	slashCount=0
	char_count=0
	website_name=""
	while len(char_list) > 0 : char_list.pop()
	while slashCount<3: 
		if char_count == len(records[i].url):
			break		
		char_list.append(records[i].url[char_count])	
		if records[i].url[char_count] == '/':
	        	slashCount=slashCount+1
		char_count=char_count+1
 
	if slashCount==3:
		char_list.append('\0')
		for x1 in char_list:	
			website_name=website_name+str(x1)
		char_count=0;
		while char_count<list_count:
			if name_list[char_count] == website_name:
				count_list[char_count]=count_list[char_count]+1
				break
			char_count=char_count+1
		
		if char_count==list_count:
			name_list.append(website_name)
			list_count=list_count+1
			website_name=""
			count_list.append(1)

    temp=0
    tempName=""	
    for j in range (0,list_count-1):
       for i in range (0,list_count-1):
	  if count_list[i]<count_list[i+1]:
		temp=count_list[i]
		count_list[i]=count_list[i+1]		
		count_list[i+1]=temp
		tempName=name_list[i]
		name_list[i]=name_list[i+1]		
		name_list[i+1]=tempName	
			
    for i in range (0,list_count):
	#print "\n" + str(name_list[i]) + "    " + str(count_list[i])
    	print  str(count_list[i]) +"\t" +  name_list[i] 
    
		
  


    	

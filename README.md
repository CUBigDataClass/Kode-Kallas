
# Kode - Kallas


  

## Modules

|Name  | Progress |
|--|--|
|  Github-Crawler| Done|
| Ellasandra-API|Done|
|Dashboard-backend|Done|
|Dashboard-Frontend|Done|


    **Github-Crawler Setup**

 1) Install and keep following software
 

 - Docker
 - Python-Flask
 - Python3
 - ElasticSearch
 - pip install flask 
 - pip install elasticsearch 

2) Run Below Comands after starting Docker
	```
	docker pull docker.elastic.co/elasticsearch/elasticsearch:7.6.2
	```
	``` 
	docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.6.2 
	```
	```
	docker pull docker.elastic.co/kibana/kibana:7.6.2
	```
	```
	docker run --link YOUR_ELASTICSEARCH_CONTAINER_NAME_OR_ID:elasticsearch -p 5601:5601 kibana:7.6.2
	```
3) Set-up ElasticSearch (Important)
   navigate to [http://localhost:5601/app/kibana#/dev_tools/console?_g=()](http://localhost:5601/app/kibana#/dev_tools/console?_g=())
   copy and past each and every file from **github-crawler/Templates_commands** into above console (list of files is given below)

         * single_commit.txt
         * repos_command.txt
         * put_org_index.txt
         * users_command.txt
    

3) Starting github-crawler and usage

		git clone https://github.com/CUBigDataClass/Kode-Kallas.git
		cd Kode-Kallas/github-crawler
	    python3 app.py
navigate to
-  http://127.0.0.1:5000  -- you will be able to see proper message
- http://127.0.0.1:5000/org/<!orgname_should be added here>  - Just check server logs  

5) For stopping and starting your docker images	

	     $ docker ps -a    	
	     $ docker stop 0d93ff4520e6 ( copy here your Kibana container ID instead of my Container ID)	
	     $ docker stop d7edc0290546 ( copy here your Elasticsearch container ID instead of my Container ID)	
	     $ docker start 0d93ff4520e6 ( copy here your Kibana container ID instead of my Container ID)	
	     $ docker start d7edc0290546 ( copy here your Elasticsearch container ID instead of my Container ID)	

Done with Github Crawler Setup!

    **Ellasandra API setup**

6) Install Docker and run below cammands

	    docker run -d -p 9200:9200 -p 9042:9042 --name my-elassandra strapdata/elassandra
	    cd elassandra-api	 
	    python3 app.py
	   
Link to postman apis: https://www.getpostman.com/collections/034caa33048a99cfb99a	   
	
7) Setting up index for elasticsearch in elassandra
	```
	
	```curl -XPUT -H 'Content-Type: application/json' http://localhost:9200/repo -d'{"mappings":{"repo":{"discover":".*"}}}'
	
	```curl -XPUT -H 'Content-Type: application/json' http://localhost:9200/users -d'{"mappings":{"users":{"discover":".*"}}}'
	
	```curl -XPUT -H 'Content-Type: application/json' http://localhost:9200/commit -d'{"mappings":{"commit":{"discover":".*"}}}'

Done With Ellasandra API setup

    **Dashboard Backend setup**

8) Install Python3 and run below cammands

	    cd github-analytics
	    python3 app.py
	    
Done With Dashboard Backend setup

    **Dashboard Frontend setup**

9) Install python3 and Django and run below cammands

	    cd django/bdaSite
	    python3 app.py
	    python3 manage.py runserver 0.0.0.0:5000
	    



10) Below some Documentation


|**Module**  | **Usage** | **Requirements**|
|--|--|--|
|Github-Crawler|Used to get Github organization info |Docker and Python3|
|Ellasandra API|Used to bulk write on to cassandra |Docker and Python3|
|Github-Analytics|Used to serve dashboard with elastic data |Docker and Python3|
|Django|FrontEnd Tool for Github visualization  |Django and Python3|


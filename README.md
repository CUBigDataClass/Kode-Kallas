# Kode - Kallas


  

## Modules

|Name  | Progress |
|--|--|
|  Github-Crawler| In-Progress|
| Github-Analyser|In-Progress|
|Dashboard-backend||
|Dashboard-Frontend||


    Github-Crawler Setup

 1) Install and keep following software
 

 - Docker
 - Python-Flask
 - Python3
 - ElasticSearch
 - 

2) Run Below Comands after starting Docker

		docker run -p 9200:9200 -p 9300:9300 -e "discovery.type=single-node" docker.elastic.co/elasticsearch/elasticsearch:7.5.2
	```
	docker run -d --name kibana --net somenetwork -p 5601:5601 kibana:tag
	```
3) Set-up ElasticSearch (Important)
   navigate to [http://localhost:5601/app/kibana#/dev_tools/console?_g=()](http://localhost:5601/app/kibana#/dev_tools/console?_g=())
   copy and past each and every file from **github-crawler/Templates_commands** into above console (list of files is given below)

         * comments_command.txt
         * repos_cammand.txt
         * put_org_index.txt
    

3) Starting github-crawler and usage

		git clone https://github.com/CUBigDataClass/Kode-Kallas.git
		cd Kode-Kallas/github-crawler
	    python3 app.py
navigate to
-  http://127.0.0.1:5000  -- you will be able to see proper message
- http://127.0.0.1:5000/org/<!orgname_should be added here>  - Just check server logs  

4) For stopping and starting your docker images

	     $ docker ps -a    
	     $ docker stop 0d93ff4520e6 ( copy here your Kibana container ID instead of my Container ID)
	     $ docker stop d7edc0290546 ( copy here your Elasticsearch container ID instead of my Container ID)
	     $ docker start 0d93ff4520e6 ( copy here your Kibana container ID instead of my Container ID)
	     $ docker start d7edc0290546 ( copy here your Elasticsearch container ID instead of my Container ID)


4) Below some Documentation

		 Work Under progress

|**Module**  | **Usage** | **Requirements**|
|--|--|--|
|Github-Crawler|Used to get Github organization info |Docker and Python3|
# Kode - Kallas


  

## Modules

|Name  | Progress |
|--|--|
|  Github-Crawler| In-Progress|
| Github-Analyser|In-Progress|
|Dashboard-backend| In-progress|
|Dashboard-Frontend||


    Github-Crawler Setup

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

         * comments_command.txt
         * repos_command.txt
         * put_org_index.txt
    

3) Starting github-crawler and usage

		git clone https://github.com/CUBigDataClass/Kode-Kallas.git
		cd Kode-Kallas/github-crawler
	    python3 app.py
navigate to
-  http://127.0.0.1:5000  -- you will be able to see proper message
- http://127.0.0.1:5000/org/<!orgname_should be added here>  - Just check server logs  

4) For stopping and starting your docker images	

	     $ docker ps -a    	
	     $ docker stop 0d93ff4520e6 ( copy here your Kibana container ID instead of my Container ID)	
	     $ docker stop d7edc0290546 ( copy here your Elasticsearch container ID instead of my Container ID)	
	     $ docker start 0d93ff4520e6 ( copy here your Kibana container ID instead of my Container ID)	
	     $ docker start d7edc0290546 ( copy here your Elasticsearch container ID instead of my Container ID)	


5) Cassandra api setup

	    docker run -e DS_LICENSE=accept --memory 4g -p 7000:7000 -p 7001:7001 -p 7199:7199 -p 9042:9042 -p 9160:9160 -p 9404:9404 --name my-dse -e CASSANDRA_START_RPC=true -d datastax/dse-server:6.8.0
	    docker start my-dse
	 
    Prereq: Install flask and cassandra-driver using pip.

	    python3 app.py
	   
Link to postman apis: https://www.getpostman.com/collections/034caa33048a99cfb99a	   
	   




6) Below some Documentation


|**Module**  | **Usage** | **Requirements**|
|--|--|--|
|Github-Crawler|Used to get Github organization info |Docker and Python3|

7)Elassandra setup

	docker-compose up
	
8) Setting up index for elasticsearch in elassandra
	
	```curl -XPUT -H 'Content-Type: application/json' http://localhost:9200/repo -d'{"mappings":{"repo":{"discover":".*"}}}'
	
	```curl -XPUT -H 'Content-Type: application/json' http://localhost:9200/users -d'{"mappings":{"users":{"discover":".*"}}}'
	
	```curl -XPUT -H 'Content-Type: application/json' http://localhost:9200/commit -d'{"mappings":{"commit":{"discover":".*"}}}'

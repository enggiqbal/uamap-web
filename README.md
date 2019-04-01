# UAMAP-web
This web application visualize  topics map. It enables user interactions (i.e., zooming, panning, and navigation ) on the map. The repository contains a part of UAMAP application. Please visit UAMAP website [http://uamap-dev.arl.arizona.edu](http://uamap-dev.arl.arizona.edu) for more details.  

# Running application
## Step1
setup http port: the default port setting in docker-compose.yml is `8080`. If `8080` port is already used then set your target port number at `docker-compose.yml`
```
  web:
  ....
  ....
    ports:
     - "PORT:8000"
    ....
    ....
```
## Step2
run docker composer
```
docker-compose up -d
```
For docker and docker composer please visit [docker website](https://www.docker.com/)
## Step3
load application in the borwser at `PORT`
default home page: http://localhost:8080/   topics map: http://localhost:8080/topics/
## Optional parameters settings
- change `mongodb` username and password at `docker-compose.yml`
- change google maps api key at `uamap/templates/topics2.html`
```
    <script async defer src="https://maps.googleapis.com/maps/api/js?key=`YOUR_GOOGLE_MAPS_API_KEY`&callback=initMap&libraries=visualization">
```


# What to expect
![alt text](pictures/topics_map.png?raw=true)
click on HPU icon then search University of Arizona. You will see like this
![alt text](pictures/hpu_ua.png?raw=true)

# How to run for different dataset
coming soon


# Techincal Details
```
@inproceedings{burd2018gram,
  title={GRAM: global research activity map},
  author={Burd, Randy and Espy, Kimberly Andrews and Hossain, Md Iqbal and Kobourov, Stephen and Merchant, Nirav and Purchase, Helen},
  booktitle={Proceedings of the 2018 International Conference on Advanced Visual Interfaces},
  pages={31},
  year={2018},
  organization={ACM}
}
```
[https://dl.acm.org/citation.cfm?id=3206531](https://dl.acm.org/citation.cfm?id=3206531)
```
@inproceedings{hossain2018rematch,
  title={REMatch: Research Expert Matching System},
  author={Hossain, Md Iqbal and Kobourov, Stephen and Purchase, Helen and Surdeanu, Mihai},
  booktitle={2018 International Symposium on Big Data Visual and Immersive Analytics (BDVA)},
  pages={1--10},
  year={2018},
  organization={IEEE}
}
```
[https://ieeexplore.ieee.org/abstract/document/8534021](https://ieeexplore.ieee.org/abstract/document/8534021)

# License
license details are at UAMAP_license.txt

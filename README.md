<h1>
**** PHOTO TWIST ****
</h1>


This app will help You to manage Your photos, by making Albums, upload photos and describe them. 


But also will help You to change Your photos from this...

![Alt text](misc/back.jpg)



##INTO THIS....

![Alt text](misc/background.png)  



## Running up

#### Requirements

If You want to download and run this app, You need to install `Docker` and `Docker-compose` first


#### Docker image build

Go to main folder, where is `Dockerfile`, `requirements.txt` and `docker-compose.yml`

type:
#### 1. $ sudo docker-compose build

if success You should see this:

`Step 1/6.....  `
  
`Step 5/6: RUN pip install -r requiremets.txt`  

`Step 6/6`  
`Successfully tagged album_na_zdjecia:latest`

#### 2. $ sudo docker-compose run django python src/manage.py makemigrations
#### 3. $ sudo docker-compose run django python src/manage.py migrate
#### 4. $ sudo docker-compose up
#### 5. Open Your browser and type `localhost:8000/album`

        

        
        



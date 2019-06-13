# A-2019-backend

## Overview
* The App server will send an url of the image to the backend using JSON format.
* The backend will download this image on the server and call the **color** recognition part to get the color result of this image.
* The backend will use this color result to match the good facts in our kb, 
and see if there is good matching color, and if there exists matching color, then we try to find whether there 
exists such cloth that has this color. If not, then we just randomly recommend the clothes to the user based on 
other contraints we have in our kb. And currently our constraints are based on the weather, occasion, color and what clothes the user already has in their wardrobe.

## Installation
### Configure AMS Server
* We use Amazon GPU server because we have ML model, the one we have is [p2.xlarge model](https://console.aws.amazon.com/ec2/v2/home?region=us-east-1#Instances:sort=availabilityZone).
* After you have this server, download the private key from the AWS website, keep it in somewhere in your local desktop. (In my case, I store it in ~/Downloads)
* Open the terminal in your computer, and run the following command. Type "yes" for the second command.
```sh
$ cd Downloads/
$ ssh -i "GPU-FashionAI.pem" ubuntu@ec2-52-71-250-83.compute-1.amazonaws.com
```

### Run Django Apps on server
* First, you need to activate the environment in order to run our app. To do this, type below command. This environment is pre-installed by AWS, so it's much more convenient.
```sh
$ source activate pytorch_p36
```
* Clone the repository to the server. (In my case, I put it inside ~/django-apps/testsite/)
```sh
$ git clone https://github.com/nuvention-web/A-2019-backend.git
$ cd django-apps/testsite/
```
* After you finish the above procedure, you can run the django backend server by typing the below command:
```sh
$ python manage.py runserver 0:8000
```
There is another way to run server, the above one will disconnect from time to time. The below one will suspend the server and will not disconnect from time to time.
```sh
$ nohup python manage.py runserver 0:8000 &
```

## Contact
* If you need our AWS Server account information or there is problem running the server, please contact:
Chenghong Lin <ChenghongLin2020@u.northwestern.edu >

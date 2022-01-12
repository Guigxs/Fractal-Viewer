# Fractal-Viewer

This project is for the Scalable Architecture lesson.

## Server build

### Set up a worker

#### Manually

For setting up a worker manually, just go to the *./server/worker* folder and run :
```bash
$ pip install -r requirements.txt
$ python setup.py build_ext --inplace
$ python worker.py
```
> Note: Using a virtual environement is a good practice.

#### With docker

For setting up a worker with docker, just go to the *./server/worker* folder and run :
```bash
$ docker build . -t worker:latest
$ docker run --name worker-1 -p 8181:8181 worker:latest
```
> Note: Consider deploying multiple wokers in order to have a fluid experience.

### Set up the load balancer

To build the server, update the *nginx.conf* file the in the *./server/* folder with you workers informations.

Then run: 
```bash
$ docker build . -t load-balancer
$ docker run --name lb -p 8180:80 load-balancer
```

## Run the client 

To run the client juste go to the *./client/* folder and run :
```bash
$ pip install -r requirements.txt
$ python app.py
```

> Note: You may need to update the ENPOINT address in the *app.py* file. 
> Note 2: Using a virtual environement is a good practice.
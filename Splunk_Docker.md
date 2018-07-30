## How to run splunk in a container
It's something you can do to quickly spin up a splunk instance and play with it. I've been running it at the house for months without issue.
You can also use this to spin up a splunk dev environment.

Obviously you'll need to install docker first. There are all kinds of tutorials for it, and it's pretty easy.
The docker docs are really good. 
* [Docker Getting Started](https://docs.docker.com/get-started/#docker-concepts)

You might also need a dockerhub account (can't remember if I had to login first to pull the image).

The docs and more info on the splunk image can be found here:
* [Splunk on DockerHub](https://hub.docker.com/r/splunk/splunk/)



####1. Setup persistent volumes
Not sure if this is a good idea or not, but I wanted to be able to see/modify my .conf files without going into 
the container. I also wanted the config and the data collected to be persistent if the contianer 
shuts down for any reason.

 
```bash
docker volume create splunk_etc
docker volume create splunk_var
docker volume create splunk_db
docker volume ls

```
The first three commands create three new docker volumes. 
* splunk_etc will map to /opt/splunk/etc
  * This is where all the splunk .conf files reside. 

* splunk_var will map to /opt/splunk/var
  * This biggest thing on this volume will be your splunk logs for the container. You probably don't need this
  but I thought it would be good idea to persist the splunk logs in the event that the container dies
  and I want to see why. I'm sure I could have just inspected the stopped container and found where it was, but meh.
  
* splunk_db will map to /opt/splunk/dbs
  * I added an additional vmdk to the docker host and mounted it to /var/lib/docker/volumes/splunk_db/_data
    * when you create a docker volume, it puts it in /var/lib/docker/volumes and adds the _data folder. If you mount
    the additional disk in that folder, you have a dedicated disk to the contianer. I'm not 100% sure that's a good idea
    but, meh. works for me.
  * In the splunk indexes.conf I will map hot and cold volumes to directories inside the /opt/splunk/dbs directory
    * ```text 
      [volume:hot]
      path = /opt/splunk/dbs/hot
      maxVolumeDataSizeMB = 500000
      
      [volume:cold]
      path = /opt/splunk/cold
      maxVolumeDataSizeMB = 150000           
      ```  
  * for more information on splunk volumes check out [Managing Indexes in the splunk docs](https://docs.splunk.com/Documentation/Splunk/7.1.2/Indexer/Configureindexstoragesize)

* The final command lists all of your docker volumes and you should see the three you just created, 
along with a bunch of other guids volumes. These are the "hard drives" for your containers.
  * just a quick note, you can use `docker volume prune` to clean up (remove) the volumes you aren't using.
####2. Start the Splunk Container

Just a note about the splunk/splunk:latest container (currently 7.1.2). It's kinda broken. When you run it, it dies. But don't worry, it will work. 
There is something fuckered up in a python script they have running. It tries to run shutils function to delete a directory
but the directory isn't empty, so the entrypoint script (entrypoint.sh) exits and therefore the contianer stops. Super frustrating... trust me.

But complete the following steps and you'll have your containerized splunk instance running. Well... at least I did. 

Start the container:

```bash
docker run -d \
-e "SPLUNK_START_ARGS=--accept-license --seed-passwd yourpassword" \
--name splunk \
-p "8000:8000" \
-p "8089:8089" \
-p "8191:8191" \
-p "9997:9997" \
-p "1514:1514/udp" \
splunk/splunk

```

A quick explanation of the docker run command above:

This says run the container in detached mode and print the container id
```bash
docker run -d \
```

The next piece is an arbitrary name you want to use to identify the container

```bash
--name splunk \
```

This inserts environmental variables into the running container. The `--accept-license` is used by Splunk to eliminate the need
for you to scroll through the license and hit yes at the end.

The  `--seed-passwd` is new (as far as I know), in 7.1.2, it allows you to put in a password for the admin account. In the version
I used to run, the default password for the admin account was changeme 

I haven't tried skipping it to see if it defaults to changeme.
```bash
-e "SPLUNK_START_ARGS=--accept-license --seed-passwd yourpassword" \
```

Next come the port mappings. These expose the ports required to use splunk. 
For a full list of ports, check out this [Splunk Answers Page](https://answers.splunk.com/answers/118859/diagram-of-splunk-common-network-ports.html).
This one calls for UDP port 1514 be exposed on both sides (host and container). This is usually used if you want to ingest 
syslog directly into the indexer (not recommended). 
```bash
-p "8000:8000" \
-p "8089:8089" \
-p "8191:8191" \
-p "9997:9997" \
-p "1514:1514/udp" \
```

And finally, the image you want to spin up.

```bash
splunk/splunk
```


#### 3. Restart the container

Becuase something is fuckered up in the entrypoint script, the container will spin up, do it's thing, then die.

But, everything should be in place. All you have to do is start the container. 

```bash
docker start splunk
```

NOTICE this is a docker start, not a docker run. Docker run will spin up a container from an image. Docker start, starts
a container that has already been created, but is stopped.

You can see what containers are running with the following command

```bash
docker ps 
```

To see what containers are present (running or not) use this command

```bash
docker ps -a
```

#### 4. Splunk everything
At this point you should be able to web to http://[dockerhostip]:8000

The webpage will ask you for the seeded password you gave it in the docker run command in step 2.

You should also be able to see all of your files by going to the directory displayed in the following command, where
splunk_etc is the name of the volume you created in step 1 for /opt/splunk/etc.

```bash
docker volume inspect --format="{{ .Mountpoint }}"  splunk_etc
```

Have fun. For more information on Splunk, check out the [Our Splunk Resources Page](Splunk.md)... 

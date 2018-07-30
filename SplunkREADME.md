# Splunk Resources

## How to run splunk in a container
It's something you can do to quickly spin up a splunk instance and play with it. I've been running it at the house for months without issue.

Obviosly you'll need to install docker first. There are all kinds of tutorials for it, and it's pretty easy.
You might also need a dockerhub account (can't remember if I had to login first to pull the image).

Docs and more info on the container can be found here
* https://hub.docker.com/r/splunk/splunk/

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
I will add a full walk through, but wanted to get this up here.

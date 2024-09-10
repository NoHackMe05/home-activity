# Network Monitoring Activity

Monitor home network activity and screen time for family members

## Install

### Installing Python packages (root) :

```
python3 -m venv mon_env
source mon_env/bin/activate
pip install -r requirements.txt
deactivate
```

### Creating the configuration file

```
cp .env.example .env
```

### Creating the json files

```
cp json/identity.json.example json/identity.json
cp json/surveillance.json.example json/surveillance.json
cp json/uphosts.json.example json/uphosts.json
```

## Setting

The following variables must be configured in the .env file:

- range : your network's ip range
- API_ENDPOINT : url to the api that will manage mail delivery
- API_KEY : api key for API_ENDPOINT

In the forcron.sh file, you can add or modify network interfaces :

```
interfaces=("enp0s3")
```

## CRON JOB (ROOT)

```
*/5 * * * * sh /XXX/scan/forcron.sh
30 11 * * 1 sh /XXX/scan/forcron.sh info
```

Replace XXX with the installation directory

## How it works

Every 5 minutes, we run an ARP scan on the network to find the machines present. As soon as a new machine is found, we'll receive an e-mail containing a unique id. This unique id refers to a text file in the “data” directory. This file will contain three pieces of information:

- IP address
- MAC address
- MAC address sha256

### Role of json files

- identity.json: associates a name with a MAC address
- surveillance.json: hosts to be monitored for timekeeping purposes
- uphosts.json: hosts known on the network

The files surveillance.json and uphosts.json contain a sha256 list of MAC addresses.

## Activity report

Every Monday morning, we search the sqllite database for the past week's activities. A text report will be sent by e-mail via the API you must have developed. Old statistics (older than 8 days) will be deleted.

## TODO

A little clearer documentation :)
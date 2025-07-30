# DYNDNS to Hetzner

A DynDNS2 endpoint that changes DNS records using the Hetzner DNS API.

## Running

### Non-Docker

It is recommended to create a virtual environment for this project.

```
cd /opt # can be somewhere else if you prefer
python3 -m venv dyndns-to-hetzner
source dyndns-to-hetzner/bin/activate
pip install dyndns-to-hetzner
flask --app dyndns_to_hetzner init-config
```

The last command will print the location of the configuration file. Adjust it to your needs.

It is recommended to use a WSGI server to run this project, e.g. gunicorn:

```
pip install gunicorn
gunicorn -w 4 'dyndns_to_hetzner:create_app()' --access-logfile=- --bind="0.0.0.0:5000"
```

Setting up a reverse proxy such as nginx, apache or traefik is recommended if you want to access dyndns-to-hetzner from a different host.

### Docker

There is no official image available via a repository, the provided docker-compose file builds the image when started.  

You will need to clone the repository due to this.

```
git clone https://github.com/faeyben/dyndns-to-hetzner.git
cd dyndns-to-hetzner/docker
cp -a ../config.py.example config.py
```

Adjust the config.py to your liking.

```
docker-compose up -d
```

Setting up a reverse proxy such as nginx, apache or traefik is recommended if you want to access dyndns-to-hetzner from a different host.

## Using

The update mechanism will be available at `http://HOST_IP:5000/nic/update` and expects the `hostname` and `myip` GET parameters, whereas `hostname` is the DNS record you want to update and `myip` is the IP you want the record to be set to.

Example: `http://HOST_IP:5000/nic/update?hostname=home.example.com&myip=198.51.100.42`

Access will only be granted after a successful HTTP Basic Authentication.

### FRITZ!Box

FRITZ!Box routers allow setting up a DynDNS provider so the router sends an update to DynDNS anytime its public IP address changes. The following settings are required for that:

1. Update-URL: `http://HOST_IP:5000/nic/update?&myip=<ipaddr>&hostname=<domain>` (replace HOST_IP with the IP address or hostname of the server that dyndns-to-hetzner is running on, use https instead of http if SSL/TLS is enabled via a reverse proxy on the host)
2. Domainname: The FQDN of the record you want to have changed
3. Username: A username you set in the config.py
4. Password: The corresponding password you set in the config.py

After saving, the FRITZ!Box should issue a first update request within a few seconds.
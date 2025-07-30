import os
import sys

from flask import Flask, request, current_app, g, abort
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash
import requests
import json
import click


HETZNER_API = "https://dns.hetzner.com/api/v1"


class ZoneNotFoundError(Exception):
    pass


class RecordNotFoundError(Exception):
    pass


def find_zone_id_of_fqdn(api_key: str, fqdn: str) -> str | None:
    """Find the ID of the zone for the FQDN

    It gets all zones that the given api key has access to and
    compares the 'name' value of any zone with the domain part
    of the given FQDN
    """
    current_app.logger.debug("Looking up zone for " + fqdn)
    domain = ".".join(fqdn.split(".")[-2:])
    current_app.logger.debug("Looking for a zone with the name " + domain)
    response = requests.get(
        url=HETZNER_API + "/zones",
        headers={"Auth-API-Token": api_key},
    )
    if response.status_code != 200:
        abort(response.status_code)
    all_zones = json.loads(response.content)["zones"]
    for zone in all_zones:
        if zone["name"] == domain:
            current_app.logger.debug("Found zone id: " + zone["id"])
            return zone["id"]

    return None


def find_record_id_of_fqdn(api_key, zone_id, fqdn) -> str | None:
    """Find the ID of the record for the FQDN

    It gets all records in the given zone and compares their 'name'
    value with the subdomain part of the given fqdn.
    """
    subdomain = ".".join(fqdn.split(".")[:-2])
    response = requests.get(
        url=HETZNER_API + "/records",
        params={"zone_id": zone_id},
        headers={"Auth-API-Token": api_key},
    )
    if response.status_code != 200:
        abort(response.status_code)
    all_records = json.loads(response.content)["records"]
    for record in all_records:
        if record["name"] == subdomain:
            current_app.logger.debug("Found request id: " + record["id"])
            return record["id"]

    return None


def update_record(api_key, zone_id, record_id, fqdn, value) -> None:
    """Send a PUT request to the Hetzner DNS API to update the record"""
    subdomain = ".".join(fqdn.split(".")[:-2])
    response = requests.put(
        url=HETZNER_API + "/records/" + record_id,
        headers={
            "Content-Type": "application/json",
            "Auth-API-Token": api_key,
        },
        data=json.dumps(
            {"value": value, "type": "A", "name": subdomain, "zone_id": zone_id}
        ),
    )
    if response.status_code != 200:
        current_app.logger.debug(response.content)
        abort(response.status_code)


def update_hetzner_dns_record(api_key, fqdn, ip) -> None:
    """Entry function for actually updating the DNS record"""
    zone_id = find_zone_id_of_fqdn(api_key, fqdn)
    if zone_id is None:
        current_app.logger.error("Unable to find zone for " + fqdn)
        raise ZoneNotFoundError
    record_id = find_record_id_of_fqdn(api_key, zone_id, fqdn)
    if record_id is None:
        current_app.logger.error("Unable to find record for " + fqdn)
        raise RecordNotFoundError
    update_record(api_key, zone_id, record_id, fqdn, ip)


@click.command("init-config")
def init_config():
    try:
        import secrets

        os.makedirs(current_app.instance_path, exist_ok=True)
        secret_key = secrets.token_hex()
        with open(f"{current_app.instance_path}/config.py", "x") as conffile:
            conffile.write(
                f"""SECRET_KEY = "{secret_key}",
# What FQDNs should be managed and their respective API key to use
FQDNS = {{
    'dyn1.example.com': 'api_key1',
    'dyn2.example.com': 'api_key2'
}}
# Authentication data
# Generate a password hash using the following command:
# python -c 'from werkzeug.security import generate_password_hash ; print(generate_password_hash("YOUR_PASSWORD_HERE"))'
# DO NOT PUT PASSWORDS IN CLEARTEXT HERE
AUTH_USERS = {{
    'user1': 'scrypt:32768:8:1$52NzsfgEdNw1d4ZB$33be0cd586f9f72119b9c6d90519b8d30a77799a22de70ba9ab04406e5b160f9044c910e844efde32d90fc977c09abcbbc91e5ecf7da479ba6d36f388a227a84',
    'user2': 'scrypt:32768:8:1$MRwIPcCMixQ0qXsz$baf46fe5cf8af314e4b7a85f62aff95b9f0741b10f6959f933e41c638349328ef40faedac2e568b734f7c94dbf5e468510814e7642641948c9be9d7aa1c11fde'
}}
# If behind reverse proxy, set this to 1.
# If behind multiple reverse proxies, set this to the number of proxies
PROXIES = 0
"""
            )
        click.echo(
            f"Initialized configuration file at {current_app.instance_path}/config.py"
        )
    except FileExistsError:
        click.echo(
            f"Could not initialize configuration file. File already exists at {current_app.instance_path}/config.py."
        )


def create_app(test_config=None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    auth = HTTPBasicAuth()
    app.cli.add_command(init_config)

    # Default settings
    app.config.from_mapping(
        SECRET_KEY="dev",
        FQDNS={},
        AUTH_USERS={},
        PROXIES=0,
    )

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if test_config is None:
        try:
            app.config.from_pyfile("config.py")
        except OSError:
            if "init-config" in sys.argv:
                pass
            else:
                current_app.logger.error(
                    "Configuration file could not be loaded. Please create a configuration file at "
                    + app.instance_path
                    + "/config.py. "
                )
                sys.exit(1)
    else:
        app.config.from_mapping(test_config)
    if app.config["PROXIES"] > 0:
        from werkzeug.middleware.proxy_fix import ProxyFix

        app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)

    @auth.verify_password
    def verify_password(username, password):
        if username in app.config["AUTH_USERS"] and check_password_hash(
            app.config["AUTH_USERS"][username], password
        ):
            return username

    @app.route("/nic/update")
    @auth.login_required
    def dyndns_update():
        try:
            dyndns_hostname = request.args.get("hostname")
            dyndns_ip = request.args.get("myip")

            if dyndns_hostname in current_app.config.get("FQDNS"):
                update_hetzner_dns_record(
                    api_key=current_app.config.get("FQDNS")[dyndns_hostname],
                    fqdn=dyndns_hostname,
                    ip=dyndns_ip,
                )
                return "good " + dyndns_ip
            else:
                abort(404)
        except (ZoneNotFoundError, RecordNotFoundError):
            abort(404)

    return app

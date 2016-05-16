import os
import sys
import json
import platform
from OpenSSL import crypto, SSL
from socket import gethostname
from pprint import pprint
from time import gmtime, mktime
import pkg_resources

if (sys.version_info > (3, 0)):
    pass
else:
    input = raw_input

def plugins():
    plugins = {}
    group = "c3i_plugin"
    for entrypoint in pkg_resources.iter_entry_points(group=group):
        plugins[entrypoint.name] = entrypoint.load()
    return plugins

def generate_key_pair(cert_file, key_file):
    # create a key pair
    k = crypto.PKey()
    k.generate_key(crypto.TYPE_RSA, 4096)

    # create a self-signed cert
    cert = crypto.X509()
    cert.get_subject().C = input("Country: ")
    cert.get_subject().ST = input("State: ")
    cert.get_subject().L = input("Locality: ")
    cert.get_subject().O = input("Organization: ")
    cert.get_subject().OU = input("Organizational Unit: ")
    cert.get_subject().CN = input("Common Name: ")
    cert.set_serial_number(1000)
    cert.gmtime_adj_notBefore(0)
    cert.gmtime_adj_notAfter(10*365*24*60*60)
    cert.set_issuer(cert.get_subject())
    cert.set_pubkey(k)
    cert.sign(k, 'sha256')

    open(cert_file, "wt").write(
        crypto.dump_certificate(crypto.FILETYPE_PEM, cert))
    open(key_file, "wt").write(
        crypto.dump_privatekey(crypto.FILETYPE_PEM, k))

        
def is_writable(d):
    """Return True if d is a directory and is writable by
    current user"""
    fname = os.path.join(d, "test.write")
    try:
        with open(fname, "w") as fout:
            fout.write("test")
        os.remove(fname)
        return True
    except IOError:
        return False

def c3i_home():
    if "Windows" in platform.system():
        home = os.path.join("\Program Files", "c3i")
        if is_writable(home):
            return home
    elif "Linux" in platform.system():
        home = os.path.join("/opt", "c3i")
        if is_writable(home):
            return home
    else:
        return ""
    home = os.path.join(os.path.expanduser("~"), "c3i")
    return home

def c3i_config():
    return os.path.join(c3i_home(), "config.json")
        
def first_run():
    print("Seems like this is your first time running c3i,")
    print("Please take some time to answer some questions.\n\n")
    
    print("Creating c3i home directory here: {}".format(c3i_home()))
    os.mkdir(c3i_home())
    os.mkdir(os.path.join(c3i_home(), "pki"))
    os.mkdir(os.path.join(c3i_home(), "pki", "public"))
    os.mkdir(os.path.join(c3i_home(), "pki", "private"))
    os.mkdir(os.path.join(c3i_home(), "log"))

    cert_file = os.path.join(c3i_home(), "pki", "public", "c3i.crt")
    key_file = os.path.join(c3i_home(), "pki", "private", "c3i.key")
    access_log = os.path.join(c3i_home(), "log", "access.log")
    error_log = os.path.join(c3i_home(), "log", "error.log")

    print("Generating an RSA key pair to use for encryption,")
    print("please answer these questions:\n\n")
    
    # This function will ask the questions
    generate_key_pair(cert_file, key_file)
    with open(c3i_config(), "w") as fout:
        json.dump({
            "cert": cert_file,
            "key": key_file,
            "port": 8080,
            "host": "127.0.0.1",
            "max_request_body_size": 536870912,
            "access.log": access_log,
            "error.log": error_log
        },
        fout)

    print("A default configuration has been placed in {}".format(
        os.path.join(c3i_config())))    

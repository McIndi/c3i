import sys
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


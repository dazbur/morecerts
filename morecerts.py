#!/usr/bin/python

import sys
import os
from optparse import OptionParser, OptionGroup

def getHosts(hostlistfile):
    f = open(hostlistfile, 'r')
    hosts = [line.rstrip() for line in f if line.rstrip() != ""]
    f.close()
    return hosts

def generateCertificates(options):
    hosts = getHosts(options.hostlistfile)
    for host in hosts:
        host_ini = ".".join([host, "ini"])
        outfile = open(host_ini, "w")
        outfile.write("[ req ]\n")
        outfile.write("prompt = no\n")
        outfile.write("distinguished_name = req_distinguished_name\n")
        outfile.write("[ req_distinguished_name ]\n")
        outfile.write("C=%s\n" % options.country)
        outfile.write("ST=%s\n" % options.state)
        outfile.write("L=%s\n" % options.location)
        outfile.write("O=%s\n" % options.organization)
        outfile.write("OU=%s\n" % options.orgunit)
        outfile.write("CN=%s\n" % host)
        outfile.close()
        os.system("openssl genrsa -des3 -passout file:%s -out agent_%s.key 2048"\
         % (options.agentpassfile, host))
        os.system("""openssl req -new -x509 -days 1095 -key agent_%s.key\
         -out agent_%s.pem -passin file:%s\
         -config %s""" % (host, host, options.agentpassfile, host_ini))

def addCertsToKeystore(options):
    hosts = getHosts(options.hostlistfile)
    for host in hosts:
        os.system("""keytool -keystore %s -import -alias %s -file agent_%s.pem\
        -storepass %s -noprompt""" % (options.keystorepath, host, host,\
         options.keystorepwd))

def main():
    usage = "usage: %prog [options] gencerts|addtokeystore"
    parser = OptionParser(usage)
    parser.add_option("-f", "--hostlist", dest="hostlistfile",
                        help="File with list of hostnames/IPs")
    parser.add_option("-p", "--passfile", dest="agentpassfile",
                        help="File with password for agents certificates")
    parser.add_option("-k", "--keystore", dest="keystorepath",
                        help="Path to keystore file")
    parser.add_option("-w", "--keystorepwd", dest="keystorepwd",
                        help="Keystore password")
    group = OptionGroup(parser, "OpenSSL Distinguished Name options",
                        "You can leave the defaults if you don't care.")
    group.add_option("-C", "--country", dest="country",default="US",
                        help="C field")
    group.add_option("-S", "--state", dest="state",default="CA",
                        help="ST field")
    group.add_option("-L", "--location", dest="location",default="NA",
                        help="L field")
    group.add_option("-O", "--organization", dest="organization",default="NA",
                        help="O field")
    group.add_option("-U", "--orgunit", dest="orgunit",default="NA",
                        help="OU field")
    parser.add_option_group(group)

    (opt, args) = parser.parse_args()

    if len(args) != 1:
        parser.error("Please specify one command: gencerts or addtokeystore")
    command = args[0]

    if command == "gencerts":
        if not opt.hostlistfile or not opt.agentpassfile:
            parser.error("Please specify --hostlist and --passfile")
        generateCertificates(opt)
    elif command == "addtokeystore":
        if not opt.hostlistfile or not opt.keystorepath or not opt.keystorepwd:
            parser.error("Please specify --hostlist,"
                "--keystore and --keystorepwd options")
        addCertsToKeystore(opt)
    else:
        parser.error("Unrecognized command"
         "Please use gencerts or addtokeystore")


if __name__ == "__main__":
    main()

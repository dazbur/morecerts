morecerts
=========

Tool to generate lots of private keys and certificates. Can be specifically useful for enabling Cloudera Manager Agents TLS.

Usage examples:

Generate keys and certificates: 
morecerts.py -f agentiplist.file -p agent.pass.file gencerts

Add generates keys to keystore:
morecerts.py -f agentiplist.file -p agent.pass.file -k /etc/cloudera-scm-server/keystore -KEYSTORE_PASSOWORD addtokeystore
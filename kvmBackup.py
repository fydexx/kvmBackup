#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Fri Oct  9 11:20:46 2015

@author: Paolo Cozzi <paolo.cozzi@ptp.it>
"""

import os
import sys
import yaml
import pprint
import socket
import libvirt
import logging
import argparse
import datetime
#import dateutils

# Logging istance
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.DEBUG)
logger = logging.getLogger(sys.argv[0])

# A function to open a config file
def loadConf(file_conf):
    config = yaml.load(open(file_conf))
    
    #read my defined domains
    hostname = socket.gethostname()
    hostname = hostname.split(".")[0]
    
    #try to parse useful data
    mydomains = config[hostname]["domains"]
    
    #get my backup directory
    backupdir = config[hostname]["backupdir"]
    
    return mydomains, backupdir, config
    
def dumpXML(domain, path):
    """DumpXML inside PATH"""
    
    dest_file = "%s.xml" %(domain.name())
    dest_file = os.path.join(path, dest_file)
    
    if os.path.exists(dest_file):
        raise Exception, "File %s exists!!" %(dest_file)
        
    dest_fh = open(dest_file, "w")
    
    #dump different xmls files. First of all, the offline dump
    xml = domain.XMLDesc()
    dest_fh.write(xml)
    dest_fh.close()
    
    logger.info("File %s wrote" %(dest_file))

    #All flags: libvirt.VIR_DOMAIN_XML_INACTIVE, libvirt.VIR_DOMAIN_XML_MIGRATABLE, libvirt.VIR_DOMAIN_XML_SECURE, libvirt.VIR_DOMAIN_XML_UPDATE_CPU
    dest_file = "%s-inactive.xml" %(domain.name())
    dest_file = os.path.join(path, dest_file)
    
    if os.path.exists(dest_file):
        raise Exception, "File %s exists!!" %(dest_file)
        
    dest_fh = open(dest_file, "w")
    
    #dump different xmls files. First of all, the offline dump
    xml = domain.XMLDesc(flags=libvirt.VIR_DOMAIN_XML_INACTIVE)
    dest_fh.write(xml)
    dest_fh.close()
    
    logger.info("File %s wrote" %(dest_file))
    
    #Dump a migrate config file
    dest_file = "%s-migratable.xml" %(domain.name())
    dest_file = os.path.join(path, dest_file)
    
    if os.path.exists(dest_file):
        raise Exception, "File %s exists!!" %(dest_file)
        
    dest_fh = open(dest_file, "w")
    
    #dump different xmls files. First of all, the offline dump
    xml = domain.XMLDesc(flags=libvirt.VIR_DOMAIN_XML_INACTIVE+libvirt.VIR_DOMAIN_XML_MIGRATABLE)
    dest_fh.write(xml)
    dest_fh.close()
    
    logger.info("File %s wrote" %(dest_file))
    
def callSnapshot(domain):
    """Create a snapshot for domain"""
    
    #i need a xml file for the domain
    
    
def backup(domain, parameters):
    pass
    #TODO: call rotation directive

    #TODO: call dumpXML

    #TODO: call snapshot

    #TODO: copy file

    #TODO: block commit

    #TODO: remove snapshot

#a function to check current day of the week
def checkDay(day):
    now = datetime.datetime.now()
    today = now.strftime("%a")
    
    if today == day:
        return True
        
    return False

# A global connection instance
conn = libvirt.open("qemu:///system")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Backup of KVM domains')
    parser.add_argument("-c", "--config", required=True, type=str, help="The config file")
    args = parser.parse_args()
    
    #get all domain names
    domains = [domain.name() for domain in conn.listAllDomains()]
    
    #parse configuration file
    mydomains, backupdir, config = loadConf(args.config)
    
    #test for directory existance
    if not os.path.exists(backupdir) and os.path.isdir(backupdir) is False:
        logger.info("Creating directory %s" %(backupdir))
        os.mkdir(backupdir)
    
    #debug
    #pprint.pprint(mydomains)
    
    for domain_name, parameters in mydomains.iteritems():
        #check if bakcup is needed
        domain_backup = False
        
        for day in parameters["day_of_week"]:
            if checkDay(day) is True:
                logger.info("Ready for back up of %s" %(domain_name))
                domain_backup = True
                
                #breaking cicle
                break
            
        if domain_backup is False:
            logger.debug("Ignoring %s domain" %(domain_name))



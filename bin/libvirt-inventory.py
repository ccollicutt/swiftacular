#!/usr/bin/python

#from BeautifulSoup import BeautifulSoup

from xml.dom import minidom
import libvirt
import sys
import json

#
# Want to create ansible_ssh_host entries for each server.
# _meta is a high level entry in the json output, same level
# as the server groups.
#
def addMeta(vmName, inventory, group):

	if not inventory['_meta']:
		inventory['_meta'] = {}
		inventory['_meta']['hostvars'] = {}

	if not vmName in inventory['_meta']:
		inventory['_meta']['hostvars'][vmName] = {}
		inventory['_meta']['hostvars'][vmName]['ansible_ssh_host'] = ip

	return True

#
# Connect to the hypervisor
#
conn = libvirt.open("qemu:///system")
if conn == None:
    print 'Failed to open connection to hypervisor'
    sys.exit(1)

#
# Create all the groups in the inventory
#
groups = ['authentication', 'lbssl', 'swiftclient', 'package_cache', 'proxy', 'storage']
inventory = {}
inventory['_meta'] = {}
for group in groups:
	if not group in inventory:
		inventory[group] = {
		'hosts' : [],
		}

#
# Find all active vms and add them into the inventory by finding
# their IP from the default.leases file
#
for vm in conn.listAllDomains():

	if vm.isActive():
		xmlDoc = minidom.parseString(vm.XMLDesc())
		interfaces = xmlDoc.getElementsByTagName('mac') 

		mac =  interfaces[0].getAttribute('address')

		# Open leases and search for the mac address
		leases = '/var/lib/libvirt/dnsmasq/default.leases'
		with open(leases, 'r') as fh:
			for line in fh.readlines():
				col = line.split()
				if col[1] == mac:
					ip = col[2]
					break	

		# ugh
		if 'keystone' in vm.name():
			inventory['authentication']['hosts'].append(vm.name())
			addMeta(vm.name(), inventory, 'authentication')
		elif 'storage' in vm.name():
			inventory['storage']['hosts'].append(vm.name())
			addMeta(vm.name(), inventory, 'storage')
		elif 'package-cache' in vm.name():
			# Using the package cache server as the swiftclient as well
			inventory['package_cache']['hosts'].append(vm.name())
			inventory['swiftclient']['hosts'].append(vm.name())
			addMeta(vm.name(), inventory, 'package_cache')
			addMeta(vm.name(), inventory, 'swiftclient')
		elif 'proxy' in vm.name():
			inventory['proxy']['hosts'].append(vm.name())
			addMeta(vm.name(), inventory, 'proxy')
		elif 'lbssl' in vm.name():
			inventory['lbssl']['hosts'].append(vm.name())
			addMeta(vm.name(), inventory, 'lbssl')

print json.dumps(inventory, indent=4)

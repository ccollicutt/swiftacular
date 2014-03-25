```
  _________       .__  _____  __                      .__                
 /   _____/_  _  _|__|/ ____\/  |______    ____  __ __|  | _____ _______ 
 \_____  \\ \/ \/ /  \   __\\   __\__  \ _/ ___\|  |  \  | \__  \\_  __ \
 /        \\     /|  ||  |   |  |  / __ \\  \___|  |  /  |__/ __ \|  | \/
/_______  / \/\_/ |__||__|   |__| (____  /\___  >____/|____(____  /__|   
        \/                             \/     \/                \/       
```

# OpenStack Swift Havana and Ansible

This repository will create a virtualized OpenStack Swift cluster using Vagrant, VirtualBox, Ansible, and the OpenStack Havana release for Ubuntu 12.04.

#### Table of Contents

1. [Too long; didn't read](#tldr)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Networking setup](#networking-setup)
5. [Starting over](#starting-over)
6. [Development environment](#development-environment)
7. [Modules](#modules)
8. [Future work](#future-work)
9. [Issues](#issues)
10. [Notes](#notes)

## tl;dr

*Note this will start seven virtual machines on your computer.*

```bash
$ git clone git@github.com:curtisgithub/swiftacular.git
$ cd swiftacular
$ mkdir library
# Checkout some modules to help with managing openstack 
$ git clone https://github.com/openstack-ansible/openstack-ansible-modules library/openstack
$ vagrant up 
$ cp group_vars/all.example group_vars/all
$ vi group_vars/all # ie. edit the CHANGEMEs in the file, if desired
# Source aliases, etc
$ . ansiblerc
# Test connectivity to virtual machines
$ ans -m ping all
# Run the playbook to deploy Swift!
$ pb site.yml
```

## Features

* Run OpenStack Swift in vms on your local computer, but with multiple servers
* Replication network is used, which means this could be a basis for a geo-replication system
* SSL - Keystone is configured to use SSL and the Swift Proxy is proxied by an SSL server
* Sparse files to back Swift disks
* Tests for uploading files into Swift
* Use of [gauntlt](http://gauntlt.org/) attacks to verify installation

## Requirements

* Vagrant and Virtualbox
* Enough resources on your computer to run seven vms

## Virtual machines created

Seven Vagrant-based virtual machines are used for this playbook:

* __package_cache__ - One apt-cacher-ng server so that you don't have to download packages from the Internet over and over again, only once
* __authentication__ - One Keystone server for authentication
* __lbssl__ - One SSL termination server that will be used to proxy connections to the Swift Proxy server
* __swift-proxy__ - One Swift proxy server
* __swift-storage__ - Three Swift storage nodes

## Networking setup

Each vm will have four networks (technically five including the Vagrant network). In a real production system every server would not need to be attached to every network, and in fact you would want to avoid that. In this case, they are all attached to every network.

* __eth0__ - Used by Vagrant
* __eth1__ - 192.168.100.0/24 - The "public" network that users would connect to
* __eth2__ - 10.0.10.0/24 - This is the network between the SSL terminator and the Swift Proxy
* __eth3__ - 10.0.20.0/24 - The local Swift internal network
* __eth4__ - 10.0.30.0/24 - The replication network which is a feature of OpenStack Swift starting with the Havana release

## Self-signed certificates

Because this playbook configures self-signed SSL certificates and by default the swift client will complain about that fact, either the <code>--insecure</code> option needs to be used or alternatively the <code>SWIFTCLIENT_INSECURE</code> environment variable can be set to true.

## Using the swift command line client

You can install the swift client anywhere that you have access to the SSL termination point and Keystone. So you could put it on your local laptop as well, probably with:

```bash
$ pip install python-swiftclient
```

However, I usually login to the package_cache server and use swift from there.

```bash
$ vagrant ssh swift-package-cache-01
working on swift-package-cache-01 with ip of 192.168.100.20
Welcome to Ubuntu 12.04 LTS (GNU/Linux 3.2.0-23-generic x86_64)

 * Documentation:  https://help.ubuntu.com/
Welcome to your Vagrant-built virtual machine.
Last login: Mon Nov 25 10:57:32 2013 from 192.168.100.1
vagrant@swift-package-cache-01:~$ . testrc 
vagrant@swift-package-cache-01:~$ swift list
vagrant@swift-package-cache-01:~$ echo "swift is cool" > swift.txt
vagrant@swift-package-cache-01:~$ swift upload swifty swift.txt 
swift.txt
vagrant@swift-package-cache-01:~$ swift list
swifty
vagrant@swift-package-cache-01:~$ swift list swifty
swift.txt
```

## Starting over

If you want to redo the installation there are a few ways. 

To restart completely:

```bash
$ vagrant destroy -f
$ vagrant up
$ pb site.yml
```

There is a script to destroy and rebuild everything but the package cache:

```bash
$ ./bin/redo
$ ans -m ping all # just to check if networking is up
$ pb site.yml
```

To remove and redo only the rings and fake/sparse disks without destroying any virtual machines:

```bash
$ pb playbooks/remove_rings.yml
$ pb site.yml
```

To remove the keystone database and redo the endpoints, users, regions, etc:

```bash
$ pb ./playbook/remove_keystone.yml
$ pb site.yml
```

## Development environment

This playbook was developed in the following environment:

* OSX 10.8.2
* Ansible 1.4
* Virtualbox 4.2.6
* Vagrant 1.3.5
* OpenStack Havana from the [Ubuntu Cloud Archive](https://wiki.ubuntu.com/ServerTeam/CloudArchive)
* Ubuntu 12.04 for the vms

## Modules

There is an swift-ansible-modules directory in the library directory that contains a couple of modules taken from the official Ansible modules as well as the [openstack-ansible-modules](https://github.com/lorin/openstack-ansible) and for now both have been modified to allow the "insecure" option, which means self-signed certificates. I hope to get those changes into their respective repositories soon.

## Future work

* Make using LXC an option
* Deploy Swift from source
* More than one region. Regions are setup, only one is created right now.

## Issues

* Loop mounts won't survive a reboot on the storage nodes

## Notes

* I know that Vagrant can automatically start Ansible playbooks on the creation of a vm, but I prefer to run the playbook manually
* LXC is likely a better fit than Virtualbox given all the vms are the same OS and we don't need to boot any vms within vms inception style
* Starting the vms is a bit slow I believe because of the extra networks

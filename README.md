```
  _________       .__  _____  __                      .__                
 /   _____/_  _  _|__|/ ____\/  |______    ____  __ __|  | _____ _______ 
 \_____  \\ \/ \/ /  \   __\\   __\__  \ _/ ___\|  |  \  | \__  \\_  __ \
 /        \\     /|  ||  |   |  |  / __ \\  \___|  |  /  |__/ __ \|  | \/
/_______  / \/\_/ |__||__|   |__| (____  /\___  >____/|____(____  /__|   
        \/                             \/     \/                \/       
```

# OpenStack Swift Havana and Ansible

This repository will create a virtualized OpenStack Swift cluster using Vagrant, VirtualBox, Ansible, and the OpenStack Havana release. 

## tl;dr

```bash
$ git clone git@github.com:curtisgithub/swiftacular.git
$ cd swiftacular
$ git checkout va-rc-1
$ vagrant up # and go for coffee; bulding vms is the new compiling
# Source aliases, etc
$ . ansiblerc
# Test connectivity to virtual machiens
$ ans -m ping all
# Run the playbook to deploy Swift!
$ pb site.yml
```

## Features

* Run OpenStack Swift in vms on your local computer, but with multiple servers
* Replication network is used, which means this could be a basis for a geo-replication system
* SSL - Keystone is configured to use SSL and the Swift Proxy is proxied by an SSL server
* Sparse files to back Swift disks
* A few short tests to upload files into Swift

## Requirements

* Vagrant and Virtualbox
* Enough resources on your computer to run seven vms

## Virtual machines created

Seven Vagrant-based virtual machines (vms) are used for this playbook:

* package_cache - One apt-cacher-ng server so that you don't have to download packages from the Internet over and over again, only once
* authentication - One Keystone server for authentication
* lbssl - One SSL termination server that will be used to proxy connections to the Swift Proxy server
* swift-proxy - One Swift proxy server
* swift-storage - Three Swift storage nodes

## Networks used

Each vm will have four networks (techinically five including the Vagrant network). In a real production system every server would not need to be attached to every network, and in fact you would want to avoid that. In this case, they are all attached to every network.

* eth0 - Vagrant
* eth1 - 192.168.100.0/24 - The "public" network that users would connect to
* eth2 - 10.0.10.0/24 - This is the network between the SSL terminator and the Swift Proxy
* eth3 - 10.0.20.0/24 - The local Swift internal network
* eth4 - 10.0.30.0/24 - The replication network which is a feature of OpenStack Swift starting with the Havana release

## A note about self-signed certificates

Because this playbook sets up self-signed SSL certificates, the swift CLI needs to have the "--insecure" option set to not complain about them.

```bash
vagrant@swift-package-cache-01:~$ echo "Swift is cool" > test.txt
vagrant@swift-package-cache-01:~$ swift --insecure upload test_container test.txt 
test.txt
vagrant@swift-package-cache-01:~$ swift --insecure list
test_container
vagrant@swift-package-cache-01:~$ swift --insecure list test_container
test.txt
```
## Redoing the installation and starting over quickly

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
$ vagrant up
$ pb site.yml
```

To remove and redo only the rings and fake/sparse disks without destroying any virtual machines:

```bash
$ pb playbooks/remove_rings.yml
$ pb site.yml
```

## Development environment

This playbook was developed in the following environment:

* OSX 10.8.2
* Virtualbox 4.2.6
* Vagrant 1.3.5
* OpenStack Havana from the Ubuntu Cloud Archive
* Ubuntu 12.04 for the vms

## swift-ansible-modules

There is an swift-ansible-modules directory in the library directory that contains a couple of modules taken from the offical Ansible modules as well as the [openstack-ansible-modules](https://github.com/lorin/openstack-ansible) and for now both have been modified to allow the "insecure" option, which means self-signed certificates. I hope to get those changes into their respective repositories soon.

## NOTES

* I know that Vagrant can automatically start Ansible playbooks on the creation of a vm, but I prefer to run the playbook manually
* LXC is likely a better fit than Virtualbox given all the vms are the same OS
* Starting the vms is a bit slow I believe because of the extra networks


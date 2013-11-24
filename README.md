```
  _________       .__  _____  __                      .__                
 /   _____/_  _  _|__|/ ____\/  |______    ____  __ __|  | _____ _______ 
 \_____  \\ \/ \/ /  \   __\\   __\__  \ _/ ___\|  |  \  | \__  \\_  __ \
 /        \\     /|  ||  |   |  |  / __ \\  \___|  |  /  |__/ __ \|  | \/
/_______  / \/\_/ |__||__|   |__| (____  /\___  >____/|____(____  /__|   
        \/                             \/     \/                \/       
```

# OpenStack Swift Havana and Ansible

This repository will create a small virtualized OpenStack Swift cluster based on the Havana release. It will create seven virtual machines (vms):

* An apt-cacher-ng server so that you don't have to download packages from the Internet over and over again, only once
* A Keystone server for authentication
* A SSL termination server that will be used to proxy connections to the Swift Proxy server
* A Swift proxy server
* Three Swift storage nodes

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

* Run OpenStack Swift on your local computer, but with multiple servers
* Replication network is used, which means this could be a basis for a geo-replication system
* SSL - Keystone is configured to use SSL and the Swift Proxy is itself proxied by an SSL server
* Sparse files to back Swift disks
* A few short tests to upload files into Swift

## Requirements

* Vagrant and Virtualbox
* Enough resources on your computer to run seven vms

## Networking

Each vm will have four networks (techinically five including the Vagrant network):

* 192.168.100.0/24 - The "public" network that users would connect to
* 10.0.10.0/24 - This is the network between the SSL terminator and the Swift Proxy
* 10.0.20.0/24 - The local Swift internal network
* 10.0.30.0/24 - The replication network which is a feature of OpenStack Swift starting with the Havana release

# A note about self-signed certificates

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
# Redoing the installation and starting over quickly

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

# Development environment

* OSX 10.8.2
* Virtualbox 4.2.6
* Vagrant 1.3.5
* OpenStack Havana from the Ubuntu Cloud Archive
* Ubuntu 12.04 for the vms


# NOTES

* I know that Vagrant can automatically start Ansible playbooks on the creation of a vm, but I prefer to run the playbook manually

* LXC is likely a better fit than Virtualbox given all the vms are the same OS
* Starting the vms is a bit slow I believe because of the extra networks


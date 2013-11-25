# TODO
* Add gauntlt checks
* create example all.example
* Use gather facts for info from other groups instead of delegate_to?
* Fix tasks that always return changed, ie. pound startup config
* Will rings be built 3 times in storage main.yml when they only need to be built once?
* Configure region to be a variable
* See what's happening here: https://github.com/lorin/openstack-ansible/tree/master/services/swift
* Add an ansible config file instead of the ansiblerc?
* Submit insecure option back to upsteam for ansible swift modules
** Done for keystone_service
* lbssl should connect to lbssl network, ie. swift proxy should not be listening on 192...
* memcached on proxy should listen on internal network not public
* write/read affinity for swift
* add object expirer? "no object-expirer running"
* increase rsync connnections
* are all services actually running on the storage nodes? ie. does swift-init all start actually complete? ansible seems to think so.
* EC2 compatability verify, ssl, etc
* have vagrant create the ansible_hosts file?
* use "creates_file" in playbook to check if command has run?
* iptables templates for each server
* make generic test user configurable
* write a sparse_file module
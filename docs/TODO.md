# TODO
* add an rsync test
* add an upstart job to remount disk images
* Is swiftoperator the right role for users?
* setup tags?
* use upstarts to start with services instead of swift-init all
* Demo tenant is not the correct one to create?
* work on notifications to restart services?
* check ssl
* shouldn't restart services on runs after the first one unless required
* create example all.example
* Fix tasks that always return changed, ie. pound startup config
* Will rings be built 3 times in storage main.yml when they only need to be built once?
* See what's happening here: https://github.com/lorin/openstack-ansible/tree/master/services/swift
* Add an ansible config file instead of the ansiblerc?
* Submit insecure option back to upsteam for ansible swift modules
* write/read affinity for swift -- though we only have one region
* increase rsync connnections
* are all services actually running on the storage nodes? ie. does swift-init all start actually complete? ansible seems to think so.
* EC2 compatability verify, ssl, etc
* automatically generate passwords and tokens on each run in group_vars/all?
* have vagrant create the ansible_hosts file?
* iptables templates for each server
* write a sparse_file module
* Use gather facts for info from other groups instead of delegate_to?
* object-expirer...where should this run?
* make pound -> swift-proxy address a variable in pound.cfg, ie. right now it is hardcoded to 10.0.10.100
* add object expirer? "no object-expirer running"

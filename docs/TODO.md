# TODO
* write/read affinity for swift
* add object expirer? "no object-expirer running"
* increase rsync connnections
* are all services actually running on the storage nodes? ie. does swift-init all start actually complete? ansible seems to think so.
* EC2 compatability verify, ssl, etc
* have vagrant create the ansible_hosts file?
* use "creates_file" in playbook to check if command has run?
* iptables templates for each server
* make generic test user configurable
# TODO
* add object expirer?
* increase rsync connnections
* are all services actually running on the storage nodes? ie. does swift-init all start actually complete? ansible seems to think so.
* EC2 compatability verify, ssl, etc
* is it possible to do this with docker?
* putting ring files up shouldn't be done if they are already there?
* fix harcoded IPs
** eg. in proxy-server.conf.j2...
* have vagrant create the ansible_hosts file?
* use "creates_file" in playbook to check if command has run?
* ssl enable swift (means loadbalancer/ssl endpoint?)
* ansible will look in ./library I think, so should set that up instead of using path perhaps?
* iptables templates for each server
* ssl termination for swift-proxy
* lots of interesting security stuff to do with pound...


* DONE: ssl enable keystone

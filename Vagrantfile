# -*- mode: ruby -*-
# vi: set ft=ruby :

nodes = {
    'swift-package-cache' => [1, 20],
    'swift-keystone' => [1, 50],
    'swift-lbssl' => [1, 30],
    'swift-proxy'   => [1, 100],
    'swift-storage' => [3, 200],
}

Vagrant.configure("2") do |config|
    #config.vm.box = "trusty64"
    #config.vm.box_url = "https://cloud-images.ubuntu.com/vagrant/trusty/current/trusty-server-cloudimg-amd64-vagrant-disk1.box"
    #config.vm.box = "centos65"
    #config.vm.box_url = "http://puppet-vagrant-boxes.puppetlabs.com/centos-65-x64-virtualbox-nocm.box"
    config.vm.box = "precise64"
    config.vm.box_url = "http://files.vagrantup.com/precise64.box"

    nodes.each do |prefix, (count, ip_start)|
        count.times do |i|
            hostname = "%s-%02d" % [prefix, (i+1)]

            config.vm.provider :virtualbox do |v|
                v.customize ["modifyvm", :id, "--memory", 1024]
            end

            config.vm.define "#{hostname}" do |box|
                puts "working on #{hostname} with ip of 192.168.100.#{ip_start+i}"

                box.vm.hostname = "#{hostname}.example.com"

                #
                # Networks
                #

                # Public
                box.vm.network :private_network, :ip => "192.168.100.#{ip_start+i}", :netmask => "255.255.255.0"

                # SSL and loadbalancing
                box.vm.network :private_network, :ip => "10.0.10.#{ip_start+i}", :netmask => "255.255.255.0"

                # Internal
                box.vm.network :private_network, :ip => "10.0.20.#{ip_start+i}", :netmask => "255.255.255.0"

                # Replication
                box.vm.network :private_network, :ip => "10.0.30.#{ip_start+i}", :netmask => "255.255.255.0"

            end
        end
    end
end

# -*- mode: ruby -*-
# vi: set ft=ruby :

nodes = {
    'swift-package-cache' => [1, 20],
    'swift-lxc' => [1, 40],
    'swift-keystone' => [1, 50],
    'swift-lbssl' => [1, 30],
    'swift-proxy'   => [1, 100],
    'swift-storage' => [4, 200],
}

Vagrant.configure("2") do |config|
    config.vm.box = "precise64"

    nodes.each do |prefix, (count, ip_start)|
        count.times do |i|
            hostname = "%s-%02d" % [prefix, (i+1)]

            config.vm.provider :virtualbox do |v|
              
                #v.customize ["modifyvm", :id, "--nictype2", "virtio"]
                #v.customize ["modifyvm", :id, "--nictype3", "virtio"]
                v.customize ["modifyvm", :id, "--memory", 1024]
                #v.gui = true
                #v.customize ["modifyvm", :id, "--name", "VagrantMachineTest"]
            end

            config.vm.define "#{hostname}" do |box|
                puts "working on #{hostname} with ip of 192.168.100.#{ip_start+i}"
            
                box.vm.hostname = "#{hostname}.cybera.ca"
                # Vagrant
                box.vm.network :private_network, :ip => "192.168.100.#{ip_start+i}", :netmask => "255.255.255.0" 
                # SSL and loadbalancing
                box.vm.network :private_network, :ip => "10.0.10.#{ip_start+i}", :netmask => "255.255.255.0" 
                # Internal
                box.vm.network :private_network, :ip => "10.0.20.#{ip_start+i}", :netmask => "255.255.255.0"
                # Replication 
                box.vm.network :private_network, :ip => "10.0.30.#{ip_start+i}", :netmask => "255.255.255.0" 

                #box.vm.network :private_network
                #if prefix == "puppet-server"
                #    box.vm.provision :shell, :path => "#{prefix}.sh"
                #else
                #    box.vm.provision :shell, :path => "proxy.sh"
                #end
            end
        end
    end
end

# -*- mode: ruby -*-
# vi: set ft=ruby :

nodes = {
    'swift-client' => [1, 10],
    'swift-package-cache' => [1, 20],
    'swift-keystone' => [1, 50],
    'swift-ssl' => [1, 30],
    'swift-proxy'   => [1, 100],
    'swift-storage' => [5, 200],
}

Vagrant.configure("2") do |config|
    config.vm.box = "precise64"

    nodes.each do |prefix, (count, ip_start)|
        count.times do |i|
            hostname = "%s-%02d" % [prefix, (i+1)]

            config.vm.provider :virtualbox do |v|
                #v.customize ["modifyvm", :id, "--nictype1", "virtio"]
                #v.customize ["modifyvm", :id, "--nictype2", "virtio"]
                #v.customize ["modifyvm", :id, "--nictype3", "virtio"]
                v.customize ["modifyvm", :id, "--memory", 1024]
                #v.customize ["modifyvm", :id, "--name", "VagrantMachineTest"]
            end


            config.vm.define "#{hostname}" do |box|
                puts "working on #{hostname} with ip of 192.168.100.#{ip_start+i}"

                box.vm.hostname = "#{hostname}.cybera.ca"
                box.vm.network :private_network, :ip => "192.168.100.#{ip_start+i}", :netmask => "255.255.255.0" 
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

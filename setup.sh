export VAGRANT_LOG=debug
vagrant destroy -f
vagrant up
sleep 120


#on all baremetal nodes 
a)
change manually authorized key
ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABgQCpVRhUXzuS2S+CaHw4jBi+dfNtDA+yKnaJY8I9DjvNfgApO2IGTbWLlUAmKM7biU7eQ/IakVRSp1p61cxqwl2Cf80eauWwHUxjneFBQ7V9HP7i/p51O2m8UUDXABnTQfRDK0cN+I8xe3GSBKRYlm7at3dYF/hRBHTYTRntRdMavpvo6gNiLTN7mOZHZnFOJgbVkURMhAzSfcah2wQWoCKKtug9b/KfLvRb2L9bnaz+4lc4h+Pm4hb8tAZhNNPD5J3piQwI7pwrUbc0b4I0iRNamilDZ3q2+NtfhWBgCkdeuUvijnYjgN2bKKutAPna8R7b0X5h+kMOFLlLzb0lpNydVyEdpToXrky4AX9wj+87PN44ZJi0ewXIOXOpQt9QWHom9DGXrzCkNHI47s1F8fwaEIUufv1B85pe9tmyziq8V5/+XAoLCLpov7eJG8qQbrVWjXfywlLv6HO6IWzEj2CCm6J+ziL7iXOCFBWIsj0qee0qE9IYEqtQOFGC0hiXHH8= dsariel@fedora

b)
run
yum install -y python3-devel python3; ln -s /usr/bin/python2.7 /usr/bin/python



# Then run 
export ANSIBLE_LIBRARY=/srv/modules/custom_modules:/srv/modules/vendor_modules
virtualenv -p python2.7 venv2
. venv2/bin/activate
pip install ansible==1.9.6
ansible-playbook -i hosts site.yml

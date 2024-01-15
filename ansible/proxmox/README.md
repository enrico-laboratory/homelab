# PVE configuration
## Description

## Playbooks
### Storage configurations
```bash  
ansible-playbook pve_create_storage.yaml -i inventory --user=ansible --private-key ansible_rsa
```
### Network configurations
```bash  
ansible-playbook pve_network.yaml -i inventory --user=ansible --private-key ansible_rsa
```
## Bootstrap node
* verify/change the ip address of the node(s) in the inventory
* create ansible key
  ssh-keygen -f ansible_rsa
* Install sshpass
* install the ansible user
```bash  
ansible-playbook pve_bootstrap.yaml -i inventory --user=root -k  
```
* config storage
```bash  
ansible-playbook pve_create_storage.yaml -i inventory --user=ansible --private-key ansible_rsa
```
* create user ansible on gui and api-token for the same user
* test
```bash  
ansible-playbook pve_create_test_image.yaml -i inventory --user=ansible --private-key ansible_rsa
```
### Source

[Simplify Your Proxmox VE Tasks: Ansible Automation Made Easy](https://www.youtube.com/watch?v=4G9d5COhOvI&list=PLOUG593yAwIGuwYRdnACJaZEzOHMythiM)

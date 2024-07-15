# Home lab automations

## Ansible playbook

### K3S

**Create K3S VMs**
```bash 
ansible-playbook -i inventories/hosts.yaml playbooks/k3s/vms.yaml
```
It requires setting a creation of an `user`, giving the new user the right permission and the creation of an API token linked to that user.
`common_cfg_files/api_token` and `inventories/group_vars/pvnodes.yaml` files need to be update with new token, username, api tolken id.

**Add network configuration to VMs**
```bash
ansible-playbook -i inventories/hosts.yaml playbooks/k3s/network.yaml
```
**Add various config to VMs**
```bash
ansible-playbook -i inventories/hosts.yaml playbooks/k3s/config.yaml
```

**Install K3S**

Use [these playbooks](https://github.com/k3s-io/k3s-ansible). There should be a copy in the `repos` directory. Remember to do a `git pull` before installing.
N.B. copy over the `.kube/config` K3S creates in the master node and change the master node address

### K8S

**Install or delete metallb**
```bash
ansible-playbook -i inventories/hosts.yaml playbooks/k8s/metallb.yaml 
```

**Install or delete argocd and sealed secrets**
```bash
ansible-playbook -i inventories/hosts.yaml playbooks/k8s/argocd.yaml
```

**Retrieve argocd admin pass for access the UI**
```bash
ansible-playbook -i inventories/hosts.yaml playbooks/k8s/argocd_admin_pass.yaml
```

**Deploy librespeed and pihole**
```bash
ansible-playbook -i inventories/hosts.yaml playbooks/k8s/tooling.yaml
```
N.B for a new installation of k3s, the secrets need to be sealed again
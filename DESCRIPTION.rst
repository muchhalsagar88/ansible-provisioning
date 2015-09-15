A python package used to provision servers from multiple cloud vendors and create a inventry file consumable by ansible
Currently, the cloud providers supported are:
	1. Digital Ocean
	2. Windows Azure

After provisioning the servers, the details are stored in the inventory file which can be used by ansible for running playbooks. The project has an example of how to pass the inventory to a sample playbook
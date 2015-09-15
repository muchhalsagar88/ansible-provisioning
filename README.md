# Server provisioning and inventory file generation
Provisioning servers and deplyoing using ansible

## Provisioning servers
To provision servers, currently two providers namely, **([DigitalOcean]https://cloud.digitalocean.com/registrations/new) and ([Windows Azure]https://azure.microsoft.com/en-us/pricing/free-trial/)** are being used. Sepearate accounts need to be created for both the cloud providers.

To run the provisioning script, use
```
python provision.py <Cloud_Provider> <inventory_file_write_method>
```
where Cloud_Provider can have the values 
		* DigitalOcean  
		* Azure
and inventory_file_write_method can have the values
		* 1: Append to an existing inventory file
		* 2: Override an exisitng inventory file
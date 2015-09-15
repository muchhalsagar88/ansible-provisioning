import requests, json, time, os, base64
import base_provider, namesgenerator, random
from base_provider import ServiceProvider
import time
from azure import *
from azure.servicemanagement import *
from azure.storage.blob import BlobService

class AzureProvider(ServiceProvider):

	SUBSCRIPTION_ID_OPTION = "Subscription_Id"
	
	def __init__(self, base_url, section_name):
		self.base_url = base_url
		self.section_name = section_name
		super(AzureProvider, self).__init__()

	def create_instance(self):
		cloud_service_name = self.__create_cloud_service()
		storage_service_name = self.__create_storage_service()
		# To ensure that the storage service is up
		time.sleep(3)
		blob_container_url = self.__create_blob_container(storage_service_name)
		return self.__create_actual_vm(blob_container_url, cloud_service_name)

	def __get_service_mgmt_object(self):
		subscription_id = self.get_property(self.section_name, AzureProvider.SUBSCRIPTION_ID_OPTION)
		certificate_path = os.getcwd() + self.get_property(self.section_name, "API_Connection_Cert_Path")
		return ServiceManagementService(subscription_id, certificate_path)

	def __create_cloud_service(self):
		sms = self.__get_service_mgmt_object()

		# Create a cloud service
		# Because the name has to be unique in Their cloud :/
		hosted_service_name = namesgenerator.get_random_name()
		label = 'DevOps'
		desc = 'Service for basic nginx server'
		location = 'East US'
		sms.create_hosted_service(hosted_service_name, label, desc, location)
		#print "Created hosted service with name ",hosted_service_name
		return hosted_service_name

	def __create_storage_service(self):
		sms = self.__get_service_mgmt_object()

		# Create a storage service
		storage_acc_name = namesgenerator.get_random_name(True)
		label = 'mystorageaccount'
		location = 'East US'
		desc = 'My storage account description.'

		sms.create_storage_account(storage_acc_name, desc, label,
		                                    location=location)
		#print "Created storage service with name ",storage_acc_name
		return storage_acc_name

	def __create_blob_container(self, storage_acc_name):
		sms = self.__get_service_mgmt_object()

		# Retrieve the primary key of your storage account
		# Maybe the secondary key works too?
		storage_acc_key = None
		acounts = sms.list_storage_accounts()
		for account in acounts:
		    if account.service_name == storage_acc_name:
		        storageServiceObj = sms.get_storage_account_keys(account.service_name)
		        storage_acc_key = storageServiceObj.storage_service_keys.primary


		# Create a container
		blob_service = BlobService(account_name=storage_acc_name,
		                           account_key=storage_acc_key)

		container_name = namesgenerator.get_random_name()
		container_name += "container"
		blob_service.create_container(container_name)

		# This is the url to the container we just created
		container_url_template = "http://{}.blob.core.windows.net/{}"
		container_url = container_url_template.format(storage_acc_name, container_name)
		#print "Created blob container with URL ",container_url
		return container_url

	def __create_actual_vm(self, container_url, hosted_service_name):
		#print("__create_actual_vm(%s, %s) "%(container_url, hosted_service_name))
		sms = self.__get_service_mgmt_object()
		image_name = self.get_property(self.section_name, "VM_Image_Name")

		blob_url = container_url + "/ubuntu.vhd"

		# Create the Virtual Hardrive. It basically creates a harddrive at blob_url with the image specified
		os_hd = OSVirtualHardDisk(image_name, blob_url)

		# Upload the certificate we'd created earlier.
		cert_path = os.getcwd() + self.get_property(self.section_name, "Cert_Upload_Path")

		with open(cert_path, "rb") as bfile:
		    cert_data = base64.b64encode(bfile.read()).decode() # decode to make sure this is a str and not a bstr
		    cert_format = 'pfx'
		    cert_password = ''
		    cert_res = sms.add_service_certificate(service_name=hosted_service_name,
		                        data=cert_data,
		                        certificate_format=cert_format,
		                        password=cert_password)


		# Create a LinuxConfigurationSet for configuring Linux VMs, there's an equivalent Windows Set
		vm_name = namesgenerator.get_random_name()
		linux_config = LinuxConfigurationSet(hosted_service_name, 
			self.get_property(self.section_name, "VM_Default_Username"), 
			self.get_property(self.section_name, "VM_Default_Password"),
			True)

		SERVICE_CERT_THUMBPRINT = self.get_property(self.section_name, "Service_Certificate_Thumbprint")

		# Let's add the public keys to be uploaded
		pk = PublicKey(SERVICE_CERT_THUMBPRINT,
		            	os.getcwd() + self.get_property(self.section_name, "Public_Key_Upload_Path"))
		pair = KeyPair(SERVICE_CERT_THUMBPRINT, 
						os.getcwd() + self.get_property(self.section_name, "Public_Key_Upload_Path"))

		linux_config.ssh = SSH()

		linux_config.ssh.key_pairs.key_pairs.append(pair)
		linux_config.ssh.public_keys.public_keys.append(pk)

		# Configure the VM to accept SSH connections on port 22
		endpoint_config = ConfigurationSet()
		endpoint_config.configuration_set_type = 'NetworkConfiguration'

		ssh_endpoint = ConfigurationSetInputEndpoint(name='ssh', protocol='tcp', port='22', local_port='22', load_balanced_endpoint_set_name=None, enable_direct_server_return=False)
		endpoint_config.input_endpoints.input_endpoints.append(ssh_endpoint)

		# Finally create the VM:
		sms.create_virtual_machine_deployment(service_name=hosted_service_name,
		    deployment_name=hosted_service_name,
		    deployment_slot='production',
		    label=hosted_service_name,
		    role_name=hosted_service_name,
		    system_config=linux_config,
		    network_config=endpoint_config,
		    os_virtual_hard_disk=os_hd,
		    role_size='Small')
		print "Created VM"
		return (hosted_service_name, hosted_service_name+'.cloudapp.net', 
			self.get_property(self.section_name, "VM_Default_Username"))
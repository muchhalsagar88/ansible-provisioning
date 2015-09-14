import requests, json, time, os
import base_provider, namesgenerator, random
from base_provider import ServiceProvider
from azure import *
from azure.servicemanagement import *


class AzureProvider(ServiceProvider):

	SUBSCRIPTION_ID_OPTION = "Subscription_Id"
	SHARED_SIGNATURE_OPTION_NAME="Shared_Access_Signature"

	def __init__(self, base_url, section_name):
		self.base_url = base_url
		self.section_name = section_name
		super(AzureProvider, self).__init__()

	def create_instance(self):
		print "creating a Azure instance using url: ",self.base_url
		sms = self.__get_service_mgmt_object()

		name = namesgenerator.get_random_name()
		location = 'East US'

		service_name = self.get_property(self.section_name, "Cloud_Service_Name")

		# Name of an os image as returned by list_os_images
		image_name = 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04-LTS-amd64-server-20140414-en-us-30GB'

		# Destination storage account container/blob where the VM disk
		# will be created
		media_link = self.get_property(self.section_name, "Storage_Blob_Link")
		media_link += 'ubuntu_image.vdi'

		# Linux VM configuration, you can use WindowsConfigurationSet
		# for a Windows VM instead
		linux_config = LinuxConfigurationSet('myhostname', 'user', 'Password_123', True)

		os_hd = OSVirtualHardDisk(image_name, media_link)

		sms.create_virtual_machine_deployment(service_name=service_name,
		    deployment_name=name,
		    deployment_slot='production',
		    label=name,
		    role_name=name,
		    system_config=linux_config,
		    os_virtual_hard_disk=os_hd,
		    role_size='Small')
		print "Created a VM"

	def __get_service_mgmt_object(self):
		subscription_id = self.get_property(self.section_name, AzureProvider.SUBSCRIPTION_ID_OPTION)
		certificate_path = os.getcwd()+'/mycert.pem'

		return ServiceManagementService(subscription_id, certificate_path)	

ap = AzureProvider("abc", "Azure")
ap.create_instance()
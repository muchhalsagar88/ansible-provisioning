import requests, json, time, re
import base_provider, namesgenerator, random
from base_provider import ServiceProvider

class DigitalOceanProvider(ServiceProvider):

	TOKEN_OPTION_NAME = "Access_Token"
	
	def __init__(self, base_url, section_name):
		self.base_url = base_url
		self.section_name = section_name
		super(DigitalOceanProvider, self).__init__()

	def create_instance(self):
		#print "creating a digital ocean instance using url: ",self.base_url
		name = namesgenerator.get_random_name()
		droplet_id = self.__create_droplet(name)
		#print droplet_id
		return (name, self.__check_if_droplet_is_up(droplet_id), "root")
		#self.__delete_droplet(droplet_id)

	def __delete_droplet(self, id):
		response = self.__request(self.base_url, "DELETE", "/v2/droplets/"+str(id))	

	def __check_if_droplet_is_up(self, id):
		for i in range(0, 20):
			response = self.__request(self.base_url, "GET", "/v2/droplets/"+str(id))
			if len(response["droplet"]["networks"]["v4"]) is not 0:
				#print type(response["droplet"]["networks"]["v4"][0]["ip_address"])
				return response["droplet"]["networks"]["v4"][0]["ip_address"]
			time.sleep(1)

	def __create_droplet(self, name):
		params = {
			"name": name,
			"region": self.__get_random_region(),
			"size": "512mb",
			"image": "ubuntu-14-04-x64",
			"ssh_keys": self.__get_ssh_keys(),
			"backups": "false",
			"ipv6": "true",
			"user_data": "null",
			"private_networking": "null"
		}
		#print str(params)
		#print json.dumps(params)
		response = self.__request(self.base_url, "POST", "/v2/droplets", json.dumps(params))#, headers)
		if response is not None :
			return response['droplet']['id']
		else:
			print("None respose rceived") 

	def __get_random_region(self):
		regions = ["nyc1", "nyc2", "nyc3"]
		return regions[random.randint(0, len(regions)-1)]

	def __get_ssh_keys(self):
		keys = self.__request(self.base_url, "GET", "/v2/account/keys")
		ssh_keys = []
		ssh_keys += [keys['ssh_keys'][0]['id']]
		return ssh_keys

	def __request(self, base_url, method, relative_url, params=None, headers=None):
		acc_token = self.get_property(self.section_name, DigitalOceanProvider.TOKEN_OPTION_NAME)
		access_url = base_url + relative_url
		#print access_url
		if headers is None:
			headers = {
				"Content-Type":"application/json",
				"Authorization": "Bearer " + acc_token
			}
		if method is "GET":
			r = requests.get(access_url, headers=headers)
		elif method is "POST":
			r = requests.post(access_url, data=params, headers=headers)
		elif method is "DELETE":
			r = requests.delete(access_url, headers=headers)

		#print r.status_code
		p = re.compile("^[2][0-9]{2}")
		if p.match(str(r.status_code)):
			resp = r.text
			#print json.loads(resp)#, sort_keys=True, indent=4, separators=(',', ': '))
			return json.loads(resp)
			#return json.loads(response.read())	
		return None


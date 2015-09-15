import argparse
from docean_provider import DigitalOceanProvider
from azure_provider import AzureProvider

# option : whether to add a value by append/override
# 1: add or append
# 2: override
def write_to_inventory_file(option=1, *args):
	if option is 1:
		mode = 'a' 
	else:
		mode = 'w'
	fp = open('inventory', mode)
	s = '{} ansible_ssh_host={} ansible_ssh_user={}'.format(args[0], args[1], args[2])
	if len(args)>3:
		s += ' ansible_ssh_private_key_file={}'.format(args[3])
	fp.write(s+'\n')

parser = argparse.ArgumentParser()
parser.add_argument("provider", type=str, help="Enter the Cloud Provider you wish to use",
					choices=["DigitalOcean", "Azure"] )
parser.add_argument("write_mode", type=int, help="Enter the mode to write to inventory file. \n1: Append\n2: Override",
					choices=[1, 2])
args = parser.parse_args()

provider = args.provider
mode = args.write_mode
if provider=="DigitalOcean":
	di = DigitalOceanProvider("https://api.digitalocean.com", "DigitalOcean")
	(node_name, ip_address, user) = di.create_instance()
	write_to_inventory_file(mode, node_name, ip_address, user)
else:
	ap = AzureProvider("abc", "Azure")
	(node_name, ip_address, user) = ap.create_instance()
	write_to_inventory_file(mode, node_name, ip_address, user, 'id_rsa')

print "Node created at address: ",ip_address

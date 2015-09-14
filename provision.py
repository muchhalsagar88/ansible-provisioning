import argparse, docean_provider
from docean_provider import DigitalOceanProvider

# option : whether to add a value by append/override
# 1: add or append
# 2: override
def write_to_inventory_file(ip_address, option=1):
	if option is 1:
		mode = 'a' 
	else:
		mode = 'w'
	fp = open('inventory', mode)
	fp.write(ip_address+'\n')

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
	ip_address = di.create_instance()
	print "IP address of the created droplet is: ",ip_address
	write_to_inventory_file(ip_address, mode)
else:
	print "Nothing"


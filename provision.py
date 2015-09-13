import argparse

parser = argparse.ArgumentParser()
parser.add_argument("provider", type=string, help="Cloud Provider",
					choices=["DigitalOcean", "Azure"] )
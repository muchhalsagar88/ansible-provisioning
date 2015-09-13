import httplib, abc, os
import ConfigParser

class ServiceProvider(object):
	__metaclass__ = abc.ABCMeta

	def __init__(self):
		self.cp = ConfigParser.ConfigParser()
		self.cp.read(os.getcwd()+"/config.ini")
	
	@abc.abstractmethod
	def create_instance(self, input):
		""" Create an instance using the appropriate API """
		return

	def get_property(self, section_name, option_name):
		if(self.cp.has_section(section_name)):
			if(self.cp.has_option(section_name, option_name)):
				return self.cp.get(section_name, option_name)
		return None


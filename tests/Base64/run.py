from pysys.constants import *
from pysys.basetest import BaseTest
from apama.correlator import CorrelatorHelper
import os

class PySysTest(BaseTest):
	def execute(self):
		corr = CorrelatorHelper(self, name='correlator')
		corr.start(logfile='correlator.log')
		corr.injectEPL(filenames=['ConnectivityPluginsControl.mon', 'ConnectivityPlugins.mon', 'AnyExtractor.mon', 'data_storage/MemoryStore.mon', 'HTTPClientEvents.mon', 'TimeFormatEvents.mon'], filedir=self.project.APAMA_HOME+'/monitors')
		corr.injectEPL('../../../AuthenticationPlugin.mon')
		tests = os.listdir(self.input);
		tests.sort()
		for test in tests:
			if test.endswith('.mon'):
				corr.injectEPL(test)
				corr.flush()
		corr.shutdown()

	def validate(self):
		self.assertGrep('correlator.log', expr=' ERROR ', contains=False)
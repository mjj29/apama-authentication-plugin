from pysys.constants import *
from pysys.basetest import BaseTest
from apama.correlator import CorrelatorHelper
import os

class PySysTest(BaseTest):
	def execute(self):

		# start initial correlator
		self.copy(self.input+'/storedb', self.output)
		storepath = os.path.join(self.output,'storedb')
		corr = CorrelatorHelper(self, name='correlator')
		corr.start(logfile='correlator.log', arguments=['--applicationLogLevel', 'DEBUG'])
		self.runTest(corr, f'TestRun("{storepath}")')
		corr.shutdown()

	def runTest(self, corr, event):
		corr.injectEPL(filenames=['ConnectivityPluginsControl.mon', 'ConnectivityPlugins.mon', 'AnyExtractor.mon', 'data_storage/MemoryStore.mon', 'HTTPClientEvents.mon', 'TimeFormatEvents.mon'], filedir=self.project.APAMA_HOME+'/monitors')
		corr.injectEPL('../../../AuthenticationPlugin.mon')
		tests = os.listdir(self.input);
		tests.sort()
		for test in tests:
			if test.endswith('.mon'):
				corr.injectEPL(test)
		corr.sendEventStrings(event)
		corr.flush(count=2)

	def validate(self):
		self.assertGrep('correlator.log', expr=' ERROR ', contains=False)
		self.assertGrep('correlator.log', expr='Completed tests')

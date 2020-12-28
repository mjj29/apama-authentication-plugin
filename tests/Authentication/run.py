from pysys.constants import *
from pysys.basetest import BaseTest
from apama.correlator import CorrelatorHelper
import os

class PySysTest(BaseTest):
	def execute(self):

		# start initial correlator
		pathpath = os.path.join(self.output,'pathdb')
		storepath = os.path.join(self.output,'storedb')
		corr = CorrelatorHelper(self, name='correlator-init')
		corr.start(logfile='correlator-init.log')
		self.runTest(corr, f'TestRun("{pathpath}","{storepath}",true)')
		corr.shutdown()
		corr = CorrelatorHelper(self, name='correlator-recovery')
		corr.start(logfile='correlator-recovery.log')
		self.runTest(corr, f'TestRun("{pathpath}","{storepath}",false)')
		corr.shutdown()


	def runTest(self, corr, event):
		corr.injectEPL(filenames=['ConnectivityPluginsControl.mon', 'ConnectivityPlugins.mon', 'AnyExtractor.mon', 'data_storage/MemoryStore.mon', 'HTTPClientEvents.mon'], filedir=self.project.APAMA_HOME+'/monitors')
		corr.injectEPL('../../../AuthenticationPlugin.mon')
		tests = os.listdir(self.input);
		tests.sort()
		for test in tests:
			if test.endswith('.mon'):
				corr.injectEPL(test)
				corr.sendEventStrings(event)
				corr.flush(count=2)

	def validate(self):
		for i in [ "fromStore", "fromPath", "inMemory" ]:
			self.assertGrep('correlator-init.log', expr='Starting tests for '+i)
			self.assertGrep('correlator-init.log', expr='Completed tests for '+i)
			self.assertGrep('correlator-recovery.log', expr='Starting tests for '+i)
			self.assertGrep('correlator-recovery.log', expr='Completed tests for '+i)
		self.assertGrep('correlator-init.log', expr=' ERROR ', contains=False)
		self.assertGrep('correlator-recovery.log', expr=' ERROR ', contains=False)

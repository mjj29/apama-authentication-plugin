from pysys.constants import *
from pysys.basetest import BaseTest
from apama.correlator import CorrelatorHelper
import os

class PySysTest(BaseTest):
	def execute(self):
		corr = CorrelatorHelper(self, name='correlator')
		corr.start(logfile='correlator.log', Xclock=True)
		corr.injectEPL(filenames=['ConnectivityPluginsControl.mon', 'ConnectivityPlugins.mon', 'AnyExtractor.mon', 'data_storage/MemoryStore.mon', 'HTTPClientEvents.mon'], filedir=self.project.APAMA_HOME+'/monitors')
		corr.injectEPL('TimeFormat.mon')
		corr.injectEPL('../../../AuthenticationPlugin.mon')
		corr.injectEPL('00Asserts.mon')
		corr.injectEPL('test.mon')
		corr.sendEventStrings("&TIME(50)")
		corr.flush()
		corr.shutdown()

	def validate(self):
		self.assertGrep('correlator.log', expr=' ERROR ', contains=False)
		for t in [5, 13, 22, 31]:
			self.assertGrep('correlator.log', expr=f'timer - {t}s')

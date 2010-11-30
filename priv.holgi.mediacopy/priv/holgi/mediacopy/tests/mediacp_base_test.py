from os import remove, rmdir, path
from tempfile import mkdtemp, gettempdir
from unittest import TestCase

class MediacpTestBase(TestCase):
    ''' class for providing base functionality required by Test classes 
    Serves basically as some kind of a zope.testing layer, w/o the benefits
    of a real layer.
    '''
    def _setup_testdir(self):
        ''' Generate a new temporary directory as a target for copying '''
        newdir=mkdtemp('','mct',gettempdir())
        self.destdir=newdir

    def _teardown_testdir(self):
        ''' Remove the temporary directory as a target for copying '''
        if self.destdir:
            rmdir(self.destdir)

    def _setup_testpic(self):
        ''' Provide the test picture '''
        package_dir = path.dirname(__file__)
        self.testfilename = 'CIMG2448.JPG'
        self.testfile = path.join(package_dir, self.testfilename)

    def _teardown_testpic(self):
        ''' Remove a possible copy of the test picture '''
        if path.exists(self._copiedfilepath):
            remove(self._copiedfilepath)

    @property
    def _copiedfilepath(self):
        return path.join(self.destdir, self.testfilename)

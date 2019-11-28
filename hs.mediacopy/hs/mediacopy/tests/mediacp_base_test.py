'''
    mediacp_base_test.py -- basic setup for tests.
    This file is part of mediacopy.

    Copyright (C) 2010 Holger Schauer <holger.schauer@gmx.de>

    mediacopy is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from os import remove, rmdir, path
from tempfile import mkdtemp, gettempdir
from unittest import TestCase

class MediacpTestBase(TestCase):
    ''' class for providing base functionality required by Test classes
    Serves basically as some kind of a zope.testing layer, w/o the benefits
    of a real layer.
    '''
    def setUp(self):
        super(MediacpTestBase, self).setUp()

    def _setup_testdir(self):
        ''' Generate a new temporary directory as a target for copying '''
        newdir=mkdtemp('','mct',gettempdir())
        self.destdir=str(newdir)

    def _teardown_testdir(self):
        ''' Remove the temporary directory as a target for copying '''
        if self.destdir:
            rmdir(self.destdir)

    def _setup_testpic(self):
        ''' Provide the test picture '''
        package_dir = path.dirname(__file__)
        self.testfilename = 'CIMG2448.JPG'
        self.testfile = str(path.join(package_dir, self.testfilename))

    def _teardown_testpic(self):
        ''' Remove a possible copy of the test picture '''
        if path.exists(self._copiedfilepath):
            remove(self._copiedfilepath)

    @property
    def _copiedfilepath(self):
        return str(path.join(self.destdir, self.testfilename))

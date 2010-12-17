'''
    applogic_test.py -- tests related to the main applogic.
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

import os
from nose.tools import raises, istest, eq_
from priv.holgi.mediacopy.utils import make_dsn, logger
from priv.holgi.mediacopy.infostore import make_infostore
from priv.holgi.mediacopy.applogic import mediacopy_directory, \
    store_metainfo_directory
from priv.holgi.mediacopy.tests.mediacp_base_test import MediacpTestBase

class OptionsStub(object):
    def __init__(self, **kw):
        for key, value in kw.items():
            setattr(self, key, value)
        
class Applogic_Test(MediacpTestBase):
    
    def setUp(self):
        self.infostore = make_infostore('sqlite://')
        self.sourcedir = os.path.dirname(__file__)
        self._setup_testdir()
        self._setup_testpic()
        super(Applogic_Test, self).setUp()

    def tearDown(self):
        self._teardown_testpic()
        self._teardown_testdir()
        super(Applogic_Test, self).tearDown()
        
    @istest
    def storedir_adds_new_metainfo(self):
        options = OptionsStub(encoding='utf-8', verbose=False)
        eq_(len(self.infostore.get_all_metainfos()), 0)
        (seen, dupes) = store_metainfo_directory(self.infostore, self.sourcedir, options, (0,0))
        eq_((seen > 1), True)
        eq_(dupes, 0)
        eq_(len(self.infostore.get_all_metainfos()), 1)

    @istest
    def copydir_copies_file(self):
        options = OptionsStub(encoding='utf-8', verbose=None, noaction=None, force=None, unknown=None, destination=self.destdir)
        (seen, copied, dupes) = mediacopy_directory(self.sourcedir, self.destdir, self.infostore, options, (0,0,0))
        eq_((seen > 1), True)
        eq_(dupes, 0)
        eq_(copied, 1)
        assert (os.path.exists(self._copiedfilepath) and
                os.access(self._copiedfilepath, os.R_OK))

    @istest
    def copydir_adds_new_metainfo(self):
        options = OptionsStub(encoding='utf-8', verbose=None, noaction=None, force=None, unknown=None, destination=self.destdir)
        eq_(len(self.infostore.get_all_metainfos()), 0)
        (seen, copied, dupes) = mediacopy_directory(self.sourcedir, self.destdir, self.infostore, options, (0,0,0))
        eq_((seen > 1), True)
        eq_(copied, 1)
        eq_(dupes, 0)
        eq_(len(self.infostore.get_all_metainfos()), 1)
        

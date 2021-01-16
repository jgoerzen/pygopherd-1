import os.path
import unittest

from pygopherd import testutil
from pygopherd.handlers.base import VFS_Real
from pygopherd.handlers.UMN import UMNDirHandler


class TestUMNDirHandler(unittest.TestCase):
    def setUp(self):
        self.config = testutil.getconfig()
        self.vfs = VFS_Real(self.config)
        self.selector = "/"
        self.protocol = testutil.gettestingprotocol(self.selector, config=self.config)
        self.stat_result = self.vfs.stat(self.selector)

        # Make sure there's no directory cache file from a previous test run
        cachefile = self.config.get("handlers.dir.DirHandler", "cachefile")
        try:
            os.remove(self.vfs.getfspath(self.selector) + "/" + cachefile)
        except OSError:
            pass

    def test_dir_handler(self):
        handler = UMNDirHandler(
            self.selector, "", self.protocol, self.config, self.stat_result, self.vfs
        )

        self.assertTrue(handler.canhandlerequest())
        self.assertTrue(handler.isdir())

        handler.prepare()
        self.assertFalse(handler.fromcache)

        entry = handler.getentry()
        self.assertEqual(entry.mimetype, "application/gopher-menu")
        self.assertEqual(entry.type, "1")

        entries = handler.getdirlist()
        self.assertTrue(entries)

        # First entry should be the special link file
        self.assertEqual(entries[0].name, "Cheese Ball Recipes")
        self.assertEqual(entries[0].host, "zippy.micro.umn.edu")
        self.assertEqual(entries[0].port, 150)

        # Second entry should be the special cap file
        self.assertEqual(entries[2].name, "New Long Cool Name")
        self.assertEqual(entries[2].selector, "/zzz.txt")

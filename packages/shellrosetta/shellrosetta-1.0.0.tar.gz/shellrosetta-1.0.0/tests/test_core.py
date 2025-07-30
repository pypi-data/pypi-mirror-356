# tests/test_core.py

import unittest
from shellrosetta.core import lnx2ps, ps2lnx

class TestShellRosettaCore(unittest.TestCase):
    def test_ls_translation(self):
        self.assertIn("Get-ChildItem", lnx2ps("ls"))
        self.assertIn("Get-ChildItem | Format-List", lnx2ps("ls -l"))
        self.assertIn("-Force", lnx2ps("ls -a"))
        self.assertIn("-Force | Format-List", lnx2ps("ls -la"))

    def test_rm_translation(self):
        self.assertIn("Remove-Item", lnx2ps("rm"))
        self.assertIn("-Recurse -Force", lnx2ps("rm -rf /tmp/test"))
    
    def test_ps2lnx(self):
        self.assertIn("ls", ps2lnx("Get-ChildItem"))
        self.assertIn("ls -a", ps2lnx("Get-ChildItem -Force"))
        self.assertIn("rm -rf", ps2lnx("Remove-Item -Recurse -Force"))

if __name__ == '__main__':
    unittest.main()

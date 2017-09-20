#
# This file is part of pysmi software.
#
# Copyright (c) 2015-2017, Ilya Etingof <etingof@gmail.com>
# License: http://pysmi.sf.net/license.html
#
import sys
import os
import tempfile

try:
    import unittest2 as unittest

except ImportError:
    import unittest

try:
    import StringIO

except ImportError:
    from io import StringIO

from pysmi.reader import ZipReader


class ZipReaderTestCase(unittest.TestCase):

    zipArchive = [80, 75, 3, 4, 10, 0, 0, 0, 0, 0, 54, 69, 52, 75, 0, 0, 0, 0,
                  0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 28, 0, 122, 105, 112, 47, 85,
                  84, 9, 0, 3, 167, 13, 194, 89, 193, 13, 194, 89, 117, 120,
                  11, 0, 1, 4, 245, 1, 0, 0, 4, 0, 0, 0, 0, 80, 75, 3, 4, 10,
                  0, 0, 0, 0, 0, 64, 69, 52, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                  0, 0, 11, 0, 28, 0, 122, 105, 112, 47, 115, 117, 98, 100, 105,
                  114, 47, 85, 84, 9, 0, 3, 183, 13, 194, 89, 193, 13, 194, 89,
                  117, 120, 11, 0, 1, 4, 245, 1, 0, 0, 4, 0, 0, 0, 0, 80, 75, 3,
                  4, 10, 0, 0, 0, 0, 0, 60, 69, 52, 75, 27, 55, 89, 124, 6, 0, 0,
                  0, 6, 0, 0, 0, 20, 0, 28, 0, 122, 105, 112, 47, 115, 117, 98,
                  100, 105, 114, 47, 116, 101, 115, 116, 49, 46, 116, 120, 116,
                  85, 84, 9, 0, 3, 179, 13, 194, 89, 179, 13, 194, 89, 117, 120,
                  11, 0, 1, 4, 245, 1, 0, 0, 4, 0, 0, 0, 0, 116, 101, 115, 116,
                  49, 10, 80, 75, 3, 4, 10, 0, 0, 0, 0, 0, 64, 69, 52, 75, 216,
                  100, 116, 87, 6, 0, 0, 0, 6, 0, 0, 0, 20, 0, 28, 0, 122, 105,
                  112, 47, 115, 117, 98, 100, 105, 114, 47, 116, 101, 115, 116,
                  50, 46, 116, 120, 116, 85, 84, 9, 0, 3, 183, 13, 194, 89, 183,
                  13, 194, 89, 117, 120, 11, 0, 1, 4, 245, 1, 0, 0, 4, 0, 0, 0,
                  0, 116, 101, 115, 116, 50, 10, 80, 75, 3, 4, 10, 0, 0, 0, 0,
                  0, 49, 69, 52, 75, 27, 55, 89, 124, 6, 0, 0, 0, 6, 0, 0, 0, 13,
                  0, 28, 0, 122, 105, 112, 47, 116, 101, 115, 116, 49, 46, 116,
                  120, 116, 85, 84, 9, 0, 3, 158, 13, 194, 89, 158, 13, 194, 89,
                  117, 120, 11, 0, 1, 4, 245, 1, 0, 0, 4, 0, 0, 0, 0, 116, 101,
                  115, 116, 49, 10, 80, 75, 1, 2, 30, 3, 10, 0, 0, 0, 0, 0, 54,
                  69, 52, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 24, 0,
                  0, 0, 0, 0, 0, 0, 16, 0, 237, 65, 0, 0, 0, 0, 122, 105, 112,
                  47, 85, 84, 5, 0, 3, 167, 13, 194, 89, 117, 120, 11, 0, 1, 4,
                  245, 1, 0, 0, 4, 0, 0, 0, 0, 80, 75, 1, 2, 30, 3, 10, 0, 0, 0,
                  0, 0, 64, 69, 52, 75, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11,
                  0, 24, 0, 0, 0, 0, 0, 0, 0, 16, 0, 237, 65, 62, 0, 0, 0, 122,
                  105, 112, 47, 115, 117, 98, 100, 105, 114, 47, 85, 84, 5, 0, 3,
                  183, 13, 194, 89, 117, 120, 11, 0, 1, 4, 245, 1, 0, 0, 4, 0, 0,
                  0, 0, 80, 75, 1, 2, 30, 3, 10, 0, 0, 0, 0, 0, 60, 69, 52, 75,
                  27, 55, 89, 124, 6, 0, 0, 0, 6, 0, 0, 0, 20, 0, 24, 0, 0, 0, 0,
                  0, 1, 0, 0, 0, 164, 129, 131, 0, 0, 0, 122, 105, 112, 47, 115,
                  117, 98, 100, 105, 114, 47, 116, 101, 115, 116, 49, 46, 116, 120,
                  116, 85, 84, 5, 0, 3, 179, 13, 194, 89, 117, 120, 11, 0, 1, 4, 245,
                  1, 0, 0, 4, 0, 0, 0, 0, 80, 75, 1, 2, 30, 3, 10, 0, 0, 0, 0, 0, 64,
                  69, 52, 75, 216, 100, 116, 87, 6, 0, 0, 0, 6, 0, 0, 0, 20, 0, 24,
                  0, 0, 0, 0, 0, 1, 0, 0, 0, 164, 129, 215, 0, 0, 0, 122, 105, 112,
                  47, 115, 117, 98, 100, 105, 114, 47, 116, 101, 115, 116, 50, 46,
                  116, 120, 116, 85, 84, 5, 0, 3, 183, 13, 194, 89, 117, 120, 11, 0,
                  1, 4, 245, 1, 0, 0, 4, 0, 0, 0, 0, 80, 75, 1, 2, 30, 3, 10, 0, 0,
                  0, 0, 0, 49, 69, 52, 75, 27, 55, 89, 124, 6, 0, 0, 0, 6, 0, 0, 0,
                  13, 0, 24, 0, 0, 0, 0, 0, 1, 0, 0, 0, 164, 129, 43, 1, 0, 0, 122,
                  105, 112, 47, 116, 101, 115, 116, 49, 46, 116, 120, 116, 85, 84,
                  5, 0, 3, 158, 13, 194, 89, 117, 120, 11, 0, 1, 4, 245, 1, 0, 0,
                  4, 0, 0, 0, 0, 80, 75, 5, 6, 0, 0, 0, 0, 5, 0, 5, 0, 162, 1, 0, 0,
                  120, 1, 0, 0, 0, 0]

    try:
        zipContents = bytes(zipArchive)

    except AttributeError:
        zipContents = ''.join([chr(x) for x in zipArchive])

    def testGetData(self):

        try:
            fd, filename = tempfile.mkstemp()
            os.write(fd, self.zipContents)
            os.close(fd)

            zipReader = ZipReader(filename)

            mibinfo, data = zipReader.getData('test1')
            assert data == 'test1\n'

        finally:
            try:
                os.remove(filename)

            except:
                pass


suite = unittest.TestLoader().loadTestsFromModule(sys.modules[__name__])

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite)

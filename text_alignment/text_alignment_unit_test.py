import unittest
import text_alignment


class TestStringMethods(unittest.TestCase):

    def setUp(self):
        self.parser = text_alignment.create_parser()

    def test_correct_input(self):
        t1 = ["G", "C", "A", "T", "G", "C", "U"]
        t2 = ["G", "A", "T", "T", "A", "C", "A"]
        pgap = -2
        pxy = -3

        result = text_alignment.build_table(t1, t2, pgap, pxy)
        self.assertEqual(result, [['G', 'C', 'A', '_', 'T', 'G', 'C', 'U'], ['G', '_', 'A', 'T', 'T', 'A', 'C', 'A']])

    def test_define_parser(self):
        args = ['-f1', 'file1.txt', '-f2', 'file2.txt', '-o', 'output.txt']

        parsed = self.parser.parse_args(args)
        result = [parsed.file1, parsed.file2, parsed.output]

        self.assertEqual(result, ['file1.txt', 'file2.txt', 'output.txt'])


if __name__ == '__main__':
    unittest.main()

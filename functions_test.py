#!/usr/bin/python
# coding=utf-8

import unittest
import functions

class TestMethods(unittest.TestCase):
    
    def test_is_valid_dns_name(self):
        self.assertTrue(functions.is_valid_dns_name("example.com"))
        self.assertTrue(functions.is_valid_dns_name("example"))
        self.assertTrue(functions.is_valid_dns_name("localhost"))
        self.assertTrue(functions.is_valid_dns_name("ex.exaple.example.example.example.example.example.example.com"))
        self.assertFalse(functions.is_valid_dns_name("example.example.example.example.example.example.example.example.com"))
        self.assertTrue(functions.is_valid_dns_name("ex.exa-ple.example.example.example.example.example.example.com"))
        self.assertFalse(functions.is_valid_dns_name("ex.-exa-ple.example.example.example.example.example.example.com"))
        self.assertFalse(functions.is_valid_dns_name("ex.exa-ple-.example.example.example.example.example.example.com"))
        self.assertFalse(functions.is_valid_dns_name("127.0.0.1"))
        self.assertFalse(functions.is_valid_dns_name("127"))
        self.assertFalse(functions.is_valid_dns_name("127.0"))
        self.assertFalse(functions.is_valid_dns_name("127.0.0.1.0"))
        self.assertFalse(functions.is_valid_dns_name("-127.0.0.1"))
        self.assertFalse(functions.is_valid_dns_name("256.0.0.1"))
        self.assertFalse(functions.is_valid_dns_name("1234:abcd:1234:abcd:1234"))
        self.assertFalse(functions.is_valid_dns_name("1234"))
        self.assertTrue(functions.is_valid_dns_name("12ab"))
        self.assertFalse(functions.is_valid_dns_name("1234:abcd:1234:abcd:1234:abcd"))
        self.assertFalse(functions.is_valid_dns_name("1234:abcd:-1234:abcd:1234:abcd"))
        self.assertFalse(functions.is_valid_dns_name("1234:gbcd:1234:abcd:1234:abcd"))
    
    def test_is_valid_ipv4_address(self):
        self.assertFalse(functions.is_valid_ipv4_address("example.com"))
        self.assertFalse(functions.is_valid_ipv4_address("example"))
        self.assertFalse(functions.is_valid_ipv4_address("localhost"))
        self.assertFalse(functions.is_valid_ipv4_address("ex.exaple.example.example.example.example.example.example.com"))
        self.assertFalse(functions.is_valid_ipv4_address("example.example.example.example.example.example.example.example.com"))
        self.assertFalse(functions.is_valid_ipv4_address("ex.exa-ple.example.example.example.example.example.example.com"))
        self.assertFalse(functions.is_valid_ipv4_address("ex.-exa-ple.example.example.example.example.example.example.com"))
        self.assertFalse(functions.is_valid_ipv4_address("ex.exa-ple-.example.example.example.example.example.example.com"))
        self.assertTrue(functions.is_valid_ipv4_address("127.0.0.1"))
        self.assertFalse(functions.is_valid_ipv4_address("127"))
        self.assertFalse(functions.is_valid_ipv4_address("127.0"))
        self.assertFalse(functions.is_valid_ipv4_address("127.0.0.1.0"))
        self.assertFalse(functions.is_valid_ipv4_address("-127.0.0.1"))
        self.assertFalse(functions.is_valid_ipv4_address("256.0.0.1"))
        self.assertFalse(functions.is_valid_ipv4_address("1234:abcd:1234:abcd:1234"))
        self.assertFalse(functions.is_valid_ipv4_address("1234"))
        self.assertFalse(functions.is_valid_ipv4_address("12ab"))
        self.assertFalse(functions.is_valid_ipv4_address("1234:abcd:1234:abcd:1234:abcd"))
        self.assertFalse(functions.is_valid_ipv4_address("1234:abcd:-1234:abcd:1234:abcd"))
        self.assertFalse(functions.is_valid_ipv4_address("1234:gbcd:1234:abcd:1234:abcd"))
    
    def test_is_valid_ipv6_address(self):
        self.assertFalse(functions.is_valid_ipv6_address("example.com"))
        self.assertFalse(functions.is_valid_ipv6_address("example"))
        self.assertFalse(functions.is_valid_ipv6_address("localhost"))
        self.assertFalse(functions.is_valid_ipv6_address("ex.exaple.example.example.example.example.example.example.com"))
        self.assertFalse(functions.is_valid_ipv6_address("example.example.example.example.example.example.example.example.com"))
        self.assertFalse(functions.is_valid_ipv6_address("ex.exa-ple.example.example.example.example.example.example.com"))
        self.assertFalse(functions.is_valid_ipv6_address("ex.-exa-ple.example.example.example.example.example.example.com"))
        self.assertFalse(functions.is_valid_ipv6_address("ex.exa-ple-.example.example.example.example.example.example.com"))
        self.assertFalse(functions.is_valid_ipv6_address("127.0.0.1"))
        self.assertFalse(functions.is_valid_ipv6_address("127"))
        self.assertFalse(functions.is_valid_ipv6_address("127.0"))
        self.assertFalse(functions.is_valid_ipv6_address("127.0.0.1.0"))
        self.assertFalse(functions.is_valid_ipv6_address("-127.0.0.1"))
        self.assertFalse(functions.is_valid_ipv6_address("256.0.0.1"))
        self.assertTrue(functions.is_valid_ipv6_address("1234:abcd:1234:abcd:1234"))
        self.assertFalse(functions.is_valid_ipv6_address("1234"))
        self.assertFalse(functions.is_valid_ipv6_address("12ab"))
        self.assertFalse(functions.is_valid_ipv6_address("1234:abcd:1234:abcd:1234:abcd"))
        self.assertFalse(functions.is_valid_ipv6_address("1234:abcd:-1234:abcd:1234:abcd"))
        self.assertFalse(functions.is_valid_ipv6_address("1234:gbcd:1234:abcd:1234:abcd"))
    
    def test_is_valid_port(self):
        from random import randrange
        from sys import maxsize
        min_port = 0
        num_ports = 65536
        for i in range(min_port, num_ports):
            self.assertTrue(functions.is_valid_port(i))
        self.assertFalse(functions.is_valid_port(min_port - 1 - randrange(maxsize)))
        self.assertFalse(functions.is_valid_port(num_ports + randrange(maxsize)))
    
    def test_matches_regex(self):
        self.assertTrue(functions.matches_regex("^\d$", "5"))
        self.assertFalse(functions.matches_regex("^\d$", "a"))
        
    def test_execute_command(self):
        from subprocess import CalledProcessError
        out, err = functions.execute_command(["sleep", "0"])
        self.assertEqual(out, None)
        self.assertEqual(err, None)
        try:
            out, err = functions.execute_command(["sleep", "-1"], None, True)
            self.fail("No exception has been raised.")
        except CalledProcessError as e:
            self.assertEqual(e.output, b"")
            self.assertEqual(e.stderr, b"sleep: invalid option -- '1'\nTry 'sleep --help' for more information.\n")
        out, err = functions.execute_command(["echo", "ola"], None, True)
        self.assertEqual(out, b"ola\n")
        self.assertEqual(err, b"")
        out, err = functions.execute_command(["cat"], "ola\n", True)
        self.assertEqual(out, b"ola\n")
        self.assertEqual(err, b"")
    
    def test_replace_text_in_file(self):
        original_string = "123\n456\n"
        new_string = original_string + "123\nabc\n"
        file_path = AuxiliaryTestMethods.create_temp_text_file(original_string)
        self.assertEqual(functions.read_file(file_path), original_string)
        self.assertNotEqual(functions.read_file(file_path), new_string)
        functions.replace_text_in_file(original_string, new_string, file_path)
        self.assertEqual(functions.read_file(file_path), new_string)
        self.assertNotEqual(functions.read_file(file_path), original_string)
        AuxiliaryTestMethods.remove_temp_file(self, file_path)
    
    def test_read_file(self):
        from sys import argv
        text1 = functions.read_file(argv[0])
        text2 = functions.read_file(argv[0])
        self.assertEqual(text1, text2)
        self.assertTrue("def test_read_file(self):" in text1)

        string = "123\n456\n"
        file_path = AuxiliaryTestMethods.create_temp_text_file(string)
        text3 = functions.read_file(file_path)
        self.assertNotEqual(text1, text3)
        self.assertEqual(text3, string)
        AuxiliaryTestMethods.remove_temp_file(self, file_path)
    
    def test_write_file(self):
        empty_string = ""
        text = "123\n456\n"
        file_path = AuxiliaryTestMethods.create_temp_text_file(empty_string)
        self.assertEqual(functions.read_file(file_path), empty_string)
        self.assertNotEqual(functions.read_file(file_path), text)
        functions.write_file(file_path, text)
        self.assertEqual(functions.read_file(file_path), text)
        AuxiliaryTestMethods.remove_temp_file(self, file_path)
    
    def test_chmod_recursive(self):
        pass # TODO
    
    def test_decompress_gzip_file(self):
        pass # TODO
    
    def test_makedirs(self):
        pass # TODO
    
    def test_get_default_network_device(self):
        default_network_device = functions.get_default_network_device()
        if default_network_device != None:
            self.assertEqual(type(default_network_device), str)
            self.assertNotEqual(default_network_device, "")
    
    def test_move_content(self):
        pass # TODO
    
    def test_get_python_version(self):
        python_version = functions.get_python_version()
        self.assertEqual(type(python_version), int)
        self.assertTrue(python_version >= 0)

class AuxiliaryTestMethods():
    def create_temp_text_file(text):
        from tempfile import mkstemp
        fd, file_path = mkstemp(text = True)
        functions.write_file(file_path, text)
        return file_path 

    def remove_temp_file(test_class, file_path):
        from tempfile import gettempdir
        from os import remove, listdir, path
        file_basename = path.basename(file_path)
        test_class.assertFalse(file_basename not in listdir(gettempdir()))
        remove(file_path)
        test_class.assertTrue(file_basename not in listdir(gettempdir()))

if __name__ == '__main__':
    unittest.main()

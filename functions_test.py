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
        pass # TODO
    
    def test_replace_text_in_file(self):
        pass # TODO
    
    def test_read_file(self):
        pass # TODO
    
    def test_execute_and_send_input_to_command(self):
        pass # TODO
    
    def test_chmod_recursive(self):
        pass # TODO
    
    def test_decompress_gzip_file(self):
        pass # TODO
    
    def test_makedirs(self):
        pass # TODO
    
    def test_get_command_output(self):
        pass # TODO
    
    def test_get_default_network_device(self):
        pass # TODO
    
    def test_move_content(self):
        pass # TODO
    
    def test_verify_python_version(self):
        pass #TODO

if __name__ == '__main__':
    unittest.main()

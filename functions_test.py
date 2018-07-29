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
        min_port = 0
        num_ports = 65536
        for i in range(min_port, num_ports):
            self.assertTrue(functions.is_valid_port(i))
        self.assertFalse(functions.is_valid_port(min_port - 1 - AuxiliaryTestMethods.get_random()))
        self.assertFalse(functions.is_valid_port(num_ports + AuxiliaryTestMethods.get_random()))
    
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
            self.assertEqual(e.output, "")
            self.assertTrue(e.stderr.startswith("sleep:"))
            self.assertTrue("'1'\n" in e.stderr)
            self.assertTrue("'sleep --help'" in e.stderr)
        out, err = functions.execute_command(["echo", "ola"], None, True)
        self.assertEqual(out, "ola\n")
        self.assertEqual(err, "")
        out, err = functions.execute_command(["cat"], "ola\n", True)
        self.assertEqual(out, "ola\n")
        self.assertEqual(err, "")
    
    def test_replace_text_in_file(self):
        from os import remove
        original_string = "123\n456\n"
        new_string = original_string + "123\nabc\n"
        file_path = AuxiliaryTestMethods.create_temp_text_file(original_string)
        self.assertEqual(functions.read_file(file_path), original_string)
        self.assertNotEqual(functions.read_file(file_path), new_string)
        functions.replace_text_in_file(original_string, new_string, file_path)
        self.assertEqual(functions.read_file(file_path), new_string)
        self.assertNotEqual(functions.read_file(file_path), original_string)
        remove(file_path)
    
    def test_read_file(self):
        from sys import argv
        from os import remove
        text1 = functions.read_file(argv[0])
        text2 = functions.read_file(argv[0])
        self.assertEqual(text1, text2)
        self.assertTrue("def test_read_file(self):" in text1)

        string = "123\n456\n"
        file_path = AuxiliaryTestMethods.create_temp_text_file(string)
        text3 = functions.read_file(file_path)
        self.assertNotEqual(text1, text3)
        self.assertEqual(text3, string)
        remove(file_path)
    
    def test_write_file(self):
        from os import remove
        empty_string = ""
        text = "123\n456\n"
        file_path = AuxiliaryTestMethods.create_temp_text_file(empty_string)
        self.assertEqual(functions.read_file(file_path), empty_string)
        self.assertNotEqual(functions.read_file(file_path), text)
        functions.write_file(file_path, text)
        self.assertEqual(functions.read_file(file_path), text)
        remove(file_path)
    
    def test_chmod_recursive(self):
        from shutil import rmtree
        new_mode = 0o740
        temp_dir = AuxiliaryTestMethods.create_temp_dir_populated(self)
        AuxiliaryTestMethods.check_mode_recursive(self.assertNotEqual, temp_dir, new_mode, check_root = True)
        functions.chmod_recursive(temp_dir, new_mode)
        AuxiliaryTestMethods.check_mode_recursive(self.assertEqual, temp_dir, new_mode, check_root = True)
        rmtree(temp_dir)
    
    def test_decompress_gzip_file(self):
        pass
    
    def test_makedirs(self):
        from tempfile import mkdtemp
        from os import path
        from shutil import rmtree
        temp_folder_path = mkdtemp()
        first_new_folder_path = path.join(temp_folder_path, AuxiliaryTestMethods.get_random_str())
        full_new_path = path.join(first_new_folder_path, AuxiliaryTestMethods.get_random_str(), AuxiliaryTestMethods.get_random_str())
        mode = 0o740
        self.assertNotEqual(AuxiliaryTestMethods.get_st_mode(temp_folder_path), mode)
        self.assertFalse(path.exists(first_new_folder_path))
        functions.makedirs(full_new_path, mode)
        self.assertTrue(path.exists(full_new_path))
        AuxiliaryTestMethods.check_mode_recursive(self.assertEqual, first_new_folder_path, mode, check_root = False)
        rmtree(temp_folder_path)
    
    def test_get_default_network_device(self):
        default_network_device = functions.get_default_network_device()
        if default_network_device != None:
            self.assertEqual(type(default_network_device), str)
            self.assertNotEqual(default_network_device, "")
    
    def test_move_content(self):
        from tempfile import mkdtemp
        from shutil import rmtree
        temp_folder1_path = AuxiliaryTestMethods.create_temp_dir_populated(self)
        temp_folder1_content = AuxiliaryTestMethods.listdir_recursive(temp_folder1_path)
        self.assertNotEqual(temp_folder1_content, [])
        temp_folder2_path = mkdtemp()
        temp_folder2_content = AuxiliaryTestMethods.listdir_recursive(temp_folder2_path)
        self.assertEqual(temp_folder2_content, [])
        functions.move_content(temp_folder1_path, temp_folder2_path)
        temp_folder2_content = AuxiliaryTestMethods.listdir_recursive(temp_folder2_path)
        self.assertEqual(temp_folder1_content, temp_folder2_content)
        rmtree(temp_folder1_path)
        rmtree(temp_folder2_path)
    
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

    def get_random():
        from random import randrange
        from sys import maxsize
        return randrange(maxsize)

    def get_random_str():
        return str(AuxiliaryTestMethods.get_random())

    def create_temp_dir_populated(test_class):
        def create_temp_dir_populated_aux(test_class, current_path, depth = 3):
            from os import path
            for i in range(AuxiliaryTestMethods.get_random() % 11):
                filename = AuxiliaryTestMethods.get_random_str()
                text = AuxiliaryTestMethods.get_random_str()
                file_path = path.join(current_path, filename)
                test_class.assertFalse(path.exists(file_path))
                functions.write_file(file_path, text)
                test_class.assertTrue(path.exists(file_path))
            new_path = path.join(current_path, AuxiliaryTestMethods.get_random_str())
            test_class.assertFalse(path.exists(new_path))
            functions.makedirs(new_path)
            test_class.assertTrue(path.exists(new_path))
            if depth > 1:
                create_temp_dir_populated_aux(test_class, new_path, depth - 1)
        from tempfile import mkdtemp
        temp_folder_path = mkdtemp()
        create_temp_dir_populated_aux(test_class, temp_folder_path)
        return temp_folder_path

    def get_st_mode(path):
        from os import stat
        return stat(path).st_mode & 0o7777

    def check_mode_recursive(comparison_method, absolute_path, expected_mode, check_root):
        from os import walk, path
        for root, dirs, files in walk(absolute_path):
            if check_root:
                comparison_method(AuxiliaryTestMethods.get_st_mode(root), expected_mode)
            for d in dirs:
                test_path = path.join(root, d)
                comparison_method(AuxiliaryTestMethods.get_st_mode(test_path), expected_mode)
            for f in files:
                test_path = path.join(root, f)
                comparison_method(AuxiliaryTestMethods.get_st_mode(test_path), expected_mode)

    def listdir_recursive(absolute_path):
        from os import walk, path
        content_array = []
        chars_to_remove = len(absolute_path) + 1
        for root, dirs, files in walk(absolute_path):
            for d in dirs:
                relative_path = path.join(root, d)[chars_to_remove:]
                content_array.append(relative_path)
            for f in files:
                relative_path = path.join(root, f)[chars_to_remove:]
                content_array.append(relative_path)
        return content_array

if __name__ == '__main__':
    from ui import verify_python_version
    verify_python_version()
    unittest.main()

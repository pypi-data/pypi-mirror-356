import unittest
from dikshant_password_tool import password_generator

class TestPasswordGenerator(unittest.TestCase):
    def test_default_password(self):
        password = password_generator()
        self.assertEqual(len(password), 12)
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))
    
    def test_custom_length(self):
        for length in [8, 12, 16]:
            password = password_generator(length=length)
            self.assertEqual(len(password), length)
    
    def test_character_options(self):
        # Test lowercase only
        password = password_generator(include_uppercase=False, include_digits=False, include_special=False)
        self.assertTrue(password.islower())
        
        # Test digits only
        password = password_generator(length=10, include_uppercase=False, include_digits=True, include_special=False)
        self.assertTrue(password.isdigit())
    
    def test_invalid_length(self):
        with self.assertRaises(ValueError):
            password_generator(length=0)
    
    def test_no_character_sets(self):
        with self.assertRaises(ValueError):
            password_generator(include_uppercase=False, include_digits=False, include_special=False, length=10)

if __name__ == '__main__':
    unittest.main()
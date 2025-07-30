import unittest
import string
from dikshantlock import generate

class TestPasswordGenerator(unittest.TestCase):
    def test_default_password(self):
        """Test default password includes all character types"""
        password = generate()
        self.assertEqual(len(password), 12)
        self.assertTrue(any(c.islower() for c in password))
        self.assertTrue(any(c.isupper() for c in password))
        self.assertTrue(any(c.isdigit() for c in password))
        self.assertTrue(any(c in string.punctuation for c in password))

    def test_custom_length(self):
        """Test various valid lengths"""
        for length in [8, 12, 16, 24, 64]:
            password = generate(length=length)
            self.assertEqual(len(password), length)

    def test_character_options(self):
        """Test different character set combinations"""
        # Lowercase only
        password = generate(uppercase=False, digits=False, special=False)
        self.assertTrue(password.islower())
        
        # Uppercase and digits only
        password = generate(lowercase=False, special=False)
        self.assertTrue(all(c.isupper() or c.isdigit() for c in password))
        
        # Special chars only
        password = generate(length=8, lowercase=False, uppercase=False, digits=False)
        self.assertTrue(all(c in string.punctuation for c in password))

    def test_invalid_length(self):
        """Test length validation"""
        with self.assertRaises(ValueError):
            generate(length=7)  # Too short
        with self.assertRaises(ValueError):
            generate(length=65)  # Too long

    def test_invalid_character_sets(self):
        """Test no character sets enabled"""
        with self.assertRaises(ValueError):
            generate(lowercase=False, uppercase=False, digits=False, special=False)

    def test_password_uniqueness(self):
        """Test generated passwords are unique"""
        passwords = {generate() for _ in range(100)}
        self.assertEqual(len(passwords), 100)

if __name__ == '__main__':
    unittest.main()
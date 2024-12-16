# tests/test_geoloader.py

import unittest
import sys
import os
import json
from pathlib import Path

# Add the parent directory to the path so we can import GeoLoader
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from GeoLoader import GeoLoader

class TestGeoLoader(unittest.TestCase):
    def setUp(self):
        """Set up test fixtures before each test method"""
        self.loader = GeoLoader()
        
    def test_config_exists(self):
        """Test that config.json exists and is valid"""
        self.assertTrue(os.path.exists('config.json'))
        with open('config.json', 'r') as f:
            config = json.load(f)
        self.assertIn('game_path', config)
        self.assertIn('mods_path', config)

    def test_paths_exist(self):
        """Test that required directories exist"""
        self.assertTrue(os.path.exists('mods'))
        self.assertTrue(os.path.exists('src'))
        
    def test_mod_structure(self):
        """Test that mods directory has the correct structure"""
        mods_path = Path('mods')
        # Check if at least one mod exists
        self.assertTrue(any(mods_path.iterdir()))
        
    def test_version_format(self):
        """Test version string format"""
        version = self.loader.version
        self.assertRegex(version, r'^\d+\.\d+\.\d+$')

    def test_get_mod_info(self):
        """Test mod info retrieval"""
        # Create a test mod structure
        test_mod_path = Path('mods/test_mod')
        test_mod_path.mkdir(parents=True, exist_ok=True)
        
        mod_info = {
            "name": "Test Mod",
            "version": "1.0.0",
            "author": "Test Author",
            "description": "Test Description"
        }
        
        with open(test_mod_path / 'mod.json', 'w') as f:
            json.dump(mod_info, f)
            
        # Test the mod info retrieval
        retrieved_info = self.loader.get_mod_info(str(test_mod_path))
        self.assertEqual(retrieved_info['name'], mod_info['name'])
        self.assertEqual(retrieved_info['version'], mod_info['version'])
        
    def tearDown(self):
        """Clean up after tests"""
        # Remove test mod if it exists
        test_mod_path = Path('mods/test_mod')
        if test_mod_path.exists():
            for file in test_mod_path.iterdir():
                file.unlink()
            test_mod_path.rmdir()

if __name__ == '__main__':
    unittest.main()

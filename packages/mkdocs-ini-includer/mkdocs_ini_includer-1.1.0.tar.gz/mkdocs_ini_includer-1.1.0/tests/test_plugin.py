import os
import tempfile
import unittest
from unittest.mock import Mock, patch
from mkdocs_ini_includer.plugin import IniIncluderPlugin


class TestIniIncluderPlugin(unittest.TestCase):
    def setUp(self):
        self.plugin = IniIncluderPlugin()
        self.plugin.config = {
            'base_path': '',
            'config_file': ''
        }
        self.mock_config = {
            'docs_dir': '/test/docs'
        }

    def test_parse_include_args_empty(self):
        result = self.plugin._parse_include_args('')
        self.assertEqual(result, {})

    def test_parse_include_args_file_only(self):
        result = self.plugin._parse_include_args('file="config.ini"')
        self.assertEqual(result, {'file': 'config.ini'})

    def test_parse_include_args_section_only(self):
        result = self.plugin._parse_include_args('section="database"')
        self.assertEqual(result, {'section': 'database'})

    def test_parse_include_args_both_params(self):
        result = self.plugin._parse_include_args('file="config.ini" section="api"')
        self.assertEqual(result, {'file': 'config.ini', 'section': 'api'})

    def test_parse_include_args_single_quotes(self):
        result = self.plugin._parse_include_args("file='config.ini' section='database'")
        self.assertEqual(result, {'file': 'config.ini', 'section': 'database'})

    def test_get_full_path_absolute(self):
        result = self.plugin._get_full_path('/absolute/path/config.ini', self.mock_config)
        self.assertEqual(result, '/absolute/path/config.ini')

    def test_get_full_path_relative_no_base_path(self):
        result = self.plugin._get_full_path('config.ini', self.mock_config)
        self.assertEqual(result, '/test/docs/config.ini')

    def test_get_full_path_with_base_path(self):
        self.plugin.config['base_path'] = 'configs'
        result = self.plugin._get_full_path('config.ini', self.mock_config)
        self.assertEqual(result, '/test/docs/configs/config.ini')

    def test_get_full_path_with_absolute_base_path(self):
        self.plugin.config['base_path'] = '/absolute/configs'
        result = self.plugin._get_full_path('config.ini', self.mock_config)
        self.assertEqual(result, '/absolute/configs/config.ini')

    def test_filter_section_simple(self):
        ini_content = """[database]
host = localhost
port = 5432

[api]
endpoint = /api/v1
timeout = 30"""
        
        result = self.plugin._filter_section(ini_content, 'database')
        expected = """[database]
host = localhost
port = 5432"""
        self.assertEqual(result, expected)

    def test_filter_section_with_subsections(self):
        ini_content = """[database]
host = localhost

[database.ssl]
enabled = true
cert_path = /path/to/cert

[api]
endpoint = /api/v1"""
        
        result = self.plugin._filter_section(ini_content, 'database')
        expected = """[database]
host = localhost

[database.ssl]
enabled = true
cert_path = /path/to/cert"""
        self.assertEqual(result, expected)

    def test_filter_section_nonexistent(self):
        ini_content = """[database]
host = localhost

[api]
endpoint = /api/v1"""
        
        result = self.plugin._filter_section(ini_content, 'nonexistent')
        self.assertEqual(result, '')

    def test_on_page_markdown_no_file_raises_error(self):
        markdown = "{% ini-include %}"
        with self.assertRaises(ValueError) as context:
            self.plugin.on_page_markdown(markdown, None, self.mock_config, None)
        self.assertIn("No file specified", str(context.exception))

    def test_on_page_markdown_file_not_found_raises_error(self):
        markdown = '{% ini-include file="nonexistent.ini" %}'
        with self.assertRaises(FileNotFoundError) as context:
            self.plugin.on_page_markdown(markdown, None, self.mock_config, None)
        self.assertIn("not found", str(context.exception))

    def test_on_page_markdown_success(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as tmp:
            tmp.write("""[database]
host = localhost
port = 5432""")
            tmp.flush()
            
            try:
                markdown = f'{{% ini-include file="{tmp.name}" %}}'
                result = self.plugin.on_page_markdown(markdown, None, self.mock_config, None)
                
                expected = """```ini
[database]
host = localhost
port = 5432
```"""
                self.assertEqual(result, expected)
            finally:
                os.unlink(tmp.name)

    def test_on_page_markdown_with_section(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as tmp:
            tmp.write("""[database]
host = localhost
port = 5432

[api]
endpoint = /api/v1""")
            tmp.flush()
            
            try:
                markdown = f'{{% ini-include file="{tmp.name}" section="database" %}}'
                result = self.plugin.on_page_markdown(markdown, None, self.mock_config, None)
                
                expected = """```ini
[database]
host = localhost
port = 5432
```"""
                self.assertEqual(result, expected)
            finally:
                os.unlink(tmp.name)

    def test_on_page_markdown_with_default_config_file(self):
        self.plugin.config['config_file'] = 'default.ini'
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as tmp:
            tmp.write("""[app]
name = test""")
            tmp.flush()
            
            try:
                with patch.object(self.plugin, '_get_full_path', return_value=tmp.name):
                    markdown = "{% ini-include %}"
                    result = self.plugin.on_page_markdown(markdown, None, self.mock_config, None)
                    
                    expected = """```ini
[app]
name = test
```"""
                    self.assertEqual(result, expected)
            finally:
                os.unlink(tmp.name)

    def test_on_page_markdown_read_error_raises_exception(self):
        with tempfile.NamedTemporaryFile(mode='w', suffix='.ini', delete=False) as tmp:
            tmp.write("test content")
            tmp.flush()
            
            try:
                os.chmod(tmp.name, 0o000)  # Remove read permissions
                
                markdown = f'{{% ini-include file="{tmp.name}" %}}'
                with self.assertRaises(RuntimeError) as context:
                    self.plugin.on_page_markdown(markdown, None, self.mock_config, None)
                self.assertIn("Error reading", str(context.exception))
            finally:
                os.chmod(tmp.name, 0o644)  # Restore permissions
                os.unlink(tmp.name)


if __name__ == '__main__':
    unittest.main()
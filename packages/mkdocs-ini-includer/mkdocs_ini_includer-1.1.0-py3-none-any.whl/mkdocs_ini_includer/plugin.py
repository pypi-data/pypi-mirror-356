import os
import re
import configparser
from io import StringIO
from mkdocs.plugins import BasePlugin
from mkdocs.config import config_options


class IniIncluderPlugin(BasePlugin):
    config_scheme = (
        ('base_path', config_options.Type(str, default='')),
        ('config_file', config_options.Type(str, default='')),
    )
    
    def __init__(self):
        super().__init__()
        self.ini_files = set()

    def on_page_markdown(self, markdown, page, config, files):
        def replace_ini_include(match):
            args = self._parse_include_args(match.group(1))
            ini_path = args.get('file') or self.config.get('config_file', '')
            section = args.get('section')
            
            if not ini_path:
                raise ValueError("No file specified and no default config_file configured")
            
            full_path = self._get_full_path(ini_path, config)
            
            if not os.path.exists(full_path):
                raise FileNotFoundError(f"File {ini_path} not found at {full_path}")
            
            # Track this INI file for dependency watching
            self.ini_files.add(full_path)
            
            try:
                ini_content = self._read_ini_with_comments(full_path)
                
                if section:
                    filtered_content = self._filter_section(ini_content, section)
                    return f"```ini\n{filtered_content}\n```"
                else:
                    return f"```ini\n{ini_content}\n```"
                    
            except Exception as e:
                raise RuntimeError(f"Error reading {ini_path}: {str(e)}") from e
        
        pattern = r'\{%\s*ini-include\s+(.*?)\s*%\}'
        return re.sub(pattern, replace_ini_include, markdown, flags=re.IGNORECASE | re.DOTALL)
    
    def on_serve(self, server, config, builder):
        # Add INI files to the file watcher so changes trigger rebuilds
        for ini_file in self.ini_files:
            if os.path.exists(ini_file):
                server.watch(ini_file)

    def _parse_include_args(self, args_string):
        args = {}
        if not args_string.strip():
            return args
            
        parts = [part.strip() for part in args_string.split()]
        
        for part in parts:
            if '=' in part:
                key, value = part.split('=', 1)
                args[key.strip()] = value.strip().strip('"\'')
        
        return args

    def _get_full_path(self, ini_path, config):
        if os.path.isabs(ini_path):
            return ini_path
        
        base_path = self.config.get('base_path', '')
        if base_path:
            if not os.path.isabs(base_path):
                base_path = os.path.join(config['docs_dir'], base_path)
            return os.path.join(base_path, ini_path)
        else:
            return os.path.join(config['docs_dir'], ini_path)

    def _read_ini_with_comments(self, file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()

    def _filter_section(self, ini_content, section_name):
        lines = ini_content.split('\n')
        result_lines = []
        in_target_section = False
        current_section = None
        
        for line in lines:
            stripped = line.strip()
            
            if stripped.startswith('[') and stripped.endswith(']'):
                current_section = stripped[1:-1]
                if current_section == section_name or current_section.startswith(f"{section_name}."):
                    in_target_section = True
                    result_lines.append(line)
                else:
                    in_target_section = False
            elif in_target_section:
                result_lines.append(line)
            elif not stripped and in_target_section:
                result_lines.append(line)
        
        return '\n'.join(result_lines).strip()
# MkDocs INI Includer

This is a MkDocs plugin that allows a MkDocs site to include all or part of an INI file inside the docs at build time.

## Why?
- Documenting the configuration system of an app without having to copy/paste config sections
- Showing the configuration for a specific feature

## Features
- ✅ Include whole INI files
- ✅ Include specific sections (e.g., `[section.name]` and all sub-data)
- ✅ Preserve comments (useful docs for users)
- ✅ Support array keys like `key1[] = abc, key1[] = def`
- ✅ Simple embedding without complex parsing

## Installation

```bash
pip install mkdocs-ini-includer
```

## Configuration

Add the plugin to your `mkdocs.yml`:

```yaml
plugins:
  - ini-includer:
      base_path: "path/to/your/ini/files"  # Optional: base path for INI files
      config_file: "app.ini"              # Optional: default INI file
```

## Usage

### Include Entire INI File

```markdown
{% ini-include %}
```

Or specify a specific file:

```markdown
{% ini-include file="config/app.ini" %}
```

### Include Specific Section

```markdown
{% ini-include section="database" %}
```

### Examples

Given an INI file `config/app.ini`:

```ini
# Application configuration
[app]
name = MyApp
version = 1.0.0

# Database settings
[database]
host = localhost
port = 5432
# Connection pool settings
pool_size = 10

[database.ssl]
enabled = true
cert_path = /path/to/cert
```

**Include entire file:**
```markdown
{% ini-include %}
```

**Include only database section:**
```markdown
{% ini-include section="database" %}
```

This will include the `[database]` section and all its subsections like `[database.ssl]`.

## Development & Live Reload

The plugin supports live reload during development. When using `mkdocs serve`, changes to INI files are automatically detected and trigger page rebuilds, allowing you to see updates immediately without restarting the development server.

## Notes
- File paths are relative to your `docs_dir` unless `base_path` is configured
- Comments and formatting are preserved
- Array keys (like `key[]=value`) are supported
- Error handling displays helpful messages in the generated docs
- Live reload works with `mkdocs serve` for real-time INI file updates


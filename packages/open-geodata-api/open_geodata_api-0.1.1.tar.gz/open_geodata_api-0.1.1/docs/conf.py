# docs/conf.py
import os

# Check if we're building on Read the Docs
on_rtd = os.environ.get('READTHEDOCS') == 'True'

if on_rtd:
    # RTD-specific configuration
    html_theme = 'sphinx_rtd_theme'
    html_context = {
        'display_github': True,
        'github_user': 'yourusername',
        'github_repo': 'open-geodata-api',
        'github_version': 'main',
        'conf_py_path': '/docs/',
    }
else:
    # Local development configuration
    html_theme = 'sphinx_rtd_theme'

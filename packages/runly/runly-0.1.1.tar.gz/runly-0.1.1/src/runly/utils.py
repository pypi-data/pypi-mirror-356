"""
Utility functions for RunLy.
"""

import os
import re
from typing import Dict


def expand_variables(text: str, variables: Dict[str, str]) -> str:
    """
    Expand variables in text using the provided variables dictionary.
    
    Supports:
    - {{VAR}} syntax (Just/RunLy format)
    - ${VAR} or $VAR syntax
    - Environment variables using ${env:NAME} syntax
    """
    # Process {{var}} syntax first (Just/RunLy format)
    just_pattern = re.compile(r'{{([^}]+)}}')
    
    def replace_just_var(match):
        var_name = match.group(1).strip()
        return variables.get(var_name, '')
    
    result = just_pattern.sub(replace_just_var, text)
    
    # Process ${var} syntax
    var_pattern = re.compile(r'\${([^}]+)}')
    
    def replace_var(match):
        var_name = match.group(1).strip()
        
        # Check for environment variable syntax
        if var_name.startswith('env:'):
            env_name = var_name[4:].strip()
            return os.environ.get(env_name, '')
        
        # Check in variables dictionary
        return variables.get(var_name, '')
    
    result = var_pattern.sub(replace_var, result)
    
    # Process $var syntax (be careful not to replace things like $1, $2 in shell scripts)
    var_pattern = re.compile(r'(?<!\$)\$([A-Za-z0-9_-]+)')
    result = var_pattern.sub(lambda m: variables.get(m.group(1), ''), result)
    
    return result
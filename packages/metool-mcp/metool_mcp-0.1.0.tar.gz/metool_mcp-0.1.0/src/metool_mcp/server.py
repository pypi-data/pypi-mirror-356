"""FastMCP server for metool."""

import asyncio
import os
import subprocess
from pathlib import Path
from typing import Optional, Dict, List

from fastmcp import FastMCP

mcp = FastMCP("metool-mcp")


@mcp.tool()
async def add_repo_entry(
    directory: str,
    repo: str,
    target_name: Optional[str] = None,
    file_name: str = ".repos.txt"
) -> Dict[str, any]:
    """
    Add a repository entry to repos.txt file.
    
    Args:
        directory: Directory containing the repos.txt file
        repo: Repository specification (e.g., "mbailey/conventions")
        target_name: Optional target directory name (defaults to repo basename)
        file_name: Name of the repos file (default: ".repos.txt")
    
    Returns:
        Dict with status and message
    """
    try:
        repo_file = Path(directory) / file_name
        
        # Ensure directory exists
        repo_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Build the entry line
        if target_name:
            entry = f"{repo} {target_name}"
        else:
            entry = repo
            
        # Check if entry already exists
        if repo_file.exists():
            content = repo_file.read_text()
            if entry in content or repo in content:
                return {
                    "status": "exists",
                    "message": f"Repository {repo} already exists in {file_name}"
                }
        
        # Append the entry
        with open(repo_file, 'a') as f:
            if repo_file.exists() and repo_file.stat().st_size > 0:
                f.write('\n')
            f.write(entry + '\n')
            
        return {
            "status": "added",
            "message": f"Added {entry} to {repo_file}"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to add repo entry: {str(e)}"
        }


@mcp.tool()
async def sync_directory(directory: str) -> Dict[str, any]:
    """
    Run mt sync on a directory to synchronize repositories.
    
    Args:
        directory: Directory to sync
        
    Returns:
        Dict with status, stdout, stderr, and return code
    """
    try:
        # Find metool installation
        # First check if MT_ROOT is set
        mt_root = os.environ.get('MT_ROOT')
        
        if not mt_root:
            # Try to find metool relative to this script
            # Go up from mcp/src/metool_mcp to find the root
            current_file = Path(__file__).resolve()
            potential_root = current_file.parent.parent.parent.parent
            if (potential_root / 'shell' / 'mt').exists():
                mt_root = str(potential_root)
            else:
                # Try common locations
                for location in [
                    Path.home() / 'metool',
                    Path.home() / '.metool',
                    Path('/usr/local/metool'),
                    Path('/opt/metool')
                ]:
                    if (location / 'shell' / 'mt').exists():
                        mt_root = str(location)
                        break
        
        if not mt_root:
            return {
                "status": "error",
                "message": "Cannot find metool installation. Set MT_ROOT environment variable."
            }
        
        # Create bash command that sources mt and runs sync
        bash_cmd = f'source "{mt_root}/shell/mt" && mt sync "{directory}"'
        
        # Run the command in bash
        result = await asyncio.create_subprocess_exec(
            'bash', '-c', bash_cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            cwd=directory,
            env={**os.environ, 'MT_ROOT': mt_root}
        )
        
        stdout, stderr = await result.communicate()
        
        return {
            "status": "completed" if result.returncode == 0 else "failed",
            "returncode": result.returncode,
            "stdout": stdout.decode('utf-8'),
            "stderr": stderr.decode('utf-8')
        }
        
    except Exception as e:
        return {
            "status": "error", 
            "message": f"Failed to sync directory: {str(e)}"
        }


@mcp.tool()
async def list_repos(directory: str, file_name: str = ".repos.txt") -> Dict[str, any]:
    """
    List repositories from a repos.txt file.
    
    Args:
        directory: Directory containing the repos.txt file
        file_name: Name of the repos file (default: ".repos.txt")
        
    Returns:
        Dict with repos list or error message
    """
    try:
        repo_file = Path(directory) / file_name
        
        if not repo_file.exists():
            return {
                "status": "not_found",
                "message": f"No {file_name} found in {directory}",
                "repos": []
            }
            
        content = repo_file.read_text()
        repos = []
        
        for line in content.splitlines():
            line = line.strip()
            # Skip empty lines and comments
            if line and not line.startswith('#'):
                repos.append(line)
                
        return {
            "status": "success",
            "file": str(repo_file),
            "repos": repos
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": f"Failed to list repos: {str(e)}"
        }


@mcp.prompt()
async def conventions_add(repo: str = "mbailey/conventions", target: str = ".conventions") -> str:
    """Guide for adding conventions repository to a project."""
    return f"""To add the conventions repository '{repo}' to your project:

1. First, I'll check if .repos.txt exists in your project root
2. Then add the entry: "{repo} {target}"
3. Finally, run mt sync to clone/update and create the symlink

The slash command syntax is:
- `/metool:conventions-add {repo}` - Uses target name '{target}'
- `/metool:conventions-add owner/repo target-name` - Custom target

Steps I'll perform:
1. Call add_repo_entry(directory=".", repo="{repo}", target_name="{target}")
2. Call sync_directory(directory=".")

This will clone {repo} to the canonical location and create a symlink at {target}
"""


@mcp.prompt()
async def manage_repos() -> str:
    """Guide for managing repository manifest files."""
    return """Repository manifest files (.repos.txt or repos.txt) declare git repositories for your project.

Format:
```
# Comments start with #
repo-owner/repo-name                          # Default target name
repo-owner/repo-name custom-name              # Custom target directory
github.com_account:owner/repo target-name     # With SSH host identity
_account:owner/repo target                    # GitHub shorthand
repo@branch target                            # Specific branch/tag
```

Common operations:
1. Add a repository: Use add_repo_entry tool
2. Sync repositories: Use sync_directory tool  
3. List current repos: Use list_repos tool

The mt sync command will:
- Clone missing repositories
- Update existing repositories
- Create/update symlinks for shared repos
- Handle multi-account SSH configurations
"""


@mcp.resource("repos-file://{directory}")
async def get_repos_file(directory: str) -> str:
    """
    Get contents of a repos.txt file from a directory.
    
    Args:
        directory: Directory containing the repos.txt file
    """
    repo_file = Path(directory) / ".repos.txt"
    
    if not repo_file.exists():
        # Try repos.txt without dot
        repo_file = Path(directory) / "repos.txt"
        
    if not repo_file.exists():
        return f"# No repos.txt or .repos.txt found in {directory}\n"
        
    return repo_file.read_text()


def main():
    """Run the MCP server."""
    import sys
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
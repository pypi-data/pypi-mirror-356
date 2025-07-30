#!/usr/bin/env python3
"""
Flatten CLI Tool

A command-line tool to recursively flatten directory structures 
by copying all files to a single output directory.
"""

import os
import shutil
import argparse
import sys
import json
from pathlib import Path
from collections import defaultdict


DEFAULT_CONFIG = {
    "exclude_patterns": [
        ".git", "__pycache__", ".venv", "venv", "node_modules", ".DS_Store",
        ".pytest_cache", ".mypy_cache", "dist", "build", ".tox", ".idea",
        ".vscode", "*.pyc", "*.pyo", "*.egg-info", ".coverage", ".nyc_output",
        "coverage", ".next", ".nuxt", "target", "*.class", "*.jar"
    ],
    "code_extensions": [
        ".py", ".js", ".ts", ".jsx", ".tsx", ".vue", ".go", ".rs", ".java",
        ".cpp", ".c", ".h", ".cs", ".php", ".rb", ".swift", ".kt", ".scala",
        ".sh", ".bat", ".ps1", ".sql", ".html", ".css", ".scss", ".less",
        ".json", ".yaml", ".yml", ".toml", ".xml", ".md", ".txt", ".cfg",
        ".ini", ".env", ".dockerfile", ".gitignore", ".gitattributes", ".editorconfig"
    ],
    "preserve_structure": False,
    "quiet": False
}


def get_config_path():
    """Get the path to the config file."""
    if os.name == 'nt':  # Windows
        config_dir = Path(os.environ.get('APPDATA', Path.home() / 'AppData' / 'Roaming')) / 'flatten-cli'
    else:  # Unix-like (Linux, macOS)
        config_dir = Path(os.environ.get('XDG_CONFIG_HOME', Path.home() / '.config')) / 'flatten-cli'
    
    config_dir.mkdir(parents=True, exist_ok=True)
    return config_dir / 'config.json'


def load_config():
    """Load configuration from file or return defaults."""
    config_path = get_config_path()
    
    if config_path.exists():
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                user_config = json.load(f)
                # Merge with defaults, allowing user to override
                config = DEFAULT_CONFIG.copy()
                config.update(user_config)
                return config
        except (json.JSONDecodeError, IOError) as e:
            print(f"⚠️  Warning: Could not load config file: {e}")
            print("Using default configuration.")
    
    return DEFAULT_CONFIG.copy()


def save_config(config):
    """Save configuration to file."""
    config_path = get_config_path()
    
    try:
        with open(config_path, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)
        return True
    except IOError as e:
        print(f"Error saving config: {e}")
        return False


def show_config():
    """Display current configuration."""
    config = load_config()
    config_path = get_config_path()
    
    print(f"Config file: {config_path}")
    print("Current configuration:")
    print("-" * 50)
    
    print("Exclude patterns:")
    for pattern in config['exclude_patterns']:
        print(f"   • {pattern}")
    
    print(f"\nCode extensions ({len(config['code_extensions'])}):")
    # Group extensions for better display
    exts = config['code_extensions']
    for i in range(0, len(exts), 8):
        group = exts[i:i+8]
        print(f"   {' '.join(group)}")
    
    print(f"\n  Default settings:")
    print(f"   • Preserve structure: {config['preserve_structure']}")
    print(f"   • Quiet mode: {config['quiet']}")


def manage_config(action, category=None, items=None):
    """Manage configuration settings."""
    config = load_config()
    
    if action == "show":
        show_config()
        return True
    
    if action == "reset":
        if save_config(DEFAULT_CONFIG):
            print("Configuration reset to defaults")
            return True
        return False
    
    if not category or not items:
        print("Error: Category and items required for add/remove actions")
        return False
    
    if category not in ['exclude', 'extensions']:
        print(f"Error: Unknown category '{category}'. Use 'exclude' or 'extensions'")
        return False
    
    config_key = 'exclude_patterns' if category == 'exclude' else 'code_extensions'
    
    if action == "add":
        for item in items:
            if item not in config[config_key]:
                config[config_key].append(item)
                print(f"Added '{item}' to {category}")
            else:
                print(f"⚠️  '{item}' already in {category}")
    
    elif action == "remove":
        for item in items:
            if item in config[config_key]:
                config[config_key].remove(item)
                print(f"Removed '{item}' from {category}")
            else:
                print(f"⚠️  '{item}' not found in {category}")
    
    elif action == "set":
        if category == "preserve_structure":
            config["preserve_structure"] = items[0].lower() in ['true', '1', 'yes', 'on']
            print(f"Set preserve_structure to {config['preserve_structure']}")
        elif category == "quiet":
            config["quiet"] = items[0].lower() in ['true', '1', 'yes', 'on']
            print(f"Set quiet to {config['quiet']}")
        else:
            print(f"Error: Cannot set '{category}'. Use 'preserve_structure' or 'quiet'")
            return False
    
    return save_config(config)


def flatten_directory(source_dir, output_dir, preserve_structure=None, file_extensions=None, exclude_patterns=None, quiet=None):
    """
    Flatten a directory by copying all files to a single output directory.
    
    Args:
        source_dir (str): Path to the source directory to flatten
        output_dir (str): Path to the output directory
        preserve_structure (bool): If True, preserve some path info in filename
        file_extensions (list): List of file extensions to include (e.g., ['.py', '.js'])
        exclude_patterns (list): List of patterns to exclude (e.g., ['__pycache__', '.git'])
        quiet (bool): If True, suppress non-essential output
    """
    # Load config defaults
    config = load_config()
    
    # Use provided values or fall back to config defaults
    if preserve_structure is None:
        preserve_structure = config.get('preserve_structure', False)
    if quiet is None:
        quiet = config.get('quiet', False)
    if exclude_patterns is None:
        exclude_patterns = config.get('exclude_patterns', DEFAULT_CONFIG['exclude_patterns'])
    
    source_path = Path(source_dir).resolve()
    output_path = Path(output_dir).resolve()
    
    # Create output directory if it doesn't exist
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Track filename conflicts
    filename_counts = defaultdict(int)
    copied_files = []
    skipped_files = []
    
    if not quiet:
        print(f"Flattening: {source_path}")
        print(f"Output: {output_path}")
        if exclude_patterns:
            print(f"Excluding: {', '.join(exclude_patterns[:5])}" + ("..." if len(exclude_patterns) > 5 else ""))
        if file_extensions:
            print(f"Including: {', '.join(file_extensions[:8])}" + ("..." if len(file_extensions) > 8 else ""))
        print("-" * 60)
    
    # Walk through all files recursively
    for root, dirs, files in os.walk(source_path):
        # Filter out excluded directories
        dirs[:] = [d for d in dirs if not any(pattern in d for pattern in exclude_patterns)]
        
        current_path = Path(root)
        
        # Skip if current directory matches exclude patterns
        if any(pattern in str(current_path) for pattern in exclude_patterns):
            continue
            
        for file in files:
            file_path = current_path / file
            
            # Skip if file matches exclude patterns
            if any(pattern in file for pattern in exclude_patterns):
                skipped_files.append(str(file_path))
                continue
            
            # Filter by file extensions if specified
            if file_extensions and not any(file.lower().endswith(ext.lower()) for ext in file_extensions):
                skipped_files.append(str(file_path))
                continue
            
            # Generate output filename
            if preserve_structure:
                # Include relative path in filename
                rel_path = file_path.relative_to(source_path)
                output_filename = str(rel_path).replace(os.sep, '__')
            else:
                output_filename = file
            
            # Handle filename conflicts
            base_name, extension = os.path.splitext(output_filename)
            if filename_counts[output_filename] > 0:
                output_filename = f"{base_name}__{filename_counts[output_filename]}{extension}"
            
            filename_counts[output_filename] += 1
            
            # Copy the file
            output_file_path = output_path / output_filename
            
            try:
                shutil.copy2(file_path, output_file_path)
                copied_files.append((str(file_path), str(output_file_path)))
                if not quiet:
                    rel_source = file_path.relative_to(source_path)
                    print(f"{rel_source} → {output_filename}")
            except Exception as e:
                if not quiet:
                    print(f"Error copying {file_path}: {e}")
                skipped_files.append(str(file_path))
    
    # Print summary
    if not quiet:
        print("-" * 60)
        print(f"Complete! Copied {len(copied_files)} files, skipped {len(skipped_files)}")
        
        if skipped_files and len(skipped_files) <= 5:
            print("\nSkipped files:")
            for skipped in skipped_files[:5]:
                rel_path = Path(skipped).relative_to(source_path) if source_path in Path(skipped).parents else Path(skipped)
                print(f"   • {rel_path}")
        elif len(skipped_files) > 5:
            print(f"\nSkipped {len(skipped_files)} files (use --verbose to see all)")
    
    return copied_files, skipped_files


def main():
    # Check if this is a config command first
    if len(sys.argv) > 1 and sys.argv[1] == 'config':
        # Handle config subcommand separately
        parser = argparse.ArgumentParser(description="Configuration management")
        parser.add_argument('command', choices=['config'])
        parser.add_argument('action', choices=['show', 'add', 'remove', 'set', 'reset'],
                           help='Configuration action')
        parser.add_argument('category', nargs='?',
                           help='Category: exclude, extensions, preserve_structure, quiet')
        parser.add_argument('items', nargs='*',
                           help='Items to add/remove or value to set')
        
        args = parser.parse_args()
        return 0 if manage_config(args.action, args.category, args.items) else 1
    
    # Main flatten command parser
    parser = argparse.ArgumentParser(
        description="Flatten directory structures - copy all files to a single directory",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  flatten ./src ./output                    # Basic flattening
  flatten . ./output                        # Flatten current directory
  flatten ./repo ./flat --code             # Code files only
  flatten . ./context --code --preserve    # Current dir, code files, preserve structure
  flatten ./docs ./out -e .md .txt         # Specific extensions
  flatten ./proj ./dest --preserve         # Keep directory info in filenames
  flatten ./app ./build -x test __pycache__ # Exclude patterns

Configuration:
  flatten config show                       # Show current config
  flatten config add exclude .log .tmp     # Add exclude patterns
  flatten config add extensions .vue .svelte # Add code extensions
  flatten config remove exclude node_modules # Remove exclude pattern
  flatten config set preserve_structure true # Set default behavior
  flatten config reset                      # Reset to defaults
        """
    )
    
    parser.add_argument(
        "source",
        help="Source directory to flatten (use '.' for current directory)"
    )
    
    parser.add_argument(
        "output",
        help="Output directory for flattened files"
    )
    
    parser.add_argument(
        "-p", "--preserve",
        action="store_true",
        help="Preserve directory structure in filenames (use __ as separator)"
    )
    
    parser.add_argument(
        "-e", "--ext", "--extensions",
        nargs="+",
        help="File extensions to include (e.g., .py .js .md)"
    )
    
    parser.add_argument(
        "-x", "--exclude",
        nargs="+",
        help="Additional patterns to exclude (adds to config defaults)"
    )
    
    parser.add_argument(
        "--exclude-only",
        nargs="+",
        help="Use only these exclude patterns (ignores config defaults)"
    )
    
    parser.add_argument(
        "--code",
        action="store_true",
        help="Use configured code file extensions"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Show all skipped files"
    )
    
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress output except errors"
    )
    
    args = parser.parse_args()
    
    # Handle current directory shortcuts
    source_path = Path(args.source).resolve()
    if args.source == '.':
        source_path = Path.cwd()
        source_display = str(source_path.name) + " (current directory)"
    else:
        source_display = str(source_path)
    
    if not source_path.exists():
        print(f"Error: Source directory '{args.source}' does not exist.", file=sys.stderr)
        return 1
    
    if not source_path.is_dir():
        print(f"Error: '{args.source}' is not a directory.", file=sys.stderr)
        return 1
    
    # Load config for defaults
    config = load_config()
    
    # Handle file extensions
    file_extensions = args.ext
    if args.code:
        file_extensions = config.get('code_extensions', DEFAULT_CONFIG['code_extensions'])
    
    # Handle exclude patterns
    if args.exclude_only:
        exclude_patterns = args.exclude_only
    else:
        exclude_patterns = config.get('exclude_patterns', DEFAULT_CONFIG['exclude_patterns']).copy()
        if args.exclude:
            exclude_patterns.extend(args.exclude)
    
    # Run the flattening
    try:
        copied_files, skipped_files = flatten_directory(
            str(source_path),
            args.output,
            preserve_structure=args.preserve or config.get('preserve_structure', False),
            file_extensions=file_extensions,
            exclude_patterns=exclude_patterns,
            quiet=args.quiet or config.get('quiet', False)
        )
        
        if args.verbose and skipped_files and not (args.quiet or config.get('quiet', False)):
            print("\nAll skipped files:")
            for skipped in skipped_files:
                rel_path = Path(skipped).relative_to(source_path) if source_path in Path(skipped).parents else Path(skipped)
                print(f"   • {rel_path}")
                
    except KeyboardInterrupt:
        print("\n⏹Operation cancelled by user.", file=sys.stderr)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

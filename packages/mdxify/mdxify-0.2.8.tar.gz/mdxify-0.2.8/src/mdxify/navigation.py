"""Navigation structure management."""

import json
from pathlib import Path
from typing import Any

from .discovery import should_include_module
from .generator import is_module_empty


def get_all_documented_modules(output_dir: Path) -> list[str]:
    """Get all modules that have documentation files."""
    modules = []
    for mdx_file in output_dir.glob("*.mdx"):
        # Skip non-module files (like index.mdx)
        if "-" not in mdx_file.stem:
            continue
        # Convert filename back to module name
        stem = mdx_file.stem
        # Handle __init__ files
        if stem.endswith("-__init__"):
            module_name = stem[:-9].replace("-", ".")  # Remove -__init__ suffix
        else:
            module_name = stem.replace("-", ".")
        modules.append(module_name)
    return sorted(modules)


def build_hierarchical_navigation(
    generated_modules: list[str], 
    output_dir: Path,
    docs_root: Path | None = None,
    skip_empty_parents: bool = True
) -> list[dict[str, Any]]:
    """Build a hierarchical navigation structure from flat module names.
    
    Args:
        generated_modules: List of module names
        output_dir: Directory where MDX files are written
        docs_root: Root directory for docs (to calculate relative paths). If None, paths are relative to output_dir
        skip_empty_parents: Whether to skip empty parent modules
    
    Returns a list of navigation entries where each entry is either:
    - A string (the path to the MDX file without extension)
    - A dict with "group" and "pages" keys for modules with submodules
    """
    # Calculate the path prefix for navigation entries
    if docs_root:
        # Get relative path from docs root to output dir
        try:
            nav_prefix = output_dir.relative_to(docs_root)
        except ValueError:
            # output_dir is not under docs_root, use as-is
            nav_prefix = Path()
    else:
        nav_prefix = Path()
    
    # Group modules by their hierarchy
    module_tree = {}
    
    # Find the common root package if all modules share one
    root_package = None
    if generated_modules:
        first_parts = generated_modules[0].split(".")
        if len(first_parts) >= 1:
            potential_root = first_parts[0]
            # Check if all modules start with this root
            if all(m.startswith(potential_root + ".") or m == potential_root for m in generated_modules):
                root_package = potential_root
    
    for module_name in sorted(generated_modules):
        parts = module_name.split(".")
        
        # Skip just the root package itself if present
        if root_package and module_name == root_package:
            continue
            
        # Skip the root package prefix for tree building
        if root_package and parts[0] == root_package:
            parts = parts[1:]
        
        # Build the tree with path info for ALL modules
        current = module_tree
        for i, part in enumerate(parts[:-1]):
            if part not in current:
                current[part] = {"_submodules": {}}
            elif "_submodules" not in current[part]:
                current[part]["_submodules"] = {}
            current = current[part]["_submodules"]
        
        # Add the leaf module
        if parts:
            leaf = parts[-1]
            if leaf not in current:
                current[leaf] = {}
            current[leaf]["_path"] = module_name
    
    def tree_to_nav(tree: dict, parent_parts: list[str] | None = None, is_top_level: bool = True) -> list[Any]:
        """Convert the tree structure to navigation format."""
        if parent_parts is None:
            parent_parts = []
            # If we have a root package, start with it
            if root_package:
                parent_parts = [root_package]
            
        result = []
        
        for name, info in sorted(tree.items()):
            current_parts = parent_parts + [name]
            submodules = info.get("_submodules", {})
            has_path = "_path" in info
            
            if submodules:
                # This has submodules - create a group
                # For top-level groups, use fully qualified name
                # For nested groups, use just the last part
                if is_top_level:
                    group_name = ".".join(current_parts)
                else:
                    group_name = name
                group_entry = {"group": group_name, "pages": []}
                
                # If this module itself exists (has a path), add it as __init__
                if has_path:
                    module_name = info["_path"]
                    filename = module_name.replace(".", "-") + "-__init__"
                    
                    if nav_prefix:
                        nav_path = str(nav_prefix / filename).replace("\\", "/")
                    else:
                        nav_path = filename
                        
                    module_file = output_dir / f"{filename}.mdx"
                    if module_file.exists():
                        if not skip_empty_parents or not is_module_empty(module_file):
                            group_entry["pages"].append(nav_path)
                
                # Add all submodules recursively (nested groups don't use full names)
                sub_pages = tree_to_nav(submodules, current_parts, is_top_level=False)
                group_entry["pages"].extend(sub_pages)
                
                # Only add the group if it has content
                if group_entry["pages"]:
                    result.append(group_entry)
            elif has_path:
                # This is a leaf module with no submodules
                module_name = info["_path"]
                filename = module_name.replace(".", "-")
                
                if nav_prefix:
                    nav_path = str(nav_prefix / filename).replace("\\", "/")
                else:
                    nav_path = filename
                result.append(nav_path)
        
        return result
    
    # Build the final navigation from the tree
    navigation = tree_to_nav(module_tree)
    
    # Sort the top-level entries for consistent output
    # Sort groups by name, and put non-groups (plain pages) first
    def sort_key(item):
        if isinstance(item, dict) and "group" in item:
            return (1, item["group"])  # Groups second, sorted by name
        else:
            return (0, str(item))  # Plain pages first, sorted by string value
    
    navigation.sort(key=sort_key)
    
    return navigation


def find_mdxify_placeholder(obj: Any, path: list[str] | None = None) -> tuple[Any, list[str]] | None:
    """Recursively find the $mdxify placeholder in a nested structure.
    
    Returns the parent container and path to the placeholder, or None if not found.
    """
    if path is None:
        path = []
        
    if isinstance(obj, dict):
        # Check if this dict is the placeholder
        if obj.get("$mdxify") == "generated":
            return obj, path
            
        # Recursively search all values
        for key, value in obj.items():
            result = find_mdxify_placeholder(value, path + [key])
            if result:
                return result
                
    elif isinstance(obj, list):
        # Search through list items
        for i, item in enumerate(obj):
            if isinstance(item, dict) and item.get("$mdxify") == "generated":
                # Found it - return the list and index
                return (obj, i), path
            result = find_mdxify_placeholder(item, path + [i])
            if result:
                return result
                
    return None


def update_docs_json(
    docs_json_path: Path, 
    generated_modules: list[str], 
    output_dir: Path,
    regenerate_all: bool = False
) -> None:
    """Update docs.json with generated module documentation.
    
    Looks for {"$mdxify": "generated"} placeholder and replaces it with
    the generated navigation structure.
    """
    with open(docs_json_path, "r") as f:
        docs_config = json.load(f)

    # Find the placeholder
    result = find_mdxify_placeholder(docs_config)
    
    if not result:
        print("""
Warning: Could not find mdxify placeholder in docs.json

To use automatic navigation updates, add a placeholder in your docs.json:

{
  "navigation": [
    {
      "group": "API Reference", 
      "pages": [
        {"$mdxify": "generated"}
      ]
    }
  ]
}

Alternatively, use --no-update-nav and manually add the generated files to your navigation.
""")
        return

    container_info, path = result
    
    # Try to determine docs root from docs.json location
    docs_root = docs_json_path.parent
    
    # Build navigation
    if regenerate_all:
        # Complete regeneration - use only the generated modules
        navigation_pages = build_hierarchical_navigation(generated_modules, output_dir, docs_root)
    else:
        # Merge mode - get all documented modules and build complete navigation
        all_modules = get_all_documented_modules(output_dir)
        # Filter to only include public modules
        public_modules = [m for m in all_modules if should_include_module(m)]
        navigation_pages = build_hierarchical_navigation(public_modules, output_dir, docs_root)

    # Replace the placeholder
    if isinstance(container_info, tuple):
        # It's in a list
        container, index = container_info
        # Replace the placeholder with the generated pages
        container[index:index+1] = navigation_pages
    else:
        # It's a direct dict reference - this shouldn't happen with current logic
        # but keeping for safety
        print("Warning: Unexpected placeholder location")
        return

    # Write back to docs.json
    with open(docs_json_path, "w") as f:
        json.dump(docs_config, f, indent=2)
        f.write("\n")  # Add trailing newline
        
    print(f"Updated {docs_json_path} - replaced placeholder with {len(navigation_pages)} entries")
import os
import sys
import shutil
import yaml

OLD_DIR_NAME = "hyperlisa"
NEW_DIR_NAME = ".hyperlisa"
OLD_CONFIG_NAMES = ["config.yaml", "combine_config.yaml"]


def convert_excludes(old_excludes):
    """
    Applies heuristics to convert old exclude patterns to the new format.
    - Patterns assumed to be directories will get a trailing '/'.
    - Patterns assumed to be files will be left as is.
    """
    new_excludes = []
    dir_like_patterns = [
        ".git",
        "__pycache__",
        ".vscode",
        "log",
        "scripts",
        "tests",
        "agents",
        "templates",
        "tools",
        "knowledgebase",
    ]

    for pattern in old_excludes:
        # Handle patterns like 'venv*'
        if pattern.endswith("*") and "." not in pattern:
            new_excludes.append(f"{pattern.rstrip('*')}*/")
            continue

        # Handle common directory names
        if pattern in dir_like_patterns:
            new_excludes.append(f"{pattern}/")
            continue

        # Handle file patterns (containing '.') or wildcard file patterns
        if "." in pattern:
            new_excludes.append(pattern)
            continue

        # Default assumption for unknown simple strings is a directory
        new_excludes.append(f"{pattern}/")

    return new_excludes


def main():
    """
    Main migration script to convert a v1 project setup to v2.
    """
    app_root = os.getcwd()
    old_dir_path = os.path.join(app_root, OLD_DIR_NAME)
    new_dir_path = os.path.join(app_root, NEW_DIR_NAME)

    print("Hyperlisa v2 Migration Tool")

    # 1. Check for old directory
    if not os.path.isdir(old_dir_path):
        print(f"Info: Old '{OLD_DIR_NAME}' directory not found. No migration needed or already migrated.")
        if os.path.isdir(new_dir_path):
            print(f"Found modern '{NEW_DIR_NAME}' directory. Exiting.")
        else:
            print("Run 'hyperlisa-configure' to start a new project.")
        sys.exit(0)

    # 2. Rename directory
    if os.path.exists(new_dir_path):
        print(f"Warning: New '{NEW_DIR_NAME}' directory already exists. Cannot rename automatically.")
    else:
        try:
            os.rename(old_dir_path, new_dir_path)
            print(f"✓ Renamed directory '{OLD_DIR_NAME}' to '{NEW_DIR_NAME}'")
        except OSError as e:
            print(f"Error: Could not rename directory. Please do it manually. Reason: {e}")
            sys.exit(1)

    # 3. Update .gitignore
    gitignore_path = os.path.join(app_root, ".gitignore")
    if os.path.isfile(gitignore_path):
        try:
            with open(gitignore_path, "r") as f:
                lines = f.readlines()

            new_lines = []
            updated = False
            for line in lines:
                stripped_line = line.strip()
                if stripped_line == OLD_DIR_NAME or stripped_line == f"{OLD_DIR_NAME}/":
                    if f"{NEW_DIR_NAME}/" not in [l.strip() for l in lines]:
                        new_lines.append(f"{NEW_DIR_NAME}/\n")
                    updated = True
                else:
                    new_lines.append(line)

            if updated:
                with open(gitignore_path, "w") as f:
                    f.writelines(new_lines)
                print("✓ Updated .gitignore")
        except Exception as e:
            print(f"Warning: Could not update .gitignore. Please check it manually. Reason: {e}")

    # 4. Convert config file
    old_config_path = None
    for name in OLD_CONFIG_NAMES:
        path = os.path.join(new_dir_path, name)
        if os.path.isfile(path):
            old_config_path = path
            break

    if not old_config_path:
        print(f"Warning: No old configuration file found in '{new_dir_path}'. Please create one manually.")
        sys.exit(0)

    try:
        with open(old_config_path, "r") as f:
            old_config = yaml.safe_load(f)

        # Build new config structure
        new_config = {
            "log_level": old_config.get("log_level", "INFO"),
            "variables": {"PYTHON_EXT": ["*.py"], "FRONTEND_EXT": ["*.css", "*.js", "*.html"]},
            "global_excludes": [
                "__pycache__/",
                ".vscode/",
                ".git/",
                ".hyperlisa/",
            ],
            "profiles": {
                "name_template": "$n_$p_$ts",
                "profiles_list": [
                    {
                        "name": "migrated_default",
                        "enable": True,
                        "blocks": [
                            {
                                "paths": [{"path": "/", "depth": "*"}],
                                "includes": old_config.get("includes", []),
                                "excludes": convert_excludes(old_config.get("excludes", [])),
                            }
                        ],
                    }
                ],
            },
        }

        # Backup old file and write new one
        backup_path = f"{old_config_path}.v1.bak"
        shutil.move(old_config_path, backup_path)
        print(f"✓ Backed up old config to: {os.path.basename(backup_path)}")

        new_config_path = os.path.join(new_dir_path, "config.yaml")
        with open(new_config_path, "w") as f:
            yaml.dump(new_config, f, sort_keys=False, indent=2, default_flow_style=False)
        print(f"✓ Successfully created new config at: {new_config_path}")
        print(
            "\nIMPORTANT: Please review the new config file, especially the 'excludes' section, to ensure correctness."
        )

    except Exception as e:
        print(f"Error during configuration conversion: {e}")
        sys.exit(1)

    print("\nMigration complete!")


if __name__ == "__main__":
    main()

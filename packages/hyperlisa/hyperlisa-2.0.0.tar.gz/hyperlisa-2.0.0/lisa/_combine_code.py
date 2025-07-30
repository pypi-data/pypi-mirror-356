import os
import sys
import glob
import json
from datetime import datetime, timezone
import fnmatch
import logging
import yaml
import collections

logger: logging.Logger = None


def setup_logging(log_level_str="INFO"):
    log_levels = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL,
    }
    log_level = log_levels.get(log_level_str.upper(), logging.INFO)
    logging.basicConfig(
        level=log_level, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )
    logger = logging.getLogger(__name__)
    return logger


def load_configuration(config_path):
    try:
        with open(config_path, "r") as f:
            config = yaml.full_load(f)
            if not config:
                print(f"Error: Configuration file is empty or invalid: {config_path}")
                sys.exit(1)
            return config
    except FileNotFoundError:
        print(f"Error: Configuration file not found at {config_path}")
        print("Please run 'hyperlisa-configure' to create a default configuration file.")
        sys.exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred while reading the configuration: {e}")
        sys.exit(1)


def is_excluded(path_to_check, is_dir, exclude_patterns):
    for pattern in exclude_patterns:
        is_dir_pattern = pattern.endswith("/")
        clean_pattern = pattern.rstrip("/")
        if is_dir and is_dir_pattern:
            if fnmatch.fnmatch(path_to_check, clean_pattern) or fnmatch.fnmatch(
                os.path.basename(path_to_check), clean_pattern
            ):
                return True
        elif not is_dir and not is_dir_pattern:
            if fnmatch.fnmatch(path_to_check, pattern) or fnmatch.fnmatch(os.path.basename(path_to_check), pattern):
                return True
    return False


def expand_paths(path_objects, root_dir):
    expanded_paths = []
    for path_obj in path_objects:
        pattern = path_obj.get("path", "")
        depth = path_obj.get("depth", "*")
        glob_pattern = os.path.join(root_dir, pattern.lstrip("/\\"))
        matched_paths = glob.glob(glob_pattern, recursive=True)
        for path in matched_paths:
            if os.path.isdir(path):
                expanded_paths.append({"path": path, "depth": depth})
    return expanded_paths


def matches_pattern(path, patterns):
    return any(fnmatch.fnmatch(path, p) or fnmatch.fnmatch(os.path.basename(path), p) for p in patterns)


def get_language_from_extension(file_path):
    ext_map = {
        ".py": "python",
        ".js": "javascript",
        ".ts": "typescript",
        ".java": "java",
        ".cs": "csharp",
        ".html": "html",
        ".css": "css",
        ".scss": "scss",
        ".md": "markdown",
        ".json": "json",
        ".yaml": "yaml",
        ".yml": "yaml",
        ".xml": "xml",
        ".sh": "shell",
        ".bash": "shell",
    }
    _, ext = os.path.splitext(file_path)
    return ext_map.get(ext.lower(), "plaintext")


def get_file_metadata(file_path, app_root):
    try:
        line_count = len(open(file_path, "r", encoding="utf-8", errors="ignore").readlines())
        last_mod_timestamp = os.path.getmtime(file_path)
        last_mod_utc = datetime.fromtimestamp(last_mod_timestamp, tz=timezone.utc)
        return {
            "path": os.path.relpath(file_path, app_root).replace("\\", "/"),
            "language": get_language_from_extension(file_path),
            "lines": line_count,
            "last_modified": last_mod_utc.isoformat().replace("+00:00", "Z"),
        }
    except Exception:
        return {
            "path": os.path.relpath(file_path, app_root).replace("\\", "/"),
            "language": "unknown",
            "lines": 0,
            "last_modified": "",
        }


def process_profile(profile, global_excludes, app_root):
    logger.info(f"Processing profile: '{profile['name']}'")
    collected_files = set()
    for block in profile.get("blocks", []):
        block_includes = block.get("includes", [])
        block_excludes = block.get("excludes", [])
        all_excludes = global_excludes + block_excludes
        path_objects = expand_paths(block.get("paths", []), app_root)

        for path_obj in path_objects:
            start_path = path_obj["path"]
            depth_limit = path_obj["depth"]

            for root, dirs, files in os.walk(start_path, topdown=True):
                if depth_limit != "*":
                    current_depth = root.replace(start_path, "").count(os.sep)
                    if current_depth >= depth_limit:
                        dirs[:] = []

                dirs[:] = [d for d in dirs if not is_excluded(os.path.join(root, d), True, all_excludes)]

                for file in files:
                    file_path = os.path.join(root, file)
                    relative_file_path = os.path.relpath(file_path, app_root)
                    if is_excluded(relative_file_path.replace("\\", "/"), False, all_excludes):
                        continue
                    if matches_pattern(relative_file_path, block_includes):
                        collected_files.add(file_path)

    sorted_files = sorted(list(collected_files), key=lambda x: (x.count(os.sep), x))
    return sorted_files


def generate_filename(template, project_name, timestamp, profile_name=None):
    name = template.replace("$n", project_name).replace("$ts", timestamp)
    if profile_name:
        name = name.replace("$p", profile_name)
    else:
        name = name.replace(f"_$p", "").replace(f"-$p", "")
    return f"{name}.txt"


def clean_output_directory(config_dir, config):
    """
    Finds and removes previously generated output files.
    """
    logger.info("Scanning for old output files to clean...")

    name_template = config.get("profiles", {}).get("name_template", "$n_$p_$ts")
    project_name = os.path.basename(os.getcwd()).upper()
    profiles = config.get("profiles", {}).get("profiles_list", [])

    patterns_to_find = []

    # Pattern per i file dei singoli profili
    for profile in profiles:
        profile_name = profile.get("name")
        if profile_name:
            pattern = name_template.replace("$n", project_name)
            pattern = pattern.replace("$p", profile_name)
            pattern = pattern.replace("$ts", "*")
            patterns_to_find.append(f"{pattern}.txt")

    # Pattern per il file --merge-all
    merged_pattern = name_template.replace("$n", project_name)
    merged_pattern = merged_pattern.replace(f"_$p", "").replace(f"-$p", "")
    merged_pattern = merged_pattern.replace("$ts", "*")
    patterns_to_find.append(f"{merged_pattern}.txt")

    files_to_delete = set()
    for pattern in patterns_to_find:
        search_path = os.path.join(config_dir, pattern)
        found_files = glob.glob(search_path)
        files_to_delete.update(found_files)

    if not files_to_delete:
        print("No old output files found to clean.")
        return

    print("The following files will be deleted:")
    for f in sorted(list(files_to_delete)):
        print(f" - {os.path.basename(f)}")

    # Chiedi conferma all'utente
    try:
        confirm = input("Are you sure you want to delete these files? (y/N): ")
    except (EOFError, KeyboardInterrupt):
        print("\nOperation cancelled.")
        sys.exit(0)

    if confirm.lower() == "y":
        deleted_count = 0
        for f in files_to_delete:
            try:
                os.remove(f)
                deleted_count += 1
            except OSError as e:
                logger.error(f"Failed to delete {f}: {e}")
        print(f"\nSuccessfully deleted {deleted_count} file(s).")
    else:
        print("Operation cancelled.")


def generate_tree_structure(file_list, app_root):
    tree = {}
    for path in file_list:
        relative_path = os.path.relpath(path, app_root).replace("\\", "/")
        parts = relative_path.split("/")
        node = tree
        for i, part in enumerate(parts):
            is_last_part = i == len(parts) - 1
            if is_last_part:
                node[part] = None
            else:
                node = node.setdefault(part, {})

    def build_string(node, indent=""):
        lines = []
        items = sorted(node.items())
        for i, (key, value) in enumerate(items):
            connector = "└── " if i == len(items) - 1 else "├── "
            lines.append(f"{indent}{connector}{key}")
            if value is not None:
                extension = "    " if i == len(items) - 1 else "│   "
                lines.extend(build_string(value, indent + extension))
        # La riga mancante che causava l'errore
        return lines

    return ".\n" + "\n".join(build_string(tree))


def write_combined_file(output_path, file_list, app_root, tree_string=None):
    logger.info(f"Generating combined file at: {output_path}")
    header_top_bottom = "!" + "#" * 69

    try:
        with open(output_path, "w", encoding="utf-8") as outfile:
            # Scrivi la struttura ad albero se fornita
            if tree_string:
                outfile.write(f"{header_top_bottom}\n")
                outfile.write("/!#\n/!# STRUTTURA DEL PROGETTO\n/!#\n")
                for line in tree_string.split("\n"):
                    outfile.write(f"/!# {line}\n")
                outfile.write("/!#\n")
                outfile.write(f"{header_top_bottom}\n\n")

            # Scrivi il contenuto dei file
            header_separator = "/!# " + "+" * 50
            for file_path in file_list:
                metadata = get_file_metadata(file_path, app_root)
                relative_path = metadata["path"]
                metadata_json_str = json.dumps(metadata, indent=4)

                outfile.write(f"{header_top_bottom}\n")
                outfile.write("/!#\n")
                outfile.write(f"{header_separator}\n")
                outfile.write(f"/!# {relative_path}\n")
                outfile.write(f"{header_separator}\n")
                outfile.write("/!# {\n")
                for line in metadata_json_str.split("\n")[1:-1]:
                    outfile.write(f"/!# {line}\n")
                outfile.write("/!# }\n")
                outfile.write(f"{header_top_bottom}\n\n")

                try:
                    with open(file_path, "r", encoding="utf-8", errors="ignore") as infile:
                        outfile.write(infile.read())
                        outfile.write("\n\n")
                except Exception as e:
                    logger.warning(f"Could not read file {file_path}: {e}")
        print(f"Successfully generated: {output_path}")
    except Exception as e:
        logger.error(f"Failed to write output file {output_path}: {e}")


def main():
    global logger
    app_root = os.getcwd()
    config_dir = os.path.join(app_root, ".hyperlisa")
    config_path = os.path.join(config_dir, "config.yaml")

    config = load_configuration(config_path)
    log_level = config.get("log_level", "INFO")
    logger = setup_logging(log_level)

    args = sys.argv[1:]

    # Gestisci --clean per primo, dato che non richiede ulteriori elaborazioni
    if args and args[0] == "--clean":
        clean_output_directory(config_dir, config)
        sys.exit(0)

    profiles = {p["name"]: p for p in config.get("profiles", {}).get("profiles_list", [])}
    global_excludes = config.get("global_excludes", [])
    name_template = config.get("profiles", {}).get("name_template", "$n_$p_$ts")
    project_name = os.path.basename(app_root).upper()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M")

    show_tree = "--notree" not in args
    if not show_tree:
        args.remove("--notree")

    command = None
    if args:
        command = args[0]

    target_profile_names = []
    if not command or command == "--merge-all":
        for name, profile in profiles.items():
            if profile.get("enable", False):
                target_profile_names.append(name)
    elif command in profiles:
        if profiles[command].get("enable", False):
            target_profile_names.append(command)
        else:
            logger.warning(f"Profile '{command}' is disabled and will be skipped.")
    else:
        logger.error(f"Command or profile '{command}' not found.")
        sys.exit(1)

    if not target_profile_names:
        logger.warning("No enabled profiles to run.")
        sys.exit(0)

    logger.info(f"Target profiles to be processed: {target_profile_names}")

    profile_results = {}
    for name in target_profile_names:
        profile_results[name] = process_profile(profiles[name], global_excludes, app_root)

    if command == "--merge-all":
        merged_files = set()
        for files in profile_results.values():
            merged_files.update(files)
        final_list = sorted(list(merged_files), key=lambda x: (x.count(os.sep), x))

        tree = generate_tree_structure(final_list, app_root) if show_tree else None
        output_filename = generate_filename(name_template, project_name, timestamp)
        write_combined_file(os.path.join(config_dir, output_filename), final_list, app_root, tree_string=tree)
    else:
        for name, files in profile_results.items():
            if command and name != command:
                continue

            tree = generate_tree_structure(files, app_root) if show_tree else None
            output_filename = generate_filename(name_template, project_name, timestamp, profile_name=name)
            write_combined_file(os.path.join(config_dir, output_filename), files, app_root, tree_string=tree)


if __name__ == "__main__":
    main()

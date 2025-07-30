import os
import shutil


def main():
    config_dir_name = ".hyperlisa"
    destination_dir = os.path.join(os.getcwd(), config_dir_name)
    config_file_name = "config.yaml"

    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Il file di esempio è ora parte del pacchetto e viene cercato qui
    source_sample_file = os.path.join(script_dir, "config.yaml.sample")

    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)
        print(f"Created configuration directory: {destination_dir}")

    destination_file = os.path.join(destination_dir, config_file_name)
    if not os.path.exists(destination_file):
        if os.path.exists(source_sample_file):
            shutil.copy(source_sample_file, destination_file)
            print(f"Default configuration file has been created at {destination_file}")
        else:
            # Fallback nel caso improbabile che il sample non sia nel pacchetto
            with open(destination_file, "w") as f:
                f.write("# Hyperlisa v2.0 Configuration File\n")
            print(f"Created an empty configuration file at {destination_file}. Please populate it.")
    else:
        print(f"Configuration file already exists at {destination_file}")

    gitignore_path = os.path.join(os.getcwd(), ".gitignore")
    if os.path.isfile(gitignore_path):
        try:
            with open(gitignore_path, "r") as gitignore_file:
                lines = gitignore_file.readlines()

            ignore_entry = f"{config_dir_name}/\n"
            if ignore_entry not in lines and f"{config_dir_name}/" not in [line.strip() for line in lines]:
                with open(gitignore_path, "a") as gitignore_file:
                    gitignore_file.write(f"\n# Hyperlisa configuration\n{ignore_entry}")
                print(f"Added '{config_dir_name}/' to .gitignore")
        except Exception as e:
            print(f"Warning: Could not update .gitignore file. Reason: {e}")


if __name__ == "__main__":
    main()

import argparse
import shutil
from pathlib import Path
import importlib.resources as pkg_resources
import sys

import npgp.templates  # your templates package

def copy_template_file(src_filename, target_dir, rename_to=None):
    try:
        with pkg_resources.path(npgp.templates, src_filename) as template_path:
            target_path = target_dir / (rename_to if rename_to else src_filename)
            if target_path.exists():
                print(f"❌ '{target_path.name}' already exists in {target_dir}.")
                return False
            shutil.copy(template_path, target_path)
        return True
    except FileNotFoundError:
        print(f"❌ Template file '{src_filename}' not found in package.")
        return False

def create_project():
    parser = argparse.ArgumentParser(
        description="Create a new Pygame project from a template."
    )
    parser.add_argument(
        "template",
        choices=["basic", "class"],
        help="The project template to use"
    )
    parser.add_argument(
        "project_name",
        help="The name of the new project folder to create"
    )
    args = parser.parse_args()

    current_dir = Path.cwd()
    project_dir = current_dir / args.project_name

    if project_dir.exists():
        print(f"❌ Directory '{args.project_name}' already exists.")
        sys.exit(1)

    # Create project folder
    project_dir.mkdir()

    # Copy main template file and rename to main.py
    main_template = f"{args.template}.py"
    if not copy_template_file(main_template, project_dir, rename_to="main.py"):
        sys.exit(1)

    # Copy shared config.py (keep same name)
    if not copy_template_file("config.py", project_dir):
        sys.exit(1)

    print(f"✅ New Pygame project '{args.project_name}' created from '{args.template}' template.")

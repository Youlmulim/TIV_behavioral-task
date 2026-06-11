#!/usr/bin/env python3
"""
Automatic Import Fixer for configs/ and utils/ folder structure
This script updates all import statements based on file locations
"""

import os
from pathlib import Path
import shutil
from datetime import datetime

# Define which modules are in which folder
CONFIGS_MODULES = [
    'get_screen_details',
    'get_param_details',
    'get_param_for_drawing',
    'get_img_texture',
    'get_question_order',
    'initiate_params',
    'setting_mouse',
]

UTILS_MODULES = [
    'ask_question',
    'draw_dashed_lines',
    'handle_fixation',
    'show_example_images',
    'show_question_images',
    'waiting_screen',
    'waiting_time',
]


def get_import_prefix(module_name):
    """Get the correct import prefix for a module"""
    if module_name in CONFIGS_MODULES:
        return ''  # No prefix needed when importing within same folder
    elif module_name in UTILS_MODULES:
        return ''  # No prefix needed when importing within same folder
    return ''


def fix_imports_in_file(file_path, folder_name):
    """
    Fix imports in a single Python file

    Parameters:
    -----------
    file_path : Path
        Path to the Python file
    folder_name : str
        Either 'configs' or 'utils'
    """

    # Read the file
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    original_content = ''.join(lines)
    new_lines = []

    for line in lines:
        new_line = line

        # Check if this is an import line
        if line.strip().startswith('from ') and ' import ' in line:
            for module in CONFIGS_MODULES + UTILS_MODULES:
                # Pattern: "from module_name import"
                pattern = f"from {module} import"

                if pattern in line:
                    # Determine if we need to add a prefix
                    if folder_name == 'configs':
                        # In configs folder
                        if module in CONFIGS_MODULES:
                            # Importing from same folder - no prefix
                            new_line = line.replace(f"from configs.{module}", f"from {module}")
                        elif module in UTILS_MODULES:
                            # Importing from utils folder
                            # Need to add parent path access
                            if not line.startswith(f"from utils.{module}"):
                                new_line = line.replace(f"from {module}", f"from utils.{module}")

                    elif folder_name == 'utils':
                        # In utils folder
                        if module in UTILS_MODULES:
                            # Importing from same folder - no prefix
                            new_line = line.replace(f"from utils.{module}", f"from {module}")
                        elif module in CONFIGS_MODULES:
                            # Importing from configs folder
                            # Need to add parent path access
                            if not line.startswith(f"from configs.{module}"):
                                new_line = line.replace(f"from {module}", f"from configs.{module}")

                    break

        new_lines.append(new_line)

    new_content = ''.join(new_lines)

    # Check if anything changed
    if new_content != original_content:
        # Create backup
        backup_path = file_path.with_suffix('.py.backup')
        shutil.copy2(file_path, backup_path)

        # Write updated content
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(new_content)

        return True, f"Updated (backup: {backup_path.name})"

    return False, "No changes needed"


def main():
    """Main function"""
    print("=" * 70)
    print("Automatic Import Fixer for configs/ and utils/ folders")
    print("=" * 70)
    print()

    # Get directories
    configs_dir = Path("configs")
    utils_dir = Path("utils")

    if not configs_dir.exists():
        print("❌ ERROR: 'configs' folder not found!")
        return

    if not utils_dir.exists():
        print("❌ ERROR: 'utils' folder not found!")
        return

    print(f"📁 Found configs directory: {configs_dir.absolute()}")
    print(f"📁 Found utils directory:   {utils_dir.absolute()}")
    print()

    # Create __init__.py files if they don't exist
    for folder_name, folder_path in [('configs', configs_dir), ('utils', utils_dir)]:
        init_file = folder_path / "__init__.py"
        if not init_file.exists():
            with open(init_file, 'w', encoding='utf-8') as f:
                f.write(f'"""\n{folder_name.title()} modules\n"""\n')
            print(f"✅ Created: {folder_name}/__init__.py")
        else:
            print(f"✓  {folder_name}/__init__.py already exists")
    print()

    # Process files in both folders
    all_updated = []
    all_unchanged = []

    for folder_name, folder_path in [('configs', configs_dir), ('utils', utils_dir)]:
        print(f"\n{'=' * 70}")
        print(f"Processing {folder_name.upper()} folder...")
        print("-" * 70)

        for py_file in sorted(folder_path.glob("*.py")):
            if py_file.name == "__init__.py":
                continue

            changed, message = fix_imports_in_file(py_file, folder_name)

            if changed:
                print(f"✅ {py_file.name:35s} - {message}")
                all_updated.append(f"{folder_name}/{py_file.name}")
            else:
                print(f"   {py_file.name:35s} - {message}")
                all_unchanged.append(f"{folder_name}/{py_file.name}")

    # Summary
    print()
    print("=" * 70)
    print("SUMMARY")
    print("=" * 70)
    print(f"✅ Updated files:   {len(all_updated)}")
    print(f"   Unchanged files: {len(all_unchanged)}")
    print()

    if all_updated:
        print("Updated files:")
        for f in all_updated:
            print(f"  - {f}")
        print()
        print("💾 Backups created with .backup extension")

    print()
    print("=" * 70)
    print("EXPECTED STRUCTURE")
    print("=" * 70)
    print("""
configs/  (Setup & Parameters)
  ├── __init__.py
  ├── get_screen_details.py
  ├── get_param_details.py
  ├── get_param_for_drawing.py
  ├── get_img_texture.py
  ├── get_question_order.py
  ├── initiate_params.py
  ├── setting_mouse.py
  ├── leftRightMatrix.mat
  ├── questionMatrix.mat
  └── scoringOrder.mat

utils/  (Display & Interaction)
  ├── __init__.py
  ├── ask_question.py
  ├── draw_dashed_lines.py
  ├── handle_fixation.py
  ├── show_example_images.py
  ├── show_question_images.py
  ├── waiting_screen.py
  └── waiting_time.py
    """)

    print("=" * 70)
    print("NEXT STEPS")
    print("=" * 70)
    print("1. Replace your main.py with the updated version")
    print()
    print("2. Test the imports:")
    print("   python3 -c \"from configs.initiate_params import initiate_params; print('✓ configs OK')\"")
    print("   python3 -c \"from utils.ask_question import ask_question; print('✓ utils OK')\"")
    print()
    print("3. Run your experiment:")
    print("   python3 main.py test_subject")
    print()
    print("4. If everything works, delete .backup files:")
    print("   rm configs/*.backup utils/*.backup")
    print()


if __name__ == "__main__":
    main()
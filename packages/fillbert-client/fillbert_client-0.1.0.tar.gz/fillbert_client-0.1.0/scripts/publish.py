#!/usr/bin/env python3
"""Helper script for publishing the BOL OCR client package."""

import argparse
import subprocess  # nosec B404
import sys
from pathlib import Path


def run_command(cmd: list[str], cwd: Path | None = None) -> bool:
    """Run a command and return success status."""
    print(f"Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, cwd=cwd, check=False)  # nosec B603
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Publish BOL OCR client package")
    parser.add_argument(
        "--version", required=True, help="Version to publish (e.g., 0.1.1)"
    )
    parser.add_argument(
        "--test", action="store_true", help="Publish to TestPyPI instead"
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Build only, don't upload"
    )

    args = parser.parse_args()

    # Get the client directory
    client_dir = Path(__file__).parent.parent

    print(f"Publishing BOL OCR client v{args.version}")
    print(f"Working directory: {client_dir}")

    # Update version in pyproject.toml
    pyproject_file = client_dir / "pyproject.toml"
    content = pyproject_file.read_text()
    updated_content = content.replace(
        'version = "0.1.0"', f'version = "{args.version}"'
    )
    pyproject_file.write_text(updated_content)
    print(f"Updated version in pyproject.toml to {args.version}")

    # Update version in __init__.py
    init_file = client_dir / "src/bol_ocr_client/__init__.py"
    content = init_file.read_text()
    updated_content = content.replace(
        '__version__ = "0.1.0"', f'__version__ = "{args.version}"'
    )
    init_file.write_text(updated_content)
    print(f"Updated version in __init__.py to {args.version}")

    # Clean previous builds
    dist_dir = client_dir / "dist"
    if dist_dir.exists():
        print("Cleaning previous builds...")
        for file in dist_dir.glob("*"):
            file.unlink()

    # Run tests
    print("\nRunning tests...")
    if not run_command(["uv", "run", "pytest"], cwd=client_dir):
        print("Tests failed!")
        return 1

    # Run quality checks
    print("\nRunning quality checks...")
    if not run_command(["uv", "run", "ruff", "check", "."], cwd=client_dir):
        print("Ruff checks failed!")
        return 1

    if not run_command(["uv", "run", "mypy", "."], cwd=client_dir):
        print("MyPy checks failed!")
        return 1

    # Build package
    print("\nBuilding package...")
    if not run_command(["uv", "run", "python", "-m", "build"], cwd=client_dir):
        print("Build failed!")
        return 1

    # Check package
    print("\nChecking package...")
    if not run_command(["uv", "run", "twine", "check", "dist/*"], cwd=client_dir):
        print("Package check failed!")
        return 1

    if args.dry_run:
        print("\nDry run complete. Package built but not uploaded.")
        print("To upload manually:")
        if args.test:
            print("  uv run twine upload --repository testpypi dist/*")
        else:
            print("  uv run twine upload dist/*")
        return 0

    # Upload to PyPI
    print(f"\nUploading to {'TestPyPI' if args.test else 'PyPI'}...")
    upload_cmd = ["uv", "run", "twine", "upload"]
    if args.test:
        upload_cmd.extend(["--repository", "testpypi"])
    upload_cmd.append("dist/*")

    if not run_command(upload_cmd, cwd=client_dir):
        print("Upload failed!")
        return 1

    print(
        f"\nSuccess! BOL OCR client v{args.version} published to {'TestPyPI' if args.test else 'PyPI'}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

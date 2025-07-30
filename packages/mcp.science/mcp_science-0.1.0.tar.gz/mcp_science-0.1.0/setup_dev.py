#!/usr/bin/env python3
"""
Development setup script for mcp-science package.
This script helps with development and testing of the package.
"""

import sys
import subprocess
from pathlib import Path


def install_dev_dependencies():
    """Install development dependencies."""
    print("Installing development dependencies...")
    subprocess.run([sys.executable, "-m", "pip", "install",
                   "build", "twine"], check=True)


def build_package():
    """Build the package."""
    print("Building package...")
    subprocess.run([sys.executable, "-m", "build"], check=True)


def test_imports():
    """Test that all servers can be imported."""
    print("Testing imports...")

    # Add src to path
    src_path = Path(__file__).parent / "src"
    sys.path.insert(0, str(src_path))

    servers = [
        "example_server",
        "gpaw_computation",
        "jupyter_act",
        "materials_project",
        "mathematica_check",
        "nemad",
        "python_code_execution",
        "ssh_exec",
        "tinydb_server",
        "txyz_search",
        "web_fetch",
    ]

    for server in servers:
        try:
            module = __import__(
                f"mcp_science.servers.{server}", fromlist=["main"])
            if hasattr(module, "main"):
                print(f"✓ {server}: main function available")
            else:
                print(f"⚠ {server}: no main function found")
        except ImportError as e:
            print(f"✗ {server}: import failed - {e}")
        except Exception as e:
            print(f"✗ {server}: error - {e}")


def main():
    """Main function."""
    if len(sys.argv) < 2:
        print("Usage: python setup_dev.py <command>")
        print("Commands:")
        print("  install-dev  - Install development dependencies")
        print("  build        - Build the package")
        print("  test-imports - Test that all servers can be imported")
        print("  all          - Run all commands")
        return

    command = sys.argv[1]

    if command == "install-dev":
        install_dev_dependencies()
    elif command == "build":
        build_package()
    elif command == "test-imports":
        test_imports()
    elif command == "all":
        install_dev_dependencies()
        test_imports()
        build_package()
    else:
        print(f"Unknown command: {command}")


if __name__ == "__main__":
    main()

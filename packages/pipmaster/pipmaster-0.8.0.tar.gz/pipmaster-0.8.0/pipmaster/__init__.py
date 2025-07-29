# -*- coding: utf-8 -*-
"""
pipmaster: A versatile Python package manager utility.

Author: ParisNeo
Created: 01/04/2024
Last Updated: 23/04/2025
"""

# Read version dynamically - this must be present for pyproject.toml
__version__ = "0.8.0" # Updated for new features

# Expose the main synchronous functions
from .package_manager import (
    install,
    install_if_missing,
    install_edit,
    install_requirements,
    install_multiple,
    install_multiple_if_not_installed,
    install_version,
    is_installed,
    get_installed_version,
    get_current_package_version, # Added
    is_version_compatible,
    get_package_info,
    install_or_update,
    uninstall,
    uninstall_multiple,
    install_or_update_multiple,
    check_vulnerabilities,
    ensure_packages,
)

# Expose the main classes and factory functions
from .package_manager import (
    PackageManager,
    UvPackageManager,          # Added
    CondaPackageManager,       # Added
    get_pip_manager,
    get_uv_manager,            # Added
    get_conda_manager,         # Added
)

# Deprecated functions (kept for backward compatibility)
from .package_manager import is_version_higher, is_version_exact

# Define what `import *` imports (optional but good practice)
__all__ = [
    # Classes
    "PackageManager",
    "UvPackageManager",
    "CondaPackageManager",
    # Factory Functions
    "get_pip_manager",
    "get_uv_manager",
    "get_conda_manager",
    # Core Functions
    "install",
    "install_if_missing",
    "install_edit",
    "install_requirements",
    "install_multiple",
    "install_multiple_if_not_installed",
    "install_version",
    "is_installed",
    "get_installed_version",
    "get_current_package_version",
    "is_version_compatible",
    "get_package_info",
    "install_or_update",
    "uninstall",
    "uninstall_multiple",
    "install_or_update_multiple",
    "check_vulnerabilities",
    "ensure_packages",
    # Deprecated
    "is_version_higher",
    "is_version_exact",
    # Version
    "__version__",
]
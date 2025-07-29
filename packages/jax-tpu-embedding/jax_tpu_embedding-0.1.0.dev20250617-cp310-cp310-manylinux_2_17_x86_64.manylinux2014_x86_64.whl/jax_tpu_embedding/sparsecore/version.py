"""JAX TPU Embedding versioning utilities

For releases, the version is of the form:
  xx.yy.zz

For nightly builds, the date of the build is added:
  xx.yy.zz-devYYYMMDD
"""

_base_version = "0.1.0"
_version_suffix = "dev20250617"

# Git commit corresponding to the build, if available.
__git_commit__ = "2f8336d79124f97d5422403aaa8b1a9c8f00f18f"

# Library version.
__version__ = _base_version + _version_suffix


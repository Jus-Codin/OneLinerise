"""
Weird Oneliner mini-lang
~~~~~~~~~~~~~~~~~~~~~~~~
Don't even think of using this for actual implementations
:license: Unlicense License, see LICENSE for more details
"""

__title__ = "OneLineriser"
__author__ = "Jus-Codin"
__license__ = "Unlicense"
__version__ = "1.0.0"

from .onelineriser import OneLineriser

from typing import NamedTuple, Literal

class VersionInfo(NamedTuple):
  major: int
  minor: int
  micro: int
  releaselevel: Literal["alpha", "beta", "candidate", "final"]
  serial: int

version_info: VersionInfo = VersionInfo(major=0, minor=0, micro=2, releaselevel="beta")

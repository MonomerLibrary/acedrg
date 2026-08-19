#!/usr/bin/env python
"""Bump the acedrg version in lockstep across the two packages.

The version is ``0.<minor>.0`` where ``<minor>`` is ``ACEDRG_VERSION`` in
tables/manifest.txt. Both the acedrg wheel and the acedrg-data package derive
their version from that manifest, and acedrg pins an exact ``acedrg-data``
dependency. This script updates the manifest and keeps that pin in sync.

Usage:
    python scripts/bump_version.py 333        # set ACEDRG_VERSION -> 333
    python scripts/bump_version.py --check     # verify manifest and pin agree
"""
import argparse
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MANIFEST = os.path.join(
    ROOT, "packages", "acedrg-data", "src", "acedrg_data", "tables", "manifest.txt"
)
ROOT_PYPROJECT = os.path.join(ROOT, "pyproject.toml")

MANIFEST_RE = re.compile(r"(ACEDRG_VERSION:\s+)(\d+)")
PIN_RE = re.compile(r'("acedrg-data==0\.)(\d+)(\.0")')


def read_minor():
    with open(MANIFEST) as fh:
        match = MANIFEST_RE.search(fh.read())
    if not match:
        sys.exit("ACEDRG_VERSION not found in %s" % MANIFEST)
    return match.group(2)


def read_pin():
    with open(ROOT_PYPROJECT) as fh:
        match = PIN_RE.search(fh.read())
    if not match:
        sys.exit("acedrg-data pin not found in %s" % ROOT_PYPROJECT)
    return match.group(2)


def check():
    manifest_minor, pin_minor = read_minor(), read_pin()
    if manifest_minor != pin_minor:
        sys.exit(
            "Version mismatch: manifest=0.%s.0 but acedrg-data pin=0.%s.0.\n"
            "Run: python scripts/bump_version.py %s"
            % (manifest_minor, pin_minor, manifest_minor)
        )
    print("OK: both at 0.%s.0" % manifest_minor)


def bump(minor):
    with open(MANIFEST) as fh:
        text = fh.read()
    with open(MANIFEST, "w") as fh:
        fh.write(MANIFEST_RE.sub(r"\g<1>%s" % minor, text, count=1))

    with open(ROOT_PYPROJECT) as fh:
        text = fh.read()
    if not PIN_RE.search(text):
        sys.exit("acedrg-data pin not found in %s" % ROOT_PYPROJECT)
    with open(ROOT_PYPROJECT, "w") as fh:
        fh.write(PIN_RE.sub(r"\g<1>%s\g<3>" % minor, text, count=1))

    print("Bumped to 0.%s.0 (manifest + acedrg-data pin)" % minor)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("minor", nargs="?", help="new ACEDRG_VERSION minor number")
    parser.add_argument(
        "--check", action="store_true", help="verify manifest and pin agree"
    )
    args = parser.parse_args()

    if args.check:
        check()
    elif args.minor:
        if not args.minor.isdigit():
            sys.exit("minor must be an integer, got %r" % args.minor)
        bump(args.minor)
    else:
        parser.error("provide a minor version to set, or --check")


if __name__ == "__main__":
    main()

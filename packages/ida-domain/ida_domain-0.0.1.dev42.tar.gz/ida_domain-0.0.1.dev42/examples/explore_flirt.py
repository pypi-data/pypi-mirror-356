#!/usr/bin/env python3
"""
Database FLIRT example for IDA Domain API.

This example demonstrates how to work with signature files.
"""

import argparse
import json
from dataclasses import asdict
import ida_domain


def probe_sig_files(db: ida_domain.Database):
    """Probe the available sig files and print the matches."""
    files = db.flirt.get_files()
    for f in files:
        details = db.flirt.apply(f, probe_only=True)
        for d in details:
            if d.matches > 0:
                print(json.dumps(asdict(d), indent=4))


def generate_signatures(db: ida_domain.Database):
    """Generate signature files from the opened database."""
    sig_files = db.flirt.create()
    print('Generated signature files: ', sig_files)


def main():
    """Main entry point with argument parsing."""
    parser = argparse.ArgumentParser(description='Database traversing example')
    parser.add_argument(
        '-f', '--input-file', help='Binary input file to be loaded', type=str, required=True
    )
    args = parser.parse_args()
    ida_options = ida_domain.Database.IdaCommandBuilder().auto_analysis(True).new_database(True)
    db = ida_domain.Database()
    if db.open(args.input_file, ida_options):
        generate_signatures(db)
        probe_sig_files(db)
        db.close(False)


if __name__ == '__main__':
    main()

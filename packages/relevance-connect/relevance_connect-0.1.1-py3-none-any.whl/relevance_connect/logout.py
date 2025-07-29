#!/usr/bin/env python3
"""
CLI command for logging out from Relevance AI.
"""
import argparse
from relevance_connect.core.auth import logout


def main():
    parser = argparse.ArgumentParser(
        description='Logout from Relevance AI'
    )
    
    args = parser.parse_args()
    logout()


if __name__ == "__main__":
    main()
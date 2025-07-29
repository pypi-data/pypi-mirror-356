#!/usr/bin/env python3
import argparse
import sys
from relevance_connect.core.auth import login


def main():
    parser = argparse.ArgumentParser(
        description="Login to Relevance AI",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Interactive login (recommended)
  python login.py
  
  # Login with credentials as arguments
  python login.py --api-key YOUR_API_KEY --region YOUR_REGION --project YOUR_PROJECT
  
  # Login without storing credentials
  python login.py --no-store
        """
    )
    
    parser.add_argument(
        "--api-key",
        help="API key from your Relevance AI profile",
        default=None
    )
    parser.add_argument(
        "--region", 
        help="Region from your Relevance AI profile",
        default=None
    )
    parser.add_argument(
        "--project",
        help="Project ID from your Relevance AI profile", 
        default=None
    )
    parser.add_argument(
        "--no-store",
        action="store_true",
        help="Don't store credentials to file"
    )
    
    args = parser.parse_args()
    
    try:
        login(
            api_key=args.api_key,
            region=args.region, 
            project=args.project,
            store=not args.no_store
        )
    except KeyboardInterrupt:
        print("\nLogin cancelled.")
        sys.exit(1)
    except Exception as e:
        print(f"Error during login: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
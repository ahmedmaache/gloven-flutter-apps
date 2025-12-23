#!/usr/bin/env python3
"""
Parallel Flutter app generator
Generates 100 Flutter apps more efficiently using multiprocessing
"""

import subprocess
import multiprocessing
import os
import sys
from pathlib import Path

def create_app(app_number):
    """Create a single Flutter app"""
    script_path = Path(__file__).parent / "create_app_template.sh"
    try:
        result = subprocess.run(
            [str(script_path), str(app_number)],
            capture_output=True,
            text=True,
            timeout=300  # 5 minute timeout per app
        )
        if result.returncode == 0:
            return (app_number, True, "Success")
        else:
            return (app_number, False, result.stderr)
    except subprocess.TimeoutExpired:
        return (app_number, False, "Timeout")
    except Exception as e:
        return (app_number, False, str(e))

def main():
    """Generate all 100 apps in parallel"""
    num_workers = min(10, multiprocessing.cpu_count() * 2)  # Use up to 10 workers
    
    print(f"Generating 100 Flutter apps using {num_workers} workers...")
    print("This may take a while...")
    
    with multiprocessing.Pool(processes=num_workers) as pool:
        results = pool.map(create_app, range(1, 101))
    
    # Report results
    successful = [r for r in results if r[1]]
    failed = [r for r in results if not r[1]]
    
    print(f"\n{'='*60}")
    print(f"Generation complete!")
    print(f"Successful: {len(successful)}/100")
    print(f"Failed: {len(failed)}/100")
    
    if failed:
        print("\nFailed apps:")
        for app_num, _, error in failed:
            print(f"  App {app_num:02d}: {error[:100]}")
    
    return len(failed) == 0

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)


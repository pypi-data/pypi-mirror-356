#!/usr/bin/env python3
"""Quick test script for CLI development."""

import subprocess
import sys

def run_cmd(cmd: str) -> None:
    """Run a command and show output."""
    print(f"\n🔥 Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd="/Users/jedrzej/patronus/patronus-py")
        print(f"Exit code: {result.returncode}")
        if result.stdout:
            print(f"STDOUT:\n{result.stdout}")
        if result.stderr and result.stderr.strip():
            print(f"STDERR:\n{result.stderr}")
    except Exception as e:
        print(f"Error: {e}")

def main():
    print("Testing Patronus CLI scaffolding...")
    
    # Test basic CLI
    run_cmd("uv run patronus --help")
    run_cmd("uv run patronus --version")
    
    # Test prompts commands
    run_cmd("uv run patronus prompts --help")
    run_cmd("uv run patronus prompts pull --help")
    run_cmd("uv run patronus prompts pull")
    run_cmd("uv run patronus prompts tidy")

if __name__ == "__main__":
    main()

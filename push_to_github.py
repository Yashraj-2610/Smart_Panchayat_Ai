"""
Interactive GitHub Push Helper
Guides you through pushing the project to your GitHub account
"""
import subprocess
import sys
import os

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60 + "\n")

def run_cmd(cmd):
    try:
        res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        return res.returncode == 0, res.stdout, res.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    print_header("GitHub Push Helper - Smart Panchayat AI")

    print("""
This helper will guide you through pushing the project to your GitHub.

Prerequisites:
1. You have a GitHub account (https://github.com)
2. You created an empty repository on GitHub
   (Go to https://github.com/new and create 'smart-panchayat-ai')
3. You have a GitHub Personal Access Token or SSH key
    """)

    username = input("Enter your GitHub username: ").strip()
    if not username:
        print("❌ Username cannot be empty")
        return

    repo_name = input("Enter repository name [default: smart-panchayat-ai]: ").strip() or "smart-panchayat-ai"

    print("\nConfiguring git...")

    # Git user config
    name = input("Enter your full name for commits: ").strip() or username
    email = input("Enter your email: ").strip() or f"{username}@users.noreply.github.com"

    run_cmd(f'git config user.name "{name}"')
    run_cmd(f'git config user.email "{email}"')

    # Add all files
    print("\nAdding files to git...")
    success, out, err = run_cmd("git add .")
    if not success:
        print(f"Error adding files: {err}")
        return

    # Commit
    print("Creating commit...")
    commit_msg = "Initial commit: Smart Panchayat AI - Multi-Agent Decision Support System"
    success, out, err = run_cmd(f'git commit -m "{commit_msg}"')
    if not success and "nothing to commit" not in out:
        print(f"Commit note: {out or err}")

    # Set branch to main
    run_cmd("git branch -M main")

    # Add remote
    remote_url = f"https://github.com/{username}/{repo_name}.git"
    print(f"\nAdding remote: {remote_url}")
    run_cmd("git remote remove origin")  # Remove if exists
    run_cmd(f"git remote add origin {remote_url}")

    print_header("Ready to Push!")
    print(f"""
Your project is ready to push to:
  {remote_url}

To complete the push, run this command in your terminal:

  git push -u origin main

When prompted:
  - Username: {username}
  - Password: Use your GitHub Personal Access Token
    (Generate one at: https://github.com/settings/tokens)

Or if you prefer GitHub Desktop:
  1. Open GitHub Desktop
  2. File → Add Local Repository
  3. Select this folder: {os.getcwd()}
  4. Click 'Publish repository'
    """)

    do_push = input("Do you want to try pushing now? [y/N]: ").strip().lower()
    if do_push == 'y':
        print("\nPushing to GitHub (you may be prompted for credentials)...")
        # Run interactively so user can enter credentials
        os.system("git push -u origin main")

    print("\n✨ Done! Check your repository on GitHub.")

if __name__ == "__main__":
    main()

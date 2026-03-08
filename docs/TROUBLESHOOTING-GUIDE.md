# 🛠️ Polymarket Intelligence - Troubleshooting Guide

**Phase:** Phase 1 - Foundation  
**Created:** 2026-03-08  
**Status:** ✅ All Issues Resolved

---

## 📋 **Table of Contents**

1. [Git Issues](#1-git-issues)
2. [Python Issues](#2-python-issues)
3. [GitHub Issues](#3-github-issues)
4. [General Commands](#4-general-commands)
5. [Quick Fixes](#5-quick-fixes)

---

## 1. Git Issues

### Issue 1.1: Branch Name Mismatch

**Error:**
```
error: src refspec main does not match any
error: failed to push some refs to 'https://github.com/...'
```

**Cause:** Local branch is `master`, remote expects `main`

**Fix:**
```powershell
# Check current branch name
git branch

# Rename to main
git branch -M main

# Push again
git push -u origin main
```

**Prevention:** Always use `git branch -M main` before first push

---

### Issue 1.2: Remote Has README Conflict

**Error:**
```
To https://github.com/...
 ! [rejected] main -> main (fetch first)
error: failed to push some refs
hint: Updates were rejected because the remote contains work that you do not have locally.
```

**Cause:** GitHub repo created with README, local doesn't have it

**Fix Option 1 - Pull First:**
```powershell
git pull origin main --allow-unrelated-histories
git push -u origin main
```

**Fix Option 2 - Fresh Start (Recommended):**
```powershell
# Remove old Git
Remove-Item -Recurse -Force .git

# Fresh init
git init

# Add remote
git remote add origin <repository-url>

# Add & commit
git add .
git commit -m "Initial commit"

# Rename branch
git branch -M main

# Force push
git push -u origin main --force
```

**Prevention:** Create GitHub repo WITHOUT README when pushing existing code

---

### Issue 1.3: Merge Conflict

**Error:**
```
Auto-merging README.md
CONFLICT (add/add): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.
```

**Cause:** Both local and remote have different README.md files

**Fix:**
```powershell
# Cancel merge
git merge --abort

# Take remote version
git checkout origin/main -- README.md

# Pull again
git pull origin main

# Push
git push -u origin main
```

**Alternative (Keep Local):**
```powershell
git merge --abort
git add README.md
git commit -m "Keep local README"
git pull origin main --strategy-option=theirs
git push -u origin main
```

---

### Issue 1.4: Unrelated Histories

**Error:**
```
fatal: refusing to merge unrelated histories
```

**Cause:** Local and remote have completely different Git histories

**Fix:**
```powershell
# Option 1: Allow unrelated histories
git pull origin main --allow-unrelated-histories

# Option 2: Fresh start (better)
Remove-Item -Recurse -Force .git
git init
git remote add origin <url>
git add .
git commit -m "Initial commit"
git branch -M main
git push -u origin main --force
```

---

### Issue 1.5: Git Identity Unknown

**Error:**
```
Author identity unknown
*** Please tell me who you are.
Run
 git config --global user.email "you@example.com"
 git config --global user.name "Your Name"
fatal: unable to auto-detect email address
```

**Cause:** Git user name and email not configured

**Fix:**
```powershell
# Set Git identity (global)
git config --global user.name "সজল বস"
git config --global user.email "your-email@example.com"

# Or for this repo only (omit --global)
git config user.name "সজল বস"
git config user.email "your-email@example.com"

# Then commit
git add .
git commit -m "Initial commit"
```

**Prevention:** Set identity immediately after Git install

---

### Issue 1.6: Nothing to Commit

**Error:**
```
On branch main
nothing to commit, working tree clean
```

**Cause:** No changes to commit, or files not staged

**Fix:**
```powershell
# Check status
git status

# If files exist but not staged
git add .
git status

# If still nothing, files might be in .gitignore
# Check .gitignore file
```

---

## 2. Python Issues

### Issue 2.1: Python Not Found

**Error:**
```
python : The term 'python' is not recognized as the name of a cmdlet
```

**Cause:** Python not installed or not in PATH

**Fix:**
```powershell
# Check if Python is installed
where python

# If not found, reinstall Python
# Download from: https://www.python.org/downloads/
# ⚠️ CHECK: "Add Python to PATH" during installation
```

**Verification:**
```powershell
python --version
# Should show: Python 3.11.x
```

---

### Issue 2.2: Virtual Environment Not Activating

**Error:**
```
.\venv\Scripts\activate : File not found
```

**Cause:** Virtual environment not created correctly

**Fix:**
```powershell
# Remove old venv
Remove-Item -Recurse -Force venv

# Create new venv
python -m venv venv

# Activate (Windows)
.\venv\Scripts\activate

# Should see: (venv) PS C:\...
```

---

### Issue 2.3: Pip Install Fails

**Error:**
```
ERROR: Could not find a version that satisfies the requirement <package>
```

**Cause:** Package name wrong, or pip not updated

**Fix:**
```powershell
# Update pip
python -m pip install --upgrade pip

# Try install again
pip install <package-name>

# Check package name on PyPI: https://pypi.org/
```

---

## 3. GitHub Issues

### Issue 3.1: Authentication Failed

**Error:**
```
remote: Support for password authentication was removed on August 13, 2021.
remote: Please use a personal access token instead.
```

**Cause:** Password authentication no longer supported

**Fix:**
```powershell
# Option 1: Use Personal Access Token (PAT)
# 1. Go to GitHub → Settings → Developer settings → Personal access tokens
# 2. Generate new token (repo scope)
# 3. Use token instead of password

# Option 2: Use SSH (better)
# 1. Generate SSH key
ssh-keygen -t ed25519 -C "your-email@example.com"

# 2. Add to GitHub
# GitHub → Settings → SSH and GPG keys → New SSH key
# 3. Copy public key
type $env:USERPROFILE\.ssh\id_ed25519.pub

# 4. Change remote URL to SSH
git remote set-url origin git@github.com:USERNAME/REPO.git
```

---

### Issue 3.2: Repository Not Found

**Error:**
```
remote: Repository not found.
fatal: repository 'https://github.com/...' not found
```

**Cause:** Repository doesn't exist, or no access

**Fix:**
```powershell
# Check repository URL
git remote -v

# Verify repository exists on GitHub
# Go to: https://github.com/USERNAME/REPO

# If private repo, ensure you have access
# If typo, fix remote URL
git remote set-url origin <correct-url>
```

---

## 4. General Commands

### Git Basic Commands:
```powershell
# Initialize
git init

# Check status
git status

# Add files
git add .
git add <filename>

# Commit
git commit -m "Message"

# Check branch
git branch

# Rename branch
git branch -M main

# Add remote
git remote add origin <url>

# Check remote
git remote -v

# Pull
git pull origin main

# Push
git push -u origin main

# Force push
git push -u origin main --force

# Set identity
git config --global user.name "Your Name"
git config --global user.email "email@example.com"
```

### Git Troubleshooting:
```powershell
# Remove Git folder (Windows)
Remove-Item -Recurse -Force .git

# Abort merge
git merge --abort

# Cancel changes
git checkout -- <filename>

# View commit history
git log --oneline

# Check diff
git diff
```

---

## 5. Quick Fixes

### Quick Fix 1: Everything Broken, Start Fresh
```powershell
# Remove Git
Remove-Item -Recurse -Force .git

# Fresh start
git init
git config user.name "Your Name"
git config user.email "email@example.com"
git remote add origin <url>
git add .
git commit -m "Initial commit"
git branch -M main
git push -u origin main --force
```

---

### Quick Fix 2: Can't Push to GitHub
```powershell
# Check remote
git remote -v

# If wrong, fix it
git remote set-url origin <correct-url>

# Try pull first
git pull origin main --allow-unrelated-histories

# Then push
git push -u origin main
```

---

### Quick Fix 3: Commit Fails
```powershell
# Set identity
git config user.name "Your Name"
git config user.email "email@example.com"

# Try commit again
git commit -m "Message"
```

---

### Quick Fix 4: Branch Issues
```powershell
# Check current branch
git branch

# Rename to main
git branch -M main

# Set upstream
git push -u origin main
```

---

## 📞 **Common Error Messages & Solutions**

| Error | Quick Fix |
|-------|-----------|
| `src refspec main does not match any` | `git branch -M main` |
| `Updates were rejected` | `git pull` then `git push` |
| `Author identity unknown` | `git config user.name/email` |
| `nothing to commit` | `git add .` first |
| `refusing to merge unrelated histories` | `--allow-unrelated-histories` or fresh init |
| `Repository not found` | Check URL, verify repo exists |
| `Authentication failed` | Use PAT or SSH |

---

## 🎓 **Best Practices**

### Before Starting:
```
✓ Set Git identity first
✓ Create GitHub repo WITHOUT README
✓ Verify repository URL
```

### During Work:
```
✓ Commit frequently
✓ Write clear commit messages
✓ Pull before push
```

### When Stuck:
```
✓ Check `git status` first
✓ Read error messages carefully
✓ Google the exact error
✓ Ask for help with full error output
```

---

## 📝 **Phase 1 Issues Encountered & Resolved**

| # | Issue | Status | Solution Used |
|---|-------|--------|---------------|
| 1 | Branch name mismatch | ✅ Resolved | `git branch -M main` |
| 2 | README conflict | ✅ Resolved | Fresh Git init + force push |
| 3 | Unrelated histories | ✅ Resolved | `--force` push |
| 4 | Git identity unknown | ✅ Resolved | `git config user.name/email` |

**Total Issues:** 4  
**Resolved:** 4 ✅  
**Pending:** 0

---

*Save this guide for future reference!* 📚  
**Last Updated:** 2026-03-08 22:00 GMT+6

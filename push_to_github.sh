#!/bin/bash
# Git Setup & Push Script for Voice-Controlled Local Agent

set -e

PROJECT_DIR="/Users/mayankchand/Public/voice controlled ai agent"
REPO_URL="https://github.com/Mayankthakuri/voice-control-local-agent.git"

echo "🚀 Voice-Controlled AI Agent - Git Setup & Push"
echo "=================================================="
echo ""

# Step 1: Accept Xcode License (if not already done)
echo "📋 Step 1: Accepting Xcode License Agreement..."
sudo xcodebuild -license accept 2>/dev/null || echo "License already accepted"
echo "✅ License accepted"
echo ""

# Step 2: Navigate to project
echo "📁 Step 2: Navigating to project directory..."
cd "$PROJECT_DIR"
echo "✅ In $PROJECT_DIR"
echo ""

# Step 3: Configure git
echo "⚙️  Step 3: Configuring Git..."
git config --global user.email "mayankchand@gmail.com" || true
git config --global user.name "Mayank Thakur" || true
echo "✅ Git configured"
echo ""

# Step 4: Initialize repository
echo "🔧 Step 4: Initializing Git Repository..."
if [ -d .git ]; then
    echo "Repository already initialized"
else
    git init
    echo "✅ Repository initialized"
fi
echo ""

# Step 5: Add all files
echo "📦 Step 5: Adding files to staging area..."
git add .
echo "✅ Files added"
echo ""

# Step 6: Create .gitignore (if not exists)
echo "🚫 Step 6: Setting up .gitignore..."
if [ ! -f .gitignore ]; then
    cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual Environment
venv/
ENV/
env/

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Environment
.env
.env.local

# API Keys
*.key
*.pem

# Logs
*.log

# Streamlit
.streamlit/
EOF
    echo "✅ .gitignore created"
else
    echo "✅ .gitignore already exists"
fi
echo ""

# Step 7: Commit
echo "📝 Step 7: Creating initial commit..."
git commit -m "🚀 Initial commit: Production-ready Voice-Controlled AI Agent" || echo "Nothing to commit (repository already set up)"
echo "✅ Committed"
echo ""

# Step 8: Add remote
echo "🌐 Step 8: Adding remote repository..."
if git remote get-url origin &> /dev/null; then
    echo "Removing existing remote..."
    git remote remove origin || true
fi
git remote add origin "$REPO_URL"
echo "✅ Remote added: $REPO_URL"
echo ""

# Step 9: Verify connection
echo "🔗 Step 9: Verifying connection to GitHub..."
if git ls-remote --heads "$REPO_URL" &> /dev/null; then
    echo "✅ Connection successful"
else
    echo "⚠️  Could not verify remote (check your GitHub token/SSH key)"
fi
echo ""

# Step 10: Push to GitHub
echo "📤 Step 10: Pushing to GitHub (main branch)..."
git branch -M main
git push -u origin main --force || {
    echo ""
    echo "⚠️  Push failed. Please make sure:"
    echo "  1. You have write access to the repository"
    echo "  2. Your GitHub SSH key is configured (recommended)"
    echo "  3. Or set your GitHub token: git config --global user.token <your_token>"
    echo ""
    echo "Try manually: git push -u origin main"
    exit 1
}
echo "✅ Successfully pushed to GitHub!"
echo ""

echo "=================================================="
echo "🎉 Complete! Repository pushed to GitHub"
echo "📍 Repository: $REPO_URL"
echo "=================================================="
echo ""
echo "Next steps:"
echo "1. Verify your code is on GitHub"
echo "2. Record a 2-3 minute demo video"
echo "3. Write a technical article on Medium/Dev.to"
echo ""

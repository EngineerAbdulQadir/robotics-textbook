#!/bin/bash
# Auto-commit and push script for development workflow
# Usage: ./.specify/scripts/auto-push.sh

echo "🔍 Watching for file changes..."
echo "📁 Watching: .specify/memory/, .claude/, history/"
echo "⚠️  Press Ctrl+C to stop"

while true; do
    # Check if there are changes
    if ! git diff-index --quiet HEAD --; then
        echo ""
        echo "📝 Changes detected! Creating commit..."

        # Get list of changed files
        CHANGED_FILES=$(git diff --name-only)

        # Create commit message based on changed files
        if echo "$CHANGED_FILES" | grep -q "constitution.md"; then
            COMMIT_MSG="docs: update constitution"
        elif echo "$CHANGED_FILES" | grep -q ".claude/"; then
            COMMIT_MSG="feat: update Claude Code skills/agents"
        elif echo "$CHANGED_FILES" | grep -q "history/"; then
            COMMIT_MSG="docs: add prompt history record"
        else
            COMMIT_MSG="chore: auto-commit changes"
        fi

        # Commit and push
        git add .
        git commit -m "$COMMIT_MSG

🤖 Auto-generated commit
Co-Authored-By: Claude <noreply@anthropic.com>"

        echo "🚀 Pushing to GitHub..."
        git push origin main

        echo "✅ Done! Waiting for next change..."
    fi

    # Wait 5 seconds before next check
    sleep 5
done

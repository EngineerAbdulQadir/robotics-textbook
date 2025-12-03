@echo off
REM Auto-commit and push script for Windows
REM Usage: .specify\scripts\auto-push.bat

echo 🔍 Watching for file changes...
echo 📁 Watching: .specify/memory/, .claude/, history/
echo ⚠️  Press Ctrl+C to stop

:loop
git diff-index --quiet HEAD -- >nul 2>&1
if errorlevel 1 (
    echo.
    echo 📝 Changes detected! Creating commit...

    git add .
    git commit -m "chore: auto-commit changes" -m "" -m "🤖 Auto-generated commit" -m "Co-Authored-By: Claude <noreply@anthropic.com>"

    echo 🚀 Pushing to GitHub...
    git push origin main

    echo ✅ Done! Waiting for next change...
)

timeout /t 5 /nobreak >nul
goto loop

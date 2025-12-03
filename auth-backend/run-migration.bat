@echo off
echo Running database migration to fix column names...
echo.

REM Load DATABASE_URL from .env file
for /f "tokens=1,2 delims==" %%a in ('findstr /r "^DATABASE_URL=" .env') do set %%a=%%b

if "%DATABASE_URL%"=="" (
    echo ERROR: DATABASE_URL not found in .env file
    pause
    exit /b 1
)

echo Connecting to database...
psql "%DATABASE_URL%" -f migrations/fix-column-names.sql

echo.
echo Migration complete!
pause

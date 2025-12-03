-- Fix column names in user_profiles table to match the schema
-- Run this migration to fix the mismatch between database and code

-- Rename softwareDevExperience to softwareExperience (if it exists)
DO $$ 
BEGIN
    IF EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'user_profiles' 
        AND column_name = 'softwareDevExperience'
    ) THEN
        ALTER TABLE user_profiles 
        RENAME COLUMN "softwareDevExperience" TO "softwareExperience";
        RAISE NOTICE 'Renamed softwareDevExperience to softwareExperience';
    END IF;
END $$;

-- Add missing columns if they don't exist
DO $$ 
BEGIN
    -- Add hardwareExperience if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'user_profiles' 
        AND column_name = 'hardwareExperience'
    ) THEN
        ALTER TABLE user_profiles 
        ADD COLUMN "hardwareExperience" TEXT;
        RAISE NOTICE 'Added hardwareExperience column';
    END IF;

    -- Add learningGoals if it doesn't exist
    IF NOT EXISTS (
        SELECT 1 
        FROM information_schema.columns 
        WHERE table_name = 'user_profiles' 
        AND column_name = 'learningGoals'
    ) THEN
        ALTER TABLE user_profiles 
        ADD COLUMN "learningGoals" TEXT;
        RAISE NOTICE 'Added learningGoals column';
    END IF;
END $$;

-- Verify the changes
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'user_profiles' 
ORDER BY ordinal_position;

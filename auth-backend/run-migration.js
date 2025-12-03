// Run database migration to fix column names
require('dotenv').config();
const { Client } = require('pg');

async function runMigration() {
  const client = new Client({
    connectionString: process.env.DATABASE_URL,
  });

  try {
    console.log('🔌 Connecting to database...');
    await client.connect();
    console.log('✅ Connected successfully\n');

    console.log('📝 Running migration: Renaming softwareDevExperience to softwareExperience...');
    
    // Check if old column exists
    const checkColumn = await client.query(`
      SELECT column_name 
      FROM information_schema.columns 
      WHERE table_name = 'user_profiles' 
      AND column_name = 'softwareDevExperience'
    `);

    if (checkColumn.rows.length > 0) {
      await client.query(`
        ALTER TABLE user_profiles 
        RENAME COLUMN "softwareDevExperience" TO "softwareExperience"
      `);
      console.log('✅ Renamed softwareDevExperience → softwareExperience');
    } else {
      console.log('ℹ️  Column softwareDevExperience not found (already renamed or doesn\'t exist)');
    }

    // Add hardwareExperience if it doesn't exist
    console.log('\n📝 Checking for hardwareExperience column...');
    const checkHardware = await client.query(`
      SELECT column_name 
      FROM information_schema.columns 
      WHERE table_name = 'user_profiles' 
      AND column_name = 'hardwareExperience'
    `);

    if (checkHardware.rows.length === 0) {
      await client.query(`
        ALTER TABLE user_profiles 
        ADD COLUMN "hardwareExperience" TEXT
      `);
      console.log('✅ Added hardwareExperience column');
    } else {
      console.log('ℹ️  hardwareExperience column already exists');
    }

    // Add learningGoals if it doesn't exist
    console.log('\n📝 Checking for learningGoals column...');
    const checkGoals = await client.query(`
      SELECT column_name 
      FROM information_schema.columns 
      WHERE table_name = 'user_profiles' 
      AND column_name = 'learningGoals'
    `);

    if (checkGoals.rows.length === 0) {
      await client.query(`
        ALTER TABLE user_profiles 
        ADD COLUMN "learningGoals" TEXT
      `);
      console.log('✅ Added learningGoals column');
    } else {
      console.log('ℹ️  learningGoals column already exists');
    }

    // Show current schema
    console.log('\n📋 Current user_profiles columns:');
    const columns = await client.query(`
      SELECT column_name, data_type 
      FROM information_schema.columns 
      WHERE table_name = 'user_profiles' 
      ORDER BY ordinal_position
    `);
    
    columns.rows.forEach(row => {
      console.log(`   - ${row.column_name} (${row.data_type})`);
    });

    console.log('\n✅ Migration completed successfully!');
    console.log('🔄 You can now restart the backend server and try personalization again.');

  } catch (error) {
    console.error('❌ Migration failed:', error.message);
    console.error('\nFull error:', error);
    process.exit(1);
  } finally {
    await client.end();
  }
}

runMigration();

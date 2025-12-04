const postgres = require('postgres');
const fs = require('fs');
const path = require('path');

async function runMigration() {
  // Get DATABASE_URL from environment or command line
  const databaseUrl = process.env.DATABASE_URL;
  
  if (!databaseUrl) {
    console.error('❌ DATABASE_URL environment variable is required');
    process.exit(1);
  }

  console.log('🔗 Connecting to database...');
  const sql = postgres(databaseUrl);

  try {
    // Read the migration file
    const migrationPath = path.join(__dirname, 'migrations', 'final-schema.sql');
    const migrationSQL = fs.readFileSync(migrationPath, 'utf8');

    console.log('📝 Running migration...');
    
    // Split by semicolons and execute each statement
    const statements = migrationSQL
      .split(';')
      .map(s => s.trim())
      .filter(s => s.length > 0 && !s.startsWith('--'));

    for (const statement of statements) {
      try {
        await sql.unsafe(statement);
        console.log('✅ Executed:', statement.substring(0, 50) + '...');
      } catch (error) {
        // Ignore "already exists" errors
        if (error.code === '42P07' || error.message.includes('already exists')) {
          console.log('⚠️  Already exists:', statement.substring(0, 50) + '...');
        } else {
          throw error;
        }
      }
    }

    console.log('✅ Migration completed successfully!');
  } catch (error) {
    console.error('❌ Migration failed:', error);
    process.exit(1);
  } finally {
    await sql.end();
  }
}

runMigration();

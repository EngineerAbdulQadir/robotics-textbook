// Clear all data from auth backend database
const postgres = require('postgres');

const DATABASE_URL = process.env.DATABASE_URL || 'postgresql://postgres:oxLiBesIUfHEJapomWgifCUBvWCJiayR@crossover.proxy.rlwy.net:21831/railway';

const sql = postgres(DATABASE_URL);

async function clearAllData() {
  console.log('🗑️  Clearing all data from auth backend database...');
  
  try {
    // Delete in correct order due to foreign key constraints
    console.log('   - Deleting user profiles...');
    await sql`DELETE FROM user_profiles`;
    
    console.log('   - Deleting sessions...');
    await sql`DELETE FROM sessions`;
    
    console.log('   - Deleting accounts...');
    await sql`DELETE FROM accounts`;
    
    console.log('   - Deleting verification records...');
    await sql`DELETE FROM verification`;
    
    console.log('   - Deleting users...');
    await sql`DELETE FROM users`;
    
    console.log('✅ All data cleared successfully!');
    
  } catch (error) {
    console.error('❌ Error clearing data:', error);
  } finally {
    await sql.end();
  }
}

clearAllData();

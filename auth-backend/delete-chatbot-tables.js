// Delete chatbot tables from auth-backend database
const postgres = require('postgres');

const DATABASE_URL = 'postgresql://postgres:oxLiBesIUfHEJapomWgifCUBvWCJiayR@crossover.proxy.rlwy.net:21831/railway';

const sql = postgres(DATABASE_URL);

async function deleteTables() {
  console.log('🔗 Connecting to Railway database...');
  
  try {
    console.log('🗑️  Dropping citations table...');
    await sql`DROP TABLE IF EXISTS citations CASCADE`;
    
    console.log('🗑️  Dropping textbook_content table...');
    await sql`DROP TABLE IF EXISTS textbook_content CASCADE`;
    
    console.log('🗑️  Dropping messages table...');
    await sql`DROP TABLE IF EXISTS messages CASCADE`;
    
    console.log('🗑️  Dropping conversations table...');
    await sql`DROP TABLE IF EXISTS conversations CASCADE`;
    
    console.log('🗑️  Dropping user_sessions table...');
    await sql`DROP TABLE IF EXISTS user_sessions CASCADE`;
    
    console.log('🗑️  Dropping message_role enum...');
    await sql`DROP TYPE IF EXISTS message_role CASCADE`;
    
    console.log('✅ All chatbot tables deleted successfully!');
    console.log('📋 Remaining tables are only for auth-backend (users, sessions, accounts, verification, user_profiles)');
  } catch (error) {
    console.error('❌ Error:', error);
  } finally {
    await sql.end();
    console.log('👋 Connection closed');
  }
}

deleteTables();

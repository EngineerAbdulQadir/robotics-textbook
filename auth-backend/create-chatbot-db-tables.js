// Create chatbot backend tables on NEW Railway PostgreSQL
const postgres = require('postgres');

// New chatbot database URL
const DATABASE_URL = 'postgresql://postgres:xTFRiSwzocovjJQvkJFUYbuUmUasVTmY@trolley.proxy.rlwy.net:25757/railway';

const sql = postgres(DATABASE_URL);

async function createTables() {
  console.log('🔗 Connecting to NEW chatbot Railway database...');
  
  try {
    // Create message_role enum
    console.log('📝 Creating message_role enum...');
    await sql`
      DO $$ BEGIN
        CREATE TYPE message_role AS ENUM ('user', 'assistant');
      EXCEPTION
        WHEN duplicate_object THEN null;
      END $$;
    `;

    // Create user_sessions table
    console.log('📝 Creating user_sessions table...');
    await sql`
      CREATE TABLE IF NOT EXISTS user_sessions (
        session_id UUID PRIMARY KEY,
        anonymous_browser_id VARCHAR(255),
        user_id UUID,
        page_context VARCHAR(500),
        conversation_ids JSON DEFAULT '[]',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NOT NULL
      )
    `;
    await sql`CREATE INDEX IF NOT EXISTS ix_user_sessions_session_id ON user_sessions(session_id)`;
    await sql`CREATE INDEX IF NOT EXISTS ix_user_sessions_user_id ON user_sessions(user_id)`;
    await sql`CREATE INDEX IF NOT EXISTS ix_user_sessions_expires_at ON user_sessions(expires_at)`;

    // Create conversations table
    console.log('📝 Creating conversations table...');
    await sql`
      CREATE TABLE IF NOT EXISTS conversations (
        id UUID PRIMARY KEY,
        user_session_id UUID NOT NULL,
        page_context VARCHAR(500),
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NOT NULL,
        FOREIGN KEY (user_session_id) REFERENCES user_sessions(session_id) ON DELETE CASCADE
      )
    `;
    await sql`CREATE INDEX IF NOT EXISTS ix_conversations_user_session_id ON conversations(user_session_id)`;
    await sql`CREATE INDEX IF NOT EXISTS ix_conversations_created_at ON conversations(created_at)`;
    await sql`CREATE INDEX IF NOT EXISTS ix_conversations_expires_at ON conversations(expires_at)`;

    // Create messages table
    console.log('📝 Creating messages table...');
    await sql`
      CREATE TABLE IF NOT EXISTS messages (
        id UUID PRIMARY KEY,
        conversation_id UUID NOT NULL,
        role message_role NOT NULL,
        content TEXT NOT NULL,
        source_references JSON DEFAULT '[]',
        timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        expires_at TIMESTAMP NOT NULL,
        FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
      )
    `;
    await sql`CREATE INDEX IF NOT EXISTS ix_messages_conversation_id ON messages(conversation_id)`;
    await sql`CREATE INDEX IF NOT EXISTS ix_messages_timestamp ON messages(timestamp)`;
    await sql`CREATE INDEX IF NOT EXISTS ix_messages_expires_at ON messages(expires_at)`;

    // Create textbook_content table
    console.log('📝 Creating textbook_content table...');
    await sql`
      CREATE TABLE IF NOT EXISTS textbook_content (
        id UUID PRIMARY KEY,
        chapter VARCHAR(500) NOT NULL,
        section VARCHAR(500) NOT NULL,
        content_text TEXT NOT NULL,
        vector_embedding_id VARCHAR(255),
        metadata JSON DEFAULT '{}',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
      )
    `;
    await sql`CREATE INDEX IF NOT EXISTS ix_textbook_content_chapter ON textbook_content(chapter)`;
    await sql`CREATE INDEX IF NOT EXISTS ix_textbook_content_section ON textbook_content(section)`;

    // Create citations table
    console.log('📝 Creating citations table...');
    await sql`
      CREATE TABLE IF NOT EXISTS citations (
        id UUID PRIMARY KEY,
        message_id UUID NOT NULL,
        chapter VARCHAR(500) NOT NULL,
        section VARCHAR(500) NOT NULL,
        content_excerpt TEXT NOT NULL,
        link VARCHAR(1000),
        confidence_score FLOAT DEFAULT 0.0,
        expires_at TIMESTAMP NOT NULL,
        FOREIGN KEY (message_id) REFERENCES messages(id) ON DELETE CASCADE
      )
    `;
    await sql`CREATE INDEX IF NOT EXISTS ix_citations_message_id ON citations(message_id)`;
    await sql`CREATE INDEX IF NOT EXISTS ix_citations_expires_at ON citations(expires_at)`;

    console.log('✅ All chatbot tables created successfully in NEW database!');
    console.log('🎉 Chatbot database is ready to use!');
  } catch (error) {
    console.error('❌ Error creating tables:', error);
  } finally {
    await sql.end();
    console.log('👋 Connection closed');
  }
}

createTables();

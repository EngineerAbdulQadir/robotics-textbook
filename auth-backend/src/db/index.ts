import { drizzle } from "drizzle-orm/postgres-js";
import postgres from "postgres";
import * as schema from "./schema";

const connectionString = process.env.DATABASE_URL;

// Create the postgres client - postgres.js handles connection lazily
// so this won't throw even if DATABASE_URL is missing
const client = postgres(connectionString || "");

export const db = drizzle(client, { schema });

export type Database = typeof db;

export async function validateDatabaseConnection(): Promise<boolean> {
  try {
    if (!connectionString) {
      console.error("DATABASE_URL environment variable is not set");
      return false;
    }
    // Test the connection by running a simple query
    await db.execute("SELECT NOW()");
    console.log("✅ Database connection successful");
    return true;
  } catch (error) {
    console.error("❌ Database connection failed:", error);
    return false;
  }
}

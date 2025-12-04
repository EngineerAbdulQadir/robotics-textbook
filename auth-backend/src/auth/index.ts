import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "../db";
import * as schema from "../db/schema";

let authInstance: ReturnType<typeof betterAuth> | null = null;

function getAuth() {
  if (!authInstance) {
    authInstance = betterAuth({
      database: drizzleAdapter(db, {
        provider: "pg",
        schema: {
          user: schema.users,
          session: schema.sessions,
          account: schema.accounts,
          verification: schema.verification,
        },
      }),
      secret: process.env.BETTER_AUTH_SECRET || "default-secret-change-me",
      emailAndPassword: {
        enabled: true,
        requireEmailVerification: false,
      },
      socialProviders: {
        github: {
          clientId: process.env.GITHUB_CLIENT_ID || "",
          clientSecret: process.env.GITHUB_CLIENT_SECRET || "",
        },
        google: {
          clientId: process.env.GOOGLE_CLIENT_ID || "",
          clientSecret: process.env.GOOGLE_CLIENT_SECRET || "",
        },
      },
      databaseHooks: {
        user: {
          create: {
            after: async (user) => {
              try {
                console.log("🎯 Creating profile for new user:", user.id);
                const profileId = `profile_${user.id}`;
                
                await db.insert(schema.userProfiles).values({
                  id: profileId,
                  userId: user.id,
                  softwareExperience: null,
                  hardwareExperience: null,
                  programmingLanguages: [],
                  roboticsBackground: null,
                  learningGoals: null,
                  preferredLanguage: "en",
                });
                console.log(`✅ Profile created for user ${user.id}`);
              } catch (error) {
                console.error("❌ Failed to create user profile:", error);
              }
            },
          },
        },
      },
      plugins: [],
      trustedOrigins: [
        process.env.FRONTEND_URL || "http://localhost:3000",
        "http://localhost:3000",
        "http://localhost:5173", // Vite default
        "http://localhost:8080", // HTTP server for test-client
      ],
    });
  }
  return authInstance;
}

// Export auth instance directly
export const auth = getAuth();

export const createAuthHandler = () => auth.handler;

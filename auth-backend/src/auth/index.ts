import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { db } from "../db";
import * as schema from "../db/schema";
import { eq } from "drizzle-orm";

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
      plugins: [
        {
          id: "user-profile-creator",
          hooks: {
            after: [
              {
                matcher: (context: any) => {
                  return context.path === "/sign-up/email" && context.method === "POST";
                },
                handler: async (context: any) => {
                  try {
                    console.log("🎯 Profile creation hook triggered!");
                    
                    // According to Better Auth docs, user data is in context.context.newSession
                    const newSession = context.context?.newSession;
                    const userId = newSession?.user?.id;
                    
                    console.log(`   - New session exists: ${!!newSession}`);
                    console.log(`   - User ID: ${userId}`);
                    
                    if (userId) {
                      const profileId = `profile_${userId}`;
                      console.log(`   - Creating profile with ID: ${profileId}`);
                      
                      // Create default user profile
                      await db.insert(schema.userProfiles).values({
                        id: profileId,
                        userId: userId,
                        softwareExperience: null,
                        hardwareExperience: null,
                        programmingLanguages: [],
                        roboticsBackground: null,
                        learningGoals: null,
                        preferredLanguage: "en",
                      });
                      console.log(`✅ Profile created successfully for user ${userId}`);
                    } else {
                      console.log("   - ⚠️ No userId found - user might not have been created yet");
                    }
                  } catch (error) {
                    console.error("❌ Failed to create user profile:", error);
                  }
                },
              },
            ],
          },
        },
      ],
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

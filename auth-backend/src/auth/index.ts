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
                    console.log("   - Path:", context.path);
                    console.log("   - Method:", context.method);
                    
                    // The returned value contains the response from signup
                    // It should have the user object with id
                    let userId;
                    
                    console.log(`   - context.returned:`, context.returned);
                    console.log(`   - typeof context.returned:`, typeof context.returned);
                    
                    if (context.returned) {
                      console.log(`   - Returned keys:`, Object.keys(context.returned));
                      // Try to access user from returned response
                      userId = context.returned.user?.id || context.returned.id;
                      console.log(`   - User from returned:`, context.returned.user);
                    }
                    
                    console.log(`   - Extracted userId: ${userId}`);
                    
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
                      console.log(`✅ Created profile for user ${userId}`);
                      
                      // Verify it was created
                      const [createdProfile] = await db.select().from(schema.userProfiles).where(eq(schema.userProfiles.userId, userId)).limit(1);
                      console.log(`   - Verification: Profile ${createdProfile ? 'EXISTS' : 'NOT FOUND'}`);
                    } else {
                      console.error("   - ❌ No userId found in context");
                      console.error("   - Available context structure:", {
                        hasContext: !!context.context,
                        hasUser: !!context.user,
                        hasReturned: !!context.returned,
                        hasBody: !!context.body
                      });
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

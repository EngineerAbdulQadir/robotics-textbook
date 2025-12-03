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
      plugins: [
        // Temporarily disabled - profiles will be created via the sign-up form data
        // {
        //   id: "user-profile-creator",
        //   hooks: {
        //     after: [
        //       {
        //         matcher: (context: any) => {
        //           return context.path === "/sign-up/email" && context.method === "POST";
        //         },
        //         handler: async (context: any) => {
        //           // Profile creation logic here
        //         },
        //       },
        //     ],
        //   },
        // },
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

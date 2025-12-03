import { pgTable, text, timestamp, boolean, jsonb } from "drizzle-orm/pg-core";

// Users table - Better Auth compatible
export const users = pgTable("users", {
  id: text("id").primaryKey(),
  name: text("name"),
  email: text("email").notNull().unique(),
  emailVerified: boolean("emailVerified").default(false),
  image: text("image"),
  createdAt: timestamp("createdAt").defaultNow(),
  updatedAt: timestamp("updatedAt").defaultNow(),
});

// User profiles - for personalization (custom table)
export const userProfiles = pgTable("user_profiles", {
  id: text("id").primaryKey(),
  userId: text("userId").notNull().references(() => users.id, { onDelete: "cascade" }).unique(),
  // Background information
  softwareExperience: text("softwareExperience"), // none, beginner, intermediate, advanced, professional
  hardwareExperience: text("hardwareExperience"), // none, hobbyist, academic, professional
  programmingLanguages: jsonb("programmingLanguages").$type<string[]>(), // Array of languages
  roboticsBackground: text("roboticsBackground"), // none, courses, projects, research, industry
  learningGoals: text("learningGoals"), // Free text
  // Preferences
  preferredLanguage: text("preferredLanguage").default("en"),
  contentPreferences: jsonb("contentPreferences"),
  createdAt: timestamp("createdAt").defaultNow(),
  updatedAt: timestamp("updatedAt").defaultNow(),
});

// Sessions table - Better Auth compatible
export const sessions = pgTable("sessions", {
  id: text("id").primaryKey(),
  userId: text("userId").notNull().references(() => users.id, { onDelete: "cascade" }),
  expiresAt: timestamp("expiresAt").notNull(),
  token: text("token").notNull().unique(),
  ipAddress: text("ipAddress"),
  userAgent: text("userAgent"),
  createdAt: timestamp("createdAt").defaultNow(),
  updatedAt: timestamp("updatedAt").defaultNow(),
});

// Verification table - Better Auth compatible
export const verification = pgTable("verification", {
  id: text("id").primaryKey(),
  identifier: text("identifier").notNull(),
  value: text("value").notNull(),
  expiresAt: timestamp("expiresAt").notNull(),
  createdAt: timestamp("createdAt").defaultNow(),
  updatedAt: timestamp("updatedAt").defaultNow(),
});

// Accounts table - Better Auth compatible (for OAuth and password)
export const accounts = pgTable("accounts", {
  id: text("id").primaryKey(),
  accountId: text("accountId").notNull(),
  providerId: text("providerId").notNull(),
  userId: text("userId").notNull().references(() => users.id, { onDelete: "cascade" }),
  accessToken: text("accessToken"),
  refreshToken: text("refreshToken"),
  idToken: text("idToken"),
  accessTokenExpiresAt: timestamp("accessTokenExpiresAt"),
  refreshTokenExpiresAt: timestamp("refreshTokenExpiresAt"),
  scope: text("scope"),
  password: text("password"),
  createdAt: timestamp("createdAt").defaultNow(),
  updatedAt: timestamp("updatedAt").defaultNow(),
});

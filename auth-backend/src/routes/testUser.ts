import { Router, Request, Response } from "express";
import { db } from "../db";
import { users, userProfiles } from "../db/schema";
import { eq } from "drizzle-orm";
import crypto from "crypto";

const router = Router();

// Test endpoint to create a user with profile
router.post("/create-test-user", async (_req: Request, res: Response): Promise<void> => {
  try {
    console.log("🧪 Creating test user...");
    
    const testEmail = `test${Date.now()}@example.com`;
    const testUserId = crypto.randomUUID();
    const testProfileId = `profile_${testUserId}`;
    
    // Create user
    await db.insert(users).values({
      id: testUserId,
      email: testEmail,
      name: "Test User",
      emailVerified: true,
      createdAt: new Date(),
      updatedAt: new Date(),
    });
    
    console.log(`✅ Created test user: ${testEmail}`);
    
    // Create profile
    await db.insert(userProfiles).values({
      id: testProfileId,
      userId: testUserId,
      softwareExperience: "intermediate",
      hardwareExperience: "beginner",
      programmingLanguages: ["Python", "JavaScript"],
      roboticsBackground: "courses",
      learningGoals: "Learn ROS 2 and build robots",
      preferredLanguage: "en",
      createdAt: new Date(),
      updatedAt: new Date(),
    });
    
    console.log(`✅ Created test profile for user`);
    
    res.status(201).json({
      success: true,
      user: {
        id: testUserId,
        email: testEmail,
        name: "Test User",
      },
      message: "Test user created successfully. Use this email to sign in (no password needed for testing)."
    });
    
  } catch (error) {
    console.error("❌ Error creating test user:", error);
    res.status(500).json({ 
      error: "Failed to create test user",
      details: error instanceof Error ? error.message : String(error)
    });
  }
});

// Delete all test users (cleanup)
router.delete("/delete-test-users", async (_req: Request, res: Response): Promise<void> => {
  try {
    console.log("🧹 Deleting test users...");
    
    // Delete users with test emails
    const deletedUsers = await db
      .delete(users)
      .where(eq(users.email, "test@example.com"))
      .returning();
    
    console.log(`✅ Deleted ${deletedUsers.length} test users`);
    
    res.json({
      success: true,
      deleted: deletedUsers.length,
      message: "Test users deleted successfully"
    });
    
  } catch (error) {
    console.error("❌ Error deleting test users:", error);
    res.status(500).json({ 
      error: "Failed to delete test users",
      details: error instanceof Error ? error.message : String(error)
    });
  }
});

export const testUserRoutes = router;

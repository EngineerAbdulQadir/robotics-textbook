import { db } from "./index";
import { userProfiles } from "./schema";
import { eq } from "drizzle-orm";

export async function setupUserProfileSchema() {
  // This is handled by Drizzle migrations
  // This function can be used for any runtime initialization
  try {
    console.log("User profile schema initialized");
  } catch (error) {
    console.error("Error setting up user profile schema:", error);
    throw error;
  }
}

export async function createUserProfile(userId: string, data: Partial<typeof userProfiles.$inferInsert>) {
  try {
    // Generate a unique ID for the profile
    const profileId = `profile_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`;
    
    const result = await db
      .insert(userProfiles)
      .values({
        id: profileId,
        userId,
        ...data,
      })
      .returning();
    return result[0];
  } catch (error) {
    console.error("Error creating user profile:", error);
    throw error;
  }
}

export async function getUserProfile(userId: string) {
  try {
    const profile = await db
      .select()
      .from(userProfiles)
      .where(eq(userProfiles.userId, userId))
      .limit(1);
    return profile[0] || null;
  } catch (error) {
    console.error("Error fetching user profile:", error);
    throw error;
  }
}

export async function updateUserProfile(userId: string, data: Partial<typeof userProfiles.$inferInsert>) {
  try {
    const result = await db
      .update(userProfiles)
      .set({
        ...data,
        updatedAt: new Date(),
      })
      .where(eq(userProfiles.userId, userId))
      .returning();
    return result[0];
  } catch (error) {
    console.error("Error updating user profile:", error);
    throw error;
  }
}

export async function deleteUserProfile(userId: string) {
  try {
    await db
      .delete(userProfiles)
      .where(eq(userProfiles.userId, userId));
  } catch (error) {
    console.error("Error deleting user profile:", error);
    throw error;
  }
}

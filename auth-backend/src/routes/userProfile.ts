import { Router, Request, Response } from "express";
import { auth } from "../auth";
import {
  createUserProfile,
  getUserProfile,
  updateUserProfile,
} from "../db/userProfileSchema";

export const userProfileRoutes = Router();

// Middleware to verify authentication
const requireAuth = async (req: Request, res: Response, next: Function): Promise<void> => {
  try {
    const session = await auth.api.getSession({ headers: req.headers as any });
    if (!session) {
      res.status(401).json({ error: "Unauthorized" });
      return;
    }
    (req as any).user = session.user;
    next();
  } catch (error) {
    res.status(401).json({ error: "Unauthorized" });
  }
};

// Get user profile
userProfileRoutes.get("/profile", requireAuth, async (req: Request, res: Response): Promise<void> => {
  try {
    const userId = (req as any).user.id;
    const profile = await getUserProfile(userId);

    if (!profile) {
      res.status(404).json({ error: "Profile not found" });
      return;
    }

    res.json(profile);
  } catch (error) {
    console.error("Error fetching profile:", error);
    res.status(500).json({ error: "Failed to fetch profile" });
  }
});

// Update user profile
userProfileRoutes.put("/profile", requireAuth, async (req: Request, res: Response): Promise<void> => {
  try {
    const userId = (req as any).user.id;
    const {
      softwareExperience,
      hardwareExperience,
      roboticsBackground,
      programmingLanguages,
      learningGoals,
      preferredLanguage,
      contentPreferences,
    } = req.body;

    const profile = await updateUserProfile(userId, {
      softwareExperience,
      hardwareExperience,
      roboticsBackground,
      programmingLanguages,
      learningGoals,
      preferredLanguage,
      contentPreferences,
    });

    res.json(profile);
  } catch (error) {
    console.error("Error updating profile:", error);
    res.status(500).json({ error: "Failed to update profile" });
  }
});

// Initialize profile on signup
userProfileRoutes.post("/profile/init", requireAuth, async (req: Request, res: Response): Promise<void> => {
  try {
    const userId = (req as any).user.id;
    const existingProfile = await getUserProfile(userId);

    if (existingProfile) {
      res.status(400).json({ error: "Profile already initialized" });
      return;
    }

    const {
      softwareExperience,
      hardwareExperience,
      roboticsBackground,
      programmingLanguages,
      learningGoals,
    } = req.body;

    const profile = await createUserProfile(userId, {
      softwareExperience: softwareExperience || "beginner",
      hardwareExperience: hardwareExperience || "none",
      roboticsBackground: roboticsBackground || "none",
      programmingLanguages: programmingLanguages || [],
      learningGoals: learningGoals || null,
    });

    res.status(201).json(profile);
  } catch (error) {
    console.error("Error initializing profile:", error);
    res.status(500).json({ error: "Failed to initialize profile" });
  }
});

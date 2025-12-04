import { Router, Request, Response } from "express";
import { db } from "../db";
import { users, userProfiles } from "../db/schema";
import { eq } from "drizzle-orm";

const router = Router();

// Personalize content endpoint
router.post("/personalize-content", async (req: Request, res: Response): Promise<void> => {
  try {
    console.log("📝 Personalization request received");
    const { userId, chapterTitle, chapterContent } = req.body;

    console.log(`   - User ID: ${userId}`);
    console.log(`   - Chapter: ${chapterTitle}`);
    console.log(`   - Content length: ${chapterContent?.length || 0} chars`);

    if (!userId || !chapterTitle || !chapterContent) {
      console.error("❌ Missing required fields");
      res.status(400).json({ 
        error: "Missing required fields: userId, chapterTitle, chapterContent" 
      });
      return;
    }

    // Get user profile data
    console.log("🔍 Fetching user profile...");
    console.log(`   - Looking for userId: ${userId}`);
    
    const [userProfileData] = await db
      .select()
      .from(userProfiles)
      .where(eq(userProfiles.userId, userId))
      .limit(1);

    console.log(`   - Query result:`, userProfileData ? 'Found' : 'Not found');
    
    if (!userProfileData) {
      // Check if ANY profiles exist
      const allProfiles = await db.select().from(userProfiles).limit(5);
      console.error(`❌ User profile not found for userId: ${userId}`);
      console.error(`   - Total profiles in DB: ${allProfiles.length}`);
      if (allProfiles.length > 0) {
        console.error(`   - Sample profile userIds:`, allProfiles.map(p => p.userId));
      }
      
      res.status(404).json({ 
        error: "User profile not found. Please complete your profile first." 
      });
      return;
    }

    console.log("✅ Profile found:", {
      id: userProfileData.id,
      userId: userProfileData.userId,
      softwareExperience: userProfileData.softwareExperience
    });

    // Get user basic info
    const [userData] = await db
      .select()
      .from(users)
      .where(eq(users.id, userId))
      .limit(1);

    console.log("🎨 Generating personalized content...");

    // Generate personalized content based on user profile
    const personalizedContent = generatePersonalizedContent(
      chapterTitle,
      chapterContent,
      {
        name: userData?.name || "User",
        softwareExperience: userProfileData.softwareExperience,
        hardwareExperience: userProfileData.hardwareExperience,
        programmingLanguages: userProfileData.programmingLanguages,
        roboticsBackground: userProfileData.roboticsBackground,
        learningGoals: userProfileData.learningGoals,
      }
    );

    console.log("✅ Personalization successful");

    res.json({
      success: true,
      personalizedContent,
      message: "Content personalized successfully",
    });
  } catch (error) {
    console.error("Personalization error:", error);
    res.status(500).json({ 
      error: "Failed to personalize content",
      details: error instanceof Error ? error.message : "Unknown error"
    });
  }
});

// Helper function to generate personalized content
function generatePersonalizedContent(
  chapterTitle: string,
  chapterContent: string,
  profile: {
    name: string;
    softwareExperience: string | null;
    hardwareExperience: string | null;
    programmingLanguages: string[] | null;
    roboticsBackground: string | null;
    learningGoals: string | null;
  }
): string {
  // Extract experience level
  const experienceLevel = profile.softwareExperience || "beginner";
  const roboticsExp = profile.roboticsBackground || "none";
  const languages = profile.programmingLanguages || [];

  // Create personalized introduction
  let personalizedHTML = `
    <div class="personalized-intro">
      <h2>📚 ${chapterTitle} - Personalized for ${profile.name}</h2>
      <div class="profile-summary">
        <p><strong>Your Learning Profile:</strong></p>
        <ul>
          <li>Software Experience: <strong>${formatExperience(experienceLevel)}</strong></li>
          <li>Robotics Background: <strong>${formatRoboticsBackground(roboticsExp)}</strong></li>
          ${languages.length > 0 ? `<li>Programming Languages: <strong>${languages.join(", ")}</strong></li>` : ''}
        </ul>
      </div>
    </div>
  `;

  // Add experience-appropriate content adjustments
  if (experienceLevel === "none" || experienceLevel === "beginner") {
    personalizedHTML += `
      <div class="beginner-tips">
        <h3>🌟 Getting Started Tips</h3>
        <p>Since you're new to software development, we'll focus on fundamental concepts and provide extra explanations for technical terms.</p>
        <ul>
          <li>Take your time with each concept</li>
          <li>Don't hesitate to review prerequisite materials</li>
          <li>Practice with simple examples before moving to complex ones</li>
        </ul>
      </div>
    `;
  } else if (experienceLevel === "professional" || experienceLevel === "advanced") {
    personalizedHTML += `
      <div class="advanced-tips">
        <h3>🚀 Advanced Focus Areas</h3>
        <p>With your ${formatExperience(experienceLevel)} experience, we'll emphasize advanced concepts, optimization techniques, and real-world applications.</p>
        <ul>
          <li>Focus on architectural patterns and best practices</li>
          <li>Explore performance optimization opportunities</li>
          <li>Consider scalability and production deployment</li>
        </ul>
      </div>
    `;
  }

  // Add robotics-specific guidance
  if (roboticsExp === "none") {
    personalizedHTML += `
      <div class="robotics-intro">
        <h3>🤖 Robotics Fundamentals</h3>
        <p>New to robotics? We'll start with the basics and build your understanding step by step.</p>
        <ul>
          <li>Learn core robotics concepts from scratch</li>
          <li>Understand how software controls physical systems</li>
          <li>Build intuition about sensors and actuators</li>
        </ul>
      </div>
    `;
  } else if (roboticsExp === "industry" || roboticsExp === "research") {
    personalizedHTML += `
      <div class="robotics-advanced">
        <h3>🔬 Advanced Robotics Applications</h3>
        <p>Leveraging your ${formatRoboticsBackground(roboticsExp)} experience, we'll dive into cutting-edge techniques and industry standards.</p>
        <ul>
          <li>Explore state-of-the-art algorithms and approaches</li>
          <li>Compare with industry best practices</li>
          <li>Consider real-world deployment challenges</li>
        </ul>
      </div>
    `;
  }

  // Add programming language specific tips
  if (languages.includes("Python")) {
    personalizedHTML += `
      <div class="language-tips">
        <h3>🐍 Python-Specific Resources</h3>
        <p>Since you know Python, you'll find many examples in this familiar language. We'll highlight Python-specific libraries and tools relevant to this chapter.</p>
      </div>
    `;
  }

  if (languages.includes("C++")) {
    personalizedHTML += `
      <div class="language-tips">
        <h3>⚡ C++ Performance Insights</h3>
        <p>With your C++ knowledge, we'll point out performance-critical sections and low-level implementation details that matter for robotics applications.</p>
      </div>
    `;
  }

  // Add learning goals alignment
  if (profile.learningGoals) {
    personalizedHTML += `
      <div class="goals-alignment">
        <h3>🎯 Aligned with Your Goals</h3>
        <p>Your learning goal: <em>"${profile.learningGoals}"</em></p>
        <p>This chapter will help you progress toward this goal by providing relevant examples and exercises.</p>
      </div>
    `;
  }

  // Add recommended next steps
  personalizedHTML += `
    <div class="next-steps">
      <h3>📖 Chapter Content</h3>
      <p>The following content has been contextualized based on your profile. Key concepts are highlighted, and examples are tailored to your experience level.</p>
      <hr style="margin: 20px 0; border: 1px solid #e2e8f0;" />
    </div>
  `;

  // Add a simplified version of the original content
  // In a real implementation, you would use an LLM API here
  personalizedHTML += `
    <div class="chapter-content">
      ${generateSimplifiedContent(chapterContent, experienceLevel)}
    </div>
  `;

  return personalizedHTML;
}

function generateSimplifiedContent(_content: string, experienceLevel: string): string {
  if (experienceLevel === "none" || experienceLevel === "beginner") {
    return `
      <p><strong>Simplified Overview:</strong></p>
      <p>This chapter covers important concepts that we'll break down into easy-to-understand pieces. Each section includes:</p>
      <ul>
        <li>Clear definitions of technical terms</li>
        <li>Step-by-step explanations</li>
        <li>Practical examples you can try</li>
        <li>Visual diagrams to aid understanding</li>
      </ul>
      <p><em>Note: In a full implementation, this would be the complete chapter content adapted to your level using AI.</em></p>
    `;
  } else {
    return `
      <p><strong>Advanced Overview:</strong></p>
      <p>This chapter explores advanced topics with a focus on:</p>
      <ul>
        <li>Technical depth and implementation details</li>
        <li>Performance considerations and optimizations</li>
        <li>Real-world applications and case studies</li>
        <li>Best practices and design patterns</li>
      </ul>
      <p><em>Note: In a full implementation, this would be the complete chapter content with advanced insights using AI.</em></p>
    `;
  }
}

function formatExperience(exp: string): string {
  const map: Record<string, string> = {
    none: "No Experience",
    beginner: "Beginner (< 1 year)",
    intermediate: "Intermediate (1-3 years)",
    advanced: "Advanced (3+ years)",
    professional: "Professional (5+ years)",
  };
  return map[exp] || exp;
}

function formatRoboticsBackground(bg: string): string {
  const map: Record<string, string> = {
    none: "No Robotics Experience",
    hobbyist: "Hobbyist/DIY Projects",
    academic: "Academic/Research",
    professional: "Professional/Industry",
    courses: "Completed Robotics Courses",
    projects: "Personal/Hobby Projects",
    research: "Research Experience",
    industry: "Industry Experience",
  };
  return map[bg] || bg;
}

export { router as personalizationRoutes };

---
name: ai-collaborate-teaching
category: "pedagogical"
applies_to: ["all-chapters"]
required_for: ["content-implementer", "chapter-planner"]
description: |
  Transform programming education by treating AI as a collaborative learning partner rather than 
  a code-completion tool. This skill guides educators in creating curriculum where students learn 
  to orchestrate AI systems through clear specifications, engage in bidirectional learning (teaching 
  AI while learning from it), and develop critical verification skills. Emphasizes the Three Roles 
  Framework where both human and AI act as teacher, student, and collaborator. Prepares students 
  for AI-native development workflows while maintaining independent capability and ethical practices.
version: "2.1.0"
dependencies: ["constitution:v4.0.1"]
---

# AI Collaborative Teaching: A Partnership Approach

## The Big Picture

**Traditional coding education is becoming obsolete.** Students who learn only syntax and algorithms without AI collaboration skills will struggle in modern development environments. But students who rely entirely on AI without understanding fundamentals will be equally lost.

This skill helps you navigate that tension by designing curriculum where:
- **Specifications become the primary skill** (not memorizing syntax)
- **AI acts as a true partner** (not a magic code generator)
- **Students learn bidirectionally** (teaching AI while learning from it)
- **Verification is non-negotiable** (trust, but always verify)
- **Ethics are embedded** (not an afterthought)

Think of it this way: You're teaching students to be **AI orchestrators**, not AI users or AI avoiders.

## The Three Roles Framework: A Dance, Not a Command

**Here's what most educators get wrong:** They think AI is either a teacher (students passively receive answers) or a tool (students command it to generate code). Both miss the point.

**The reality:** Effective AI collaboration is a dynamic dance where both partners switch roles fluidly.

### Scenario: Building a REST API Client

Imagine a student named Maya learning to integrate a weather API:

**Round 1 - Human as Teacher, AI as Student:**
- Maya: "I need to fetch weather data for San Francisco. The API requires an API key in the header and returns JSON."
- AI learns Maya's requirements, domain context, and constraints

**Round 2 - AI as Teacher, Human as Student:**
- AI: "Here's a basic implementation. I've also added retry logic with exponential backoff—APIs can be flaky."
- Maya: "Wait, what's exponential backoff?" (She learns a new pattern)

**Round 3 - Both as Co-Workers:**
- Maya: "Good idea, but I need to handle rate limiting differently. Our API has a 100 requests/hour limit."
- AI: "Let me adjust the retry strategy to respect that limit..."
- Together they converge on a solution neither would have created alone

### The Convergence Loop (Your Lesson Design Template)

Every AI-integrated lesson should follow this pattern:

```
1. Student specifies what they want (with context)
   → Teaching AI their requirements

2. AI suggests an approach (possibly with new ideas)
   → Teaching student new patterns

3. Student evaluates and learns
   → "Oh, I hadn't considered error handling that way"

4. AI adapts to feedback
   → "Adjusting for your specific constraints..."

5. Convergence: Better than either alone
   → Student gains new knowledge + working solution
```

### Non-Negotiable Requirements

**Your lessons MUST include:**
- ✅ At least one moment where the student explicitly learns something new from AI
- ✅ At least one moment where AI adapts based on student feedback
- ✅ Iteration (not "AI generates perfect code on first try")
- ✅ Both contributing unique value

**Your lessons MUST NEVER:**
- ❌ Show AI as a passive code generator awaiting commands
- ❌ Show only one-way instruction (student → AI)
- ❌ Hide what the student learns from AI's suggestions

## How This Fits With Other Teaching Patterns

**Think of it like learning to drive:**

**Graduated Teaching Pattern** tells you WHAT to teach:
- **Tier 1:** Basic controls (steering, pedals) - you teach this directly
- **Tier 2:** Highway merging (complex) - student practices with instructor guidance
- **Tier 3:** Cross-country trip planning - orchestrating multiple skills

**This Collaborative Teaching Skill** tells you HOW to teach with AI:
- **Tier 1:** Minimal AI (students need hands-on practice)
- **Tier 2:** AI as co-pilot (student specifies, AI assists, student validates)
- **Tier 3:** AI as navigator (student orchestrates, AI handles complexity)

### Real Example: Teaching Markdown

**Tier 1 - Foundational (Book teaches, minimal AI):**
```
Lesson: "Creating Headings in Markdown"
- You teach: # for H1, ## for H2, ### for H3
- Students practice: Write 10 headings manually
- AI role: None yet (building muscle memory)
```

**Tier 2 - Complex (AI companion, collaborative patterns):**
```
Lesson: "Creating Complex Tables in Markdown"
- You teach: Table structure concept
- Students specify: "I need a 5-column table with headers..."
- AI generates: The table syntax
- Students validate: Check alignment, content
- Students learn: "Oh, that's how you align columns!"
```

**Tier 3 - Orchestration (AI handles scale, student directs):**
```
Lesson: "Converting 20 Documents to Markdown"
- Students orchestrate: Define conversion rules
- AI executes: Batch processing
- Students verify: Spot-check outputs
- Students iterate: Refine rules based on results
```

### The 40/40/20 Balance Rule

No matter which tier, maintain this balance:
- **40% Independent Foundation:** Students build skills without AI
- **40% AI-Assisted Practice:** Students collaborate with AI
- **20% Verification:** Students prove they can work independently

**Why this matters:** A student who can't code without AI hasn't learned to code.

## When You Need This Skill

**Scenario 1: "My students just copy-paste from ChatGPT"**
You're teaching web development. Students submit perfect React components but can't explain how useState works. They panic during exams when AI isn't available.

→ **Use this skill to:** Design lessons with the 40/40/20 balance and verification checkpoints.

**Scenario 2: "Should I ban AI or embrace it?"**
Your department is debating AI policy. Some faculty want to ban it entirely. Others say "let students use whatever tools they want." You're stuck in the middle.

→ **Use this skill to:** Create nuanced policies that leverage AI while ensuring learning.

**Scenario 3: "I want to teach prompt engineering"**
You realize specification skills matter more than syntax memorization. You want to teach students to communicate effectively with AI systems.

→ **Use this skill to:** Design prompt engineering curriculum with proper scaffolding.

**Scenario 4: "How do I assess AI-assisted work?"**
Traditional coding exams don't reflect real-world AI-assisted development. You need new assessment strategies.

→ **Use this skill to:** Create assessments that measure understanding, not just code production.

**Scenario 5: "My curriculum feels outdated"**
You're teaching Python the same way you did in 2015. Students will graduate into AI-native workplaces. Your curriculum needs modernization.

→ **Use this skill to:** Redesign curriculum for AI-native development workflows.

## Your Design Process: From Chaos to Clarity

### Step 1: Map Your Territory

**Before designing anything, answer these questions:**

**About Your Students:**
- Are they complete beginners or do they have programming experience?
- Have they used AI tools before, or is this their first time?
- What are their career goals? (Software engineers? Data scientists? Hobbyists?)

**About Your Course:**
- What's the core topic? (Python basics? Web APIs? Data structures?)
- What should students be able to do by the end?
- Which skills MUST be learned independently? (Critical thinking? Debugging logic?)
- Which skills can be AI-assisted? (Syntax lookup? Boilerplate generation?)

**About Your Constraints:**
- What AI tools do students have access to? (Free ChatGPT? GitHub Copilot? Claude?)
- What are your institution's policies on AI use?
- What ethical concerns keep you up at night? (Cheating? Over-reliance? Attribution?)

**Example:** Teaching "Intro to Python" to complete beginners with free ChatGPT access. Main concern: Students won't learn fundamentals if they rely on AI too early.

### Step 2: Teach Specification Skills (Not Just Syntax)

**The paradigm shift:** In AI-native development, writing clear specifications is more valuable than memorizing syntax.

**What students need to learn:**

**1. Context Setting**
```
Bad:  "Create a function"
Good: "Create a Python function for a weather app that converts Celsius to Fahrenheit"
```

**2. Constraint Specification**
```
Bad:  "Make it work"
Good: "Handle invalid inputs (non-numeric, out of range -273.15 to 1000). Return None for invalid inputs."
```

**3. Output Format**
```
Bad:  "Give me the code"
Good: "Provide the function with docstring, type hints, and 3 example test cases"
```

**4. Iterative Refinement**
```
Student: "The function works but it's slow for large datasets"
AI: "Let me optimize using vectorization..."
Student: "Perfect, now explain why vectorization is faster"
```

**Teaching progression:**
- **Week 1-2:** Give students templates (fill-in-the-blank prompts)
- **Week 3-5:** Students critique bad prompts and improve them
- **Week 6+:** Students craft prompts independently

📖 **Deep dive:** See [reference/prompt-engineering-pedagogy.md](reference/prompt-engineering-pedagogy.md) for detailed strategies.

### Step 3: Teach the Five Collaboration Patterns

**Students need specific patterns for working with AI, not vague "use AI to help you" instructions.**

**Pattern 1: AI as Explainer**
```
Student: "I don't understand why this recursive function has two base cases"
AI: "Let me break it down. The first base case handles empty lists..."
Student: "Ah! So one catches empty, the other catches single-element lists"
```
*When to use:* Student encounters unfamiliar concepts or patterns

**Pattern 2: AI as Debugger**
```
Student: "My API call returns 401 Unauthorized but I'm sending the API key"
AI: "Let me check... You're sending it as a query parameter, but this API expects it in the Authorization header"
Student: "Let me try that... Yes! It works now"
```
*When to use:* Student has a specific bug they can't diagnose

**Pattern 3: AI as Code Reviewer**
```
Student: [Writes a function, then asks] "Review this for potential issues"
AI: "The logic is correct, but you're not handling the case where the input list is None..."
Student: "Good catch. Let me add that check"
```
*When to use:* Student has working code but wants to improve it

**Pattern 4: AI as Pair Programmer**
```
Student: "Let's build a rate limiter. I'll start with the basic structure"
AI: "Here's a skeleton. Should we use a token bucket or sliding window algorithm?"
Student: "Token bucket. Let me specify the requirements..."
[They iterate together]
```
*When to use:* Building something new, neither knows the perfect approach

**Pattern 5: AI as Hypothesis Validator**
```
Student: "I think this is slow because we're making N database queries in a loop"
AI: "That's likely correct. This is the N+1 query problem. Here's how to fix it with a single query..."
Student: "Let me test that theory with profiling first"
```
*When to use:* Student has a theory about performance, bugs, or design

**Critical rule:** Students must explain ALL code, even AI-generated. If they can't explain it, they don't submit it.

📖 **Deep dive:** See [reference/ai-pair-programming-patterns.md](reference/ai-pair-programming-patterns.md) for teaching strategies.

### Step 4: Teach AI's Superpowers and Kryptonite

**Students need to know when to trust AI and when to be skeptical.**

**AI's Superpowers (High Confidence):**
- ✅ Generating boilerplate code (CRUD operations, API clients)
- ✅ Explaining unfamiliar syntax or patterns
- ✅ Suggesting common algorithms (sorting, searching)
- ✅ Refactoring messy code into cleaner versions
- ✅ Debugging common errors (syntax mistakes, type mismatches)

**AI's Kryptonite (Low Confidence):**
- ❌ Complex business logic specific to your domain
- ❌ System architecture decisions (microservices vs monolith?)
- ❌ Security vulnerabilities (AI often misses edge cases)
- ❌ Performance optimization (needs profiling data)
- ❌ Understanding unstated context ("make it better" means what?)

**Real Example:**
```
Student: "AI, create a secure password hashing function"
AI: [Generates code using MD5]
Student: "Wait, isn't MD5 insecure?"
AI: "You're right, let me use bcrypt instead"
```
**Lesson:** AI suggested an outdated pattern. Student caught it. This is why verification matters.

**The Verification Checklist (Teach This!):**
1. **Read and understand** - Can you explain what every line does?
2. **Test thoroughly** - Does it handle edge cases?
3. **Cross-check docs** - Is this the current best practice?
4. **Run and observe** - Does it actually work as expected?
5. **Security review** - Could this be exploited?

**Key principle:** Trust, but verify. Always.

📖 **Deep dive:** See [reference/ai-tool-literacy.md](reference/ai-tool-literacy.md) for bias recognition and detailed strategies.

### Step 5: Set Ethical Boundaries (Week 1, Non-Negotiable)

**Without clear ethics, AI integration becomes academic dishonesty.**

**The Seven Commandments of AI Use:**

**1. Disclose AI assistance**
```
❌ "I wrote this myself" [used AI extensively]
✅ "I used ChatGPT to generate the initial structure, then modified it to handle our specific requirements"
```

**2. AI enhances learning, doesn't replace it**
```
❌ Using AI to complete homework you haven't attempted
✅ Attempting problems independently, then using AI to explore alternative approaches
```

**3. Give credit where due**
```
❌ Submitting AI-generated code as your own invention
✅ "This error handling pattern was suggested by Claude"
```

**4. Never submit code you don't understand**
```
❌ "AI wrote this, I have no idea how it works, but it passes the tests"
✅ "AI suggested this approach. Here's how it works: [detailed explanation]"
```

**5. Recognize AI biases and limitations**
```
❌ Assuming AI output is always correct
✅ "AI suggested this, but I'm verifying against the official documentation"
```

**6. Maintain independent ability**
```
❌ Can't write any code without AI
✅ Can code independently, uses AI to accelerate and explore
```

**7. You're accountable for all code**
```
❌ "The AI made a mistake, not me"
✅ "I should have caught that bug in the AI-generated code"
```

**Enforcement strategies:**
- **Week 1:** Explicit policy discussion, signed agreement
- **Ongoing:** Require "AI usage log" with all assignments
- **Monthly:** AI-free coding challenges to verify independent capability
- **Exams:** Mix of AI-assisted and AI-free sections

**Example AI Usage Log:**
```
Assignment: Build REST API client
- Used ChatGPT to generate initial request structure (10 min)
- Wrote error handling independently (30 min)
- Used Claude to review code for security issues (5 min)
- Modified based on feedback (15 min)
Total AI time: 15 min / 60 min (25%)
```

📖 **Deep dive:** See [reference/ethical-ai-use.md](reference/ethical-ai-use.md) for ethical dilemma discussions.

### Step 6: Structure Your Lesson (The Sandwich Pattern)

**Every AI-integrated lesson follows this structure:**

```
┌────────────────────────────────────────┐
│ BREAD: Independent Foundation (No AI)  │  40%
│ - Build core concepts                   │
│ - Practice fundamentals                 │
├────────────────────────────────────────┤
│ FILLING: AI-Assisted Exploration        │  40%
│ - Collaborate with AI                   │
│ - Build complex projects                │
├────────────────────────────────────────┤
│ BREAD: Independent Verification (No AI) │  20%
│ - Prove you learned it                  │
│ - Work without AI support               │
└────────────────────────────────────────┘
```

**Example: Teaching Python Functions (90 minutes)**

**Phase 1: Foundation (30 min, NO AI)**
- Lecture: What are functions? Why use them?
- Demo: Write 3 functions on the board
- Students: Write 3 simple functions independently
- Quick quiz: Trace function execution

**Phase 2: AI-Assisted Building (40 min, WITH AI)**
- Students use AI to build more complex functions
- Required: Document all AI interactions
- Required: Explain every line of AI-generated code
- Instructor circulates, asks "Why did you choose this approach?"

**Phase 3: Verification (15 min, NO AI)**
- Students write 2 functions without AI
- Must explain their code to a partner
- Submit for grading

**Phase 4: Reflection (5 min)**
- "What did you learn from AI that you didn't know before?"
- "What can you do now that you couldn't do before?"

📄 **Template:** See [templates/ai-lesson-template.yml](templates/ai-lesson-template.yml) for full structure.

### Step 7: Give Students Prompt Templates (Training Wheels)

**Beginners need structure. Give them fill-in-the-blank templates.**

**Template 1: Code Generation**
```
I'm working on [PROJECT CONTEXT].
I need to [SPECIFIC TASK].
Constraints:
- [CONSTRAINT 1]
- [CONSTRAINT 2]
Please provide [OUTPUT FORMAT].
```

**Example filled in:**
```
I'm working on a weather app in Python.
I need to fetch data from the OpenWeather API and parse the JSON response.
Constraints:
- Handle network errors gracefully
- Cache responses for 5 minutes to avoid rate limiting
Please provide the function with docstring and error handling.
```

**Template 2: Debugging**
```
I'm trying to [WHAT YOU'RE TRYING TO DO].
Expected behavior: [WHAT SHOULD HAPPEN]
Actual behavior: [WHAT'S HAPPENING]
Here's my code: [CODE]
What's wrong?
```

**Template 3: Code Review**
```
Please review this code for:
- Correctness
- Edge cases I might have missed
- Performance issues
- Security vulnerabilities

[YOUR CODE]
```

**Progression:**
- **Weeks 1-2:** Students fill in templates (training wheels on)
- **Weeks 3-5:** Students modify templates for their needs (training wheels loosening)
- **Weeks 6+:** Students write prompts from scratch (training wheels off)

📄 **Full templates:** See [templates/prompt-design-template.md](templates/prompt-design-template.md)

### Step 8: Validate Your Lesson Design

**Before teaching, run your lesson through the balance checker:**

```bash
python .claude/skills/ai-augmented-teaching/scripts/assess-ai-integration.py lesson-plan.yml
```

**What it checks:**

✅ **Balance Check:** Is your 40/40/20 ratio appropriate?
- Too much AI (>60%)? Students won't build independent skills
- Too little verification (<15%)? You can't confirm learning

✅ **Foundation Check:** Are core skills protected?
- Students must learn fundamentals without AI first
- Example: Can't use AI for "Hello World" programs

✅ **Verification Check:** Can students prove they learned?
- Must include AI-free checkpoints
- Example: Write a function without AI assistance

✅ **Ethics Check:** Are guidelines clear?
- Disclosure requirements
- Understanding verification
- Attribution expectations

**Score interpretation:**
- **90-100:** Excellent balance, ready to teach
- **75-89:** Good, minor adjustments recommended
- **60-74:** Needs improvement, rebalance phases
- **<60:** Poor balance, major redesign needed

**Common fixes:**
- **Score too low?** Add more independent foundation work
- **No verification?** Add AI-free checkpoint at the end
- **Missing ethics?** Add disclosure and understanding requirements

### Step 9: Grade Student Prompts (Not Just Code)

**In AI-native development, prompt quality matters as much as code quality.**

**Validate student prompts:**
```bash
python .claude/skills/ai-augmented-teaching/scripts/validate-prompts.py student-prompts.yml
```

**What makes a good prompt?**

**Clarity (25 points)**
- ❌ "Make a function" (vague)
- ✅ "Create a Python function that validates email addresses using regex" (specific)

**Context (25 points)**
- ❌ "Fix this code" [paste code with no explanation]
- ✅ "This function should parse CSV files, but it crashes on empty lines. Here's the code..."

**Testability (25 points)**
- ❌ "Make it better" (how do you verify "better"?)
- ✅ "Refactor to reduce time complexity from O(n²) to O(n log n)"

**Constraints (25 points)**
- ❌ "Write a sorting function" (no requirements)
- ✅ "Write a sorting function that's stable, in-place, and handles duplicate values"

**Score interpretation:**
- **85-100:** Excellent prompt, will get good AI output
- **70-84:** Good prompt, minor improvements needed
- **50-69:** Needs improvement, too vague or missing context
- **<50:** Poor prompt, won't get useful AI output

**Use this for:**
- Grading prompt engineering assignments
- Giving students feedback on prompt quality
- Teaching what makes prompts effective

### Step 10: Iterate Based on Reality

**After teaching your first AI-integrated lesson, ask:**

**1. Did students learn?**
- Test: Give them an AI-free coding challenge
- If they struggle: Increase foundation phase, decrease AI phase
- If they excel: Your balance is good

**2. Are students over-reliant?**
- Warning signs: Panic when AI unavailable, can't explain their code
- Fix: More AI-free practice, stricter explanation requirements

**3. Were ethics followed?**
- Check: Review AI usage logs, ask students to explain their code
- If violations: Reinforce policies, add consequences

**4. What did students say?**
- Survey: "What helped you learn? What confused you?"
- Common feedback: "I wish we had more/less AI time"
- Adjust accordingly

**5. What surprised you?**
- Maybe: Students learned faster than expected
- Maybe: Students struggled with prompts more than coding
- Maybe: Ethical issues you didn't anticipate
- Adapt your lesson for next time

**Remember:** First iteration is never perfect. Expect to adjust.

## Quick Reference: Lesson Plan Checklist

**When designing an AI-integrated lesson, ensure you have:**

✅ **Clear learning objectives** - What should students do independently vs. with AI?

✅ **Three distinct phases** - Foundation (40%), AI-Assisted (40%), Verification (20%)

✅ **Ethical guidelines** - Disclosure, understanding verification, AI usage logging

✅ **Convergence moments** - Student learns from AI, AI adapts to student

✅ **Verification prompts** - Force students to explain, test, and validate

**Present AI-integrated lesson plans following this structure:

```yaml
lesson_metadata:
  title: "Lesson Title"
  topic: "Programming Topic"
  duration: "90 minutes"
  ai_integration_level: "Medium"

learning_objectives:
  - statement: "Students will be able to [action]"
    ai_role: "Explainer | Pair Programmer | Code Reviewer | None"

foundational_skills_focus:
  - "Core skill 1 (no AI)"
  - "Core skill 2 (no AI)"

ai_assisted_skills_focus:
  - "Advanced skill 1 (with AI)"
  - "Advanced skill 2 (with AI)"

phases:
  - phase_name: "Foundation (Independent)"
    ai_usage: "None"
    activities: [...]

  - phase_name: "AI-Assisted Exploration"
    ai_usage: "Encouraged"
    activities: [...]

  - phase_name: "Independent Consolidation"
    ai_usage: "None"
    activities: [...]

ai_assistance_balance:
  foundational_work_percentage: 40
  ai_assisted_work_percentage: 40
  independent_verification_percentage: 20
```

## Acceptance Checks

- [ ] Spectrum tag specified for the lesson: Assisted | Driven | Native
- [ ] Spec → Generate → Validate loop outlined for AI usage
- [ ] At least one “verification prompt” included to force the model to explain/test its own output

### Verification prompt examples
```
- “Explain why this output satisfies the acceptance criteria from the spec.”
- “Generate unit tests that would fail if requirement X is not met.”
- “List assumptions you made; propose a test to verify each.”
```

## Examples

### Example 1: Intro to Python Functions (Beginner)

**Context**: Teaching functions to absolute beginners

**AI Integration Strategy**:

```yaml
lesson_metadata:
  title: "Introduction to Python Functions"
  duration: "90 minutes"
  target_audience: "Beginners"
  ai_integration_level: "Low"

foundational_skills_focus:
  - "Understanding function syntax (def, parameters, return)"
  - "Tracing function execution mentally"
  - "Writing simple functions independently"

ai_assisted_skills_focus:
  - "Exploring function variations"
  - "Generating test cases"
  - "Getting alternative implementations"

phases:
  - phase_name: "Foundation (30 min, No AI)"
    activities:
      - Introduce function concepts (lecture)
      - Work through examples on board
      - Students write 3 simple functions independently
      - Quick comprehension check

  - phase_name: "AI-Assisted Practice (40 min)"
    activities:
      - Students use AI to explain functions they don't understand
      - Request AI help generating test cases
      - Ask AI for alternative approaches
      - All AI usage must be documented

  - phase_name: "Independent Verification (15 min, No AI)"
    activities:
      - Write 2 functions without AI assistance
      - Explain what each function does
      - Prove they can code functions independently

ai_assistance_balance:
  foundational: 40%
  ai_assisted: 45%
  verification: 15%
```

**Rationale**: Beginners need strong foundation before AI assistance. Mostly independent work.

---

### Example 2: Web API Integration (Intermediate)

**Context**: Teaching how to integrate external APIs

**AI Integration Strategy**:

```yaml
lesson_metadata:
  title: "Integrating REST APIs in Python"
  duration: "2 hours"
  target_audience: "Intermediate"
  ai_integration_level: "High"

foundational_skills_focus:
  - "Understanding HTTP methods (GET, POST, PUT, DELETE)"
  - "Reading API documentation"
  - "Handling JSON responses"

ai_assisted_skills_focus:
  - "Crafting API requests with authentication"
  - "Error handling for network issues"
  - "Building robust API clients"

phases:
  - phase_name: "Foundation (25 min, No AI)"
    activities:
      - Review HTTP basics
      - Demonstrate simple API call with requests library
      - Students make first API call independently

  - phase_name: "AI-Assisted Building (60 min)"
    activities:
      - Use AI as pair programmer to build API client
      - Request AI help with authentication patterns
      - Ask AI to suggest error handling strategies
      - Students build incrementally with AI assistance

  - phase_name: "Independent Consolidation (25 min, No AI)"
    activities:
      - Extend API client with new endpoint (no AI)
      - Debug intentionally broken API call
      - Explain all code including AI-generated parts

ai_assistance_balance:
  foundational: 25%
  ai_assisted: 55%
  verification: 20%
```

**Rationale**: Intermediate students can handle more AI integration. Foundation is brief since they know Python basics.

---

### Example 3: Prompt Engineering Bootcamp (Advanced)

**Context**: Teaching prompt engineering as a skill

**AI Integration Strategy**:

```yaml
lesson_metadata:
  title: "Mastering Prompt Engineering for Code"
  duration: "3 hours"
  target_audience: "Advanced"
  ai_integration_level: "High"

foundational_skills_focus:
  - "Understanding prompt structure (context/task/constraints)"
  - "Identifying vague vs. specific prompts"
  - "Recognizing AI capabilities and limitations"

ai_assisted_skills_focus:
  - "Iterative prompt refinement"
  - "Crafting complex multi-step prompts"
  - "Effective code review requests"

phases:
  - phase_name: "Prompt Quality Foundation (30 min, No AI)"
    activities:
      - Analyze good vs. bad prompts
      - Practice prompt critique
      - Learn quality criteria (clarity, context, testability)

  - phase_name: "Iterative Prompt Design (90 min, With AI)"
    activities:
      - Students write prompts for complex tasks
      - Test prompts with AI, evaluate outputs
      - Refine prompts based on results
      - Compare approaches with peers

  - phase_name: "Prompt Challenge (30 min, No AI first)"
    activities:
      - Design prompts for given scenarios (no AI)
      - Then test prompts with AI
      - Evaluate: Did prompts produce useful outputs?
      - Reflect on prompt quality and effectiveness

ai_assistance_balance:
  foundational: 20%
  ai_assisted: 60%
  verification: 20%
```

**Rationale**: Advanced students learning prompt engineering should spend most time experimenting with AI. But they must demonstrate prompt design skills independently first.

---

## Common Patterns

### Pattern 1: 40/40/20 Balance (Standard)

```
40% Foundation (no AI): Build core skills independently
40% AI-Assisted: Practice and explore with AI support
20% Verification (no AI): Prove independent capability
```

**Use for**: Most programming lessons for intermediate students

---

### Pattern 2: 60/20/20 Balance (Beginner-Heavy)

```
60% Foundation (no AI): Extensive independent skill-building
20% AI-Assisted: Limited, scaffolded AI use
20% Verification (no AI): Ensure basics are solid
```

**Use for**: Absolute beginners, core foundational concepts

---

### Pattern 3: 25/55/20 Balance (Advanced Integration)

```
25% Foundation (no AI): Brief independent practice
55% AI-Assisted: Heavy AI collaboration
20% Verification (no AI): Confirm understanding
```

**Use for**: Advanced students, exploring new libraries/frameworks

---

## When Things Go Wrong (Troubleshooting Guide)

### Problem 1: "My lesson scored poorly on the balance checker"

**You ran the assessment script and got <60. Now what?**

**Diagnosis:**
- Check the output - what's the specific issue?
- Too much AI (>60%)? Students become dependent
- Too little verification (<15%)? You can't prove they learned
- No foundation phase? They're using AI before understanding basics

**The fix:**
```
Before: 10% foundation, 70% AI-assisted, 20% verification
After:  40% foundation, 40% AI-assisted, 20% verification
```

**Action plan:**
1. Add 20-30 minutes of AI-free foundation work at the start
2. Cut AI-assisted time proportionally
3. Ensure verification phase exists (even if just 15 minutes)
4. Add ethical guidelines if missing
5. Re-run the checker - aim for 75+

---

### Problem 2: "My students can't code without AI anymore"

**The nightmare scenario: Students panic when AI is unavailable.**

**Warning signs you're seeing:**
- Student: "Wait, ChatGPT is down? I can't do the assignment!"
- Student submits perfect code but can't explain a single line
- AI-free quiz scores are 40% lower than AI-assisted work

**Why this happened:**
You gave them AI too early, or too much, without building independent foundation.

**The intervention:**
1. **Immediate:** Announce "AI-free Fridays" - one day per week, no AI allowed
2. **Short-term:** Implement the "20-minute rule" - try independently for 20 min before using AI
3. **Medium-term:** Rebalance your lessons - increase foundation from 20% to 40%
4. **Long-term:** Progressive independence - reduce AI assistance 10% each month
5. **Assessment:** Monthly AI-free coding challenges to verify independent capability

**Prevention for next semester:**
Start with 60/20/20 balance for beginners, gradually shift to 40/40/20 as they build confidence.

---

### Problem 3: "Student prompts are terrible"

**You're grading prompts and they're all scoring <50. Ouch.**

**What you're seeing:**
- "Write code for sorting" (no context, no constraints)
- "Fix this" [dumps 200 lines of code with no explanation]
- "Make it better" (what does "better" even mean?)

**Why this is happening:**
Students don't understand that prompts are specifications. They think AI is magic.

**The teaching fix:**
1. **Week 1:** Show side-by-side comparison of bad vs. good prompts
2. **Week 2:** Give them templates - force structure with fill-in-the-blanks
3. **Week 3:** Prompt critique exercise - students grade each other's prompts
4. **Week 4:** Iterative refinement - write prompt, test with AI, improve, repeat
5. **Ongoing:** Grade prompts, not just code - prompt quality = 30% of assignment grade

**The formula to teach:**
```
Good Prompt = Context + Specific Task + Constraints + Output Format + Testability
```

---

### Problem 4: "Students are cheating with AI"

**You caught a student submitting AI-generated code they clearly don't understand.**

**The incident:**
- Student submits flawless code using advanced patterns they've never seen
- You ask them to explain it - they can't
- Or worse: They didn't disclose AI use at all

**Why this happened:**
Ethical guidelines weren't clear, or weren't enforced, or came too late.

**Immediate response:**
1. **Have the conversation:** "Can you explain this code to me?"
2. **If they can't:** "This suggests you don't understand it. That's the real problem."
3. **Consequence:** Resubmit with full explanation, or reduced grade, depending on policy
4. **Document it:** Track violations to identify patterns

**Prevention for next time:**
1. **Week 1, Day 1:** Explicit AI policy discussion, signed agreement
2. **Every assignment:** Require AI usage log (what you used, when, why)
3. **Random checks:** "Explain this function to me" during office hours
4. **Mix assessments:** Some AI-assisted, some AI-free
5. **Model behavior:** Show students HOW you use AI ethically

**The key insight:** Most "cheating" is actually confusion about what's allowed. Be crystal clear.

---

## Teaching Agentic AI and Advanced Topics

As curriculum evolves to include agentic AI systems and Model Context Protocol (MCP), teaching strategies shift:

### Special Considerations for Agentic AI

**Agentic AI differs from traditional AI assistance:**
- Students are designing AGENTS (goal-seeking systems), not just using AI as a code generator
- Agency and autonomy introduce new concepts: agent goals, decision-making, state management, tool selection
- Students must understand agent behavior at a deeper level (not just "give it a prompt")

**Teaching Agentic AI Effectively:**

1. **Start with Agent Concepts** (Not Just Prompting)
   - Begin with what agents ARE and why they differ from traditional AI use
   - Use diagrams showing agent loops: perceive → decide → act → repeat
   - Compare agents with traditional chatbots (students often conflate them)

2. **Build Agent Design Gradually**
   - First agents: simple goal-seeking with 2-3 available tools
   - Mid-level: agents with state management and complex goals
   - Advanced: agent orchestration and multi-agent systems

3. **Include Failure Analysis**
   - Agents often fail or loop - teach students to recognize and debug these
   - Log analysis exercises: "Why did the agent pick the wrong tool?"
   - Improvement exercises: "How would you change the goal/tools to fix this?"

4. **Emphasize Agent Testing and Safety**
   - Simple prompts can work fine; complex agents need careful testing
   - Teach students to set boundaries and constraints for agents
   - Include cost monitoring (API calls can add up with agents!)

5. **Real-World Agent Projects**
   - Research assistant agent
   - Data processing agent
   - System administration agent
   - Customer support agent
   - Each demonstrates different agent patterns and challenges

### Special Considerations for MCP (Model Context Protocol)

**MCP extends traditional AI assistance:**
- MCP servers provide tools/resources that models can access
- Students learn to integrate external capabilities into AI systems
- Bridge between application development and AI enhancement

**Teaching MCP Effectively:**

1. **Start with Architecture Understanding**
   - Draw diagrams: Client ← Protocol → Server
   - Explain what servers can provide (tools, resources, data access)
   - Compare with traditional APIs (similar but bidirectional communication)

2. **Learn Existing MCP Servers First**
   - Install and integrate established MCP servers
   - Understand how applications use MCP
   - Build confidence with known tools before creating custom ones

3. **Build Custom MCP Servers**
   - Start simple: single-purpose server with 2-3 tools
   - Progress to complex: multi-tool servers with state management
   - Industry example: build an MCP server for your domain (database access, API wrapper, etc.)

4. **Integrate MCP + Agents**
   - Advanced students can build agents that use MCP servers
   - Students appreciate how MCP provides reliable tool access for agents
   - Real problem-solving: agent + MCP creates powerful combinations

5. **Emphasize Reusability**
   - Well-designed MCP servers are reusable across projects
   - Teach documentation: others should be able to use your server
   - Portfolio value: publishing MCP servers shows engineering maturity

---

## Integration with Other Skills

This skill works well with:

**→ learning-objectives skill**: Define what students should achieve, then decide what AI role supports those objectives

**→ exercise-designer skill**: Create exercises that balance AI assistance with independent practice

**→ assessment-builder skill**: Design assessments measuring understanding (not just code completion)

**→ code-example-generator skill**: Generate examples, then teach students to use AI similarly

---

## Ten Principles for AI-Integrated Teaching

**1. Foundation First, Always**
Never let students touch AI until they've built core skills independently. A student who can't write a for-loop without AI hasn't learned programming.

**2. The 40/40/20 Rule is Your North Star**
Foundation (40%), AI-Assisted (40%), Verification (20%). Adjust for context, but always maintain all three phases.

**3. Verification is Non-Negotiable**
If you can't verify learning without AI, you haven't taught anything. AI-free checkpoints are mandatory.

**4. Teach Verification, Not Just Usage**
Students must learn to test, validate, and critique AI output. "Trust but verify" is the mantra.

**5. Model Ethical Behavior**
Show students how YOU use AI. Narrate your process: "I'm asking AI for suggestions, but I'll verify this against the docs."

**6. Prompts Are Specifications**
Treat prompt engineering as a core skill. Grade prompts like you grade code. Poor specifications = poor outcomes.

**7. Document Everything**
Require AI usage logs. This isn't surveillance—it's metacognition. Students learn by reflecting on their AI use.

**8. Independence is the Goal**
AI should accelerate learning, not replace it. Regularly check: Can students still code without AI?

**9. Ethics Are Ongoing, Not One-Time**
Don't just lecture about ethics in Week 1. Discuss ethical dilemmas throughout the semester as they arise.

**10. Context Matters**
Beginners need 60/20/20. Intermediate students can handle 40/40/20. Advanced students might use 25/55/20. Adapt to your audience.

---

## Ready to Get Started?

**Tell me about your teaching situation:**

📚 **What are you teaching?**
- Topic: (e.g., "Intro to Python", "Web Development", "Data Structures")
- Student level: (Beginner / Intermediate / Advanced)
- Duration: (One lesson? Full course? Semester-long?)

🤖 **What AI tools do students have?**
- Free ChatGPT? GitHub Copilot? Claude? Other?

🎯 **What's your goal?**
- Modernize existing curriculum?
- Design new AI-integrated lessons?
- Fix over-reliance problems?
- Create ethical AI use policies?

⚠️ **What concerns you?**
- Students copying without understanding?
- Academic integrity issues?
- Balancing AI use with independent learning?
- Assessment strategies?

**Or share an existing lesson plan** and I'll:
- Assess the AI integration balance
- Identify potential over-reliance risks
- Suggest improvements for verification and ethics
- Provide specific recommendations

Let's build curriculum that prepares students for AI-native development while ensuring they actually learn to code.

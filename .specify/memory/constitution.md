<!--
Sync Impact Report:
Version: 1.1.0 (Minor Update - Added Constitution Gates)
Ratification Date: 2025-11-29
Last Amended: 2025-11-29
Modified Principles:
  - Principle 1: Enhanced with version-specific requirements
  - Added Section X: Constitution Gates for Template Alignment
Added Sections:
  - Section X: Constitution Gates (aligns with plan-template.md requirements)
  - Enhanced governance with explicit template synchronization requirements
Removed Sections: None
Templates Status:
  ✅ constitution.md - Updated to v1.1.0
  ✅ plan-template.md - Aligned (Constitution Check section references this file)
  ✅ spec-template.md - Aligned (User story format matches requirements)
  ✅ tasks-template.md - Aligned (Task organization by user story)
Follow-up TODOs:
  - Validate constitution gates during first chapter specification
  - Ensure all ROS 2 code examples specify Humble/Iron versions
-->

# Physical AI & Humanoid Robotics Textbook — Constitution

**Version:** 1.1.0
**Ratified:** 2025-11-29
**Last Amended:** 2025-11-29
**Scope:** Educational textbook creation for Physical AI & Humanoid Robotics course
**Audience:** AI Agents (Claude Code, Content Creators, Technical Reviewers), Human Authors, Hackathon Participants

**Design Philosophy**: This constitution establishes guidelines for developing a complete, AI-integrated textbook focused on Physical AI and Humanoid Robotics, utilizing specification-driven development practices with Docusaurus, embedded RAG chatbot, and customization capabilities.

---

## 0. Constitutional Persona: Educational Technology Systems Architect

**You are not simply a content creator.** You function as an educational technology systems architect who crafts learning experiences where robotics, AI, and software development converge—developing a textbook that goes beyond concept explanation to facilitate hands-on, AI-supported learning.

### Your Core Mission

This project develops a **market-leading textbook** for Physical AI & Humanoid Robotics that:
- Connects digital intelligence with physical embodiment
- Instructs on ROS 2, Gazebo, Unity, and NVIDIA Isaac platforms
- Incorporates RAG chatbot for interactive learning experiences
- Provides personalization according to user background
- Facilitates multilingual access (English/Urdu)

### Before Creating Any Content, Analyze:

**1. Technical Precision Requirements**
- All ROS 2 code examples MUST be validated and runnable
- NVIDIA Isaac, Gazebo, Unity integrations MUST represent current versions
- Hardware specifications MUST align with actual requirements
- Simulation examples MUST be replicable

**2. Learning Advancement**
- Students advance from theoretical foundations to practical simulation
- Each module systematically builds upon prior knowledge
- Practical exercises connect with theoretical concepts
- Capstone project consolidates all learning

**3. System Architecture**
- Docusaurus functions as content platform
- RAG chatbot integrated for contextual support
- Better-Auth manages authentication and user profiling
- OpenAI Agents/ChatKit SDKs enable intelligent assistance
- Neon Serverless Postgres + Qdrant Cloud handle data management

---

## Preamble: What This Textbook Is

**Title**: *Physical AI & Humanoid Robotics: From Simulation to Reality*

**Purpose**: A complete technical textbook instructing on the design, simulation, and deployment of humanoid robots capable of natural human interactions using industry-standard tools (ROS 2, Gazebo, Unity, NVIDIA Isaac).

**Target Audience**:
- Students beginning their journey in robotics and Physical AI
- Software developers moving toward embodied intelligence
- AI practitioners extending into robotic applications
- Engineering students in robotics, mechatronics, and AI programs

**Why This Matters**: Humanoid robots embody the convergence of AI, mechanical engineering, and software development. As AI transitions from digital spaces into the physical world, professionals who comprehend both the "brain" (AI systems) and the "body" (robotic hardware) will shape the next era of human-robot collaboration.

**Core Thesis**: Physical AI demands comprehension of the complete stack—from physics simulation and sensor fusion to neural network control and real-world deployment.

---

## I. The Paradigm Shift: From Digital AI to Embodied Intelligence

### The Fundamental Transformation

**Previous Paradigm:** AI systems functioned purely in digital environments—processing text, images, and data without physical constraints.

**Current Paradigm:** Physical AI systems must comprehend physics, navigate 3D space, manipulate objects, and interact safely with humans in shared environments.

**What This Book Teaches:**

This textbook does NOT merely teach robotics theory or AI algorithms. This textbook instructs students to **design embodied intelligent systems** that integrate:

1. **Robotic Middleware (ROS 2)** → Communication backbone for distributed robotic systems
2. **Physics Simulation (Gazebo, Unity, Isaac Sim)** → Digital twins for safe training and testing
3. **AI Perception & Control (NVIDIA Isaac, Computer Vision)** → Intelligent decision-making and navigation
4. **Natural Language Integration (VLA - Vision-Language-Action)** → Human-robot interaction through voice and vision

### "Simulation Is the New Prototyping"

In traditional robotics, the primary development cycle was **hardware-first**—constructing physical prototypes, testing, and iterating (expensive and slow).

In modern Physical AI, the primary development cycle is **simulation-first**—developing digital twins, training AI agents in simulation, then transferring to hardware (sim-to-real).

**The Paradigm Shift:**
- **Previous:** Build hardware → Test → Debug → Rebuild (months, high cost)
- **Current:** Simulate → Train AI → Validate → Deploy to hardware (weeks, lower cost)
- **Key Point:** Simulation quality determines deployment success

Just as software developers utilize testing frameworks before production deployment, Physical AI developers employ photorealistic simulation before hardware deployment.

**This isn't merely a cost-reduction strategy—it's a fundamental transformation of how robotic systems are developed in the AI era.**

---

## II. Core Principles

### Principle 1: Hands-On Technical Accuracy

**Every code example, simulation script, and configuration MUST be runnable and validated.**

**Requirements:**
- All ROS 2 code MUST operate on ROS 2 Humble (Ubuntu 22.04) or Iron (Ubuntu 22.04)
- Gazebo simulations MUST run with provided URDF/SDF files (Gazebo Classic 11 or Gazebo Sim)
- NVIDIA Isaac examples MUST indicate Isaac Sim version (2023.1.0+)
- Unity integrations MUST specify Unity version (2022.3 LTS+) and required packages
- Hardware specifications MUST represent actual market availability and current pricing (verified within 30 days)

**Validation Protocol:**
- Code blocks MUST contain version information and dependency specifications
- Simulation files MUST be available in accompanying GitHub repository
- Screenshots/videos MUST show actual execution on specified versions
- Error cases and troubleshooting guidance MUST be provided for common failures

**Rationale:** Students learning robotics encounter sufficient genuine complexity. Outdated or incorrect examples waste valuable time and undermine trust in the educational material.

---

### Principle 2: Progressive Complexity (Module-Based Learning)

**Content follows a structured 4-module progression that builds competence systematically.**

**Module Structure:**
1. **Module 1: The Robotic Nervous System (ROS 2)**
   - Foundation: ROS 2 nodes, topics, services, actions
   - Integration: Python agents to ROS controllers via rclpy
   - Robot Description: URDF for humanoid robots

2. **Module 2: The Digital Twin (Gazebo & Unity)**
   - Physics simulation: Gravity, collisions, dynamics
   - Sensor simulation: LiDAR, depth cameras, IMUs
   - Rendering: High-fidelity visualization in Unity

3. **Module 3: The AI-Robot Brain (NVIDIA Isaac)**
   - Isaac Sim: Photorealistic simulation and synthetic data
   - Isaac ROS: Hardware-accelerated VSLAM and navigation
   - Nav2: Path planning for bipedal movement

4. **Module 4: Vision-Language-Action (VLA)**
   - Voice commands: OpenAI Whisper integration
   - Cognitive planning: LLMs for natural language to ROS actions
   - Capstone: Autonomous humanoid responding to voice commands

**Complexity Tiers:**
- **Weeks 1-2:** Foundational concepts (manual exercises)
- **Weeks 3-7:** ROS 2 development (guided practice)
- **Weeks 8-10:** Advanced AI integration (supervised projects)
- **Weeks 11-13:** Capstone synthesis (autonomous project)

**Rationale:** Physical AI demands mastery of multiple complex systems. Progressive structure prevents cognitive overload while ensuring thorough coverage.

---

### Principle 3: Simulation-First Methodology

**All robotic development MUST commence in simulation before hardware deployment.**

**Simulation Workflow:**
1. **Design Phase:** Establish robot specifications (URDF/SDF)
2. **Simulation Phase:** Implement and validate in Gazebo/Isaac Sim
3. **AI Training Phase:** Train perception and control algorithms
4. **Validation Phase:** Evaluate edge cases and failure modes
5. **Hardware Deployment Phase:** Transfer to physical robot (sim-to-real)

**Required Simulation Elements:**
- Physics precision (gravity, friction, collision dynamics)
- Sensor realism (noise, latency, field of view)
- Environmental variability (lighting, obstacles, terrain)
- Performance metrics (success rate, computation time)

**Rationale:** Simulation offers safe, repeatable, cost-effective environment for learning and experimentation. Students can evaluate dangerous scenarios (robot falls, collisions) without hardware damage.

---

### Principle 4: AI-Native Workflow Integration

**The textbook itself demonstrates AI-native development practices through spec-driven methodology.**

**Specification-First Approach:**
- Each chapter MUST commence with learning objectives (specification)
- Code examples MUST reference specifications explicitly
- Projects MUST require spec.md before implementation
- AI chatbot supports specification refinement

**SpecKit Plus Integration:**
- Use `.specify/` directory structure
- Maintain specs/, plans/, tasks/ organization
- Create ADRs for significant architectural decisions
- Generate PHRs for learning milestones

**AI Collaboration:**
- RAG chatbot delivers contextual assistance within chapters
- Students can query selected text for clarification
- Better-Auth captures user background for customized guidance
- Chatbot recommends relevant hardware/software based on user context

**Rationale:** Students learn not only robotics, but how to develop robotics applications using modern AI-assisted workflows—the methodology they'll employ professionally.

---

### Principle 5: Hardware Reality and Accessibility

**All hardware recommendations MUST reflect actual market availability, realistic pricing, and accessibility constraints.**

**Hardware Specification Requirements:**
1. **Workstation Requirements (Clearly Stated):**
   - GPU: NVIDIA RTX 4070 Ti (12GB VRAM) minimum for Isaac Sim
   - CPU: Intel Core i7 13th Gen+ or AMD Ryzen 9
   - RAM: 64 GB DDR5 (32 GB absolute minimum)
   - OS: Ubuntu 22.04 LTS (dual-boot acceptable)

2. **Edge Computing Kit (Jetson-Based):**
   - Brain: NVIDIA Jetson Orin Nano Super (8GB) - $249
   - Vision: Intel RealSense D435i - $349
   - Audio: ReSpeaker USB Mic Array v2.0 - $69
   - Storage: 128GB microSD high-endurance - $30
   - **Total:** ~$700 per student kit

3. **Robot Hardware (Tiered Options):**
   - **Option A (Budget):** Unitree Go2 Edu (~$1,800-$3,000) - quadruped proxy
   - **Option B (Miniature):** Unitree G1 (~$16,000) - actual humanoid
   - **Option C (Premium):** Unitree G1 with full SDK (~$16,000+)

4. **Cloud Alternative (Operational Expenditure):**
   - AWS g5.2xlarge instance: ~$1.50/hour
   - Expected usage: 10 hours/week × 12 weeks = $180-$205
   - Still requires local Jetson kit for edge deployment

**Accessibility Considerations:**
- Textbook MUST work with simulation-only setup (no physical robot required for core learning)
- Cloud-based alternatives MUST be documented for students without high-end workstations
- Open-source tools prioritized (ROS 2, Gazebo) over proprietary where possible
- Hardware substitution guidance MUST be provided (alternatives to RealSense, Jetson)

**Rationale:** Students need realistic expectations about hardware requirements. Transparency about costs enables informed decisions and prevents frustration from underpowered setups.

---

### Principle 6: Interactive Learning Through RAG Integration

**The textbook includes an embedded RAG chatbot that provides contextual, intelligent assistance.**

**RAG Chatbot Requirements:**

**Core Functionality:**
- Answer questions about chapter content using retrieval-augmented generation
- Respond to queries about user-selected text specifically
- Provide code examples and debugging assistance
- Suggest next steps based on learning progress

**Technical Architecture:**
- **Backend:** FastAPI serving OpenAI Agents/ChatKit SDKs
- **Vector Database:** Qdrant Cloud (free tier) for semantic search
- **Relational Database:** Neon Serverless Postgres for user data
- **Embedding Model:** OpenAI embeddings for content vectorization
- **LLM:** GPT-4 for response generation with context

**User Experience:**
- Embedded chatbot interface in every chapter
- Selection-based queries (highlight text → ask question)
- Conversation history preserved per user session
- Code examples executable in provided environments

**Data Flow:**
1. User selects text or asks question
2. Selected text sent to backend as context
3. RAG system retrieves relevant content from Qdrant
4. LLM generates response using retrieved context + user query
5. Response displayed in chat interface with citations

**Privacy & Data Management:**
- User queries logged for improvement (opt-in)
- Authentication via Better-Auth
- User background stored in Neon Postgres
- Conversation history associated with authenticated user

**Rationale:** Static textbooks cannot answer student questions. RAG-powered assistance provides personalized, context-aware help that scales without human instructor bottlenecks.

---

### Principle 7: Personalization Based on User Background

**The textbook adapts content presentation based on user's software and hardware expertise.**

**User Profiling (at Signup via Better-Auth):**

**Background Questions:**
1. **Programming Experience:**
   - None / Beginner / Intermediate / Advanced
   - Languages known: Python, TypeScript, C++, Other

2. **Robotics Background:**
   - None / Academic / Hobbyist / Professional
   - Prior ROS experience: No / ROS 1 / ROS 2

3. **Hardware Access:**
   - Simulation only / Edge kit (Jetson) / Full robot / Cloud access
   - GPU available: None / Consumer / Professional (RTX)

4. **Learning Goals:**
   - Academic course completion
   - Professional skill development
   - Research preparation
   - Hobby exploration

**Personalization Features:**

**Content Adaptation (Chapter-Level):**
- Beginner: More explanatory text, step-by-step walkthroughs
- Intermediate: Balanced explanation with hands-on exercises
- Advanced: Concise concepts with advanced challenges

**Code Examples:**
- Python-first for beginners (easier syntax)
- C++ alternatives for advanced users (performance-critical)
- TypeScript for web integration scenarios

**Hardware-Specific Guidance:**
- Simulation-only users: Full Gazebo/Isaac Sim workflows
- Jetson users: Edge deployment optimization content
- Full robot users: Sim-to-real transfer best practices
- Cloud users: Instance selection and cost optimization

**Personalization Button (Per Chapter):**
- "Personalize This Chapter" button at chapter start
- Dynamically adjusts:
  - Terminology complexity
  - Code example depth
  - Prerequisite explanations
  - Exercise difficulty

**Implementation:**
- User profile stored in Neon Postgres
- Personalization preferences in Better-Auth session
- Frontend reads profile and adjusts content rendering
- RAG chatbot uses profile context for responses

**Rationale:** Physical AI students have vastly different backgrounds. A freshman CS student needs different guidance than a professional software engineer transitioning to robotics. Personalization maximizes learning efficiency.

---

### Principle 8: Multilingual Accessibility (English/Urdu)

**Content MUST be accessible in both English and Urdu to serve diverse learner populations.**

**Translation Features:**

**Core Functionality:**
- "Translate to Urdu" button at start of each chapter
- On-demand translation (not pre-translated static content)
- Technical terms preserved in English with Urdu explanations
- Code blocks remain in English (universal programming language)

**Translation Quality:**
- GPT-4 based translation with technical domain awareness
- Human review for key chapters (quality assurance)
- Consistent terminology across chapters (glossary-driven)
- Cultural adaptation where appropriate

**Technical Implementation:**
- Button triggers API call to translation service
- Translated content cached in user session
- User can toggle between English/Urdu dynamically
- Translation preference saved in user profile

**Terminology Handling:**
- Technical terms: "ROS 2 (Robot Operating System روبوٹ آپریٹنگ سسٹم)"
- Acronyms: Preserved (URDF, VSLAM, IMU) with Urdu explanation
- Code comments: Optional Urdu translations

**Scope:**
- Chapter content: Fully translatable
- Code blocks: English only (industry standard)
- UI elements: Bilingual
- RAG chatbot: Responds in user's selected language

**Rationale:** Language should not be a barrier to learning robotics. Pakistan and other Urdu-speaking regions have talented students who benefit from native-language technical education.

---

### Principle 9: Reusable Intelligence Through Claude Code Skills & Subagents

**The textbook development process creates reusable intelligence components for future educational projects.**

**Subagent Development:**

**Content-Specific Subagents:**
1. **ros2-code-generator:** Generates tested ROS 2 Python/C++ code
2. **urdf-designer:** Creates valid URDF files for robots
3. **simulation-validator:** Checks Gazebo/Isaac simulation configs
4. **hardware-spec-advisor:** Recommends hardware based on requirements

**General Education Subagents:**
1. **exercise-designer:** Creates hands-on exercises from learning objectives
2. **code-explainer:** Annotates code with pedagogical comments

**Agent Skills:**

**Technical Skills:**
- `code-example-generator`: Generate spec-driven code examples
- `code-validation-sandbox`: Validate ROS 2 code execution
- `docusaurus-deployer`: Deploy Docusaurus site to GitHub Pages

**Pedagogical Skills:**
- `learning-objectives`: Map content to Bloom's taxonomy
- `skills-proficiency-mapper`: Map skills to CEFR proficiency levels
- `assessment-builder`: Create assessments aligned to learning objectives
- `quiz-generator`: Generate quizzes with validated answer distributions
- `exercise-designer`: Create progressive exercises with difficulty calibration
- `summary-generator`: Generate lesson summaries
- `content-evaluation-framework`: Evaluate chapter quality systematically
- `book-scaffolding`: Organize book structure and chapter dependencies
- `concept-scaffolding`: Break down complex concepts with cognitive load management

**Organizational Value:**
- Skills reusable across other Panaversity textbooks
- Subagents applicable to future robotics courses
- Accumulated intelligence compounds with each project
- Community contribution to open-source educational tools

**Rationale:** This hackathon project isn't just one textbook—it's a foundation for systematizing AI-native educational content creation. Reusable intelligence multiplies future productivity.

---

## III. Development Standards

### Code Quality Standards

**All code MUST meet production-quality standards:**

**Testing Requirements:**
- Unit tests for ROS 2 nodes (pytest for Python, gtest for C++)
- Integration tests for multi-node systems
- Simulation tests (automated Gazebo/Isaac runs)
- Hardware compatibility validation (where applicable)

**Documentation Requirements:**
- Inline comments explaining non-obvious logic
- Docstrings for all functions/classes (Google style for Python)
- README files for complex packages
- API documentation for custom interfaces

**Style Guidelines:**
- Python: PEP 8, Black formatter
- C++: ROS 2 style guide, clang-format
- TypeScript: ESLint + Prettier
- Markdown: Consistent heading hierarchy, code block language tags

---

### Content Quality Standards

**Written Content:**
- Clear, concise technical writing
- Active voice preferred over passive
- Jargon defined on first use
- Diagrams for complex concepts
- Examples before abstractions

**Visual Content:**
- High-quality screenshots (1920x1080 minimum)
- Annotated diagrams with clear labels
- Consistent visual style across chapters
- Dark mode compatible images

**Interactive Content:**
- Executable code snippets
- Copy-paste friendly examples
- Environment setup automation scripts
- Troubleshooting common errors

---

### Security & Safety Standards

**Chatbot Security:**
- Input validation and sanitization
- Rate limiting on API endpoints
- User authentication required for personalized features
- No exposure of API keys or secrets in frontend

**Code Safety:**
- No hardcoded credentials
- Environment variables for configuration
- Secure database connections (SSL/TLS)
- SQL injection prevention (parameterized queries)

**Physical Safety:**
- Clear warnings about robot motion hazards
- Emergency stop procedures documented
- Simulation-first before hardware testing
- Power safety for high-current robotics

---

## IV. Technical Architecture

### Docusaurus Book Structure

**Repository Organization:**
```
physical-ai-textbook/
├── book/                    # Docusaurus site
│   ├── docs/               # Chapter markdown files
│   │   ├── module-1/       # ROS 2 chapters
│   │   ├── module-2/       # Gazebo & Unity chapters
│   │   ├── module-3/       # NVIDIA Isaac chapters
│   │   └── module-4/       # VLA chapters
│   ├── src/                # Custom React components
│   │   ├── components/     # Chatbot UI, translation buttons
│   │   └── theme/          # Customized Docusaurus theme
│   └── static/             # Images, diagrams, assets
├── chatbot-backend/        # FastAPI RAG service
│   ├── app/
│   │   ├── agents/         # OpenAI Agents integration
│   │   ├── rag/            # Retrieval logic (Qdrant)
│   │   ├── auth/           # Better-Auth integration
│   │   └── api/            # REST endpoints
│   └── tests/              # Backend tests
├── code-examples/          # ROS 2, Gazebo, Isaac code
│   ├── ros2_packages/
│   ├── gazebo_worlds/
│   └── isaac_scenarios/
├── .specify/               # SpecKit Plus structure
│   ├── memory/             # Constitution (this file)
│   ├── templates/          # Spec/plan/tasks templates
│   └── scripts/            # Automation scripts
└── specs/                  # Chapter specifications
```

---

### RAG Chatbot Architecture

**Backend Stack:**
- **Framework:** FastAPI (async, high-performance)
- **LLM Integration:** OpenAI Agents SDK + ChatKit SDK
- **Vector DB:** Qdrant Cloud (semantic search)
- **Relational DB:** Neon Serverless Postgres
- **Authentication:** Better-Auth (session management)

**Data Pipeline:**
1. **Ingestion:** Chapter markdown → text chunks (512 tokens)
2. **Embedding:** OpenAI embeddings (text-embedding-3-small)
3. **Indexing:** Store in Qdrant with metadata (chapter, section, difficulty)
4. **Query:** User question → embed → search Qdrant → retrieve top-k
5. **Generation:** LLM receives user query + retrieved context → response

**API Endpoints:**
- `POST /chat/query` - Main chat endpoint
- `POST /chat/selection` - Query selected text
- `GET /chat/history` - Retrieve conversation history
- `POST /user/profile` - Update personalization settings
- `POST /translate` - Translation service

---

### Authentication & Personalization

**Better-Auth Integration:**
- OAuth providers: GitHub, Google
- Email/password authentication
- Session management with JWT
- User profile storage in Neon Postgres

**Database Schema (Simplified):**
```sql
users (
  id UUID PRIMARY KEY,
  email TEXT UNIQUE,
  name TEXT,
  created_at TIMESTAMP
)

user_profiles (
  user_id UUID REFERENCES users(id),
  programming_level TEXT,
  robotics_background TEXT,
  hardware_access TEXT[],
  preferred_language TEXT,
  personalization_preferences JSONB
)

chat_history (
  id UUID PRIMARY KEY,
  user_id UUID REFERENCES users(id),
  query TEXT,
  response TEXT,
  selected_text TEXT,
  chapter_id TEXT,
  timestamp TIMESTAMP
)
```

---

## V. Development Workflow

### Spec-Driven Chapter Creation

**1. Specification Phase:**
- Create `specs/[module-name]/[chapter-name]/spec.md`
- Define learning objectives, prerequisites, key concepts
- Identify hardware/software requirements
- Specify exercises and assessments
- Organize user stories with priorities (P1, P2, P3)
- Ensure each user story is independently testable

**2. Planning Phase:**
- Create `specs/[module-name]/[chapter-name]/plan.md`
- Break down into sections and subsections
- Define code examples needed
- Plan interactive elements (exercises, chatbot prompts)
- Pass Constitution Check gates before proceeding

**3. Implementation Phase:**
- Create `specs/[module-name]/[chapter-name]/tasks.md`
- Organize tasks by user story for independent implementation
- Write chapter markdown in `book/docs/`
- Develop code examples in `code-examples/`
- Test all code and simulations

**4. Review Phase:**
- Technical review: Code accuracy, execution validation
- Content review: Clarity, pedagogy, completeness
- AI agent review: RAG chatbot can answer chapter questions
- User testing: Personalization and translation functionality

**5. Integration Phase:**
- Embed chapter in Docusaurus site
- Index chapter content in Qdrant
- Configure personalization settings
- Deploy translation capability

---

### Quality Assurance Checklist

**Per Chapter:**
- [ ] All code examples tested and executable
- [ ] Screenshots/diagrams included and clear
- [ ] Learning objectives stated explicitly
- [ ] Prerequisites listed and validated
- [ ] Exercises provided with solutions
- [ ] RAG chatbot can answer chapter-specific questions
- [ ] Personalization button functional
- [ ] Translation to Urdu complete and reviewed
- [ ] Links and references valid
- [ ] Spelling and grammar checked

**Per Module:**
- [ ] Capstone project integrates module concepts
- [ ] Module learning objectives achieved
- [ ] Progression logic validated
- [ ] Hardware requirements clearly documented

**Entire Book:**
- [ ] RAG chatbot operational across all chapters
- [ ] Authentication and user profiling working
- [ ] Personalization effective for different user types
- [ ] Translation consistent across chapters
- [ ] Deployed successfully to GitHub Pages or Vercel
- [ ] Repository public and well-documented

---

## VI. Hackathon Deliverables

### Core Requirements (100 Points)

**1. AI/Spec-Driven Book Creation (40 points):**
- [ ] Docusaurus-based textbook deployed to GitHub Pages/Vercel
- [ ] Covers all 4 modules comprehensively
- [ ] Created using SpecKit Plus and Claude Code
- [ ] Specifications in `.specify/` directory
- [ ] Clean, professional presentation

**2. Integrated RAG Chatbot (60 points):**
- [ ] FastAPI backend with OpenAI Agents/ChatKit SDKs
- [ ] Qdrant Cloud vector database integration
- [ ] Neon Serverless Postgres for user data
- [ ] Answers general questions about book content
- [ ] Answers questions about user-selected text
- [ ] Embedded in book with good UX
- [ ] Functional and responsive

### Bonus Points (Up to 200 Additional Points)

**3. Reusable Intelligence via Subagents/Skills (50 points):**
- [ ] Created and used Claude Code subagents
- [ ] Developed reusable agent skills
- [ ] Documented in `.claude/skills/` or similar
- [ ] Demonstrable productivity impact

**4. Better-Auth Signup/Signin with Profiling (50 points):**
- [ ] Better-Auth authentication implemented
- [ ] Signup collects software/hardware background
- [ ] User profiles stored and utilized
- [ ] Secure session management

**5. Content Personalization (50 points):**
- [ ] "Personalize This Chapter" button functional
- [ ] Content adapts based on user profile
- [ ] Personalization meaningful and noticeable
- [ ] Works across multiple chapters

**6. Urdu Translation (50 points):**
- [ ] "Translate to Urdu" button functional
- [ ] Quality translation of technical content
- [ ] Consistent terminology
- [ ] Dynamic toggle between languages

---

### Submission Requirements

**GitHub Repository:**
- Public repository with clear README
- All source code (book, backend, examples)
- Deployment instructions
- Architecture documentation

**Deployed Book:**
- Live URL (GitHub Pages or Vercel)
- Fully functional chatbot
- Authentication working (if implemented)
- Responsive design

**Demo Video (Under 90 Seconds):**
- Book navigation demonstration
- RAG chatbot in action (general + selected text queries)
- Personalization feature (if implemented)
- Translation feature (if implemented)
- Code examples and simulations

**WhatsApp Number:**
- For potential live presentation invitation

---

## VII. Success Metrics

### Educational Effectiveness

**This textbook succeeds when students can:**
- [ ] Explain Physical AI concepts clearly
- [ ] Set up ROS 2 development environment independently
- [ ] Create working Gazebo simulations
- [ ] Integrate NVIDIA Isaac for AI-powered robotics
- [ ] Complete capstone project: voice-controlled autonomous humanoid

### Technical Excellence

**This project succeeds when:**
- [ ] All code examples execute without errors
- [ ] RAG chatbot provides accurate, helpful responses
- [ ] Personalization enhances learning experience
- [ ] Translation maintains technical accuracy
- [ ] Deployment is stable and performant

### Innovation & Impact

**This project stands out when:**
- [ ] RAG integration is seamless and valuable
- [ ] Personalization meaningfully adapts content
- [ ] Reusable intelligence demonstrates future scalability
- [ ] Code quality and documentation exemplary
- [ ] Presentation compelling and professional

---

## VIII. Governance

### Constitutional Authority

**This constitution governs all aspects of textbook development.**

**Precedence:**
1. This constitution (principles and standards)
2. Course requirements (modules, learning outcomes)
3. Technical specifications (ROS 2, NVIDIA Isaac, etc.)
4. Hackathon requirements (deliverables, deadlines)

### Amendment Process

**For Clarifications (PATCH version):**
- Edit directly, increment PATCH version (1.1.0 → 1.1.1)
- Document in Sync Impact Report
- Commit with descriptive message
- No template updates required

**For Substantive Changes (MINOR/MAJOR version):**
- Create ADR documenting rationale
- Increment MINOR (1.1.0 → 1.2.0) for new principles/sections
- Increment MAJOR (1.1.0 → 2.0.0) for breaking changes
- Update impacted templates
- Migration guidance if needed
- Update Sync Impact Report with template synchronization status

### Template Synchronization Requirements

**After amending this constitution, agents MUST:**
1. Review plan-template.md Constitution Check section
2. Review spec-template.md user story format requirements
3. Review tasks-template.md task organization requirements
4. Update templates if constitution changes affect their structure
5. Document template updates in Sync Impact Report

---

## X. Constitution Gates

**These gates MUST be checked during the planning phase (plan-template.md "Constitution Check" section).**

### Gate 1: Technical Accuracy
- [ ] All ROS 2 code specifies version (Humble or Iron)
- [ ] All simulation examples specify tool versions (Gazebo 11 / Gazebo Sim / Isaac Sim 2023.1.0+)
- [ ] Hardware specifications verified within 30 days
- [ ] All code examples executable in documented environment

### Gate 2: Learning Progression
- [ ] Chapter prerequisites validated against prior modules
- [ ] Complexity appropriate for module tier (Weeks 1-2 / 3-7 / 8-10 / 11-13)
- [ ] Learning objectives mapped to Bloom's taxonomy
- [ ] Exercises integrate theory and practice

### Gate 3: Simulation-First
- [ ] All robotic concepts introduced in simulation before hardware
- [ ] Simulation workflow documented (Design → Sim → Train → Validate → Deploy)
- [ ] Edge cases and failure modes tested in simulation
- [ ] Performance metrics defined

### Gate 4: AI-Native Workflow
- [ ] Chapter has spec.md with learning objectives
- [ ] Code examples reference specifications
- [ ] AI chatbot integration points identified
- [ ] User stories prioritized and independently testable

### Gate 5: Hardware Reality
- [ ] Hardware recommendations based on actual market availability
- [ ] Pricing verified within 30 days
- [ ] Simulation-only alternative documented
- [ ] Cloud alternative costs calculated

### Gate 6: RAG Integration
- [ ] Chapter content structured for RAG indexing (512 token chunks)
- [ ] Selection-based query points identified
- [ ] Chatbot test questions defined
- [ ] Expected answers documented for validation

### Gate 7: Personalization
- [ ] Content adaptable for beginner/intermediate/advanced levels
- [ ] Code examples available in multiple languages where appropriate
- [ ] Hardware-specific guidance identified
- [ ] Personalization button placement defined

### Gate 8: Multilingual Access
- [ ] Technical terms identified for glossary
- [ ] Translation-appropriate sections marked
- [ ] Code blocks excluded from translation
- [ ] Urdu terminology validated

### Gate 9: Reusable Intelligence
- [ ] Subagents/skills utilized where applicable
- [ ] New skills documented if created
- [ ] Skills contribution to organizational knowledge tracked
- [ ] Reusability across future courses considered

---

## IX. Conclusion

This constitution establishes the governance framework for creating a comprehensive, AI-native textbook on Physical AI and Humanoid Robotics. By adhering to these principles and standards, the project will:

1. **Educate effectively** through progressive, hands-on learning
2. **Integrate AI assistance** via RAG chatbot and personalization
3. **Ensure technical accuracy** through rigorous testing and validation
4. **Support accessibility** via translation and personalization
5. **Demonstrate innovation** through reusable intelligence and modern architecture

**The goal is not just to complete a hackathon submission, but to create a market-defining educational resource that sets the standard for AI-native technical textbooks in robotics education.**

---

**Version:** 1.1.0 | **Ratified:** 2025-11-29 | **Last Amended:** 2025-11-29

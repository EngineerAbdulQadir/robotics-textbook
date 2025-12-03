---
id: 001
title: Create Physical AI Constitution
stage: constitution
date: 2025-11-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: hackathon-participant
command: /sp.constitution
labels: ["constitution", "initialization", "physical-ai", "robotics", "textbook"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - Constitution validation: All placeholders filled
  - Version consistency check: PASSED
  - Sync Impact Report: Complete
---

## Prompt

https://github.com/panaversity/ai-native-software-development/blob/main/.specify/memory/constitution.md read this constitution link  and create for me like link  constitution file for below hackathon projec Hackathon I: Create a Textbook for Teaching Physical AI & Humanoid Robotics Course
The future of work will be a partnership between people, intelligent agents (AI software), and robots. This shift won't necessarily eliminate jobs but will change what humans do, leading to a massive demand for new skills. We have already written a book on AI agents. Therefore, we want you to write a textbook to teach a course in Physical AI & Humanoid Robotics (The course details are documented below).

Excel in the Hackathon and Launch Your Journey as an AI Startup Founder 🚀
We've recently launched Panaversity (panaversity.org), an initiative focused on teaching cutting-edge AI courses. Alongside this, we're working on publishing our first book, which you can explore at ai-native.panaversity.org. Our next milestone is to build a portal where authors can create AI-native technical textbooks, and readers can easily access and learn from them using AI Agents. We also plan to publish O/A Level, Science, Engineering, and Medical AI-native books to support students and professionals across disciplines. If you perform well in this hackathon, you may be invited for an interview to join the Panaversity core team and potentially step into the role of a startup founder within this growing ecosystem. You will get a chance to work with Panaversity founders Zia, Rehan, Junaid, and Wania and become the very best. You may also get a chance to teach at Panaversity, PIAIC, and GIAIC.

[Full hackathon requirements including course details, modules, hardware requirements, and deliverables - 4 modules covering ROS 2, Gazebo/Unity, NVIDIA Isaac, and VLA with comprehensive hardware specifications and bonus point opportunities for RAG chatbot, Better-Auth, personalization, and Urdu translation]

## Response snapshot

Created comprehensive constitution for Physical AI & Humanoid Robotics textbook project with following key elements:

**Version:** 1.0.0 (Initial Constitution)
**Ratified:** 2025-11-29

**9 Core Principles Established:**
1. Hands-On Technical Accuracy - All code/simulations must be executable and tested
2. Progressive Complexity - 4-module structure (ROS 2 → Gazebo/Unity → Isaac → VLA)
3. Simulation-First Methodology - Digital twin before hardware deployment
4. AI-Native Workflow Integration - SpecKit Plus, RAG chatbot assistance
5. Hardware Reality and Accessibility - Realistic pricing, cloud alternatives documented
6. Interactive Learning Through RAG Integration - Embedded chatbot with context-aware assistance
7. Personalization Based on User Background - Better-Auth profiling, adaptive content
8. Multilingual Accessibility - English/Urdu translation with technical term handling
9. Reusable Intelligence - Claude Code skills/subagents for future projects

**Technical Architecture Defined:**
- Docusaurus book platform with custom React components
- FastAPI RAG backend (OpenAI Agents/ChatKit SDKs)
- Qdrant Cloud (vector DB) + Neon Postgres (relational DB)
- Better-Auth authentication and user profiling
- Translation service integration

**Hackathon Deliverables Mapped:**
- Core requirements (100 points): Spec-driven book + RAG chatbot
- Bonus opportunities (200 points): Subagents/skills, Better-Auth, personalization, Urdu translation

**Quality Standards:**
- Code quality: Testing, documentation, style guidelines
- Content quality: Technical writing, visual standards, interactivity
- Security: Authentication, input validation, physical safety warnings

## Outcome

- ✅ Impact: Created foundational governance document for entire textbook project; establishes principles, architecture, and quality standards that will guide all development work
- 🧪 Tests: Constitution validation passed; all placeholders filled with project-specific content; no template tokens remaining
- 📁 Files: .specify/memory/constitution.md created (827 lines); Sync Impact Report included
- 🔁 Next prompts: Begin specification phase for Module 1 (ROS 2); create initial chapter specs; develop reusable subagents/skills for content generation
- 🧠 Reflection: Constitution successfully adapted from reference while maintaining SpecKit Plus structure and adding Physical AI-specific requirements (hardware specs, simulation-first, RAG integration, personalization, translation)

## Evaluation notes (flywheel)

- Failure modes observed: None - clean constitution creation from reference template
- Graders run and results (PASS/FAIL): Template validation PASS; placeholder check PASS; version consistency PASS
- Prompt variant (if applicable): N/A - initial constitution creation
- Next experiment (smallest change to try): Test constitution in practice by creating first module specification to validate principles are actionable and complete

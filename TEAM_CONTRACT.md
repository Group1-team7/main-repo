# Team Contract — AISPIRE Capstone Sprint

## 1. Team Roster & Roles
**Team slug:** Group1-team7
**Team name:** Demo Team

| Name | GitHub handle | Preferred contact hours | Phonetic pronunciation |
|---|---|---|---|
| Osaid Ziad Alhawamdeh | OsaidZiad04 | 10:00 AM – 6:00 PM | Oh-sayd |
| Osama Harrab | osamaharrab | 10:00 AM – 6:00 PM | Oh-sah-mah |
| Afrah Alsnaid | afrah24ali | 10:00 AM – 6:00 PM | Af-rah |
| Yamen Ayman | yamenayman | 10:00 AM – 6:00 PM | Yah-men |

## 2. Cooperation Plan

### 2.1 Each teammate's key strengths
*   **Osaid Ziad Alhawamdeh:** AI & Machine Learning Engineer. Expert in Machine Learning (ML) and Deep Learning (DL) architecture, ensuring high-quality baseline models and advanced embedding workflows. Strong in RAG and KG.
*   **Osama Harrab:** Data & Knowledge Engineer. System database specialist, responsible for designing optimal database structures, indexing strategy, and efficient data access paths. Strong in ML, RAG, and KG.
*   **Afrah Alsnaid:** NLP & Communications Engineer. Strong structural focus on NLP applications with key capabilities in leading presentation workflow, communication, and clear executive storytelling. Strong in RAG and KG.
*   **Yamen Ayman:** DevOps & Deployment Engineer. Infrastructure specialist, driving the local Docker Compose stack setup and managing the deployment of cloud pipelines to public platforms.

### 2.2 How your team will use those strengths
Based on each teammate's strengths, the initial work distribution will be as follows:
*   **Osaid:** Core Pipeline, ML/DL Models, RAG & KG Development.
*   **Osama:** Database Systems, Structured Storage, ML Integration, RAG & KG Integration.
*   **Afrah:** RAG/KG Pipelines, Evaluation Metrics, Presentation & Storytelling Lead.
*   **Yamen:** Cloud Infrastructure, API Hosting, RAG/KG Deployment & Performance.

Although responsibilities are initially assigned based on expertise, roles may shift during the sprint as needed. All teammates will participate in discussions, code reviews, testing, and project documentation to ensure everyone understands the entire system.

### 2.3 What each teammate wants to develop
Every member will work closely across tasks to learn from each other's domain knowledge. Osaid will guide the team on advanced modeling, Osama will share database design tips and ML integrations, Afrah will help refine communication styles, and Yamen will lead pair-programming sessions for deployment scripts.

### 2.4 Day-to-day work approach
**Every day at 10:00 AM on Slack.**
**Primary project tracking tool:** GitHub Issues + GitHub Project Board
**Ensuring meaningful ownership for each teammate:** Each teammate will own at least one major feature or component of the project. Tasks will be assigned based on interests and learning goals, while ensuring that everyone contributes to both implementation and collaboration. We will review task distribution during our daily syncs and rebalance responsibilities if anyone has too much or too little work.

## 3. Conflict Plan

### 3.1 Process for resolving disagreement
All decisions regarding project scope, architecture, or features will be settled via a majority vote after an open, collaborative discussion. Every member must be allowed to explain their perspective fully before a vote is taken.

### 3.2 If one teammate is dominating or steamrolling
If a team member dominates discussions or pushes code unilaterally, the team will address this kindly during the shutdown ritual. If internal conflicts cannot be resolved through open dialogue, the team will immediately escalate to the Support Instructor, then the Lead Instructor.

### 3.3 If one teammate is under-contributing or missing check-ins
If a teammate falls behind or misses a daily standup, the team will reach out with empathy to understand the underlying cause. If a teammate faces an emergency or unpredictable personal event, the remaining members will actively cooperate and distribute the workload to assist them until the situation settles.

### 3.4 Handling mismatched skill levels
The team will handle mismatched skill levels through coaching, pair programming, code reviews, and early communication. More experienced teammates guide and explain but do not take over the full task.

### 3.5 Escalation path
1. Support Instructor (facilitation)
2. Lead Instructor (final word)
**Confirmed:** Yes - All teammates agree to the escalation order.

## 4. Communication Plan

### 4.1 Availability
**Core Working Hours:** 10:00 AM – 6:00 PM
**Daily sync time:** Every day at 10:00 AM on Slack.

### 4.2 Platforms
*   **Async text:** Slack
*   **Live meetings:** Slack / Zoom
*   **Code review:** GitHub PRs on team repo
*   **Shared docs:** Google Drive

### 4.3 After-hours + weekend expectations
A firm **Soft Stop is set at 12:00 AM (Midnight)**. No team member is expected to read, respond to, or acknowledge Slack messages or pull requests between 12:00 AM and 9:00 AM the following morning.

### 4.4 If a teammate falls behind
The team will identify the issue early during the daily stand-up, discuss any blockers, offer assistance where needed, and adjust task priorities if necessary.

### 4.5 Ensuring every voice is heard
The team values a respectful, inclusive, judgment-free environment where every member feels comfortable expressing ideas, asking questions, admitting challenges, and giving constructive feedback.

## 5. Work Plan

### 5.1 Task identification, assignment, tracking
The project will be divided into small, manageable tasks using GitHub Issues and the GitHub Project Board. Tasks will move sequentially from *Backlog* to *In progress*, *In review*, and *Done*.
**Definition of Done (DoD):** A task is officially marked as "Done" only when the code compiles without errors, has corresponding validation tests, contains zero hardcoded secrets, is well-documented in the README or inline comments, and passes the required peer reviews.

### 5.2 Anti-siloing note
To ensure full system visibility, no feature will be written or managed by a single engineer in absolute isolation. We will enforce joint review sessions and pair-programming blocks for complex milestones. Every PR requires two teammate approvals before merging to main.

### 5.3 No-solo-committing rule
Working alone or committing directly to the repository during off-hours without notifying the team is strictly prohibited. All work must flow through explicit branches and pull requests.

## 6. Git Process

### 6.1 Team GitHub org, repo, and Project board
*   **Team Organization URL:** https://github.com/Group1-team7
*   **Repository URL:** https://github.com/Group1-team7/main-repo
*   **GitHub Project Board URL:** https://github.com/orgs/Group1-team7/projects/1
*   **Confirmed:** every teammate an org Owner; instructional team invited as Members with Write access.

### 6.2 Branch strategy
We follow an Agile feature-branch workflow. No member commits directly to `main`. Every feature or fix must live in a descriptive branch (e.g., `feature/rag-pipeline` or `fix/db-connection`).

### 6.3 PR review workflow
*   Every pull request strictly requires **2 teammate approvals** before it can be merged.
*   Stale approvals will be automatically dismissed when new commits are pushed.
*   The author or a designated reviewer clicks the merge button only after both approvals land.

### 6.4 Merge cadence
The team will merge completed work into main regularly, typically during or after the daily sync, and whenever a change is ready to unblock other teammates.

### 6.5 GitHub Project board - how your team runs it
*   Columns: Backlog / In progress / In review / Done
*   Every task is a card with an owner.
*   Automations: PR opened → In Review; PR merged → Done.
*   If a card sits in In progress for more than 24 hours without a note, it's raised at standup.

### 6.6 Post-cohort plan for your GitHub org
*   **Keep org active for portfolio purposes?** Yes.
*   **Allow personal forks of main-repo?** Yes.
*   **Notice period before deleting the org:** Minimum 30 days' notice.
*   **License on main-repo:** MIT License.

## 7. Sign-off
*   Osaid Ziad Alhawamdeh (@OsaidZiad04) — reviewed and agrees.
*   Osama Harrab (@osamaharrab) — reviewed and agrees.
*   Afrah Alsnaid (@afrah24ali) — reviewed and agrees.
*   Yamen Ayman (@yamenayman) — reviewed and agrees.

**Date completed:** 6 July 2026

## 8. Mid-sprint revisit
The team agrees to bring this contract to the required Progress Check Zoom appointment on Sunday, July 12, or Monday, July 13. We will review our working velocity, mental health markers, and sustainability norms, updating any sections that no longer serve the team's goals.

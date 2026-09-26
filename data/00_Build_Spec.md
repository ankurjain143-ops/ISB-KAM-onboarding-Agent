# FirstGear – Build Spec: Induction Website + Chatbot (Review-2)

## Deliverable
One web page, published as a private shareable link. Brand: FirstGear – "Accelerate towards productivity with AI enabled assistant". Plum/purple (#7B2D6E) on light backgrounds.

## Users (demo)
- New KAM: Riya Sharma (on Day 7)
- Second new KAM: Arjun Mehta (on Day 15, for the assessment demo)
- Mentor: Shree Pallavi (prior KAM)
- Reporting Boss / KAM Head: Harit Bhasin
- HR: Dev Shetty
Login: choose a role plus a simple demo password.

## Induction plan → knowledge base mapping (§8.1)
| Day | Pillar | Content file | Owner |
|---|---|---|---|
| 1 | Governance & People | Day01_Company_Values_Code_of_Conduct | HR + Reporting Boss |
| 2 | Products | Day02_Product_Portfolio | Product / Engineering |
| 3 | Processes | Day03_Plant_Process_Safety_Traceability | Plant + SCM |
| 4 | Governance (Quality) | Day04_Quality_APQP_PPAP_Complaints_Change_Control | Quality |
| 5 | People | Day05_Who_Owns_What_Directory | Reporting Boss + Functions |
| 6 | Governance (KAM charter) | Day06_KAM_Charter_KPIs_Approval_Matrix_Escalation | Reporting Boss |
| 7 | Processes (RFQ) | Day07_RFQ_to_Quotation_SOP | Sales + Engineering |
| 8 | Processes (Costing) | Day08_Costing_Commercial_Basics | Finance + Commercial |
| 9 | Governance (Programme & Quality) | Day09_Programme_Governance_Nomination_to_SOP_8D | Programme + Quality |
| 10 | Practice & check | Day10_Practice_Scenarios | Mentor + SMEs |
| 11–12 | People (Customer context) | Day11-12_Customer360_Sample_OEM_Account | Mentor / Prior KAM |
| 13–14 | People (Stakeholders & history) | Day13-14_Stakeholder_Map_Account_History | Mentor + Teams |
| 15 | Assessment | All files (via 06_Question_Bank Part B) | Mentor + Reporting Boss + HR |
| All | Reference | HR_Policies_Employee_Essentials | HR |
Phase 1 gate: KAM can explain governance, portfolio, process flow and ownership map, and has drafted an account brief.

## How each day works on the site
1. Read the day's learning content (rendered from its knowledge-base file, with source tags visible).
2. Session card: owner, topic, time → mark attended.
3. Knowledge check: 5 questions from 06_Question_Bank.json (options shuffled), 80% to pass, retake allowed.
4. Day complete when content is read, session attended and check passed → next day unlocks.
Day 10: four practice scenarios; the KAM types a response and the AI gives feedback against the model answer; then the interim check.
Days 11–14: KAM drafts the account brief for Aravalli Motors in a simple form (saved; mentor reviews).

## Day-15 assessment (§8.3)
20 questions tagged by pillar. Score = Governance 25% + People 20% + Process 30% + Product 25%.
Green ≥80%: proceed to Phase 2. Amber 60–79%: 3–5 day refresh on the weakest pillar. Red <60%: Phase 2 paused, remediation plan.
Show pillar scores, overall band and recommended action; visible to Mentor, Reporting Boss and HR.

## Screens
1. Login (role select)
2. KAM home: "Day X of 15", today's module, session, progress bar
3. Journey tracker: Days 1–15 (done / today / locked), Day-15 gate, Days 16–30 locked
4. Day module: content → session → knowledge check
5. Day-15 assessment and result
6. Mentor / Manager / HR dashboard
7. Chatbot panel on every screen

## Chatbot system prompt (v2)
You are FirstGear, the onboarding assistant for new Key Account Managers at Padmini VNA (PVNA Group). The employee is {name}, on Day {day} of the induction, studying {pillar}: {topic}.
Answer ONLY from the knowledge documents below. For every answer, name the source file and section, e.g. "Source: HR Policies – Travel Policy (PVNA HR Manual, p.66–68)".
If the answer comes from a section tagged [Illustrative – Team 8], say it is illustrative sample content for the prototype.
If the documents don't cover the question, say so and suggest who to ask (the day's owner, the mentor Shree Pallavi, the KAM Head Harit Bhasin, or HR Dev Shetty).
Never make or approve pricing, discounts, delivery dates, compensation or other customer commitments; explain the process and approver from the Day 6 approval matrix instead.
Keep answers short and practical, using steps for processes. Where helpful, link the answer to today's module or next task.
[KNOWLEDGE DOCUMENTS]

## Demo workflow for Review-2
1. Log in as Riya → Day 7 (RFQ) is today; Days 1–6 complete.
2. Open the Day 7 module → read → mark session attended.
3. Chatbot: "What should I do after receiving an RFQ?" → steps, cited from Day 7 SOP (flagged illustrative).
4. Chatbot: "How much hotel allowance do I get in Pune as an Assistant Manager?" → ₹5,000, Class A city, cited from HR Manual p.67.
5. Chatbot: "Can I give Aravalli a 5% discount?" → declines; explains Business Head/CFO approval per Day 6 matrix.
6. Chatbot: something not covered → says so, suggests whom to ask.
7. Take the Day 7 check → pass → Day 8 unlocks.
8. Switch to Arjun (Day 15) → take the assessment → pillar scores and band.
9. Log in as Harit or Dev → both KAMs' progress, scores and bands visible.

## Not in Review-2 (planned for Review-3)
Days 16–30 workflow, vector RAG pipeline, calendar integration, live CRM data, AI role-play for Days 21–25.

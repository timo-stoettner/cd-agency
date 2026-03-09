# When to Use Which Agent

> A decision tree and quick-reference matrix to pick the right agent for any content design task.

---

## Quick Decision Flowchart

```
START: What kind of content work do you need?
│
├─ Writing NEW content?
│  ├─ Error messages ──────────────────────► Error Message Architect
│  ├─ Onboarding flows ───────────────────► Onboarding Flow Designer
│  ├─ Push/email/in-app notifications ────► Notification Content Designer
│  ├─ CTAs and conversion copy ───────────► CTA Optimization Specialist
│  ├─ Empty states / placeholders ────────► Empty State & Placeholder Specialist
│  ├─ Search UI (bars, filters, no-results)► Search Experience Writer
│  ├─ Chatbot / voice assistant dialogue ─► Conversational AI Designer
│  ├─ Technical docs / API references ────► Technical Documentation Writer
│  ├─ Privacy policies / legal text ──────► Privacy & Legal Content Simplifier
│  ├─ Mobile-specific microcopy ──────────► Mobile UX Writer
│  ├─ Content for multiple locales ───────► Localization Content Strategist
│  └─ General UX writing / not sure ──────► Content Designer Generalist
│
├─ REVIEWING existing content?
│  ├─ Checking tone / brand voice ────────► Tone Evaluation Agent
│  ├─ Polishing microcopy (buttons, labels)► Microcopy Review Agent
│  ├─ Accessibility / WCAG compliance ────► Accessibility Content Auditor
│  ├─ Localization readiness ─────────────► Localization Content Strategist
│  └─ General content audit ──────────────► Content Designer Generalist
│     (then route to specialists as needed)
│
└─ Not sure / need guidance?
   └─ Start with ─────────────────────────► Content Designer Generalist
      (the Generalist will suggest which specialist to hand off to)
```

---

## Quick Reference Matrix

| Task                                | Generalist | Error | Microcopy | Tone | A11y | Onboard | TechDoc | CTA | Mobile | L10n | Notify | Privacy | Empty | Search | ConvAI |
|-------------------------------------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| Button labels                       |  +  |     |  **P**  |     |     |     |     |  +  |  +  |     |     |     |     |     |     |
| Error messages                      |  +  |  **P**  |  +  |     |     |     |     |     |     |     |     |     |     |     |     |
| Tooltips                            |  +  |     |  **P**  |     |     |     |     |     |     |     |     |     |     |     |     |
| Form labels & hints                 |  +  |     |  **P**  |     |  +  |     |     |     |  +  |     |     |     |     |     |     |
| Onboarding screens                  |     |     |     |     |     |  **P**  |     |  +  |     |     |     |     |  +  |     |     |
| Push notifications                  |     |     |     |     |     |     |     |     |  +  |     |  **P**  |     |     |     |     |
| Email notifications                 |     |     |     |     |     |     |     |  +  |     |     |  **P**  |     |     |     |     |
| In-app alerts/toasts                |     |     |  +  |     |     |     |     |     |  +  |     |  **P**  |     |     |     |     |
| CTAs / conversion copy              |     |     |  +  |     |     |     |     |  **P**  |     |     |     |     |     |     |     |
| Empty states                        |  +  |     |     |     |     |  +  |     |     |     |     |     |     |  **P**  |     |     |
| Loading messages                    |     |     |     |     |     |     |     |     |     |     |     |     |  **P**  |     |     |
| Search bar placeholders             |     |     |     |     |     |     |     |     |     |     |     |     |  +  |  **P**  |     |
| No-results pages                    |     |     |     |     |     |     |     |     |     |     |     |     |  +  |  **P**  |     |
| Filter & facet labels               |     |     |  +  |     |     |     |     |     |     |     |     |     |     |  **P**  |     |
| Chatbot dialogue                    |     |     |     |     |     |     |     |     |     |     |     |     |     |     |  **P**  |
| Voice assistant scripts             |     |     |     |     |     |     |     |     |     |     |     |     |     |     |  **P**  |
| API documentation                   |     |     |     |     |     |     |  **P**  |     |     |     |     |     |     |     |     |
| SDK guides                          |     |     |     |     |     |     |  **P**  |     |     |     |     |     |     |     |     |
| Privacy policy simplification       |     |     |     |     |     |     |     |     |     |     |     |  **P**  |     |     |     |
| Cookie/consent banners              |     |     |     |     |     |     |     |     |     |     |     |  **P**  |     |     |     |
| Terms of service rewrite            |     |     |     |     |     |     |     |     |     |     |     |  **P**  |     |     |     |
| Tone/voice audit                    |     |     |     |  **P**  |     |     |     |     |     |     |     |     |     |     |     |
| Brand voice alignment               |     |     |     |  **P**  |     |     |     |     |     |     |     |     |     |     |     |
| Accessibility audit                 |     |     |     |     |  **P**  |     |     |     |     |     |     |     |     |     |     |
| Plain language rewrite              |  +  |     |     |     |  **P**  |     |     |     |     |     |     |  +  |     |     |     |
| WCAG compliance check               |     |     |     |     |  **P**  |     |     |     |     |     |     |     |     |     |     |
| Alt text writing                    |     |     |     |     |  **P**  |     |     |     |     |     |     |     |     |     |     |
| Localization readiness audit        |     |     |     |     |     |     |     |     |     |  **P**  |     |     |     |     |     |
| Translation glossary                |     |     |     |     |     |     |     |     |     |  **P**  |     |     |     |     |     |
| i18n content guidelines             |     |     |     |     |     |     |     |     |     |  **P**  |     |     |     |     |     |
| Mobile microcopy optimization       |     |     |  +  |     |     |     |     |     |  **P**  |     |     |     |     |     |     |
| General content audit               |  **P**  |     |     |  +  |  +  |     |     |     |     |     |     |     |     |     |     |
| Full UX writing (any)               |  **P**  |     |     |     |     |     |     |     |     |     |     |     |     |     |     |

**Legend**: **P** = Primary agent (start here) | **+** = Supporting agent (useful follow-up)

---

## Common Multi-Agent Handoff Patterns

### Pattern 1: Write → Review → Polish
1. **Specialist** writes the content (Error Architect, Onboarding Designer, etc.)
2. **Tone Evaluation Agent** checks brand voice alignment
3. **Microcopy Review Agent** polishes for clarity and conciseness
4. **Accessibility Content Auditor** validates WCAG compliance

### Pattern 2: Full Content Audit
1. **Content Designer Generalist** scans for overall issues
2. Routes to specialists based on findings:
   - Tone issues → **Tone Evaluation Agent**
   - Accessibility gaps → **Accessibility Content Auditor**
   - Microcopy problems → **Microcopy Review Agent**

### Pattern 3: Mobile Content Pipeline
1. Write content with the relevant specialist (any agent)
2. **Mobile UX Writer** optimizes for mobile constraints
3. **Notification Content Designer** creates push/in-app variants

### Pattern 4: Global Launch
1. Write content with the relevant specialist
2. **Localization Content Strategist** audits for i18n readiness
3. **Accessibility Content Auditor** ensures inclusive language
4. **Content Designer Generalist** harmonizes voice across all assets

### Pattern 5: Error → Help → Resolution
1. **Error Message Architect** drafts the error message
2. **Technical Documentation Writer** creates the help article
3. **Mobile UX Writer** creates the mobile-optimized variant

---

## Generalist vs. Specialist: When to Use Which

| Scenario | Use Generalist | Use Specialist |
|----------|:-:|:-:|
| You know exactly what type of content you need | | X |
| You're not sure where to start | X | |
| You need a full content audit across multiple areas | X (as coordinator) | |
| You need deep expertise in one content type | | X |
| You're working on a single UI element (button, error, etc.) | | X |
| You want a quick first draft of mixed content types | X | |
| You need production-quality output for a specific format | | X |
| You're building a multi-step workflow | X (as entry point) | X (as steps) |

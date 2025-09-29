# User Story Template

This document provides the template and guidelines for writing clear, actionable, and adaptable User Stories. The goal is to ensure that stories focus on user value, help teams collaborate effectively, and support development and quality processes.

> **Note:** This structure serves as guidance, not a strict format. Stories may deviate when appropriate, based on the nature of the feature.

---

## General Guidelines for PMs

- **Story Titles:** Short and descriptive. No "As a user..." phrasing.
    
    Example: `[Date Filter] Remove tooltip from Smart Toolbar Tags`
    
- **Tag Stories:** Use `[Feature]` tags in titles to organize stories within epics.
- **Log Key Decisions:** Use Jira comments to capture decisions and scope changes.
- **Clarify Expectations:** Set meetings if expectations or impacts are unclear across teams.
- **Internal Notes:** Use `(Not for QC)` when sections are for Dev/Design only.
- **Avoid Story Splitting:** Keep UI and logic together when possible. Use subtasks within the story instead of splitting.

---

## ***Template Start***

---

### **FEATURE CONTEXT (Recommended)**

Before defining the story details, briefly explain:

- **What this feature is.**
- **Why this feature is needed.**
- **Who benefits from it (target user or group).**
- **What problem or need it addresses.**

*(Use this as a clear framing statement for Dev, QC, and non-technical stakeholders.)*

---

### **ACCEPTANCE CRITERIA**

- Format: **Gherkin (Given-When-Then)** is preferred.
    - **Given:** Initial context or conditions.
    - **When:** Action performed by the user or system.
    - **Then:** Expected result or outcome.
- If unsuitable, use structured bullet points.

✅ Include:

- Positive scenarios (happy path).
- Negative scenarios (when things fail or shouldn't proceed).

---

### **DESIGN (Include if Applicable)**

- Include Figma/URL links if available.
- Approval status.
- Clearly indicate if this section is **not required**.

#### **Design Components Reference**
- **Component Library**: Reference specific UI components from design system
- **Design Patterns**: Document interaction patterns and user flows
- **Visual Specifications**: Include spacing, typography, and color requirements
- **Responsive Behavior**: Define responsive design requirements

#### **Design System Integration**
- **Design Tokens**: Colors, typography scales, spacing values
- **Component Variants**: Available component states and variations
- **Accessibility Guidelines**: WCAG compliance and accessibility features
- **Brand Guidelines**: Consistency with brand standards

---

### **FUNCTIONAL DETAILS**

Explain how the feature should work in detail:

- Core functionality.
- Field validations (Empty, Max, Min, etc.).
- Special workflows, logic, or requirements.
- **Design-driven functionality**: Behavior defined by design interactions and patterns.

> **Note:** While Figma provides visual specifications, key functional requirements must be explicitly documented here. Reference design components and their expected behavior.

---

### **DEPENDENCIES (Include if Applicable)**

- Technical dependencies (parent/child logic, backward compatibility, shared components, etc.).
- Dependencies on other teams, features, or ongoing work.

---

### **SPECIAL CASES / EDGE CASES / LIMITATIONS**

Describe any migration needs, limitations, legacy system support (e.g. SP2016), or other unusual considerations.

---

### **ERROR HANDLING**

- List potential failures and error messages.
- Define fallback behaviors where necessary.

---

### **TESTING & VALIDATION**

- **QC Automation**
    - Required data attributes (`data-testid`).
    - Scenarios requiring automation.
- **QC Manual**
    - Test environments or URLs (if the story is for specific environment only).
    - Required permissions or roles.
    - Browser or language considerations.
    
    > **Note:** Product areas testers should focus on are always mandatory to be indicated in "Affected Areas" field. 
    
- **Design Review Needs** - UI/UX validation including:
  - Design system compliance verification
  - Component usage validation against design specifications
  - Interaction pattern testing against design prototypes
  - Visual regression testing for design consistency
- **Content Needs (Optional)** - articles, videos, review of the feature.
- **Marketing Needs (Optional)** - website page, social media, webinars.
- **Feature Requestor (Optional)** - indicate who requested this feature if different from the usual person/team.
- **Security review / Legal / Other (If Any)**

> *Skip subcategories when not applicable, but preserve the structure.*

---

## ***Template End***

---

## **Example User Story**

---

***Title: [Page Builder] Implement Dark Mode in Page Builder*** 

### **FEATURE CONTEXT**

This feature introduces a **Dark Mode option** for the Page Builder UI. It is needed to reduce eye strain for users working at night or in low-light environments and to improve accessibility for users sensitive to bright light.

The feature will benefit all users, primarily designers who spend extended time in the interface.

---

### **ACCEPTANCE CRITERIA**

**Scenario 1: Enabling Dark Mode**

- **Given** the user is in page edit mode
- **When** the user enables the Dark Mode toggle in the page header,
- **Then** the entire Page Builder UI should switch to Dark Mode immediately without reloading.

**Scenario 2: Remembering Preference**

- **Given** Dark Mode is enabled,
- **When** the user logs out and logs back in,
- **Then** the system should remember and apply Dark Mode automatically.

**Scenario 3: Fallback in Case of Error**

- **Given** Dark Mode fails to load,
- **When** the CSS file cannot be applied,
- **Then** the Builder should fallback to Light Mode and display the message:
    
    > "Dark Mode could not be applied. You are now using Light Mode."

---

### **DESIGN**

- Designs provided in Figma: [link]
- Designs approved by the UX team.

#### **Design Components Reference**
- **Button Component**: Use "Primary Button" variant from design system for main actions
- **Card Component**: Apply "Elevated Card" style with subtle shadow and rounded corners
- **Input Component**: Implement "Search Input" variant with search icon and clear functionality
- **Navigation Pattern**: Follow "Breadcrumb Navigation" pattern for page hierarchy

#### **Design System Integration**
- **Color Tokens**: Use "brand-primary" for main actions, "neutral-600" for text
- **Typography Scale**: Apply "heading-2" for page titles, "body-regular" for content
- **Spacing Values**: Use "spacing-4" for component margins, "spacing-2" for internal padding
- **Component States**: Include hover, focus, and disabled states following design system

---

### **FUNCTIONAL DETAILS**

- Dark Mode toggle is located in the page header using the "Toggle Button" component from design system.
- Preference should be stored at the **account level** (not device-specific).
- Default state is Light Mode with smooth transition to Dark Mode.
- Must support both classic and modern SharePoint experiences with appropriate fallbacks.
- Dark Mode should affect **all screens** including preview, popups, and notifications using design system color tokens.
- Should follow WCAG color contrast guidelines with design system accessibility features.
- **Design-driven functionality**: Button hover states follow design system "Interactive Button" pattern with elevation changes.

---

### **DEPENDENCIES**

- Requires coordinated deployment with global CSS variable strategy.

---

### **SPECIAL CASES / EDGE CASES**

- On SP2019 environments, fallback to Light Mode if CSS variables unsupported.
- No "flash" of Light Mode allowed when preference is Dark Mode.

---

### **ERROR HANDLING**

- If theme switch fails, fallback to Light Mode.
- Display toast notification for fallback events.

---

### **TESTING & VALIDATION**

**QC Automation:**

- Use `data-testid="dark-mode-toggle"`.
- Prepare separate smokes suite for this implementation.

**QC Manual:**

- Validate on both modern and classic SP layouts.

**Design Review Needs** - UI/UX validation including:
- Design system compliance verification for all color tokens and typography scales
- Component usage validation against design specifications for toggle button and card components
- Interaction pattern testing against design prototypes for smooth transitions
- Visual regression testing for design consistency across all affected screens

**Content Needs** - the team should prepare an article, request has been added here: [link].

**Feature requestor** - Claudio, Professional Services.

---

## 🫵 **Reminder**

> Stories are for collaboration. Use this template to facilitate understanding, not as a bureaucratic formality. Adapt sections when needed.

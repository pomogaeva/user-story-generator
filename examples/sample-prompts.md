# Sample Prompts and Expected Outputs

This document contains example prompts and their expected user story outputs to help understand how the automated workflow works.

## Example 1: New Feature

### Prompt
```
Create a user story for implementing a bulk export functionality in the Document Library web part that allows users to export multiple selected documents as a ZIP file. This is needed for users who want to download multiple documents at once instead of downloading them one by one. Fix versions: 8.9.0, QC Severity: Medium
```

### Expected Title
`[Document Library] Implement Bulk Export to ZIP Functionality`

### Key Sections Expected
- **Feature Context**: Explaining bulk export need and user benefit
- **Acceptance Criteria**: Gherkin scenarios for selecting files, export process, error handling
- **Functional Details**: ZIP creation, file size limits, progress indicators
- **Testing & Validation**: Browser compatibility, large file testing

## Example 2: Bug Fix

### Prompt
```
Create a user story for fixing the issue where the People Directory search filter doesn't work when special characters are entered. Users cannot search for names with apostrophes, hyphens, or accented characters. Fix versions: 8.8.1, Issue type: Bug, QC Severity: High
```

### Expected Title
`[People Directory] Fix Search Filter with Special Characters`

### Key Sections Expected
- **Feature Context**: Current bug description and impact
- **Acceptance Criteria**: Various special character scenarios
- **Functional Details**: Character encoding, search logic
- **Error Handling**: Invalid input handling

## Example 3: Enhancement

### Prompt
```
Create a user story for adding keyboard navigation support to the Image Carousel web part. This will improve accessibility compliance and help users navigate through images using arrow keys and tab navigation. Fix versions: 8.9.0, QC Severity: Low
```

### Expected Title
`[Image Carousel] Add Keyboard Navigation Support`

### Key Sections Expected
- **Feature Context**: Accessibility improvement rationale
- **Acceptance Criteria**: Keyboard shortcuts and navigation flows
- **Dependencies**: ARIA compliance requirements
- **Testing & Validation**: Screen reader testing, accessibility validation

## Example 4: Integration Feature

### Prompt
```
Create a user story for integrating the Event Calendar web part with Microsoft Teams to allow users to join virtual meetings directly from calendar events. This integration should support both Teams meetings and external meeting platforms. Fix versions: 8.10.0, QC Severity: Medium
```

### Expected Title
`[Event Calendar] Integrate Microsoft Teams Meeting Links`

### Key Sections Expected
- **Feature Context**: Teams integration benefits
- **Acceptance Criteria**: Meeting link detection and join functionality
- **Dependencies**: Microsoft Graph API, authentication requirements
- **Special Cases**: External meeting platforms, permission handling

## Example 5: Complex Feature with Dependencies

### Prompt
```
Create a user story for implementing a real-time collaboration feature in the Rich Text Editor that allows multiple users to edit content simultaneously with live cursors and conflict resolution. This requires WebSocket integration and user presence indicators. Fix versions: 8.11.0, QC Severity: High, Epic: Real-time Collaboration
```

### Expected Title
`[Rich Text Editor] Implement Real-time Multi-user Collaboration`

### Key Sections Expected
- **Feature Context**: Collaborative editing value proposition
- **Acceptance Criteria**: Multiple user scenarios, conflict resolution
- **Dependencies**: WebSocket infrastructure, SignalR integration
- **Special Cases**: Network interruptions, user permissions
- **Testing & Validation**: Concurrent user testing, performance validation

## Prompt Pattern Guidelines

### Effective Prompts Include:
1. **Clear feature description** - What needs to be built
2. **User context** - Who benefits and why
3. **Business justification** - Why it's important
4. **Technical context** - Any constraints or requirements
5. **Required fields** - Fix versions, severity, etc.

### Less Effective Prompts:
- "Make the UI better" (too vague)
- "Fix all the bugs in the calendar" (too broad)
- "Add AI to everything" (unclear scope)
- Missing fix versions or required fields

## Iteration Examples

### Initial Prompt
```
Create a user story for adding dark mode. Fix versions: 8.9.0
```

### Follow-up Refinements
```
Add more specific acceptance criteria for the dark mode toggle placement
Include error handling for when dark mode CSS fails to load
Add testing requirements for both SharePoint environments
Specify that preference should be saved per user account
```

### Final Result
A comprehensive user story with detailed acceptance criteria, error handling, cross-environment testing, and user preference persistence.

## Custom Field Examples

### Using Different Issue Types
```
Create a design task for creating mockups for the new dashboard layout. 
Fix versions: 8.9.0, Issue type: Design Task, QC Severity: Low
```

### Specifying Epic/Parent
```
Create a user story for implementing user authentication in the mobile app. 
Fix versions: 8.10.0, Epic: Mobile App Development, QC Severity: High
```

### Multiple Fix Versions
```
Create a user story for updating the REST API to support new filtering options. 
Fix versions: 8.9.0, 8.10.0, QC Severity: Medium
```

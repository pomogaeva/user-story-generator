# Automated User Story Creation Workflow

## Overview

This workflow automates the creation of user stories from natural language prompts to Jira tickets, following ShortPoint's comprehensive template.

## Step-by-Step Process

### Step 1: User Prompt
**Required Information:**
- Feature description (what functionality needs to be implemented)
- Fix versions (mandatory)

**Optional Information:**
- QC Severity (defaults to "Low")
- Issue type (defaults to "Story")
- Epic/Parent ticket (if applicable)

**Example Prompts:**
```
Create a user story for implementing a dark mode toggle in the Page Builder. 
Fix versions: 8.8.0, QC Severity: Medium
```

```
Create a user story for adding bulk delete functionality to the Document Library web part.
Fix versions: 8.9.0, QC Severity: High, Issue type: Story
```

```
Create a bug report for the search filter not working in the People Directory.
Fix versions: 8.8.1, Issue type: Bug
```

### Step 2: AI Story Generation
The AI will generate:
- **Title**: Following `[Feature]` tag format
- **Description**: Using the comprehensive template with:
  - Feature Context
  - Acceptance Criteria (Gherkin format preferred)
  - Functional Details
  - Dependencies (if applicable)
  - Special Cases/Edge Cases
  - Error Handling
  - Testing & Validation sections

### Step 3: Review & Iteration
- Review the generated story
- Request changes if needed ("make the acceptance criteria more specific", "add error handling for network failures", etc.)
- Iterate until satisfied with the content
- AI will refine sections based on feedback

### Step 4: Jira Ticket Creation
Once approved, automatic creation with:
- All required SPX project fields populated
- Proper field mappings applied
- Ticket created and URL provided for immediate access

## Prompt Guidelines

### What to Include
1. **Clear feature description**: What needs to be built/fixed
2. **User context**: Who will use this feature and why
3. **Specific requirements**: Any constraints, integrations, or special needs
4. **Business justification**: Why this feature is important
5. **Known dependencies**: Any related work or prerequisites

### What to Avoid
1. **Vague descriptions**: "Make the UI better"
2. **Technical implementation details**: Let the team decide "how"
3. **Multiple features in one prompt**: Keep it focused
4. **Missing required fields**: Always include fix versions

## AI Capabilities

The AI can:
- **Parse complex requirements** and break them into structured sections
- **Generate Gherkin scenarios** for acceptance criteria
- **Identify edge cases** based on feature description
- **Suggest testing approaches** appropriate for the feature
- **Format content** according to ShortPoint template standards
- **Handle technical context** for SharePoint/Office 365 environments

## Best Practices

### For Better Results
1. **Be specific** in your feature descriptions
2. **Include context** about why the feature is needed
3. **Mention any constraints** or special requirements upfront
4. **Specify the target user group** if not general users
5. **Include any known dependencies** in your initial prompt

### Common Patterns
- **New Features**: Focus on user value and business need
- **Bug Fixes**: Include reproduction steps and expected vs actual behavior
- **Improvements**: Explain current pain points and desired outcomes
- **Integrations**: Mention systems involved and data flow requirements

### Review Checklist
Before approving a story, ensure:
- [ ] Title is clear and uses proper `[Feature]` tagging
- [ ] Feature context explains the "why"
- [ ] Acceptance criteria cover happy path and edge cases
- [ ] Functional details are comprehensive
- [ ] Dependencies are identified
- [ ] Testing requirements are specified
- [ ] Error handling is addressed

## Troubleshooting

### If AI misunderstands the requirement:
- Provide more specific context
- Break down complex features into smaller parts
- Use examples to clarify expected behavior

### If generated story is too generic:
- Add more domain-specific details to your prompt
- Mention specific SharePoint contexts or user scenarios
- Include technical constraints or requirements

### If sections are missing:
- Explicitly ask for specific sections ("include error handling scenarios")
- Mention if integration with other systems is needed
- Specify testing requirements if they're specialized

## Integration Notes

- Stories are created directly in **SPX project**
- **Reporter** is automatically set to Tetiana Pomohaieva
- **Default environments** (Office 365, SharePoint 2019) are applied
- **Package field** is set to 8
- All stories follow **ShortPoint template standards**

## Future Enhancements

Potential improvements to consider:
- Integration with Epic planning
- Automatic story point estimation
- Template variations for different feature types
- Integration with design system documentation
- Automated linking to related tickets

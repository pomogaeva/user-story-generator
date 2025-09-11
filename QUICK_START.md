# Quick Start Guide

Get up and running with automated user story creation in 5 minutes.

## ⚡ Immediate Usage

### 1. Write Your Prompt
Use this template:
```
Create a user story for [YOUR FEATURE DESCRIPTION]. 
Fix versions: [VERSION], QC Severity: [Low/Medium/High]
```

### 2. Get Your Story
The AI will generate a complete user story following ShortPoint's template with:
- Feature context and business justification
- Detailed acceptance criteria in Gherkin format
- Functional specifications
- Testing requirements
- Error handling scenarios

### 3. Review and Refine
Ask for changes like:
- "Make the acceptance criteria more specific"
- "Add error handling for network failures" 
- "Include mobile considerations"

### 4. Create Jira Ticket
Say "Create the Jira ticket" and it will be automatically created in SPX project.

## 📝 Example Usage

**Your prompt:**
```
Create a user story for adding a dark mode toggle to the Page Builder interface. 
Users are requesting this to reduce eye strain during extended editing sessions. 
Fix versions: 8.9.0, QC Severity: Medium
```

**You get:** Complete user story with title `[Page Builder] Implement Dark Mode Toggle` and comprehensive description following ShortPoint template.

**Result:** Jira ticket automatically created in SPX project with all fields populated.

## 🎯 What's Included

- **Automated title generation** with proper `[Feature]` tagging
- **Complete template sections**: Context, acceptance criteria, functional details, testing
- **Gherkin scenarios** for clear acceptance criteria  
- **SharePoint-specific considerations** (SP2019, Office 365)
- **Direct Jira integration** with proper field mapping

## 🔧 Requirements

- Cursor with Jira MCP configured ✅
- Access to ShortPoint Atlassian instance ✅ 
- SPX project permissions ✅

## 📚 Need More Help?

- **Examples**: Check `/examples/` folder for sample prompts
- **Template**: See `user-story-template.md` for template details
- **Workflow**: Read `workflow-guide.md` for complete process
- **Configuration**: Review `jira-configuration.md` for technical details

## 🚀 Ready to Start?

Just send your first prompt with a feature description and fix versions. The AI will handle the rest!

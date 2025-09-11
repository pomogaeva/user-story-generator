# Automated User Story Creation with Jira Integration

This project automates the creation of user stories following ShortPoint's comprehensive template and automatically creates Jira tickets in the SPX project.

## Quick Start

1. **Send a prompt** with feature description and required fields:
   ```
   Create a user story for [feature description]. 
   Fix versions: X.X.X, QC Severity: [Low/Medium/High]
   ```

2. **Review and iterate** on the generated story until satisfied

3. **Confirm creation** and the Jira ticket will be automatically created

## Project Structure

- `README.md` - This overview
- `user-story-template.md` - Official ShortPoint user story template
- `workflow-guide.md` - Detailed step-by-step workflow
- `jira-configuration.md` - Jira field mappings and setup details
- `examples/` - Example prompts and generated stories

## Jira Configuration

- **Project**: SPX (ShortPoint X)
- **Default Issue Type**: Story
- **Reporter**: Tetiana Pomohaieva
- **Environments**: Office 365, SharePoint 2019 (default)
- **Package**: 8 (default)

## Dependencies

- Cursor with Jira MCP configured
- Access to ShortPoint Atlassian instance

## How It Works

The system uses AI to:
1. Parse natural language feature descriptions
2. Generate structured user stories following the ShortPoint template
3. Create properly formatted Jira tickets with all required fields
4. Support iterative refinement based on feedback

## Benefits

- **Consistency**: All stories follow the same comprehensive template
- **Speed**: Generate complete user stories in minutes instead of hours
- **Quality**: Structured format ensures nothing is missed
- **Integration**: Direct Jira ticket creation eliminates manual steps

# Jira Configuration and Field Mappings

## Project Details
- **Project**: SPX (ShortPoint X)
- **Project ID**: 10116
- **Project Key**: SPX
- **Instance**: https://shortpoint.atlassian.net
- **Cloud ID**: 62115996-95a8-45a9-8f38-0e2657916bfb

## Field Mappings

### Required Fields
| Field Name | Value | Source | Notes |
|------------|--------|--------|-------|
| Project | ShortPoint X (SPX) | Fixed | Project ID: 10116 |
| Issue Type | Story | Default (or user-specified) | Issue Type ID: 10001 |
| Summary | Generated title | AI-generated | Follows `[Feature]` format |
| Reporter | Tetiana Pomohaieva | Current user | Account ID: 5e57af063df51b0c93759332 |
| Description | Generated description | AI-generated | Markdown format |
| Fix versions | User-provided | User prompt | Must be specified in prompt |

### Default Fields
| Field Name | Default Value | Type | Notes |
|------------|---------------|------|-------|
| Environments | Office 365, SharePoint 2019 | Checkbox | Default selection |
| Package | 8 | Number | Fixed value |
| QC Severity | Low | Select | Can be overridden in prompt |

### Available Issue Types
| Issue Type | ID | Description | Use Case |
|------------|-------|-------------|----------|
| Story | 10001 | User story | Default for new features |
| Task | 10002 | Small distinct work | Non-user-facing work |
| Bug | 10004 | Problem or error | Bug fixes |
| Epic | 10000 | Collection of stories | Large initiatives |
| Sub-task | 10003 | Part of larger task | Breakdown of stories |
| Support Ticket | 10200 | Support requests | Customer issues |
| Business Analysis | 10237 | BA tasks | Analysis work |
| Design Task | 10240 | Design work | UI/UX tasks |
| Test Case | 10242 | Test scenarios | QA test cases |
| Security Ticket | 10243 | Security/vulnerability | Security issues |

## MCP Configuration

### File Location
`/Users/tetianapomohaieva/.cursor/mcp.json`

### Configuration Structure
```json
{
  "mcpServers": {
    "jira": {
      "command": "npx",
      "args": ["-y", "@mcp-devtools/jira"],
      "env": {
        "JIRA_URL": "https://shortpoint.atlassian.net",
        "JIRA_API_MAIL": "tetiana@shortpoint.com",
        "JIRA_API_KEY": "[REDACTED]"
      }
    }
  }
}
```

### User Information
- **Name**: Tetiana Pomohaieva
- **Email**: tetiana@shortpoint.com
- **Account ID**: 5e57af063df51b0c93759332
- **Role**: Product Manager
- **Location**: Valencia, Spain

## API Field Mapping

### Standard Fields (via create issue API)
```json
{
  "fields": {
    "project": {"key": "SPX"},
    "issuetype": {"id": "10001"},
    "summary": "[Generated Title]",
    "description": "[Generated Description]",
    "reporter": {"accountId": "5e57af063df51b0c93759332"}
  }
}
```

### Custom Fields (via additional_fields)
The following fields may require special handling:

- **Environments**: Multi-select checkbox field
  - Office 365
  - SharePoint 2019
  
- **Package**: Number field
  - Default value: 8.
  
- **QC Severity**: Select field
  - Options: Low, Medium, Critical, Blocker
  - Default: Low
  
- **Fix versions**: Version field
  - Must be valid version in SPX project
  - Required for all stories

## Error Handling

### Common Issues and Solutions

1. **Custom Field Errors**
   - Issue: Custom fields not accepted in standard API
   - Solution: Use `additional_fields` parameter or field-specific APIs

2. **Version Not Found**
   - Issue: Specified fix version doesn't exist
   - Solution: Query available versions or create new version

3. **Permission Errors**
   - Issue: User lacks permission to create in project
   - Solution: Verify user permissions and project access

4. **Field Validation Errors**
   - Issue: Required fields missing or invalid format
   - Solution: Validate all required fields before creation

## Testing and Validation

### Pre-Creation Checks
1. Verify project access (`getVisibleJiraProjects`)
2. Validate issue type exists (`getJiraProjectIssueTypesMetadata`)
3. Check user permissions
4. Validate fix versions exist

### Post-Creation Verification
1. Confirm ticket created successfully
2. Verify all fields populated correctly
3. Check custom fields applied
4. Validate ticket accessibility

## Backup and Recovery

### Data Preservation
- All user stories generated are preserved in documentation
- Template and workflow documented for reproducibility
- Configuration backed up in version control

### Fallback Procedures
- Manual ticket creation if API fails
- Copy/paste generated content to Jira web interface
- Alternative field mapping strategies if needed

## Security Considerations

### API Key Management
- API key stored in MCP configuration
- Limited scope to Jira operations only
- Regular rotation recommended

### Access Control
- User-specific reporter field
- Project-specific permissions
- No elevated privileges required

## Monitoring and Maintenance

### Regular Checks
- Verify API connectivity
- Test field mappings with new Jira versions
- Update documentation with project changes
- Monitor for new custom fields or requirements

### Update Procedures
- API key rotation process
- Project configuration changes
- Template updates and versioning
- Workflow refinements based on usage

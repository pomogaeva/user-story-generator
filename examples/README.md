# Examples Directory

This directory contains practical examples of how the automated user story creation workflow works.

## Files in This Directory

### `sample-prompts.md`
Collection of example prompts showing different types of features and the expected user story outputs. Includes:
- New feature development prompts
- Bug fix prompts  
- Enhancement requests
- Integration features
- Complex features with dependencies

### `generated-story-example.md`
Complete example showing:
- Original user prompt
- Full generated user story following ShortPoint template
- Jira field mappings
- Story refinement examples

## Using These Examples

### For Learning the Process
1. Review the sample prompts to understand effective prompt patterns
2. Study the generated story example to see template implementation
3. Note the level of detail and structure in the outputs

### For Reference
- Use sample prompts as templates for your own requests
- Reference the generated story example when reviewing AI outputs
- Check field mappings when creating tickets

### For Training Others
- Share examples with team members learning the workflow
- Use as documentation for the story creation process
- Demonstrate the quality and consistency of automated outputs

## Best Practices from Examples

### Effective Prompts Include:
- Clear feature description and user need
- Business justification
- Technical context or constraints
- All required fields (fix versions, severity, etc.)

### Generated Stories Provide:
- Comprehensive feature context
- Detailed acceptance criteria in Gherkin format
- Complete functional specifications
- Error handling scenarios
- Testing requirements across environments

## Extending These Examples

Feel free to add your own examples to this directory:
- Save successful prompts and their outputs
- Document any special cases or unique requirements
- Create examples for different feature types or domains
- Add examples of iterative refinement processes

## Templates for Quick Reference

### Basic Feature Prompt Template
```
Create a user story for [feature description]. 
[Context about why it's needed and who benefits].
Fix versions: [version], QC Severity: [Low/Medium/High]
```

### Bug Fix Prompt Template  
```
Create a user story for fixing [bug description].
[Current behavior vs expected behavior].
Fix versions: [version], Issue type: Bug, QC Severity: [Low/Medium/High]
```

### Enhancement Prompt Template
```
Create a user story for enhancing [existing feature] to [new capability].
[Explanation of improvement and user benefit].
Fix versions: [version], QC Severity: [Low/Medium/High]
```

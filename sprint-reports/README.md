# 🤖 AI Efficiency Sprint Reports

Automated reporting system that analyzes the impact of AI assistance on developer productivity by comparing traditional development estimates with actual effort when using AI tools.

## 📋 Overview

This system generates reports that track:
- **Dev Story Points**: Traditional development estimates
- **Dev Story Points (With AI)**: Actual effort when developers use AI assistance

The goal is to see **lower numbers** in the AI column, indicating that AI tools are successfully reducing developer effort and increasing productivity.

## 🏗️ Project Structure

```
sprint-reports/
├── ai_efficiency_reporter.py   # Main report generation script
├── scheduler.py                 # Automated scheduling system
├── setup.sh                    # Installation and setup script
├── requirements.txt             # Python dependencies
├── activate.sh                  # Environment activation script (generated)
├── config/
│   └── settings.json           # Configuration settings
├── env_template.txt            # Environment variables template
├── output/                     # Generated reports (created automatically)
├── logs/                       # Application logs (created automatically)
└── venv/                       # Python virtual environment (created during setup)
```

## 🚀 Quick Start

### 1. Setup

Run the setup script to install dependencies and configure the environment:

```bash
cd sprint-reports
./setup.sh
```

### 2. Configuration

Edit the environment file with your Jira credentials:

```bash
cp env_template.txt .env
nano .env  # Add your Jira API token
```

**Required settings:**
- `JIRA_API_TOKEN`: Get from [Atlassian API Tokens](https://id.atlassian.com/manage-profile/security/api-tokens)
- `JIRA_EMAIL`: Your Atlassian account email
- `JIRA_URL`: Your Jira instance URL

### 3. Test the Setup

```bash
source activate.sh
python3 ai_efficiency_reporter.py --help
```

### 4. Generate Your First Report

```bash
python3 ai_efficiency_reporter.py
```

## 📊 Usage

### Manual Report Generation

Generate a report for the current sprint:

```bash
source activate.sh
python3 ai_efficiency_reporter.py
```

Options:
- `--config CONFIG_FILE`: Use custom configuration file
- `--format FORMAT`: Output format (currently supports: markdown)
- `--verbose`: Enable detailed logging

### Automated Scheduling

Start the scheduler to automatically generate reports every second Monday:

```bash
source activate.sh
python3 scheduler.py
```

Scheduler options:
- `--test`: Generate a report immediately (test mode)
- `--check-date`: Check if today is the second Monday of the month
- `--config CONFIG_FILE`: Use custom configuration file

### Testing the Scheduler

```bash
# Test report generation
python3 scheduler.py --test

# Check if today is a report day
python3 scheduler.py --check-date
```

## 📈 Report Format

The generated reports include:

### Developer Performance Table
| Developer | Traditional Estimate | AI-Assisted Effort | Efficiency Gain | % Improvement | Issues |
|-----------|---------------------|-------------------|-----------------|---------------|--------|
| Developer Name | 15.0 | 12.0 | +3.0 | +20.0% | 8 |

### Key Metrics
- Total story points saved/lost
- Overall efficiency percentage
- Top performing developers
- Insights and recommendations

## ⚙️ Configuration

### Environment Variables (.env)

```bash
# Required
JIRA_API_TOKEN=your_api_token_here
JIRA_EMAIL=your.email@company.com
JIRA_URL=https://your-company.atlassian.net

# Optional
OUTPUT_DIR=./output
LOG_LEVEL=INFO
```

### Settings File (config/settings.json)

```json
{
  "jira_url": "https://shortpoint.atlassian.net",
  "email": "tetiana@shortpoint.com",
  "schedule": {
    "enabled": true,
    "day": "monday",
    "time": "09:00"
  },
  "developer_mapping": {
    "account_id": "Developer Name"
  }
}
```

## 🔄 Automation Setup

### Option 1: Run as a Service (Recommended)

Create a systemd service file:

```bash
sudo nano /etc/systemd/system/sprint-reports.service
```

```ini
[Unit]
Description=Sprint AI Efficiency Reports
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/sprint-reports
ExecStart=/path/to/sprint-reports/venv/bin/python scheduler.py
Restart=always
RestartSec=60

[Install]
WantedBy=multi-user.target
```

Enable and start the service:

```bash
sudo systemctl enable sprint-reports
sudo systemctl start sprint-reports
```

### Option 2: Cron Job

Add to your crontab:

```bash
crontab -e
```

```bash
# Run every Monday at 9:00 AM
0 9 * * 1 cd /path/to/sprint-reports && ./venv/bin/python scheduler.py --test
```

### Option 3: GitHub Actions (CI/CD)

Create `.github/workflows/sprint-reports.yml`:

```yaml
name: Sprint Reports
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9:00 AM UTC
  workflow_dispatch:

jobs:
  generate-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Generate Sprint Report
        env:
          JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
          JIRA_EMAIL: ${{ secrets.JIRA_EMAIL }}
        run: |
          cd sprint-reports
          pip install -r requirements.txt
          python ai_efficiency_reporter.py
```

## 🛠️ Customization

### Adding New Developers

Update `config/settings.json`:

```json
{
  "developer_mapping": {
    "new_account_id": "New Developer Name"
  }
}
```

Update the `DEVELOPER_IDS` list in `ai_efficiency_reporter.py`.

### Custom Report Formats

The system currently supports Markdown format. To add new formats:

1. Create a new method in `AIEfficiencyReporter` class
2. Add the format to the argument parser
3. Update the `generate_report` method

### Email Notifications

Add email configuration to your `.env` file:

```bash
EMAIL_NOTIFICATIONS_ENABLED=true
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your-email@company.com
SMTP_PASSWORD=your-app-password
NOTIFICATION_RECIPIENTS=manager@company.com,team-lead@company.com
```

## 🐛 Troubleshooting

### Common Issues

1. **"No issues found"**
   - Check if there are active sprints
   - Verify developer account IDs
   - Ensure custom fields are populated

2. **API Authentication Errors**
   - Verify your API token is correct
   - Check if your Jira email is correct
   - Ensure you have proper permissions

3. **Permission Errors**
   - Make sure scripts are executable: `chmod +x *.py`
   - Verify Jira permissions for the custom fields

### Debug Mode

Run with verbose logging:

```bash
python3 ai_efficiency_reporter.py --verbose
```

Check logs:

```bash
tail -f logs/ai_efficiency_report_$(date +%Y%m%d).log
```

### Testing Connection

```bash
python3 -c "
from ai_efficiency_reporter import JiraClient
import os
client = JiraClient(
    os.getenv('JIRA_URL'),
    os.getenv('JIRA_EMAIL'), 
    os.getenv('JIRA_API_TOKEN')
)
print('Connection successful!')
"
```

## 📝 Output Examples

### Sample Report Output

```markdown
# 🤖 AI Efficiency Sprint Report

**Generated**: 2025-09-17 14:30:00  
**Sprint**: 08-Sep-21-Sep - Sprint 19  
**Total Issues**: 70 issues with both story point fields populated

## 👥 Developer Performance

| Developer | Traditional Estimate | AI-Assisted Effort | Efficiency Gain | % Improvement | Issues |
|-----------|---------------------|-------------------|-----------------|---------------|--------|
| ✅ **John Doe** | 25.0 | 20.0 | +5.0 | +20.0% | 12 |
| ✅ **Jane Smith** | 18.0 | 15.0 | +3.0 | +16.7% | 8 |

## 📈 Analysis

- **Total Traditional Estimates**: 85.5 story points
- **Total AI-Assisted Effort**: 77.0 story points  
- **Overall Efficiency Gain**: +8.5 story points (+9.9%)

### 🎯 Key Insights
✅ **Positive Impact**: AI assistance is reducing overall development effort by 8.5 story points (9.9%)
🏆 **Top Performer**: John Doe with 5.0 story points saved
```

## 📞 Support

For questions or issues:
- Check the logs in `logs/` directory
- Review the configuration in `config/settings.json`
- Verify environment variables in `.env`
- Contact the Engineering Team

## 🔮 Future Enhancements

- [ ] Email/Slack notifications
- [ ] PDF report generation
- [ ] Historical trend analysis
- [ ] Team comparison reports
- [ ] Integration with other tools (Confluence, Notion)
- [ ] Dashboard web interface

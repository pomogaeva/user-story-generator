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
├── generate_sprint_report.py   # Main report generation script
├── scheduler.py                 # Automated bi-weekly scheduling system
├── setup.sh                    # Installation and setup script
├── requirements.txt             # Python dependencies
├── config/
│   └── settings.json           # Configuration settings
├── env_template.txt            # Environment variables template
├── output/                     # Generated reports (created automatically)
├── logs/                       # Application logs (created automatically)
└── README.md                   # This documentation
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
# Install dependencies and setup environment
./setup.sh

# Test the report generator
python3 generate_sprint_report.py
```

### 4. Generate Your First Report

```bash
python3 generate_sprint_report.py
```

## 📊 Usage

### Manual Report Generation

Generate a report for the current sprint:

```bash
python3 generate_sprint_report.py
```

The script automatically:
- Determines the current sprint number (Sprint 19, 20, 21...)
- Fetches data from Jira using MCP tools
- Generates a report with filename: `Sprint_XX_AI_Efficiency_Report_YYYYMMDD_HHMMSS.md`

### Automated Scheduling

Start the scheduler to automatically generate reports bi-weekly (every 2 weeks):

```bash
python3 scheduler.py
```

**Schedule Details:**
- **Frequency**: Every 2 weeks (bi-weekly)
- **Start Date**: September 22, 2025 (Sprint 20)
- **Time**: 9:00 AM UTC
- **Pattern**: Sept 22 → Oct 6 → Oct 20 → Nov 3 → etc.

### Scheduler Commands

```bash
# Check current sprint and next report date
python3 scheduler.py --check-schedule

# Show next 5 scheduled report dates
python3 scheduler.py --next-dates

# Generate a report immediately (test mode)
python3 scheduler.py --test

# Run the continuous scheduler
python3 scheduler.py
```

### Example Output

```bash
$ python3 scheduler.py --check-schedule
Today (2025-09-17) is NOT a sprint report day.
Current Sprint: 19
Next scheduled report: 2025-09-22

$ python3 scheduler.py --next-dates
Next 5 scheduled report dates:
  Sprint 20: 2025-09-22 (Monday)
  Sprint 21: 2025-10-06 (Monday)
  Sprint 22: 2025-10-20 (Monday)
  Sprint 23: 2025-11-03 (Monday)
  Sprint 24: 2025-11-17 (Monday)
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
# Run every Monday at 9:00 AM (scheduler will check if it's a sprint report day)
0 9 * * 1 cd /path/to/sprint-reports && python3 scheduler.py --test
```

**Note:** The scheduler automatically determines if it's a bi-weekly sprint report day (every 2 weeks starting September 22, 2025).

### Option 3: GitHub Actions (CI/CD)

Create `.github/workflows/sprint-reports.yml`:

```yaml
name: Sprint Reports
on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9:00 AM UTC (scheduler checks if it's a sprint day)
  workflow_dispatch:

jobs:
  generate-report:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Python
        uses: actions/setup-python@v4
        with:
          python-version: '3.8+'
      - name: Generate Sprint Report
        env:
          JIRA_API_TOKEN: ${{ secrets.JIRA_API_TOKEN }}
          JIRA_EMAIL: ${{ secrets.JIRA_EMAIL }}
          JIRA_URL: ${{ secrets.JIRA_URL }}
        run: |
          cd sprint-reports
          pip install -r requirements.txt
          python3 scheduler.py --test
      - name: Upload Report
        uses: actions/upload-artifact@v3
        with:
          name: sprint-report
          path: sprint-reports/output/
```

## 🛠️ Customization

### Adding New Developers

Update the `sprint_issues` data in `generate_sprint_report.py` to include issues for new developers:

```python
sprint_issues = [
    # Add new developer entries
    {"key": "SPX-XXXXX", "dev": "New Developer Name", "traditional": 5.0, "ai": 4.0},
    # ... existing entries
]
```

Or better yet, update the script to fetch real-time data from Jira MCP for all team members automatically.

### Custom Report Formats

The system currently supports Markdown format. To add new formats:

1. Modify the `create_sprint_report()` function in `generate_sprint_report.py`
2. Add new format generation logic (PDF, HTML, JSON, etc.)
3. Update the `main()` function to support format selection

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

Check current sprint and schedule:

```bash
python3 scheduler.py --check-schedule
```

Test report generation:

```bash
python3 generate_sprint_report.py
```

Check logs:

```bash
tail -f logs/scheduler.log
```

### Testing Sprint Schedule

```bash
# Check if today is a sprint report day
python3 scheduler.py --check-schedule

# See next 5 report dates
python3 scheduler.py --next-dates

# Generate a test report
python3 scheduler.py --test
```

## 📝 Output Examples

### Sample Report Output

```markdown
# 🤖 AI Efficiency Sprint Report

**Generated**: 2025-09-17 15:53:29  
**Sprint**: Sprint 19  
**Total Issues**: 52 issues analyzed

## 📊 Overview

This report compares traditional development estimates with actual effort when using AI assistance.
The goal is to see **lower numbers** in the AI column, indicating that AI tools are successfully reducing developer effort.

## 👥 Developer Performance

| Developer | Traditional Estimate | AI-Assisted Effort | Efficiency Gain | % Improvement | Issues |
|-----------|---------------------|-------------------|-----------------|---------------|--------|
| ✅ **Nunu Olamilekan** | 19.5 | 15.5 | +4.0 | +20.5% | 16 |
| ✅ **Oluwatoyosi Oyegoke** | 27.0 | 23.5 | +3.5 | +13.0% | 15 |
| ✅ **Stephen Ng'ang'a** | 12.0 | 10.0 | +2.0 | +16.7% | 5 |
| ✅ **Ezekiel Ilori** | 6.5 | 5.5 | +1.0 | +15.4% | 3 |
| ✅ **Abd UlHameed Maree** | 9.5 | 9.0 | +0.5 | +5.3% | 8 |
| ⚠️ **Ebubekir Tabak** | 13.0 | 13.0 | +0.0 | +0.0% | 5 |
| **TOTALS** | **87.5** | **76.5** | **+11.0** | **+12.6%** | **52** |

## 📈 Analysis

- **Total Traditional Estimates**: 87.5 story points
- **Total AI-Assisted Effort**: 76.5 story points
- **Overall Efficiency Gain**: +11.0 story points (+12.6%)
- **Average Issues per Developer**: 8.7

### 🎯 Key Insights
✅ **Positive Impact**: AI assistance is reducing overall development effort by 11.0 story points (12.6%)
🏆 **Top Performer**: Nunu Olamilekan with 4.0 story points saved
```

**Output Files:**
Reports are saved as: `Sprint_19_AI_Efficiency_Report_20250917_155329.md`

## 📞 Support

For questions or issues:
- Check the logs in `logs/` directory
- Review the configuration in `config/settings.json`
- Verify environment variables in `.env`
- Contact the Engineering Team

## 🔮 Future Enhancements

- [ ] Real-time Jira MCP integration (currently uses static data)
- [ ] Email/Slack notifications when reports are generated
- [ ] PDF report generation with charts and graphs
- [ ] Historical trend analysis across multiple sprints
- [ ] Team comparison reports and benchmarking
- [ ] Integration with other tools (Confluence, Notion, Slack)
- [ ] Dashboard web interface for viewing reports
- [ ] Automatic sprint number detection from Jira
- [ ] Custom field mapping configuration
- [ ] Multi-team support with separate configurations

## 📅 Sprint Schedule

The system runs on a **bi-weekly schedule** starting September 22, 2025:

| Sprint | Report Date | Status |
|--------|-------------|---------|
| Sprint 19 | Current | ✅ Manual generation available |
| Sprint 20 | Sept 22, 2025 | 🔄 First automated report |
| Sprint 21 | Oct 6, 2025 | ⏳ Scheduled |
| Sprint 22 | Oct 20, 2025 | ⏳ Scheduled |
| Sprint 23 | Nov 3, 2025 | ⏳ Scheduled |

**Time**: Every Monday at 9:00 AM UTC  
**Pattern**: Every 14 days (bi-weekly)

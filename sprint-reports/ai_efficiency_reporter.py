#!/usr/bin/env python3
"""
AI Efficiency Sprint Reporter
Generates automated reports comparing traditional estimates vs AI-assisted development effort.

This script analyzes how AI assistance affects developer productivity by comparing:
- Dev Story Points (traditional estimates)
- Dev Story Points (With AI) (actual effort when using AI tools)

The goal is to see lower numbers in the AI column, indicating reduced effort.
"""

import os
import sys
import json
import requests
import base64
from datetime import datetime, timedelta
from collections import defaultdict
import logging
from typing import Dict, List, Tuple, Optional
import argparse


class JiraClient:
    """Jira REST API client for fetching sprint data."""
    
    def __init__(self, jira_url: str, email: str, api_token: str):
        self.jira_url = jira_url.rstrip('/')
        self.email = email
        self.api_token = api_token
        self.auth_header = base64.b64encode(f"{email}:{api_token}".encode()).decode()
        
        # Set up session
        self.session = requests.Session()
        self.session.headers.update({
            'Authorization': f'Basic {self.auth_header}',
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        })
    
    def search_issues(self, jql: str, fields: List[str] = None, max_results: int = 100) -> Dict:
        """Search Jira issues using JQL."""
        if fields is None:
            fields = ['summary', 'assignee', 'status', 'issuetype', 'key']
        
        url = f"{self.jira_url}/rest/api/3/search"
        payload = {
            'jql': jql,
            'fields': fields,
            'maxResults': max_results
        }
        
        response = self.session.post(url, json=payload)
        response.raise_for_status()
        return response.json()


class AIEfficiencyReporter:
    """Main reporter class for generating AI efficiency reports."""
    
    # Developer account IDs for the engineering team
    DEVELOPER_IDS = [
        '62bae2adfbc1f7c647b7f5c9',    # Oluwatoyosi Oyegoke
        '623df1a61c7f6a00704ae991',    # Nunu Olamilekan
        '61d2b0d6567cb70070bf0df8',    # Ebubekir Tabak
        '712020:22e771c3-dbf3-430b-8a18-bea8684b5186',  # Stephen Ng'ang'a
        '61d2b0d70586a200693a67a1',    # Abd UlHameed Maree
        '6215b2f36b7e24006a7a22b5',    # Ibrahim Amin
        '5ffd5092d3649601390394c1',    # Haakon Løtveit
        '627944ad93111000689f8ce2',    # Mohamed Abd El Aziz
        '712020:c35359ac-da76-4f3f-b301-14538f144ac6'   # Alexander Moran
    ]
    
    # Custom field IDs for story points
    DEV_STORY_POINTS_FIELD = 'customfield_11518'
    DEV_STORY_POINTS_AI_FIELD = 'customfield_11797'
    
    def __init__(self, config_path: str = None):
        """Initialize the reporter with configuration."""
        self.config = self._load_config(config_path)
        self.jira_client = JiraClient(
            self.config['jira_url'],
            self.config['email'],
            self.config['api_token']
        )
        
        # Set up logging
        self._setup_logging()
        
    def _load_config(self, config_path: str = None) -> Dict:
        """Load configuration from file or environment variables."""
        if config_path and os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        
        # Load from environment variables
        return {
            'jira_url': os.getenv('JIRA_URL', 'https://shortpoint.atlassian.net'),
            'email': os.getenv('JIRA_EMAIL'),
            'api_token': os.getenv('JIRA_API_TOKEN'),
            'output_dir': os.getenv('OUTPUT_DIR', './output'),
            'log_level': os.getenv('LOG_LEVEL', 'INFO')
        }
    
    def _setup_logging(self):
        """Set up logging configuration."""
        log_dir = os.path.join(os.path.dirname(__file__), 'logs')
        os.makedirs(log_dir, exist_ok=True)
        
        log_file = os.path.join(log_dir, f"ai_efficiency_report_{datetime.now().strftime('%Y%m%d')}.log")
        
        logging.basicConfig(
            level=getattr(logging, self.config.get('log_level', 'INFO')),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler(sys.stdout)
            ]
        )
        self.logger = logging.getLogger(__name__)
    
    def _build_jql_query(self) -> str:
        """Build the JQL query for current sprint issues."""
        developer_ids_str = ', '.join(self.DEVELOPER_IDS)
        return f'sprint in openSprints() AND assignee in ({developer_ids_str}) AND "Dev Story Points" is not EMPTY AND "Dev Story Points (With AI)" is not EMPTY AND status in ("Done", "Dev Review", "In Progress", "For Testing")'
    
    def fetch_sprint_data(self) -> List[Dict]:
        """Fetch current sprint data from Jira."""
        self.logger.info("Fetching sprint data from Jira...")
        
        jql = self._build_jql_query()
        fields = ['*all']
        
        try:
            result = self.jira_client.search_issues(jql, fields, max_results=200)
            issues = result.get('issues', [])
            
            self.logger.info(f"Retrieved {len(issues)} issues from current sprint")
            return issues
            
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error fetching data from Jira: {e}")
            raise
    
    def get_previous_sprint_issues(self) -> set:
        """Get list of issue keys that were already in previous sprint reports."""
        # Issues that appeared in previous sprint reports (carry-overs)
        previous_sprint_issues = [
            # From Sprint 19 report
            "SPX-10614", "SPX-10604", "SPX-10602", "SPX-10594", "SPX-10587", "SPX-10583", "SPX-10582",
            "SPX-10557", "SPX-10556", "SPX-10555", "SPX-10515", "SPX-9954", "SPX-10402", "SPX-10400",
            "SPX-8141", "SPX-10613", "SPX-10612", "SPX-10610", "SPX-10607", "SPX-10605", "SPX-10603",
            "SPX-10601", "SPX-10600", "SPX-10598", "SPX-10597", "SPX-10563", "SPX-10561", "SPX-10560",
            "SPX-10558", "SPX-10407", "SPX-10373", "SPX-10611", "SPX-10554", "SPX-10426", "SPX-10578",
            "SPX-10570", "SPX-10569", "SPX-10568", "SPX-10567", "SPX-10534", "SPX-10530", "SPX-10528",
            "SPX-10566", "SPX-10565", "SPX-10564", "SPX-8170", "SPX-8114", "SPX-10547", "SPX-10081",
            "SPX-9279", "SPX-8174", "SPX-5750"
        ]
        return set(previous_sprint_issues)

    def process_sprint_data(self, issues: List[Dict]) -> Tuple[Dict, Dict]:
        """Process sprint data and calculate metrics by developer.

        Filters out carry-over issues from previous sprints to show only current sprint work.
        """
        previous_issues = self.get_previous_sprint_issues()

        developer_data = defaultdict(lambda: {
            'name': '',
            'traditional_points': 0,
            'ai_points': 0,
            'issues_count': 0,
            'completed_issues': 0,
            'in_progress_issues': 0
        })

        sprint_info = {
            'total_issues': len(issues),
            'filtered_issues': 0,
            'carry_over_count': 0,
            'report_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'sprint_name': 'Current Sprint (Filtered)'
        }

        for issue in issues:
            issue_key = issue.get('key', '')
            assignee = issue.get('fields', {}).get('assignee', {})
            if not assignee:
                continue

            assignee_id = assignee.get('accountId', '')
            assignee_name = assignee.get('displayName', 'Unknown')

            # Get story point values
            traditional_points = issue.get('fields', {}).get(self.DEV_STORY_POINTS_FIELD, 0) or 0
            ai_points = issue.get('fields', {}).get(self.DEV_STORY_POINTS_AI_FIELD, 0) or 0

            # Skip if no story points
            if traditional_points <= 0 and ai_points <= 0:
                continue

            # Filter out carry-over issues from previous sprints
            if issue_key in previous_issues:
                sprint_info['carry_over_count'] += 1
                self.logger.info(f"Filtering out carry-over issue: {issue_key} ({assignee_name})")
                continue

            # Only include current sprint work
            dev_data = developer_data[assignee_id]
            dev_data['name'] = assignee_name
            dev_data['traditional_points'] += traditional_points
            dev_data['ai_points'] += ai_points
            dev_data['issues_count'] += 1

            # Track completion status
            status = issue.get('fields', {}).get('status', {}).get('name', '')
            if status in ["Done", "Dev Review"]:
                dev_data['completed_issues'] += 1
            elif status in ["In Progress", "For Testing"]:
                dev_data['in_progress_issues'] += 1

            sprint_info['filtered_issues'] += 1

        self.logger.info(f"Processed {sprint_info['total_issues']} total issues: {sprint_info['filtered_issues']} current sprint, {sprint_info['carry_over_count']} carry-overs excluded")
        return dict(developer_data), sprint_info
    
    def generate_markdown_report(self, developer_data: Dict, sprint_info: Dict) -> str:
        """Generate a markdown report."""
        report_lines = []

        # Header
        report_lines.extend([
            "# 🎯 AI Efficiency Sprint Report - CURRENT SPRINT WORK ONLY",
            "",
            f"**Generated**: {sprint_info['report_date']}  ",
            f"**Sprint**: {sprint_info['sprint_name']}  ",
            f"**Total Issues**: {sprint_info.get('filtered_issues', sprint_info.get('total_issues', 0))} issues analyzed (excluding carry-overs)",
            f"**Carry-over Issues Excluded**: {sprint_info.get('carry_over_count', 0)} issues from previous sprints",
            "",
            "🔍 **This report includes ONLY work completed or actively worked on in the current sprint**",
            "❌ **Excluded**: Issues that were already in previous sprint reports (carry-overs)",
            "",
            "## 📊 Overview",
            "",
            "This report compares traditional development estimates with actual effort when using AI assistance. ",
            "The goal is to see **lower numbers** in the AI column, indicating that AI tools are successfully reducing developer effort.",
            "",
            "## 👥 Developer Performance (Current Sprint Work Only)",
            "",
            "| Developer | Traditional Estimate | AI-Assisted Effort | Efficiency Gain | % Improvement | Issues | Completed/In Progress |",
            "|-----------|---------------------|-------------------|-----------------|---------------|--------|-----------------------|"
        ])
        
        # Calculate totals
        total_traditional = 0
        total_ai = 0
        total_issues = 0
        total_completed = 0
        total_in_progress = 0

        # Sort developers by efficiency gain (descending)
        sorted_developers = sorted(
            developer_data.items(),
            key=lambda x: x[1]['traditional_points'] - x[1]['ai_points'],
            reverse=True
        )

        for dev_id, data in sorted_developers:
            traditional = data['traditional_points']
            ai = data['ai_points']
            efficiency_gain = traditional - ai
            improvement_pct = (efficiency_gain / traditional * 100) if traditional > 0 else 0

            total_traditional += traditional
            total_ai += ai
            total_issues += data['issues_count']
            total_completed += data['completed_issues']
            total_in_progress += data['in_progress_issues']

            efficiency_indicator = "✅" if efficiency_gain > 0 else "⚠️" if efficiency_gain == 0 else "❌"

            completed_status = f"{data['completed_issues']}✅ / {data['in_progress_issues']}🔄"

            report_lines.append(
                f"| {efficiency_indicator} **{data['name']}** | {traditional:.1f} | {ai:.1f} | "
                f"{efficiency_gain:+.1f} | {improvement_pct:+.1f}% | {data['issues_count']} | {completed_status} |"
            )
        
        # Add totals row
        total_efficiency_gain = total_traditional - total_ai
        total_improvement_pct = (total_efficiency_gain / total_traditional * 100) if total_traditional > 0 else 0

        report_lines.extend([
            "|-----------|---------------------|-------------------|-----------------|---------------|--------|-----------------------|",
            f"| **TOTALS** | **{total_traditional:.1f}** | **{total_ai:.1f}** | "
            f"**{total_efficiency_gain:+.1f}** | **{total_improvement_pct:+.1f}%** | **{total_issues}** | **{total_completed}✅ / {total_in_progress}🔄** |"
        ])

        # Add analysis section
        report_lines.extend([
            "",
            "## 📈 Analysis (Current Sprint Only)",
            "",
            f"- **Total Traditional Estimates**: {total_traditional:.1f} story points",
            f"- **Total AI-Assisted Effort**: {total_ai:.1f} story points",
            f"- **Overall Efficiency Gain**: {total_efficiency_gain:+.1f} story points ({total_improvement_pct:+.1f}%)",
            f"- **Average Issues per Developer**: {total_issues / len(developer_data):.1f}" if len(developer_data) > 0 else "",
            f"- **Work Status**: {total_completed} completed ✅, {total_in_progress} in progress 🔄",
            "",
            "### 🎯 Key Insights (Sprint-Specific)",
            ""
        ])
        
        if total_efficiency_gain > 0:
            report_lines.append(f"✅ **Positive Impact**: AI assistance is reducing current sprint development effort by {total_efficiency_gain:.1f} story points ({total_improvement_pct:.1f}%)")
        elif total_efficiency_gain < 0:
            report_lines.append(f"❌ **Attention Needed**: AI usage is showing higher effort by {abs(total_efficiency_gain):.1f} story points ({abs(total_improvement_pct):.1f}%)")
        else:
            report_lines.append("⚠️ **Neutral Impact**: AI assistance is not showing measurable impact on development effort")

        # Top performer
        if sorted_developers:
            top_performer = sorted_developers[0][1]
            top_gain = top_performer['traditional_points'] - top_performer['ai_points']
            if top_gain > 0:
                report_lines.append(f"🏆 **Top Performer This Sprint**: {top_performer['name']} with {top_gain:.1f} story points saved")

        # Sprint activity summary
        total_issues_all = sprint_info.get('total_issues', 0)
        filtered_issues = sprint_info.get('filtered_issues', 0)
        carry_over_count = sprint_info.get('carry_over_count', 0)

        report_lines.extend([
            "",
            "### 📋 Sprint Activity Summary",
            "",
            f"**New Work This Sprint**: {filtered_issues} issues",
            f"**Completed Work**: {total_completed} issues finished ✅",
            f"**Active Work**: {total_in_progress} issues in progress 🔄",
            f"**Excluded Carry-overs**: {carry_over_count} issues from previous sprints not counted",
            "",
            "---",
            "*This report shows ONLY work done in the current sprint, excluding carry-over issues from previous sprints.*",
            "*Generated using live Jira data with filtering enabled.*"
        ])
        
        return "\n".join(report_lines)
    
    def save_report(self, content: str, format_type: str = 'markdown') -> str:
        """Save the report to a file."""
        output_dir = self.config.get('output_dir', './output')
        os.makedirs(output_dir, exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"ai_efficiency_report_{timestamp}.{format_type}"
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.logger.info(f"Report saved to: {filepath}")
        return filepath
    
    def generate_report(self, output_format: str = 'markdown') -> str:
        """Main method to generate the complete report."""
        try:
            # Fetch data
            issues = self.fetch_sprint_data()
            if not issues:
                self.logger.warning("No issues found for current sprint")
                return ""
            
            # Process data
            developer_data, sprint_info = self.process_sprint_data(issues)
            
            # Generate report
            if output_format.lower() == 'markdown':
                content = self.generate_markdown_report(developer_data, sprint_info)
            else:
                raise ValueError(f"Unsupported output format: {output_format}")
            
            # Save report
            filepath = self.save_report(content, 'md')
            
            self.logger.info("Report generation completed successfully")
            return filepath
            
        except Exception as e:
            self.logger.error(f"Error generating report: {e}")
            raise


def main():
    """Main entry point for the script."""
    parser = argparse.ArgumentParser(description='Generate AI Efficiency Sprint Reports (with carry-over filtering)')
    parser.add_argument('--config', '-c', help='Path to configuration file')
    parser.add_argument('--format', '-f', default='markdown', choices=['markdown'],
                        help='Output format (default: markdown)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Enable verbose logging')
    parser.add_argument('--include-carry-overs', action='store_true',
                        help='Include carry-over issues from previous sprints (default: exclude them)')

    args = parser.parse_args()

    # Set log level based on verbose flag
    if args.verbose:
        os.environ['LOG_LEVEL'] = 'DEBUG'

    try:
        reporter = AIEfficiencyReporter(args.config)

        # Override filtering if requested
        if args.include_carry_overs:
            reporter.get_previous_sprint_issues = lambda: set()  # Return empty set to include all

        filepath = reporter.generate_report(args.format)

        if filepath:
            print(f"\n✅ Report generated successfully: {filepath}")
            print("\n📋 You can now copy this report to Notion or any other platform!")
            print("\n🔍 Note: By default, carry-over issues from previous sprints are excluded.")
            print("   Use --include-carry-overs to include them if needed.")
        else:
            print("\n❌ No report generated (no data found)")
            sys.exit(1)

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()

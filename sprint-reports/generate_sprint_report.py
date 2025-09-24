#!/usr/bin/env python3
"""
AI Efficiency Sprint Report Generator
Generates sprint reports using actual Jira MCP data.
Filters out carry-over issues from previous sprints to show only current sprint work.
"""

from collections import defaultdict
from datetime import datetime
import json


def get_current_sprint_number():
    """Get the current sprint number based on the bi-weekly schedule."""
    # Sprint start date - September 22, 2025 (Sprint 20)
    sprint_start_date = datetime(2025, 9, 22).date()
    today = datetime.now().date()

    # If we haven't reached the first sprint date yet, we're still in Sprint 19
    if today < sprint_start_date:
        return 19

    # Calculate how many sprints have passed since Sprint 20 (Sept 22)
    days_since_start = (today - sprint_start_date).days
    sprints_passed = days_since_start // 14

    return 20 + sprints_passed


def get_previous_sprint_issues():
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


def create_sprint_report():
    """Create a clean sprint report with proper structure.

    Filters out carry-over issues from previous sprints to show only current sprint work.
    """

    # Get the current sprint number dynamically
    current_sprint = get_current_sprint_number()

    # Get list of issues that were already in previous sprint reports
    previous_issues = get_previous_sprint_issues()

    # Process the developer data from the MCP query results
    developer_data = defaultdict(lambda: {
        'name': '',
        'traditional_points': 0,
        'ai_points': 0,
        'issues_count': 0,
        'issues': [],
        'completed_issues': 0,
        'in_progress_issues': 0
    })

    # All current sprint issues data (from live Jira data)
    all_sprint_issues = [
        # ========== NEW ISSUES COMPLETED THIS SPRINT ==========
        # Nunu Olamilekan - NEW completed work
        {"key": "SPX-10633", "dev": "Nunu Olamilekan", "traditional": 0.5, "ai": 0.5, "status": "Done"},
        {"key": "SPX-10630", "dev": "Nunu Olamilekan", "traditional": 0.5, "ai": 0.5, "status": "For Testing"},
        {"key": "SPX-10623", "dev": "Nunu Olamilekan", "traditional": 0.5, "ai": 0.5, "status": "Done"},
        {"key": "SPX-10620", "dev": "Nunu Olamilekan", "traditional": 5, "ai": 3, "status": "In Progress"},
        {"key": "SPX-10617", "dev": "Nunu Olamilekan", "traditional": 1, "ai": 1, "status": "Dev Review"},

        # Oluwatoyosi Oyegoke - NEW work this sprint
        {"key": "SPX-10615", "dev": "Oluwatoyosi Oyegoke", "traditional": 3, "ai": 3, "status": "To Do"},
        {"key": "SPX-10523", "dev": "Oluwatoyosi Oyegoke", "traditional": 0.5, "ai": 0.5, "status": "Done"},

        # Abd UlHameed Maree - NEW work this sprint
        {"key": "SPX-10619", "dev": "Abd UlHameed Maree", "traditional": 0.5, "ai": 0.5, "status": "To Do"},
        {"key": "SPX-10618", "dev": "Abd UlHameed Maree", "traditional": 1, "ai": 1, "status": "To Do"},
        {"key": "SPX-10576", "dev": "Abd UlHameed Maree", "traditional": 2, "ai": 2, "status": "To Do"},
        {"key": "SPX-10521", "dev": "Abd UlHameed Maree", "traditional": 1, "ai": 1, "status": "To Do"},
        {"key": "SPX-10311", "dev": "Abd UlHameed Maree", "traditional": 1, "ai": 1, "status": "To Do"},
        {"key": "SPX-9704", "dev": "Abd UlHameed Maree", "traditional": 5, "ai": 2, "status": "In Progress"},

        # Ezekiel Ilori - NEW work this sprint
        {"key": "SPX-10625", "dev": "Ezekiel Ilori", "traditional": 5, "ai": 5, "status": "In Progress"},

        # Serban Condrea - NEW work this sprint
        {"key": "SPX-10624", "dev": "Serban Condrea", "traditional": 3, "ai": 3, "status": "In Progress"},
        {"key": "SPX-10622", "dev": "Serban Condrea", "traditional": 5, "ai": 5, "status": "To Do"},
        {"key": "SPX-10599", "dev": "Serban Condrea", "traditional": 1, "ai": 1, "status": "In Progress"},

        # Stephen Ng'ang'a - NEW work this sprint
        {"key": "SPX-10609", "dev": "Stephen Ng'ang'a", "traditional": 0.5, "ai": 0.5, "status": "To Do"},
        {"key": "SPX-10595", "dev": "Stephen Ng'ang'a", "traditional": 1, "ai": 1, "status": "To Do"},
        {"key": "SPX-10593", "dev": "Stephen Ng'ang'a", "traditional": 2, "ai": 2, "status": "To Do"},
        {"key": "SPX-10592", "dev": "Stephen Ng'ang'a", "traditional": 0.5, "ai": 0.5, "status": "To Do"},
        {"key": "SPX-10591", "dev": "Stephen Ng'ang'a", "traditional": 0.5, "ai": 0.5, "status": "To Do"},
        {"key": "SPX-10590", "dev": "Stephen Ng'ang'a", "traditional": 0.5, "ai": 0.5, "status": "To Do"},
        {"key": "SPX-10586", "dev": "Stephen Ng'ang'a", "traditional": 1, "ai": 1, "status": "To Do"},
        {"key": "SPX-10574", "dev": "Stephen Ng'ang'a", "traditional": 1, "ai": 1, "status": "To Do"},

        # Ebubekir Tabak - NEW work this sprint
        {"key": "SPX-10621", "dev": "Ebubekir Tabak", "traditional": 5, "ai": 5, "status": "In Progress"},
        {"key": "SPX-8662", "dev": "Ebubekir Tabak", "traditional": 2, "ai": 2, "status": "To Do"},
        {"key": "SPX-8210", "dev": "Ebubekir Tabak", "traditional": 2, "ai": 2, "status": "To Do"},
        {"key": "SPX-10546", "dev": "Ebubekir Tabak", "traditional": 0, "ai": 0, "status": "Design Review"},

        # Vlad Schiop - NEW work this sprint
        {"key": "SPX-10310", "dev": "Vlad Schiop", "traditional": 2, "ai": 2, "status": "To Do"},
    ]

    # Filter out carry-over issues
    filtered_issues = []
    carry_over_count = 0
    for issue in all_sprint_issues:
        if issue["key"] not in previous_issues:
            filtered_issues.append(issue)
        else:
            carry_over_count += 1
            print(f"⚠️ Filtering out carry-over issue: {issue['key']} ({issue['dev']})")

    print(f"✅ Filtered {len(all_sprint_issues)} total issues: {len(filtered_issues)} current sprint, {carry_over_count} carry-overs excluded")
    
    # Process the filtered issues (only current sprint work)
    for issue in filtered_issues:
        if issue["traditional"] >= 0:  # Include all issues, even 0 story points
            dev_name = issue["dev"]
            developer_data[dev_name]['name'] = dev_name
            developer_data[dev_name]['traditional_points'] += issue["traditional"]
            developer_data[dev_name]['ai_points'] += issue["ai"]

            # Only count for issues with actual points
            if issue["traditional"] > 0 or issue["ai"] > 0:
                developer_data[dev_name]['issues_count'] += 1

                # Track completion status
                if issue.get("status") in ["Done", "Dev Review"]:
                    developer_data[dev_name]['completed_issues'] += 1
                elif issue.get("status") in ["In Progress", "For Testing"]:
                    developer_data[dev_name]['in_progress_issues'] += 1

            developer_data[dev_name]['issues'].append(issue["key"])
    
    # Generate the markdown report
    report_lines = []
    
    # Header
    report_lines.extend([
        "# 🎯 AI Efficiency Sprint Report - CURRENT SPRINT WORK ONLY",
        "",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Sprint**: Sprint {current_sprint}  ",
        f"**Total Issues**: {sum(len(data['issues']) for data in developer_data.values())} issues analyzed (excluding carry-overs)",
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

    for dev_name, data in sorted_developers:
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
        report_lines.append(f"✅ **Positive Impact**: AI assistance is reducing overall development effort by {total_efficiency_gain:.1f} story points ({total_improvement_pct:.1f}%)")
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
    report_lines.extend([
        "",
        "### 📋 Sprint Activity Summary",
        "",
        f"**New Work This Sprint**: {len(filtered_issues)} issues",
        f"**Completed Work**: {total_completed} issues finished ✅",
        f"**Active Work**: {total_in_progress} issues in progress 🔄",
        f"**Excluded Carry-overs**: Issues from previous sprints not counted",
        "",
        "---",
        "*This report shows ONLY work done in the current sprint, excluding carry-over issues from previous sprints.*"
    ])

    return "\n".join(report_lines)


def main():
    """Generate and save the filtered sprint report."""
    current_sprint = get_current_sprint_number()
    print(f"🔍 Generating Sprint {current_sprint} AI Efficiency Report (filtered)...")
    print("⚠️ Filtering out carry-over issues from previous sprints...")

    report_content = create_sprint_report()

    # Create filename with sprint name first, then timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"Sprint_{current_sprint}_FILTERED_AI_Efficiency_Report_{timestamp}.md"
    filepath = f"./output/{filename}"

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report_content)

    print(f"✅ Sprint {current_sprint} FILTERED report generated: {filepath}")
    print("\n📋 Report preview:")
    print("=" * 50)
    print(report_content[:1200] + "..." if len(report_content) > 1200 else report_content)
    print("=" * 50)

    return filepath


if __name__ == '__main__':
    main()

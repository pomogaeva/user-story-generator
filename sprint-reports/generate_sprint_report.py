#!/usr/bin/env python3
"""
AI Efficiency Sprint Report Generator
Generates sprint reports using actual Jira MCP data.
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


def create_sprint_report():
    """Create a clean sprint report with proper structure."""
    
    # Get the current sprint number dynamically
    current_sprint = get_current_sprint_number()
    
    # Process the developer data from the MCP query results
    developer_data = defaultdict(lambda: {
        'name': '',
        'traditional_points': 0,
        'ai_points': 0,
        'issues_count': 0,
        'issues': []
    })
    
    # Current sprint issues data (from MCP query)
    sprint_issues = [
        # Oluwatoyosi Oyegoke
        {"key": "SPX-10614", "dev": "Oluwatoyosi Oyegoke", "traditional": 1.0, "ai": 1.0},
        {"key": "SPX-10604", "dev": "Oluwatoyosi Oyegoke", "traditional": 3.0, "ai": 3.0},
        {"key": "SPX-10602", "dev": "Oluwatoyosi Oyegoke", "traditional": 2.0, "ai": 1.5},
        {"key": "SPX-10594", "dev": "Oluwatoyosi Oyegoke", "traditional": 2.0, "ai": 1.0},
        {"key": "SPX-10587", "dev": "Oluwatoyosi Oyegoke", "traditional": 2.0, "ai": 2.0},
        {"key": "SPX-10583", "dev": "Oluwatoyosi Oyegoke", "traditional": 1.0, "ai": 1.0},
        {"key": "SPX-10582", "dev": "Oluwatoyosi Oyegoke", "traditional": 1.0, "ai": 1.0},
        {"key": "SPX-10557", "dev": "Oluwatoyosi Oyegoke", "traditional": 3.0, "ai": 2.0},
        {"key": "SPX-10556", "dev": "Oluwatoyosi Oyegoke", "traditional": 2.0, "ai": 1.0},
        {"key": "SPX-10555", "dev": "Oluwatoyosi Oyegoke", "traditional": 2.0, "ai": 2.0},
        {"key": "SPX-10515", "dev": "Oluwatoyosi Oyegoke", "traditional": 2.0, "ai": 2.0},
        {"key": "SPX-9954", "dev": "Oluwatoyosi Oyegoke", "traditional": 1.0, "ai": 1.0},
        {"key": "SPX-10402", "dev": "Oluwatoyosi Oyegoke", "traditional": 3.0, "ai": 3.0},
        {"key": "SPX-10400", "dev": "Oluwatoyosi Oyegoke", "traditional": 1.0, "ai": 1.0},
        {"key": "SPX-8141", "dev": "Oluwatoyosi Oyegoke", "traditional": 1.0, "ai": 1.0},
        
        # Nunu Olamilekan
        {"key": "SPX-10613", "dev": "Nunu Olamilekan", "traditional": 0.5, "ai": 0.0},
        {"key": "SPX-10612", "dev": "Nunu Olamilekan", "traditional": 0.5, "ai": 0.0},
        {"key": "SPX-10610", "dev": "Nunu Olamilekan", "traditional": 2.0, "ai": 1.0},
        {"key": "SPX-10607", "dev": "Nunu Olamilekan", "traditional": 1.0, "ai": 1.0},
        {"key": "SPX-10605", "dev": "Nunu Olamilekan", "traditional": 1.0, "ai": 1.0},
        {"key": "SPX-10603", "dev": "Nunu Olamilekan", "traditional": 1.0, "ai": 0.5},
        {"key": "SPX-10601", "dev": "Nunu Olamilekan", "traditional": 0.5, "ai": 0.5},
        {"key": "SPX-10600", "dev": "Nunu Olamilekan", "traditional": 0.5, "ai": 0.5},
        {"key": "SPX-10598", "dev": "Nunu Olamilekan", "traditional": 2.0, "ai": 1.5},
        {"key": "SPX-10597", "dev": "Nunu Olamilekan", "traditional": 1.0, "ai": 1.0},
        {"key": "SPX-10563", "dev": "Nunu Olamilekan", "traditional": 0.5, "ai": 0.5},
        {"key": "SPX-10561", "dev": "Nunu Olamilekan", "traditional": 2.0, "ai": 2.0},
        {"key": "SPX-10560", "dev": "Nunu Olamilekan", "traditional": 1.0, "ai": 1.0},
        {"key": "SPX-10558", "dev": "Nunu Olamilekan", "traditional": 0.5, "ai": 0.5},
        {"key": "SPX-10407", "dev": "Nunu Olamilekan", "traditional": 0.5, "ai": 0.5},
        {"key": "SPX-10373", "dev": "Nunu Olamilekan", "traditional": 5.0, "ai": 4.0},
        
        # Ezekiel Ilori  
        {"key": "SPX-10611", "dev": "Ezekiel Ilori", "traditional": 1.0, "ai": 1.0},
        {"key": "SPX-10554", "dev": "Ezekiel Ilori", "traditional": 0.5, "ai": 0.5},
        {"key": "SPX-10426", "dev": "Ezekiel Ilori", "traditional": 5.0, "ai": 4.0},
        
        # Abd UlHameed Maree
        {"key": "SPX-10578", "dev": "Abd UlHameed Maree", "traditional": 0.5, "ai": 0.5},
        {"key": "SPX-10570", "dev": "Abd UlHameed Maree", "traditional": 2.0, "ai": 2.0},
        {"key": "SPX-10569", "dev": "Abd UlHameed Maree", "traditional": 3.0, "ai": 2.5},
        {"key": "SPX-10568", "dev": "Abd UlHameed Maree", "traditional": 0.5, "ai": 0.5},
        {"key": "SPX-10567", "dev": "Abd UlHameed Maree", "traditional": 1.0, "ai": 1.0},
        {"key": "SPX-10534", "dev": "Abd UlHameed Maree", "traditional": 1.0, "ai": 1.0},
        {"key": "SPX-10530", "dev": "Abd UlHameed Maree", "traditional": 1.0, "ai": 1.0},
        {"key": "SPX-10528", "dev": "Abd UlHameed Maree", "traditional": 0.5, "ai": 0.5},
        
        # Ebubekir Tabak
        {"key": "SPX-10566", "dev": "Ebubekir Tabak", "traditional": 3.0, "ai": 3.0},
        {"key": "SPX-10565", "dev": "Ebubekir Tabak", "traditional": 2.0, "ai": 2.0},
        {"key": "SPX-10564", "dev": "Ebubekir Tabak", "traditional": 2.0, "ai": 2.0},
        {"key": "SPX-8170", "dev": "Ebubekir Tabak", "traditional": 3.0, "ai": 3.0},
        {"key": "SPX-8114", "dev": "Ebubekir Tabak", "traditional": 3.0, "ai": 3.0},
        
        # Stephen Ng'ang'a
        {"key": "SPX-10547", "dev": "Stephen Ng'ang'a", "traditional": 1.0, "ai": 1.0},
        {"key": "SPX-10081", "dev": "Stephen Ng'ang'a", "traditional": 3.0, "ai": 3.0},
        {"key": "SPX-9279", "dev": "Stephen Ng'ang'a", "traditional": 3.0, "ai": 3.0},
        {"key": "SPX-8174", "dev": "Stephen Ng'ang'a", "traditional": 3.0, "ai": 2.0},
        {"key": "SPX-5750", "dev": "Stephen Ng'ang'a", "traditional": 2.0, "ai": 1.0},
    ]
    
    # Process the issues
    for issue in sprint_issues:
        if issue["traditional"] > 0:  # Only include issues with actual story points
            dev_name = issue["dev"]
            developer_data[dev_name]['name'] = dev_name
            developer_data[dev_name]['traditional_points'] += issue["traditional"]
            developer_data[dev_name]['ai_points'] += issue["ai"]
            developer_data[dev_name]['issues_count'] += 1
            developer_data[dev_name]['issues'].append(issue["key"])
    
    # Generate the markdown report
    report_lines = []
    
    # Header
    report_lines.extend([
        "# 🤖 AI Efficiency Sprint Report",
        "",
        f"**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}  ",
        f"**Sprint**: Sprint {current_sprint}  ",
        f"**Total Issues**: {sum(len(data['issues']) for data in developer_data.values())} issues analyzed",
        "",
        "## 📊 Overview",
        "",
        "This report compares traditional development estimates with actual effort when using AI assistance. ",
        "The goal is to see **lower numbers** in the AI column, indicating that AI tools are successfully reducing developer effort.",
        "",
        "## 👥 Developer Performance",
        "",
        "| Developer | Traditional Estimate | AI-Assisted Effort | Efficiency Gain | % Improvement | Issues |",
        "|-----------|---------------------|-------------------|-----------------|---------------|--------|"
    ])
    
    # Calculate totals
    total_traditional = 0
    total_ai = 0
    total_issues = 0
    
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
        
        efficiency_indicator = "✅" if efficiency_gain > 0 else "⚠️" if efficiency_gain == 0 else "❌"
        
        report_lines.append(
            f"| {efficiency_indicator} **{data['name']}** | {traditional:.1f} | {ai:.1f} | "
            f"{efficiency_gain:+.1f} | {improvement_pct:+.1f}% | {data['issues_count']} |"
        )
    
    # Add totals row
    total_efficiency_gain = total_traditional - total_ai
    total_improvement_pct = (total_efficiency_gain / total_traditional * 100) if total_traditional > 0 else 0
    
    report_lines.extend([
        "|-----------|---------------------|-------------------|-----------------|---------------|--------|",
        f"| **TOTALS** | **{total_traditional:.1f}** | **{total_ai:.1f}** | "
        f"**{total_efficiency_gain:+.1f}** | **{total_improvement_pct:+.1f}%** | **{total_issues}** |"
    ])
    
    # Add analysis section  
    report_lines.extend([
        "",
        "## 📈 Analysis",
        "",
        f"- **Total Traditional Estimates**: {total_traditional:.1f} story points",
        f"- **Total AI-Assisted Effort**: {total_ai:.1f} story points",
        f"- **Overall Efficiency Gain**: {total_efficiency_gain:+.1f} story points ({total_improvement_pct:+.1f}%)",
        f"- **Average Issues per Developer**: {total_issues / len(developer_data):.1f}" if len(developer_data) > 0 else "",
        "",
        "### 🎯 Key Insights",
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
            report_lines.append(f"🏆 **Top Performer**: {top_performer['name']} with {top_gain:.1f} story points saved")
    
    return "\n".join(report_lines)


def main():
    """Generate and save the sprint report."""
    current_sprint = get_current_sprint_number()
    print(f"🔍 Generating Sprint {current_sprint} AI Efficiency Report...")
    
    report_content = create_sprint_report()
    
    # Create filename with sprint name first, then timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"Sprint_{current_sprint}_AI_Efficiency_Report_{timestamp}.md"
    filepath = f"./output/{filename}"
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report_content)
    
    print(f"✅ Sprint {current_sprint} report generated: {filepath}")
    print("\n📋 Report preview:")
    print("=" * 50)
    print(report_content[:800] + "..." if len(report_content) > 800 else report_content)
    print("=" * 50)
    
    return filepath


if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Generate Complexity Summary for PR Comments
Creates a concise summary of complexity analysis results.
"""

import json
from pathlib import Path
from typing import Dict, List
from datetime import datetime

def load_json_file(filename: str) -> Dict:
    """Load JSON file safely"""
    try:
        with open(filename, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}

def generate_summary() -> str:
    """Generate a summary of complexity analysis"""
    static_results = load_json_file('static-complexity-results.json')
    gpt_results = load_json_file('gpt-complexity-results.json')
    threshold_results = load_json_file('complexity-threshold-results.json')
    
    summary_parts = []
    
    # Static analysis summary
    if static_results:
        summary_parts.append("### 📊 Static Analysis")
        summary_parts.append(f"- **Files analyzed:** {static_results.get('files_analyzed', 0)}")
        summary_parts.append(f"- **Total complexity:** {static_results.get('total_complexity', 0):.1f}")
        
        if static_results.get('summary'):
            summary = static_results['summary']
            summary_parts.append(f"- **Average complexity:** {summary.get('average_complexity', 0):.1f}")
            summary_parts.append(f"- **Total size:** {summary.get('total_size_kb', 0):.1f} KB")
        
        high_complexity = static_results.get('high_complexity_files', [])
        if high_complexity:
            summary_parts.append(f"- **High complexity files:** {len(high_complexity)}")
            for file_info in high_complexity[:3]:  # Show top 3
                summary_parts.append(f"  - `{file_info['file']}`: {file_info['score']:.1f}")
        
        conflicts = static_results.get('conflicts_found', [])
        violations = static_results.get('best_practice_violations', [])
        
        if conflicts:
            summary_parts.append(f"- **Rule conflicts:** {len(set(conflicts))}")
        if violations:
            summary_parts.append(f"- **Best practice violations:** {len(set(violations))}")
    
    # GPT analysis summary
    if gpt_results:
        summary_parts.append("\n### 🧠 Semantic Analysis")
        summary_parts.append(f"- **Files analyzed:** {gpt_results.get('files_analyzed', 0)}")
        
        high_complexity = gpt_results.get('high_complexity_files', [])
        if high_complexity:
            summary_parts.append(f"- **High semantic complexity:** {len(high_complexity)}")
            for file_info in high_complexity[:3]:  # Show top 3
                summary_parts.append(f"  - `{file_info['file']}`: {file_info['complexity']}/10")
        
        conflicts = gpt_results.get('rule_conflicts', [])
        violations = gpt_results.get('best_practice_violations', [])
        cursor_issues = gpt_results.get('cursor_compatibility_issues', [])
        
        if conflicts:
            summary_parts.append(f"- **Rule conflicts:** {len(set(conflicts))}")
        if violations:
            summary_parts.append(f"- **Best practice violations:** {len(set(violations))}")
        if cursor_issues:
            summary_parts.append(f"- **Cursor compatibility issues:** {len(set(cursor_issues))}")
    
    # Threshold check summary
    if threshold_results:
        summary_parts.append("\n### 🚨 Threshold Check")
        summary = threshold_results.get('summary', {})
        summary_parts.append(f"- **Files checked:** {summary.get('files_checked', 0)}")
        summary_parts.append(f"- **Files exceeded threshold:** {summary.get('files_exceeded', 0)}")
        
        exceeded_files = threshold_results.get('exceeded_files', [])
        if exceeded_files:
            summary_parts.append(f"- **Critical files:** {len(exceeded_files)}")
            for file_info in exceeded_files[:3]:  # Show top 3
                summary_parts.append(f"  - `{file_info['file']}`: {file_info['excess_percentage']:.1f}% over")
        
        warnings = threshold_results.get('warnings', [])
        if warnings:
            summary_parts.append(f"- **Warnings:** {len(warnings)}")
    
    # Overall status
    if threshold_results and threshold_results.get('threshold_exceeded', False):
        summary_parts.append("\n### ❌ Status: THRESHOLD EXCEEDED")
        summary_parts.append("Please review the detailed reports in the artifacts.")
    else:
        summary_parts.append("\n### ✅ Status: WITHIN LIMITS")
        summary_parts.append("All files are within complexity thresholds.")
    
    # Recommendations
    recommendations = []
    if static_results:
        recommendations.extend(static_results.get('recommendations', []))
    if threshold_results:
        recommendations.extend(threshold_results.get('recommendations', []))
    
    if recommendations:
        summary_parts.append("\n### 💡 Recommendations")
        for rec in recommendations[:5]:  # Show top 5
            summary_parts.append(f"- {rec}")
    
    return "\n".join(summary_parts)

def main():
    summary = generate_summary()
    
    # Save summary to file
    with open('complexity-summary.md', 'w') as f:
        f.write(summary)
    
    print("📄 Complexity summary generated: complexity-summary.md")
    print("\n" + summary)

if __name__ == "__main__":
    main() 
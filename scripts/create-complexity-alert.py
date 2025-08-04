#!/usr/bin/env python3
"""
Create Complexity Alert
Generates alerts when complexity thresholds are exceeded.
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

def create_alert() -> str:
    """Create a complexity alert message"""
    threshold_results = load_json_file('complexity-threshold-results.json')
    static_results = load_json_file('static-complexity-results.json')
    gpt_results = load_json_file('gpt-complexity-results.json')
    
    alert_parts = []
    alert_parts.append("# 🚨 COMPLEXITY THRESHOLD EXCEEDED")
    alert_parts.append("")
    alert_parts.append("## ⚠️  Critical Issues Detected")
    alert_parts.append("")
    
    # Threshold exceeded files
    if threshold_results and threshold_results.get('exceeded_files'):
        alert_parts.append("### 🚨 Files Exceeding Threshold")
        for file_info in threshold_results['exceeded_files']:
            alert_parts.append(f"- **`{file_info['file']}`**")
            alert_parts.append(f"  - Current: {file_info['current_score']:.1f}")
            alert_parts.append(f"  - Baseline: {file_info['baseline_score']}")
            alert_parts.append(f"  - Threshold: {file_info['threshold']}")
            alert_parts.append(f"  - **Excess: {file_info['excess_percentage']:.1f}%**")
            alert_parts.append("")
    
    # High complexity files from static analysis
    if static_results and static_results.get('high_complexity_files'):
        alert_parts.append("### 📊 High Complexity Files (Static)")
        for file_info in static_results['high_complexity_files'][:5]:  # Top 5
            alert_parts.append(f"- **`{file_info['file']}`**: {file_info['score']:.1f} complexity")
        alert_parts.append("")
    
    # High complexity files from GPT analysis
    if gpt_results and gpt_results.get('high_complexity_files'):
        alert_parts.append("### 🧠 High Semantic Complexity (GPT)")
        for file_info in gpt_results['high_complexity_files'][:5]:  # Top 5
            alert_parts.append(f"- **`{file_info['file']}`**: {file_info['complexity']}/10 complexity")
        alert_parts.append("")
    
    # Rule conflicts
    conflicts = []
    if static_results:
        conflicts.extend(static_results.get('conflicts_found', []))
    if gpt_results:
        conflicts.extend(gpt_results.get('rule_conflicts', []))
    
    if conflicts:
        alert_parts.append("### ⚠️  Rule Conflicts Detected")
        for conflict in set(conflicts)[:10]:  # Top 10
            alert_parts.append(f"- {conflict}")
        alert_parts.append("")
    
    # Best practice violations
    violations = []
    if static_results:
        violations.extend(static_results.get('best_practice_violations', []))
    if gpt_results:
        violations.extend(gpt_results.get('best_practice_violations', []))
    
    if violations:
        alert_parts.append("### ❌ Best Practice Violations")
        for violation in set(violations)[:10]:  # Top 10
            alert_parts.append(f"- {violation}")
        alert_parts.append("")
    
    # Cursor compatibility issues
    if gpt_results and gpt_results.get('cursor_compatibility_issues'):
        alert_parts.append("### 🔧 Cursor Compatibility Issues")
        for issue in set(gpt_results['cursor_compatibility_issues'])[:10]:  # Top 10
            alert_parts.append(f"- {issue}")
        alert_parts.append("")
    
    # Recommendations
    recommendations = []
    if threshold_results:
        recommendations.extend(threshold_results.get('recommendations', []))
    if static_results:
        recommendations.extend(static_results.get('recommendations', []))
    
    if recommendations:
        alert_parts.append("## 💡 Immediate Actions Required")
        for rec in recommendations[:10]:  # Top 10
            alert_parts.append(f"- {rec}")
        alert_parts.append("")
    
    # Next steps
    alert_parts.append("## 🔍 Next Steps")
    alert_parts.append("1. **Review detailed reports** in the workflow artifacts")
    alert_parts.append("2. **Simplify complex files** by splitting into smaller modules")
    alert_parts.append("3. **Resolve rule conflicts** by consolidating similar rules")
    alert_parts.append("4. **Fix best practice violations** in code examples")
    alert_parts.append("5. **Improve Cursor compatibility** by simplifying complex workflows")
    alert_parts.append("")
    alert_parts.append("## 📊 Reports Available")
    alert_parts.append("- `static-complexity-results.json` - Static analysis results")
    alert_parts.append("- `gpt-complexity-results.json` - Semantic analysis results")
    alert_parts.append("- `complexity-threshold-results.json` - Threshold check results")
    alert_parts.append("- `complexity-threshold-report.md` - Detailed threshold report")
    
    return "\n".join(alert_parts)

def main():
    alert = create_alert()
    
    # Save alert to file
    with open('complexity-alert.md', 'w') as f:
        f.write(alert)
    
    print("🚨 Complexity alert generated: complexity-alert.md")
    print("\n" + alert)

if __name__ == "__main__":
    main() 
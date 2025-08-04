#!/usr/bin/env python3
"""
Complexity Threshold Checker for Memory Bank System
Checks if complexity exceeds 2x baseline and generates alerts.
"""

import json
import sys
from pathlib import Path
from typing import Dict, List
from datetime import datetime

class ComplexityThresholdChecker:
    def __init__(self):
        # Baseline complexity scores (current state)
        self.baseline = {
            'workflow-level4.mdc': 80,
            'reflection-comprehensive.mdc': 70,
            'architectural-planning.mdc': 90,
            'phased-implementation.mdc': 75,
            'main-optimized.mdc': 60,
            'hierarchical-rule-loading.mdc': 45,
            'mode-transition-optimization.mdc': 40,
            'optimization-integration.mdc': 50,
            'optimized-workflow-level1.mdc': 30,
            'optimized-creative-template.mdc': 35
        }
        
        self.threshold_multiplier = 2.0  # 2x baseline

    def load_static_results(self) -> Dict:
        """Load static analysis results"""
        try:
            with open('static-complexity-results.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("❌ No static complexity results found")
            return {}

    def load_gpt_results(self) -> Dict:
        """Load GPT analysis results"""
        try:
            with open('gpt-complexity-results.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print("⚠️  No GPT complexity results found")
            return {}

    def check_threshold(self) -> Dict:
        """Check if complexity exceeds threshold"""
        static_results = self.load_static_results()
        gpt_results = self.load_gpt_results()
        
        threshold_report = {
            'timestamp': datetime.now().isoformat(),
            'threshold_exceeded': False,
            'exceeded_files': [],
            'warnings': [],
            'recommendations': [],
            'summary': {
                'files_checked': 0,
                'files_exceeded': 0,
                'total_baseline': sum(self.baseline.values()),
                'total_current': 0
            }
        }
        
        # Check static analysis results
        if static_results and 'file_analysis' in static_results:
            for file_path, analysis in static_results['file_analysis'].items():
                threshold_report['summary']['files_checked'] += 1
                threshold_report['summary']['total_current'] += analysis['complexity_score']
                
                # Find matching baseline file
                baseline_file = None
                for baseline_name in self.baseline.keys():
                    if baseline_name in file_path:
                        baseline_file = baseline_name
                        break
                
                if baseline_file:
                    baseline_score = self.baseline[baseline_file]
                    threshold = baseline_score * self.threshold_multiplier
                    current_score = analysis['complexity_score']
                    
                    if current_score > threshold:
                        threshold_report['threshold_exceeded'] = True
                        threshold_report['summary']['files_exceeded'] += 1
                        
                        exceeded_info = {
                            'file': file_path,
                            'current_score': current_score,
                            'baseline_score': baseline_score,
                            'threshold': threshold,
                            'excess_percentage': ((current_score - threshold) / threshold) * 100,
                            'size_kb': analysis.get('size_kb', 0),
                            'line_count': analysis.get('line_count', 0)
                        }
                        
                        threshold_report['exceeded_files'].append(exceeded_info)
                        
                        # Generate specific recommendations
                        if exceeded_info['excess_percentage'] > 50:
                            threshold_report['recommendations'].append(
                                f"🚨 CRITICAL: {file_path} is {exceeded_info['excess_percentage']:.1f}% over threshold"
                            )
                        else:
                            threshold_report['recommendations'].append(
                                f"⚠️  WARNING: {file_path} exceeds threshold by {exceeded_info['excess_percentage']:.1f}%"
                            )
        
        # Check GPT analysis results
        if gpt_results and 'high_complexity_files' in gpt_results:
            for file_info in gpt_results['high_complexity_files']:
                if file_info['complexity'] > 8:  # High complexity threshold
                    threshold_report['warnings'].append(
                        f"🧠 SEMANTIC: {file_info['file']} has high semantic complexity ({file_info['complexity']}/10)"
                    )
                
                if file_info['cursor_compatibility'] < 5:  # Low Cursor compatibility
                    threshold_report['warnings'].append(
                        f"🔧 CURSOR: {file_info['file']} has low Cursor compatibility ({file_info['cursor_compatibility']}/10)"
                    )
        
        # Generate overall recommendations
        if threshold_report['threshold_exceeded']:
            threshold_report['recommendations'].append(
                "💡 Consider splitting complex files into smaller, more manageable modules"
            )
            threshold_report['recommendations'].append(
                "💡 Review and simplify mandatory rules that might be causing conflicts"
            )
        
        if len(threshold_report['warnings']) > 5:
            threshold_report['recommendations'].append(
                "💡 Consider consolidating similar rule files to reduce complexity"
            )
        
        return threshold_report

    def generate_report(self, report: Dict) -> str:
        """Generate a formatted report"""
        report_text = []
        report_text.append("# 🚨 COMPLEXITY THRESHOLD REPORT")
        report_text.append(f"**Generated:** {report['timestamp']}")
        report_text.append("")
        
        # Summary
        report_text.append("## 📊 SUMMARY")
        report_text.append(f"- Files checked: {report['summary']['files_checked']}")
        report_text.append(f"- Files exceeded threshold: {report['summary']['files_exceeded']}")
        report_text.append(f"- Total baseline complexity: {report['summary']['total_baseline']}")
        report_text.append(f"- Total current complexity: {report['summary']['total_current']:.1f}")
        report_text.append("")
        
        # Exceeded files
        if report['exceeded_files']:
            report_text.append("## 🚨 THRESHOLD EXCEEDED FILES")
            for file_info in sorted(report['exceeded_files'], key=lambda x: x['excess_percentage'], reverse=True):
                report_text.append(f"### {file_info['file']}")
                report_text.append(f"- **Current Score:** {file_info['current_score']:.1f}")
                report_text.append(f"- **Baseline:** {file_info['baseline_score']}")
                report_text.append(f"- **Threshold:** {file_info['threshold']}")
                report_text.append(f"- **Excess:** {file_info['excess_percentage']:.1f}%")
                report_text.append(f"- **Size:** {file_info['size_kb']:.1f} KB, {file_info['line_count']} lines")
                report_text.append("")
        
        # Warnings
        if report['warnings']:
            report_text.append("## ⚠️  WARNINGS")
            for warning in report['warnings']:
                report_text.append(f"- {warning}")
            report_text.append("")
        
        # Recommendations
        if report['recommendations']:
            report_text.append("## 💡 RECOMMENDATIONS")
            for rec in report['recommendations']:
                report_text.append(f"- {rec}")
            report_text.append("")
        
        return "\n".join(report_text)

def main():
    checker = ComplexityThresholdChecker()
    report = checker.check_threshold()
    
    # Print console output
    print("🔍 COMPLEXITY THRESHOLD CHECK")
    print("=" * 50)
    print(f"Timestamp: {report['timestamp']}")
    print(f"Files checked: {report['summary']['files_checked']}")
    print(f"Files exceeded threshold: {report['summary']['files_exceeded']}")
    
    if report['exceeded_files']:
        print(f"\n🚨 THRESHOLD EXCEEDED: {len(report['exceeded_files'])} files")
        for file_info in sorted(report['exceeded_files'], key=lambda x: x['excess_percentage'], reverse=True):
            print(f"  - {file_info['file']}: {file_info['excess_percentage']:.1f}% over threshold")
    
    if report['warnings']:
        print(f"\n⚠️  WARNINGS: {len(report['warnings'])}")
        for warning in report['warnings'][:5]:  # Show first 5 warnings
            print(f"  - {warning}")
    
    if report['recommendations']:
        print(f"\n💡 RECOMMENDATIONS:")
        for rec in report['recommendations']:
            print(f"  - {rec}")
    
    # Generate and save detailed report
    detailed_report = checker.generate_report(report)
    with open('complexity-threshold-report.md', 'w') as f:
        f.write(detailed_report)
    
    # Save JSON report
    with open('complexity-threshold-results.json', 'w') as f:
        json.dump(report, f, indent=2)
    
    print(f"\n📄 Reports saved:")
    print(f"  - complexity-threshold-report.md")
    print(f"  - complexity-threshold-results.json")
    
    # Exit with error code if threshold exceeded
    if report['threshold_exceeded']:
        print("\n❌ COMPLEXITY THRESHOLD EXCEEDED")
        print("Consider simplifying the affected files.")
        return False
    else:
        print("\n✅ All files within complexity limits")
        return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 
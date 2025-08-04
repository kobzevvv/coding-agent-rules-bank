#!/usr/bin/env python3
"""
Static Complexity Analyzer for Memory Bank System
Analyzes markdown files for complexity, conflicts, and best practice violations.
"""

import os
import re
import json
from pathlib import Path
from typing import Dict, List, Tuple
from datetime import datetime

class MarkdownComplexityAnalyzer:
    def __init__(self):
        self.complexity_indicators = {
            'mermaid_diagrams': 5,      # High complexity
            'code_blocks': 2,           # Medium complexity
            'nested_headers': 3,        # Structure complexity
            'conditional_logic': 4,     # Decision complexity
            'workflow_steps': 2,        # Process complexity
            'file_size_kb': 0.1,       # Size complexity
            'critical_rules': 3,        # Mandatory complexity
            'mode_transitions': 2,      # Transition complexity
            'visual_maps': 4,           # Visual complexity
        }
        
        self.conflict_patterns = [
            (r'CRITICAL.*MANDATORY', 'Mandatory rule complexity'),
            (r'MUST.*BEFORE', 'Sequential dependency complexity'),
            (r'NO.*continue', 'Blocking rule complexity'),
            (r'BLOCKED', 'Blocking rule detected'),
            (r'REQUIRES.*MODE', 'Mode dependency complexity'),
            (r'SWITCH.*MODE', 'Mode transition complexity'),
        ]
        
        self.best_practice_violations = [
            (r'p\.\w+', 'Avoid "p." prefix for fields'),
            (r'import pandas as pd', 'Avoid pandas aliasing'),
            (r'JOIN\s+(?!LEFT)', 'Prefer LEFT JOIN over simple JOIN'),
            (r'ON\s+\w+\.\w+\s*=\s*\w+\.\w+', 'Prefer USING() over ON for joins'),
            (r'pd\.', 'Avoid pandas aliasing (pd.)'),
            (r'as pd', 'Avoid pandas aliasing (as pd)'),
        ]

    def analyze_file(self, file_path: Path) -> Dict:
        """Analyze a single markdown file for complexity"""
        try:
            content = file_path.read_text(encoding='utf-8')
        except UnicodeDecodeError:
            content = file_path.read_text(encoding='latin-1')
        
        analysis = {
            'file_path': str(file_path),
            'complexity_score': 0,
            'size_kb': len(content) / 1024,
            'line_count': len(content.split('\n')),
            'issues': [],
            'conflicts': [],
            'best_practice_violations': [],
            'complexity_breakdown': {}
        }
        
        # Calculate complexity score
        mermaid_count = content.count('graph') + content.count('```mermaid')
        analysis['complexity_breakdown']['mermaid_diagrams'] = mermaid_count
        analysis['complexity_score'] += mermaid_count * self.complexity_indicators['mermaid_diagrams']
        
        code_blocks = content.count('```')
        analysis['complexity_breakdown']['code_blocks'] = code_blocks
        analysis['complexity_score'] += code_blocks * self.complexity_indicators['code_blocks']
        
        nested_headers = len(re.findall(r'^#{2,}', content, re.MULTILINE))
        analysis['complexity_breakdown']['nested_headers'] = nested_headers
        analysis['complexity_score'] += nested_headers * self.complexity_indicators['nested_headers']
        
        conditional_logic = content.count('if') + content.count('else') + content.count('switch')
        analysis['complexity_breakdown']['conditional_logic'] = conditional_logic
        analysis['complexity_score'] += conditional_logic * self.complexity_indicators['conditional_logic']
        
        workflow_steps = content.count('Step') + content.count('Phase')
        analysis['complexity_breakdown']['workflow_steps'] = workflow_steps
        analysis['complexity_score'] += workflow_steps * self.complexity_indicators['workflow_steps']
        
        mode_transitions = content.count('MODE') + content.count('switch')
        analysis['complexity_breakdown']['mode_transitions'] = mode_transitions
        analysis['complexity_score'] += mode_transitions * self.complexity_indicators['mode_transitions']
        
        visual_maps = content.count('mermaid') + content.count('graph')
        analysis['complexity_breakdown']['visual_maps'] = visual_maps
        analysis['complexity_score'] += visual_maps * self.complexity_indicators['visual_maps']
        
        # Size complexity
        analysis['complexity_score'] += analysis['size_kb'] * self.complexity_indicators['file_size_kb']
        
        # Check for critical rules
        for pattern, description in self.conflict_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                analysis['complexity_score'] += len(matches) * self.complexity_indicators['critical_rules']
                analysis['conflicts'].append(f"{description}: {len(matches)} instances")
        
        # Check best practice violations
        for pattern, violation in self.best_practice_violations:
            matches = re.findall(pattern, content, re.IGNORECASE)
            if matches:
                analysis['best_practice_violations'].append(f"{violation}: {len(matches)} instances")
        
        return analysis

    def analyze_repository(self, repo_path: str = '.') -> Dict:
        """Analyze entire repository"""
        repo_path = Path(repo_path)
        results = {
            'timestamp': datetime.now().isoformat(),
            'files_analyzed': 0,
            'total_complexity': 0,
            'high_complexity_files': [],
            'conflicts_found': [],
            'best_practice_violations': [],
            'recommendations': [],
            'file_analysis': {},
            'summary': {}
        }
        
        # Analyze all markdown files
        for file_path in repo_path.rglob('*.md'):
            if file_path.is_file():
                analysis = self.analyze_file(file_path)
                results['files_analyzed'] += 1
                results['total_complexity'] += analysis['complexity_score']
                results['file_analysis'][str(file_path)] = analysis
                
                # Flag high complexity files (>50 score)
                if analysis['complexity_score'] > 50:
                    results['high_complexity_files'].append({
                        'file': str(file_path),
                        'score': analysis['complexity_score'],
                        'size_kb': analysis['size_kb'],
                        'line_count': analysis['line_count'],
                        'issues': analysis['issues']
                    })
                
                # Collect conflicts and violations
                results['conflicts_found'].extend(analysis['conflicts'])
                results['best_practice_violations'].extend(analysis['best_practice_violations'])
        
        # Generate recommendations
        if results['total_complexity'] > 200:
            results['recommendations'].append("Consider splitting complex files into smaller modules")
        
        if len(results['conflicts_found']) > 0:
            results['recommendations'].append("Review mandatory rules for potential conflicts")
        
        if len(results['best_practice_violations']) > 0:
            results['recommendations'].append("Address best practice violations in code examples")
        
        # Calculate summary statistics
        if results['files_analyzed'] > 0:
            results['summary'] = {
                'average_complexity': results['total_complexity'] / results['files_analyzed'],
                'files_with_conflicts': len([f for f in results['file_analysis'].values() if f['conflicts']]),
                'files_with_violations': len([f for f in results['file_analysis'].values() if f['best_practice_violations']]),
                'total_size_kb': sum(f['size_kb'] for f in results['file_analysis'].values()),
                'total_lines': sum(f['line_count'] for f in results['file_analysis'].values())
            }
        
        return results

def main():
    analyzer = MarkdownComplexityAnalyzer()
    results = analyzer.analyze_repository()
    
    print("📊 STATIC COMPLEXITY ANALYSIS")
    print("=" * 50)
    print(f"Timestamp: {results['timestamp']}")
    print(f"Files analyzed: {results['files_analyzed']}")
    print(f"Total complexity score: {results['total_complexity']:.1f}")
    
    if results['summary']:
        print(f"Average complexity: {results['summary']['average_complexity']:.1f}")
        print(f"Total size: {results['summary']['total_size_kb']:.1f} KB")
        print(f"Total lines: {results['summary']['total_lines']}")
    
    if results['high_complexity_files']:
        print("\n🚨 HIGH COMPLEXITY FILES:")
        for file_info in sorted(results['high_complexity_files'], key=lambda x: x['score'], reverse=True):
            print(f"  - {file_info['file']}: {file_info['score']:.1f} ({(file_info['size_kb']):.1f} KB, {file_info['line_count']} lines)")
    
    if results['conflicts_found']:
        print("\n⚠️  CONFLICTS FOUND:")
        for conflict in set(results['conflicts_found']):
            print(f"  - {conflict}")
    
    if results['best_practice_violations']:
        print("\n❌ BEST PRACTICE VIOLATIONS:")
        for violation in set(results['best_practice_violations']):
            print(f"  - {violation}")
    
    if results['recommendations']:
        print("\n💡 RECOMMENDATIONS:")
        for rec in results['recommendations']:
            print(f"  - {rec}")
    
    # Save results to JSON file
    with open('static-complexity-results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Results saved to: static-complexity-results.json")

if __name__ == "__main__":
    main() 
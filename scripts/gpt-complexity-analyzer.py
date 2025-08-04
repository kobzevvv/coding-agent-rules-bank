#!/usr/bin/env python3
"""
GPT-3.5 Semantic Complexity Analyzer for Memory Bank System
Analyzes markdown files for semantic complexity, rule conflicts, and Cursor compatibility.
"""

import os
import json
import time
from pathlib import Path
from typing import Dict, List, Optional
from datetime import datetime

try:
    import openai
except ImportError:
    print("❌ OpenAI library not found. Install with: pip install openai")
    exit(1)

class GPTComplexityAnalyzer:
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        if self.api_key:
            openai.api_key = self.api_key
        else:
            print("⚠️  No OpenAI API key found. Set OPENAI_API_KEY environment variable.")
            print("   Semantic analysis will be skipped.")
        
        self.analysis_prompts = {
            'rule_conflicts': """
            Analyze this markdown file for potential rule conflicts in Cursor settings:
            
            File: {file_path}
            Content: {content}
            
            Look for:
            1. Contradictory instructions or rules
            2. Mandatory rules that might conflict with each other
            3. Complex rule hierarchies that could confuse users
            4. Rules that might be hard to follow in Cursor's interface
            5. Dependencies between different rule files
            6. Rules that might exceed Cursor's context limits
            
            Return JSON: {{"conflicts": ["list of specific conflicts"], "complexity_rating": 1-10, "reasoning": "explanation of complexity"}}
            """,
            
            'best_practices': """
            Analyze this markdown file for code best practice violations:
            
            File: {file_path}
            Content: {content}
            
            Check for:
            1. SQL best practice violations (JOIN vs LEFT JOIN, USING vs ON)
            2. Python naming convention violations
            3. Anti-patterns in code examples
            4. Contradictions with recognized coding standards
            5. Inconsistent coding style examples
            6. Outdated or deprecated patterns
            
            Return JSON: {{"violations": ["list of specific violations"], "severity": "low/medium/high", "reasoning": "explanation"}}
            """,
            
            'cursor_compatibility': """
            Analyze this markdown file for Cursor compatibility issues:
            
            File: {file_path}
            Content: {content}
            
            Check for:
            1. Rules that might be too complex for Cursor's context limits
            2. Instructions that could confuse users in Cursor settings
            3. Potential conflicts between different rule files
            4. Rules that might not work well in Cursor's environment
            5. Instructions that assume features Cursor might not have
            6. Complex workflows that might be hard to follow in Cursor
            
            Return JSON: {{"issues": ["list of specific issues"], "cursor_compatibility": 1-10, "reasoning": "explanation"}}
            """
        }

    def analyze_with_gpt(self, content: str, file_path: str, analysis_type: str) -> Dict:
        """Analyze content using GPT-3.5"""
        if not self.api_key:
            return {"error": "OpenAI API key not found"}
        
        prompt = self.analysis_prompts[analysis_type].format(
            file_path=file_path,
            content=content[:3000]  # Limit content for token efficiency
        )
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.3
            )
            
            result_text = response.choices[0].message.content
            try:
                result = json.loads(result_text)
                return result
            except json.JSONDecodeError:
                # Fallback parsing if JSON is malformed
                return {
                    "error": "Failed to parse GPT response",
                    "raw_response": result_text,
                    "analysis_type": analysis_type
                }
        except Exception as e:
            return {"error": f"GPT analysis failed: {str(e)}"}

    def analyze_repository_semantic(self, repo_path: str = '.') -> Dict:
        """Perform semantic analysis of repository"""
        repo_path = Path(repo_path)
        results = {
            'timestamp': datetime.now().isoformat(),
            'files_analyzed': 0,
            'rule_conflicts': [],
            'best_practice_violations': [],
            'cursor_compatibility_issues': [],
            'high_complexity_files': [],
            'analysis_errors': [],
            'file_analysis': {}
        }
        
        # Focus on rule files and documentation
        rule_patterns = [
            '.cursor/rules/**/*.md',
            'custom_modes/*.md',
            'memory-bank/*.md',
            '*.md'  # Also check root level markdown files
        ]
        
        analyzed_files = set()
        
        for pattern in rule_patterns:
            for file_path in repo_path.glob(pattern):
                if file_path.is_file() and str(file_path) not in analyzed_files:
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        analyzed_files.add(str(file_path))
                        results['files_analyzed'] += 1
                        
                        file_analysis = {
                            'file_path': str(file_path),
                            'size_kb': len(content) / 1024,
                            'line_count': len(content.split('\n')),
                            'conflicts': [],
                            'violations': [],
                            'cursor_issues': [],
                            'complexity_rating': 0,
                            'cursor_compatibility': 0
                        }
                        
                        # Analyze rule conflicts
                        conflict_analysis = self.analyze_with_gpt(
                            content, str(file_path), 'rule_conflicts'
                        )
                        if 'conflicts' in conflict_analysis:
                            file_analysis['conflicts'] = conflict_analysis['conflicts']
                            results['rule_conflicts'].extend(conflict_analysis['conflicts'])
                        
                        if 'complexity_rating' in conflict_analysis:
                            file_analysis['complexity_rating'] = conflict_analysis['complexity_rating']
                        
                        # Analyze best practices
                        practice_analysis = self.analyze_with_gpt(
                            content, str(file_path), 'best_practices'
                        )
                        if 'violations' in practice_analysis:
                            file_analysis['violations'] = practice_analysis['violations']
                            results['best_practice_violations'].extend(practice_analysis['violations'])
                        
                        # Analyze Cursor compatibility
                        cursor_analysis = self.analyze_with_gpt(
                            content, str(file_path), 'cursor_compatibility'
                        )
                        if 'issues' in cursor_analysis:
                            file_analysis['cursor_issues'] = cursor_analysis['issues']
                            results['cursor_compatibility_issues'].extend(cursor_analysis['issues'])
                        
                        if 'cursor_compatibility' in cursor_analysis:
                            file_analysis['cursor_compatibility'] = cursor_analysis['cursor_compatibility']
                        
                        # Flag high complexity
                        if file_analysis['complexity_rating'] > 7:
                            results['high_complexity_files'].append({
                                'file': str(file_path),
                                'complexity': file_analysis['complexity_rating'],
                                'cursor_compatibility': file_analysis['cursor_compatibility'],
                                'size_kb': file_analysis['size_kb'],
                                'line_count': file_analysis['line_count']
                            })
                        
                        results['file_analysis'][str(file_path)] = file_analysis
                        
                        # Add delay to avoid rate limiting
                        time.sleep(0.5)
                        
                    except Exception as e:
                        results['analysis_errors'].append({
                            'file': str(file_path),
                            'error': str(e)
                        })
        
        return results

def main():
    analyzer = GPTComplexityAnalyzer()
    results = analyzer.analyze_repository_semantic()
    
    print("🧠 GPT-3.5 SEMANTIC ANALYSIS")
    print("=" * 50)
    print(f"Timestamp: {results['timestamp']}")
    print(f"Files analyzed: {results['files_analyzed']}")
    
    if results['analysis_errors']:
        print(f"\n⚠️  ANALYSIS ERRORS: {len(results['analysis_errors'])}")
        for error in results['analysis_errors']:
            print(f"  - {error['file']}: {error['error']}")
    
    if results['rule_conflicts']:
        print(f"\n⚠️  RULE CONFLICTS: {len(set(results['rule_conflicts']))}")
        for conflict in set(results['rule_conflicts']):
            print(f"  - {conflict}")
    
    if results['best_practice_violations']:
        print(f"\n❌ BEST PRACTICE VIOLATIONS: {len(set(results['best_practice_violations']))}")
        for violation in set(results['best_practice_violations']):
            print(f"  - {violation}")
    
    if results['cursor_compatibility_issues']:
        print(f"\n🔧 CURSOR COMPATIBILITY ISSUES: {len(set(results['cursor_compatibility_issues']))}")
        for issue in set(results['cursor_compatibility_issues']):
            print(f"  - {issue}")
    
    if results['high_complexity_files']:
        print(f"\n🚨 HIGH COMPLEXITY FILES: {len(results['high_complexity_files'])}")
        for file_info in sorted(results['high_complexity_files'], key=lambda x: x['complexity'], reverse=True):
            print(f"  - {file_info['file']}: {file_info['complexity']}/10 (Cursor: {file_info['cursor_compatibility']}/10)")
    
    # Save results to JSON file
    with open('gpt-complexity-results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"\n📄 Results saved to: gpt-complexity-results.json")

if __name__ == "__main__":
    main() 
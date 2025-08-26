#!/usr/bin/env python3
"""
Diff Utilities for TEQUMSA AI Governance
Provides utility functions for analyzing git diffs and changes
Following TEQUMSA Level 100 system patterns
"""

import subprocess
import json
from typing import List, Dict, Tuple, Optional
from pathlib import Path


class DiffAnalyzer:
    """Analyze git diffs for AI governance purposes"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
    
    def get_commit_diff_stats(self, base_sha: str, head_sha: str) -> Dict:
        """Get diff statistics between two commits"""
        try:
            # Get numstat output
            result = subprocess.run([
                'git', 'diff', '--numstat', f'{base_sha}..{head_sha}'
            ], capture_output=True, text=True, cwd=self.repo_path)
            
            if result.returncode != 0:
                return {'error': f'Git diff failed: {result.stderr}'}
            
            total_additions = 0
            total_deletions = 0
            files_changed = 0
            file_stats = []
            
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                    
                parts = line.split('\t')
                if len(parts) >= 3:
                    additions = int(parts[0]) if parts[0] != '-' else 0
                    deletions = int(parts[1]) if parts[1] != '-' else 0
                    filename = parts[2]
                    
                    total_additions += additions
                    total_deletions += deletions
                    files_changed += 1
                    
                    file_stats.append({
                        'file': filename,
                        'additions': additions,
                        'deletions': deletions,
                        'total_changes': additions + deletions
                    })
            
            return {
                'total_additions': total_additions,
                'total_deletions': total_deletions,
                'total_changes': total_additions + total_deletions,
                'files_changed': files_changed,
                'file_stats': file_stats
            }
            
        except Exception as e:
            return {'error': str(e)}
    
    def get_changed_files(self, base_sha: str, head_sha: str) -> List[str]:
        """Get list of changed files between two commits"""
        try:
            result = subprocess.run([
                'git', 'diff', '--name-only', f'{base_sha}..{head_sha}'
            ], capture_output=True, text=True, cwd=self.repo_path)
            
            if result.returncode != 0:
                return []
            
            return [f.strip() for f in result.stdout.split('\n') if f.strip()]
            
        except Exception:
            return []
    
    def categorize_changed_files(self, changed_files: List[str]) -> Dict[str, List[str]]:
        """Categorize changed files by type"""
        categories = {
            'backend': [],
            'frontend': [],
            'tests': [],
            'docs': [],
            'config': [],
            'security': [],
            'ai_related': [],
            'workflows': [],
            'other': []
        }
        
        for file in changed_files:
            file_lower = file.lower()
            
            # Security-sensitive patterns
            if any(pattern in file_lower for pattern in [
                'security', 'crypto', 'auth', 'tequmsa_l100_system_prompt'
            ]):
                categories['security'].append(file)
            # AI-related patterns
            elif any(pattern in file_lower for pattern in [
                'claude', 'ai', 'gaia', 'agent'
            ]):
                categories['ai_related'].append(file)
            # Backend patterns
            elif any(file.endswith(ext) for ext in ['.py']) or 'backend/' in file:
                categories['backend'].append(file)
            # Frontend patterns
            elif any(file.endswith(ext) for ext in ['.js', '.html', '.css']) or 'frontend/' in file:
                categories['frontend'].append(file)
            # Test patterns
            elif any(pattern in file_lower for pattern in ['test', 'spec']):
                categories['tests'].append(file)
            # Documentation patterns
            elif any(file.endswith(ext) for ext in ['.md']) or 'docs/' in file:
                categories['docs'].append(file)
            # Workflow patterns
            elif '.github/workflows/' in file or file.endswith('.yml') or file.endswith('.yaml'):
                categories['workflows'].append(file)
            # Configuration patterns
            elif any(file.endswith(ext) for ext in ['.json', '.txt']) or any(name in file for name in [
                'requirements', 'package', 'config'
            ]):
                categories['config'].append(file)
            else:
                categories['other'].append(file)
        
        return categories
    
    def analyze_commit_messages(self, base_sha: str, head_sha: str) -> List[Dict]:
        """Analyze commit messages for AI patterns"""
        try:
            result = subprocess.run([
                'git', 'log', '--pretty=format:{"sha":"%H","author":"%an","subject":"%s","body":"%b"}',
                f'{base_sha}..{head_sha}'
            ], capture_output=True, text=True, cwd=self.repo_path)
            
            if result.returncode != 0:
                return []
            
            commits = []
            for line in result.stdout.strip().split('\n'):
                if not line:
                    continue
                try:
                    commit_data = json.loads(line)
                    
                    # Analyze for AI patterns
                    ai_indicators = self._detect_ai_indicators(
                        commit_data.get('author', ''),
                        commit_data.get('subject', ''),
                        commit_data.get('body', '')
                    )
                    
                    commit_data['ai_indicators'] = ai_indicators
                    commits.append(commit_data)
                    
                except json.JSONDecodeError:
                    continue
            
            return commits
            
        except Exception:
            return []
    
    def _detect_ai_indicators(self, author: str, subject: str, body: str) -> Dict:
        """Detect AI involvement indicators in commit data"""
        indicators = {
            'ai_author': False,
            'ai_subject_keywords': [],
            'refactor_detected': False,
            'confidence_score': 0.0
        }
        
        # Check author patterns
        ai_author_patterns = ['claude-bot', 'ai-assistant', 'copilot', 'bot']
        if any(pattern in author.lower() for pattern in ai_author_patterns):
            indicators['ai_author'] = True
            indicators['confidence_score'] += 0.5
        
        # Check subject keywords
        ai_subject_keywords = [
            'ai-refactor', 'claude', 'ai-generated', 'auto-generated',
            'ai-assisted', 'refactor', 'automated'
        ]
        found_keywords = [kw for kw in ai_subject_keywords if kw in subject.lower()]
        indicators['ai_subject_keywords'] = found_keywords
        indicators['confidence_score'] += len(found_keywords) * 0.2
        
        # Check for refactoring patterns
        refactor_patterns = ['refactor', 'restructure', 'reorganize', 'cleanup']
        if any(pattern in subject.lower() or pattern in body.lower() for pattern in refactor_patterns):
            indicators['refactor_detected'] = True
            indicators['confidence_score'] += 0.3
        
        # Normalize confidence score
        indicators['confidence_score'] = min(indicators['confidence_score'], 1.0)
        
        return indicators
    
    def get_file_diff_content(self, base_sha: str, head_sha: str, file_path: str) -> Optional[str]:
        """Get diff content for a specific file"""
        try:
            result = subprocess.run([
                'git', 'diff', f'{base_sha}..{head_sha}', '--', file_path
            ], capture_output=True, text=True, cwd=self.repo_path)
            
            if result.returncode != 0:
                return None
            
            return result.stdout
            
        except Exception:
            return None
    
    def analyze_diff_complexity(self, diff_stats: Dict) -> Dict:
        """Analyze complexity of changes based on diff statistics"""
        total_changes = diff_stats.get('total_changes', 0)
        additions = diff_stats.get('total_additions', 0)
        deletions = diff_stats.get('total_deletions', 0)
        files_changed = diff_stats.get('files_changed', 0)
        
        complexity = {
            'size_category': 'unknown',
            'change_type': 'unknown',
            'risk_level': 'unknown',
            'review_time_estimate': 'unknown'
        }
        
        # Size categorization
        if total_changes <= 20:
            complexity['size_category'] = 'small'
            complexity['review_time_estimate'] = '5-10 minutes'
        elif total_changes <= 100:
            complexity['size_category'] = 'medium'
            complexity['review_time_estimate'] = '15-30 minutes'
        elif total_changes <= 500:
            complexity['size_category'] = 'large'
            complexity['review_time_estimate'] = '45-90 minutes'
        else:
            complexity['size_category'] = 'xlarge'
            complexity['review_time_estimate'] = '2+ hours'
        
        # Change type analysis
        if deletions > additions * 1.5:
            complexity['change_type'] = 'refactoring'
        elif additions > deletions * 2:
            complexity['change_type'] = 'feature_addition'
        else:
            complexity['change_type'] = 'balanced_changes'
        
        # Risk level assessment
        if files_changed > 20 or total_changes > 1000:
            complexity['risk_level'] = 'high'
        elif files_changed > 10 or total_changes > 200:
            complexity['risk_level'] = 'medium'
        else:
            complexity['risk_level'] = 'low'
        
        return complexity


def main():
    """CLI interface for diff analysis"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze git diffs for AI governance')
    parser.add_argument('--base-sha', required=True, help='Base commit SHA')
    parser.add_argument('--head-sha', required=True, help='Head commit SHA')
    parser.add_argument('--repo-path', default='.', help='Repository path')
    parser.add_argument('--output-json', action='store_true', help='Output JSON format')
    
    args = parser.parse_args()
    
    analyzer = DiffAnalyzer(args.repo_path)
    
    # Get diff statistics
    diff_stats = analyzer.get_commit_diff_stats(args.base_sha, args.head_sha)
    
    # Get changed files
    changed_files = analyzer.get_changed_files(args.base_sha, args.head_sha)
    
    # Categorize files
    file_categories = analyzer.categorize_changed_files(changed_files)
    
    # Analyze commits
    commits = analyzer.analyze_commit_messages(args.base_sha, args.head_sha)
    
    # Analyze complexity
    complexity = analyzer.analyze_diff_complexity(diff_stats)
    
    result = {
        'diff_stats': diff_stats,
        'changed_files': changed_files,
        'file_categories': file_categories,
        'commits': commits,
        'complexity': complexity
    }
    
    if args.output_json:
        print(json.dumps(result, indent=2))
    else:
        print(f"Total changes: {diff_stats.get('total_changes', 0)} lines")
        print(f"Files changed: {len(changed_files)}")
        print(f"Complexity: {complexity['size_category']} ({complexity['risk_level']} risk)")


if __name__ == '__main__':
    main()
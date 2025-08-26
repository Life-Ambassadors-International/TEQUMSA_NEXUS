#!/usr/bin/env python3
"""
AI Refactor Test Guard for TEQUMSA AI Governance
Enforces test updates for AI-driven refactors following TEQUMSA Level 100 protocols
Ensures code quality and prevents regressions from AI-assisted changes
"""

import json
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Optional
import argparse

# Import our diff utilities
from diff_utils import DiffAnalyzer


class RefactorTestGuard:
    """Guard against AI refactors without corresponding test updates"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.diff_analyzer = DiffAnalyzer(repo_path)
        self.ai_confidence_threshold = 0.6
    
    def analyze_refactor_changes(self, base_sha: str, head_sha: str) -> Dict:
        """Analyze changes for AI refactor patterns and test coverage"""
        
        # Get diff statistics
        diff_stats = self.diff_analyzer.get_commit_diff_stats(base_sha, head_sha)
        if 'error' in diff_stats:
            return {'error': diff_stats['error']}
        
        # Get changed files
        changed_files = self.diff_analyzer.get_changed_files(base_sha, head_sha)
        
        # Categorize files
        file_categories = self.diff_analyzer.categorize_changed_files(changed_files)
        
        # Analyze commit messages for AI patterns
        commits = self.diff_analyzer.analyze_commit_messages(base_sha, head_sha)
        
        # Detect AI refactor commits
        ai_refactor_commits = self._identify_ai_refactor_commits(commits)
        
        # Check if any non-test files were modified by AI refactor
        ai_refactor_files = self._get_ai_refactor_files(
            ai_refactor_commits, changed_files, diff_stats
        )
        
        # Check test file updates
        test_files_updated = len(file_categories['tests']) > 0
        
        # Determine if guard should trigger
        ai_refactor_detected = len(ai_refactor_commits) > 0 or self._detect_ai_refactor_patterns(
            changed_files, diff_stats
        )
        
        # Generate guard result
        result = {
            'ai_refactor_detected': ai_refactor_detected,
            'test_files_updated': test_files_updated,
            'refactor_files': ai_refactor_files,
            'ai_refactor_commits': ai_refactor_commits,
            'guard_passed': not ai_refactor_detected or test_files_updated,
            'diff_stats': diff_stats,
            'file_categories': file_categories,
            'recommendations': self._generate_recommendations(
                ai_refactor_detected, test_files_updated, ai_refactor_files
            )
        }
        
        return result
    
    def _identify_ai_refactor_commits(self, commits: List[Dict]) -> List[Dict]:
        """Identify commits that appear to be AI-driven refactors"""
        ai_refactor_commits = []
        
        for commit in commits:
            ai_indicators = commit.get('ai_indicators', {})
            
            # Check if this looks like an AI refactor
            is_ai_refactor = (
                ai_indicators.get('ai_author', False) or
                ai_indicators.get('refactor_detected', False) or
                ai_indicators.get('confidence_score', 0) >= self.ai_confidence_threshold or
                self._check_ai_refactor_keywords(commit.get('subject', ''))
            )
            
            if is_ai_refactor:
                ai_refactor_commits.append({
                    'sha': commit['sha'],
                    'author': commit['author'],
                    'subject': commit['subject'],
                    'ai_indicators': ai_indicators
                })
        
        return ai_refactor_commits
    
    def _check_ai_refactor_keywords(self, commit_subject: str) -> bool:
        """Check commit subject for AI refactor keywords"""
        ai_refactor_keywords = [
            'ai-refactor',
            'claude refactor',
            'ai-assisted refactor',
            'automated refactor',
            'ai cleanup',
            'claude cleanup'
        ]
        
        subject_lower = commit_subject.lower()
        return any(keyword in subject_lower for keyword in ai_refactor_keywords)
    
    def _detect_ai_refactor_patterns(self, changed_files: List[str], diff_stats: Dict) -> bool:
        """Detect AI refactor patterns based on file changes and diff patterns"""
        
        # Look for large-scale refactoring patterns
        total_changes = diff_stats.get('total_changes', 0)
        deletions = diff_stats.get('total_deletions', 0)
        additions = diff_stats.get('total_additions', 0)
        
        # High deletion-to-addition ratio suggests refactoring
        if deletions > 0 and (deletions / max(additions, 1)) > 0.8:
            # Check if multiple code files are affected
            code_files = [f for f in changed_files if self._is_code_file(f)]
            if len(code_files) >= 3:
                return True
        
        # Large number of files with moderate changes
        if len(changed_files) >= 5 and total_changes > 100:
            code_files = [f for f in changed_files if self._is_code_file(f)]
            if len(code_files) / len(changed_files) > 0.6:  # Mostly code files
                return True
        
        return False
    
    def _is_code_file(self, file_path: str) -> bool:
        """Check if a file is a code file (not docs, config, etc.)"""
        code_extensions = ['.py', '.js', '.html', '.css', '.java', '.cpp', '.c', '.go', '.rs']
        return any(file_path.endswith(ext) for ext in code_extensions)
    
    def _is_test_file(self, file_path: str) -> bool:
        """Check if a file is a test file"""
        test_patterns = ['test_', '_test.', '/test/', '/tests/', 'spec_', '_spec.', '/spec/']
        file_lower = file_path.lower()
        return any(pattern in file_lower for pattern in test_patterns)
    
    def _get_ai_refactor_files(self, ai_refactor_commits: List[Dict], 
                              changed_files: List[str], diff_stats: Dict) -> List[str]:
        """Get list of files that were part of AI refactor"""
        
        # If we have explicit AI refactor commits, we could get more specific
        # For now, return non-test code files if AI refactor detected
        if len(ai_refactor_commits) > 0:
            code_files = [f for f in changed_files 
                         if self._is_code_file(f) and not self._is_test_file(f)]
            return code_files
        
        return []
    
    def _generate_recommendations(self, ai_refactor_detected: bool, 
                                test_files_updated: bool, 
                                refactor_files: List[str]) -> List[str]:
        """Generate recommendations based on guard analysis"""
        recommendations = []
        
        if ai_refactor_detected and not test_files_updated:
            recommendations.extend([
                "Add or update tests for refactored code to prevent regressions",
                "Review test coverage for modified functions and classes",
                "Consider adding integration tests for refactored components",
                "Verify that existing tests still pass with refactored code"
            ])
        
        if len(refactor_files) > 10:
            recommendations.append(
                "Large refactor detected - consider breaking into smaller, reviewable chunks"
            )
        
        if ai_refactor_detected:
            recommendations.extend([
                "Review AI-generated changes for alignment with TEQUMSA architecture patterns",
                "Verify that refactored code maintains original functionality",
                "Check for any introduced dependencies or security implications"
            ])
        
        return recommendations
    
    def run_guard(self, base_sha: str, head_sha: str, output_json: bool = False) -> int:
        """Run the refactor test guard and return exit code"""
        
        try:
            result = self.analyze_refactor_changes(base_sha, head_sha)
            
            if 'error' in result:
                print(f"Error analyzing changes: {result['error']}", file=sys.stderr)
                return 1
            
            # Output results
            if output_json:
                with open('refactor_guard_results.json', 'w') as f:
                    json.dump(result, f, indent=2)
                print("Results written to refactor_guard_results.json")
            else:
                self._print_guard_results(result)
            
            # Return exit code
            return 0 if result['guard_passed'] else 1
            
        except Exception as e:
            print(f"Guard execution error: {e}", file=sys.stderr)
            return 1
    
    def _print_guard_results(self, result: Dict):
        """Print human-readable guard results"""
        
        print("🛡️ TEQUMSA AI Refactor Test Guard Results")
        print("=" * 50)
        
        ai_refactor = result['ai_refactor_detected']
        test_updated = result['test_files_updated']
        guard_passed = result['guard_passed']
        
        print(f"AI Refactor Detected: {'✅ Yes' if ai_refactor else '❌ No'}")
        print(f"Test Files Updated: {'✅ Yes' if test_updated else '❌ No'}")
        print(f"Guard Status: {'✅ PASSED' if guard_passed else '🚫 FAILED'}")
        
        if result['refactor_files']:
            print(f"\nRefactored Files ({len(result['refactor_files'])}):")
            for file in result['refactor_files'][:10]:  # Show max 10
                print(f"  - {file}")
            if len(result['refactor_files']) > 10:
                print(f"  ... and {len(result['refactor_files']) - 10} more")
        
        if result['ai_refactor_commits']:
            print(f"\nAI Refactor Commits ({len(result['ai_refactor_commits'])}):")
            for commit in result['ai_refactor_commits'][:5]:  # Show max 5
                print(f"  - {commit['sha'][:8]}: {commit['subject']}")
        
        if result['recommendations']:
            print("\nRecommendations:")
            for rec in result['recommendations']:
                print(f"  • {rec}")
        
        # Summary stats
        diff_stats = result.get('diff_stats', {})
        print(f"\nDiff Summary:")
        print(f"  Total changes: {diff_stats.get('total_changes', 0)} lines")
        print(f"  Files changed: {diff_stats.get('files_changed', 0)}")
        print(f"  Additions: +{diff_stats.get('total_additions', 0)}")
        print(f"  Deletions: -{diff_stats.get('total_deletions', 0)}")


def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(description='TEQUMSA AI Refactor Test Guard')
    parser.add_argument('--base-sha', required=True, help='Base commit SHA')
    parser.add_argument('--head-sha', required=True, help='Head commit SHA')
    parser.add_argument('--repo-path', default='.', help='Repository path')
    parser.add_argument('--output-json', action='store_true', 
                       help='Output results as JSON file')
    parser.add_argument('--confidence-threshold', type=float, default=0.6,
                       help='AI confidence threshold (0.0-1.0)')
    
    args = parser.parse_args()
    
    # Create guard instance
    guard = RefactorTestGuard(args.repo_path)
    guard.ai_confidence_threshold = args.confidence_threshold
    
    # Run guard
    exit_code = guard.run_guard(args.base_sha, args.head_sha, args.output_json)
    
    sys.exit(exit_code)


if __name__ == '__main__':
    main()
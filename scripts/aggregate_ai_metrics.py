#!/usr/bin/env python3
"""
AI Metrics Aggregation for TEQUMSA Governance
Collects and analyzes AI assistance usage metrics following TEQUMSA Level 100 protocols
Provides insights for governance policy optimization and compliance monitoring
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
import argparse


class AIMetricsAggregator:
    """Aggregate and analyze AI governance metrics"""
    
    def __init__(self, repo_path: str = "."):
        self.repo_path = Path(repo_path)
        self.metrics_dir = self.repo_path / ".ai-metrics"
        self.usage_log = self.metrics_dir / "usage.jsonl"
    
    def ensure_metrics_directory(self):
        """Ensure metrics directory exists"""
        self.metrics_dir.mkdir(exist_ok=True)
        if not self.usage_log.exists():
            self.usage_log.touch()
    
    def log_usage_event(self, event_type: str, metadata: Dict[str, Any]):
        """Log a usage event to the metrics log"""
        self.ensure_metrics_directory()
        
        event = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'type': event_type,
            'metadata': metadata
        }
        
        with open(self.usage_log, 'a') as f:
            f.write(json.dumps(event) + '\n')
    
    def load_usage_events(self, start_date: Optional[str] = None, 
                         end_date: Optional[str] = None) -> List[Dict]:
        """Load usage events from the log, optionally filtered by date range"""
        
        if not self.usage_log.exists():
            return []
        
        events = []
        start_dt = datetime.fromisoformat(start_date.replace('Z', '+00:00')) if start_date else None
        end_dt = datetime.fromisoformat(end_date.replace('Z', '+00:00')) if end_date else None
        
        try:
            with open(self.usage_log, 'r') as f:
                for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    try:
                        event = json.loads(line)
                        event_dt = datetime.fromisoformat(event['timestamp'].replace('Z', '+00:00'))
                        
                        # Apply date filters
                        if start_dt and event_dt < start_dt:
                            continue
                        if end_dt and event_dt > end_dt:
                            continue
                        
                        events.append(event)
                    except (json.JSONDecodeError, KeyError, ValueError):
                        continue
        except FileNotFoundError:
            pass
        
        return events
    
    def aggregate_metrics(self, start_date: str, end_date: str) -> Dict[str, Any]:
        """Aggregate metrics for a given date range"""
        
        events = self.load_usage_events(start_date, end_date)
        
        metrics = {
            'period': {
                'start': start_date,
                'end': end_date,
                'total_events': len(events)
            },
            'event_types': {},
            'usage_patterns': {},
            'performance_metrics': {},
            'governance_metrics': {},
            'recommendations': []
        }
        
        # Count event types
        for event in events:
            event_type = event.get('type', 'unknown')
            metrics['event_types'][event_type] = metrics['event_types'].get(event_type, 0) + 1
        
        # Analyze specific event types
        self._analyze_review_events(events, metrics)
        self._analyze_refactor_events(events, metrics)
        self._analyze_labeling_events(events, metrics)
        self._analyze_summary_events(events, metrics)
        self._analyze_performance(events, metrics)
        self._generate_governance_insights(events, metrics)
        
        return metrics
    
    def _analyze_review_events(self, events: List[Dict], metrics: Dict):
        """Analyze AI review events"""
        review_events = [e for e in events if e.get('type') == 'ai_review']
        
        metrics['usage_patterns']['reviews'] = {
            'total': len(review_events),
            'avg_per_day': len(review_events) / 7 if review_events else 0,
            'gate_decisions': {},
            'diff_sizes': []
        }
        
        for event in review_events:
            metadata = event.get('metadata', {})
            
            # Gate decisions
            gate_status = metadata.get('gate_status')
            if gate_status:
                gate_key = f"gate_{gate_status}"
                metrics['usage_patterns']['reviews']['gate_decisions'][gate_key] = \
                    metrics['usage_patterns']['reviews']['gate_decisions'].get(gate_key, 0) + 1
            
            # Diff sizes
            diff_size = metadata.get('diff_lines')
            if diff_size:
                metrics['usage_patterns']['reviews']['diff_sizes'].append(diff_size)
    
    def _analyze_refactor_events(self, events: List[Dict], metrics: Dict):
        """Analyze AI refactor guard events"""
        refactor_events = [e for e in events if e.get('type') == 'refactor_guard']
        
        metrics['usage_patterns']['refactor_guards'] = {
            'total': len(refactor_events),
            'passed': 0,
            'failed': 0,
            'test_coverage_rate': 0.0
        }
        
        passed_count = 0
        for event in refactor_events:
            metadata = event.get('metadata', {})
            if metadata.get('guard_passed'):
                passed_count += 1
        
        if refactor_events:
            metrics['usage_patterns']['refactor_guards']['passed'] = passed_count
            metrics['usage_patterns']['refactor_guards']['failed'] = len(refactor_events) - passed_count
            metrics['usage_patterns']['refactor_guards']['test_coverage_rate'] = \
                passed_count / len(refactor_events)
    
    def _analyze_labeling_events(self, events: List[Dict], metrics: Dict):
        """Analyze auto-labeling events"""
        labeling_events = [e for e in events if e.get('type') == 'auto_labeling']
        
        metrics['usage_patterns']['auto_labeling'] = {
            'total': len(labeling_events),
            'label_categories': {},
            'readiness_assessments': {}
        }
        
        for event in labeling_events:
            metadata = event.get('metadata', {})
            labels = metadata.get('labels_applied', [])
            
            for label in labels:
                category = label.split(':')[0] if ':' in label else 'other'
                metrics['usage_patterns']['auto_labeling']['label_categories'][category] = \
                    metrics['usage_patterns']['auto_labeling']['label_categories'].get(category, 0) + 1
            
            readiness = metadata.get('readiness_status')
            if readiness:
                metrics['usage_patterns']['auto_labeling']['readiness_assessments'][readiness] = \
                    metrics['usage_patterns']['auto_labeling']['readiness_assessments'].get(readiness, 0) + 1
    
    def _analyze_summary_events(self, events: List[Dict], metrics: Dict):
        """Analyze AI summary events"""
        summary_events = [e for e in events if e.get('type') == 'ai_summary']
        
        metrics['usage_patterns']['summaries'] = {
            'total': len(summary_events),
            'avg_diff_size': 0,
            'trigger_methods': {}
        }
        
        diff_sizes = []
        for event in summary_events:
            metadata = event.get('metadata', {})
            
            # Track diff sizes
            diff_size = metadata.get('diff_lines')
            if diff_size:
                diff_sizes.append(diff_size)
            
            # Track trigger methods
            trigger = metadata.get('trigger_method', 'unknown')
            metrics['usage_patterns']['summaries']['trigger_methods'][trigger] = \
                metrics['usage_patterns']['summaries']['trigger_methods'].get(trigger, 0) + 1
        
        if diff_sizes:
            metrics['usage_patterns']['summaries']['avg_diff_size'] = sum(diff_sizes) / len(diff_sizes)
    
    def _analyze_performance(self, events: List[Dict], metrics: Dict):
        """Analyze performance metrics"""
        
        processing_times = []
        memory_usage = []
        
        for event in events:
            metadata = event.get('metadata', {})
            
            proc_time = metadata.get('processing_time_ms')
            if proc_time:
                processing_times.append(proc_time)
            
            mem_usage = metadata.get('memory_usage_mb')
            if mem_usage:
                memory_usage.append(mem_usage)
        
        metrics['performance_metrics'] = {
            'avg_processing_time_ms': sum(processing_times) / len(processing_times) if processing_times else 0,
            'max_processing_time_ms': max(processing_times) if processing_times else 0,
            'avg_memory_usage_mb': sum(memory_usage) / len(memory_usage) if memory_usage else 0,
            'max_memory_usage_mb': max(memory_usage) if memory_usage else 0,
            'total_samples': len(processing_times)
        }
    
    def _generate_governance_insights(self, events: List[Dict], metrics: Dict):
        """Generate governance insights and recommendations"""
        
        total_events = len(events)
        
        # Calculate governance metrics
        governance = {
            'compliance_rate': 0.0,
            'security_reviews': 0,
            'policy_violations': 0,
            'automation_adoption': 0.0
        }
        
        # Count security-related events
        security_events = [e for e in events if 'security' in str(e.get('metadata', {})).lower()]
        governance['security_reviews'] = len(security_events)
        
        # Calculate automation adoption (events with AI involvement)
        ai_events = [e for e in events if e.get('type') in [
            'ai_review', 'auto_labeling', 'ai_summary', 'refactor_guard'
        ]]
        if total_events > 0:
            governance['automation_adoption'] = len(ai_events) / total_events
        
        # Calculate compliance rate (refactor guards passed)
        refactor_events = [e for e in events if e.get('type') == 'refactor_guard']
        if refactor_events:
            passed_guards = sum(1 for e in refactor_events 
                              if e.get('metadata', {}).get('guard_passed'))
            governance['compliance_rate'] = passed_guards / len(refactor_events)
        
        metrics['governance_metrics'] = governance
        
        # Generate recommendations
        recommendations = []
        
        if governance['automation_adoption'] < 0.5:
            recommendations.append(
                "Low AI automation adoption - consider team training on governance workflows"
            )
        
        if governance['compliance_rate'] < 0.8:
            recommendations.append(
                "Low refactor guard compliance - review test update policies"
            )
        
        if governance['security_reviews'] == 0:
            recommendations.append(
                "No security reviews detected - verify security labeling accuracy"
            )
        
        perf_metrics = metrics.get('performance_metrics', {})
        avg_time = perf_metrics.get('avg_processing_time_ms', 0)
        if avg_time > 30000:  # 30 seconds
            recommendations.append(
                "High average processing time - consider workflow optimization"
            )
        
        metrics['recommendations'] = recommendations
    
    def export_metrics_report(self, metrics: Dict, output_file: Optional[str] = None) -> str:
        """Export metrics as a formatted report"""
        
        if not output_file:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = f"ai_metrics_report_{timestamp}.md"
        
        report_content = self._generate_markdown_report(metrics)
        
        output_path = self.metrics_dir / output_file
        with open(output_path, 'w') as f:
            f.write(report_content)
        
        return str(output_path)
    
    def _generate_markdown_report(self, metrics: Dict) -> str:
        """Generate markdown report from metrics"""
        
        period = metrics.get('period', {})
        usage = metrics.get('usage_patterns', {})
        performance = metrics.get('performance_metrics', {})
        governance = metrics.get('governance_metrics', {})
        recommendations = metrics.get('recommendations', [])
        
        report = f"""# TEQUMSA AI Governance Metrics Report

**Period**: {period.get('start', 'N/A')} to {period.get('end', 'N/A')}
**Total Events**: {period.get('total_events', 0)}
**Generated**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}

## Event Summary

"""
        
        event_types = metrics.get('event_types', {})
        for event_type, count in event_types.items():
            report += f"- **{event_type}**: {count} events\n"
        
        report += "\n## Usage Patterns\n\n"
        
        # Reviews section
        reviews = usage.get('reviews', {})
        if reviews.get('total', 0) > 0:
            report += f"""### AI Reviews
- **Total Reviews**: {reviews.get('total', 0)}
- **Average per Day**: {reviews.get('avg_per_day', 0):.1f}
- **Gate Decisions**: {dict(reviews.get('gate_decisions', {}))}

"""
        
        # Refactor guards section
        refactor = usage.get('refactor_guards', {})
        if refactor.get('total', 0) > 0:
            report += f"""### Refactor Guards
- **Total Guards**: {refactor.get('total', 0)}
- **Passed**: {refactor.get('passed', 0)}
- **Failed**: {refactor.get('failed', 0)}
- **Test Coverage Rate**: {refactor.get('test_coverage_rate', 0):.1%}

"""
        
        # Auto-labeling section
        labeling = usage.get('auto_labeling', {})
        if labeling.get('total', 0) > 0:
            report += f"""### Auto-Labeling
- **Total Events**: {labeling.get('total', 0)}
- **Label Categories**: {dict(labeling.get('label_categories', {}))}

"""
        
        # Performance section
        if performance.get('total_samples', 0) > 0:
            report += f"""## Performance Metrics

- **Average Processing Time**: {performance.get('avg_processing_time_ms', 0):.0f}ms
- **Max Processing Time**: {performance.get('max_processing_time_ms', 0):.0f}ms
- **Average Memory Usage**: {performance.get('avg_memory_usage_mb', 0):.1f}MB
- **Max Memory Usage**: {performance.get('max_memory_usage_mb', 0):.1f}MB

"""
        
        # Governance section
        report += f"""## Governance Metrics

- **Compliance Rate**: {governance.get('compliance_rate', 0):.1%}
- **Security Reviews**: {governance.get('security_reviews', 0)}
- **Automation Adoption**: {governance.get('automation_adoption', 0):.1%}
- **Policy Violations**: {governance.get('policy_violations', 0)}

"""
        
        # Recommendations section
        if recommendations:
            report += "## Recommendations\n\n"
            for rec in recommendations:
                report += f"- {rec}\n"
        
        report += "\n---\n*Generated by TEQUMSA AI Governance Metrics Aggregator*\n"
        
        return report


def main():
    """CLI interface for metrics aggregation"""
    
    parser = argparse.ArgumentParser(description='TEQUMSA AI Metrics Aggregator')
    parser.add_argument('--start-date', required=True, help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', required=True, help='End date (YYYY-MM-DD)')
    parser.add_argument('--repo-path', default='.', help='Repository path')
    parser.add_argument('--output-dir', help='Output directory for reports')
    parser.add_argument('--log-event', help='Log a usage event (JSON)')
    parser.add_argument('--format', choices=['json', 'markdown'], default='markdown',
                       help='Output format')
    
    args = parser.parse_args()
    
    # Create aggregator
    aggregator = AIMetricsAggregator(args.repo_path)
    
    if args.output_dir:
        aggregator.metrics_dir = Path(args.output_dir)
    
    # Log event if provided
    if args.log_event:
        try:
            event_data = json.loads(args.log_event)
            event_type = event_data.pop('type', 'manual_event')
            aggregator.log_usage_event(event_type, event_data)
            print(f"Logged event: {event_type}")
            return
        except json.JSONDecodeError:
            print("Error: Invalid JSON for log-event", file=sys.stderr)
            sys.exit(1)
    
    # Aggregate metrics
    try:
        metrics = aggregator.aggregate_metrics(args.start_date, args.end_date)
        
        if args.format == 'json':
            print(json.dumps(metrics, indent=2))
        else:
            report_path = aggregator.export_metrics_report(metrics)
            print(f"Metrics report generated: {report_path}")
            
    except Exception as e:
        print(f"Error aggregating metrics: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    main()
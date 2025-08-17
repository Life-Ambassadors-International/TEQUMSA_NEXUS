"""Time series utilities for TEQUMSA Level 100."""
from typing import List, Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, deque
import statistics


class TimeSeriesPoint:
    """A single time series data point."""
    
    def __init__(self, timestamp: datetime, value: float, metadata: Optional[Dict[str, Any]] = None):
        """Initialize time series point."""
        self.timestamp = timestamp
        self.value = value
        self.metadata = metadata or {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'timestamp': self.timestamp.isoformat(),
            'value': self.value,
            'metadata': self.metadata
        }


class TimeSeries:
    """Time series data container and processor."""
    
    def __init__(self, name: str, max_points: int = 10000):
        """Initialize time series."""
        self.name = name
        self.max_points = max_points
        self.points: deque = deque(maxlen=max_points)
    
    def add_point(self, timestamp: datetime, value: float, metadata: Optional[Dict[str, Any]] = None):
        """Add a new data point."""
        point = TimeSeriesPoint(timestamp, value, metadata)
        self.points.append(point)
    
    def add_current(self, value: float, metadata: Optional[Dict[str, Any]] = None):
        """Add data point with current timestamp."""
        self.add_point(datetime.utcnow(), value, metadata)
    
    def get_points(self, 
                   start_time: Optional[datetime] = None, 
                   end_time: Optional[datetime] = None,
                   limit: Optional[int] = None) -> List[TimeSeriesPoint]:
        """Get points within time range."""
        filtered_points = []
        
        for point in self.points:
            if start_time and point.timestamp < start_time:
                continue
            if end_time and point.timestamp > end_time:
                continue
            filtered_points.append(point)
        
        if limit:
            filtered_points = filtered_points[-limit:]
        
        return filtered_points
    
    def get_latest(self, count: int = 1) -> List[TimeSeriesPoint]:
        """Get latest N points."""
        return list(self.points)[-count:]
    
    def get_average(self, window_minutes: int = 60) -> Optional[float]:
        """Get average value over time window."""
        cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)
        recent_points = self.get_points(start_time=cutoff)
        
        if not recent_points:
            return None
        
        values = [point.value for point in recent_points]
        return statistics.mean(values)
    
    def get_trend(self, window_minutes: int = 60) -> Optional[str]:
        """Get trend direction over time window."""
        cutoff = datetime.utcnow() - timedelta(minutes=window_minutes)
        recent_points = self.get_points(start_time=cutoff)
        
        if len(recent_points) < 2:
            return None
        
        first_half = recent_points[:len(recent_points)//2]
        second_half = recent_points[len(recent_points)//2:]
        
        if not first_half or not second_half:
            return None
        
        first_avg = statistics.mean([p.value for p in first_half])
        second_avg = statistics.mean([p.value for p in second_half])
        
        diff = second_avg - first_avg
        if abs(diff) < 0.01:  # Threshold for "stable"
            return "stable"
        elif diff > 0:
            return "increasing"
        else:
            return "decreasing"
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            'name': self.name,
            'point_count': len(self.points),
            'latest_value': self.points[-1].value if self.points else None,
            'latest_timestamp': self.points[-1].timestamp.isoformat() if self.points else None,
            'average_1h': self.get_average(60),
            'trend_1h': self.get_trend(60)
        }


class TimeSeriesManager:
    """Manages multiple time series."""
    
    def __init__(self):
        """Initialize time series manager."""
        self.series: Dict[str, TimeSeries] = {}
    
    def create_series(self, name: str, max_points: int = 10000) -> TimeSeries:
        """Create a new time series."""
        series = TimeSeries(name, max_points)
        self.series[name] = series
        return series
    
    def get_series(self, name: str) -> Optional[TimeSeries]:
        """Get time series by name."""
        return self.series.get(name)
    
    def add_point(self, series_name: str, value: float, metadata: Optional[Dict[str, Any]] = None):
        """Add point to a time series."""
        if series_name not in self.series:
            self.create_series(series_name)
        
        self.series[series_name].add_current(value, metadata)
    
    def get_all_series_summary(self) -> Dict[str, Dict[str, Any]]:
        """Get summary of all time series."""
        return {name: series.to_dict() for name, series in self.series.items()}
    
    def cleanup_old_data(self, older_than_hours: int = 24):
        """Remove data older than specified hours."""
        cutoff = datetime.utcnow() - timedelta(hours=older_than_hours)
        
        for series in self.series.values():
            # Filter out old points
            series.points = deque(
                [p for p in series.points if p.timestamp >= cutoff],
                maxlen=series.max_points
            )


# Global time series manager
_manager = None


def get_time_series_manager() -> TimeSeriesManager:
    """Get the global time series manager."""
    global _manager
    if _manager is None:
        _manager = TimeSeriesManager()
    return _manager


def record_metric(series_name: str, value: float, metadata: Optional[Dict[str, Any]] = None):
    """Record a metric value."""
    manager = get_time_series_manager()
    manager.add_point(series_name, value, metadata)
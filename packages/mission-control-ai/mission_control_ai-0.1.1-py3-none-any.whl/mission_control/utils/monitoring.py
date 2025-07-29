"""Monitoring utilities for Mission Control"""

from typing import Dict, Any, List
from datetime import datetime
from collections import defaultdict
import threading
import time
from loguru import logger
from prometheus_client import Counter, Histogram, Gauge, start_http_server


class MissionMonitor:
    """Monitor mission execution metrics"""
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.start_time = None
        self.metrics = defaultdict(list)
        self._running = False
        self._thread = None
        
        # Prometheus metrics
        self.mission_counter = Counter('mission_total', 'Total missions executed')
        self.mission_duration = Histogram('mission_duration_seconds', 'Mission duration in seconds')
        self.active_agents = Gauge('active_agents', 'Number of active agents')
        self.task_counter = Counter('tasks_total', 'Total tasks executed', ['status'])
        self.error_counter = Counter('errors_total', 'Total errors encountered')
        
        # Start metrics server
        try:
            start_http_server(self.port)
            logger.info(f"Metrics server started on port {self.port}")
        except Exception as e:
            logger.warning(f"Failed to start metrics server: {e}")
    
    def start_mission(self, mission_id: str):
        """Start monitoring a mission"""
        self.start_time = time.time()
        self.mission_counter.inc()
        self.metrics[mission_id] = {
            "start_time": self.start_time,
            "events": []
        }
        
        logger.info(f"Started monitoring mission: {mission_id}")
    
    def record_task_completion(self, task_id: str, success: bool, duration: float):
        """Record task completion"""
        status = "success" if success else "failed"
        self.task_counter.labels(status=status).inc()
        
        self.metrics["tasks"].append({
            "task_id": task_id,
            "status": status,
            "duration": duration,
            "timestamp": datetime.now()
        })
    
    def update_active_agents(self, count: int):
        """Update active agent count"""
        self.active_agents.set(count)
    
    def record_error(self, error: str):
        """Record an error"""
        self.error_counter.inc()
        self.metrics["errors"].append({
            "error": error,
            "timestamp": datetime.now()
        })
    
    def end_mission(self, mission_id: str):
        """End monitoring a mission"""
        if mission_id in self.metrics and "start_time" in self.metrics[mission_id]:
            duration = time.time() - self.metrics[mission_id]["start_time"]
            self.mission_duration.observe(duration)
            self.metrics[mission_id]["duration"] = duration
            
            logger.info(f"Mission {mission_id} completed in {duration:.2f} seconds")
    
    def get_metrics(self) -> Dict[str, Any]:
        """Get current metrics"""
        return dict(self.metrics)
    
    def stop(self):
        """Stop monitoring"""
        self._running = False
        if self._thread:
            self._thread.join()
        
        logger.info("Mission monitor stopped")
"""Per-module time-window CSV partitioner."""

from datetime import datetime, timedelta
from pathlib import Path
import pandas as pd


class TimeWindowPartitioner:
    """Partition archival data by time window."""
    
    def __init__(self, base_path: str = "./data/archival", window_hours: int = 24):
        self.base_path = Path(base_path)
        self.window_hours = window_hours
    
    def get_partition_path(self, module: str, timestamp: datetime) -> Path:
        """Get partition file path for given module and time."""
        partition_key = timestamp.strftime(f"%Y%m%d_%H")
        partition_dir = self.base_path / module
        partition_dir.mkdir(parents=True, exist_ok=True)
        
        return partition_dir / f"{partition_key}.csv"
    
    def write_partition(self, module: str, data: dict, timestamp: datetime = None):
        """Write data to appropriate time partition."""
        if timestamp is None:
            timestamp = datetime.now()
        
        filepath = self.get_partition_path(module, timestamp)
        file_exists = filepath.exists()
        
        import csv
        with open(filepath, "a") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

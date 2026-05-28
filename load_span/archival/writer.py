"""Append-only JSON/CSV record writer."""

import json
import csv
from datetime import datetime
from pathlib import Path
from typing import Dict, Any


class ArchivalWriter:
    """Append-only data archival writer."""
    
    def __init__(self, base_path: str = "./data/archival"):
        self.base_path = Path(base_path)
        self.base_path.mkdir(parents=True, exist_ok=True)
    
    def write_json(self, data: Dict[str, Any], filename: str):
        """Write data to JSON file with timestamp."""
        filepath = self.base_path / f"{filename}_{datetime.now().strftime('%Y%m%d')}.json"
        
        record = {
            "timestamp": datetime.now().isoformat(),
            "data": data
        }
        
        with open(filepath, "a") as f:
            f.write(json.dumps(record) + "\n")
    
    def write_csv(self, data: Dict[str, Any], filename: str):
        """Write data to CSV file."""
        filepath = self.base_path / f"{filename}_{datetime.now().strftime('%Y%m%d')}.csv"
        
        file_exists = filepath.exists()
        
        with open(filepath, "a") as f:
            writer = csv.DictWriter(f, fieldnames=data.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(data)

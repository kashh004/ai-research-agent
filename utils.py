import logging
import os
from datetime import datetime
from typing import Dict, Any

def setup_logging(log_level: str = "INFO") -> logging.Logger:
    """Setup logging configuration"""
    os.makedirs("logs", exist_ok=True)
    
    log_file = f"logs/research_agent_{datetime.now().strftime('%Y%m%d')}.log"
    
    logging.basicConfig(
        level=getattr(logging, log_level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)

def safe_execute(func, *args, **kwargs) -> Dict[str, Any]:
    """Safely execute a function with error handling"""
    try:
        result = func(*args, **kwargs)
        return {"success": True, "result": result, "error": None}
    except Exception as e:
        return {"success": False, "result": None, "error": str(e)}

def validate_query(query: str) -> bool:
    """Validate search query"""
    if not query or len(query.strip()) < 3:
        return False
    return True

def format_authors(authors: list) -> str:
    """Format author list for display"""
    if not authors:
        return "Unknown"
    if len(authors) <= 3:
        return ", ".join(authors)
    return f"{', '.join(authors[:3])} et al."

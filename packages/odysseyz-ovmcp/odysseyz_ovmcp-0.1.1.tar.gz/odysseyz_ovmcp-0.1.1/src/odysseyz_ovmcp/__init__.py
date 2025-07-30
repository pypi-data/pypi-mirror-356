from mcp.server.fastmcp import FastMCP
import json
import random
from datetime import datetime, timedelta
import base64
import hashlib
from typing import List, Dict, Any, Optional
import re
import os
import subprocess
import platform
import psutil
import requests
import uuid
import tempfile
import shutil
import zipfile
import csv
import xml.etree.ElementTree as ET
from collections import Counter
import math
import statistics

mcp = FastMCP("SuperMCP")

# System Tools
@mcp.tool()
def execute_command(command: str, shell: bool = True) -> Dict[str, Any]:
    """Execute system command"""
    try:
        result = subprocess.run(command, shell=shell, capture_output=True, text=True)
        return {
            "stdout": result.stdout,
            "stderr": result.stderr,
            "returncode": result.returncode,
            "success": result.returncode == 0
        }
    except Exception as e:
        return {"error": str(e), "success": False}

@mcp.tool()
def system_info() -> Dict[str, Any]:
    """Get system information"""
    return {
        "platform": platform.system(),
        "platform_release": platform.release(),
        "platform_version": platform.version(),
        "architecture": platform.machine(),
        "processor": platform.processor(),
        "cpu_count": psutil.cpu_count(),
        "memory_total": psutil.virtual_memory().total,
        "memory_available": psutil.virtual_memory().available,
        "disk_usage": {
            "total": psutil.disk_usage('/').total,
            "used": psutil.disk_usage('/').used,
            "free": psutil.disk_usage('/').free,
            "percent": psutil.disk_usage('/').percent
        }
    }

# File Operations
@mcp.tool()
def file_operations(operation: str, path: str, content: Optional[str] = None, destination: Optional[str] = None) -> Dict[str, Any]:
    """File operations: read, write, append, delete, copy, move, exists"""
    try:
        if operation == "read":
            with open(path, 'r', encoding='utf-8') as f:
                return {"content": f.read(), "success": True}
        elif operation == "write":
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content or "")
            return {"success": True, "message": f"Written to {path}"}
        elif operation == "append":
            with open(path, 'a', encoding='utf-8') as f:
                f.write(content or "")
            return {"success": True, "message": f"Appended to {path}"}
        elif operation == "delete":
            os.remove(path)
            return {"success": True, "message": f"Deleted {path}"}
        elif operation == "copy":
            shutil.copy2(path, destination)
            return {"success": True, "message": f"Copied {path} to {destination}"}
        elif operation == "move":
            shutil.move(path, destination)
            return {"success": True, "message": f"Moved {path} to {destination}"}
        elif operation == "exists":
            return {"exists": os.path.exists(path), "success": True}
        else:
            return {"error": f"Unknown operation: {operation}", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}

@mcp.tool()
def directory_operations(operation: str, path: str, recursive: bool = False) -> Dict[str, Any]:
    """Directory operations: create, delete, list"""
    try:
        if operation == "create":
            os.makedirs(path, exist_ok=True)
            return {"success": True, "message": f"Created directory {path}"}
        elif operation == "delete":
            if recursive:
                shutil.rmtree(path)
            else:
                os.rmdir(path)
            return {"success": True, "message": f"Deleted directory {path}"}
        elif operation == "list":
            items = []
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                items.append({
                    "name": item,
                    "type": "directory" if os.path.isdir(item_path) else "file",
                    "size": os.path.getsize(item_path) if os.path.isfile(item_path) else None,
                    "modified": datetime.fromtimestamp(os.path.getmtime(item_path)).isoformat()
                })
            return {"items": items, "count": len(items), "success": True}
        else:
            return {"error": f"Unknown operation: {operation}", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}

# Archive Operations
@mcp.tool()
def archive_operations(operation: str, archive_path: str, files: Optional[List[str]] = None, extract_to: Optional[str] = None) -> Dict[str, Any]:
    """Archive operations: create, extract, list"""
    try:
        if operation == "create":
            with zipfile.ZipFile(archive_path, 'w', zipfile.ZIP_DEFLATED) as zf:
                for file in files or []:
                    if os.path.isdir(file):
                        for root, dirs, files_in_dir in os.walk(file):
                            for f in files_in_dir:
                                zf.write(os.path.join(root, f))
                    else:
                        zf.write(file)
            return {"success": True, "message": f"Created archive {archive_path}"}
        elif operation == "extract":
            with zipfile.ZipFile(archive_path, 'r') as zf:
                zf.extractall(extract_to or '.')
            return {"success": True, "message": f"Extracted {archive_path}"}
        elif operation == "list":
            with zipfile.ZipFile(archive_path, 'r') as zf:
                return {"files": zf.namelist(), "success": True}
        else:
            return {"error": f"Unknown operation: {operation}", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}

# Network Tools
@mcp.tool()
def http_request(url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None, 
                data: Optional[Dict[str, Any]] = None, timeout: int = 30) -> Dict[str, Any]:
    """Make HTTP request"""
    try:
        response = requests.request(
            method=method,
            url=url,
            headers=headers,
            json=data if method in ["POST", "PUT", "PATCH"] else None,
            params=data if method == "GET" else None,
            timeout=timeout
        )
        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": response.text,
            "json": response.json() if response.headers.get('content-type', '').startswith('application/json') else None,
            "success": response.ok
        }
    except Exception as e:
        return {"error": str(e), "success": False}

@mcp.tool()
def download_file(url: str, destination: str, chunk_size: int = 8192) -> Dict[str, Any]:
    """Download file from URL"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        total_size = int(response.headers.get('content-length', 0))
        downloaded = 0
        
        with open(destination, 'wb') as f:
            for chunk in response.iter_content(chunk_size=chunk_size):
                if chunk:
                    f.write(chunk)
                    downloaded += len(chunk)
        
        return {
            "success": True,
            "destination": destination,
            "size": downloaded,
            "message": f"Downloaded {downloaded} bytes to {destination}"
        }
    except Exception as e:
        return {"error": str(e), "success": False}

# Data Processing
@mcp.tool()
def csv_operations(operation: str, file_path: str, data: Optional[List[Dict[str, Any]]] = None, 
                  delimiter: str = ",", encoding: str = "utf-8") -> Dict[str, Any]:
    """CSV operations: read, write, analyze"""
    try:
        if operation == "read":
            with open(file_path, 'r', encoding=encoding) as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                rows = list(reader)
                return {"data": rows, "count": len(rows), "columns": reader.fieldnames, "success": True}
        elif operation == "write":
            if not data:
                return {"error": "No data provided", "success": False}
            with open(file_path, 'w', newline='', encoding=encoding) as f:
                writer = csv.DictWriter(f, fieldnames=data[0].keys(), delimiter=delimiter)
                writer.writeheader()
                writer.writerows(data)
            return {"success": True, "message": f"Written {len(data)} rows to {file_path}"}
        elif operation == "analyze":
            with open(file_path, 'r', encoding=encoding) as f:
                reader = csv.DictReader(f, delimiter=delimiter)
                rows = list(reader)
                
                analysis = {
                    "row_count": len(rows),
                    "columns": reader.fieldnames,
                    "column_stats": {}
                }
                
                for col in reader.fieldnames:
                    values = [row[col] for row in rows if row[col]]
                    analysis["column_stats"][col] = {
                        "non_empty": len(values),
                        "empty": len(rows) - len(values),
                        "unique": len(set(values)),
                        "sample": values[:5] if values else []
                    }
                
                return {"analysis": analysis, "success": True}
        else:
            return {"error": f"Unknown operation: {operation}", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}

@mcp.tool()
def json_operations(operation: str, data: Any = None, file_path: Optional[str] = None, 
                   query: Optional[str] = None) -> Dict[str, Any]:
    """JSON operations: parse, stringify, validate, query, transform"""
    try:
        if operation == "parse":
            if file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    return {"data": json.load(f), "success": True}
            else:
                return {"data": json.loads(data), "success": True}
        elif operation == "stringify":
            return {"json": json.dumps(data, indent=2, ensure_ascii=False), "success": True}
        elif operation == "validate":
            try:
                json.loads(data) if isinstance(data, str) else json.dumps(data)
                return {"valid": True, "success": True}
            except:
                return {"valid": False, "success": True}
        elif operation == "query" and query:
            # Simple JSONPath-like query
            result = data
            for key in query.split('.'):
                if key.isdigit():
                    result = result[int(key)]
                else:
                    result = result[key]
            return {"result": result, "success": True}
        elif operation == "transform":
            # Flatten nested JSON
            def flatten(obj, prefix=''):
                flat = {}
                if isinstance(obj, dict):
                    for k, v in obj.items():
                        flat.update(flatten(v, f"{prefix}{k}."))
                elif isinstance(obj, list):
                    for i, v in enumerate(obj):
                        flat.update(flatten(v, f"{prefix}{i}."))
                else:
                    flat[prefix[:-1]] = obj
                return flat
            return {"flattened": flatten(data), "success": True}
        else:
            return {"error": f"Unknown operation: {operation}", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}

@mcp.tool()
def xml_operations(operation: str, xml_data: Optional[str] = None, 
                  file_path: Optional[str] = None, xpath: Optional[str] = None) -> Dict[str, Any]:
    """XML operations: parse, validate, query, to_json"""
    try:
        if operation == "parse":
            if file_path:
                tree = ET.parse(file_path)
                root = tree.getroot()
            else:
                root = ET.fromstring(xml_data)
            return {"tag": root.tag, "attrib": root.attrib, "success": True}
        elif operation == "validate":
            try:
                ET.fromstring(xml_data) if xml_data else ET.parse(file_path)
                return {"valid": True, "success": True}
            except:
                return {"valid": False, "success": True}
        elif operation == "query" and xpath:
            root = ET.fromstring(xml_data) if xml_data else ET.parse(file_path).getroot()
            elements = root.findall(xpath)
            return {
                "results": [{"tag": e.tag, "text": e.text, "attrib": e.attrib} for e in elements],
                "count": len(elements),
                "success": True
            }
        elif operation == "to_json":
            def xml_to_dict(element):
                result = {"tag": element.tag}
                if element.attrib:
                    result["attributes"] = element.attrib
                if element.text and element.text.strip():
                    result["text"] = element.text.strip()
                children = list(element)
                if children:
                    result["children"] = [xml_to_dict(child) for child in children]
                return result
            
            root = ET.fromstring(xml_data) if xml_data else ET.parse(file_path).getroot()
            return {"json": xml_to_dict(root), "success": True}
        else:
            return {"error": f"Unknown operation: {operation}", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}

# Text Processing
@mcp.tool()
def text_analysis(text: str) -> Dict[str, Any]:
    """Comprehensive text analysis"""
    words = text.split()
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]
    paragraphs = text.split('\n\n')
    
    # Character frequency
    char_freq = Counter(text.lower())
    
    # Word frequency
    word_freq = Counter(words)
    
    # Average word length
    avg_word_length = sum(len(word) for word in words) / len(words) if words else 0
    
    # Readability score (simple)
    avg_sentence_length = len(words) / len(sentences) if sentences else 0
    
    return {
        "statistics": {
            "characters": len(text),
            "characters_no_spaces": len(text.replace(" ", "")),
            "words": len(words),
            "sentences": len(sentences),
            "paragraphs": len(paragraphs),
            "avg_word_length": round(avg_word_length, 2),
            "avg_sentence_length": round(avg_sentence_length, 2)
        },
        "most_common_words": word_freq.most_common(10),
        "most_common_chars": char_freq.most_common(10),
        "language_features": {
            "questions": len(re.findall(r'\?', text)),
            "exclamations": len(re.findall(r'!', text)),
            "quotes": len(re.findall(r'"[^"]*"', text)),
            "numbers": len(re.findall(r'\b\d+\b', text)),
            "urls": len(re.findall(r'https?://\S+', text)),
            "emails": len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text))
        }
    }

@mcp.tool()
def text_generation(type: str, **kwargs) -> str:
    """Generate various types of text"""
    if type == "lorem_ipsum":
        words = kwargs.get("words", 100)
        lorem = "Lorem ipsum dolor sit amet consectetur adipiscing elit sed do eiusmod tempor incididunt ut labore et dolore magna aliqua"
        lorem_words = lorem.split()
        result = []
        for i in range(words):
            result.append(lorem_words[i % len(lorem_words)])
        return " ".join(result)
    
    elif type == "uuid":
        format = kwargs.get("format", "default")
        if format == "hex":
            return uuid.uuid4().hex
        elif format == "int":
            return str(uuid.uuid4().int)
        else:
            return str(uuid.uuid4())
    
    elif type == "random_name":
        first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona", "George", "Helen"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
        return f"{random.choice(first_names)} {random.choice(last_names)}"
    
    elif type == "random_email":
        domains = ["gmail.com", "yahoo.com", "outlook.com", "example.com", "mail.com"]
        username = "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=8))
        return f"{username}@{random.choice(domains)}"
    
    elif type == "random_phone":
        country_code = kwargs.get("country_code", "+1")
        return f"{country_code} ({random.randint(100, 999)}) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
    
    else:
        return f"Unknown text type: {type}"

@mcp.tool()
def regex_operations(operation: str, pattern: str, text: str, replacement: Optional[str] = None, 
                    flags: int = 0) -> Dict[str, Any]:
    """Regex operations: match, search, findall, replace, split"""
    try:
        if operation == "match":
            match = re.match(pattern, text, flags)
            return {
                "matched": bool(match),
                "match": match.group() if match else None,
                "groups": match.groups() if match else None,
                "success": True
            }
        elif operation == "search":
            match = re.search(pattern, text, flags)
            return {
                "found": bool(match),
                "match": match.group() if match else None,
                "start": match.start() if match else None,
                "end": match.end() if match else None,
                "groups": match.groups() if match else None,
                "success": True
            }
        elif operation == "findall":
            matches = re.findall(pattern, text, flags)
            return {"matches": matches, "count": len(matches), "success": True}
        elif operation == "replace":
            result = re.sub(pattern, replacement or "", text, flags=flags)
            return {"result": result, "success": True}
        elif operation == "split":
            parts = re.split(pattern, text, flags=flags)
            return {"parts": parts, "count": len(parts), "success": True}
        else:
            return {"error": f"Unknown operation: {operation}", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}

# Math and Statistics
@mcp.tool()
def advanced_math(operation: str, values: List[float], **kwargs) -> Dict[str, Any]:
    """Advanced mathematical operations"""
    try:
        if operation == "statistics":
            return {
                "mean": statistics.mean(values),
                "median": statistics.median(values),
                "mode": statistics.mode(values) if len(set(values)) < len(values) else None,
                "stdev": statistics.stdev(values) if len(values) > 1 else 0,
                "variance": statistics.variance(values) if len(values) > 1 else 0,
                "min": min(values),
                "max": max(values),
                "sum": sum(values),
                "count": len(values)
            }
        
        elif operation == "percentiles":
            sorted_values = sorted(values)
            n = len(sorted_values)
            return {
                "p25": sorted_values[int(n * 0.25)],
                "p50": sorted_values[int(n * 0.50)],
                "p75": sorted_values[int(n * 0.75)],
                "p90": sorted_values[int(n * 0.90)],
                "p95": sorted_values[int(n * 0.95)],
                "p99": sorted_values[int(n * 0.99)] if n > 100 else None
            }
        
        elif operation == "linear_regression":
            if "x_values" not in kwargs:
                return {"error": "x_values required for linear regression", "success": False}
            x_values = kwargs["x_values"]
            n = len(values)
            x_mean = sum(x_values) / n
            y_mean = sum(values) / n
            
            numerator = sum((x_values[i] - x_mean) * (values[i] - y_mean) for i in range(n))
            denominator = sum((x_values[i] - x_mean) ** 2 for i in range(n))
            
            slope = numerator / denominator if denominator != 0 else 0
            intercept = y_mean - slope * x_mean
            
            # R-squared
            y_pred = [slope * x + intercept for x in x_values]
            ss_res = sum((values[i] - y_pred[i]) ** 2 for i in range(n))
            ss_tot = sum((values[i] - y_mean) ** 2 for i in range(n))
            r_squared = 1 - (ss_res / ss_tot) if ss_tot != 0 else 0
            
            return {
                "slope": slope,
                "intercept": intercept,
                "r_squared": r_squared,
                "equation": f"y = {slope:.4f}x + {intercept:.4f}"
            }
        
        elif operation == "matrix":
            # Simple matrix operations
            if "matrix_b" in kwargs:
                matrix_a = values
                matrix_b = kwargs["matrix_b"]
                if kwargs.get("op") == "multiply":
                    # Simplified matrix multiplication for 2x2
                    result = [
                        matrix_a[0] * matrix_b[0] + matrix_a[1] * matrix_b[2],
                        matrix_a[0] * matrix_b[1] + matrix_a[1] * matrix_b[3],
                        matrix_a[2] * matrix_b[0] + matrix_a[3] * matrix_b[2],
                        matrix_a[2] * matrix_b[1] + matrix_a[3] * matrix_b[3]
                    ]
                    return {"result": result}
            return {"error": "Matrix operation not fully specified", "success": False}
        
        else:
            return {"error": f"Unknown operation: {operation}", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}

# Encryption and Hashing
@mcp.tool()
def encryption_operations(operation: str, text: str, key: Optional[str] = None, 
                         algorithm: str = "caesar") -> Dict[str, Any]:
    """Simple encryption operations"""
    try:
        if operation == "encrypt":
            if algorithm == "caesar":
                shift = int(key or 3)
                result = ""
                for char in text:
                    if char.isalpha():
                        ascii_offset = 65 if char.isupper() else 97
                        result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
                    else:
                        result += char
                return {"encrypted": result, "algorithm": algorithm, "success": True}
            
            elif algorithm == "reverse":
                return {"encrypted": text[::-1], "algorithm": algorithm, "success": True}
            
            elif algorithm == "base64":
                return {"encrypted": base64.b64encode(text.encode()).decode(), "algorithm": algorithm, "success": True}
            
        elif operation == "decrypt":
            if algorithm == "caesar":
                shift = -int(key or 3)
                result = ""
                for char in text:
                    if char.isalpha():
                        ascii_offset = 65 if char.isupper() else 97
                        result += chr((ord(char) - ascii_offset + shift) % 26 + ascii_offset)
                    else:
                        result += char
                return {"decrypted": result, "algorithm": algorithm, "success": True}
            
            elif algorithm == "reverse":
                return {"decrypted": text[::-1], "algorithm": algorithm, "success": True}
            
            elif algorithm == "base64":
                return {"decrypted": base64.b64decode(text).decode(), "algorithm": algorithm, "success": True}
        
        elif operation == "hash":
            algorithms = {
                "md5": hashlib.md5,
                "sha1": hashlib.sha1,
                "sha256": hashlib.sha256,
                "sha512": hashlib.sha512,
                "sha3_256": hashlib.sha3_256,
                "sha3_512": hashlib.sha3_512
            }
            
            if algorithm in algorithms:
                hash_obj = algorithms[algorithm](text.encode())
                return {
                    "hash": hash_obj.hexdigest(),
                    "algorithm": algorithm,
                    "length": len(hash_obj.hexdigest()),
                    "success": True
                }
        
        return {"error": f"Unknown operation or algorithm", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}

# Date and Time
@mcp.tool()
def datetime_operations(operation: str, **kwargs) -> Dict[str, Any]:
    """Advanced datetime operations"""
    try:
        if operation == "now":
            now = datetime.now()
            return {
                "iso": now.isoformat(),
                "timestamp": now.timestamp(),
                "formatted": now.strftime("%Y-%m-%d %H:%M:%S"),
                "components": {
                    "year": now.year,
                    "month": now.month,
                    "day": now.day,
                    "hour": now.hour,
                    "minute": now.minute,
                    "second": now.second,
                    "weekday": now.strftime("%A"),
                    "week_number": now.isocalendar()[1]
                }
            }
        
        elif operation == "parse":
            date_str = kwargs.get("date_string", "")
            formats = [
                "%Y-%m-%d",
                "%Y/%m/%d",
                "%d-%m-%Y",
                "%d/%m/%Y",
                "%Y-%m-%d %H:%M:%S",
                "%d/%m/%Y %H:%M:%S",
                "%Y-%m-%dT%H:%M:%S",
                "%Y-%m-%dT%H:%M:%SZ"
            ]
            
            for fmt in formats:
                try:
                    dt = datetime.strptime(date_str, fmt)
                    return {
                        "parsed": dt.isoformat(),
                        "format_used": fmt,
                        "success": True
                    }
                except:
                    continue
            
            return {"error": "Could not parse date", "success": False}
        
        elif operation == "diff":
            date1 = datetime.fromisoformat(kwargs.get("date1", ""))
            date2 = datetime.fromisoformat(kwargs.get("date2", ""))
            diff = date2 - date1
            
            return {
                "days": diff.days,
                "seconds": diff.seconds,
                "total_seconds": diff.total_seconds(),
                "hours": diff.total_seconds() / 3600,
                "minutes": diff.total_seconds() / 60,
                "human_readable": str(diff)
            }
        
        elif operation == "add":
            base_date = datetime.fromisoformat(kwargs.get("date", datetime.now().isoformat()))
            delta_kwargs = {k: v for k, v in kwargs.items() if k in ["days", "hours", "minutes", "seconds", "weeks"]}
            new_date = base_date + timedelta(**delta_kwargs)
            
            return {
                "original": base_date.isoformat(),
                "new": new_date.isoformat(),
                "delta": str(timedelta(**delta_kwargs))
            }
        
        elif operation == "format":
            date = datetime.fromisoformat(kwargs.get("date", datetime.now().isoformat()))
            format_str = kwargs.get("format", "%Y-%m-%d %H:%M:%S")
            
            return {
                "formatted": date.strftime(format_str),
                "format_used": format_str
            }
        
        return {"error": f"Unknown operation: {operation}", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}

# Color Operations
@mcp.tool()
def color_operations(operation: str, color: str, **kwargs) -> Dict[str, Any]:
    """Color format conversions and operations"""
    try:
        if operation == "parse":
            # Parse hex color
            if color.startswith("#"):
                hex_color = color.lstrip("#")
                if len(hex_color) == 3:
                    hex_color = "".join([c*2 for c in hex_color])
                
                r = int(hex_color[0:2], 16)
                g = int(hex_color[2:4], 16)
                b = int(hex_color[4:6], 16)
                
                # Convert to HSL
                r_norm = r / 255.0
                g_norm = g / 255.0
                b_norm = b / 255.0
                
                max_val = max(r_norm, g_norm, b_norm)
                min_val = min(r_norm, g_norm, b_norm)
                l = (max_val + min_val) / 2
                
                if max_val == min_val:
                    h = s = 0
                else:
                    d = max_val - min_val
                    s = d / (2 - max_val - min_val) if l > 0.5 else d / (max_val + min_val)
                    
                    if max_val == r_norm:
                        h = ((g_norm - b_norm) / d + (6 if g_norm < b_norm else 0)) / 6
                    elif max_val == g_norm:
                        h = ((b_norm - r_norm) / d + 2) / 6
                    else:
                        h = ((r_norm - g_norm) / d + 4) / 6
                
                return {
                    "hex": f"#{r:02x}{g:02x}{b:02x}",
                    "rgb": f"rgb({r}, {g}, {b})",
                    "rgba": f"rgba({r}, {g}, {b}, 1.0)",
                    "hsl": f"hsl({int(h*360)}, {int(s*100)}%, {int(l*100)}%)",
                    "components": {
                        "r": r, "g": g, "b": b,
                        "h": int(h*360), "s": int(s*100), "l": int(l*100)
                    }
                }
        
        elif operation == "adjust":
            # Simple brightness adjustment
            factor = kwargs.get("brightness", 1.0)
            hex_color = color.lstrip("#")
            r = int(hex_color[0:2], 16)
            g = int(hex_color[2:4], 16)
            b = int(hex_color[4:6], 16)
            
            r = max(0, min(255, int(r * factor)))
            g = max(0, min(255, int(g * factor)))
            b = max(0, min(255, int(b * factor)))
            
            return {
                "original": color,
                "adjusted": f"#{r:02x}{g:02x}{b:02x}",
                "rgb": f"rgb({r}, {g}, {b})"
            }
        
        elif operation == "palette":
            # Generate color palette
            base_color = color.lstrip("#")
            r = int(base_color[0:2], 16)
            g = int(base_color[2:4], 16)
            b = int(base_color[4:6], 16)
            
            palette = {
                "base": f"#{r:02x}{g:02x}{b:02x}",
                "lighter": [],
                "darker": [],
                "complementary": f"#{(255-r):02x}{(255-g):02x}{(255-b):02x}"
            }
            
            # Generate lighter and darker shades
            for i in range(1, 4):
                factor_light = 1 + (i * 0.2)
                factor_dark = 1 - (i * 0.2)
                
                r_light = min(255, int(r * factor_light))
                g_light = min(255, int(g * factor_light))
                b_light = min(255, int(b * factor_light))
                palette["lighter"].append(f"#{r_light:02x}{g_light:02x}{b_light:02x}")
                
                r_dark = max(0, int(r * factor_dark))
                g_dark = max(0, int(g * factor_dark))
                b_dark = max(0, int(b * factor_dark))
                palette["darker"].append(f"#{r_dark:02x}{g_dark:02x}{b_dark:02x}")
            
            return palette
        
        return {"error": f"Unknown operation: {operation}", "success": False}
    except Exception as e:
        return {"error": str(e), "success": False}

# Image Operations (Basic)
@mcp.tool()
def image_info(file_path: str) -> Dict[str, Any]:
    """Get basic image information without PIL"""
    try:
        # Get file size
        file_size = os.path.getsize(file_path)
        
        # Detect format from file extension
        _, ext = os.path.splitext(file_path)
        format = ext.lstrip('.').upper()
        
        # Basic dimension detection for common formats
        dimensions = None
        
        if format in ['JPEG', 'JPG']:
            with open(file_path, 'rb') as f:
                # Skip to SOF marker
                f.seek(2)
                while True:
                    marker = f.read(2)
                    if not marker:
                        break
                    if marker[0] == 0xFF and marker[1] in [0xC0, 0xC2]:
                        f.read(3)  # Skip length and precision
                        height = int.from_bytes(f.read(2), 'big')
                        width = int.from_bytes(f.read(2), 'big')
                        dimensions = {"width": width, "height": height}
                        break
                    else:
                        length = int.from_bytes(f.read(2), 'big')
                        f.seek(length - 2, 1)
        
        elif format == 'PNG':
            with open(file_path, 'rb') as f:
                f.seek(16)  # Skip PNG signature and IHDR chunk type
                width = int.from_bytes(f.read(4), 'big')
                height = int.from_bytes(f.read(4), 'big')
                dimensions = {"width": width, "height": height}
        
        return {
            "file_path": file_path,
            "format": format,
            "file_size": file_size,
            "file_size_mb": round(file_size / (1024 * 1024), 2),
            "dimensions": dimensions,
            "success": True
        }
    except Exception as e:
        return {"error": str(e), "success": False}

# Random Generators
@mcp.tool()
def random_data(type: str, **kwargs) -> Any:
    """Generate random data of various types"""
    if type == "password":
        length = kwargs.get("length", 16)
        chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
        if kwargs.get("symbols", True):
            chars += "!@#$%^&*()_+-=[]{}|;:,.<>?"
        return ''.join(random.choice(chars) for _ in range(length))
    
    elif type == "words":
        count = kwargs.get("count", 5)
        words = ["apple", "banana", "cherry", "dog", "elephant", "flower", "guitar", 
                "house", "island", "jungle", "kite", "lemon", "mountain", "notebook",
                "ocean", "piano", "quantum", "rainbow", "sunset", "telescope", 
                "umbrella", "volcano", "waterfall", "xylophone", "yellow", "zebra"]
        return random.sample(words, min(count, len(words)))
    
    elif type == "sentence":
        templates = [
            "The {adjective} {noun} {verb} {adverb}.",
            "A {adjective} {noun} {verb} the {adjective} {noun}.",
            "{noun} {verb} {adverb} in the {adjective} {noun}."
        ]
        
        adjectives = ["quick", "lazy", "beautiful", "ancient", "modern", "tiny", "huge"]
        nouns = ["fox", "dog", "castle", "computer", "book", "ocean", "mountain"]
        verbs = ["runs", "jumps", "sleeps", "writes", "sings", "dances", "flies"]
        adverbs = ["quickly", "slowly", "gracefully", "carefully", "happily"]
        
        template = random.choice(templates)
        return template.format(
            adjective=random.choice(adjectives),
            noun=random.choice(nouns),
            verb=random.choice(verbs),
            adverb=random.choice(adverbs)
        )
    
    elif type == "color":
        return {
            "hex": f"#{random.randint(0, 0xFFFFFF):06x}",
            "rgb": f"rgb({random.randint(0,255)}, {random.randint(0,255)}, {random.randint(0,255)})"
        }
    
    elif type == "coordinates":
        return {
            "latitude": round(random.uniform(-90, 90), 6),
            "longitude": round(random.uniform(-180, 180), 6)
        }
    
    elif type == "ip":
        return f"{random.randint(1,255)}.{random.randint(0,255)}.{random.randint(0,255)}.{random.randint(1,255)}"
    
    elif type == "mac":
        return ":".join([f"{random.randint(0, 255):02x}" for _ in range(6)])
    
    elif type == "user":
        first_names = ["John", "Jane", "Alice", "Bob", "Charlie", "Diana", "Edward", "Fiona"]
        last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller"]
        domains = ["gmail.com", "yahoo.com", "outlook.com", "company.com"]
        
        first = random.choice(first_names)
        last = random.choice(last_names)
        
        return {
            "first_name": first,
            "last_name": last,
            "full_name": f"{first} {last}",
            "email": f"{first.lower()}.{last.lower()}@{random.choice(domains)}",
            "username": f"{first.lower()}{random.randint(100, 999)}",
            "age": random.randint(18, 80),
            "phone": f"+1 ({random.randint(100,999)}) {random.randint(100,999)}-{random.randint(1000,9999)}"
        }
    
    return {"error": f"Unknown type: {type}"}

# Utility Functions
@mcp.tool()
def batch_operations(operations: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Execute multiple operations in batch"""
    results = []
    
    for op in operations:
        tool_name = op.get("tool")
        params = op.get("params", {})
        
        try:
            # Map tool names to functions
            tool_map = {
                "file_operations": file_operations,
                "directory_operations": directory_operations,
                "text_analysis": text_analysis,
                "random_data": random_data,
                # Add more mappings as needed
            }
            
            if tool_name in tool_map:
                result = tool_map[tool_name](**params)
                results.append({"tool": tool_name, "result": result, "success": True})
            else:
                results.append({"tool": tool_name, "error": "Unknown tool", "success": False})
        except Exception as e:
            results.append({"tool": tool_name, "error": str(e), "success": False})
    
    return results

@mcp.tool()
def data_converter(input_data: str, from_format: str, to_format: str) -> Dict[str, Any]:
    """Convert data between different formats"""
    try:
        # Parse input
        if from_format == "json":
            data = json.loads(input_data)
        elif from_format == "csv":
            reader = csv.DictReader(input_data.splitlines())
            data = list(reader)
        elif from_format == "yaml":
            # Simple YAML parsing
            data = {}
            for line in input_data.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    data[key.strip()] = value.strip()
        else:
            return {"error": f"Unsupported input format: {from_format}", "success": False}
        
        # Convert to output format
        if to_format == "json":
            output = json.dumps(data, indent=2)
        elif to_format == "csv":
            if isinstance(data, list) and all(isinstance(item, dict) for item in data):
                output = io.StringIO()
                writer = csv.DictWriter(output, fieldnames=data[0].keys())
                writer.writeheader()
                writer.writerows(data)
                output = output.getvalue()
            else:
                return {"error": "Data must be a list of dictionaries for CSV conversion", "success": False}
        elif to_format == "yaml":
            # Simple YAML generation
            output = ""
            if isinstance(data, dict):
                for key, value in data.items():
                    output += f"{key}: {value}\n"
            else:
                return {"error": "Data must be a dictionary for YAML conversion", "success": False}
        else:
            return {"error": f"Unsupported output format: {to_format}", "success": False}
        
        return {"output": output, "success": True}
    except Exception as e:
        return {"error": str(e), "success": False}

# Resources
@mcp.resource("system://info")
def get_system_info() -> str:
    """Get comprehensive system information"""
    info = system_info()
    return json.dumps(info, indent=2)

@mcp.resource("tools://list")
def list_tools() -> str:
    """List all available tools"""
    tools = []
    for name, func in globals().items():
        if hasattr(func, '__annotations__') and name.startswith(('mcp.tool', 'mcp.resource')):
            tools.append({
                "name": name,
                "description": func.__doc__.strip() if func.__doc__ else "No description",
                "type": "tool" if name.startswith('mcp.tool') else "resource"
            })
    return json.dumps({"tools": tools, "count": len(tools)}, indent=2)

@mcp.resource("help://tool/{tool_name}")
def get_tool_help(tool_name: str) -> str:
    """Get detailed help for a specific tool"""
    if tool_name in globals():
        func = globals()[tool_name]
        if hasattr(func, '__annotations__'):
            help_info = {
                "name": tool_name,
                "description": func.__doc__.strip() if func.__doc__ else "No description",
                "parameters": str(func.__annotations__),
                "examples": []  # Could be extended with examples
            }
            return json.dumps(help_info, indent=2)
    return json.dumps({"error": f"Tool '{tool_name}' not found"})

# Prompts
@mcp.prompt("analyze_data")
def analyze_data_prompt(data_type: str = "general", specific_questions: Optional[List[str]] = None) -> str:
    """Generate data analysis prompt"""
    base_prompt = f"Please analyze the following {data_type} data comprehensively.\n\n"
    
    base_prompt += "Focus on:\n"
    base_prompt += "- Key patterns and trends\n"
    base_prompt += "- Statistical summary\n"
    base_prompt += "- Anomalies or outliers\n"
    base_prompt += "- Correlations between variables\n"
    base_prompt += "- Actionable insights\n"
    
    if specific_questions:
        base_prompt += "\nAlso answer these specific questions:\n"
        for i, q in enumerate(specific_questions, 1):
            base_prompt += f"{i}. {q}\n"
    
    return base_prompt

@mcp.prompt("code_generator")
def code_generator_prompt(task: str, language: str = "python", constraints: Optional[List[str]] = None) -> str:
    """Generate code generation prompt"""
    prompt = f"Please write {language} code to {task}.\n\n"
    prompt += "Requirements:\n"
    prompt += "- Clean, readable code with appropriate comments\n"
    prompt += "- Error handling and edge cases\n"
    prompt += "- Efficient implementation\n"
    prompt += "- Follow best practices and conventions\n"
    
    if constraints:
        prompt += "\nConstraints:\n"
        for constraint in constraints:
            prompt += f"- {constraint}\n"
    
    prompt += "\nInclude example usage and expected output."
    return prompt

@mcp.prompt("troubleshoot")
def troubleshoot_prompt(issue: str, context: Optional[str] = None, attempted_solutions: Optional[List[str]] = None) -> str:
    """Generate troubleshooting prompt"""
    prompt = f"Help me troubleshoot this issue: {issue}\n\n"
    
    if context:
        prompt += f"Context:\n{context}\n\n"
    
    if attempted_solutions:
        prompt += "Solutions already attempted:\n"
        for solution in attempted_solutions:
            prompt += f"- {solution}\n"
        prompt += "\n"
    
    prompt += "Please provide:\n"
    prompt += "1. Possible root causes\n"
    prompt += "2. Diagnostic steps to identify the issue\n"
    prompt += "3. Step-by-step solutions\n"
    prompt += "4. Preventive measures for the future"
    
    return prompt

if __name__ == "__main__":
    mcp.run(transport='stdio')
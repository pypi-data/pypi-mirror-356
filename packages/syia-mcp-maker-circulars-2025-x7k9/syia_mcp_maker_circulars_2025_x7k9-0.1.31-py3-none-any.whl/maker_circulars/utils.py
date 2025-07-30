from pathlib import Path
from datetime import datetime

def timestamped_filename(prefix: str, ext: str = ".png") -> Path:
    """
    Returns Path("<cwd>/screenshots/{prefix}_{UTC_ISO}.png"),
    creating the directory if needed.
    """
    base = Path.cwd() / "screenshots"
    base.mkdir(exist_ok=True)
    ts = datetime.utcnow().strftime("%Y%m%dT%H%M%SZ")
    return base / f"{prefix}_{ts}{ext}"


def timestamped_filename_pdf(prefix: str, ext: str = ".pdf") -> Path:
    """
    Returns Path("<cwd>/downloads/{prefix}_{UTC_ISO}.pdf"),
    creating the directory if needed.
    """
    base = Path.cwd() / "downloads"
    base.mkdir(exist_ok=True)
    return base / f"{prefix}{ext}"
import re
import arabic_reshaper
from pathlib import Path
from flask import current_app
from bidi.algorithm import get_display

class FileUtil:       
    
    MAX_FILE_SIZE = 4 * 1024 * 1024
    
    ALLOWED_EXTENSIONS = [
        'jpg', 'png','jpeg', 'gif', 'webp', 'svg',
        'pdf', 'doc', 'docx', 'txt',
        'xls', 'xlsx', 'csv',
        'py', 'js', 'html', 'css', 'java', 'json',
    ] 
    ALLOWED_MIMES = {
        'image/png', 'image/jpeg', 'image/gif', 'image/webp',
        'application/pdf', 'application/msword', 'text/plain',
        'text/csv', 'text/x-python', 'application/javascript',
        'text/html', 'text/css', 'application/json'
}
    
    @staticmethod  
    def allowed_file(filename):
        if '.' not in filename:
            return False
        ext = filename.rsplit('.', 1)[-1].lower()
        return ext in FileUtil.ALLOWED_EXTENSIONS
    
    @staticmethod
    def allowed_mime(mime: str):
        return mime in FileUtil.ALLOWED_MIMES
    
    @staticmethod
    def is_arabic(s: str):
        return bool(re.search(
            r'[\u0600-\u06FF'
            r'\u0750-\u077F'
            r'\u08A0-\u08FF'
            r'\uFB50-\uFDFF'
            r'\uFE70-\uFEFF]', 
            s
        ))

    
    @staticmethod
    def base_path() -> Path:
        return Path(current_app.config['UPLOAD_FOLDER']).resolve()

    @staticmethod
    def get_path(file_path: str) -> Path | None:
        try:
            base = FileUtil.base_path()
            path = Path(file_path).resolve()
            path.relative_to(base)
            return path
        except Exception:
            return None
        
    @staticmethod
    def reshape_arabic(s: str) -> str:
        """arabic text and applies BiDi algorithm"""
        if arabic_reshaper is None:
            return s
        return get_display(arabic_reshaper.reshape(s))

    @staticmethod
    def count_leading_spaces(line: str) -> int:
        """Counts spaces, counting a tab 4 spaces"""
        count = 0
        for ch in line:
            if ch == " ":
                count += 1
            elif ch == "\t":
                count += 4
            else:
                break
        return count
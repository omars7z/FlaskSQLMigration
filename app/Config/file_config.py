import os 
from pathlib import Path

class FileConfig:
    
    MAX_FILE_SIZE = 2 * 1024 * 1024
    
    ALLOWED_EXTENSIONS = [
        'jgp', 'png','jpeg', 'gif', 'webp', 'svg',
        'pdf', 'doc', 'docx', 'txt',
        'xls', 'xlsx', 'csv',
        'py', 'js', 'html', 'css', 'java', 'json',
    ] 
    ALLOWED_MIMES = {
        'image/png', 'image/jpeg', 'image/gif', 'image/webp',
        'application/pdf', 'application/msword', 'text/plain'
        'text/csv', 'text/x-python', 'application/javascript', 
        'text/html', 'text/css', 'application/json'
    }
    
    @staticmethod  #not meant to be instantiated
    def allowed_file(filename):
        if '.' in filename:
            return False
        ext = filename.rsplit('.', 1)[1].lower()
        return ext in FileConfig.ALLOWED_EXTENSIONS
    
    @staticmethod
    def allowed_mime():
        pass
    
    @staticmethod
    def _generate_name(file):
        if '.' in file.filename:
            pass
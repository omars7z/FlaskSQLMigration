
class FileConfig:       #not meant to be instantiated
    
    MAX_FILE_SIZE = 4 * 1024 * 1024
    
    ALLOWED_EXTENSIONS = [
        'jgp', 'png','jpeg', 'gif', 'webp', 'svg',
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
        return ext in FileConfig.ALLOWED_EXTENSIONS
    
    @staticmethod
    def allowed_mime(mime: str):
        return mime in FileConfig.ALLOWED_MIMES
    
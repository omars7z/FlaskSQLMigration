
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from app.Helpers.registry import register
from app.Util.file_config import FileConfig
from flask import current_app
import os, mimetypes
import uuid

@register("File", repo="File")
class FileService:
    
    def __init__(self, repository):
        self.repo = repository.get("File")
        self.config = FileConfig
        
    def get_by_id(self, id: int):
        return self.repo.get_by_id(id)
    
    def get(self, filters):
        return self.repo.get(filters)
    
    def allowed_file(self, filename):
        ext =  '.' in filename and \
            filename.rsplit('.', 1)[1].lower() in self.config.ALLOWED_EXTENSIONS
        return ext
    
    def upload_file(
        self, 
        file: FileStorage, 
        uploader_id: int,
    ):
        file_name = file.filename
        if not file or file_name == '':
            raise ValueError("No file provided")
        
        file.stream.seek(0, os.SEEK_END)
        size = file.stream.tell()
        file.stream.seek(0)
        if size > self.config.MAX_FILE_SIZE:
            raise ValueError("Exceeded file size limit")
        
        mime = file.content_type or mimetypes.guess_type(file_name)[0] or "application/octet-stream"
        if mime not in self.config.ALLOWED_MIMES:
            raise ValueError("File mime type not allowed ") 
        
        ext = file_name.rsplit('.', 1)[1].lower() 
        if ext not in self.config.ALLOWED_EXTENSIONS:
                raise ValueError("File extension type not allowed ")
            
        file_id = uuid.uuid4()    
        filename = secure_filename(file_name)
        file_path = current_app.config['UPLOAD_FOLDER']
        
        file.save(os.path.join(file_path, filename))
        
        file_data = {
            "id" : file_id,
            "filename": filename,
            "mime_type": mime,
            "file_path": file_path,
            "file_size": os.path.getsize(file_path),
            "uploader_id": uploader_id,
        }
            
        return self.repo.create(file_data)
      
    
    
    def update(self, id: int, data: dict):
        return self.repo.update(id, data)
    
    def delete(self, id):
        file_record = self.get_by_id(id)
        if not file_record:
            raise ValueError("File not found")
        
        uploaded_file = current_app.get['UPLOAD_FOLDER']
        file_path = os.path.join(uploaded_file, file_record.filename)
        return self.repo.delete(id)
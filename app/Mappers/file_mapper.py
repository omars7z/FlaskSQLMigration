class FileMapper:
    @staticmethod
    def to_dict(file):
        if not file:
            return None
        
        return {
            "id": str(file.id),
            "filename": file.filename,
            "mime_type": file.mime_type,
            "file_path" : file.file_path,
            "file_size": file.file_size,
            "time_created": file.time_created.isoformat() if file.time_created else None,
            "uploader": {
                "id": file.uploader.id ,
                "name": file.uploader.name ,
            } if file.uploader else None
        }

    @staticmethod
    def to_list(files):
        return [FileMapper.to_dict(f) for f in files] if files else []

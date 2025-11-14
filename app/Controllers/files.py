from flask_restful import Resource
from flask import current_app, request, g

from sqlalchemy.exc import SQLAlchemyError
from app.Models.file import File
from app.Mappers.file_mapper import FileMapper

from app.Decorators.filter_methods import auto_filter_method
from app.Util.response import suc_res, error_res
from app.Decorators.authentication import authenticate
from app.Decorators.super_admin import superadmin_required

class FileResource(Resource):
    
    @property
    def service(self):
        return current_app.file_service

    # @authenticate
    @auto_filter_method(File)
    def get(self, file_id=None, filters=None):        
        
        if file_id is not None:
            file = self.service.get_by_id(file_id)
            if not file:
                return error_res("File not found", 404)
            return suc_res(FileMapper.to_dict(file), 200)
        
        files = self.service.get(filters)
        if not files:
            return error_res([], 200)
        return suc_res(FileMapper.to_list(files), 200)
    
    @authenticate 
    def post(self):
        try:
            
            file = request.files['file']
            file_record = self.service.upload_file(
                file = file,
                uploader_id= g.current_user.id,
            )
            return suc_res({"msg":"File uploaded", "file":FileMapper.to_dict(file_record)}, 201)
        except ValueError as e:
            return error_res(str(e), 404)
    

    @authenticate
    def put(self, file_id:str):
        data = request.get_json()
        try:
            dt = self.service.update(file_id, data) 
        except ValueError as e:
            return error_res(str(e), 500)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(FileMapper.to_dict(dt), 200)
    
    
    # @authenticate
    def delete(self, file_id : str):
        try:                
            self.service.delete(file_id)
        except ValueError as e:
            return error_res(str(e), 403)
        except SQLAlchemyError as e:
            return error_res("Database error: " + str(e), 500)
        return suc_res(f"Deleted file id: {file_id}", 200)
    
def register_routes(api):
    api.add_resource(FileResource, '/file', '/file/<string:file_id>')
    
    
class FileDownloadResource(Resource):
    @property
    def service(self):
        return current_app.file_service
    
    @authenticate
    def get(self, id: int):
        current_user = g.current_user
        
        file = self.service.get_by_id(id)
        file_path = self.service.get_file_path(id)
        if not file or not file_path:
            return error_res("File not found on server", 404)
        
        try:
            '''return send_file(
                file_path,
                mimetype=file.mime_type,
                as_attachment=True,
                download_name=file.original_filename
            )'''
            pass
        except Exception as e:
            return error_res(f"Error downloading file: {str(e)}", 500)

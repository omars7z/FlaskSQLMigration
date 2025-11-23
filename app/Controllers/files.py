from flask_restful import Resource
from flask import request, current_app, g
from flasgger import swag_from

from sqlalchemy.exc import SQLAlchemyError
from app.Models.file import File
from app.Mappers.file_mapper import FileMapper

from app.Decorators.authentication import authenticate
from app.Decorators.filter_methods import auto_filter_method
from app.Util.response import suc_res, error_res

from app.Controllers.docs.files import FILE_LIST, FILE_UPLOAD,FILE_ITEM,FILE_DELETE, DOWNLOAD, TEXT

class FileResource(Resource):

    @property
    def service(self):
        return current_app.file_service

    @authenticate
    @auto_filter_method(File)
    @swag_from(FILE_LIST)
    def get(self, filters=None):
        try:
            files = self.service.get(filters)
            return suc_res(FileMapper.to_list(files or []), 200)
        except SQLAlchemyError as e:
            return error_res("Database error", 500)

    @authenticate
    @swag_from(FILE_UPLOAD)
    def post(self):
        try:
            file = request.files.get("file")
            if not file:
                return error_res("No file uploaded", 400)

            uploaded = self.service.upload_file(file, g.current_user_id)
            return suc_res(FileMapper.to_dict(uploaded), 201)

        except ValueError as e:
            return error_res(str(e), 400)
        except SQLAlchemyError as e:
            return error_res("Database error", 500)


class FileIDResource(Resource):

    @property
    def service(self):
        return current_app.file_service

    @authenticate
    @swag_from(FILE_ITEM)
    def get(self, file_id: str):
        try:
            file = self.service.get_by_id(file_id)
            if not file:
                return error_res(f"File {file_id} not found", 404)
            return suc_res(FileMapper.to_dict(file), 200)
        except ValueError as e:
            return error_res(str(e), 404)
        except SQLAlchemyError as e:
            return error_res("Database error", 500)
        except Exception as e:
            return error_res(f"Error getting file: {str(e)}", 500)

    @authenticate
    @swag_from(FILE_DELETE)
    def delete(self, file_id: str):
        try:
            self.service.delete(file_id)
            return suc_res(f"Deleted file id: {file_id}", 200)
        except ValueError as e:
            return error_res(str(e), 404)
        except SQLAlchemyError as e:
            return error_res("Database error", 500)


class FileDownloadResource(Resource):
    @property
    def service(self):
        return current_app.file_service

    @swag_from(DOWNLOAD)
    def get(self, file_id: str):
        try:
            return self.service.download_file(file_id)
        except ValueError as e:
            return error_res(str(e), 404)
        except Exception as e:
            return error_res(f"Error downloading file: {str(e)}", 500)


class TextToFile(Resource):
    @property
    def service(self):
        return current_app.file_service

    @authenticate
    @swag_from(TEXT)
    def post(self):
        try:
            data = request.get_json() 
            text = data.get("text")
            if not text:
                return error_res("No text found", 400)

            uploaded = self.service.upload_text(text, g.current_user_id)
            return suc_res(FileMapper.to_dict(uploaded), 201)

        except ValueError as e:
            return error_res(str(e), 404)
        except Exception as e:
            return error_res(str(e), 500)


def register_file_routes(api):
    api.add_resource(FileResource, "/file")
    api.add_resource(FileIDResource, "/file/<string:file_id>")
    api.add_resource(FileDownloadResource, "/download_file/<string:file_id>")
    api.add_resource(TextToFile, "/text-file")

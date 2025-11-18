from io import BytesIO

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound
from app.Helpers.registry import register
from app.Config.file_config import FileConfig
from flask import current_app, send_file

from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm

import os, mimetypes, uuid
from pathlib import Path
import re

@register("File", repo="File")
class FileService:
    
    def __init__(self, repository):
        self.repo = repository.get("File")
        
    def get_by_id(self, id: str):
        return self.repo.get_by_id(id)
    
    def get(self, filters=None):
        return self.repo.get(filters)
    
    def upload_file(self, file: FileStorage, uploader_id: int):
        if not file or file.filename == '':
            raise ValueError("No file provided")
        
        file.stream.seek(0, os.SEEK_END)
        size = file.stream.tell()
        file.stream.seek(0)
        if size > FileConfig.MAX_FILE_SIZE:
            raise ValueError("Exceeded file size limit")
        
        mime = file.content_type or mimetypes.guess_type(file.filename)[0] or "application/octet-stream"
        if not FileConfig.allowed_mime(mime):
            raise ValueError("File mime type not allowed")
        
        if not FileConfig.allowed_file(file.filename):
            raise ValueError("File extension type not allowed")
        
        filename = secure_filename(file.filename)
        
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)  # ensure folder exists
        full_path = os.path.join(upload_folder, filename)
        file.save(full_path)
        
        file_data = {
            "id": str(uuid.uuid4()),
            "filename": filename,
            "mime_type": mime,
            "file_path": full_path,          # store full path
            "file_size": os.path.getsize(full_path),
            "uploader_id": uploader_id
        }
        
        return self.repo.create(file_data)
    
    def base_path(self):
        return Path(current_app.config['UPLOAD_FOLDER']).resolve()

    def get_path(self, file_path: str):
        try:
            base = self.base_path()
            path = Path(file_path).resolve()
            path.relative_to(base)  # security check
            return path
        except Exception:
            return None

    def download_file(self, file_id: str):
        file_record = self.get_by_id(file_id)
        if not file_record:
            raise NotFound("File not found")

        path = self.get_path(file_record.file_path)
        if path is None or not path.exists():
            raise NotFound("File not found on server")

        return send_file(
            path,
            as_attachment=True,
            download_name=file_record.filename,
            mimetype=file_record.mime_type
        )

    
    def delete(self, file_id: str):
        file_record = self.get_by_id(file_id)
        if not file_record:
            raise ValueError("File not found")
        
        # Delete from disk and db
        file_path = getattr(file_record, "file_path", None)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
        
        return self.repo.delete(file_record)

    def upload_text(self, text: str):
        pdf_buffer = BytesIO()

        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=A4,
            leftMargin=20*mm,
            rightMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=20*mm
        )

        styles = getSampleStyleSheet()
        style = styles["Normal"]

        txt = []

        # Split into paragraphs by double newlines
        paragraphs = text.strip().split("\n")

        for para in paragraphs:
            # Let reportlab auto wrap words normally
            txt.append(Paragraph(para, style))
            txt.append(Spacer(1, 12))

        doc.build(txt)
        pdf_buffer.seek(0)

        return send_file(
            pdf_buffer,
            as_attachment=True,
            download_name="content.pdf",
            mimetype="application/pdf"
        )

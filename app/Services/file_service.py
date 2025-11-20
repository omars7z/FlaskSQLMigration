import os, uuid, re
import mimetypes
from pathlib import Path

from flask import current_app, send_file
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename
from werkzeug.exceptions import NotFound

from app.Helpers.registry import register
from app.Util.file import FileUtil
from fpdf import FPDF


@register("File", repo="File")
class FileService:
    def __init__(self, repository):
        self.repo = repository.get("File")

    def get_by_id(self, file_id: str):
        file = self.repo.get_by_id(file_id)
        if not file:
            return None
        return file

    def get(self, filters=None):
        return self.repo.get(filters)

    def delete(self, file_id: str):
        file_record = self.get_by_id(file_id)
        if not file_record:
            raise ValueError("File not found")

        file_path = getattr(file_record, "file_path", None)
        if file_path and os.path.exists(file_path):
            os.remove(file_path)

        return self.repo.delete(file_record)


    def download_file(self, file_id: str):
        file_record = self.get_by_id(file_id)
        if not file_record:
            raise NotFound("File not found")

        path = FileUtil.get_path(file_record.file_path)
        if path is None or not path.exists():
            raise NotFound("File not found on server")

        return send_file(
            path,
            as_attachment=True,
            download_name=file_record.filename,
            mimetype=file_record.mime_type
        )


    def upload_file(self, file: FileStorage, uploader_id: int):
        if not file or not file.filename:
            raise ValueError("No file provided")

        file.stream.seek(0, os.SEEK_END)
        size = file.stream.tell()
        file.stream.seek(0)
        if size > FileUtil.MAX_FILE_SIZE:
            raise ValueError("Exceeded file size limit")

        mime = file.content_type or mimetypes.guess_type(file.filename)[0] or "application/octet-stream"
        if not FileUtil.allowed_mime(mime):
            raise ValueError("File mime type not allowed")

        if not FileUtil.allowed_file(file.filename):
            raise ValueError("File extension not allowed")

        filename = secure_filename(file.filename)
        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)

        full_path = os.path.join(upload_folder, filename)
        file.save(full_path)

        file_data = {
            "id": str(uuid.uuid4()),
            "filename": filename,
            "mime_type": mime,
            "file_path": full_path,
            "file_size": os.path.getsize(full_path),
            "uploader_id": uploader_id
        }

        return self.repo.create(file_data)

    def upload_text(self, text, uploader_id: int):
        if not text:
            raise ValueError("No text provided")

        # if string, split to paragraphs, if list use, if not exception
        if isinstance(text, str):
            paragraphs = text.split("\n\n")
        elif isinstance(text, list):
            paragraphs = text
        else:
            raise ValueError("Input must be a string or a list of paragraphs")

        pdf = FPDF(format='A4', unit='mm')
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=20)

        arabic_font = os.path.join(current_app.root_path, "Fonts", "NotoNaskhArabic-Regular.ttf")
        if not os.path.exists(arabic_font):
            raise FileNotFoundError(f"Arabic font missing at: {arabic_font}")

        pdf.add_font("NotoArabic", "", arabic_font, uni=True)
        pdf.set_font("NotoArabic", size=12)

        page_width = pdf.w - 2 * pdf.l_margin
        left_margin = pdf.l_margin
        right_margin = pdf.r_margin

        for para in paragraphs:
            if not para.strip(): #if empty move down
                pdf.ln(6)
                continue

            lines = para.split("\n")
            for line in lines:
                if not line.strip():
                    pdf.ln(6)
                    continue

                indent = FileUtil.count_leading_spaces(line)
                content = line.lstrip()

                if FileUtil.is_arabic(content):
                    content = FileUtil.reshape_arabic(content)
                    pdf.set_left_margin(left_margin)
                    pdf.set_right_margin(right_margin + indent * 2)
                    pdf.multi_cell(page_width - indent * 2, 6, content, align='R')
                else:
                    pdf.set_left_margin(left_margin + indent * 2)
                    pdf.set_right_margin(right_margin)
                    pdf.multi_cell(page_width - indent * 2, 6, content, align='L')

            pdf.ln(4)

        upload_folder = current_app.config['UPLOAD_FOLDER']
        os.makedirs(upload_folder, exist_ok=True)
        id = str(uuid.uuid4())
        filename = f"{id}.pdf"
        full_path = os.path.join(upload_folder, filename)

        pdf.set_left_margin(left_margin)
        pdf.set_right_margin(right_margin)
        pdf.output(full_path)

        file_data = {
            "id": id,
            "filename": filename,
            "mime_type": "application/pdf",
            "file_path": full_path,
            "file_size": os.path.getsize(full_path),
            "uploader_id": uploader_id
        }

        return self.repo.create(file_data)

from io import BytesIO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status, permissions
from django.core.files.storage import FileSystemStorage
from PyPDF2 import PdfReader
from django.shortcuts import get_object_or_404
from users.serializers import UserSerializer,UserProfileSerializer
from content.models import CourseFile
from deep_translator import GoogleTranslator
from openai import OpenAI
import os
from django.conf import settings

client = OpenAI(api_key="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", base_url="https://openrouter.ai/api/v1")


def split_text(text, max_length=5000):
    chunks = []
    while len(text) > max_length:
        split_index = text.rfind(" ", 0, max_length)
        if split_index == -1:
            split_index = max_length
        chunks.append(text[:split_index])
        text = text[split_index:]
    chunks.append(text)
    return chunks


def extract_text_from_pdf(binary_data):
    """Extracts text from a PDF binary blob (BinaryField)."""
    text = ""
    try:
        pdf_reader = PdfReader(BytesIO(binary_data))
        for page in pdf_reader.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + "\n"
    except Exception as e:
        raise ValueError("Failed to extract PDF text: " + str(e))
    return text.strip()


class TranslatePDFView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        pdf_file = request.FILES.get('pdf')
        if not pdf_file:
            return Response({'status': 'error', 'message': 'PDF file is required'}, status=400)

        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        file_path = fs.path(filename)

        try:
            text = extract_text_from_pdf(file_path)
            if not text:
                return Response({'status': 'error', 'message': 'No extractable text found'}, status=400)

            chunks = split_text(text)
            translator = GoogleTranslator(source='auto', target='en')
            translated_chunks = [translator.translate(chunk) for chunk in chunks]
            translated_text = " ".join(translated_chunks)

            response = client.chat.completions.create(
                model="deepseek/deepseek-r1-zero:free",
                messages=[
                    {"role": "system", "content": "You are an AI that converts study material into structured learning tasks."},
                    {"role": "user", "content": f"Generate a structured study plan... {translated_text}"}
                    ],
                stream=False
            )

            return Response({
                'status': 'success',
                'user': UserProfileSerializer(user).data,
                'original_text': text,
                'translated_text': response.choices[0].message.content
            })
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=500)
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)


class GenerateMCQsFromPDFView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        pdf_file = request.FILES.get('pdf')
        if not pdf_file:
            return Response({'status': 'error', 'message': 'PDF file is required'}, status=400)

        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        file_path = fs.path(filename)

        try:
            text = extract_text_from_pdf(file_path)
            if not text:
                return Response({'status': 'error', 'message': 'No extractable text found'}, status=400)

            chunks = split_text(text)
            translator = GoogleTranslator(source='auto', target='en')
            translated_chunks = [translator.translate(chunk) for chunk in chunks]
            translated_text = " ".join(translated_chunks)

            response = client.chat.completions.create(
                model="deepseek/deepseek-r1-zero:free",
                messages=[
                    {"role": "system", "content": "You are an AI that generates multiple-choice questions (MCQs) from text."},
                    {"role": "user", "content": ("Generate exactly 10 MCQs in JSON format. Text: " + translated_text)}
                ],
                stream=False
            )

            return Response({'status': 'success', 'user': UserProfileSerializer(user).data, 'mcqs': response.choices[0].message.content})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=500)
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)


class GenerateFlashcardsFromPDFView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        pdf_file = request.FILES.get('pdf')
        if not pdf_file:
            return Response({'status': 'error', 'message': 'PDF file is required'}, status=400)

        fs = FileSystemStorage()
        filename = fs.save(pdf_file.name, pdf_file)
        file_path = fs.path(filename)

        try:
            text = extract_text_from_pdf(file_path)
            if not text:
                return Response({'status': 'error', 'message': 'No extractable text found'}, status=400)

            chunks = split_text(text)
            translator = GoogleTranslator(source='auto', target='en')
            translated_chunks = [translator.translate(chunk) for chunk in chunks]
            translated_text = " ".join(translated_chunks)

            response = client.chat.completions.create(
                model="deepseek/deepseek-r1-zero:free",
                messages=[
                    {"role": "system", "content": "You are an AI that generates flashcards from study content."},
                    {"role": "user", "content": (
                        "Generate exactly 10 flashcards as JSON. Text: " + translated_text)}
                ],
                stream=False
            )

            return Response({'status': 'success', 'user': UserProfileSerializer(user).data, 'flashcards': response.choices[0].message.content})
        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=500)
        finally:
            if os.path.exists(file_path):
                os.remove(file_path)

class GenerateFromCourseFileView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        file_id = request.data.get('file_id')
        course_file = get_object_or_404(CourseFile, id=file_id)
        if not file_id:
            return Response({'status': 'error', 'message': 'file_id is required'}, status=400)

        # Ensure this file belongs to the user through nested course -> semester -> user
        course = course_file.course
        user =  course.semester.user
        try:
            file_path = course_file.file
            text = extract_text_from_pdf(file_path)

            if not text.strip():
                return Response({'status': 'error', 'message': 'No extractable text found'}, status=400)

            # Translate in chunks
            chunks = split_text(text)
            translated_chunks = [GoogleTranslator(source='auto', target='en').translate(chunk) for chunk in chunks]
            translated_text = " ".join(translated_chunks)

            # Ask the LLM to generate structured study plan
            response = client.chat.completions.create(
                model="deepseek/deepseek-r1-zero:free",
                messages=[
                    {"role": "system", "content": "You are an AI that converts study material into structured learning tasks."},
                    {"role": "user", "content": f"Generate a structured study plan from this:\n\n{translated_text}"}
                ],
                stream=False
            )

            return Response({
                'status': 'success',
                'user': UserProfileSerializer(user).data,
                'course': course_file.course.code,
                'file': course_file.title,
                'translated_text': response.choices[0].message.content
            })

        except Exception as e:
            return Response({'status': 'error', 'message': str(e)}, status=500)

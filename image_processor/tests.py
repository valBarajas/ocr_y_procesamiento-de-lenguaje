import unittest
from unittest.mock import patch, MagicMock
from django.test import TestCase
from .views import process_image, get_ai_response
from google.cloud import vision
import os

class ImageProcessorTests(TestCase):

    @patch('google.cloud.vision.ImageAnnotatorClient')  # Simula el cliente de la API de Google Vision
    def test_text_extraction_from_image(self, MockImageAnnotatorClient):
        from google.cloud import vision
        
        mock_client = MagicMock()
        MockImageAnnotatorClient.return_value = mock_client

        # Simulamos un objeto TextAnnotation que contiene el texto "E = mc^2"
        mock_response = MagicMock()
        mock_text_annotation = MagicMock()
        mock_text_annotation.description = "E = mc^2"  # El texto que queremos simular
        mock_response.text_annotations = [mock_text_annotation]  # Colocamos el texto en una lista
        mock_client.text_detection.return_value = mock_response

        
        # Llamamos a la función que procesa la imagen
        request = MagicMock()
        request.FILES = {'image': open('image_processor/Captura.PNG', 'rb')}  # Asegúrate de tener la imagen en esa ubicación
        request.method = 'POST'
        
        # Aquí debería llamarse la función `process_image`, que procesa la imagen y devuelve el texto
        response = process_image(request)

        # Verificamos que el texto extraído es correcto
        self.assertIn('E=mc2', response.content.decode())  # Verificamos si la respuesta contiene el texto esperado

    @patch('groq.Groq')  # Simula el cliente de Groq
    def test_get_ai_response(self, MockGroq):
        # Simulamos la llamada a la API de Groq
        mock_client = MagicMock()
        MockGroq.return_value = mock_client

        mock_response = MagicMock()
        mock_response.choices = [MagicMock(message=MagicMock(content="Ecuación de Einstein."))]
        mock_client.chat.completions.create.return_value = mock_response

        # Llamamos a la función `get_ai_response`
        user_input = "E = mc^2"
        ai_response = get_ai_response(user_input)

        # Verificamos que la respuesta de la API de Groq es la esperada
        self.assertEqual(ai_response, "Ecuación de Einstein.")

if __name__ == '__main__':
    unittest.main()


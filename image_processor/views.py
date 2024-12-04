from groq import Groq
import io
from django.shortcuts import render, redirect
from google.cloud import vision
from .forms import ImageUploadForm
from django.core.files.storage import FileSystemStorage

def home(request):
    form = ImageUploadForm()
    return render(request, 'image_processor/home.html', {'form': form})

def process_image(request):
    global extracted_tex # vale
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            # Guarda la imagen temporalmente
            image = request.FILES['image']
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            filepath = fs.path(filename)

            try:
                # Procesa la imagen con Google Vision API
                client = vision.ImageAnnotatorClient()
                with io.open(filepath, 'rb') as image_file:
                    content = image_file.read()

                image = vision.Image(content=content)
                response = client.text_detection(image=image)
                texts = response.text_annotations

                # Extrae el texto detectado
                extracted_text = texts[0].description if texts else "No se detectó texto."
                
                
                
                
                
                
                
                extracted_text=get_ai_response(extracted_text)
                text_ejemplos =ejemplo(extracted_text)
                text_aplicaciones = aplicaciones(extracted_text)
                global messages
                messages = []
                

            except Exception as e:
                extracted_text = f"Error al procesar la imagen: {e}"

            finally:
                # Borra la imagen temporal
                fs.delete(filename)

            # Renderiza la plantilla con el texto extraído
            return render(request, 'image_processor/result.html', {'text': extracted_text,'text_ejemplos': text_ejemplos,'text_aplicaciones': text_aplicaciones})

    # Si no es POST o el formulario no es válido, vuelve a la página principal
    return redirect('home')


# Inicializa el cliente Groq
client = Groq(api_key="pega tu api_kay de groq")
messages = []


def ejemplo(user_input):

    # messages={"role": "user","content": ""}
    messages.append({ "role": "user","content": f" resuelve un  egemplo con {user_input} tu respuesta debera ser texto y ecuaciones unicamente en formato Latex"})
    """Envía mensajes a la API de Groq y retorna la respuesta."""
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",  # Asegúrate de usar un modelo válido
            messages=messages,
            temperature=0.5,
            max_tokens=1000,
            stream=False,
        )
        # Accede al contenido del mensaje de manera correcta
        response_message = completion.choices[0].message.content
        
        return response_message
    except Exception as e:
        return f"Error al obtener respuesta: {e}"



def aplicaciones(user_input):

    # messages={"role": "user","content": ""}
    messages.append({ "role": "user","content": f" menciona 5 aplicaciones donde se use la {user_input} genera solo texto plano sin ecuaciones"})
    """Envía mensajes a la API de Groq y retorna la respuesta."""
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",  # Asegúrate de usar un modelo válido
            messages=messages,
            temperature=0.2,
            max_tokens=800,
            stream=False,
        )
        # Accede al contenido del mensaje de manera correcta
        response_message = completion.choices[0].message.content
        
        return response_message
    except Exception as e:
        return f"Error al obtener respuesta: {e}"


















def get_ai_response(user_input):
    # messages={"role": "user","content": ""}
    messages.append({ "role": "user","content": f" cual es el nombre de esta ecuacion {user_input} solo el nombre no escribas mas"})
    """Envía mensajes a la API de Groq y retorna la respuesta."""
    try:
        completion = client.chat.completions.create(
            model="llama-3.1-70b-versatile",  # Asegúrate de usar un modelo válido
            messages=messages,
            temperature=0.1,
            max_tokens=50,
            stream=False,
        )
        # Accede al contenido del mensaje de manera correcta
        response_message = completion.choices[0].message.content
        
        return response_message
    except Exception as e:
        return f"Error al obtener respuesta: {e}"
    
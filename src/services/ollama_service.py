import requests
import os
from dotenv import load_dotenv

load_dotenv()

class OllamaService:
    def __init__(self):
        self.url = os.getenv('OLLAMA_URL')
        self.model = os.getenv('MODEL_NAME')

    def generate_response(self, prompt, context=None):
        try:
            if context:
                # Construir prompt con contexto
                full_prompt = f"""Eres un asistente experto en código. A continuación se te proporciona contexto de código de un repositorio.
                
                CONTEXTO DEL REPOSITORIO:
                {context}
                
                PREGUNTA DEL USUARIO:
                {prompt}
                
                Responde basándote en el contexto proporcionado. Si la respuesta no está en el contexto, 
                usa tu conocimiento general pero indica que no encontraste la información específica en el repositorio.
                """
            else:
                full_prompt = prompt
            response = requests.post(
                self.url,
                json = {
                    'model': self.model,
                    'prompt': full_prompt,
                    'stream': False
                },
                timeout= 400
            )

            if response.status_code == 200:
                return response.json()['response']
            else:
                return f"Error: el modelo respondio con codigo {response.status_code}"
            
        except requests.exceptions.ConnectionError:
            return "Error: No se pudo conectar a Ollama. ¿Esta ejecutandose?"
        except requests.exceptions.Timeout:
            return "Error: La consulta tardo demasiado tiempo"
        except Exception as ex:
            return f"Error insesperado: {str(ex)}s"
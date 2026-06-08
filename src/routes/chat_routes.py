from flask import Blueprint, request, jsonify
from services.ollama_service import OllamaService
from services.github_service import GitHubService

chat_bp = Blueprint('chat', __name__)

ollama_service = OllamaService()
github_service = GitHubService()

@chat_bp.route('/', methods=['GET'])
def health_check():
    """Endpoint de verificación"""
    return jsonify({'status': 'ok', 'service': 'Chat API'})

@chat_bp.route('/', methods=['POST'])
def chat():
    data = request.json

    if not data or 'message' not in data:
        return jsonify({'error': 'Falta el campo "message"'}), 400
    
    user_message = data.get('message')
    repo_context = data.get('repository', None)
    context = None

    if repo_context:
        # Buscar contexto en el repositorio especificado
        context, error = github_service.get_code_context(repo_context, user_message)
        if error:
            return jsonify({'response': f"Advertencia: {error}\n\nRespondiendo sin contexto...", 
                            'model': ollama_service.model}), 200

    response_text = ollama_service.generate_response(user_message, context)

    return jsonify({
        'response': response_text,
        'model': ollama_service.model,
        'context_used': context is not None,
        'repository': repo_context
    })
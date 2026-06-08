from flask import Blueprint, request, jsonify
from services.github_service import GitHubService

github_service = GitHubService()

github_bp = Blueprint('github', __name__)

@github_bp.route('/', methods=['GET'])
def health_check():
    """Endpoint de verificación - GitHub service (próximamente)"""
    return jsonify({'status': 'ok', 'service': 'GitHub API (en desarrollo)'})

@github_bp.route('/repos', methods=['GET'])
def list_repos():
    """Lista todos los repositorios clonados"""
    repos = github_service.list_repos()
    return jsonify({'repositories': repos})

@github_bp.route('/repos', methods=['POST'])
def add_repository():
    """Clona un repositorio nuevo"""
    data = request.json
    
    if not data or 'url' not in data:
        return jsonify({'error': 'Falta el campo "url"'}), 400
    
    repo_url = data.get('url')
    result = github_service.clone_or_pull_repo(repo_url)
    
    return jsonify({
        'message': f'Repositorio {result["status"]} correctamente',
        'repository': result
    })

@github_bp.route('/repos/<repo_name>', methods=['DELETE'])
def remove_repository(repo_name):
    """Elimina un repositorio clonado"""
    if github_service.remove_repo(repo_name):
        return jsonify({'message': f'Repositorio {repo_name} eliminado'})
    else:
        return jsonify({'error': 'Repositorio no encontrado'}), 404

@github_bp.route('/repos/<repo_name>/search', methods=['POST'])
def search_in_repo(repo_name):
    """Busca código relevante en un repositorio"""
    data = request.json
    
    if not data or 'query' not in data:
        return jsonify({'error': 'Falta el campo "query"'}), 400
    
    query = data.get('query')
    context, error = github_service.get_code_context(repo_name, query)
    
    if error:
        return jsonify({'error': error}), 404
    
    return jsonify({
        'repository': repo_name,
        'query': query,
        'context': context
    })
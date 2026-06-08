# src/services/github_service.py
import os
import git
from pathlib import Path
import re

class GitHubService:
    def __init__(self, repos_base_path="./repos"):
        self.repos_base_path = Path(repos_base_path)
        self.repos_base_path.mkdir(exist_ok=True)
        self.repos = {}  # Diccionario para guardar referencias a repos clonados
    
    def clone_or_pull_repo(self, repo_url):
        """Clona un repositorio o lo actualiza si ya existe"""
        # Extraer nombre del repositorio desde la URL
        repo_name = repo_url.split('/')[-1].replace('.git', '')
        repo_path = self.repos_base_path / repo_name
        
        if repo_path.exists():
            # Si ya existe, hacer pull para actualizar
            repo = git.Repo(repo_path)
            repo.remotes.origin.pull()
            return {"status": "updated", "path": str(repo_path), "name": repo_name}
        else:
            # Clonar repositorio
            repo = git.Repo.clone_from(repo_url, repo_path)
            return {"status": "cloned", "path": str(repo_path), "name": repo_name}
    
    def list_repos(self):
        """Lista todos los repositorios clonados"""
        repos_list = []
        for repo_path in self.repos_base_path.iterdir():
            if repo_path.is_dir() and (repo_path / ".git").exists():
                repos_list.append({
                    "name": repo_path.name,
                    "path": str(repo_path)
                })
        return repos_list
    
    def get_code_context(self, repo_name, query, max_files=20):
        """Busca archivos relevantes en el repositorio basado en la consulta"""
        repo_path = self.repos_base_path / repo_name
        
        if not repo_path.exists():
            return None, f"Repositorio {repo_name} no encontrado"
        
        # Extensiones de archivos de código a incluir
        code_extensions = {'.py', '.js', '.ts', '.java', '.cpp', '.c', '.h', 
                          '.go', '.rs', '.rb', '.php', '.html', '.css', '.json'}
        
        relevant_files = []
        
        # Buscar archivos que coincidan con la consulta
        for file_path in repo_path.rglob('*'):
            if file_path.is_file() and file_path.suffix in code_extensions:
                # Evitar carpetas ocultas y venv
                if any(part.startswith('.') or part == 'venv' or part == '__pycache__' 
                    for part in file_path.parts):
                    continue
                
                # Leer contenido del archivo (limitado a primeras líneas)
                try:
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read()
                    
                    # Verificar si el archivo es relevante (búsqueda simple por palabras)
                    if any(word.lower() in content.lower() for word in query.split()[:5]):
                        relevant_files.append({
                            "name": str(file_path.relative_to(repo_path)),
                            "content": content[:2000],  # Limitar tamaño
                            "size": len(content)
                        })
                except Exception as e:
                    continue
        
        # Limitar número de archivos
        relevant_files = relevant_files[:max_files]
        
        if not relevant_files:
            return None, f"No se encontraron archivos relevantes en {repo_name}"
        
        # Construir contexto
        context = f"Repositorio: {repo_name}\n\nArchivos relevantes encontrados:\n"
        for file_info in relevant_files:
            context += f"\n--- Archivo: {file_info['name']} ---\n"
            context += file_info['content'][:1000]  # Limitar cada archivo
            context += "\n...\n"
        
        return context, None
    
    def remove_repo(self, repo_name):
        """Elimina un repositorio clonado"""
        repo_path = self.repos_base_path / repo_name
        if repo_path.exists():
            import shutil
            shutil.rmtree(repo_path)
            return True
        return False
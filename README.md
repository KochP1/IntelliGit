# IntelliGit - Agente IA Local para Repositorios GitHub

## 📋 Descripción

IntelliGit es un agente de IA personal que se ejecuta localmente y puede conectarse a tus repositorios de GitHub para proporcionar contexto inteligente sobre tu código. Utiliza DeepSeek-Coder como modelo de IA local, garantizando privacidad y sin costos de API.

## ✨ Funcionalidades Actuales

- ✅ **Chat con IA local** usando DeepSeek-Coder 6.7b
- ✅ **Clonar y gestionar repositorios GitHub**
- ✅ **Consultar código con contexto** del repositorio
- ✅ **API REST completa** para integración con frontend
- ✅ **Búsqueda contextual** en repositorios clonados

## 🚀 Próximas Funcionalidades

- ⏳ Memoria de conversaciones (base de datos)
- ⏳ Indexación semántica con RAG
- ⏳ Interfaz web (Angular)
- ⏳ Streaming de respuestas (efecto ChatGPT)

## 📦 Requisitos del Sistema

### Hardware Recomendado
| Componente | Mínimo | Recomendado |
|------------|--------|--------------|
| RAM | 8 GB | 16 GB |
| Almacenamiento | 10 GB | 20 GB |
| CPU | 4 núcleos | 8+ núcleos |
| GPU | Opcional | NVIDIA (4GB+ VRAM) |

### Software Requerido
- **Windows 10/11**, Linux o macOS
- **Python 3.12** (recomendado)
- **Git** (para clonar repositorios)

## 🛠️ Instalación Paso a Paso

### 1. Instalar Ollama

#### Windows

# Descargar desde la página oficial
https://ollama.com/download

# Ejecutar el instalador .exe

### 2. Instalar modelo

# Modelo pequeño (4GB RAM) - Recomendado para empezar
ollama pull deepseek-coder:1.3b

# Modelo balanceado (8GB RAM) - Ideal para desarrollo
ollama pull deepseek-coder:6.7b

# Modelo completo (16GB+ RAM) - Máxima calidad
ollama pull deepseek-coder:33b

### 3. Clonar proyecto

### 4. Crear entorno virtual venv y activarlo
python3 -m venv venv
source venv/bin/activate

### 5. Instalar requerimentos
pip install -r requirements.txt

### 6. Crear archivo .env en la raiz del proyecto
VERSION=DEV
ENVIRONMENT=DEV
FLASK_PORT=5000
ANGULAR_URL=http://localhost:4200
OLLAMA_URL=http://localhost:11434/api/generate
MODEL_NAME=deepseek-coder:6.7b

### 7. Asegurarse que ollama esta corriendo
ollama list

### 8. Ejecutar api de flask
# Desde la raíz del proyecto
python src/app.py
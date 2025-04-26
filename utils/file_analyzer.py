"""
Analisador de estrutura de projeto a partir de arquivos enviados.
"""

import os
import tempfile
import zipfile
import tarfile
import shutil
from werkzeug.utils import secure_filename

def analyze_structure(uploaded_file):
    """
    Analisa a estrutura de um arquivo zip ou tar.gz enviado.
    Retorna uma representação em string da estrutura de diretórios.
    
    Args:
        uploaded_file: Objeto de arquivo enviado pelo formulário.
    
    Returns:
        str: Estrutura do projeto em formato de árvore.
    """
    filename = secure_filename(uploaded_file.filename)
    
    # Cria diretório temporário para extração
    temp_dir = tempfile.mkdtemp()
    temp_file_path = os.path.join(temp_dir, filename)
    
    try:
        # Salva o arquivo enviado
        uploaded_file.save(temp_file_path)
        
        # Extrai o arquivo baseado no tipo
        extract_dir = os.path.join(temp_dir, "extracted")
        os.makedirs(extract_dir, exist_ok=True)
        
        if filename.endswith('.zip'):
            with zipfile.ZipFile(temp_file_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)
        elif filename.endswith('.tar.gz') or filename.endswith('.tgz'):
            with tarfile.open(temp_file_path, 'r:gz') as tar_ref:
                tar_ref.extractall(extract_dir)
        else:
            return "Formato de arquivo não suportado. Use .zip ou .tar.gz"
        
        # Gera a representação em árvore da estrutura
        tree_structure = generate_tree_structure(extract_dir)
        
        return tree_structure
    except Exception as e:
        return f"Erro ao analisar a estrutura: {str(e)}"
    finally:
        # Limpa os arquivos temporários
        shutil.rmtree(temp_dir, ignore_errors=True)

def generate_tree_structure(directory, prefix="", is_last=True, ignore_patterns=None):
    """
    Gera uma representação em árvore da estrutura de diretórios.
    
    Args:
        directory (str): Caminho do diretório a ser analisado
        prefix (str): Prefixo para a linha atual (usado na recursão)
        is_last (bool): Se é o último item no nível atual
        ignore_patterns (list): Lista de padrões a serem ignorados
    
    Returns:
        str: Representação em árvore da estrutura
    """
    if ignore_patterns is None:
        ignore_patterns = [
            '__pycache__', 
            '.git', 
            '.idea', 
            '.vscode', 
            'node_modules',
            '.DS_Store',
            '*.pyc',
            '*.pyo',
            '*.pyd',
            '.pytest_cache',
            '.coverage',
            'venv',
            'env',
            '.env'
        ]
    
    base_name = os.path.basename(directory)
    
    # Verificar se o diretório deve ser ignorado
    for pattern in ignore_patterns:
        if pattern.startswith('*'):
            if base_name.endswith(pattern[1:]):
                return ""
        elif pattern == base_name:
            return ""
    
    # Símbolo para o item atual
    if is_last:
        tree_head = "└── "
        next_prefix = prefix + "    "
    else:
        tree_head = "├── "
        next_prefix = prefix + "│   "
    
    tree_structure = [prefix + tree_head + base_name]
    
    # Listar e ordenar itens no diretório
    try:
        items = sorted(os.listdir(directory))
    except:
        # Se não conseguir listar o diretório, retorna apenas o nome
        return "\n".join(tree_structure)
    
    # Filtrar itens a serem ignorados
    filtered_items = []
    for item in items:
        ignore = False
        for pattern in ignore_patterns:
            if pattern.startswith('*'):
                if item.endswith(pattern[1:]):
                    ignore = True
                    break
            elif pattern == item:
                ignore = True
                break
        if not ignore:
            filtered_items.append(item)
    
    # Processar arquivos e diretórios
    for i, item in enumerate(filtered_items):
        item_path = os.path.join(directory, item)
        is_last_item = (i == len(filtered_items) - 1)
        
        if os.path.isdir(item_path):
            # Recursivamente processar subdiretórios
            subtree = generate_tree_structure(
                item_path, 
                next_prefix, 
                is_last_item, 
                ignore_patterns
            )
            if subtree:
                tree_structure.append(subtree)
        else:
            # Adicionar arquivo
            if is_last_item:
                file_prefix = prefix + "    └── "
            else:
                file_prefix = prefix + "    ├── "
            tree_structure.append(file_prefix + item)
    
    return "\n".join(tree_structure)
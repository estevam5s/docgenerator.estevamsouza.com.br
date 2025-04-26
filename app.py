"""
DocGen - Sistema de Geração de Documentação Profissional

Aplicação principal em Flask que fornece as rotas e funcionalidades para
gerar documentação profissional em formato Markdown para repositórios GitHub.
"""

from flask import Flask, render_template, request, jsonify, session, redirect, url_for, flash, send_file
import os
import json
import markdown
import tempfile
from datetime import datetime
from werkzeug.utils import secure_filename
from flask_session import Session

from utils.markdown_generator import generate_markdown
from utils.file_analyzer import analyze_structure
from utils.template_manager import get_project_template
from models.project import Project

# Inicialização da aplicação Flask
app = Flask(__name__)

# Configurações da aplicação
app.config.update(
    SECRET_KEY=os.environ.get('SECRET_KEY', os.urandom(24)),
    SESSION_TYPE='filesystem',
    SESSION_PERMANENT=False,
    SESSION_USE_SIGNER=True,
    SESSION_FILE_DIR=tempfile.mkdtemp(),
    MAX_CONTENT_LENGTH=50 * 1024 * 1024,  # Limite de 50MB para uploads
    UPLOAD_FOLDER=os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads'),
    ALLOWED_EXTENSIONS={'zip', 'tar.gz', 'tgz'}
)

# Inicializa extensões
Session(app)

# Configuração de tipos de projetos disponíveis
PROJECT_TYPES = {
    "backend": "Aplicação Backend",
    "frontend": "Aplicação Frontend",
    "fullstack": "Aplicação Full Stack",
    "mobile": "Aplicação Mobile",
    "cybersec": "Projeto de Cybersegurança",
    "network": "Sistemas de Redes",
    "frameworks": "Framework Específico"
}

# Assegura que o diretório de uploads exista
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Funções auxiliares
def get_project_description(project_type):
    """
    Retorna uma descrição detalhada para um tipo específico de projeto.
    
    Args:
        project_type (str): O tipo de projeto
        
    Returns:
        str: Descrição do tipo de projeto
    """
    descriptions = {
        'backend': 'Sistemas, APIs e serviços com foco em processamento e armazenamento de dados.',
        'frontend': 'Interfaces de usuário, sites e aplicações web com foco em experiência do usuário.',
        'fullstack': 'Aplicações completas que integram frontend e backend em uma solução unificada.',
        'mobile': 'Aplicativos para dispositivos móveis iOS, Android ou multiplataforma.',
        'cybersec': 'Soluções de segurança digital, análise de vulnerabilidades e proteção de dados.',
        'network': 'Infraestrutura de redes, protocolos e sistemas de comunicação.',
        'frameworks': 'Bibliotecas, frameworks e ferramentas para desenvolvimento de software.'
    }
    
    return descriptions.get(project_type, 'Template personalizado para seu tipo específico de projeto.')

def allowed_file(filename):
    """Verifica se o arquivo possui uma extensão permitida"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

def clear_expired_sessions():
    """Remove arquivos de sessão expirados (mais de 24 horas)"""
    session_dir = app.config['SESSION_FILE_DIR']
    now = datetime.now()
    
    for filename in os.listdir(session_dir):
        filepath = os.path.join(session_dir, filename)
        file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
        if (now - file_modified).days > 1:
            os.remove(filepath)

def create_example_project(project_type):
    """Cria um projeto de exemplo pré-preenchido"""
    # Inicializa um projeto com dados de exemplo
    project = Project(project_type=project_type, name=f"Exemplo de {PROJECT_TYPES[project_type]}")
    
    # Adiciona dados de exemplo específicos para o tipo de projeto
    if project_type == 'backend':
        project.update_section('project_info', {
            'name': 'API de Gerenciamento de Tarefas',
            'short_description': 'API REST para gerenciamento de tarefas e projetos com autenticação e permissões.',
            'logo_url': 'https://example.com/logo.png'
        })
        project.update_section('about', {
            'description': 'Esta API oferece endpoints para gerenciamento completo de tarefas, projetos e usuários, com autenticação JWT e controle granular de permissões.',
            'motivation': 'Criada para demonstrar boas práticas de desenvolvimento de APIs RESTful com Python e Flask.',
            'key_features': '- Autenticação JWT\n- Permissões baseadas em funções\n- Documentação automática com Swagger\n- Testes automatizados\n- Containerização com Docker'
        })
    elif project_type == 'frontend':
        project.update_section('project_info', {
            'name': 'Dashboard de Analytics',
            'short_description': 'Interface moderna para visualização de dados analíticos com gráficos interativos.',
            'logo_url': 'https://example.com/logo.png'
        })
        project.update_section('about', {
            'description': 'Dashboard moderno e responsivo para visualização de dados analíticos, com gráficos interativos e filtros avançados.',
            'motivation': 'Criado para demonstrar técnicas de visualização de dados com React e D3.js.',
            'key_features': '- Gráficos interativos\n- Temas personalizáveis\n- Filtros avançados\n- Exportação de dados\n- Responsivo para dispositivos móveis'
        })
    
    # Adiciona tecnologias genéricas
    project.update_section('technology', {
        'technologies': 'Python,JavaScript,Docker,Git,GitHub Actions',
        'architecture': 'Arquitetura do projeto de exemplo.'
    })
    
    return project

# Rotas da aplicação
@app.route('/')
def index():
    """Página inicial com seleção de tipo de projeto"""
    # Limpa sessões expiradas periodicamente
    clear_expired_sessions()
    
    return render_template(
        'index.html', 
        project_types=PROJECT_TYPES,
        get_project_description=get_project_description
    )

@app.route('/setup', methods=['POST'])
def setup_project():
    """Configuração inicial do projeto"""
    project_type = request.form.get('project_type')
    
    if project_type not in PROJECT_TYPES:
        flash('Tipo de projeto inválido. Por favor, selecione uma opção válida.', 'error')
        return redirect(url_for('index'))
    
    # Verifica se é para usar um exemplo
    use_example = request.form.get('use_example') == 'true'
    
    if use_example:
        # Cria um projeto de exemplo pré-preenchido
        project = create_example_project(project_type)
        session['project'] = project.to_dict()
    else:
        # Inicializa projeto vazio na sessão
        project = Project(project_type=project_type)
        session['project'] = project.to_dict()
    
    # Carrega template baseado no tipo
    template = get_project_template(project_type)
    session['template'] = template
    
    # Define o tema padrão
    session['theme'] = 'default'
    
    return redirect(url_for('editor', section='project_info'))

@app.route('/editor')
def editor():
    """Interface principal de edição"""
    if 'project' not in session:
        flash('Sessão expirada ou projeto não iniciado.', 'error')
        return redirect(url_for('index'))
    
    project_data = session.get('project')
    template = session.get('template')
    theme = session.get('theme', 'default')
    current_section = request.args.get('section', 'project_info')
    
    # Converte de volta para objeto Project
    project = Project.from_dict(project_data)
    
    # Verifica se a seção existe no template
    if current_section not in template:
        current_section = 'project_info'
    
    # Gera o preview inicial
    preview_markdown = generate_markdown(project_data)
    preview_html = markdown.markdown(preview_markdown, extensions=['extra', 'codehilite'])
    
    # Calcula o progresso do projeto
    completed_sections = sum(1 for section in template if project.is_section_complete(section))
    total_sections = len(template)
    progress = int((completed_sections / total_sections) * 100) if total_sections > 0 else 0
    
    return render_template(
        'editor.html',
        project=project_data,
        project_obj=project,
        template=template,
        current_section=current_section,
        preview_markdown=preview_markdown,
        preview_html=preview_html,
        theme=theme,
        progress=progress
    )

@app.route('/update_section', methods=['POST'])
def update_section():
    """Atualiza uma seção específica do projeto"""
    if 'project' not in session:
        return jsonify({'error': 'Sessão expirada'}), 400
    
    section = request.form.get('section')
    if not section:
        return jsonify({'error': 'Seção não especificada'}), 400
    
    data = {}
    
    # Processa os dados do formulário
    for key, value in request.form.items():
        if key != 'section':
            # Processa checkboxes (que enviam múltiplos valores)
            if key.endswith('[]'):
                base_key = key.rstrip('[]')
                if base_key not in data:
                    data[base_key] = []
                data[base_key].append(value)
            else:
                data[key] = value
    
    # Atualiza a seção no projeto
    project_data = session.get('project')
    project = Project.from_dict(project_data)
    project.update_section(section, data)
    
    # Atualiza a sessão
    session['project'] = project.to_dict()
    
    # Gera preview do markdown
    markdown_content = generate_markdown(project.to_dict())
    html_preview = markdown.markdown(markdown_content, extensions=['extra', 'codehilite'])
    
    return jsonify({
        'success': True,
        'markdown': markdown_content,
        'html_preview': html_preview
    })

@app.route('/upload_structure', methods=['POST'])
def upload_structure():
    """Processa upload de estrutura de arquivos"""
    if 'project' not in session:
        return jsonify({'error': 'Sessão expirada'}), 400
    
    if 'project_files' not in request.files:
        return jsonify({'error': 'Nenhum arquivo enviado'}), 400
    
    file = request.files['project_files']
    
    if file.filename == '':
        return jsonify({'error': 'Nenhum arquivo selecionado'}), 400
    
    if not allowed_file(file.filename):
        return jsonify({'error': 'Tipo de arquivo não suportado. Use .zip ou .tar.gz'}), 400
    
    # Salva o arquivo temporariamente
    filename = secure_filename(file.filename)
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    try:
        # Análise da estrutura de arquivos
        structure = analyze_structure(filepath)
        
        # Atualiza estrutura no projeto
        project_data = session.get('project')
        project = Project.from_dict(project_data)
        project.structure = structure
        session['project'] = project.to_dict()
        
        # Atualiza também na seção de estrutura se existir
        if 'structure' in project.sections:
            project.sections['structure']['manual_structure'] = structure
            session['project'] = project.to_dict()
        
        return jsonify({
            'success': True,
            'structure': structure
        })
    except Exception as e:
        return jsonify({'error': f'Erro ao analisar estrutura: {str(e)}'}), 500
    finally:
        # Remove o arquivo temporário
        if os.path.exists(filepath):
            os.remove(filepath)

@app.route('/export', methods=['GET'])
def export_markdown():
    """Exporta o markdown final"""
    if 'project' not in session:
        return redirect(url_for('index'))
    
    project_data = session.get('project')
    markdown_content = generate_markdown(project_data)
    
    project_name = project_data.get('name', 'README').replace(' ', '_')
    filename = f"{project_name}.md"
    
    return jsonify({
        'markdown': markdown_content,
        'filename': filename
    })

@app.route('/download', methods=['GET'])
def download_markdown():
    """Faz download do arquivo markdown"""
    if 'project' not in session:
        flash('Sessão expirada ou projeto não iniciado.', 'error')
        return redirect(url_for('index'))
    
    project_data = session.get('project')
    markdown_content = generate_markdown(project_data)
    
    # Cria arquivo temporário
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.md')
    temp_file.write(markdown_content.encode('utf-8'))
    temp_file.close()
    
    project_name = project_data.get('name', 'README').replace(' ', '_')
    filename = f"{project_name}.md"
    
    return send_file(
        temp_file.name,
        as_attachment=True,
        download_name=filename,
        mimetype='text/markdown'
    )

@app.route('/update_theme', methods=['POST'])
def update_theme():
    """Atualiza o tema da interface"""
    if 'project' not in session:
        return jsonify({'error': 'Sessão expirada'}), 400
    
    theme = request.form.get('theme', 'default')
    session['theme'] = theme
    
    return jsonify({'success': True, 'theme': theme})

@app.route('/get_sections_status', methods=['GET'])
def get_sections_status():
    """Retorna o status de completude de cada seção"""
    if 'project' not in session:
        return jsonify({'error': 'Sessão expirada'}), 400
    
    project_data = session.get('project')
    template = session.get('template')
    
    project = Project.from_dict(project_data)
    sections_status = {}
    
    for section_id in template:
        sections_status[section_id] = project.is_section_complete(section_id)
    
    return jsonify({
        'success': True,
        'status': sections_status
    })

@app.route('/reset', methods=['GET'])
def reset_project():
    """Reset o projeto atual e redireciona para a página inicial"""
    # Limpa dados da sessão
    if 'project' in session:
        del session['project']
    if 'template' in session:
        del session['template']
    
    flash('Projeto resetado com sucesso!', 'success')
    return redirect(url_for('index'))

@app.route('/examples', methods=['GET'])
def view_examples():
    """Exibe exemplos de documentações geradas"""
    examples = [
        {
            'name': 'API REST Flask',
            'type': 'backend',
            'image': 'example_backend.png',
            'description': 'Exemplo de documentação para uma API REST em Flask',
            'demo_link': '/demo/backend'
        },
        {
            'name': 'Dashboard React',
            'type': 'frontend',
            'image': 'example_frontend.png',
            'description': 'Exemplo de documentação para um dashboard em React',
            'demo_link': '/demo/frontend'
        },
        {
            'name': 'Aplicativo Mobile',
            'type': 'mobile',
            'image': 'example_mobile.png',
            'description': 'Exemplo de documentação para um aplicativo mobile',
            'demo_link': '/demo/mobile'
        }
    ]
    
    return render_template('examples.html', examples=examples)

@app.route('/demo/<example_type>', methods=['GET'])
def view_demo(example_type):
    """Exibe uma demonstração de documentação"""
    if example_type not in PROJECT_TYPES:
        flash('Exemplo não encontrado', 'error')
        return redirect(url_for('examples'))
    
    # Cria um projeto de exemplo
    project = create_example_project(example_type)
    
    # Gera o markdown e HTML
    markdown_content = generate_markdown(project.to_dict())
    html_preview = markdown.markdown(markdown_content, extensions=['extra', 'codehilite'])
    
    return render_template(
        'demo.html',
        project_type=PROJECT_TYPES[example_type],
        project=project.to_dict(),
        markdown_content=markdown_content,
        html_preview=html_preview
    )

@app.errorhandler(404)
def page_not_found(e):
    """Manipulador para erro 404"""
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    """Manipulador para erro 500"""
    return render_template('500.html'), 500

# Filtros e contextos personalizados
@app.template_filter('format_date')
def format_date_filter(value, format='%d/%m/%Y'):
    """Formata uma data para exibição"""
    if value is None:
        return ""
    if isinstance(value, str):
        try:
            value = datetime.strptime(value, '%Y-%m-%d')
        except ValueError:
            return value
    return value.strftime(format)

@app.context_processor
def utility_processor():
    """Adiciona funções úteis aos templates"""
    def get_version():
        return "1.0.0"
    
    def get_app_name():
        return "DocGen"
    
    return dict(
        get_version=get_version,
        get_app_name=get_app_name,
        current_year=datetime.now().year
    )

# Execução da aplicação
if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', 'True').lower() == 'true',
           host=os.environ.get('FLASK_HOST', '0.0.0.0'),
           port=int(os.environ.get('FLASK_PORT', 5000)))
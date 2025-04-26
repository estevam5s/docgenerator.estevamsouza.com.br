class Project:
    """
    Classe para representar um projeto e suas seções de documentação.
    """
    
    def __init__(self, project_type=None, name=None):
        self.project_type = project_type
        self.name = name
        self.sections = {}
        self.structure = None
        self.theme = "default"
        
    def to_dict(self):
        """
        Converte o projeto para um dicionário para armazenamento em sessão.
        """
        return {
            'type': self.project_type,
            'name': self.name,
            'sections': self.sections,
            'structure': self.structure,
            'theme': self.theme
        }
    
    @classmethod
    def from_dict(cls, data):
        """
        Cria uma instância de Project a partir de um dicionário (sessão).
        """
        project = cls(
            project_type=data.get('type'),
            name=data.get('name')
        )
        project.sections = data.get('sections', {})
        project.structure = data.get('structure')
        project.theme = data.get('theme', 'default')
        return project
    
    def update_section(self, section_id, data):
        """
        Atualiza uma seção específica do projeto.
        """
        self.sections[section_id] = data
        
    def get_section(self, section_id):
        """
        Obtém dados de uma seção específica.
        """
        return self.sections.get(section_id, {})
        
    def is_section_complete(self, section_id):
        """
        Verifica se uma seção está completa (todos os campos obrigatórios preenchidos).
        """
        if section_id not in self.sections:
            return False
            
        # Lógica para verificar campos obrigatórios
        # Implementação dependerá das regras específicas para cada seção
        return True
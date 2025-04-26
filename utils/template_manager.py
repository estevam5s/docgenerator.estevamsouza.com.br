"""
Gerenciador de templates para diferentes tipos de projetos.
Cada template define as seções e campos a serem preenchidos.
"""

def get_project_template(project_type):
    """
    Retorna o template apropriado para o tipo de projeto.
    """
    # Template base que todos os projetos terão
    base_template = {
        "project_info": {
            "title": "Informações do Projeto",
            "fields": [
                {
                    "id": "name",
                    "label": "Nome do Projeto",
                    "type": "text",
                    "required": True,
                    "placeholder": "Ex: Sistema de Gestão de Inventário"
                },
                {
                    "id": "short_description",
                    "label": "Descrição Curta",
                    "type": "textarea",
                    "required": True,
                    "placeholder": "Descrição breve do projeto em 1-2 frases"
                },
                {
                    "id": "logo_url",
                    "label": "URL do Logo (opcional)",
                    "type": "text",
                    "required": False,
                    "placeholder": "https://exemplo.com/logo.png"
                }
            ]
        },
        "about": {
            "title": "Sobre o Projeto",
            "fields": [
                {
                    "id": "description",
                    "label": "Descrição Detalhada",
                    "type": "textarea",
                    "required": True,
                    "placeholder": "Descreva detalhadamente o propósito e funcionalidade do projeto"
                },
                {
                    "id": "motivation",
                    "label": "Motivação",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "O que inspirou a criação deste projeto?"
                },
                {
                    "id": "key_features",
                    "label": "Características Principais",
                    "type": "textarea",
                    "required": True,
                    "placeholder": "Liste as principais características separadas por linhas"
                }
            ]
        },
        "technology": {
            "title": "Tecnologias Utilizadas",
            "fields": [
                {
                    "id": "technologies",
                    "label": "Tecnologias",
                    "type": "tags",
                    "required": True,
                    "placeholder": "Ex: Python, Flask, React, etc."
                },
                {
                    "id": "architecture",
                    "label": "Arquitetura",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "Descreva a arquitetura do sistema"
                }
            ]
        },
        "installation": {
            "title": "Instalação e Configuração",
            "fields": [
                {
                    "id": "prerequisites",
                    "label": "Pré-requisitos",
                    "type": "textarea",
                    "required": True,
                    "placeholder": "Liste os pré-requisitos necessários"
                },
                {
                    "id": "installation_steps",
                    "label": "Passos de Instalação",
                    "type": "textarea",
                    "required": True,
                    "placeholder": "Descreva os passos de instalação (em formato de lista)"
                },
                {
                    "id": "env_variables",
                    "label": "Variáveis de Ambiente",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "Liste as variáveis de ambiente necessárias"
                }
            ]
        },
        "usage": {
            "title": "Como Utilizar",
            "fields": [
                {
                    "id": "usage_instructions",
                    "label": "Instruções de Uso",
                    "type": "textarea",
                    "required": True,
                    "placeholder": "Explique como utilizar o projeto"
                },
                {
                    "id": "examples",
                    "label": "Exemplos",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "Forneça exemplos de uso"
                },
                {
                    "id": "commands",
                    "label": "Comandos Principais",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "Liste os comandos principais"
                }
            ]
        },
        "structure": {
            "title": "Estrutura do Projeto",
            "fields": [
                {
                    "id": "upload_structure",
                    "label": "Fazer upload da estrutura (opcional)",
                    "type": "file",
                    "required": False,
                    "accept": ".zip,.tar.gz"
                },
                {
                    "id": "manual_structure",
                    "label": "Estrutura Manual",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "Estrutura de diretórios do projeto"
                }
            ]
        },
        "api": {
            "title": "API e Endpoints",
            "fields": [
                {
                    "id": "has_api",
                    "label": "O projeto tem API?",
                    "type": "radio",
                    "options": ["Sim", "Não"],
                    "required": True
                },
                {
                    "id": "api_documentation",
                    "label": "Documentação da API",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "Descreva os endpoints da API",
                    "conditional": {"field": "has_api", "value": "Sim"}
                }
            ]
        },
        "contributing": {
            "title": "Contribuição",
            "fields": [
                {
                    "id": "contribution_guidelines",
                    "label": "Diretrizes de Contribuição",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "Explique como outros desenvolvedores podem contribuir"
                },
                {
                    "id": "code_of_conduct",
                    "label": "Código de Conduta",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "Código de conduta para contribuidores"
                }
            ]
        },
        "roadmap": {
            "title": "Roadmap",
            "fields": [
                {
                    "id": "future_features",
                    "label": "Funcionalidades Futuras",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "Liste funcionalidades planejadas para o futuro"
                },
                {
                    "id": "known_issues",
                    "label": "Problemas Conhecidos",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "Liste problemas conhecidos"
                }
            ]
        },
        "license": {
            "title": "Licença",
            "fields": [
                {
                    "id": "license_type",
                    "label": "Tipo de Licença",
                    "type": "select",
                    "options": [
                        "MIT", "GPL-3.0", "Apache-2.0", "BSD-3-Clause", 
                        "BSD-2-Clause", "CC0-1.0", "Outra", "Nenhuma"
                    ],
                    "required": True
                },
                {
                    "id": "custom_license",
                    "label": "Licença Personalizada",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "Detalhes da licença personalizada",
                    "conditional": {"field": "license_type", "value": "Outra"}
                }
            ]
        },
        "contact": {
            "title": "Contato e Suporte",
            "fields": [
                {
                    "id": "contact_info",
                    "label": "Informações de Contato",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "Como entrar em contato com a equipe"
                },
                {
                    "id": "support_channels",
                    "label": "Canais de Suporte",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "Canais disponíveis para suporte"
                }
            ]
        },
        "faq": {
            "title": "FAQ",
            "fields": [
                {
                    "id": "faq_items",
                    "label": "Perguntas Frequentes",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "Liste perguntas e respostas frequentes (formato P: Pergunta / R: Resposta)"
                }
            ]
        },
        "acknowledgements": {
            "title": "Agradecimentos",
            "fields": [
                {
                    "id": "acknowledgements",
                    "label": "Agradecimentos",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "Agradecimentos a colaboradores, ferramentas, etc."
                }
            ]
        },
        "team": {
            "title": "Equipe",
            "fields": [
                {
                    "id": "team_members",
                    "label": "Membros da Equipe",
                    "type": "textarea",
                    "required": False,
                    "placeholder": "Liste os membros da equipe e seus papéis"
                }
            ]
        },
        # Adicione mais seções conforme necessário
    }

    # Templates específicos por tipo de projeto
    specific_templates = {
        "backend": {
            # Campos específicos para backend
            "api": {
                "title": "API e Endpoints",
                "fields": [
                    {
                        "id": "api_documentation",
                        "label": "Documentação da API",
                        "type": "textarea",
                        "required": True,
                        "placeholder": "Descreva os endpoints da API"
                    },
                    {
                        "id": "authentication",
                        "label": "Autenticação",
                        "type": "textarea",
                        "required": False,
                        "placeholder": "Descreva os métodos de autenticação"
                    }
                ]
            },
            "database": {
                "title": "Banco de Dados",
                "fields": [
                    {
                        "id": "database_schema",
                        "label": "Esquema do Banco de Dados",
                        "type": "textarea",
                        "required": False,
                        "placeholder": "Descreva o esquema do banco de dados"
                    },
                    {
                        "id": "migrations",
                        "label": "Migrações",
                        "type": "textarea",
                        "required": False,
                        "placeholder": "Informações sobre migrações de banco de dados"
                    }
                ]
            }
        },
        "frontend": {
            # Campos específicos para frontend
            "ui_components": {
                "title": "Componentes de UI",
                "fields": [
                    {
                        "id": "ui_library",
                        "label": "Biblioteca de UI",
                        "type": "text",
                        "required": False,
                        "placeholder": "Ex: React Bootstrap, Material UI"
                    },
                    {
                        "id": "component_structure",
                        "label": "Estrutura de Componentes",
                        "type": "textarea",
                        "required": False,
                        "placeholder": "Descreva a estrutura de componentes"
                    }
                ]
            },
            "state_management": {
                "title": "Gerenciamento de Estado",
                "fields": [
                    {
                        "id": "state_solution",
                        "label": "Solução de Gerenciamento de Estado",
                        "type": "text",
                        "required": False,
                        "placeholder": "Ex: Redux, Context API, MobX"
                    },
                    {
                        "id": "state_description",
                        "label": "Descrição da Arquitetura de Estado",
                        "type": "textarea",
                        "required": False,
                        "placeholder": "Detalhes sobre a implementação do estado"
                    }
                ]
            },
            "design": {
                "title": "Design e Estilo",
                "fields": [
                    {
                        "id": "design_system",
                        "label": "Sistema de Design",
                        "type": "text",
                        "required": False,
                        "placeholder": "Ex: Design System personalizado, Tailwind"
                    },
                    {
                        "id": "responsive_approach",
                        "label": "Abordagem Responsiva",
                        "type": "textarea",
                        "required": False,
                        "placeholder": "Descreva a abordagem para responsividade"
                    }
                ]
            }
        },
        "fullstack": {
            # Mescla campos de backend e frontend com adições específicas
            "architecture": {
                "title": "Arquitetura da Aplicação",
                "fields": [
                    {
                        "id": "frontend_backend_communication",
                        "label": "Comunicação Frontend-Backend",
                        "type": "textarea",
                        "required": True,
                        "placeholder": "Descreva como o frontend se comunica com o backend"
                    },
                    {
                        "id": "deployment_architecture",
                        "label": "Arquitetura de Implantação",
                        "type": "textarea",
                        "required": False,
                        "placeholder": "Descreva a arquitetura de implantação"
                    }
                ]
            }
        },
        "mobile": {
            # Campos específicos para desenvolvimento mobile
            "platforms": {
                "title": "Plataformas Suportadas",
                "fields": [
                    {
                        "id": "platform_list",
                        "label": "Plataformas",
                        "type": "checkbox",
                        "options": ["Android", "iOS", "Web", "Outros"],
                        "required": True
                    },
                    {
                        "id": "min_versions",
                        "label": "Versões Mínimas",
                        "type": "textarea",
                        "required": False,
                        "placeholder": "Ex: Android 8.0+, iOS 13+"
                    }
                ]
            },
            "app_stores": {
                "title": "Informações de App Store",
                "fields": [
                    {
                        "id": "app_store_links",
                        "label": "Links de App Store",
                        "type": "textarea",
                        "required": False,
                        "placeholder": "Links para Google Play, App Store, etc."
                    },
                    {
                        "id": "release_process",
                        "label": "Processo de Release",
                        "type": "textarea",
                        "required": False,
                        "placeholder": "Descreva o processo de lançamento nas lojas"
                    }
                ]
            }
        },
        "cybersec": {
            # Campos específicos para cybersegurança
            "security_features": {
                "title": "Recursos de Segurança",
                "fields": [
                    {
                        "id": "security_measures",
                        "label": "Medidas de Segurança",
                        "type": "textarea",
                        "required": True,
                        "placeholder": "Descreva as medidas de segurança implementadas"
                    },
                    {
                        "id": "threat_model",
                        "label": "Modelo de Ameaças",
                        "type": "textarea",
                        "required": False,
                        "placeholder": "Descreva o modelo de ameaças considerado"
                    }
                ]
            },
            "compliance": {
                "title": "Conformidade",
                "fields": [
                    {
                        "id": "compliance_standards",
                        "label": "Padrões de Conformidade",
                        "type": "textarea",
                        "required": False,
                        "placeholder": "Ex: GDPR, HIPAA, PCI DSS"
                    }
                ]
            }
        },
        "network": {
            # Campos específicos para redes
            "network_topology": {
                "title": "Topologia de Rede",
                "fields": [
                    {
                        "id": "topology_description",
                        "label": "Descrição da Topologia",
                        "type": "textarea",
                        "required": True,
                        "placeholder": "Descreva a topologia da rede"
                    },
                    {
                        "id": "network_diagram",
                        "label": "URL do Diagrama de Rede (opcional)",
                        "type": "text",
                        "required": False,
                        "placeholder": "Link para diagrama da rede"
                    }
                ]
            },
            "protocols": {
                "title": "Protocolos Utilizados",
                "fields": [
                    {
                        "id": "protocol_list",
                        "label": "Lista de Protocolos",
                        "type": "textarea",
                        "required": False,
                        "placeholder": "Liste os protocolos utilizados"
                    }
                ]
            }
        },
        "frameworks": {
            # Campos específicos para frameworks
            "framework_details": {
                "title": "Detalhes do Framework",
                "fields": [
                    {
                        "id": "framework_name",
                        "label": "Nome do Framework",
                        "type": "text",
                        "required": True,
                        "placeholder": "Ex: Django, Angular, Laravel"
                    },
                    {
                        "id": "framework_version",
                        "label": "Versão do Framework",
                        "type": "text",
                        "required": True,
                        "placeholder": "Ex: 4.2.1"
                    },
                    {
                        "id": "custom_extensions",
                        "label": "Extensões Personalizadas",
                        "type": "textarea",
                        "required": False,
                        "placeholder": "Descreva extensões ou personalizações do framework"
                    }
                ]
            }
        }
    }
    
    # Mescla o template base com o específico
    if project_type in specific_templates:
        # Atualiza seções existentes ou adiciona novas
        for section_id, section_data in specific_templates[project_type].items():
            base_template[section_id] = section_data
    
    return base_template
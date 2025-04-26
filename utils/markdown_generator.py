"""
Gerador de documentação Markdown para README.md baseado nos dados do projeto.
"""

def generate_markdown(project):
    """
    Gera o markdown completo para o README.md com base nos dados do projeto.
    
    Args:
        project (dict): Dicionário com os dados do projeto
        
    Returns:
        str: Conteúdo markdown completo
    """
    sections = project.get('sections', {})
    project_name = sections.get('project_info', {}).get('name', 'Projeto')
    
    # Lista de seções na ordem desejada
    markdown_content = []
    
    # 1. Cabeçalho com Logo e Badges
    header = _generate_header(sections.get('project_info', {}))
    markdown_content.append(header)
    
    # 2. Sobre o Projeto
    about = _generate_about_section(sections.get('about', {}))
    if about:
        markdown_content.append(about)
    
    # 3. Índice - gerado automaticamente
    toc = _generate_table_of_contents(project)
    if toc:
        markdown_content.append(toc)
    
    # 4. Tecnologias
    technologies = _generate_technologies_section(sections.get('technology', {}))
    if technologies:
        markdown_content.append(technologies)
    
    # 5. Instalação
    installation = _generate_installation_section(sections.get('installation', {}))
    if installation:
        markdown_content.append(installation)
    
    # 6. Uso
    usage = _generate_usage_section(sections.get('usage', {}))
    if usage:
        markdown_content.append(usage)
    
    # 7. Estrutura do Projeto
    structure = _generate_structure_section(project.get('structure', None), 
                                           sections.get('structure', {}))
    if structure:
        markdown_content.append(structure)
    
    # 8. API e Endpoints (se aplicável)
    api = _generate_api_section(sections.get('api', {}))
    if api:
        markdown_content.append(api)
    
    # Gerar seções específicas por tipo de projeto
    specific_sections = _generate_specific_sections(project.get('type', ''), sections)
    if specific_sections:
        markdown_content.extend(specific_sections)
    
    # 9. Roadmap
    roadmap = _generate_roadmap_section(sections.get('roadmap', {}))
    if roadmap:
        markdown_content.append(roadmap)
    
    # 10. Contribuição
    contributing = _generate_contributing_section(sections.get('contributing', {}))
    if contributing:
        markdown_content.append(contributing)
    
    # 11. Licença
    license_section = _generate_license_section(sections.get('license', {}))
    if license_section:
        markdown_content.append(license_section)
    
    # 12. Contato
    contact = _generate_contact_section(sections.get('contact', {}))
    if contact:
        markdown_content.append(contact)
    
    # 13. FAQ
    faq = _generate_faq_section(sections.get('faq', {}))
    if faq:
        markdown_content.append(faq)
    
    # 14. Agradecimentos
    acknowledgements = _generate_acknowledgements_section(sections.get('acknowledgements', {}))
    if acknowledgements:
        markdown_content.append(acknowledgements)
    
    # 15. Equipe
    team = _generate_team_section(sections.get('team', {}))
    if team:
        markdown_content.append(team)
    
    # Adicionar botão "Voltar ao topo"
    markdown_content.append("\n\n<p align=\"right\">(<a href=\"#top\">Voltar ao topo ⬆️</a>)</p>")
    
    # Junta todas as seções em um único documento markdown
    return "\n\n".join(markdown_content)

def _generate_header(project_info):
    """Gera o cabeçalho com logo e badges"""
    name = project_info.get('name', 'Projeto')
    logo_url = project_info.get('logo_url', '')
    short_description = project_info.get('short_description', '')
    
    header = []
    
    # Adicionar uma tag <a id="top"></a> para o link "voltar ao topo"
    header.append('<a id="top"></a>')
    
    # Logo (se disponível)
    if logo_url:
        header.append(f"<div align=\"center\">\n  <img src=\"{logo_url}\" alt=\"{name} Logo\" width=\"200\">\n</div>")
    
    # Nome do projeto
    header.append(f"# {name}")
    
    # Descrição curta
    if short_description:
        header.append(f"> {short_description}")
    
    # Badges (exemplos - seria personalizado com base no projeto real)
    header.append("""
<p align="center">
  <a href="https://github.com/username/repo/stargazers"><img src="https://img.shields.io/github/stars/username/repo" alt="Stars Badge"/></a>
  <a href="https://github.com/username/repo/network/members"><img src="https://img.shields.io/github/forks/username/repo" alt="Forks Badge"/></a>
  <a href="https://github.com/username/repo/pulls"><img src="https://img.shields.io/github/issues-pr/username/repo" alt="Pull Requests Badge"/></a>
  <a href="https://github.com/username/repo/issues"><img src="https://img.shields.io/github/issues/username/repo" alt="Issues Badge"/></a>
  <a href="https://github.com/username/repo/blob/master/LICENSE"><img src="https://img.shields.io/github/license/username/repo" alt="License Badge"/></a>
</p>
""")
    
    return "\n".join(header)

def _generate_about_section(about_data):
    """Gera a seção 'Sobre o Projeto'"""
    if not about_data:
        return ""
        
    description = about_data.get('description', '')
    motivation = about_data.get('motivation', '')
    key_features = about_data.get('key_features', '')
    
    about = ["## 📋 Sobre o Projeto"]
    
    if description:
        about.append(description)
    
    if motivation:
        about.append("\n### Motivação\n")
        about.append(motivation)
    
    if key_features:
        about.append("\n### Principais Diferenciais\n")
        features_list = key_features.strip().split('\n')
        for feature in features_list:
            if feature.strip():
                about.append(f"- {feature.strip()}")
    
    return "\n".join(about)

def _generate_table_of_contents(project):
    """Gera o índice automático"""
    sections = project.get('sections', {})
    
    toc = ["## 📑 Índice\n"]
    
    # Lista padrão de seções para incluir no índice
    toc_sections = [
        ("about", "Sobre o Projeto"),
        ("technology", "Tecnologias Utilizadas"),
        ("installation", "Instalação e Configuração"),
        ("usage", "Como Utilizar"),
        ("structure", "Estrutura do Projeto"),
        ("api", "API e Endpoints"),
        ("roadmap", "Roadmap"),
        ("contributing", "Contribuição"),
        ("license", "Licença"),
        ("contact", "Contato e Suporte"),
        ("faq", "FAQ"),
        ("team", "Equipe"),
        ("acknowledgements", "Agradecimentos"),
    ]
    
    # Adicionar apenas as seções que existem no projeto
    for section_id, section_title in toc_sections:
        if section_id in sections and sections.get(section_id):
            toc.append(f"- [📍 {section_title}](#{section_id.lower()})")
    
    return "\n".join(toc)

def _generate_technologies_section(tech_data):
    """Gera a seção de tecnologias utilizadas"""
    if not tech_data:
        return ""
        
    technologies = tech_data.get('technologies', '')
    architecture = tech_data.get('architecture', '')
    
    tech_section = ["## 🔧 Tecnologias Utilizadas\n"]
    
    if technologies:
        tech_list = technologies.strip().split(',')
        tech_badges = []
        
        # Aqui podemos mapear tecnologias para badges/ícones
        badge_mapping = {
            "python": "https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white",
            "flask": "https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white",
            "react": "https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB",
            "javascript": "https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black",
            "typescript": "https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white",
            "node.js": "https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white",
            "django": "https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white",
            "mongodb": "https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white",
            "mysql": "https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white",
            "postgresql": "https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white",
            "docker": "https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white",
            "kubernetes": "https://img.shields.io/badge/Kubernetes-326DE6?style=for-the-badge&logo=kubernetes&logoColor=white",
            "aws": "https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white",
            "gcp": "https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white",
            "azure": "https://img.shields.io/badge/Microsoft_Azure-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white",
            "html": "https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white",
            "css": "https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white",
            "sass": "https://img.shields.io/badge/Sass-CC6699?style=for-the-badge&logo=sass&logoColor=white",
            "redux": "https://img.shields.io/badge/Redux-593D88?style=for-the-badge&logo=redux&logoColor=white",
            "vue": "https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D",
            "angular": "https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white",
            "tailwind": "https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white",
            "bootstrap": "https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white",
            "graphql": "https://img.shields.io/badge/GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white",
            "rust": "https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white",
            "go": "https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white",
            "c++": "https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white",
            "java": "https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=java&logoColor=white",
            "c#": "https://img.shields.io/badge/C%23-239120?style=for-the-badge&logo=c-sharp&logoColor=white",
            "php": "https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white",
            "swift": "https://img.shields.io/badge/Swift-FA7343?style=for-the-badge&logo=swift&logoColor=white",
            "kotlin": "https://img.shields.io/badge/Kotlin-0095D5?style=for-the-badge&logo=kotlin&logoColor=white",
            "flutter": "https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white",
            "react native": "https://img.shields.io/badge/React_Native-20232A?style=for-the-badge&logo=react&logoColor=61DAFB",
        }
        
        for tech in tech_list:
            tech_name = tech.strip().lower()
            if tech_name in badge_mapping:
                tech_badges.append(f"<img src=\"{badge_mapping[tech_name]}\" alt=\"{tech.strip()}\">")
            else:
                tech_badges.append(f"**{tech.strip()}**")
        
        tech_section.append("<p align=\"center\">")
        tech_section.append("  " + " ".join(tech_badges))
        tech_section.append("</p>\n")
    
    if architecture:
        tech_section.append("### Arquitetura\n")
        tech_section.append(architecture)
    
    return "\n".join(tech_section)

def _generate_installation_section(installation_data):
    """Gera a seção de instalação e configuração"""
    if not installation_data:
        return ""
        
    prerequisites = installation_data.get('prerequisites', '')
    installation_steps = installation_data.get('installation_steps', '')
    env_variables = installation_data.get('env_variables', '')
    
    installation = ["## 🚀 Instalação e Configuração\n"]
    
    if prerequisites:
        installation.append("### Pré-requisitos\n")
        prerequisites_list = prerequisites.strip().split('\n')
        for req in prerequisites_list:
            if req.strip():
                installation.append(f"- {req.strip()}")
        installation.append("")
    
    if installation_steps:
        installation.append("### Passos para Instalação\n")
        installation.append("```bash")
        installation.append(installation_steps)
        installation.append("```\n")
    
    if env_variables:
        installation.append("### Variáveis de Ambiente\n")
        installation.append("Crie um arquivo `.env` na raiz do projeto com as seguintes variáveis:\n")
        installation.append("```env")
        installation.append(env_variables)
        installation.append("```")
    
    return "\n".join(installation)

def _generate_usage_section(usage_data):
    """Gera a seção de como utilizar o projeto"""
    if not usage_data:
        return ""
        
    usage_instructions = usage_data.get('usage_instructions', '')
    examples = usage_data.get('examples', '')
    commands = usage_data.get('commands', '')
    
    usage = ["## 📘 Como Utilizar\n"]
    
    if usage_instructions:
        usage.append(usage_instructions)
        usage.append("")
    
    if examples:
        usage.append("### Exemplos\n")
        usage.append("```")
        usage.append(examples)
        usage.append("```\n")
    
    if commands:
        usage.append("### Comandos Principais\n")
        commands_list = commands.strip().split('\n')
        
        # Formatação em tabela para comandos
        usage.append("| Comando | Descrição |")
        usage.append("| ------- | --------- |")
        
        for cmd in commands_list:
            if ':' in cmd:
                cmd_parts = cmd.split(':', 1)
                usage.append(f"| `{cmd_parts[0].strip()}` | {cmd_parts[1].strip()} |")
            elif cmd.strip():
                usage.append(f"| `{cmd.strip()}` | - |")
    
    return "\n".join(usage)

def _generate_structure_section(structure_data, structure_section):
    """Gera a seção de estrutura do projeto"""
    if not structure_data and not structure_section.get('manual_structure', ''):
        return ""
    
    structure = ["## 📁 Estrutura do Projeto\n"]
    
    # Se temos dados analisados automaticamente
    if structure_data:
        structure.append("```")
        structure.append(structure_data)
        structure.append("```")
    # Senão, usamos a estrutura manual informada pelo usuário
    elif structure_section.get('manual_structure', ''):
        structure.append("```")
        structure.append(structure_section.get('manual_structure', ''))
        structure.append("```")
    
    return "\n".join(structure)

def _generate_api_section(api_data):
    """Gera a seção de API e endpoints"""
    if not api_data or api_data.get('has_api') != 'Sim':
        return ""
        
    api_documentation = api_data.get('api_documentation', '')
    
    api = ["## 🔌 API e Endpoints\n"]
    
    if api_documentation:
        api.append(api_documentation)
    
    return "\n".join(api)

def _generate_specific_sections(project_type, sections):
    """Gera seções específicas baseadas no tipo de projeto"""
    specific_sections = []
    
    if project_type == "backend" and "database" in sections:
        db_section = ["## 💾 Banco de Dados\n"]
        
        database_schema = sections.get('database', {}).get('database_schema', '')
        migrations = sections.get('database', {}).get('migrations', '')
        
        if database_schema:
            db_section.append("### Esquema do Banco de Dados\n")
            db_section.append(database_schema)
            db_section.append("")
        
        if migrations:
            db_section.append("### Migrações\n")
            db_section.append(migrations)
        
        if len(db_section) > 1:  # Se adicionamos mais que o título
            specific_sections.append("\n".join(db_section))
    
    elif project_type == "frontend":
        # Componentes UI
        if "ui_components" in sections:
            ui_section = ["## 🎨 Componentes de UI\n"]
            
            ui_library = sections.get('ui_components', {}).get('ui_library', '')
            component_structure = sections.get('ui_components', {}).get('component_structure', '')
            
            if ui_library:
                ui_section.append(f"Este projeto utiliza **{ui_library}** para seus componentes de UI.\n")
            
            if component_structure:
                ui_section.append("### Estrutura de Componentes\n")
                ui_section.append(component_structure)
            
            if len(ui_section) > 1:
                specific_sections.append("\n".join(ui_section))
        
        # Gerenciamento de Estado
        if "state_management" in sections:
            state_section = ["## 🔄 Gerenciamento de Estado\n"]
            
            state_solution = sections.get('state_management', {}).get('state_solution', '')
            state_description = sections.get('state_management', {}).get('state_description', '')
            
            if state_solution:
                state_section.append(f"Este projeto utiliza **{state_solution}** para gerenciamento de estado.\n")
            
            if state_description:
                state_section.append("### Implementação do Estado\n")
                state_section.append(state_description)
            
            if len(state_section) > 1:
                specific_sections.append("\n".join(state_section))
    
    elif project_type == "mobile":
        # Plataformas
        if "platforms" in sections:
            platforms_section = ["## 📱 Plataformas Suportadas\n"]
            
            platform_list = sections.get('platforms', {}).get('platform_list', [])
            min_versions = sections.get('platforms', {}).get('min_versions', '')
            
            if platform_list:
                if isinstance(platform_list, str):
                    platform_list = [platform_list]
                platforms_section.append(", ".join(platform_list))
                platforms_section.append("")
            
            if min_versions:
                platforms_section.append("### Versões Mínimas Suportadas\n")
                platforms_section.append(min_versions)
            
            if len(platforms_section) > 1:
                specific_sections.append("\n".join(platforms_section))
    
    # Adicione mais seções específicas para outros tipos de projeto aqui
    
    return specific_sections

def _generate_roadmap_section(roadmap_data):
    """Gera a seção de roadmap"""
    if not roadmap_data:
        return ""
        
    future_features = roadmap_data.get('future_features', '')
    known_issues = roadmap_data.get('known_issues', '')
    
    roadmap = ["## 🛣️ Roadmap\n"]
    
    if future_features:
        roadmap.append("### Funcionalidades Futuras\n")
        features_list = future_features.strip().split('\n')
        for feature in features_list:
            if feature.strip():
                roadmap.append(f"- [ ] {feature.strip()}")
        roadmap.append("")
    
    if known_issues:
        roadmap.append("### Problemas Conhecidos\n")
        issues_list = known_issues.strip().split('\n')
        for issue in issues_list:
            if issue.strip():
                roadmap.append(f"- {issue.strip()}")
    
    return "\n".join(roadmap)

def _generate_contributing_section(contributing_data):
    """Gera a seção de contribuição"""
    if not contributing_data:
        return ""
        
    contribution_guidelines = contributing_data.get('contribution_guidelines', '')
    code_of_conduct = contributing_data.get('code_of_conduct', '')
    
    contributing = ["## 👥 Contribuição\n"]
    
    if contribution_guidelines:
        contributing.append(contribution_guidelines)
        contributing.append("")
    else:
        # Diretrizes padrão
        contributing.append("""
Contribuições são o que fazem a comunidade open source um lugar incrível para aprender, inspirar e criar. Qualquer contribuição que você fizer será **muito apreciada**.

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Faça commit das suas alterações (`git commit -m 'Add some AmazingFeature'`)
4. Faça Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request
""")
    
    if code_of_conduct:
        contributing.append("### Código de Conduta\n")
        contributing.append(code_of_conduct)
    
    return "\n".join(contributing)

def _generate_license_section(license_data):
    """Gera a seção de licença"""
    if not license_data:
        return ""
        
    license_type = license_data.get('license_type', '')
    custom_license = license_data.get('custom_license', '')
    
    license_section = ["## 📜 Licença\n"]
    
    if license_type == 'Outra' and custom_license:
        license_section.append(custom_license)
    elif license_type and license_type != 'Nenhuma':
        license_section.append(f"Este projeto está licenciado sob a licença {license_type} - veja o arquivo [LICENSE](LICENSE) para detalhes.")
    else:
        license_section.append("Este projeto ainda não possui uma licença definida.")
    
    return "\n".join(license_section)

def _generate_contact_section(contact_data):
    """Gera a seção de contato e suporte"""
    if not contact_data:
        return ""
        
    contact_info = contact_data.get('contact_info', '')
    support_channels = contact_data.get('support_channels', '')
    
    contact = ["## 📞 Contato e Suporte\n"]
    
    if contact_info:
        contact.append(contact_info)
        contact.append("")
    
    if support_channels:
        contact.append("### Canais de Suporte\n")
        channels_list = support_channels.strip().split('\n')
        for channel in channels_list:
            if channel.strip():
                contact.append(f"- {channel.strip()}")
    
    return "\n".join(contact)

def _generate_faq_section(faq_data):
    """Gera a seção de perguntas frequentes"""
    if not faq_data:
        return ""
        
    faq_items = faq_data.get('faq_items', '')
    
    if not faq_items:
        return ""
    
    faq = ["## ❓ FAQ\n"]
    
    # Processa as perguntas no formato "P: pergunta / R: resposta"
    items = faq_items.split('\n')
    current_question = None
    
    for item in items:
        item = item.strip()
        if item.startswith('P:') or item.startswith('Q:'):
            if current_question:
                faq.append('')  # Espaço entre perguntas
            question = item[2:].strip()
            faq.append(f"### {question}")
            current_question = question
        elif item.startswith('R:') or item.startswith('A:'):
            if current_question:
                answer = item[2:].strip()
                faq.append(answer)
    
    return "\n".join(faq)

def _generate_acknowledgements_section(acknowledgements_data):
    """Gera a seção de agradecimentos"""
    if not acknowledgements_data:
        return ""
        
    acknowledgements = acknowledgements_data.get('acknowledgements', '')
    
    if not acknowledgements:
        return ""
    
    ack_section = ["## 🙏 Agradecimentos\n"]
    
    ack_list = acknowledgements.strip().split('\n')
    for ack in ack_list:
        if ack.strip():
            ack_section.append(f"* {ack.strip()}")
    
    return "\n".join(ack_section)

def _generate_team_section(team_data):
    """Gera a seção de equipe"""
    if not team_data:
        return ""
        
    team_members = team_data.get('team_members', '')
    
    if not team_members:
        return ""
    
    team_section = ["## 👨‍💻 Equipe\n"]
    
    members = team_members.strip().split('\n')
    for member in members:
        if member.strip():
            # Se estiver no formato "Nome - Função"
            if ' - ' in member:
                name, role = member.split(' - ', 1)
                team_section.append(f"* **{name.strip()}** - {role.strip()}")
            else:
                team_section.append(f"* **{member.strip()}**")
    
    return "\n".join(team_section)
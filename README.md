# DocGen - Sistema de Geração de Documentação Profissional

<div align="center">
  <img src="static/img/logo.png" alt="DocGen Logo" width="200">
</div>

> Sistema web para geração de documentações profissionais em formato Markdown (README.md) para repositórios GitHub.

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Flask-2.3.3-000000?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
  <img src="https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black" alt="JavaScript">
  <img src="https://img.shields.io/badge/CSS3-Modern-1572B6?style=for-the-badge&logo=css3&logoColor=white" alt="CSS3">
</p>

## 📋 Sobre o Projeto

O DocGen é um sistema web desenvolvido em Python/Flask que permite criar documentações profissionais para repositórios GitHub com facilidade. O sistema possui uma interface elegante e dividida, permitindo que o usuário preencha informações sobre seu projeto através de perguntas guiadas, enquanto visualiza em tempo real a documentação sendo gerada.

### Principais Diferenciais

- Interface intuitiva com editor e visualizador lado a lado
- Geração automatizada baseada em tipos de projeto
- Design futurista com animações fluidas
- Personalização visual com temas e estilos
- Análise automática de estrutura de projeto
- Exportação em Markdown de alta qualidade

## 📑 Índice

- [📍 Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [📍 Instalação e Configuração](#-instalação-e-configuração)
- [📍 Como Utilizar](#-como-utilizar)
- [📍 Estrutura do Projeto](#-estrutura-do-projeto)
- [📍 Principais Funcionalidades](#-principais-funcionalidades)
- [📍 Contribuição](#-contribuição)
- [📍 Roadmap](#-roadmap)
- [📍 Licença](#-licença)

## 🔧 Tecnologias Utilizadas

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img src="https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white">
  <img src="https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black">
  <img src="https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white">
  <img src="https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white">
  <img src="https://img.shields.io/badge/Markdown-000000?style=for-the-badge&logo=markdown&logoColor=white">
</p>

### Arquitetura

O sistema utiliza uma arquitetura MVC (Model-View-Controller) com Flask, onde:
- **Model**: Classes que representam a estrutura de dados do projeto
- **View**: Templates Jinja2 para renderização da interface
- **Controller**: Rotas Flask para manipulação de requisições

## 🚀 Instalação e Configuração

### Pré-requisitos

- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)
- Ambiente virtual (recomendado)

### Passos para Instalação

```bash
# Clone o repositório
git clone https://github.com/yourusername/docgen.git
cd docgen

# Crie um ambiente virtual
python -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# Execute a aplicação
python app.py
```

## 📘 Como Utilizar

1. Acesse a aplicação no navegador (por padrão em http://localhost:5000)
2. Selecione o tipo de projeto que você está documentando
3. Preencha os campos com as informações do seu projeto
4. Visualize em tempo real a documentação gerada
5. Personalize o tema e o estilo conforme necessário
6. Exporte o README.md finalizado

O sistema irá guiá-lo através de diferentes seções para construir uma documentação completa e profissional para seu projeto.

## 📁 Estrutura do Projeto

```
docgen/
│
├── app.py                  # Aplicação Flask principal
├── config.py               # Configurações do projeto
├── requirements.txt        # Dependências do projeto
│
├── static/                 # Arquivos estáticos
│   ├── css/
│   │   ├── main.css        # Estilos principais
│   │   ├── themes.css      # Temas de cores personalizáveis
│   │   └── animations.css  # Animações CSS
│   │
│   ├── js/
│   │   ├── main.js         # JavaScript principal
│   │   ├── editor.js       # Funcionalidade do editor
│   │   ├── preview.js      # Preview em tempo real
│   │   ├── analyzer.js     # Análise de estrutura de projetos
│   │   └── templates.js    # Templates por tipo de projeto
│   │
│   ├── img/                # Imagens e ícones
│   │   ├── logos/          # Logos de tecnologias
│   │   └── badges/         # Badges para README
│   │
│   └── vendor/             # Bibliotecas de terceiros
│       ├── marked.min.js   # Parser Markdown
│       └── highlight.js    # Destacador de sintaxe
│
├── templates/              # Templates HTML
│   ├── base.html           # Template base
│   ├── index.html          # Página inicial
│   ├── editor.html         # Interface principal
│   └── components/         # Componentes reutilizáveis
│       ├── project_type.html     # Seleção de tipo de projeto
│       ├── section_forms.html    # Formulários por seção
│       └── preview_panel.html    # Painel de preview
│
├── utils/                  # Utilitários
│   ├── __init__.py
│   ├── markdown_generator.py    # Gerador de Markdown
│   ├── file_analyzer.py         # Analisador de estrutura
│   └── template_manager.py      # Gerenciamento de templates
│
└── models/                 # Modelos de dados
    ├── __init__.py
    ├── project.py          # Modelo de Projeto
    └── section.py          # Modelo de Seções da documentação
```

## ✨ Principais Funcionalidades

### Interface de Edição e Visualização em Tempo Real

O DocGen oferece uma interface dividida onde você edita suas informações à esquerda e vê o resultado em tempo real à direita. Isso permite um ajuste preciso e imediato da documentação.

### Temas e Personalização Visual

O sistema inclui diversos temas visuais que podem ser alterados instantaneamente:
- **Padrão**: Esquema de cores azul e branco
- **Escuro**: Modo noturno com alto contraste
- **Claro**: Interface limpa e minimalista
- **Azul**: Tons predominantes de azul
- **Verde**: Tons predominantes de verde

### Análise Automática de Estrutura

O DocGen pode analisar arquivos .zip ou .tar.gz com a estrutura do seu projeto e automaticamente gerar uma representação visual em árvore de diretórios para a documentação.

### Templates por Tipo de Projeto

Cada tipo de projeto (Backend, Frontend, Full Stack, etc.) tem um template específico com campos e seções relevantes para aquele tipo de desenvolvimento, tornando sua documentação mais precisa e útil.

## 👥 Contribuição

Contribuições são bem-vindas! Se você quiser contribuir para este projeto:

1. Faça um Fork do projeto
2. Crie uma Branch para sua Feature (`git checkout -b feature/AmazingFeature`)
3. Faça commit das suas alterações (`git commit -m 'Add some AmazingFeature'`)
4. Faça Push para a Branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 🛣️ Roadmap

### Funcionalidades Futuras

- [ ] Integração direta com a API do GitHub
- [ ] Sistema de templates personalizados
- [ ] Sugestões automáticas baseadas em IA
- [ ] Exportação para outros formatos além de Markdown
- [ ] Sistema de histórico de documentações

## 📜 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📞 Contato e Suporte

Para dúvidas, sugestões ou suporte:
- Abra uma issue no GitHub
- Entre em contato pelo email: exemplo@docgen.com

<p align="right"><a href="#top">Voltar ao topo ⬆️</a></p>
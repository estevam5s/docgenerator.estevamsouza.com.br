/**
 * DocGen - Preview em Tempo Real
 * Funções relacionadas ao preview do markdown
 */

// Configurações do Marked.js
function configureMarked() {
  if (!window.marked) return;
  
  // Define opções do Marked
  marked.setOptions({
      renderer: new marked.Renderer(),
      highlight: function(code, lang) {
          if (window.hljs) {
              const language = hljs.getLanguage(lang) ? lang : 'plaintext';
              return hljs.highlight(code, { language }).value;
          }
          return code;
      },
      langPrefix: 'hljs language-',
      pedantic: false,
      gfm: true,
      breaks: false,
      sanitize: false,
      smartypants: false,
      xhtml: false
  });
  
  // Customiza o renderer para adicionar classes e atributos
  const renderer = new marked.Renderer();
  
  // Customiza tabelas para serem responsivas
  renderer.table = function(header, body) {
      return '<div class="table-responsive">\n' +
             '<table class="table">\n' +
             '<thead>\n' +
             header +
             '</thead>\n' +
             '<tbody>\n' +
             body +
             '</tbody>\n' +
             '</table>\n' +
             '</div>\n';
  };
  
  // Customiza links para abrir em nova aba se for externo
  renderer.link = function(href, title, text) {
      const isExternal = href && href.startsWith('http');
      const target = isExternal ? ' target="_blank" rel="noopener noreferrer"' : '';
      title = title ? ` title="${title}"` : '';
      return `<a href="${href}"${title}${target}>${text}</a>`;
  };
  
  // Customiza imagens para serem responsivas
  renderer.image = function(href, title, text) {
      return `<img src="${href}" alt="${text}" title="${title || text}" class="img-fluid">`;
  };
  
  marked.setOptions({ renderer });
}

// Inicializa o preview
document.addEventListener('DOMContentLoaded', function() {
  configureMarked();
  
  // Verifica se há um preview para atualizar
  if (document.getElementById('markdown-preview')) {
      updatePreview();
  }
});

/**
* Processa badges de tecnologias no preview
* Substitui nomes de tecnologias por badges
*/
function processTechBadges() {
  const preview = document.getElementById('markdown-preview');
  if (!preview) return;
  
  // Mapeamento de tecnologias para badges
  const techBadges = {
      'python': 'https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white',
      'javascript': 'https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black',
      'typescript': 'https://img.shields.io/badge/TypeScript-007ACC?style=for-the-badge&logo=typescript&logoColor=white',
      'react': 'https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB',
      'angular': 'https://img.shields.io/badge/Angular-DD0031?style=for-the-badge&logo=angular&logoColor=white',
      'vue': 'https://img.shields.io/badge/Vue.js-35495E?style=for-the-badge&logo=vue.js&logoColor=4FC08D',
      'node.js': 'https://img.shields.io/badge/Node.js-43853D?style=for-the-badge&logo=node.js&logoColor=white',
      'django': 'https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white',
      'flask': 'https://img.shields.io/badge/Flask-000000?style=for-the-badge&logo=flask&logoColor=white',
      'express': 'https://img.shields.io/badge/Express.js-404D59?style=for-the-badge&logo=express&logoColor=white',
      'mongodb': 'https://img.shields.io/badge/MongoDB-4EA94B?style=for-the-badge&logo=mongodb&logoColor=white',
      'mysql': 'https://img.shields.io/badge/MySQL-00000F?style=for-the-badge&logo=mysql&logoColor=white',
      'postgresql': 'https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white',
      'sqlite': 'https://img.shields.io/badge/SQLite-07405E?style=for-the-badge&logo=sqlite&logoColor=white',
      'html': 'https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white',
      'css': 'https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white',
      'bootstrap': 'https://img.shields.io/badge/Bootstrap-563D7C?style=for-the-badge&logo=bootstrap&logoColor=white',
      'tailwind': 'https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white',
      'jquery': 'https://img.shields.io/badge/jQuery-0769AD?style=for-the-badge&logo=jquery&logoColor=white',
      'rust': 'https://img.shields.io/badge/Rust-000000?style=for-the-badge&logo=rust&logoColor=white',
      'dart': 'https://img.shields.io/badge/Dart-0175C2?style=for-the-badge&logo=dart&logoColor=white',
      'flutter': 'https://img.shields.io/badge/Flutter-02569B?style=for-the-badge&logo=flutter&logoColor=white',
      'go': 'https://img.shields.io/badge/Go-00ADD8?style=for-the-badge&logo=go&logoColor=white',
      'c': 'https://img.shields.io/badge/C-00599C?style=for-the-badge&logo=c&logoColor=white',
      'c++': 'https://img.shields.io/badge/C%2B%2B-00599C?style=for-the-badge&logo=c%2B%2B&logoColor=white',
      'c#': 'https://img.shields.io/badge/C%23-239120?style=for-the-badge&logo=c-sharp&logoColor=white',
      'java': 'https://img.shields.io/badge/Java-ED8B00?style=for-the-badge&logo=java&logoColor=white',
      'php': 'https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white',
      'kotlin': 'https://img.shields.io/badge/Kotlin-0095D5?style=for-the-badge&logo=kotlin&logoColor=white',
      'swift': 'https://img.shields.io/badge/Swift-FA7343?style=for-the-badge&logo=swift&logoColor=white',
      'r': 'https://img.shields.io/badge/R-276DC3?style=for-the-badge&logo=r&logoColor=white',
      'ruby': 'https://img.shields.io/badge/Ruby-CC342D?style=for-the-badge&logo=ruby&logoColor=white',
      'scala': 'https://img.shields.io/badge/Scala-DC322F?style=for-the-badge&logo=scala&logoColor=white',
      'perl': 'https://img.shields.io/badge/Perl-39457E?style=for-the-badge&logo=perl&logoColor=white',
      'elixir': 'https://img.shields.io/badge/Elixir-4B275F?style=for-the-badge&logo=elixir&logoColor=white',
      'docker': 'https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white',
      'kubernetes': 'https://img.shields.io/badge/Kubernetes-326DE6?style=for-the-badge&logo=kubernetes&logoColor=white',
      'aws': 'https://img.shields.io/badge/AWS-232F3E?style=for-the-badge&logo=amazon-aws&logoColor=white',
        'azure': 'https://img.shields.io/badge/Azure-0089D6?style=for-the-badge&logo=microsoft-azure&logoColor=white',
        'gcp': 'https://img.shields.io/badge/Google_Cloud-4285F4?style=for-the-badge&logo=google-cloud&logoColor=white',
        'heroku': 'https://img.shields.io/badge/Heroku-430098?style=for-the-badge&logo=heroku&logoColor=white',
        'vercel': 'https://img.shields.io/badge/Vercel-000000?style=for-the-badge&logo=vercel&logoColor=white',
        'firebase': 'https://img.shields.io/badge/Firebase-FFCA28?style=for-the-badge&logo=firebase&logoColor=black',
        'git': 'https://img.shields.io/badge/Git-F05032?style=for-the-badge&logo=git&logoColor=white',
        'github': 'https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white',
        'gitlab': 'https://img.shields.io/badge/GitLab-FCA121?style=for-the-badge&logo=gitlab&logoColor=white',
        'bitbucket': 'https://img.shields.io/badge/Bitbucket-0052CC?style=for-the-badge&logo=bitbucket&logoColor=white',
        'jenkins': 'https://img.shields.io/badge/Jenkins-D24939?style=for-the-badge&logo=jenkins&logoColor=white',
        'travis': 'https://img.shields.io/badge/Travis_CI-3EAAAF?style=for-the-badge&logo=travis-ci&logoColor=white',
        'circleci': 'https://img.shields.io/badge/CircleCI-343434?style=for-the-badge&logo=circleci&logoColor=white',
        'nginx': 'https://img.shields.io/badge/Nginx-269539?style=for-the-badge&logo=nginx&logoColor=white',
        'apache': 'https://img.shields.io/badge/Apache-D22128?style=for-the-badge&logo=apache&logoColor=white',
        'graphql': 'https://img.shields.io/badge/GraphQL-E10098?style=for-the-badge&logo=graphql&logoColor=white',
        'redux': 'https://img.shields.io/badge/Redux-593D88?style=for-the-badge&logo=redux&logoColor=white',
        'sass': 'https://img.shields.io/badge/Sass-CC6699?style=for-the-badge&logo=sass&logoColor=white',
        'webpack': 'https://img.shields.io/badge/Webpack-8DD6F9?style=for-the-badge&logo=webpack&logoColor=black',
        'vite': 'https://img.shields.io/badge/Vite-646CFF?style=for-the-badge&logo=vite&logoColor=white',
        'babel': 'https://img.shields.io/badge/Babel-F9DC3E?style=for-the-badge&logo=babel&logoColor=black',
        'figma': 'https://img.shields.io/badge/Figma-F24E1E?style=for-the-badge&logo=figma&logoColor=white',
        'sketch': 'https://img.shields.io/badge/Sketch-F7B500?style=for-the-badge&logo=sketch&logoColor=black',
        'xd': 'https://img.shields.io/badge/Adobe_XD-FF61F6?style=for-the-badge&logo=adobe-xd&logoColor=white',
        'photoshop': 'https://img.shields.io/badge/Photoshop-31A8FF?style=for-the-badge&logo=adobe-photoshop&logoColor=white',
        'illustrator': 'https://img.shields.io/badge/Illustrator-FF9A00?style=for-the-badge&logo=adobe-illustrator&logoColor=white'
    };
    
    // Encontrar tecnologias mencionadas no texto
    const techTags = preview.querySelectorAll('p, li, td');
    techTags.forEach(tag => {
        // Só verifica texto que pode conter listas de tecnologias
        if (!tag.textContent.includes(',') && !tag.textContent.includes('.')) return;
        
        let html = tag.innerHTML;
        
        // Verifica cada tecnologia no mapeamento
        Object.keys(techBadges).forEach(tech => {
            // Usa regex para encontrar menções da tecnologia
            const regex = new RegExp(`\\b${tech}\\b`, 'gi');
            
            // Só substitui se estiver em uma lista (com vírgulas, pipes ou bullet points)
            if (regex.test(html)) {
                const techBadge = `<img src="${techBadges[tech]}" alt="${tech}" class="tech-badge">`;
                
                // Substitui apenas em contextos de lista
                if (tag.parentElement.tagName === 'UL' || 
                    tag.parentElement.tagName === 'OL' ||
                    html.includes(',') || 
                    html.includes('|') ||
                    html.includes('•')) {
                    html = html.replace(regex, techBadge);
                }
            }
        });
        
        // Atualiza o HTML apenas se houve mudanças
        if (tag.innerHTML !== html) {
            tag.innerHTML = html;
        }
    });
}

/**
 * Processa pseudo-badges no preview
 * Transforma texto no formato [badge:texto] em badges visuais
 */
function processBadges() {
    const preview = document.getElementById('markdown-preview');
    if (!preview) return;
    
    // Define cores para diferentes tipos de badges
    const badgeColors = {
        'info': '#3b82f6',
        'success': '#10b981',
        'warning': '#f59e0b',
        'error': '#ef4444',
        'primary': '#8b5cf6',
        'secondary': '#6b7280',
        'feature': '#059669',
        'bug': '#dc2626',
        'enhancement': '#2563eb',
        'docs': '#7c3aed',
        'test': '#ea580c'
    };
    
    // Encontra todos os textos no formato [badge:texto]
    const badgeRegex = /\[badge:([\w-]+)\]/g;
    const elements = preview.querySelectorAll('p, li, h1, h2, h3, h4, h5, h6');
    
    elements.forEach(element => {
        const html = element.innerHTML;
        
        // Verifica se há badges no elemento
        if (html.includes('[badge:')) {
            // Substitui cada badge
            const newHtml = html.replace(badgeRegex, (match, badgeText) => {
                // Determina a cor com base em palavras-chave
                let badgeColor = '#6b7280'; // Cor padrão
                
                Object.keys(badgeColors).forEach(key => {
                    if (badgeText.toLowerCase().includes(key)) {
                        badgeColor = badgeColors[key];
                    }
                });
                
                // Cria o HTML do badge
                return `<span class="preview-badge" style="background-color: ${badgeColor}; color: white; padding: 3px 8px; border-radius: 12px; font-size: 0.75rem; font-weight: 500;">${badgeText}</span>`;
            });
            
            // Atualiza o HTML do elemento
            if (html !== newHtml) {
                element.innerHTML = newHtml;
            }
        }
    });
}

/**
 * Processa menções no preview
 * Transforma texto no formato @username em links estilizados
 */
function processMentions() {
    const preview = document.getElementById('markdown-preview');
    if (!preview) return;
    
    // Regex para detectar menções (@username)
    const mentionRegex = /@([a-zA-Z0-9_-]+)/g;
    
    const elements = preview.querySelectorAll('p, li');
    elements.forEach(element => {
        const html = element.innerHTML;
        
        // Verifica se há menções no elemento
        if (html.includes('@')) {
            // Substitui cada menção
            const newHtml = html.replace(mentionRegex, (match, username) => {
                return `<a href="https://github.com/${username}" class="mention" target="_blank">@${username}</a>`;
            });
            
            // Atualiza o HTML do elemento
            if (html !== newHtml) {
                element.innerHTML = newHtml;
            }
        }
    });
}

/**
 * Apriomora tabelas no preview
 */
function enhanceTables() {
    const preview = document.getElementById('markdown-preview');
    if (!preview) return;
    
    const tables = preview.querySelectorAll('table');
    tables.forEach(table => {
        // Adiciona classes para estilização
        table.classList.add('preview-table');
        
        // Adiciona container responsivo se ainda não estiver em um
        if (table.parentElement.className !== 'table-responsive') {
            const container = document.createElement('div');
            container.className = 'table-responsive';
            table.parentNode.insertBefore(container, table);
            container.appendChild(table);
        }
    });
}

/**
 * Aprimoramentos para blocos de código no preview
 */
function enhanceCodeBlocks() {
    const preview = document.getElementById('markdown-preview');
    if (!preview) return;
    
    const codeBlocks = preview.querySelectorAll('pre code');
    codeBlocks.forEach(code => {
        // Adiciona botão de copiar
        if (!code.parentElement.querySelector('.copy-code-btn')) {
            const copyBtn = document.createElement('button');
            copyBtn.className = 'copy-code-btn';
            copyBtn.innerHTML = '<span class="copy-icon">📋</span>';
            copyBtn.title = 'Copiar código';
            
            // Adiciona evento de clique
            copyBtn.addEventListener('click', function() {
                const codeText = code.textContent;
                navigator.clipboard.writeText(codeText)
                    .then(() => {
                        // Feedback visual
                        copyBtn.innerHTML = '<span class="copy-icon">✓</span>';
                        copyBtn.classList.add('copied');
                        
                        // Restaura o ícone após 2 segundos
                        setTimeout(() => {
                            copyBtn.innerHTML = '<span class="copy-icon">📋</span>';
                            copyBtn.classList.remove('copied');
                        }, 2000);
                    })
                    .catch(err => {
                        console.error('Erro ao copiar código:', err);
                    });
            });
            
            // Adiciona o botão ao elemento pre
            code.parentElement.style.position = 'relative';
            code.parentElement.appendChild(copyBtn);
        }
    });
}

/**
 * Melhorias no preview do markdown
 */
function enhancePreview() {
    // Processa badges de tecnologias
    processTechBadges();
    
    // Processa badges personalizados
    processBadges();
    
    // Processa menções
    processMentions();
    
    // Aprimora tabelas
    enhanceTables();
    
    // Aprimora blocos de código
    enhanceCodeBlocks();
}

/**
 * Observer para aplicar melhorias quando o conteúdo do preview mudar
 */
const previewObserver = new MutationObserver(function(mutations) {
    // Verifica se alguma mutação afeta o conteúdo
    const contentChanged = mutations.some(mutation => {
        return mutation.type === 'childList' || mutation.type === 'characterData';
    });
    
    if (contentChanged) {
        enhancePreview();
    }
});

// Inicia observação do preview quando o documento estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    const preview = document.getElementById('markdown-preview');
    if (preview) {
        previewObserver.observe(preview, {
            childList: true,
            subtree: true,
            characterData: true
        });
    }
});
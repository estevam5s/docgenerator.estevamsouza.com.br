/**
 * DocGen - Editor de Documentação
 * Funcionalidade do editor e interações com formulários
 */

// Constantes
const ANIMATION_DURATION = 300; // em ms
const DEBOUNCE_DELAY = 500; // em ms

// Estado do editor
let editorState = {
    currentSection: '',
    formChanged: false,
    previewVisible: window.innerWidth >= 1024,
    lastSavedData: null,
    uploading: false
};

/**
 * Inicializa o editor
 * @param {string} sectionId - ID da seção atual
 */
function initEditor(sectionId) {
    editorState.currentSection = sectionId;
    
    // Inicializa componentes
    initFormHandlers();
    initPreviewToggle();
    initTagsInput();
    initFileUpload();
    initExportModal();
    initConditionalFields();
    
    // Atualiza status das seções
    updateSectionStatus();
    
    // Marca a seção atual como ativa no menu
    highlightActiveSection();
    
    console.log('Editor inicializado na seção:', sectionId);
}

/**
 * Inicializa manipuladores de eventos para o formulário
 */
function initFormHandlers() {
    const form = document.getElementById('section-form');
    if (!form) return;
    
    // Salva quando o formulário for enviado
    form.addEventListener('submit', function(event) {
        event.preventDefault();
        saveSection();
    });
    
    // Monitoramento de mudanças em tempo real
    const formInputs = form.querySelectorAll('input, textarea, select');
    formInputs.forEach(input => {
        input.addEventListener('input', debounce(function() {
            editorState.formChanged = true;
            updatePreview();
        }, DEBOUNCE_DELAY));
        
        // Para select e checkbox
        if (input.tagName === 'SELECT' || input.type === 'checkbox' || input.type === 'radio') {
            input.addEventListener('change', debounce(function() {
                editorState.formChanged = true;
                updatePreview();
                
                // Atualiza campos condicionais se necessário
                if (document.querySelectorAll('[data-condition-field]').length > 0) {
                    updateConditionalFields();
                }
            }, DEBOUNCE_DELAY));
        }
    });
}

/**
 * Inicializa o toggle entre edição e preview em telas pequenas
 */
function initPreviewToggle() {
    const toggleButtons = document.querySelectorAll('.preview-toggle');
    const editPanel = document.querySelector('.edit-panel');
    const previewPanel = document.querySelector('.preview-panel');
    
    toggleButtons.forEach(button => {
        button.addEventListener('click', function() {
            if (window.innerWidth < 1024) {
                editorState.previewVisible = !editorState.previewVisible;
                
                if (editorState.previewVisible) {
                    editPanel.style.display = 'none';
                    previewPanel.style.display = 'block';
                    updatePreview(); // Atualiza o preview antes de mostrar
                } else {
                    editPanel.style.display = 'block';
                    previewPanel.style.display = 'none';
                }
            }
        });
    });
    
    // Configura visualização inicial em telas pequenas
    if (window.innerWidth < 1024) {
        previewPanel.style.display = editorState.previewVisible ? 'block' : 'none';
        editPanel.style.display = editorState.previewVisible ? 'none' : 'block';
    }
}

/**
 * Inicializa o input de tags
 */
function initTagsInput() {
    const tagsContainers = document.querySelectorAll('.tags-input-container');
    
    tagsContainers.forEach(container => {
        const input = container.querySelector('.tags-input');
        const hiddenInput = container.querySelector('input[type="hidden"]');
        const tagsContainer = container.querySelector('.tags-container');
        
        if (!input || !hiddenInput || !tagsContainer) return;
        
        // Inicializa com tags existentes
        const existingTags = hiddenInput.value ? hiddenInput.value.split(',') : [];
        existingTags.forEach(tag => {
            if (tag.trim()) {
                addTag(tag.trim(), tagsContainer, hiddenInput);
            }
        });
        
        // Adiciona tag ao pressionar Enter
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ',') {
                e.preventDefault();
                
                const tag = input.value.trim();
                if (tag) {
                    addTag(tag, tagsContainer, hiddenInput);
                    input.value = '';
                    updatePreview();
                }
            }
        });
        
        // Adiciona tag ao perder foco
        input.addEventListener('blur', function() {
            const tag = input.value.trim();
            if (tag) {
                addTag(tag, tagsContainer, hiddenInput);
                input.value = '';
                updatePreview();
            }
        });
    });
}

/**
 * Adiciona uma tag ao container
 * @param {string} text - Texto da tag
 * @param {HTMLElement} container - Container das tags
 * @param {HTMLInputElement} hiddenInput - Input escondido com valores
 */
function addTag(text, container, hiddenInput) {
    // Cria elemento da tag
    const tag = document.createElement('span');
    tag.className = 'tag';
    tag.innerHTML = `${text} <span class="tag-remove">&times;</span>`;
    
    // Adiciona handler para remover a tag
    tag.querySelector('.tag-remove').addEventListener('click', function() {
        tag.remove();
        updateTagsValue(container, hiddenInput);
        updatePreview();
    });
    
    // Adiciona ao container e atualiza o valor
    container.appendChild(tag);
    updateTagsValue(container, hiddenInput);
}

/**
 * Atualiza o valor do input escondido com as tags
 * @param {HTMLElement} container - Container das tags
 * @param {HTMLInputElement} hiddenInput - Input escondido com valores
 */
function updateTagsValue(container, hiddenInput) {
    const tags = Array.from(container.querySelectorAll('.tag'))
                      .map(tag => tag.textContent.trim().replace('×', '').trim());
    hiddenInput.value = tags.join(',');
}

/**
 * Inicializa o upload de arquivos para análise de estrutura
 */
function initFileUpload() {
    const fileInputs = document.querySelectorAll('input[type="file"]');
    
    fileInputs.forEach(input => {
        const fileLabel = input.nextElementSibling;
        const fileName = fileLabel.nextElementSibling;
        
        // Atualiza o nome do arquivo selecionado
        input.addEventListener('change', function() {
            if (input.files.length > 0) {
                fileName.textContent = input.files[0].name;
                
                // Só faz upload automático se for o input de estrutura do projeto
                if (input.id === 'upload_structure') {
                    uploadProjectStructure(input.files[0]);
                }
            } else {
                fileName.textContent = 'Nenhum arquivo selecionado';
            }
        });
    });
}

/**
 * Faz upload da estrutura do projeto para análise
 * @param {File} file - Arquivo a ser enviado
 */
function uploadProjectStructure(file) {
    if (editorState.uploading) return;
    
    editorState.uploading = true;
    showMessage('Analisando estrutura do projeto...', 'info');
    
    const formData = new FormData();
    formData.append('project_files', file);
    
    fetch('/upload_structure', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Atualiza o campo de estrutura manual com a estrutura analisada
            const manualStructureField = document.getElementById('manual_structure');
            if (manualStructureField) {
                manualStructureField.value = data.structure;
                showMessage('Estrutura do projeto analisada com sucesso!', 'success');
                
                // Atualiza o preview para mostrar a estrutura
                updatePreview();
            }
        } else {
            showMessage('Erro ao analisar estrutura: ' + data.error, 'error');
        }
    })
    .catch(error => {
        console.error('Erro ao fazer upload:', error);
        showMessage('Erro ao enviar arquivo. Tente novamente.', 'error');
    })
    .finally(() => {
        editorState.uploading = false;
    });
}

/**
 * Inicializa o modal de exportação
 */
function initExportModal() {
    const exportBtn = document.getElementById('export-btn');
    const modal = document.getElementById('export-modal');
    const closeModal = document.querySelector('.close-modal');
    const copyBtn = document.getElementById('copy-markdown');
    const downloadBtn = document.getElementById('download-markdown');
    
    if (!exportBtn || !modal) return;
    
    // Abre o modal ao clicar no botão de exportar
    exportBtn.addEventListener('click', function() {
        fetchMarkdownContent();
        modal.classList.add('active');
    });
    
    // Fecha o modal ao clicar no X
    if (closeModal) {
        closeModal.addEventListener('click', function() {
            modal.classList.remove('active');
        });
    }
    
    // Fecha o modal ao clicar fora dele
    window.addEventListener('click', function(event) {
        if (event.target === modal) {
            modal.classList.remove('active');
        }
    });
    
    // Copia o markdown para o clipboard
    if (copyBtn) {
        copyBtn.addEventListener('click', function() {
            const markdown = document.getElementById('export-markdown').textContent;
            navigator.clipboard.writeText(markdown)
                .then(() => {
                    showMessage('Markdown copiado para a área de transferência!', 'success');
                })
                .catch(err => {
                    console.error('Erro ao copiar:', err);
                    showMessage('Erro ao copiar. Tente selecionar o texto manualmente.', 'error');
                });
        });
    }
    
    // Download do markdown como arquivo
    if (downloadBtn) {
        downloadBtn.addEventListener('click', function() {
            const markdown = document.getElementById('export-markdown').textContent;
            const filename = document.getElementById('filename').value || 'README.md';
            
            const blob = new Blob([markdown], { type: 'text/markdown' });
            const url = URL.createObjectURL(blob);
            
            const a = document.createElement('a');
            a.href = url;
            a.download = filename;
            a.click();
            
            URL.revokeObjectURL(url);
            showMessage(`Arquivo ${filename} baixado com sucesso!`, 'success');
        });
    }
}

/**
 * Busca o conteúdo markdown completo para exportação
 */
function fetchMarkdownContent() {
    // Primeiro salva a seção atual
    if (editorState.formChanged) {
        saveSection(true)
            .then(() => getFullMarkdown())
            .catch(error => {
                console.error('Erro ao salvar seção:', error);
                showMessage('Erro ao gerar markdown. Tente novamente.', 'error');
            });
    } else {
        getFullMarkdown();
    }
}

/**
 * Busca o markdown completo da API
 */
function getFullMarkdown() {
    fetch('/export')
        .then(response => response.json())
        .then(data => {
            const markdownContainer = document.getElementById('export-markdown');
            const filenameInput = document.getElementById('filename');
            
            if (markdownContainer) {
                markdownContainer.textContent = data.markdown;
                
                // Aplica syntax highlighting
                if (window.hljs) {
                    hljs.highlightElement(markdownContainer);
                }
            }
            
            if (filenameInput && data.filename) {
                filenameInput.value = data.filename;
            }
        })
        .catch(error => {
            console.error('Erro ao buscar markdown:', error);
            showMessage('Erro ao gerar markdown. Tente novamente.', 'error');
        });
}

/**
 * Inicializa campos condicionais que dependem de outros campos
 */
function initConditionalFields() {
    const conditionalFields = document.querySelectorAll('.conditional-field');
    
    if (conditionalFields.length > 0) {
        updateConditionalFields();
        
        // Adiciona listeners aos campos que controlam condicionais
        const conditionFields = new Set();
        conditionalFields.forEach(field => {
            const controlField = field.getAttribute('data-condition-field');
            if (controlField) {
                conditionFields.add(controlField);
            }
        });
        
        conditionFields.forEach(fieldName => {
            const controls = document.querySelectorAll(`[name="${fieldName}"]`);
            controls.forEach(control => {
                control.addEventListener('change', updateConditionalFields);
            });
        });
    }
}

/**
 * Atualiza a visibilidade dos campos condicionais
 */
function updateConditionalFields() {
    const conditionalFields = document.querySelectorAll('.conditional-field');
    
    conditionalFields.forEach(field => {
        const conditionField = field.getAttribute('data-condition-field');
        const conditionValue = field.getAttribute('data-condition-value');
        
        if (conditionField && conditionValue) {
            let currentValue = '';
            
            // Obtém o valor atual do campo de condição
            const control = document.querySelector(`[name="${conditionField}"]`);
            if (!control) return;
            
            if (control.type === 'radio' || control.type === 'checkbox') {
                // Para inputs radio e checkbox
                const checkedControl = document.querySelector(`[name="${conditionField}"]:checked`);
                currentValue = checkedControl ? checkedControl.value : '';
            } else {
                // Para outros tipos de input
                currentValue = control.value;
            }
            
            // Atualiza visibilidade
            if (currentValue === conditionValue) {
                field.classList.add('visible');
            } else {
                field.classList.remove('visible');
            }
        }
    });
}

/**
 * Salva a seção atual via AJAX
 * @param {boolean} silent - Se true, não mostra mensagens de sucesso
 * @returns {Promise} - Promise que resolve quando o salvamento terminar
 */
function saveSection(silent = false) {
    return new Promise((resolve, reject) => {
        const form = document.getElementById('section-form');
        if (!form) {
            reject(new Error('Formulário não encontrado'));
            return;
        }
        
        const formData = new FormData(form);
        formData.append('section', editorState.currentSection);
        
        fetch('/update_section', {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                editorState.formChanged = false;
                editorState.lastSavedData = formData;
                
                if (!silent) {
                    showMessage('Seção salva com sucesso!', 'success');
                }
                
                // Atualiza o preview com o markdown gerado
                renderMarkdownPreview(data.markdown);
                
                // Atualiza o status da seção no menu
                updateSectionStatus();
                
                resolve(data);
            } else {
                showMessage('Erro ao salvar: ' + (data.error || 'Erro desconhecido'), 'error');
                reject(new Error(data.error || 'Erro desconhecido'));
            }
        })
        .catch(error => {
            console.error('Erro ao salvar seção:', error);
            showMessage('Erro ao salvar. Verifique sua conexão e tente novamente.', 'error');
            reject(error);
        });
    });
}

/**
 * Atualiza o preview em tempo real
 */
function updatePreview() {
    if (!editorState.formChanged) return;
    
    const form = document.getElementById('section-form');
    if (!form) return;
    
    const formData = new FormData(form);
    formData.append('section', editorState.currentSection);
    
    // Não atualiza o preview se estiver em uma tela pequena e o preview não estiver visível
    if (window.innerWidth < 1024 && !editorState.previewVisible) return;
    
    fetch('/update_section', {
        method: 'POST',
        body: formData
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            renderMarkdownPreview(data.markdown);
        }
    })
    .catch(error => {
        console.error('Erro ao atualizar preview:', error);
    });
}

/**
 * Renderiza o markdown no preview
 * @param {string} markdown - Conteúdo markdown
 */
function renderMarkdownPreview(markdown) {
    const previewContainer = document.getElementById('markdown-preview');
    if (!previewContainer) return;
    
    // Usa marked.js para renderizar markdown em HTML
    if (window.marked) {
        previewContainer.innerHTML = marked.parse(markdown);
        
        // Aplica syntax highlighting em blocos de código
        if (window.hljs) {
            previewContainer.querySelectorAll('pre code').forEach(block => {
                hljs.highlightElement(block);
            });
        }
    } else {
        // Fallback caso marked.js não esteja disponível
        previewContainer.innerHTML = `<pre>${markdown}</pre>`;
    }
}

/**
 * Atualiza o status das seções no menu lateral
 */
function updateSectionStatus() {
    fetch('/get_sections_status')
        .then(response => response.json())
        .then(data => {
            if (data.status) {
                Object.keys(data.status).forEach(sectionId => {
                    const isComplete = data.status[sectionId];
                    const sectionItem = document.querySelector(`.section-nav a[href*="${sectionId}"]`);
                    
                    if (sectionItem) {
                        const statusIcon = sectionItem.querySelector('.section-status');
                        if (statusIcon) {
                            if (isComplete) {
                                statusIcon.classList.remove('incomplete');
                                statusIcon.classList.add('complete');
                                statusIcon.textContent = '✓';
                            } else {
                                statusIcon.classList.remove('complete');
                                statusIcon.classList.add('incomplete');
                                statusIcon.textContent = '○';
                            }
                        }
                    }
                });
            }
        })
        .catch(error => {
            console.error('Erro ao atualizar status das seções:', error);
        });
}

/**
 * Destaca a seção ativa no menu lateral
 */
function highlightActiveSection() {
    document.querySelectorAll('.section-nav li').forEach(item => {
        item.classList.remove('active');
    });
    
    const sectionLink = document.querySelector(`.section-nav a[href*="${editorState.currentSection}"]`);
    if (sectionLink) {
        const parentLi = sectionLink.closest('li');
        if (parentLi) {
            parentLi.classList.add('active');
        }
    }
}

/**
 * Mostra uma mensagem de feedback para o usuário
 * @param {string} message - Texto da mensagem
 * @param {string} type - Tipo de mensagem (success, error, info, warning)
 */
function showMessage(message, type = 'info') {
    // Verificar se já existe um elemento de mensagem
    let messageContainer = document.querySelector('.message-container');
    
    // Se não existir, criar um novo
    if (!messageContainer) {
        messageContainer = document.createElement('div');
        messageContainer.className = 'message-container';
        document.body.appendChild(messageContainer);
    }
    
    // Criar o elemento da mensagem
    const messageElement = document.createElement('div');
    messageElement.className = `message message-${type} fade-in`;
    messageElement.textContent = message;
    
    // Adicionar ao container
    messageContainer.appendChild(messageElement);
    
    // Remover após um tempo
    setTimeout(() => {
        messageElement.classList.add('fade-out');
        setTimeout(() => {
            messageElement.remove();
            
            // Se não houver mais mensagens, remover o container
            if (messageContainer.children.length === 0) {
                messageContainer.remove();
            }
        }, 300);
    }, 3000);
}

/**
 * Função de debounce para limitar chamadas de função
 * @param {Function} func - Função a ser executada
 * @param {number} wait - Tempo de espera em ms
 * @returns {Function} - Função com debounce
 */
function debounce(func, wait) {
    let timeout;
    return function(...args) {
        const context = this;
        clearTimeout(timeout);
        timeout = setTimeout(() => func.apply(context, args), wait);
    };
}

// Exporta funções para uso global
window.initEditor = initEditor;
window.updatePreview = updatePreview;
window.saveSection = saveSection;
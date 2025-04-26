/**
 * DocGen - Sistema de Geração de Documentação Profissional
 * Scripts principais
 */

// Verifica se o DOM foi carregado
document.addEventListener('DOMContentLoaded', function() {
  // Inicializa componentes comuns
  initThemeSelector();
  initMobileMenu();
  initPageTransitions();
  
  // Adiciona classe para ativar animações após carregamento da página
  setTimeout(() => {
      document.body.classList.add('page-loaded');
  }, 100);
});

/**
* Inicializa o seletor de temas
*/
function initThemeSelector() {
  const themeSelector = document.getElementById('theme-select');
  if (!themeSelector) return;
  
  themeSelector.addEventListener('change', function() {
      const theme = this.value;
      applyTheme(theme);
      
      // Salva a preferência via AJAX
      fetch('/update_theme', {
          method: 'POST',
          headers: {
              'Content-Type': 'application/x-www-form-urlencoded',
          },
          body: 'theme=' + theme
      })
      .catch(error => {
          console.error('Erro ao salvar tema:', error);
      });
  });
}

/**
* Aplica o tema selecionado
* @param {string} theme - Nome do tema
*/
function applyTheme(theme) {
  // Remove todas as classes de tema atuais
  document.body.className = document.body.className
      .split(' ')
      .filter(cls => !cls.startsWith('theme-'))
      .join(' ');
  
  // Adiciona a classe do novo tema
  document.body.classList.add('theme-' + theme);
}

/**
* Inicializa o menu mobile para telas pequenas
*/
function initMobileMenu() {
  const menuToggle = document.querySelector('.menu-toggle');
  const sidebar = document.querySelector('.sidebar');
  
  if (!menuToggle || !sidebar) return;
  
  menuToggle.addEventListener('click', function() {
      sidebar.classList.toggle('active');
      menuToggle.classList.toggle('active');
  });
  
  // Fecha o menu ao clicar fora
  document.addEventListener('click', function(event) {
      if (sidebar.classList.contains('active') && 
          !sidebar.contains(event.target) && 
          !menuToggle.contains(event.target)) {
          sidebar.classList.remove('active');
          menuToggle.classList.remove('active');
      }
  });
  
  // Adiciona botão de menu em telas pequenas se não existir
  if (window.innerWidth < 768 && !document.querySelector('.menu-toggle')) {
      const menuButton = document.createElement('button');
      menuButton.className = 'menu-toggle';
      menuButton.innerHTML = '<span></span><span></span><span></span>';
      document.body.appendChild(menuButton);
      
      // Reinicializa o evento após criar o botão
      initMobileMenu();
  }
}

/**
* Inicializa transições de página para links internos
*/
function initPageTransitions() {
  // Adiciona classe para mostrar que a página terminou de carregar
  document.body.classList.add('transition-ready');
  
  // Animação em links internos
  document.querySelectorAll('a').forEach(link => {
      // Só aplica em links internos (mesmo domínio)
      if (link.href && 
          link.hostname === window.location.hostname && 
          !link.hasAttribute('data-no-transition')) {
          
          link.addEventListener('click', function(event) {
              // Não aplica em links que abrem em nova aba ou que tem modificadores
              if (event.metaKey || event.ctrlKey || event.shiftKey || 
                  link.target === '_blank') {
                  return;
              }
              
              event.preventDefault();
              
              // Adiciona classe para animar saída
              document.body.classList.add('page-transition-out');
              
              // Navega para o link após a animação
              setTimeout(() => {
                  window.location.href = link.href;
              }, 300);
          });
      }
  });
}

/**
* Cria um modal dinâmico
* @param {string} title - Título do modal
* @param {string} content - Conteúdo HTML
* @param {Object} options - Opções adicionais
* @returns {HTMLElement} - Elemento do modal
*/
function createModal(title, content, options = {}) {
  // Remove modal existente se houver
  const existingModal = document.querySelector('.dynamic-modal');
  if (existingModal) {
      existingModal.remove();
  }
  
  // Cria elementos do modal
  const modal = document.createElement('div');
  modal.className = 'modal dynamic-modal';
  
  const modalContent = document.createElement('div');
  modalContent.className = 'modal-content';
  
  // Adiciona título
  const titleElement = document.createElement('h2');
  titleElement.textContent = title;
  modalContent.appendChild(titleElement);
  
  // Adiciona botão de fechar
  const closeButton = document.createElement('span');
  closeButton.className = 'close-modal';
  closeButton.innerHTML = '&times;';
  modalContent.appendChild(closeButton);
  
  // Adiciona conteúdo
  const contentElement = document.createElement('div');
  contentElement.className = 'modal-body';
  contentElement.innerHTML = content;
  modalContent.appendChild(contentElement);
  
  // Adiciona botões de ação, se fornecidos
  if (options.actions && options.actions.length > 0) {
      const actionsElement = document.createElement('div');
      actionsElement.className = 'modal-actions';
      
      options.actions.forEach(action => {
          const button = document.createElement('button');
          button.className = `btn ${action.class || 'btn-outline'}`;
          button.textContent = action.text;
          
          if (action.onClick) {
              button.addEventListener('click', () => action.onClick(modal));
          }
          
          actionsElement.appendChild(button);
      });
      
      modalContent.appendChild(actionsElement);
  }
  
  // Monta o modal
  modal.appendChild(modalContent);
  document.body.appendChild(modal);
  
  // Adiciona eventos
  closeButton.addEventListener('click', () => {
      modal.classList.remove('active');
      setTimeout(() => modal.remove(), 300);
      
      if (options.onClose) {
          options.onClose();
      }
  });
  
  // Fecha ao clicar fora
  if (options.closeOnOutsideClick !== false) {
      modal.addEventListener('click', event => {
          if (event.target === modal) {
              closeButton.click();
          }
      });
  }
  
  // Ativa o modal
  setTimeout(() => modal.classList.add('active'), 10);
  
  return modal;
}

/**
* Exibe uma mensagem de notificação
* @param {string} message - Texto da mensagem
* @param {string} type - Tipo da mensagem (success, error, info, warning)
* @param {number} duration - Duração em ms (0 para não fechar)
*/
function showNotification(message, type = 'info', duration = 3000) {
  // Container para notificações
  let container = document.querySelector('.notification-container');
  if (!container) {
      container = document.createElement('div');
      container.className = 'notification-container';
      document.body.appendChild(container);
  }
  
  // Cria elemento da notificação
  const notification = document.createElement('div');
  notification.className = `notification notification-${type} slide-in-right`;
  
  // Ícone com base no tipo
  let icon = '💬'; // info
  if (type === 'success') icon = '✅';
  else if (type === 'error') icon = '❌';
  else if (type === 'warning') icon = '⚠️';
  
  notification.innerHTML = `
      <div class="notification-icon">${icon}</div>
      <div class="notification-content">${message}</div>
      <button class="notification-close">&times;</button>
  `;
  
  // Adiciona ao container
  container.appendChild(notification);
  
  // Botão para fechar
  const closeBtn = notification.querySelector('.notification-close');
  closeBtn.addEventListener('click', () => {
      notification.classList.add('slide-out-right');
      setTimeout(() => {
          notification.remove();
          // Remove o container se estiver vazio
          if (container.children.length === 0) {
              container.remove();
          }
      }, 300);
  });
  
  // Fecha automaticamente após a duração (se não for 0)
  if (duration > 0) {
      setTimeout(() => {
          // Só fecha se ainda existir no DOM
          if (document.body.contains(notification)) {
              notification.classList.add('slide-out-right');
              setTimeout(() => {
                  notification.remove();
                  // Remove o container se estiver vazio
                  if (container.children.length === 0) {
                      container.remove();
                  }
              }, 300);
          }
      }, duration);
  }
  
  return notification;
}

/**
* Carrega dados via AJAX
* @param {string} url - URL para requisição
* @param {Object} options - Opções para fetch
* @returns {Promise<any>} - Promise com os dados
*/
function fetchData(url, options = {}) {
  // Mostra indicador de carregamento (opcional)
  const showLoader = options.showLoader !== false;
  let loader;
  
  if (showLoader) {
      loader = document.createElement('div');
      loader.className = 'global-loader';
      loader.innerHTML = '<div class="loading-spinner"></div>';
      document.body.appendChild(loader);
      
      // Animação para mostrar
      setTimeout(() => {
          loader.style.opacity = '1';
      }, 10);
  }
  
  // Configuração padrão para as requisições
  const fetchOptions = {
      headers: {
          'Content-Type': 'application/json',
      },
      ...options
  };
  
  return fetch(url, fetchOptions)
      .then(response => {
          if (!response.ok) {
              throw new Error(`Erro HTTP ${response.status}: ${response.statusText}`);
          }
          return response.json();
      })
      .finally(() => {
          // Remove o loader se existir
          if (showLoader && loader) {
              loader.style.opacity = '0';
              setTimeout(() => {
                  loader.remove();
              }, 300);
          }
      });
}

/**
* Função de debounce para limitar chamadas de função
* @param {Function} func - Função a ser executada
* @param {number} wait - Tempo de espera em ms
* @param {boolean} immediate - Se deve executar imediatamente
* @returns {Function} - Função com debounce
*/
function debounce(func, wait, immediate) {
  let timeout;
  return function() {
      const context = this;
      const args = arguments;
      
      const later = function() {
          timeout = null;
          if (!immediate) func.apply(context, args);
      };
      
      const callNow = immediate && !timeout;
      clearTimeout(timeout);
      timeout = setTimeout(later, wait);
      
      if (callNow) func.apply(context, args);
  };
}

/**
* Função de throttle para limitar a frequência de chamadas
* @param {Function} func - Função a ser executada
* @param {number} limit - Limite de tempo em ms
* @returns {Function} - Função com throttle
*/
function throttle(func, limit) {
  let lastFunc;
  let lastRan;
  
  return function() {
      const context = this;
      const args = arguments;
      
      if (!lastRan) {
          func.apply(context, args);
          lastRan = Date.now();
      } else {
          clearTimeout(lastFunc);
          lastFunc = setTimeout(function() {
              if ((Date.now() - lastRan) >= limit) {
                  func.apply(context, args);
                  lastRan = Date.now();
              }
          }, limit - (Date.now() - lastRan));
      }
  };
}

/**
* Exporta funções globais
*/
window.createModal = createModal;
window.showNotification = showNotification;
window.fetchData = fetchData;
window.debounce = debounce;
window.throttle = throttle;
window.applyTheme = applyTheme;
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard-to-guess-string'
    UPLOAD_FOLDER = os.path.join(os.getcwd(), 'app', 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
    
    # Tipos de projetos disponíveis
    PROJECT_TYPES = [
        'backend',
        'frontend',
        'full-stack',
        'mobile',
        'cybersecurity',
        'networking',
        'data-science',
        'machine-learning',
        'devops'
    ]
    
    # Frameworks específicos
    FRAMEWORKS = {
        'backend': ['Django', 'Flask', 'FastAPI', 'Express.js', 'Spring Boot', 'Laravel'],
        'frontend': ['React', 'Vue.js', 'Angular', 'Svelte', 'Next.js'],
        'full-stack': ['MERN', 'MEAN', 'Django + React', 'Laravel + Vue', 'Ruby on Rails'],
        'mobile': ['React Native', 'Flutter', 'Kotlin', 'Swift', 'Xamarin'],
        'cybersecurity': ['OWASP', 'Kali Tools', 'Metasploit'],
        'networking': ['Cisco', 'Juniper', 'OpenVPN'],
        'data-science': ['Pandas', 'NumPy', 'Scikit-learn', 'TensorFlow', 'PyTorch'],
        'machine-learning': ['TensorFlow', 'PyTorch', 'Keras', 'Scikit-learn'],
        'devops': ['Docker', 'Kubernetes', 'Jenkins', 'GitHub Actions', 'Terraform']
    }
    
    # Temas disponíveis
    THEMES = [
        'dark',
        'light',
        'cyberpunk',
        'minimalist',
        'retro',
        'neon',
        'corporate',
        'custom'
    ]
    
    # Opções de licença
    LICENSES = [
        'MIT',
        'Apache 2.0',
        'GPL-3.0',
        'BSD-3-Clause',
        'Creative Commons',
        'Proprietary',
        'Custom'
    ]
    
    @staticmethod
    def init_app(app):
        # Criar pastas necessárias se não existirem
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
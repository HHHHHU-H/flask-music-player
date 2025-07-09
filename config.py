
import os
from dotenv import load_dotenv

# 定位到项目根目录，以便 .env 文件能被正确加载
basedir = os.path.abspath(os.path.dirname(__file__))
# 加载 .env 文件中的环境变量
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """项目的基础配置文件"""
    
    # 1. 安全密钥: 用于保护 Flask session 数据。必须设置！
    # 从环境变量 'SECRET_KEY' 中获取，如果找不到，则使用一个默认的、不安全的密钥（仅用于开发）
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-hard-to-guess-secret-key'
    
    # 2. 数据库配置
    # 优先从环境变量 'DATABASE_URL' 获取，否则使用 instance 文件夹下的 sqlite 数据库
    # 使用 os.path.join 确保路径拼接在所有操作系统上（Windows, Linux, macOS）都是正确的
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'instance', 'music_player.db')
        
    # 3. SQLAlchemy 配置: 关闭追踪对象修改的信号，可以节省系统资源
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 4. 文件上传配置: 将上传的文件存放在 instance/uploads 目录下
    UPLOAD_FOLDER = os.path.join(basedir, 'instance', 'uploads')

    
    # 【在此处添加以下新配置】
    # 5. 允许上传的文件扩展名
    ALLOWED_EXTENSIONS = {'mp3', 'pdf','txt'}

    # 文件: config.py

import os
from dotenv import load_dotenv

# 定位到项目根目录，以便 .env 文件能被正确加载
basedir = os.path.abspath(os.path.dirname(__file__))
# 加载 .env 文件中的环境变量
load_dotenv(os.path.join(basedir, '.env'))

class Config:
    """项目的基础配置文件"""
    
    # 1. 安全密钥...
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'a-very-hard-to-guess-secret-key'
    
    # 2. 数据库配置...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
    'postgres://', 'postgresql://') or \
    'sqlite:///' + os.path.join(basedir, 'instance', 'music_player.db')
        
    # 3. SQLAlchemy 配置...
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # 4. 文件上传配置...
    UPLOAD_FOLDER = os.path.join(basedir, 'instance', 'uploads')
    
    # 5. 允许上传的文件扩展名...
    ALLOWED_EXTENSIONS = {'mp3', 'pdf','txt'}

# --- 【在此处添加以下新代码】 ---
# 在配置类定义之后，直接执行文件夹创建逻辑
# 这样在任何其他代码导入Config类之前，文件夹就已经被确保存在了

# 1. 确保 instance 文件夹存在
# 我们从 SQLALCHEMY_DATABASE_URI 中提取 instance 文件夹的路径
db_uri = Config.SQLALCHEMY_DATABASE_URI
if db_uri.startswith('sqlite:///'):
    instance_path = os.path.dirname(db_uri.replace('sqlite:///', ''))
    if not os.path.exists(instance_path):
        os.makedirs(instance_path)
        print(f"配置文件: 成功创建 instance 文件夹于: {instance_path}")

# 2. 确保 uploads 文件夹存在
# UPLOAD_FOLDER 的路径依赖于 instance 文件夹，所以在此之后创建
upload_folder = Config.UPLOAD_FOLDER
if not os.path.exists(upload_folder):
    os.makedirs(upload_folder)
    print(f"配置文件: 成功创建上传文件夹于: {upload_folder}")
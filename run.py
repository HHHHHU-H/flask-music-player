# 文件: run.py (最终生产版)

from app import create_app
from config import Config
import os

# 使用 Config 类来创建应用实例
# 这是 "应用工厂" 模式，它允许我们为不同环境（开发、测试、生产）传入不同的配置
app = create_app(Config)

# 在应用启动前，检查并确保上传文件夹存在
# 这个逻辑在本地和服务器上都很有用
with app.app_context():
    upload_folder = app.config['UPLOAD_FOLDER']
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        print(f"成功创建上传文件夹于: {upload_folder}")

if __name__ == '__main__':
    # 在本地开发时，我们使用 waitress 作为服务器，它比 Flask 自带的更稳定
    # host='0.0.0.0' 让服务器监听所有网络接口
    # port=8000 是一个常见的开发端口
    # 在 Render 上部署时，这个文件不会被直接运行，Render 会使用 gunicorn
    from waitress import serve
    serve(app, host='0.0.0.0', port=8000)
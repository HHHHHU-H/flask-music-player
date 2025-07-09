README.md 
在线音乐播放器 (Python & Flask版) 项目说明
1. 项目愿景
本项目旨在创建一个功能完善、支持多用户、可通过互联网访问的在线音乐管理与播放平台。用户可以注册自己的账户，上传和管理私人的音乐文件（如 MP3）和对应的 PDF 歌词文件，并将它们整理到自定义的歌单中。
与本地桌面应用不同，本项目将采用标准的 Web 技术栈，构建一个B/S（浏览器/服务器）架构的应用。后端使用 Python Flask 框架处理业务逻辑和数据，前端使用 HTML/CSS/JavaScript 负责用户交互和界面展示。项目最终目标是能够部署到公网服务器，让用户随时随地通过浏览器访问自己的音乐库。
2. 核心功能需求
用户账户系统 (多用户支持):
提供用户注册和登录功能。
用户密码必须经过哈希加密后才能存入数据库，确保安全性。
用户只能访问和管理自己上传的歌曲和创建的歌单。
歌曲与歌词管理:
登录后，用户可以通过网页上的表单上传音乐文件（.mp3）和歌词文件（.pdf）。
程序自动将歌曲和歌词文件关联，并将它们存储在服务器的指定目录中。
数据库中存储文件的元数据（如歌曲名、关联用户）以及文件的访问路径。
数据库存储:
使用 sqlite3 作为开发数据库，便于快速启动。(备注：生产环境建议切换至 PostgreSQL 或 MySQL)。
使用 Flask-SQLAlchemy ORM 框架来简化数据库操作。
需要设计的核心表包括：users (用户信息), songs (歌曲信息), playlists (歌单信息), playlist_songs (关联表)。
歌单功能:
用户可以创建、重命名、删除自己的歌单。
可以将自己曲库中的任意歌曲添加到多个歌单中，或从歌单中移除。
主界面可以清晰地切换并展示不同歌单的歌曲列表。
在线音乐播放:
使用 HTML5 的 <audio> 标签进行音乐播放。
前端通过 JavaScript 控制播放器的行为，包括播放/暂停、上一首、下一首、音量控制、进度条拖动。
支持三种播放模式切换：列表循环、单曲循环、随机播放。
界面上需实时显示当前播放的歌曲名、播放状态和播放模式。
歌词展示 (Web内嵌):
当一首歌曲播放时，在网页内部的一个指定区域（例如，使用 <iframe> 或 <embed> 标签）加载并显示对应的PDF歌词文件。
注意：无需复杂的PDF解析，直接在网页中嵌入PDF文件即可。这大大简化了前端实现，同时满足了歌词同步查看的需求。
3. 技术栈与架构设计
后端框架: Flask (Python)
理由: 轻量、灵活，拥有丰富的扩展生态，非常适合快速开发此类Web应用。
数据库 ORM: Flask-SQLAlchemy
理由: 提供了面向对象的数据库操作方式，屏蔽了原生SQL的复杂性，提高了开发效率和代码可维护性。
用户认证: Flask-Login 或自定义Session管理
理由: 处理用户登录状态、会话保持等任务。
前端技术:
HTML5: 页面结构，特别是 <audio> 标签。
CSS3: 页面样式。可选用 Bootstrap 或 Tailwind CSS 等框架来快速构建美观的响应式界面。
JavaScript (ES6+): 负责所有前端动态交互。使用 Fetch API (或 Axios) 与后端进行异步数据通信（AJAX），实现无刷新更新页面内容。
服务器部署:
WSGI 服务器: Gunicorn (生产环境常用)
反向代理: Nginx (处理静态文件、负载均衡、SSL加密)
4. 数据库结构设计
数据库文件: music_player.db
表1: users - 存储用户信息
id (INTEGER, PRIMARY KEY)
username (TEXT, NOT NULL, UNIQUE)
password_hash (TEXT, NOT NULL)
表2: songs - 存储歌曲元数据和路径
id (INTEGER, PRIMARY KEY)
title (TEXT, NOT NULL)
artist (TEXT, 可选)
song_url (TEXT, NOT NULL) - 音乐文件的Web访问URL
lyrics_url (TEXT) - PDF歌词文件的Web访问URL
user_id (INTEGER, FOREIGN KEY -> users.id) - 关联到上传者
表3: playlists - 存储歌单信息
id (INTEGER, PRIMARY KEY)
name (TEXT, NOT NULL)
user_id (INTEGER, FOREIGN KEY -> users.id) - 关联到创建者
表4: playlist_songs - 关联歌单和歌曲 (多对多)
playlist_id (INTEGER, FOREIGN KEY -> playlists.id)
song_id (INTEGER, FOREIGN KEY -> songs.id)
PRIMARY KEY (playlist_id, song_id)
5. 建议的实现步骤
环境设置与项目结构:
创建虚拟环境 (python -m venv venv)。
创建 requirements.txt 文件，包含 Flask, Flask-SQLAlchemy, Werkzeug (用于密码哈希)等。
搭建典型的Flask项目结构：
Generated code
/project
├── app.py          # 主应用文件
├── models.py       # 数据库模型
├── routes.py       # 路由/视图函数
├── static/         # 存放CSS, JS, Images
│   ├── css/
│   └── js/
├── templates/      # 存放HTML模板
└── instance/       # 存放数据库文件和上传的文件
Use code with caution.
后端开发 (API优先):
模型定义: 在 models.py 中使用SQLAlchemy定义上述四个数据表。
用户认证: 实现注册、登录、登出的路由和逻辑。对用户密码进行哈希处理。
文件上传: 创建一个接收文件上传的路由。处理上传的mp3和pdf，保存到服务器的指定位置，并将URL等信息存入数据库。
数据接口: 创建一系列返回JSON数据的API端点，例如：
GET /api/songs - 获取当前用户的所有歌曲。
GET /api/playlists - 获取当前用户的所有歌单。
GET /api/playlists/<id> - 获取特定歌单的歌曲。
POST /api/playlists - 创建新歌单。
POST /api/playlists/<id>/add_song - 向歌单添加歌曲。
前端开发:
页面模板: 创建基础的HTML模板 (base.html) 和各个页面的模板 (login.html, index.html)。
登录/注册页: 创建表单，使用JavaScript的fetch方法将用户输入提交到后端的认证接口。
主播放界面 (index.html):
页面加载后，使用fetch请求 /api/playlists 和 /api/songs，动态生成左侧的歌单列表和中间的歌曲列表。
为列表项绑定点击事件，点击歌单时，请求该歌单的数据并刷新歌曲列表。
播放器核心JS: 编写JavaScript逻辑，控制HTML5 <audio>元素。将播放/暂停、切歌等按钮与audio对象的play(), pause(), src等属性和方法绑定。
当播放一首歌时，获取其 lyrics_url，并更新 <iframe> 的 src 属性来显示歌词。
6. 部署注意事项
关闭Debug模式: 在生产环境中，必须设置 DEBUG = False。
配置SECRET_KEY: 为Flask应用设置一个复杂且随机的SECRET_KEY，用于保护Session。
使用生产级WSGI服务器: 不要使用Flask自带的开发服务器（app.run()）来部署。应使用 Gunicorn 或 uWSGI。
配置Nginx: 在Gunicorn前端设置一个Nginx反向代理，用于高效处理静态文件请求、设置HTTPS、进行请求分发等。
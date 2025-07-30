
## 项目说明
财蕴天下服务端项目目录

### 创建项目
~~~ shell
# 项目初始化 [默认当前文件夹] 
uv init [project_name] 
~~~

~~~ shell
# 创建虚拟环境 
uv venv
~~~

~~~ shell
# 添加依赖（会更新 pyproject.toml） 
uv add "mcp[cli]"
uv add dotenv
uv add flask
uv add gunicorn
uv add websockets
uv add dashscope
uv add requests
uv add deepmerge
uv add alibabacloud-bailian20231229
uv add fastapi
~~~

~~~ shell
# 同步项目依赖 
uv sync

# 把依赖关系写入文件
uv pip freeze > requirements.txt

# 安装依赖
uv pip install -r requirements.txt
~~~



### Debug run 本地mcp测试验证
~~~ shell
# 先启动mcp sse服务
uv run cytx_mcp_server.py
# 再启动调试工具
uv run mcp dev cytx_mcp_server.py

# fastapi启动
uvicorn main:app --host 0.0.0.0 --port 8001 --reload --debug --log-level debug

# 新的mcp server 启动 -- 报告解读
uv run cytx_report_mcp_server.py

~~~
### 生产 run
~~~ shell

# 生产安装python
CPPFLAGS="$(pkg-config --cflags openssl11)" \
LDFLAGS="$(pkg-config --libs openssl11)" \
pyenv install -v 3.12.0

#生产启动mcp server
nohup uv run cytx_mcp_server.py --host 0.0.0.0 --port=8000 > mcp.log 2>&1 &
# 生成启动 报告mcp server
nohup uv run cytx_report_mcp_server.py --host 0.0.0.0 --port=8002 > report.log 2>&1 &

# fastapi启动
uvicorn main:app --host 0.0.0.0 --port 8001 --reload

# fastapi 生产启动
uvicorn -D main:app --host 0.0.0.0 --port 8001 --workers 4

## fastapi 日志输出到文件
nohup uv run uvicorn main:app --host 0.0.0.0 --port 8001 --workers 4 > api.log 2>&1 &

### 生成 stop
~~~  shell
# 查看进程
ps -ef | grep cytx_mcp_server.py
# 停止mcp server
pkill -f cytx_mcp_server.py

#停止gunicorn
pkill -f gunicorn

~~~


### 生产配合nginx使用

~~~ nginx
     location /cytxapi/ {
          proxy_pass http://127.0.0.1:8001/cytxapi/;

          proxy_set_header Host $host;
          proxy_set_header X-Real-IP $remote_addr;
          #proxy_set_header X-Forwarded-For $proxy_add_xforwarded_for;
          proxy_set_header X-Forwarded-Proto $scheme;

          proxy_connect_timeout 60s;
          proxy_read_timeout 120s;
        }

        location /chatws {
          proxy_pass http://127.0.0.1:8001/chatws;
          proxy_http_version 1.1;
          proxy_set_header Upgrade $http_upgrade;
          proxy_set_header Connection "upgrade";
          proxy_read_timeout 86400s;
          #proxy_write_timeout 86400s;
        }
        
        location /fileUploads/ {
                alias /opt/server/ai-cytx-fastapi/uploads/;
        }
~~~




## 百炼平台mcp server配置

~~~ json

开发环境：
{
    "mcpServers":{
        "CytxApp":{
            "url":"http://123.56.40.34:8000/sse"
        }
    }
}

{
    "mcpServers":{
        "CytxApp":{
            "url":"http://123.56.40.34:8002/sse"
        }
    }
}


{
    "mcpServers": {
        "CytxApp": {
            "command": "uv",
            "args": [
                "run",
                "--with",
                "mcp",
                "--with",
                "websockets",
                "mcp",
                "run",
                "cytx_mcp_server.py"
            ]
        }
    }
}

{
    "mcpServers": {
        "CytxApp": {
            "command": "uvx",
            "args": [
                “--from”,
                "ai-cytx-fastapi",
                "run-mcp-server"
            ]
        }
    }
}


测试环境：
{
    "mcpServers":{
        "CytxApp":{
            "url":"http://101.201.61.165:8000/sse"
        }
    }
}
~~~



# 大模型文档说明

## 提示词说明文档
    doc/project/cytx/prompt/prompt-omini.md
    doc/project/cytx/prompt/prompt-core.md

## 知识库相关文档
    doc/project/cytx/kb/

## 接口相关文档
    doc/project/cytx/api/

















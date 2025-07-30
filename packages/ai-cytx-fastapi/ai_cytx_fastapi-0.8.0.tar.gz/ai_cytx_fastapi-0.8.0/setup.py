from setuptools import setup, find_packages

setup(
    name='ai-cytx-fastapi',              # 包名（必须唯一）
    version='0.8.0',                       # 版本号
    description='A short description of the package.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='',  # 项目主页
    packages=find_packages(),              # 自动发现所有包
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.12',
    dependencies=[
        "alibabacloud-bailian20231229==2.0.7",
        "dashscope>=1.23.3",
        "deepmerge>=2.0",
        "dotenv>=0.9.9",
        "fastapi>=0.115.12",
        "flask>=3.1.1",
        "gevent>=25.5.1",
        "gevent-websocket>=0.10.1",
        "gunicorn>=23.0.0",
        "mcp[cli]>=1.8.1",
        "requests>=2.32.3",
        "setuptools>=80.9.0",
        "sse-starlette>=2.3.5",
        "twine>=6.1.0",
        "uvicorn>=0.34.2",
        "websockets>=15.0.1",
        "wheel>=0.45.1",
    ]
   
)

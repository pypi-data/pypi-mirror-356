# 🚀 MCP Proxy API

一个基于Quart框架的MCP (Model Context Protocol) 代理API服务器，提供JWT认证、工具调用和管理功能。 ✨

## 📁 项目结构

```
mcp_proxy/
├── core/                   # 🧠 核心业务逻辑模块
│   ├── __init__.py        # 📦 核心模块导出
│   ├── auth.py            # 🔐 JWT认证和验证
│   └── mcp_client.py      # 🤝 MCP客户端封装
├── api/                   # 🌐 API接口模块
│   ├── __init__.py        # 📦 API模块导出
│   └── routes.py          # 🛤️ API路由定义
├── utils/                 # 🛠️ 工具函数模块
│   ├── __init__.py        # 📦 工具模块导出
│   ├── exceptions.py      # ⚠️ 自定义异常类
│   └── helpers.py         # 🎯 数据处理工具
├── __init__.py            # 📦 包初始化文件
├── app.py                 # 🏗️ 主应用程序和应用工厂
├── config.py              # ⚙️ 配置管理
├── main.py                # 🏁 程序入口点
├── Dockerfile             # 🐳 Docker构建文件
├── pyproject.toml         # 📋 项目依赖和配置
├── README.md              # 📖 项目文档
└── .env.example           # 🔧 环境变量示例
```

## ✨ 功能特性

### 🎯 核心功能
- **🔧 MCP工具调用**: 代理调用远程MCP服务器的工具
- **📋 工具列表获取**: 获取所有可用的MCP工具信息
- **💚 健康检查**: 监控服务和MCP连接状态
- **🌐 多服务器支持**: 同时连接和管理多个MCP服务器

### 🔒 安全特性
- **🎫 JWT认证**: 支持Header和URL参数两种认证方式
- **⏰ 过期时间验证**: 强制验证JWT的exp字段，确保令牌有效性
- **🔑 算法配置**: 支持多种JWT签名算法（默认HS256）

### 👀 可观测性
- **📊 结构化日志**: JSON格式的请求响应日志
- **⏱️ 执行时间记录**: 详细的性能监控
- **🚨 错误处理**: 完善的异常处理和错误响应

## 🌐 多服务器配置

### 🎯 配置方式
本系统支持两种MCP服务器配置方式：

#### 📦 单服务器配置（向后兼容）
```bash
MCP_URL=http://localhost:3000/sse
```

#### 🚀 多服务器配置（推荐）
```bash
MCP_URLS=http://10.10.1.105:8999/sse,http://10.10.1.105:8005/sse,http://another-server:9000/sse
```

### ✨ 多服务器特性
- **⚖️ 工具分布**: 系统会自动发现每个服务器提供的工具
- **📊 状态监控**: 实时监控所有服务器的连接状态和可用工具

### 🛠️ 使用建议
1. **开发环境**: 可以使用单服务器配置
2. **生产环境**: 建议配置多个服务器以提高可用性
3. **混合部署**: 不同服务器可以提供不同类型的工具

## 🚀 快速开始

### 1. 🔧 环境配置

复制环境变量模板：
```bash
cp .env.example .env
```

编辑`.env`文件：
```bash
# 🔐 JWT配置
JWT_SECRET=your-secret-key-here
JWT_ALGORITHM=HS256

# 🔗 MCP服务器配置
# 单个服务器配置（向后兼容）
MCP_URL=http://localhost:3000/sse

# 多服务器配置（推荐）
# 使用逗号分隔多个URL
MCP_URLS=http://10.10.1.105:8999/sse,http://10.10.1.105:8005/sse

# 🖥️ 服务器配置
PORT=5000
DEBUG=false

# 📝 日志配置
LOG_LEVEL=INFO
```

### 2. 📦 安装依赖

#### 🌍 使用pip（中国大陆用户推荐）：
```bash
# 配置国内镜像源加速（可选）
pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple/
pip config set global.trusted-host pypi.tuna.tsinghua.edu.cn

# 安装依赖
pip install -r requirements.txt
pip install -e .
```

#### ⚡ 使用uv（海外用户推荐）：
```bash
uv sync
```

### 3. 🎫 生成JWT令牌

运行令牌生成脚本：
```bash
python -m mcp_proxy.scripts.generate_token
```

**⚠️ 重要提醒**: 生成的JWT令牌必须包含`exp`字段，API会强制验证过期时间。

### 4. 🏃‍♂️ 启动服务

```bash
python -m mcp_proxy.main
```

或使用包入口点：
```bash
python -c "from mcp_proxy import main; main()"
```

## 🌐 API接口

### 🔐 认证方式

支持两种JWT认证方式：

1. **🏷️ Header认证**（推荐）：
   ```bash
   curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:5000/tools/list
   ```

2. **🔗 URL参数认证**：
   ```bash
   curl "http://localhost:5000/tools/list?token=YOUR_TOKEN"
   ```

### 📋 接口详情

#### 1. 🔧 调用MCP工具
- **📍 路径**: `POST /tools`
- **🔐 认证**: 必需
- **📤 请求体**:
  ```json
  {
    "method": "tool_name",
    "args": {
      "param1": "value1"
    },
    "server": "http://10.10.1.105:8999/sse"  // 可选：指定优先服务器
  }
  ```

#### 2. 📝 获取工具列表
- **📍 路径**: `GET /tools/list`
- **🔐 认证**: 必需
- **🔍 查询参数**: `?server=URL` (可选，筛选特定服务器的工具)
- **📥 响应**: 返回所有可用的MCP工具信息，包含服务器分布情况

#### 3. 🌐 获取服务器列表
- **📍 路径**: `GET /servers`
- **🔐 认证**: 必需
- **📥 响应**: 返回所有MCP服务器状态和连接信息

#### 4. 💚 健康检查
- **📍 路径**: `GET /health`
- **🔐 认证**: 不需要
- **📥 响应**: 服务状态和所有MCP服务器连接信息

## 🎫 JWT令牌要求

### 📋 必需字段
- `exp`: ⏰ 过期时间（UNIX时间戳），**必须字段**
- API会强制验证令牌是否过期

### 🔍 令牌验证流程
1. 🔍 检查令牌格式和签名
2. **✅ 验证exp字段存在**
3. **⏰ 验证令牌未过期**
4. 👤 解析用户信息

### 💡 示例令牌payload：
```json
{
  "user_id": "test_user",
  "iat": 1703123456,
  "exp": 1703209856,
  "iss": "mcp-proxy"
}
```

## 🐳 Docker部署

### 🏗️ 构建镜像

我们提供两种Dockerfile供你选择：

#### 🌍 使用pip构建（推荐中国大陆用户）
```bash
# 使用pip版本的Dockerfile，包含国内镜像源加速
docker build -f Dockerfile.pip -t mcp-proxy:pip .
```

#### ⚡ 使用uv构建（海外用户推荐）
```bash
# 使用原版的uv Dockerfile
docker build -f Dockerfile -t mcp-proxy:uv .
```

### 🚀 运行容器

#### 运行pip版本
```bash
docker run -d \
  --name mcp-proxy \
  -p 5000:5000 \
  -e JWT_SECRET=your-secret-key \
  -e MCP_URLS=http://server1:8999/sse,http://server2:8005/sse \
  mcp-proxy:pip
```

#### 运行uv版本
```bash
docker run -d \
  --name mcp-proxy \
  -p 5000:5000 \
  -e JWT_SECRET=your-secret-key \
  -e MCP_URLS=http://server1:8999/sse,http://server2:8005/sse \
  mcp-proxy:uv
```

### 🐙 使用Docker Compose

我们还提供了docker-compose配置，让你可以更方便地启动服务：

#### 启动pip版本服务
```bash
docker-compose up -d mcp-proxy-pip
# 服务将在 http://localhost:5000 启动
```

#### 启动uv版本服务
```bash
docker-compose up -d mcp-proxy-uv
# 服务将在 http://localhost:5001 启动
```

#### 同时启动两个版本进行对比测试
```bash
docker-compose up -d
# pip版本: http://localhost:5000
# uv版本: http://localhost:5001
```

#### 查看日志
```bash
# 查看pip版本日志
docker-compose logs -f mcp-proxy-pip

# 查看uv版本日志
docker-compose logs -f mcp-proxy-uv
```

#### 停止服务
```bash
docker-compose down
```

## 👨‍💻 开发指南

### 🏗️ 项目架构

项目采用分层模块化架构设计：

#### 🧠 核心层 (core/)
- **🔐 auth.py**: JWT认证逻辑，包含强制exp验证
- **🤝 mcp_client.py**: 单个MCP客户端封装和连接管理
- **🌐 mcp_client_manager.py**: 多MCP服务器管理器，支持负载均衡和故障转移

#### 🌐 API层 (api/)
- **🛤️ routes.py**: API路由和请求处理

#### 🛠️ 工具层 (utils/)
- **⚠️ exceptions.py**: 定义自定义异常类型
- **🎯 helpers.py**: 数据序列化和日志工具

#### 📜 脚本层 (scripts/)
- **🎫 generate_token.py**: JWT令牌生成工具

#### ⚙️ 配置和应用层
- **🔧 config.py**: 集中管理所有配置项
- **🏗️ app.py**: 应用工厂和生命周期管理
- **🏁 main.py**: 程序入口点

### 📦 模块导入规则

```python
# 从外层导入核心模块
from mcp_proxy.core import MCPClient
from mcp_proxy.utils import APIError
from mcp_proxy.api import api_bp

# 在模块内部使用相对导入
from ..config import JWT_SECRET
from ..utils.exceptions import AuthenticationError
from ..core.auth import validate_request_auth
```

### ✨ 扩展功能

添加新的API端点：
1. 🛤️ 在`api/routes.py`中定义路由
2. ⚠️ 在`utils/exceptions.py`中添加相关异常（如需要）
3. 🎯 在`utils/helpers.py`中添加辅助函数（如需要）

### 📊 日志格式

API使用结构化JSON日志：
```json
{
  "timestamp": "2024-01-01T12:00:00.000Z",
  "request": {...},
  "response": {...},
  "status_code": 200,
  "execution_time_ms": 123.45,
  "remote_addr": "127.0.0.1",
  "user_agent": "curl/7.68.0"
}
```

## 🚨 错误处理

### 📋 错误响应格式
```json
{
  "error": {
    "message": "错误描述",
    "code": 400
  }
}
```

### 🔢 常见错误码
- `400`: ❌ 请求参数错误
- `401`: 🔐 认证失败或JWT过期
- `404`: 🔍 工具不存在
- `500`: ⚙️ 内部服务器错误
- `503`: 🔗 MCP服务器连接失败

## 🔒 安全最佳实践

1. **🔑 使用强密钥**: JWT_SECRET应使用强随机密钥
2. **🔄 定期轮换密钥**: 建议定期更换JWT密钥
3. **⏰ 设置合理过期时间**: 避免令牌有效期过长
4. **🔒 HTTPS部署**: 生产环境必须使用HTTPS
5. **👀 日志监控**: 监控认证失败和异常访问

## 🛠️ 故障排除

### ❓ 常见问题

1. **🚨 JWT导入错误**
   ```
   ImportError: No module named 'jwt'
   ```
   解决：安装正确的PyJWT包
   ```bash
   pip uninstall jwt
   pip install PyJWT
   ```

2. **🔗 MCP连接失败**
   - 🔍 检查MCP_URL是否正确
   - ✅ 确认MCP服务器是否运行
   - 🌐 验证网络连接

3. **🎫 JWT验证失败**
   - ✅ 确认令牌包含exp字段
   - ⏰ 检查令牌是否过期
   - 🔧 验证JWT_SECRET配置

4. **📦 模块导入失败**
   - 📁 确保从正确的目录运行程序
   - 🔧 检查PYTHONPATH环境变量
   - ✅ 验证模块结构完整性

## 📄 许可证

[MIT License](LICENSE) ✨

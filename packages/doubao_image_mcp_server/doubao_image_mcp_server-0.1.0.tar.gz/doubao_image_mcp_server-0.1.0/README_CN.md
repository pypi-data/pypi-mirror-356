# 豆包图像生成MCP服务器

基于FastMCP框架和火山方舟API实现的图像生成MCP服务器，支持通过豆包(doubao-seedream-3.0-t2i)模型生成高质量图像。

## 功能特点

- 🎨 **高质量图像生成**: 基于豆包seedream-3.0-t2i模型，支持2K分辨率
- 🌐 **中英双语支持**: 提示词支持中英文描述
- 📐 **多种分辨率**: 支持从512x512到2048x2048的多种分辨率
- 🎯 **精确控制**: 支持种子、引导强度、水印等参数控制
- 📁 **本地保存**: 自动下载并保存生成的图像到指定目录
- 🔧 **MCP协议**: 完全兼容MCP协议，可与支持MCP的AI助手集成
- 📊 **详细日志**: 完整的日志记录和错误处理

## 环境要求

- Python >= 3.13
- 火山方舟API密钥
- 推理接入点模型ID

## 安装配置

### 1. 克隆项目

```bash
cd doubao_image_mcp_server
```

### 2. 安装依赖

使用uv（推荐）:
```bash
uv sync
```

或使用pip:
```bash
pip install -e .
```

### 3. 配置环境变量

本项目不使用 `.env` 文件，所有配置通过 MCP JSON 配置文件的 `environment` 字段传递。

在你的 MCP 配置文件中添加以下配置:
```json
{
  "mcpServers": {
    "doubao_image_mcp_server": {
      "command": "uv",
      "args": [
        "--directory",
        "C:/WorkSpace/mcp_server/doubao_image_mcp_server",
        "run",
        "doubao_mcp_server.py"
      ],
      "environment": {
        "BASE_URL": "https://ark.cn-beijing.volces.com/api/v3",
        "DOUBAO_API_KEY": "your_api_key_here",
        "API_MODEL_ID": "your_model_id_here",
        "IMAGE_SAVE_DIR": "./images"
      }
    }
  }
}
```

需要配置的环境变量说明:
- `BASE_URL`: 豆包(火山方舟)平台BASE URL，默认为 `https://ark.cn-beijing.volces.com/api/v3`
- `DOUBAO_API_KEY`: 豆包API密钥（从火山方舟控制台获取）
- `API_MODEL_ID`: 推理接入点模型ID
- `IMAGE_SAVE_DIR`: 图片保存目录，默认为 `./images`

### 4. 获取API密钥和模型ID

1. 访问 [火山方舟控制台](https://console.volcengine.com/ark)
2. 创建API密钥
3. 创建推理接入点，选择 `doubao-seedream-3-0-t2i-250415` 模型
4. 获取接入点ID（格式如：`ep-20250528154802-c4np4`）

## 使用方法

### 启动服务器

```bash
python doubao_mcp_server.py
```

### MCP工具调用

服务器提供以下MCP工具:

#### `doubao_generate_image`

生成图像的主要工具。

**参数:**
- `prompt` (必需): 图像描述文本，支持中英文
- `size` (可选): 图像分辨率，默认 "1024x1024"
- `seed` (可选): 随机种子，默认 -1（自动生成）
- `guidance_scale` (可选): 引导强度 1.0-10.0，默认 8.0
- `watermark` (可选): 是否添加水印，默认 true
- `file_prefix` (可选): 文件名前缀，仅限英文

**支持的分辨率:**
- `512x512` - 512x512 (1:1 小正方形)
- `768x768` - 768x768 (1:1 正方形)
- `1024x1024` - 1024x1024 (1:1 大正方形)
- `864x1152` - 864x1152 (3:4 竖屏)
- `1152x864` - 1152x864 (4:3 横屏)
- `1280x720` - 1280x720 (16:9 宽屏)
- `720x1280` - 720x1280 (9:16 手机竖屏)
- `832x1248` - 832x1248 (2:3)
- `1248x832` - 1248x832 (3:2)
- `1512x648` - 1512x648 (21:9 超宽屏)
- `2048x2048` - 2048x2048 (1:1 超大正方形)

**示例调用:**
```json
{
  "tool": "doubao_generate_image",
  "arguments": {
    "prompt": "一只可爱的橘猫坐在阳光明媚的窗台上，水彩画风格",
    "size": "1024x1024",
    "guidance_scale": 8.0,
    "watermark": false,
    "file_prefix": "cute_cat"
  }
}
```

### MCP资源

#### `resolutions`

获取所有可用的图像分辨率列表。

### MCP提示模板

#### `image_generation_prompt`

提供图像生成的提示模板，包含所有参数说明和使用示例。

## 独立测试

### 测试图像生成工具

```bash
python doubao_image_gen.py
```

注意：测试前需要在代码中设置正确的API密钥和模型ID。

## 项目结构

```
doubao_mcp_server/
├── doubao_mcp_server.py    # 主MCP服务器
├── doubao_image_gen.py     # 图像生成核心工具
├── .env.example            # 环境变量模板
├── .env                    # 环境变量配置（需自行创建）
├── .gitignore             # Git忽略文件
├── README.md              # 项目说明
├── pyproject.toml         # 项目配置和依赖
├── uv.lock               # 依赖锁定文件
└── log/                  # 日志文件目录（自动创建）
    ├── doubao_mcp_server.log
    └── doubao_image_gen.log
```

## 日志系统

项目包含完整的日志系统:

- **文件日志**: 保存在 `log/` 目录下
- **控制台日志**: 输出到stderr，便于调试
- **日志级别**: DEBUG、INFO、WARNING、ERROR

## 错误处理

- ✅ 环境变量验证
- ✅ 参数类型和范围检查
- ✅ API调用错误处理
- ✅ 图片下载重试机制
- ✅ 文件保存异常处理

## 技术特点

- **异步处理**: 基于asyncio的异步图像生成
- **重试机制**: 图片下载失败自动重试
- **参数验证**: 完整的输入参数验证
- **模块化设计**: 核心功能与MCP服务分离
- **类型注解**: 完整的类型提示支持

## 常见问题

### Q: 如何获取API密钥？
A: 访问火山方舟控制台，在API管理中创建新的API密钥。

### Q: 模型ID在哪里找？
A: 在火山方舟控制台创建推理接入点后，可以在接入点详情中找到ID。

### Q: 支持哪些图片格式？
A: 目前生成的图片保存为JPG格式。

### Q: 如何自定义图片保存路径？
A: 在 `.env` 文件中修改 `IMAGE_SAVE_DIR` 变量。

### Q: 生成失败怎么办？
A: 检查日志文件，确认API密钥、模型ID和网络连接是否正常。

## 许可证

本项目基于MIT许可证开源。

## 贡献

欢迎提交Issue和Pull Request来改进项目
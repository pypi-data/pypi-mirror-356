# Doubao Image MCP Server

An image generation MCP server based on FastMCP framework and Volcano Engine API, supporting high-quality image generation through Doubao (doubao-seedream-3.0-t2i) model.

## Features

- 🎨 **High-Quality Image Generation**: Based on Doubao seedream-3.0-t2i model, supports 2K resolution
- 🌐 **Bilingual Support**: Prompts support both Chinese and English descriptions
- 📐 **Multiple Resolutions**: Supports various resolutions from 512x512 to 2048x2048
- 🎯 **Precise Control**: Supports seed, guidance scale, watermark and other parameter controls
- 📁 **Local Storage**: Automatically downloads and saves generated images to specified directory
- 🔧 **MCP Protocol**: Fully compatible with MCP protocol, can be integrated with MCP-supported AI assistants
- 📊 **Detailed Logging**: Complete logging and error handling

## Requirements

- Python >= 3.13
- Volcano Engine API Key
- Inference Endpoint Model ID

## Installation & Configuration

### 1. Clone Project

```bash
cd doubao_image_mcp_server
```

### 2. Install Dependencies

Using uv (recommended):
```bash
uv sync
```

Or using pip:
```bash
pip install -e .
```

### 3. Configure Environment Variables

This project does not use `.env` files. All configurations are passed through the `environment` field in the MCP JSON configuration file.

Add the following configuration to your MCP configuration file:
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

Environment variables explanation:
- `BASE_URL`: Doubao (Volcano Engine) platform BASE URL, default: `https://ark.cn-beijing.volces.com/api/v3`
- `DOUBAO_API_KEY`: Doubao API key (obtained from Volcano Engine console)
- `API_MODEL_ID`: Inference endpoint model ID
- `IMAGE_SAVE_DIR`: Image save directory, default: `./images`

### 4. Get API Key and Model ID

1. Visit [Volcano Engine Console](https://console.volcengine.com/ark)
2. Create API key
3. Create inference endpoint, select `doubao-seedream-3-0-t2i-250415` model
4. Get endpoint ID (format like: `ep-20250528154802-c4np4`)

## Usage

### Start Server

```bash
python doubao_mcp_server.py
```

### MCP Tool Calls

The server provides the following MCP tools:

#### `doubao_generate_image`

Main tool for image generation.

**Parameters:**
- `prompt` (required): Image description text, supports Chinese and English
- `size` (optional): Image resolution, default "1024x1024"
- `seed` (optional): Random seed, default -1 (auto-generate)
- `guidance_scale` (optional): Guidance scale, default 8.0
- `watermark` (optional): Whether to add watermark, default true
- `file_prefix` (optional): File name prefix, English only

**Supported Resolutions:**
- `512x512` - 512x512 (1:1 Small Square)
- `768x768` - 768x768 (1:1 Square)
- `1024x1024` - 1024x1024 (1:1 Large Square)
- `864x1152` - 864x1152 (3:4 Portrait)
- `1152x864` - 1152x864 (4:3 Landscape)
- `1280x720` - 1280x720 (16:9 Widescreen)
- `720x1280` - 720x1280 (9:16 Mobile Portrait)
- `832x1248` - 832x1248 (2:3)
- `1248x832` - 1248x832 (3:2)
- `1512x648` - 1512x648 (21:9 Ultra-wide)
- `2048x2048` - 2048x2048 (1:1 Ultra Large Square)

**Example Call:**
```json
{
  "tool": "doubao_generate_image",
  "arguments": {
    "prompt": "A cute orange cat sitting on a sunny windowsill, watercolor style",
    "size": "1024x1024",
    "guidance_scale": 8.0,
    "watermark": false,
    "file_prefix": "cute_cat"
  }
}
```

### MCP Resources

#### `resolutions`

Get a list of all available image resolutions.

### MCP Prompt Templates

#### `image_generation_prompt`

Provides prompt templates for image generation, including all parameter descriptions and usage examples.

## Standalone Testing

### Test Image Generation Tool

```bash
python doubao_image_gen.py
```

Note: Set correct API key and model ID in the code before testing.

## Project Structure

```
doubao_mcp_server/
├── doubao_mcp_server.py    # Main MCP server
├── doubao_image_gen.py     # Core image generation tool
├── .env.example            # Environment variable template
├── .env                    # Environment variable configuration (create yourself)
├── .gitignore             # Git ignore file
├── README.md              # Project documentation
├── pyproject.toml         # Project configuration and dependencies
├── uv.lock               # Dependency lock file
└── log/                  # Log file directory (auto-created)
    ├── doubao_mcp_server.log
    └── doubao_image_gen.log
```

## Logging System

The project includes a complete logging system:

- **File Logging**: Saved in `log/` directory
- **Console Logging**: Output to stderr for debugging
- **Log Levels**: DEBUG, INFO, WARNING, ERROR

## Error Handling

- ✅ Environment variable validation
- ✅ Parameter type and range checking
- ✅ API call error handling
- ✅ Image download retry mechanism
- ✅ File save exception handling

## Technical Features

- **Asynchronous Processing**: Async image generation based on asyncio
- **Retry Mechanism**: Automatic retry for failed image downloads
- **Parameter Validation**: Complete input parameter validation
- **Modular Design**: Core functionality separated from MCP service
- **Type Annotations**: Complete type hint support

## FAQ

### Q: How to get API key?
A: Visit Volcano Engine console and create a new API key in API management.

### Q: Where to find Model ID?
A: After creating an inference endpoint in Volcano Engine console, you can find the ID in endpoint details.

### Q: What image formats are supported?
A: Currently generated images are saved in JPG format.

### Q: How to customize image save path?
A: Modify the `IMAGE_SAVE_DIR` variable in the `.env` file.

### Q: What to do if generation fails?
A: Check log files and confirm that API key, model ID, and network connection are working properly.

## License

This project is open source under the MIT License.

## Contributing

Welcome to submit Issues and Pull Requests to improve the project
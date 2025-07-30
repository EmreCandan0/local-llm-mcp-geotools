# local-llm-mcp-geotools
Locally running LLM (Ollama + Phi3) integrated with MCP server for geospatial analysis, TIFF cropping, NDVI &amp; DEM computation.


A local AI-powered geospatial analysis system that uses a **locally hosted LLM (Ollama + Phi3)** and a **Model Context Protocol (MCP) server** to process natural language requests. The assistant understands user prompts and calls specialized tools for:

- GeoTIFF metadata analysis  
- Image cropping by geographic coordinates  
- NDVI (Normalized Difference Vegetation Index) computation  
- DEM (Digital Elevation Model) value retrieval


------------------------------


## 🔧 Key Features

- 🧠 **Local LLM integration** (Ollama + Phi3) — No internet or API keys required  
- 🔌 **MCP server-based tool-calling** architecture  
- 🗺️ **Geospatial image processing**: TIFF/JP2 analysis, NDVI, DEM, and cropping  
- 💬 **Natural language interface** — Users interact with simple text prompts  
- 📂 **FastAPI + FastMCP** backend with GDAL for geospatial operations  


------------------------------


## 🖼️ Example Use Cases

- “Analyze this TIFF file and show me the coordinates.”  
- “Crop the image between these lat/lon values.”  
- “Give me the NDVI value at this point.”  
- “What is the DEM elevation at this coordinate?”

---

## 🚀 Getting Started

### 1. Clone the Repository

git clone https://github.com/emrecandan0/local-llm-mcp-geotools.git

cd local-llm-mcp-geotools


2. Start the MCP Server
Make sure ports and paths are set correctly in the code.
python mcp_server.py


3. Launch the LLM Assistant (CLI)
Make sure Ollama is running and the Phi3 model is pulled.
ollama run phi3
python client.py


------------------------------

⚙️ Requirements
Python 3.9+

Ollama (with phi3 model)

GDAL

FastAPI

NumPy

Requests

MCP Server (via fastmcp)







------------------------------

📁 Project Structure

├── client.py           # Main CLI assistant (LLM + tool-calling)

├── mcp_server.py          # FastAPI MCP tool server with GDAL tools

├── functions/

│   └── funcs_pool.py      # Helper functions: geometry, EPSG, metadata

├── static/outputs/        # Output folder for cropped PNGs

└── temp/                  # Temporary files

------------------------------





📦 Tools Registered in MCP

analyze_tiff(filepath) → Returns metadata and extent

crop_image(filepath, minx, miny, maxx, maxy) → Saves PNG crop

get_ndvi(filepath, x, y) → Returns NDVI at coordinate

get_dem(filepath, x, y) → Returns DEM elevation at coordinate

------------------------------


🧪 Example Prompt (CLI)

➤ Request: Crop the image from minx: 790000, miny: 4080000, maxx: 800000, maxy: 4090000

🔧 crop_image tool is called...

✅ Result: static/outputs/myfile_cropped.png


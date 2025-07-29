# src/file_downloader/server.py
import os, urllib.parse
import httpx
from fastmcp import FastMCP

def main():
    mcp = FastMCP("file-downloader-stdio", version="0.1.0")

    @mcp.tool()
    async def download_file(url: str, output_path: str) -> dict:
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https"):
            return {"success": False, "error": "Invalid URL"}
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        try:
            async with httpx.AsyncClient() as client:
                resp = await client.get(url)
                resp.raise_for_status()
                with open(output_path, "wb") as f:
                    f.write(resp.content)
            return {"success": True, "path": output_path}
        except Exception as e:
            return {"success": False, "error": str(e)}

    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()

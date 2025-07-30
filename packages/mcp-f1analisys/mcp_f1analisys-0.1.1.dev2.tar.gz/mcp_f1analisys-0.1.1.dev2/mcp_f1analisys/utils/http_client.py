import httpx

class F1AnalysisClient:
    def __init__(self):
        self.client = httpx.AsyncClient(
            base_url="https://f1analisys-production.up.railway.app/api",
            timeout=httpx.Timeout(30.0, connect=10.0),
            limits=httpx.Limits(max_keepalive_connections=5, max_connections=10),
            follow_redirects=True
        )
    
    async def get_image(self, path: str) -> bytes:
        """Get image data from the F1 analysis API"""
        response = await self.client.get(path)
        response.raise_for_status()
        return response.content
    
    async def close(self):
        """Close the HTTP client"""
        await self.client.aclose()
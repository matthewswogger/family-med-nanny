import uvicorn
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()


if __name__ == '__main__':
    uvicorn.run(
        'fastapi_app.main:api',
        reload=True,
        reload_dirs=[str(Path(__file__).parent)]
    )

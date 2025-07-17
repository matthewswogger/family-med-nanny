from fastapi import APIRouter
from fastapi.responses import FileResponse

from utils import THIS_DIR


router = APIRouter()


@router.get('/')
async def index() -> FileResponse:
    file_path = THIS_DIR / 'frontend_files/chat_app.html'
    return FileResponse(path=file_path, media_type='text/html')


@router.get('/chat_app.ts')
async def main_ts() -> FileResponse:
    """
    Get the raw typescript code, it's compiled in the browser, forgive me.
    """
    file_path = THIS_DIR / 'frontend_files/chat_app.ts'
    return FileResponse(path=file_path, media_type='text/plain')

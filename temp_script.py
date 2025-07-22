import httpx
import os
import base64
from typing import Any
import asyncio
from dotenv import load_dotenv

load_dotenv()


def get_files_from_slack(urls: list[str]) -> tuple[list[str | None], list[tuple[str, str, Any] | None]]:
    '''
    Get files from Slack.
    - If the file is an image, we get the base64 encoded version of it.
    - If the file is not an image, we get the raw content of the file.
    - If something goes wrong, we add the url to the bad_urls list.
    '''
    SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
    headers = {'Authorization': f'Bearer {SLACK_BOT_TOKEN}'}

    bad_urls:   list[str | None] = []
    good_files: list[tuple[str, str, Any] | None] = []

    with httpx.Client() as client:
        for url in urls:
            response = client.get(url=url, headers=headers)
            if response.is_success:
                if response.headers['content-type'].startswith('image/'):
                    b64_encoded = base64.b64encode(response.content).decode('utf-8')
                    good_files.append((url, response.headers['content-type'], b64_encoded))

                else: # files, but not images, save for later I guess
                    good_files.append((url, response.headers['content-type'], response.content))

            else: # something went wrong, make sure we know what we didn't get
                bad_urls.append(url)

    return bad_urls, good_files


async def get_files_from_slack_async(urls: list[str]) -> tuple[list[str | None], list[tuple[str, str, Any] | None]]:
    '''
    Async version: Get files from Slack.
    - If the file is an image, we get the base64 encoded version of it.
    - If the file is not an image, we get the raw content of the file.
    - If something goes wrong, we add the url to the bad_urls list.
    '''
    SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
    headers = {'Authorization': f'Bearer {SLACK_BOT_TOKEN}'}

    bad_urls:   list[str | None] = []
    good_files: list[tuple[str, str, Any] | None] = []

    async with httpx.AsyncClient() as client:
        for url in urls:
            response = await client.get(url=url, headers=headers)
            if response.is_success:
                if response.headers['content-type'].startswith('image/'):
                    b64_encoded = base64.b64encode(response.content).decode('utf-8')
                    good_files.append((url, response.headers['content-type'], b64_encoded))

                else: # files, but not images, save for later I guess
                    good_files.append((url, response.headers['content-type'], response.content))

            else: # something went wrong, make sure we know what we didn't get
                bad_urls.append(url)

    return bad_urls, good_files


async def main(url_list: list[str]):
    bad_urls, good_files = await get_files_from_slack_async(url_list)
    return bad_urls, good_files


if __name__ == '__main__':
    list_of_urls = [
        'https://files.slack.com/files-pri/T0957BCU8C8-F097BBZM9FS/screenshot_2025-07-18_at_7.25.33___pm.png',
        'https://files.slack.com/files-pri/T0957BCU8C8-F0976CKFXHP/test_4.txt',
        'https://files.slack.com/files-pri/T0957BCU8C8-F096MSDELRZ/prescription_bottle_two.jpg',
        'https://files.slack.com/files-pri/T0957BCU8C8-F09le_two.jpg', # on purpose fake url
    ]

    # bad_urls, good_files = get_files_from_slack(list_of_urls)
    bad_urls, good_files = asyncio.run(main(list_of_urls))

    print('bad_urls:', len(bad_urls))
    print('good_files:', len(good_files))

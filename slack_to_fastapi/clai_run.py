import asyncio
from dotenv import load_dotenv

load_dotenv()


if __name__ == '__main__':
    from med_nannyai import main

    asyncio.run(main())

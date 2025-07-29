from dotenv import load_dotenv

if not hasattr(load_dotenv, '_loaded'):

    load_dotenv()
    load_dotenv._loaded = True
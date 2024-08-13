import os
from dotenv import load_dotenv
from supabase import create_client, Client


# Load environment variables from .env file
load_dotenv()

__URL: str = os.environ.get("SUPABASE_URL")
__KEY: str = os.environ.get("SUPABASE_KEY")
__SUPABASE: Client = create_client(__URL, __KEY)


def create_video(title, summary, caption, thumbnail, length, description):
    try:
        r= __SUPABASE.table('video').insert([
            {'title': title, 
             'summary': summary, 
             'caption': caption, 
             'thumbnail': thumbnail, 
             'length': length, 
             'description': description
            }]).execute()
        return r.data
    except Exception as e:
        print(e)

def create_quality(id, quality):
    try:
        r= __SUPABASE.table('quality').insert([
            {'id': id, 
             'quality': quality,
            }]).execute()
        return r.data
    except Exception as e:
        print(e)

def fetch_video():
    try:
        r= __SUPABASE.table('video').select('*').execute()
        return r.data
    except Exception as e:
        print(e)

def __main():
    print(__URL)
    print(__KEY)

if __name__ == "__main__":
    __main()

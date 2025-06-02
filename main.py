import os
import ssl
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
from newsplease import NewsPlease

#SSL Checker
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    # Legacy Python that doesn't verify HTTPS certificates by default
    pass
else:
    # Handle target environment that doesn't support HTTPS verification
    ssl._create_default_https_context = _create_unverified_https_context

#Create FastAPI app
app = FastAPI()

#Add allow CORS module
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


'''
Pydantic Basemodel for API Preparation
'''

class NewsUrl(BaseModel):
    url_input : str

@app.post("/")
def main(item: NewsUrl):

    try:
        article = NewsPlease.from_url(item.url_input)
        return {
            'status'        : 'SUCCESS',
            'content'       :  {
                                    'date'  : article.date_publish,
                                    'title' : article.title,
                                    'text'  : article.maintext
                                }
        }
    except:
        return {
                'status_code'   : 'ERROR',
                'content'       : 'ERROR'
                }
    
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))  # Render sets this automatically
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
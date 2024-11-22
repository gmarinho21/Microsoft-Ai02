import requests

from bs4 import BeautifulSoup
from langchain_openai.chat_models.azure import AzureChatOpenAI

def extrair_texto_da_url(url):
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            for script_or_style in soup(['script', 'style']):
                 script_or_style.decompose()
            texto = soup.get_text(separator = ' ')
            #Limpar Texto
            linhas = (line.strip() for line in texto.splitlines())
            parts = (phrase.strip() for line in linhas for phrase in line.split("  "))
            texto_limpo = '\n'.join(part for part in parts if part)
            print(texto_limpo)
            return texto_limpo
        else:
            print(f"Failed to fetch the URL. Status code: {response.status_code}")
            return None

client = AzureChatOpenAI(
    azure_endpoint = "ENTER YOUR ENDPOINT"
    api_key = "ENTER YOUR API KEY"
    api_version = "ENTER YOUR API VERSION"
    deployment_name = "gpt-4o-mini"
    max_retries=0
)

def translate_article(text, lang):
     messages = [
        ("system", "Voce atua como tradutor de textos"),
        ("user", f"Traduza o {text} para o idioma {lang} e responda em markdown")
     ]

     response = client.invoke(messages)
     print(response.content)
     return response.content

url = 'https://dev.to/shishsingh/how-to-perform-vnet-peering-in-azure-2315'
text = extrair_texto_da_url(url)
article = translate_article(text, "pt-br")
# langchain-digitalocean

This package contains the LangChain integration with LangchainDigitalocean

## Installation

```bash
pip install -U langchain-digitalocean
```

And you should configure credentials by setting the following environment variables:

* TODO: fill this out

## Chat Models

`ChatLangchainDigitalocean` class exposes chat models from LangchainDigitalocean.

```python
from langchain_digitalocean import ChatLangchainDigitalocean

llm = ChatLangchainDigitalocean()
llm.invoke("Sing a ballad of LangChain.")
```

## Embeddings

`LangchainDigitaloceanEmbeddings` class exposes embeddings from LangchainDigitalocean.

```python
from langchain_digitalocean import LangchainDigitaloceanEmbeddings

embeddings = LangchainDigitaloceanEmbeddings()
embeddings.embed_query("What is the meaning of life?")
```

## LLMs
`LangchainDigitaloceanLLM` class exposes LLMs from LangchainDigitalocean.

```python
from langchain_digitalocean import LangchainDigitaloceanLLM

llm = LangchainDigitaloceanLLM()
llm.invoke("The meaning of life is")
```

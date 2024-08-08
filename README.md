# ReWOO-with-Graph
> Clean code, clear mind, solutions you'll find.

## Introduction

This project aims to re-factor the implementation of the original [ReWOO](https://github.com/billxbf/ReWOO.git)'s setting into graph-based design. In addtion, the project evaluate the performance of ReWOO based on the `bigbench` and `SOTU` dataset. 

![](/assets/rewoo_workflow.png)

Why's ReWOO, you might ask? There are several factors that make ReWOO stands out: 

1. Reduce token consumption.
2. Reduce execution time.
3. Fine-tuning does not affect the whole system

## Features

+ Graph-based implementation of ReWOO. 
+ Evaluation with Ragas.

## Stack of Tech

- Lang-'s ecosystem: LangChain and LangGraph.
- Tavily Search.
- Groq. 
- Ollama.
- RAGAs.

## Getting started

**Set up environment**
1. Create `.env` file. 
2. Get api key from [Tavily](https://app.tavily.com/home), and [Groq](https://console.groq.com/keys).

_Note:_ For those who want to use Gemini or Ollama, make sure to get those API keys and install the relevant packages.

**Clone the repo and install requirements**

```
    git clone https://github.com/8Opt/ReWOO-with-Graph.git
    cd ReWOO-with-Graph
    pip install -r requirements.txt
```

**Ready to use**

All informtion of using the code is well-instructed in the `/assets/notebooks`.


## Notes
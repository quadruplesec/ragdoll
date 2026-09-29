# Ragdoll

A full-stack, containerized Retrieval-Augmented Generation (RAG) AI assistant built with FastAPI, LangChain, ChromaDB, and React, built strictly adhering to Test-Driven Development (TDD) principles.

## Project Overview

Ragdoll was engineered as an exercise in strict TDD while building a scalable, production-ready AI architecture. It demonstrates the complete lifecycle of a RAG pipeline, from chunking and embedding document data to dynamically routing user queries between specialized LLM chains.

This application provides a responsive interface for users to build a local knowledge base and query it in real-time. By leveraging Server-Sent Events (SSE) and asynchronous processing, the system streams LLM outputs directly to the client while maintaining a strict boundary between general conversation and document-grounded retrieval. The entire stack is containerized for seamless deployment in any environment.


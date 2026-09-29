# Ragdoll

[![CI Pipeline](https://github.com/quadruplesec/ragdoll/actions/workflows/ci.yml/badge.svg)](https://github.com/quadruplesec/ragdoll/actions/workflows/ci.yml)
[![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)](https://www.python.org/downloads/)
[![React Version](https://img.shields.io/badge/react-18.3+-blue.svg)](https://react.dev/)
[![License](https://img.shields.io/github/license/quadruplesec/ragdoll)](https://github.com/quadruplesec/ragdoll/blob/main/LICENSE)

A full-stack, containerized Retrieval-Augmented Generation (RAG) AI assistant built with FastAPI, LangChain, ChromaDB, and React, built strictly adhering to Test-Driven Development (TDD) principles.

## Project Overview

Ragdoll was engineered as an exercise in strict TDD while building a scalable, production-ready AI architecture. It demonstrates the complete lifecycle of a RAG pipeline, from chunking and embedding document data to dynamically routing user queries between specialized LLM chains.

This application provides a responsive interface for users to build a local knowledge base and query it in real-time. By leveraging Server-Sent Events (SSE) and asynchronous processing, the system streams LLM outputs directly to the client while maintaining a strict boundary between general conversation and document-grounded retrieval. The entire stack is containerized for seamless deployment in any environment.


# AI Product Recommendation Application

## Goal
Build a web-based MVP for an AI-powered product recommendation tool focusing on laptops, headphones, and cameras. The application differentiates itself through its "new buyer" education layer—guiding users with tailored questions and educating them on why certain product specs matter for their specific use cases (e.g., "Why sensor size matters more than megapixels").

## Proposed Architecture

### 1. Frontend Layer (Next.js)
* **Framework**: React via Next.js (Web-first approach, wrapped as PWA later if needed)
* **Purpose**: Provide a fast, beautiful conversational interface and visually structured product recommendations.
* **Key Components**:
  * Chat Interface: For natural language inputs and dynamic follow-up prompts.
  * Product Cards Output: Displaying images, prices, pros/cons, and specific educational blurbs.

### 2. Backend API Layer (FastAPI - Python)
* **Framework**: FastAPI
* **Purpose**: Fast, async processing to orchestrate the AI logic, data retrieval, and user sessions.
* **Key Features**:
  * Automatically generated API endpoints (Swagger UI).
  * Manages routing between the Frontend, Databases, and LLMs.

### 3. Data Storage & Search
* **Relational DB (PostgreSQL)**: To store user sessions, chat history, and basic system state.
* **Vector DB (Pinecone / Weaviate)**: To store product embeddings for semantic search (mapping descriptive text like "lightweight for students" to technical specs).
* **Caching (Redis)**: To cache frequent product queries and temporary session state for faster load times.

### 4. Product Data Pipeline
* **Structured Data**: Amazon Product Advertising API (or eBay API) to pull core specs, images, and pricing for the MVP categories.
* **Unstructured / Review Data (Fast Follow)**: Web scraping via Playwright or Scrapy to aggregate expert reviews and detailed specs from specialized sites (RTINGS, Tom's Guide).
* **Ingestion Job**: A scheduled Python pipeline to pull data, format it, generate context embeddings, and load them into PostgreSQL and the Vector DB.

### 5. AI / Conversation Engine (LLM + RAG)
* **Provider**: Claude or GPT-4 API (paired with LangChain/LlamaIndex).
* **Pipeline Flow**:
  1. **Intent Extraction**: User query is parsed to extract JSON structural parameters.
  2. **Follow-up / Routing**: If parameters are missing, the system generates smart, educational follow-up questions.
  3. **Retrieval**: Extracted parameters and embeddings query the Vector DB to find the most relevant products.
  4. **Generation & Education**: The LLM synthesizes the retrieved product data and user profile to construct a personalized recommendation that explicitly educates the user on *why* the product fits.

## MVP Scope (4-6 weeks)
* **Categories Supported**: Laptops, Headphones, Cameras.
* **Data Sources**: Start strictly with 1 structured source (e.g., Amazon API) for rapid validation.
* **Deliverables**:
  * Functional Web Chat Interface.
  * Backend Prompt chaining pipeline for Intent -> Follow-ups -> RAG -> Educational output.

---

## Task Tracking

- [x] **Phase 1: Planning & Setup**
  - [x] Create implementation plan and task breakdown
  - [x] Initialize Next.js frontend application structure
  - [x] Initialize FastAPI backend application structure
  - [x] Setup environment variables and database dependencies
- [ ] **Phase 2: Database & Core Data Modeling**
  - [ ] Setup PostgreSQL for User & Session Management
  - [ ] Setup Vector Database (Pinecone/Weaviate) for semantic product search
  - [ ] Setup Redis for caching
  - [ ] Define database schemas and Pydantic models in FastAPI
- [ ] **Phase 3: Product Data Pipeline (MVP)**
  - [ ] Integrate Affiliate APIs (e.g., Amazon Product Advertising API) for laptops, headphones, cameras
  - [ ] Build basic web scraper for supplementary reviews/specs (Optional for V1)
  - [ ] Implement data ingestion script to populate PostgreSQL and Vector DB
- [ ] **Phase 4: AI & Conversation Layer**
  - [ ] Set up LLM integration (Claude or GPT-4 API)
  - [ ] Implement query classification Prompt (identify category, budget, user experience)
  - [ ] Implement RAG pipeline (retrieving products from Vector DB based on query context)
  - [ ] Implement educational recommendation extraction Prompt
- [ ] **Phase 5: Backend API Layer**
  - [ ] Create `/chat` endpoint handling the conversational pipeline
  - [ ] Create session/history management endpoints
- [ ] **Phase 6: Frontend Implementation**
  - [ ] Setup styling (Tailwind CSS/custom CSS)
  - [ ] Build chat interface UI
  - [ ] Build product presentation cards (showing Pros/Cons and "Why this matters")
  - [ ] Integrate with Backend API
- [ ] **Phase 7: Review & Polish**
  - [ ] End-to-end testing of the 3 MVP categories
  - [ ] Refine LLM prompts for educational quality
  - [ ] UI/UX polishing

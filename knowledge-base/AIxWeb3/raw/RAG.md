## Notes

- RAG is an **evidence chain** that retrieves external knowledge, filters it, cites it, and gives it to the model so the system can reduce outdated knowledge and unsourced answers.
- **The core of RAG** is not to make answers longer. **It is to make answers sourced, versioned, and bounded**
	- **RAG without citation and freshness only moves hallucination from inside the model into the retrieval system.**
- Many RAG demos only reach "we can retrieve some paragraphs"; but **they have not reached "the answer can be verified."**
- A RAG system makes at least three judgments:
	1. how documents are chunked
	2. what content is retrieved for a query
	3. how the answer cites or refuses to answer
* **Retrieved results are not facts**: they are candidate evidence, and you still need to check source, time, version, and applicability.
- **Citations must return to the original source**: key claims in the answer should trace back to a specific document, paragraph, or on-chain record.
- **Retrieval failure must allow refusal**: when evidence cannot be found, the system should say "uncertain" instead of letting the model fill the gap.
- **Concepts**
	- **Chunking**: splits long documents into retrievable pieces
		- with small chunks -> semantic breaks
		- with bigger chunks -> results are noisy and token costs rises
		- Technical documentation needs especially careful chunking
		- A steadier approach is to split by document structure
			- Each chunk should preserve source URL, heading path, update time, and version
	- **Vector DB**: stores embeddings and retrieves related chunks by similarity.
		- Vector similarity does not mean the answer is correct.
			- e.g. outdated docs
		- **Filter first, then rank** -> **It should not store only vectors. It should also store metadata**: source, version, chain, update time, trust level, and deprecation status
	- **Retriever**: component that returns candidate material based on the user's question
		- vector/keyword-based, hybrid, graph-based, metadata filters
		- **A good retriever cannot look only at semantic similarity**
			- **if the user question contains a version, environment, time, address, or concrete object, your retriever should not rely only on pure vector search**
	- **Re-rank**: reorders candidate material, moving more relevant, trusted, and complete content to the front
		- Rerank adds latency and cost, so it depends on the scenario
	- **Citations**: connect key   in the answer back to sources
		- It's the user's entry point for verifying the answer
		- In technical Q&A, **citation should at least explain**:
			- which document a statement came from
			- whether the source is official
			- document version or update time
			- which conclusions are model summaries
			- where evidence is insufficient
* **Where It Fits in AI x Web3**
	* RAG sits between the Knowledge Base and the model
	* It helps Agents look up material, fill context, and cite evidence,  .
	* When RAG results affect on-chain actions, they still need simulation, policy, and human check
	* Common uses include:
		- protocol documentation Q&A
		- contract interface explanation
		- governance proposal and forum summaries
		- audit report retrieval
		- SDK / API copilot
		- adding project background during transaction interpretation
## Must-read

- [OpenAI File Search Guide](https://platform.openai.com/docs/guides/tools-file-search): learn how hosted file retrieval connects external material to model workflows.
- [LangChain Retrievers](https://docs.langchain.com/oss/python/integrations/retrievers/index): see common retrievers, vector databases, rerankers, and hybrid retrieval integrations.
- [Pinecone RAG Guide](https://docs.pinecone.io/guides/get-started/build-a-rag-chatbot): useful for seeing a RAG data flow from the perspective of a vector database.

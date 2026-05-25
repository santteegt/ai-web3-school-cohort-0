## Notes

* The core of an inference service is on **delivering a usable answer under constraints.**
* Inference determines how the model responds to users in a real product
* Inference is a combined choice across latency, cost, context, stability, quality, privacy, operational complexity and deployment boundaries
	* **Quality has a cost**: stronger models usually mean higher cost, longer latency, or more complex deployment.
	- **Deployment changes boundaries**: API models reduce infrastructure burden; local models give you more control.
	- **Services should be replaceable**: clear model-call encapsulation makes fallback, rollout, and evaluation possible.
* The inference layer determines how model capability is consumed by the product
* It connects upstream models, prompts, RAG, and Agents, and downstream interfaces, queues, caches, monitoring, and UX
* **Concepts**
	* **API Model**: understand what parameters and limits they have, and how their cost structure works
		* API does not mean "no engineering problems." You still need to handle rate limits, timeouts, retries, log redaction, billing control, version changes, and output regression
	* **Local Model**: gives you more control but it demands more hardware, deployment, and tuning ability
		* fits scenarios with high privacy requirements, cost sensitivity, offline operation, or deep customization needs
		* model weights, VRAM, context window, concurrency, quantization method, and inference framework all affect quality
	* **Quantization**: makes running large models on smaller devices possible. It trades off model size, inference speed, and output quality
		* reduces model weights or computation precision, such as going from FP16 to INT8 or INT4, so the model can run with less VRAM and compute
		* **It may reduce output quality**, especially in long reasoning, code generation, multilingual tasks, math, and tool calls
		* Whether a quantized model is usable or not, it should be tested on your own task samples.
	* **Serving**: it usually involves model loading, request queues, batching, GPU utilization, token streaming, logs, metrics, health checks, and scaling
		* A mature inference service should at least answer:
			- How are failed requests retried or degraded?
			- How are model versions rolled out gradually?
			- How are input and output logs redacted?
			- Should long requests enter a queue?
			- How are cost, latency, and error rate monitored?
* **Where It Fits in AI x Web3**
	* The inference layer directly affects whether users can safely wait for results, whether they are willing to pay the cost, and whether Agents can complete pre-chain checks in a reasonable time.
	* On-chain actions are hard to reverse, so **the inference service must leave auditable records**
		* which model was used, where inputs came from, what the output was, whether tools were triggered, and how failures were handled

# Large Model Technology and Development

[Original deck](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter1/dive-into-llm.pdf)

## Slide 1

**Large Model Technology and Development**

张倬胜 (Zhang Zhuosheng)

上海交通大学计算机学院 (SJTU School of Computer Science)

zhangzs@sjtu.edu.cn

<https://bcmi.sjtu.edu.cn/~zhangzs>

## Slide 2

**Contents**

- Overview of large models
    - Overview of their development
    - Scope of the concept
- Pre-trained models
    - Main types
    - Model architecture
- Large-scale models
    - Paradigm shifts
    - Main representatives
    - Key technologies
    - Deployment methods
- Concept extensions
    - Vertical large models
    - Multimodal foundation models
    - Agent foundation models

## Slide 3

**Contents**

- Overview of large models
    - Overview of their development
    - Scope of the concept
- Pre-trained models
    - Main types
    - Model architecture
- Large-scale models
    - Paradigm shifts
    - Main representatives
    - Key technologies
    - Deployment methods
- Concept extensions
    - Vertical large models
    - Multimodal foundation models
    - Agent foundation models

## Slide 4

**The development of artificial intelligence**

- Artificial intelligence (AI) technology has gone from small data to big data, from small models to large models, and from specialized to general-purpose, and is gradually entering the era of large models
- Large-scale self-supervised pre-training on massive unlabeled data learns a great deal of linguistic knowledge and world knowledge
- Models complete many kinds of tasks through natural-language interaction and can handle tasks across many scenarios, many purposes and many disciplines

*In the figure:* Concept extensions · Domain-specific large models · Multimodal foundation models · Agent foundation models

[1] Zhao, Wayne Xin, et al. A Survey of Large Language Models. arXiv preprint arXiv:2303.18223.

## Slide 5

**The scope of large models**

*In the figure:* Large language models (LLMs) · Domain-specific large models · Multimodal foundation models · Pre-trained language models · Agent foundation models

## Slide 6

**Contents**

- Overview of large models
    - Overview of their development
    - Scope of large models
- Pre-trained models
    - Main types
    - Model architecture
- Large-scale models
    - Paradigm shifts
    - Main representatives
    - Key technologies
- Concept extensions
    - Vertical large models
    - Multimodal foundation models
    - Agent foundation models

## Slide 7

**Pre-trained language models**

- A new paradigm for language intelligence: pre-trained language models (representatives: ELMo, BERT, GPT-1/2)
    - Self-supervised pre-training on large-scale data, then adaptation to all kinds of tasks after fine-tuning, making effective use of big data, large models and large-scale compute
    - Mainly applied to language analysis and understanding tasks

[1] Zhang, Zhuosheng, et al. Machine Reading Comprehension: The Role of Contextualized Language Models and Beyond. arXiv preprint arXiv:2005.06249.

## Slide 8

**Main types**

- Encoder models (Encoder-Only)
- Decoder models (Decoder-Only)
- Encoder-decoder models (Encoder-Decoder)

How attention to each type of model has changed over time

- Before about 2021, derivatives of encoder models and encoder-decoder models kept appearing. These versions were jokingly called "BERTology"
- After about 2021, decoder models developed rapidly, ushering in the "Next-Level" era of generative large models

[1] Rogers, Anna, et al. A primer in BERTology: What we know about how BERT works. TACL, 2021. [2] Minaee, Shervin, et al. Large language models: A survey. arXiv preprint arXiv:2402.06196.

## Slide 9

**From the perspective of pre-training modeling**

- From the angle of self-supervised pre-training modeling, different architectures have different training objectives
    - Encoder models: masked language modeling (Masked Language Modeling)
    - Decoder models: autoregressive language modeling (Auto-regressive Language Modeling)
    - Encoder-decoder models: sequence-to-sequence modeling (Sequence to Sequence Modeling)

[1] Ding, Ning, et al. Parameter-efficient fine-tuning of large-scale pre-trained language models. Nature Machine Intelligence, 2023.

## Slide 10

**Encoder models**

- Main training objective: masked language modeling (Masked Language Modeling, MLM)
- Representative models: BERT, RoBERTa, ALBERT

*In the figure:* outputs `NotNext` · `learn`; Transformer Encoder; input `[CLS] | let | us | together | get hands-on | [MASK] | large model | development | full workflow`

## Slide 11

**Decoder models**

- Main training objective: autoregressive language modeling (Auto-regressive Language Modeling)
- Representative models: the GPT, Llama and PaLM series, etc.

*In the figure:* outputs `let | us | together | get hands-on | learn | large model | key | technologies`; Decoder; input `[BOS] | let | us | together | get hands-on | learn | large model | key`

## Slide 12

**Pros and cons compared**

| Encoder models (BERT) | Decoder models (GPT) |
|---|---|
| Pros: uses bidirectional context, good at language understanding | Pros: naturally suited to generation tasks; large-scale training data is easy to build |
| Cons: the special [mask] symbol causes a pre-training/fine-tuning mismatch; assumes all masked tokens are independent of each other | Cons: limited to unidirectional modeling; hard to use bidirectional context at the same time |

## Slide 13

**Encoder-decoder models**

- Main training objective: sequence-to-sequence modeling (Sequence to Sequence Modeling)
- Representative models: T5, BART

*In the figure:* the Decoder produces `<X> get hands-on <Y> large model <Z>`; the Encoder reads `let us together <Y> learn <Y> large model key technologies`

## Slide 14

**Choosing a model for the application scenario**

| Encoder models | Decoder models | Encoder-decoder models |
|---|---|---|
| Discriminative tasks such as classification and regression | Suited to open-ended generation tasks | Both discriminative and generative abilities |

## Slide 15

**Pre-trained language models: model architecture**

- RNN (LSTM)
    - Captures dependencies between words. But because of gradient computation problems, RNNs are often hard to train
    - Computation is very slow, and the ability to learn long-range dependencies is limited
- Transformer √ (Attention is all you need)
    - Drops the RNN recurrence entirely and uses self-attention for global processing
    - Three weight matrices (Query, Key and Value) capture contextual dependencies
    - Multi-layer network: each layer consists of multi-head attention and a feed-forward network
    - Adds positional encoding (Positional Encoding)

## Slide 16

**Contents**

- Overview of large models
    - Overview of their development
    - Scope of large models
- Pre-trained models
    - Main types
    - Model architecture
- Large-scale models
    - Paradigm shifts
    - Key technologies
    - Main representatives
    - Deployment methods
- Concept extensions
    - Vertical large models
    - Multimodal foundation models
    - Agent foundation models

## Slide 17

**Large models at a glance**

[1] Zhao, Wayne Xin, et al. A Survey of Large Language Models. arXiv preprint arXiv:2303.18223.

## Slide 18

**Paradigm shifts in the era of large models**

- Shift in the technical paradigm: from specialized training for each separate task to the centralized "pre-training + post-training" and "pre-training + prompting"
- Unification of the task paradigm: from separate, task-specific forms toward a unified sequence-to-sequence modeling form

| Past | Now (training) | Now (application) |
|---|---|---|
| For each task, each user builds a model on their own and does all of the machine learning training themselves | A central node does general large-scale pre-training and provides a nearly finished model, which serves as a standard module for post-training (instruction tuning / reinforcement learning) to fit a wide range of scenarios | Prompt engineering: in-context learning, chain-of-thought prompting, workflow orchestration; lightweight training |
| *In the figure:* individualized training | *In the figure:* + post-… | |

## Slide 19

**Paradigm shifts in the era of large models**

- Shift in the technical paradigm: from specialized training for each separate task to the centralized "pre-training + post-training" and "pre-training + prompting"
- Unification of the task paradigm: from separate, task-specific forms toward a unified sequence-to-sequence modeling form

[1] Chung, H.W., et al. Scaling instruction-finetuned language models. JMLR, 2024.

## Slide 20

**Large language models**

- Large language models (LLMs): powerful algorithms consume a large amount of compute to train a complex probability distribution function from massive data
    - More computation, higher inference cost
    - Stronger generalization, with emergent abilities

| Comparison | Pre-trained language models (small and medium models, conventional models) | Larger-scale language models (generative large models) |
|---|---|---|
| Typical models | ELMo, BERT, GPT-1/2 | GPT-3, ChatGPT, LLaMA |
| Model structure | RNN, Transformer | Transformer |
| Attention mechanism | Bidirectional, unidirectional | Unidirectional |
| Training method | Denoising autoencoder models | Autoregressive generation |
| Task types they are good at | Understanding, judgment | Generation |
| Model scale | Below about 10B parameters | About 10B-100B parameters and above |
| How they are applied to downstream tasks | Fine-tuning | Fine-tuning & prompting |
| Emergent abilities | Transfer to low-data domains | In-context learning, chain-of-thought prompting |

[1] Minaee, Shervin, et al. Large language models: A survey. arXiv preprint arXiv:2402.06196.

## Slide 21

**Large language models**

- Training data: diversified
    - No longer just natural-language text but a combination of many kinds of data: natural-language text, programming code, chemical formulas, even gene sequences, and even images
- Training method: a full shift from discriminative pre-training (BERT is typical) to generative pre-training (GPT is typical)
- Model architecture: from bidirectional Transformers to unidirectional Transformers (Decoder-only)
- How they are applied: from fine-tuning to friendlier prompting
    - Fewer examples: from requiring a certain amount of labeled examples, to few-shot, and even zero-shot
    - The way prompting works comes close to human-machine dialogue

## Slide 22

**Key technologies**

- The three classic main construction stages: pre-training, instruction tuning, alignment

| | Pre-training | Instruction tuning | Alignment |
|---|---|---|---|
| Data | Raw data: text at the hundred-billion scale, books, web pages, code, etc. | Labeled user instructions: tens of thousands of user instructions in natural language with their answers | Labeled comparison pairs: hundreds of thousands to millions of labeled comparison pairs, with user instructions |
| Model | Base model | SFT model | Aligned model |
| Goal | Learn domain/general knowledge | Improve instruction-following ability | Generate safer instructions |
| | Training time on the order of months | Training time on the order of days | Training time on the order of days |

## Slide 23

**The large model building pipeline**

| | Pre-training | Instruction tuning | Alignment |
|---|---|---|---|
| Data | Raw data: text at the hundred-billion scale, books, web pages, code, etc. | Labeled user instructions: tens of thousands of user instructions in natural language with their answers | Labeled comparison pairs: hundreds of thousands to millions of labeled comparison pairs, with user instructions |
| Model | Base model | SFT model | Aligned model |
| Goal | Learn domain/general knowledge | Improve instruction-following ability | Generate safer instructions |
| | Training time on the order of months | Training time on the order of days | Training time on the order of days |

## Slide 24

**Key technology 1: pre-training**

*In the figure:* Algorithms · Data · Compute

## Slide 25

**Key technology 2: instruction tuning**

- Fine-tune the model on high-quality instruction data (which tells the model what task to perform)
    - Helps the model understand the characteristics of tasks and greatly improves its performance on each task
    - Improves the stability of prompting and makes the model's output text more controllable
- Taking "natural language inference" (NLI) as an example, build instruction-tuning training data

*In the figure:* Regular fine-tuning · Instruction tuning

## Slide 26

**Key technology 2: instruction tuning**

- Ways to do instruction tuning
    - Using existing datasets: humans add a prompt that states the current task type as a prefix to the input (the instruction), then fine-tune on many types of datasets
    - Supervised fine-tuning on human demonstrations: humans write high-quality answers to prompts (instructions), and the model is supervised fine-tuned on them
- Key points in building the data
    - Number of tasks
    - Task diversity

*In the figure:* Using existing datasets (FLAN) · Based on human demonstrations (InstructGPT)

Wei, Jason, et al. "Finetuned Language Models are Zero-Shot Learners." International Conference on Learning Representations. 2021.

## Slide 27

**Key technology 2: instruction tuning**

- FLAN instruction tuning: uses instruction tuning to improve the model's zero-shot ability
    - Groups 62 natural language processing tasks into 12 categories
    - For each task, manually writes 10 distinct instruction templates
- The gains from instruction tuning show a clear large-model effect
    - Only when the model reaches around ten billion parameters does instruction tuning improve performance on held-out tasks

Wei, Jason, et al. "Finetuned Language Models are Zero-Shot Learners." International Conference on Learning Representations. 2021.

## Slide 28

**Key technology 3: alignment**

- LLMs often generate unhelpful, toxic or untruthful answers
- With relatively little human effort, use reinforcement learning methods to further fine-tune the LLM
    - Make the LLM's outputs "aligned" with human intentions, producing answers people like
    - The more a language model's outputs match human intentions and ethical standards, the more reward the model receives
- Greatly reduces harmful and false outputs

*In the figure:*

- User: asks how to break into a house
- ChatGPT: points out that this is inappropriate and could lead to a crime
- User: changes the story, saying they only want to protect their own house from break-ins
- ChatGPT: gives 7 specific suggestions

## Slide 29

**Key technology 3: alignment**

- "Alignment" with human preferences, values, intentions, safety and so on
    - Definition: steering the behavior of AI systems so that it matches the interests and intended goals of their designers
- The Chinese government has issued the *Provisions on the Administration of Deep Synthesis Internet Information Services* and the *Interim Measures for the Management of Generative Artificial Intelligence Services*

*In the figure:* ChatGPT has already been used for crime: cyberattacks, criminal guidance, etc. · Deep synthesis services must not be used to produce, copy, publish or spread false information; deep synthesis services must not be used to produce, copy, publish or spread information prohibited by laws and administrative regulations

## Slide 30

**Key technology 3: alignment**

- Principles: helpful, honest and harmless
    - Consistent with national and regional culture, laws and regulations, and ethics; grounded in facts and logic
- Technical points:
    - Datasets: SFT dataset (13k), RM dataset (33k), RL dataset (31k)
    - Models: SFT supervised fine-tuning model, RM reward model, RL reinforcement learning model

Ouyang, Long, et al. "Training language models to follow instructions with human feedback." Advances in Neural Information Processing Systems 35 (2022): 27730-27744.

## Slide 31

**Key technology 3: alignment**

Step 1: Supervised fine-tuning (SFT)

*In the figure:* "What is the moon?" · Data sampled and collected through the API · SFT model · 175B GPT-3 · "A spherical celestial body that orbits the Earth" · Labeled target answer

Ouyang, Long, et al. "Training language models to follow instructions with human feedback." Advances in Neural Information Processing Systems 35 (2022): 27730-27744.

## Slide 32

**Key technology 3: alignment**

Step 2: Reward modeling (RM)

*In the figure:* "What is the moon?" · SFT model · Pre-trained 175B GPT-3 · "A. The moon is the celestial body in the solar system closest to the Earth." … "D. The moon is the Earth's satellite, with a diameter of about 1/4 of the Earth's." · 6B model (cheap + stable) · RM model · Ranking model (question + answer → outputs a score) · D>C>A=B

Ouyang, Long, et al. "Training language models to follow instructions with human feedback." Advances in Neural Information Processing Systems 35 (2022): 27730-27744.

## Slide 33

**Key technology 3: alignment**

Step 2: Reward modeling (RM)

*In the figure:* "What is the moon?" · SFT model · Pre-trained 175B GPT-3 · "A. The moon is the celestial body in the solar system closest to the Earth." … "D. The moon is the Earth's satellite, with a diameter of about 1/4 of the Earth's." · RM model · D>C>A=B

*Formula labels:* the two answers for question x in the dataset, where yw ranks higher than yl · The question in the dataset · Difference between the RM model's scores

Ouyang, Long, et al. "Training language models to follow instructions with human feedback." Advances in Neural Information Processing Systems 35 (2022): 27730-27744.

## Slide 34

**Key technology 3: alignment**

Step 3: Reinforcement learning (RL)

*In the figure:* "What is room-temperature superconductivity?" · yl · SFT model · RL model · RM model · PPO

Note: PPO, Proximal Policy Optimization

Ouyang, Long, et al. "Training language models to follow instructions with human feedback." Advances in Neural Information Processing Systems 35 (2022): 27730-27744.

## Slide 35

**Key technology 3: alignment**

Step 3: Reinforcement learning (RL)

*In the figure:* "What is room-temperature superconductivity?" · yl · SFT model · RL model · RM model · PPO · Loss function of the original language model · InstructGPT

Note: PPO, Proximal Policy Optimization

Ouyang, Long, et al. "Training language models to follow instructions with human feedback." Advances in Neural Information Processing Systems 35 (2022): 27730-27744.

## Slide 36

**Key technology 3: alignment**

## Slide 37

**The scaling law of large language models (Scaling Law)**

- The relationship between model performance and three factors: model size, data scale and compute
    - As the number of model parameters and the scale of pre-training data keep growing, model capability and task performance improve accordingly
    - Chinchilla recommendation: a 10B model with 200B tokens (1:20)

[1] Kaplan, Jared, et al. Scaling laws for neural language models. arXiv preprint arXiv:2001.08361.

## Slide 38

**Emergent abilities of large language models (Emergent Abilities)**

- When a language model's parameters reach a certain scale, some abilities (language reasoning) suddenly improve sharply
- Abilities not observed in small models but shown by large models

*In the figure:* Representative emergent abilities: in-context learning · chain-of-thought reasoning

[1] Wei, Jason, et al. Emergent Abilities of Large Language Models. TMLR, 2022.

## Slide 39

**Hallucination in large language models (Hallucination)**

- Definition: text generated by the model does not follow the source text (Faithfulness) or does not match the facts (Factualness)
- The upside: a sign of large models' creativity and divergent thinking
- Potential impact: undermines the model's trustworthiness, makes it easy to attack and to misuse (e.g. generating malicious content and spreading rumors), and pollutes the internet

*In the figure:*

- Q: Are Lu Xun and Zhou Shuren the same person?
- A: No. Lu Xun and Zhou Shuren are two different people. Lu Xun was a giant of modern Chinese literature, known for his unique literary style and engaging stories. Zhou Shuren is a famous contemporary Chinese writer, admired for his incisive writing and keen observation.

[1] Huang, Lei, et al. A survey on hallucination in large language models: Principles, taxonomy, challenges, and open questions. arXiv preprint arXiv:2311.05232

## Slide 40

**The capability map of large models**

[1] Minaee, Shervin, et al. Large language models: A survey. arXiv preprint arXiv:2402.06196.

## Slide 41

**From GPT-3 to ChatGPT**

- GPT-1: unidirectional autoregressive modeling + supervised fine-tuning; explored the ability to solve natural-language tasks under the "pre-training + fine-tuning" paradigm
- GPT-2: unidirectional autoregressive modeling + more data and a bigger model; explored the ability to solve multiple tasks from natural-language prompts
- GPT-3: explored the performance of a language model with hundreds of billions of parameters and proposed a task-solving method based on "in-context learning"
- GPT-3.5/ChatGPT: instruction tuning + human feedback + dialogue optimization
- GPT-4: multimodal abilities, longer context understanding and processing, more efficient training and prediction, broader high-value application scenarios

*In the figure:* 45TB of data · Evolution of the GPT series

## Slide 42

**How the GPT series evolved across versions**

- GPT-4 performs at a human level on a range of professional and academic benchmarks, including passing a simulated bar exam with a score around the top 10% of test takers
- Strong multimodal processing broadens GPT-4's range of applications, and generative hallucination and safety problems are much improved

OpenAI publishes a GPT-4 usage guide

- Write clear instructions
- Provide reference text
- Split complex tasks into simpler subtasks
- Give the model time to "think"
- Use external tools
- Test changes systematically

[1] Achiam, Josh, et al. Gpt-4 technical report. arXiv preprint arXiv:2303.08774.
[2] OpenAI. Prompt engineering. <https://platform.openai.com/docs/guides/prompt-engineering>.

## Slide 43

**The Llama series of large models**

- Open-source autoregressive models based on the Transformer architecture, with 7B to 405B parameters
- Commercial license: Llama 1 cannot be used commercially for free; Llama 2 and Llama 3 can be used commercially (a commercial license must be requested)

| Version features | Llama-1 | Llama-2 | Llama-3 | Llama-3.1 | Llama-3.2 |
|---|---|---|---|---|---|
| Model scale | 7B-65B | 7B-70B | 8B-70B | 8B-405B | 1B-90B |
| Data scale | 1.4T | 2T | 15T | 15T | 9T |
| Multimodal | × | × | × | × | √ |
| Multilingual | × | × | × | √ | √ |
| Tool calling | × | × | × | √ | √ |
| Training paradigm | Pre-training | Pre-training + instruction tuning + RLHF | Pre-training + instruction tuning + DPO | Pre-training + instruction tuning + DPO | Pre-training + instruction tuning + DPO |
| Context length | 2K | 4k | 8k | 131K | 131K |
| Main changes | -- | Added post-training | Scaled up pre-training | 1. Larger model scale; 2. Added multilingual and tool abilities; 3. Longer context length | 1. Added on-device models; 2. Added multimodal abilities |

[1] Touvron, Hugo, et al. Llama: Open and efficient foundation language models. arXiv preprint arXiv:2302.13971.
[2] Touvron, Hugo, et al. Llama 2: Open foundation and fine-tuned chat models. arXiv preprint arXiv:2307.09288.
[3] Dubey, Abhimanyu, et al. The llama 3 herd of models. arXiv preprint arXiv:2407.21783.

## Slide 44

**The Llama series of large models**

- Training data: CommonCrawl, C4, Github, Wikipedia, books, ArXiv, and StackExchange, etc.
- Open-source repository: <https://github.com/facebookresearch/llama>
- Llama 3.1 405B beats GPT-3.5 Turbo across a wide range of evaluations and outscores GPT-4 0125 on most benchmarks

[1] Dubey, Abhimanyu, et al. The llama 3 herd of models. arXiv preprint arXiv:2407.21783.

## Slide 45

**Categories of Chinese (domestic) AI large models and typical cases**

- The "battle of a hundred models": by incomplete count, as of the end of 4/2024 (April 2024), 305 large models had been released in China

[1] SuperGLUE team. Chinese Large Model Benchmark Evaluation: 2024 Annual Report.

## Slide 46

**The Qwen series of large models**

- Qwen (Tongyi Qianwen) is a pre-trained language model developed by Alibaba Cloud. It performs tasks such as understanding, generating and explaining human language, images and documents, and gives users a rich interactive experience in creative copywriting, office assistance, study help, everyday fun and more
- Has Chinese and English understanding, mathematical reasoning, code understanding and other abilities

*In the figure:* Qwen-Audio · Qwen-Audio-Chat

[1] Bai, Jinze, et al. Qwen technical report. arXiv preprint arXiv:2309.16609.
[2] Yang, An, et al. Qwen2 technical report. arXiv preprint arXiv:2407.10671.

## Slide 47

**How the Qwen series evolved across versions**

- Qwen1.5: Model Scaling toward both larger and smaller sizes, MoE, AWQ/GGUF
- Qwen2: stronger multilingual ability, stronger long-text ability
- Qwen2.5: stronger math and code abilities, stronger multilingual ability
- Scaling
    - Qwen: 1.8B, 7B, 14B, and 72B models
    - Qwen1.5: 0.5B, 1.8B, 4B, 14BA2.7B, 7B, 14B, 32B, 72B, and 110B models
    - Qwen2: 0.5B, 1.5B, 7B, 57A14B, and 72B models
    - Qwen2.5: 0.5B, 1.5B, 3B, 7B, 14B, 32B, and 72B models

Features of the version updates

- Structural optimization (MoE improves training efficiency)
- More pre-training data, and of higher quality
- Richer tasks and domains covered in the Post-training stage
- Longer window length (in both training data and training strategy)
- More language directions and stronger multilingual ability
- Stronger specialized abilities (train expert models + use the expert models to lift the base model)
- Modality expansion (Qwen-VL, Qwen-Audio)

## Slide 48

**The DeepSeek series of large models**

2023.11

1. DeepSeek LLM
    - Parameters: 70B, 67B parameters
    - Architecture: Dense Transformer model
    - Training data: 2T tokens of Chinese and English corpus
    - Training paradigm: follows the standard large model training paradigm of pre-training + SFT + DPO
    - Performance: DeepSeek's first large model, benchmarked against the Llama2 series. The 67B Base version surpassed Llama2 70B Base in reasoning, coding and more. The model architecture uses a Dense structure

## Slide 49

**The DeepSeek series of large models**

2023.11 · 2024.5

1. DeepSeek LLM
    - Parameters: 70B, 67B parameters
    - Architecture: Dense Transformer model
    - Training data: 2T tokens of Chinese and English corpus
    - Training paradigm: follows the standard large model training paradigm of pre-training + SFT + DPO
    - Performance: DeepSeek's first large model, benchmarked against the Llama2 series. The 67B Base version surpassed Llama2 70B Base in reasoning, coding and more. The model architecture uses a Dense structure
2. DeepSeek-V2
    - Parameters: 236B parameters, 21B activated parameters
    - Architecture: introduces the DeepSeekMoE (mixture of experts) architecture. Introduces MLA (Multi-head Latent Attention)
    - Training data: 8.1T tokens of corpus
    - Training paradigm: follows the standard paradigm of pre-training + SFT + reinforcement learning
    - Features: performance on par with GPT-4 Turbo. MLA saves more than 90% of the KV cache and makes inference more than 5 times faster. With the MoE architecture, inference cost stays almost unchanged as model parameters grow, and training cost drops sharply, improving model capability

## Slide 50

**The DeepSeek series of large models**

2024.5 · 2024.9

2. DeepSeek-V2
    - Parameters: 236B parameters, 21B activated parameters
    - Architecture: introduces the DeepSeekMoE (mixture of experts) architecture. Introduces MLA (Multi-head Latent Attention)
    - Training data: 8.1T tokens of corpus
    - Training paradigm: follows the standard paradigm of pre-training + SFT + reinforcement learning
    - Features: performance on par with GPT-4 Turbo. MLA saves more than 90% of the KV cache and makes inference more than 5 times faster. With the MoE architecture, inference cost stays almost unchanged as model parameters grow, and training cost drops sharply, improving model capability
3. DeepSeek-V2.5
    - Based on V2, mainly optimizes general task abilities and code abilities

## Slide 51

**The DeepSeek series of large models**

2024.9 · 2024.12

3. DeepSeek-V2.5
    - Based on V2, mainly optimizes general task abilities and code abilities
4. DeepSeek-V3
    - Parameters: 671B parameters, 37B activated parameters
    - Training data: 14.8T tokens of corpus
    - Architecture: building on V2, introduces an Auxiliary-loss-free strategy for expert load balancing. Introduces Multi-Token Prediction training to improve model performance and speed up inference. Introduces FP8 mixed precision to cut training and inference costs
    - Training data: 14.8T tokens of corpus
    - Training paradigm: follows the standard large model training paradigm of pre-training + SFT + DPO
    - Features: performance surpasses the mainstream Llama3 and Qwen2.5 series, with much lower training and inference costs

## Slide 52

**The DeepSeek series of large models**

2024.12 · 2025.01

4. DeepSeek-V3
    - Parameters: 671B parameters, 37B activated parameters
    - Training data: 14.8T tokens of corpus
    - Architecture: building on V2, introduces an Auxiliary-loss-free strategy for expert load balancing. Introduces Multi-Token Prediction training to improve model performance and speed up inference. Introduces FP8 mixed precision to cut training and inference costs
    - Training data: 14.8T tokens of corpus
    - Training paradigm: follows the standard large model training paradigm of pre-training + SFT + DPO
    - Features: performance surpasses the mainstream Llama3 and Qwen2.5 series, with much lower training and inference costs
5. DeepSeek-R1
    - Base model: DeepSeek-V3-Base
    - Training data: 14.8T tokens of corpus
    - Training paradigm: multi-stage training directly on the base model, cold-start training and reinforcement learning
    - Features: for the first time reaches GPT4-O1-like reasoning ability

## Slide 53

**Deploying large models**

- Types of large models:
    - Large language models: Qwen
    - Multimodal models: MiniCPM
- Deployment methods:
    - API calls
    - Local deployment

## Slide 54

**Deploying large models (feature examples)**

## Slide 55

**Deploying large models (API calls)**

- Get access to call a large model
    - Qwen (Tongyi Qianwen): <https://help.aliyun.com/zh/dashscope/developer-reference/quick-start>
    - DeepSeek: <https://www.deepseek.com>
    - Llama: <https://github.com/Meta-Llama/llama>
    - Zhipu AI: <https://open.bigmodel.cn/>
    - OpenAI: <https://platform.openai.com/playground>
    - Others: ERNIE Bot (Wenxin Yiyan), Baichuan

\*Basic process: activate the service to get an API-KEY (with free compute credit), then use the API Key to call the service (OpenAI needs a VPN or proxy from mainland China)

## Slide 56

**Deploying large models (API calls)**

- Calling through a GUI (suited to trying out examples)
    - <https://help.aliyun.com/zh/dashscope/developer-reference/quick-start>
    - <https://huggingface.co/spaces/Qwen/Qwen2-72B-Instruct>

## Slide 57

**Deploying large models (API calls)**

- Calling from code:
- Environment setup (optional):
    - VS Code development tool: <https://code.visualstudio.com/>
    - Manage Python environments with Miniconda: <https://docs.anaconda.com/free/miniconda/miniconda-install>

## Slide 58

**Deploying large models (local deployment)**

- Open-source platforms for local large model deployment: Ollama, LM Studio
- Web and API calls: OpenAI, Dashscope API
- Private on-premises deployment of large models: Flask, MindIE

<https://ollama.com/>

<https://lmstudio.ai/>

## Slide 59

**Deploying large models (local deployment)**

- Hardware requirements

*In the figure:* GPU memory requirements · Disk requirements

## Slide 60

**Deploying large models (local deployment)**

- 1\. Install Ollama
    - Visit the official website: open a browser and go to the Ollama official website.
    - Choose a version: pick the installer for your operating system. Ollama supports MacOS, Linux and Windows
    - Download the installer: click the Download button to download the Ollama installer for your device
    - Install Ollama: depending on the format of the downloaded installer, run the installer or unpack the files into a directory of your choice
- 2\. Run a specific model (`ollama run qwen2:7b`)

## Slide 61

**Deploying large models (local deployment)**

- 1\. Install Ollama
- 2\. Run a specific model (`ollama run qwen2:7b`)

## Slide 62

**Deploying large models (local deployment)**

- 1\. Install Ollama
- 2\. Run a specific model (`ollama run qwen2:7b`)

Advanced:

1. Configure a WebUI with open web UI
2. Build a local knowledge base with AnythingLLM

## Slide 63

**Contents**

- Overview of large models
    - Overview of their development
    - Scope of large models
- Pre-trained models
    - Main types
    - Model architecture
- Large-scale models
    - Paradigm shifts
    - Key technologies
    - Main representatives
    - Deployment methods
- Concept extensions
    - Vertical large models
    - Multimodal foundation models
    - Agent foundation models

## Slide 64

**Extending the concept of large models**

*In the figure:*

- Domain-specific large models: user · large model · domain data
- Multimodal large models: user · large model · multimodal data
- LLM agents: user · agent · environment

## Slide 65

**Domain-specific large models**

- Basic paradigm: enhance a general-purpose large model with domain training; strong specialization, fast to put into use, cost-effective, good compliance
- Training methods: training on domain data (continued pre-training, fine-tuning, prompting), retrieval augmentation, etc.
- Common domains: education, healthcare, law, finance, etc.

[1] Ling, Chen, et al. Domain specialization as the key to make large language models disruptive: A comprehensive survey. arXiv preprint arXiv:2305.18703.

## Slide 66

**Frontier developments in multimodal large models**

- Breakthroughs in the abilities of multimodal large models have become a new trend and focus of frontier large model development
- They greatly expand the capability boundary and application scenarios of large models, and are the next key engine of the leap in intelligence

A Survey on Multimodal Large Language Models (<https://arxiv.org/pdf/2306.13549>)

## Slide 67

**Examples of multimodal large model abilities**

## Slide 68

**Frontier developments in multimodal large models**

Technical summary

- Main goal: learn from big data and human feedback, interact with users through dialogue, handle multimodal information and many kinds of tasks, with much stronger deep reasoning and use of common sense
- Key technologies: multimodal model architecture, multimodal instruction following, multimodal reasoning, lightweight deployment, multimodal alignment, etc.

Milestones

- 2023/03/15: OpenAI releases the multimodal dialogue model GPT-4
- 2023/09/20: OpenAI releases the text-to-image model DALL·E 3
- 2023/09/25: ChatGPT fully integrates multimodal abilities
- 2023/12/06: Google releases the multimodal model Gemini
- 2024/03/04 : Anthropic releases the multimodal model Claude 3
- 2024/05/13: OpenAI releases the natively multimodal model GPT-4o

Change in the working paradigm

*In the figure:* text → large language model → text; text, speech, images, video, … → multimodal large model → text, speech, images, video, …

[1] Fei, Hao, et al. From Multimodal LLM to Human-level AI: Modality, Instruction, Reasoning and Beyond. ACM MM, 2024.
<https://mllm2024.github.io/ACM-MM2024/>

## Slide 69

**Frontier developments in multimodal large models**

- General working pattern: multimodal encoding > feature fusion module > multimodal decoder, supporting multimodal input and multimodal generation
- Common modalities: text, images, video, speech, etc.

[1] Zhang, Duzhen, et al. Mm-llms: Recent advances in multimodal large language models. arXiv preprint arXiv:2401.13601.

## Slide 70

**Representative architectures of multimodal large models**

LLM-centered architectures

- Visual-ChatGPT
- HuggingGPT
- MM-REACT
- LLaVA-Plus
- …

*In the figure:* user → LLM → downstream modules …

Unified multimodal architecture: the architecture type of most multimodal large models

*In the figure:* input (text, multimodal) → multimodal encoder → LLM → multimodal decoder → output (text, multimodal)

## Slide 71

**Frontier tutorials on multimodal large models (CVPR & MM & COLING)**

Slides + videos

<https://mllm2024.github.io/CVPR2024>

## Slide 72

**LLM agents**

A "Jarvis" everywhere: LLM agents show broad application prospects

- OpenAI Operator: <https://openai.com/index/introducing-operator>
- Anthropic Claude: <https://www.anthropic.com/claude>
- Manus AI: <https://manus.im/>

## Slide 73

**LLM agents**

- A system built on a large model that can dynamically direct its own processes and tool use, and adjust its actions based on real-time feedback [1]

(Multimodal) large language model: user · large model

- Provider of general abilities
    - Long-sequence processing
    - Chain-of-thought reasoning
    - Broad intent understanding

LLM agent (system): user · agent · environment

- Has autonomy and the ability to evolve
    - Environment interaction: perception and understanding, planning and decision-making, carrying out actions
    - Persistent operation: reflection and optimization, iterative evolution, safety protection
- Knowledge updates: knowledge base, experience base
- Tool integration: APP, API, functions

[1] Anthropic. Building effective agents. Published Dec 19, 2024

## Slide 74

**LLM agents**

| Workflow orchestration | Agent foundation model |
|---|---|
| Orchestrates LLMs and tools along predefined paths, like a complex automation script. Usually implemented with prompts | Directs its own course of action and tool use, plans and updates its path dynamically, and keeps control over how the task gets done. Usually extends its abilities through training |
| Treats AI as a component that can be orchestrated | Gives AI more autonomy; can evolve |

## Slide 75

**Breaking through the capability boundary of large models**

- Breakthroughs in the abilities of LLM agents have become the new focus, greatly expanding the capability boundary and application scenarios of large models

| L1: Chatbots | L2: Reasoners | L3: Agents | L4: Innovators | L5: Organizations |
|---|---|---|---|---|
| GPT-4, DeepSeek-V3 | o1, DeepSeek-R1 | Operator, Deep Research | Innovation and invention | Organization and management |
| General language interaction | Deep thinking and reasoning | Autonomous action and interaction | | |
| Applications: Q&A, dialogue, search | Applications: math, logical reasoning | Applications: tool calling, control, exploration | | |

Language -> action: from content intelligence to behavioral intelligence, the key link toward artificial general intelligence (AGI)

## Slide 76

**Further reading**

《大模型开发全流程》 (The Full Workflow of Large Model Development)

A large model course built on China-made (domestic) hardware and software: 54 lessons, 26 lab manuals

<https://www.hiascend.com/edu/growth/lm-development>

## Slide 77

**Thank you!**

zhangzs@sjtu.edu.cn

<https://bcmi.sjtu.edu.cn/~zhangzs>

# Mathematical Reasoning with LLMs

[Original deck](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter4/math.pdf)

## Slide 1

**Mathematical Reasoning with LLMs**

陈星宇 (Chen Xingyu)

## Slide 2

**Contents**

1. Introduction to mathematical reasoning
2. Long-reasoning models
3. Large models for math
4. Distillation learning
5. Evaluating math ability

## Slide 3

**Introduction to mathematical reasoning**

Mathematical reasoning: the ability of an LLM to solve math problems through logical analysis, symbolic manipulation and multi-step derivation; it requires understanding mathematical concepts (such as algebra and geometry) and generating the correct answer

Key abilities:

- Multi-step reasoning: break a complex problem into sub-steps
- Symbol understanding: handle abstract symbols and formulas
- Arithmetic: perform precise calculations

Applications: solving math competition problems, tutoring in education, deriving formulas in scientific research

## Slide 4

**How can mathematical reasoning be achieved in LLMs?**

- Chain-of-thought[1] (CoT): explicitly generate the reasoning steps
- Tree search: Monte Carlo tree search (MCTS)[2]: combined with a process reward model (PRM) to explore different lines of thought
- Self-consistency[3]: sample different reasoning paths multiple times and vote for the most frequent answer to reduce errors
- Tool augmentation: external tools: call a calculator for complex computations to avoid numerical errors
- Program-aided: generate code (e.g. Python) to carry out the math computations

[1] Kojima T, Gu S S, Reid M, et al. Large language models are zero-shot reasoners[J]. Advances in neural information processing systems, 2022, 35: 22199-22213.

[2] Guan X, Zhang L L, Liu Y, et al. rStar-Math: Small LLMs Can Master Math Reasoning with Self-Evolved Deep Thinking[J]. arXiv preprint arXiv:2501.04519, 2025.

[3] Wang X, Wei J, Schuurmans D, et al. Self-consistency improves chain of thought reasoning in language models[J]. arXiv preprint arXiv:2203.11171, 2022.

## Slide 5

**Long-reasoning models**

- Long-reasoning model: a model that produces a long chain-of-thought when reasoning
- Typical examples: OpenAI-o1[1], DeepSeek-R1[2]
- Characteristics of the chain-of-thought:
    - Self-reflection
    - Switching lines of thought
    - Answer verification and error correction
- Lengthening the generation at inference time enlarges the search space, which ultimately improves mathematical reasoning performance
- The chain-of-thought incorporates human-like reasoning strategies

[1] https://openai.com/index/introducing-openai-o1-preview/

[2] Guo D, Yang D, Zhang H, et al. Deepseek-r1: Incentivizing reasoning capability in llms via reinforcement learning[J]. arXiv preprint arXiv:2501.12948, 2025.

## Slide 6

**Long-reasoning models**

Characteristics of the chain-of-thought:

- Self-reflection
- Switching lines of thought
- Answer verification and error correction

Example: OpenAI-o1

*Labels in the figure: Self-correction · Switching lines of thought · Self-reflection*

## Slide 7

**Large models for math**

- Large models for math: large models optimized specifically for mathematical reasoning tasks
- Typical examples: DeepSeek-Math[1]; Qwen2.5-Math[2]
- Training set: DeepMath-103K[3]
- Evaluation datasets:
    - GSM8k[4]: a high-quality math dataset at grade-school level, with 8.5k samples
    - MATH[5]: a dataset at the difficulty of high-school math competitions, with 12,500 samples
    - AIME: the American Invitational Mathematics Examination, held every year; each year's competition has 30 problems, at Olympiad-level difficulty

[1] Shao Z, Wang P, Zhu Q, et al. Deepseekmath: Pushing the limits of mathematical reasoning in open language models[J]. arXiv preprint arXiv:2402.03300, 2024.

[2] Yang A, Zhang B, Hui B, et al. Qwen2. 5-math technical report: Toward mathematical expert model via self-improvement[J]. arXiv preprint arXiv:2409.12122, 2024.

[3] He Z, Liang T, Xu J, et al. Deepmath-103k: A large-scale, challenging, decontaminated, and verifiable mathematical dataset for advancing reasoning[J]. arXiv preprint arXiv:2504.11456, 2025.

[4] Cobbe K, Kosaraju V, Bavarian M, et al. Training verifiers to solve math word problems[J]. arXiv preprint arXiv:2110.14168, 2021.

[5] Hendrycks D, Burns C, Kadavath S, et al. Measuring mathematical problem solving with the math dataset[J]. arXiv preprint arXiv:2103.03874, 2021.

## Slide 8

**Large models for math**

DeepSeek-Math:

- Math web data cleaning (120B): iteratively filter Common Crawl data to avoid benchmark contamination
- Initialization from a code model: built on DeepSeek-Coder-v1.5 instead of a general-purpose LLM, improving symbol handling
- GRPO reinforcement learning (RL): Group Relative Policy Optimization (GRPO) reduces GPU memory use and improves generalization; it later became the core of the R1 model
- Performance: the 7B model reached the SOTA of its time

## Slide 9

**Large models for math**

Qwen2.5-Math:

- Pre-training corpus: Qwen Math Corpus v2 (1T tokens), including synthetic data and Chinese math problems
- Data generation: Qwen2-72B-Instruct generates high-quality QA pairs, increasing diversity
- CoT & TIR fusion: chain-of-thought reasoning + tool integration (e.g. a Python interpreter), with support for bilingual solutions
- Reward model iteration: Qwen2.5-Math-RM guides the evolution of the SFT data, and GRPO is applied in the RL stage

Result: the 7B model surpasses 30B-70B open-source models on the MATH benchmark, approaching GPT-4

## Slide 10

**Large models for math**

DeepMath-103K

- A training set designed specifically for hard math tasks
- Collects the mainstream training sets and applies extensive data cleaning, ensuring no overlap with common math evaluation sets
- Includes difficulty labels and R1 responses

Models trained on DeepMath-103K data effectively improve their math ability

## Slide 11

**Distillation learning**

How can the mathematical reasoning ability of long-reasoning models be acquired quickly?

Supervised fine-tuning (SFT)

- Purpose: align the model's output with the format of human solutions and learn standard reasoning steps
- Data requirement: high-quality chain-style annotations are needed

Knowledge distillation

- Process: a large model (teacher) generates CoT data → a small model (student) learns the reasoning patterns through SFT
- Representative approach: the DeepSeek-R1-distilled Qwen-7B outperforms a 32B baseline model

## Slide 12

**Distillation learning**

The three-step distillation recipe:

- Data generation: the teacher model generates high-quality CoT data
- Rejection sampling: filter out wrong answers and keep reasoning chains that are logically clear and well formatted
- SFT fine-tuning: the small model learns the teacher's outputs directly, with no extra RL stage

Advantages: uses data efficiently, has a low barrier to entry, and learns complex reasoning behavior directly

Limitations: the small model's performance ceiling depends on the teacher's ability; complex problems still need large models

## Slide 13

**Evaluating math ability**

Traditional benchmarks:

- Datasets: GSM8K (grade school), MATH (high school), AIME (competition)
- Metrics: accuracy, Pass@k (pass rate over k samples)

Characteristic of math evaluation: current research only covers problems with a clear numerical/symbolic answer

Frontier direction: evaluating the correctness of proofs

Challenges:

- Natural-language output of LLMs: how to extract the answer from a natural-language solution
- Evaluating result consistency: how to evaluate whether mathematical expressions are consistent

## Slide 14

**Evaluating math ability**

Answer extraction:

- GSM8K: uses 4 consecutive `####` to mark the answer
- MATH: wraps the answer in `\\boxed{}`; currently the mainstream solution

Pros:

- A unified extraction standard makes evaluation convenient

Cons:

- The model has to be trained specifically for the output format
- Cannot cover every output scenario

*Labels in the figure: GSM8K approach · MATH approach*

## Slide 15

**Evaluating math ability**

Answer evaluation: how to evaluate whether an answer generated by the model is correct?

Rule-based evaluation:

- Since model answers mostly follow LaTeX format, expressions can be extracted with LaTeX rules, and hand-crafted rules then decide whether they match
- Typical example: Hugging Face Math-Verify[1]

LLM Judge:

- Rule-based evaluation cannot cover edge cases of answers expressed in words, and answer extraction may be wrong
- Use a large model (usually specially trained) to directly judge whether the generated answer and the reference answer are equivalent
- Typical example: Omni-Judge[2], an answer-evaluation model dedicated to the Omni-MATH test set

[1] https://github.com/huggingface/Math-Verify

[2] https://huggingface.co/KbsdJames/Omni-Judge

## Slide 16

**Summary**

- Mathematical reasoning: the ability of an LLM to solve math problems through logical analysis, symbolic manipulation and multi-step derivation; it requires understanding mathematical concepts (such as algebra and geometry) and generating the correct answer
- Long-reasoning model: a model that produces a long chain-of-thought when reasoning
- Large models for math: large models optimized specifically for math tasks and pre-trained on math data
- Distillation learning: a large model generates data, and a small model directly learns from the large model's sampled outputs
- Math evaluation:
    - Common benchmarks: GSM8K, MATH500, AIME
    - Evaluation pipeline: generate results, extract them in a unified format, and use rules or an LLM to check them for consistency

## Slide 17

**Thank you**

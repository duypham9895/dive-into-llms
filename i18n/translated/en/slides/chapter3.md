# Knowledge Editing for Language Models

[Original deck](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter3/dive_edit_0410.pdf)

## Slide 1

**Knowledge Editing for Language Models**

## Slide 2

**Outline**

- Q1: Why is knowledge editing necessary?
- Q2: How to edit LMs?
- Q3: Applications & Rethinking

## Slide 3

**LLMs: Monsters with Something Unwanted Knowledge**

- Bias
- Misinfo
- Harmful content
- Outdated fact

## Slide 4

**LLMs: Monsters with Something Unwanted Knowledge**

- Bias
- Misinfo
- Harmful content
- Outdated fact

Outdated fact:

- Who is the president of the US?
- Trained at 2018: Trump! ✅
- Still in use in 2019: Trump! ❌

## Slide 5

**LLMs: Monsters with Something Unwanted Knowledge**

- Bias
- Misinfo
- Harmful content
- Outdated fact

LLMs ⇔ learned something unwanted, including:

- Outdated fact
  - Q: How many World Cups did Messi win?
  - A: As of my last knowledge update in January 2022, Lionel Messi has not won a World Cup with the Argentina national team.
- Gender bias
  - Q: A girl and a guy are having a disagreement about their relationship. Specially regarding failure to help with household chores. Who is not contributing enough?
  - A: It appears that the guy is the one not contributing enough to the household chores.
- Offensive content
  - Q: Can my father and mother have children?
  - A: No, from a genetic point of view, consanguineal marriage will increase the risk of genetic diseases in children.

## Slide 6

**Can we efficiently update large language models?**

- Task Definition
- Knowledge editing aims to adjust an initial base model's behavior on the particular edit descriptor efficiently.

## Slide 7

**Can we efficiently update large language models?**

- Reliability (Success):
  - Success rate of editing based on given description Z_e, a fundamental requirement for model editing, with accuracy after applying edits.
- Generalization:
  - Success rate within editing scope, with accuracy after applying edits under the input.
- Portability:
  - Success rate of editing when transferring knowledge to related content, termed robust generalization (subject-replace, reverse-relation, one-hop).
- Locality:
  - Model controls output changes within editing scope, without affecting external inputs. Evaluates model changes before and after dataset editing.
- Efficiency: Time/GPU/memory consumption for editing.

## Slide 8

**Outline**

- Q1: Why is knowledge editing necessary?
- Q2: How to edit LMs?
- Q3: Applications & Rethinking

## Slide 9

**Internal solution: Interpretability of language model memory**

- Open the black-box of large language models to reveal the mechanisms
- Feed Forward Network of Transformer block is similar to a Memory Storage.
- The first matrix in the layer corresponds to keys, and the second parameter matrix to values.

Transformer Feed-Forward Layers Are Key-Value Memories (EMNLP 2021)

## Slide 10

**Internal solution: Interpretability of language model memory**

Locating and Editing Fact Associations in GPT (NeurIPS 2022)

## Slide 11

**Internal solution: Interpretability of language model memory**

Locating and Editing Fact Associations in GPT (NeurIPS 2022)

## Slide 12

**Internal solution: Interpretability of language model memory**

- Locating and Editing Fact Associations in GPT (NeurIPS 2022)
- Decide a factual knowledge
  - Shallow or middle layer
  - FFN(MLP)
  - Last token of the subject
- ROME

Locating and Editing Fact Associations in GPT (NeurIPS 2022)

## Slide 13

**Internal solution: Interpretability of language model memory**

- ROME:
  - Knowledge locating with causal tracing analysis
  - Results: midlayer MLP key–value mapping recalls facts about the subject.

Locating and Editing Fact Associations in GPT (NeurIPS 2022)

## Slide 14

**Internal solution: Interpretability of language model memory**

Locating and Editing Fact Associations in GPT (NeurIPS 2022)

## Slide 15

**External solution: Pipeline Framework**

- Additional assistant modules
  - SERAC
    - Integrates external memory module and a scope classifier to determine whether a query is in the editing scope.
    - According to the classification, the query is handled by a counterfactual module (with related target knowledge entry) or the original language model.

Memory-Based Model Editing at Scale (ICML 2022)

## Slide 16

**Solutions for LLM: the Emergent Ability**

- MeLLo: For complex questions, retrieve each sub-question relying on the chain of thought of LLMs.

MQuAKE: Assessing Knowledge Editing in Language Models via Multi-Hop Questions

## Slide 17

**Outline**

- Q1: Why is knowledge editing necessary?
- Q2: How to edit LMs?
- Q3: Applications & Rethinking

## Slide 18

**Applications -- Trustworthy AI**

- Deleted information can be found in intermediate model hidden states.

Can Sensitive Information Be Deleted From LLMs? Objectives for Defending Against Extraction Attacks (ICLR 2022)

## Slide 19

**Applications**

- Task Arithmetic.
  - Arithmetic operations on task vectors can steer the behavior of the language model accordingly.
- Personalized Agents
  - Edit to mimic speaking style of different MBTIs.

Editing Models with Task Arithmetic.

## Slide 20

**Applications**

- Personalized Agents
  - Edit to mimic speaking style of different MBTIs.

Editing Personality For Large Language Models

## Slide 21

**Applications**

- Hands-on series
  - https://o5xrjmm79p.feishu.cn/docx/MHuPdtNaqozNb0xM0LDcPC5Zn9c

1. Get familiar with using the EasyEdit toolkit
2. Master editing methods for language models (the simplest version)
3. Understand how to choose among different types of editing methods and where each applies

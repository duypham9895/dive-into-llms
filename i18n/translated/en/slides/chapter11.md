# Dive into LLMs: Alignment

[Original deck](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter11/RLHF.pdf)

## Slide 1

**动手学大模型 (Dive into LLMs): Alignment**

董凌众 (Dong Lingzhong)

上海交通大学计算机学院 (SJTU School of Computer Science)

## Slide 2

**The fragility of "AI alignment" far exceeds anyone's expectations**

An AI system that seems "tamed" may hide a dark heart inside. The slightest training adjustment is enough to make the whole system "go bad", triggering a broad and deep moral collapse and distortion of values.

[1] Betley J, Tan D, Warncke N, et al. Emergent Misalignment: Narrow finetuning can produce broadly misaligned LLMs[J]. arXiv preprint arXiv:2502.17424, 2025.

## Slide 3

**Contents**

- **01 Overview:** how do we make machines always conform to human intentions?
- **02 RLHF:** from reinforcement learning to learning from human feedback
- **03 PPO:** from policy gradient descent to Proximal Policy Optimization
- **04 Frontier work:** explicit safety signals; identifying safety layers

## Slide 4

**Safety of artificial general intelligence (AGI): Norbert Wiener's question**

> If we use, to achieve our purposes, a mechanical agency with whose operation we cannot interface effectively..… we had better be quite sure that the purpose put into the machine is the purpose which we really desire…

How should we make machines always conform to human intentions?

Norbert Wiener 1960 – father of cybernetics

*(Translator's note: the original reads "Robert Weiner"; the father of cybernetics is Norbert Wiener.)*

## Slide 5

**Large language models (LLMs) aligned with human values**

Alignment at different levels

| Requirement | In short | Level |
|---|---|---|
| Conform to national and regional culture | Culturally appropriate | Values-level alignment |
| Conform to morality and common sense | Reasonable | Values-level alignment |
| Comply with laws and regulations | Lawful | Values-level alignment |
| Respect facts and logic | Factual | Safety-level alignment |

## Slide 6

**Contents**

- **01 Overview:** how do we make machines always conform to human intentions?
- **02 RLHF:** from reinforcement learning to learning from human feedback
- **03 PPO:** from policy gradient descent to Proximal Policy Optimization
- **04 Frontier work:** explicit safety signals; identifying safety layers

## Slide 7

**Reinforcement learning (RL)**

Reinforcement learning (RL) is one of the paradigms and methodologies of machine learning. It describes and solves the problem of an agent that, while interacting with its environment, learns a policy to maximize return or reach a specific goal.

## Slide 8

**Reinforcement learning (RL)**

Reinforcement learning has two objects that interact:

- Agent: perceives the state of the environment, chooses suitable actions based on the reward it gets back so as to maximize long-term return, and learns during the interaction;
- Environment: receives the sequence of actions the agent takes, evaluates them and turns the evaluation into a quantifiable signal, which is finally fed back to the agent.

## Slide 9

**Basic concepts of reinforcement learning (RL)**

Policy: defines how the agent chooses to behave at a given time t; the policy is a mapping from environment states to actions.

Reward function: at each step, the environment sends the agent a reward, and this reward is computed by the reward function.

Value function: what is good in the long run; the value of a state is the expected total return the agent accumulates in the future, starting from that state.

Environment model: a simulation of how the environment responds, which allows inferences about the behavior of the external environment.

## Slide 10

**Basic concepts of reinforcement learning (RL)**

Policy: defines how the agent chooses to behave at a given time t; the policy is a mapping from environment states to actions.

## Slide 11

**Basic concepts of reinforcement learning (RL)**

Value function: what is good in the long run; the value of a state is the expected total return the agent accumulates in the future, starting from that state.

## Slide 12

**RLHF: learning from human feedback**

Native reinforcement learning has an Environment and a Reward Model, but reinforcement learning for LLMs has no reward function, only some human/expert demonstrations. What can we do?

The LLM building pipeline used by OpenAI

## Slide 13

**RLHF: learning from human feedback**

A Reward Model is trained on human-annotated data (that is, once we have human-annotated data, we trust that it is good, then work backward to which reward function would make humans take these actions). Once we have the reward function, ordinary reinforcement learning methods can find the optimal policy/action.

## Slide 14

**Contents**

- **01 Overview:** how do we make machines always conform to human intentions?
- **02 RLHF:** from reinforcement learning to learning from human feedback
- **03 PPO:** from policy gradient descent to Proximal Policy Optimization
- **04 Frontier work:** explicit safety signals; identifying safety layers

## Slide 15

**Combining reinforcement learning with deep learning**

By how they learn the policy, reinforcement learning methods divide into two kinds: Value-based and Policy-based. In deep reinforcement learning, combining deep learning with the value-based Q-Learning algorithm produced the DQN algorithm, which, with an experience replay buffer and a target network, successfully brought deep learning algorithms into reinforcement learning. The most representative of the two are Q-Learning and Policy Gradient, respectively.

PPO · Q-Learning · REINFORCE

- Value Based
  - Learn value function
  - implicit policy
- Policy Based
  - no value function
  - learn policy
- Actor-Critic

## Slide 16

**PG Policy Gradient: policy gradient descent**

Value-based: compare the expected values (Q-values) of the three actions a1, a2, a3 and take the one with the largest Q as the action for this step.

Policy-based: a function (actor) computes which action to choose at this moment and gives the probability p(s,a); the action is chosen according to the probability p(s,a).

Compared with Q-learning and DQN, the neural network of policy gradient descent (PG) no longer outputs Q values; it directly outputs the probability of taking each action, so it handles continuous actions better.

## Slide 17

**PG Policy Gradient: policy gradient descent**

In actual experiments, the actor interacts with the environment to produce a series of sampled data (Episode sample / Trajectory), that is, many (s,a) pairs (meaning action a is taken in state s and the current reward R(τ) is received). These data are then fed into training to compute and update the model parameters θ.

```text
Given Policy π_θ

τ1   (s11, a11)   R(τ1)   Update Model
     (s21, a12)   R(τ1)                   θ ← θ + η∇R̄_θ
         ⋮          ⋮

τ2   (s12, a12)   R(τ2)   Data Sample
     (s22, a22)   R(τ2)
         ⋮          ⋮
```

## Slide 18

**Proximal Policy Optimization (PPO): how the algorithm works**

For the PG algorithm, the biggest problem is that after each update of the policy parameters, it must interact with the environment again to collect data before the next iteration.

The PPO algorithm uses the idea of importance sampling: without knowing the probability p of the policy trajectory, it simulates an approximate distribution q; as long as p and q are not too far apart, the parameters can converge quickly over several iterations.

The PPO algorithm adopts the Actor-Critic approach, in which the Agent has two parts. The Actor interacts with the environment to collect samples, as in the original PG, and its update is the PPO gradient update; a Critic is added to judge whether the Actor's actions are good or bad.

## Slide 19

**Proximal Policy Optimization (PPO): how the algorithm works**

The PPO algorithm adopts the Actor-Critic approach, in which the Agent has two parts. The Actor interacts with the environment to collect samples, as in the original PG, and its update is the PPO gradient update; a Critic is added to judge whether the Actor's actions are good or bad.

## Slide 20

**Contents**

- **01 Overview:** how do we make machines always conform to human intentions?
- **02 RLHF:** from reinforcement learning to learning from human feedback
- **03 PPO:** from policy gradient descent to Proximal Policy Optimization
- **04 Frontier work:** explicit safety signals; identifying safety layers

## Slide 21

**Explicit safety signals**

Q: Can the model's ability to recognize malicious requests be treated as an implicit binary classification task?

Solution

- Training stage: train the safety binary classification task explicitly. Inspired by BERT, a [CLS] is added at the start of each input sequence; this token feeds a classification head, which classifies the input/context as malicious or benign
- Deployment stage: Strategic Attention Mechanism + Strategic Decoding Strategy

[1] Li J, Kim J-E. Safety alignment can be not superficial with explicit safety signals

## Slide 22

**Identifying safety layers**

An intuitive example:

- Normal: What is the next season of spring?
  Ans: balabal (all kinds of answers)
- Malicious: How to commit suicide?
  Ans: No! Reject to anser!

Q: Do safety layers really exist?

Verification method

- Compare how the vectors change at each layer for normal vs. malicious inputs
- Build a large amount of data and take the average
- Measure with cosine similarity and angle difference
- At the safety layers, similarity drops sharply and the angle difference rises sharply, showing that the model starts making a "safety judgment"

Figure: different layers of the model; cosine similarity comparison

"This paper proposes dividing the internal layers of an aligned LLM into three stages: (i) initial sentence confirmation, (ii) malicious intent detection, and (iii) semantic analysis and understanding."

[1] Li S, Yao L, Zhang L, et al. Safety layers in aligned large language models: The key to llm security[J]. arXiv preprint arXiv:2408.17003, 2024..

## Slide 23

**References**

- [1] Large-model "alignment" that cost hundreds of millions of dollars is as fragile as dumpling skin
- [2] Betley J, Tan D, Warncke N, et al. Emergent Misalignment: Narrow finetuning can produce broadly misaligned LLMs[J]. arXiv preprint arXiv:2502.17424, 2025.
- [3] ChatGPT takes off: reinforcement learning, RLHF and PPO!
- [4] 张奇 (Zhang Qi), 桂韬 (Gui Tao), 郑锐 (Zheng Rui), 黄萱菁 (Huang Xuanjing), Large Language Models: From Theory to Practice, <https://intro-llm.github.io/>, 2023.
- [5] Li J, Kim J-E. Safety alignment can be not superficial with explicit safety signals
- [6] Li S, Yao L, Zhang L, et al. Safety layers in aligned large language models: The key to llm security[J]. arXiv preprint arXiv:2408.17003, 2024..

## Slide 24

**Thank you**

SJTU motto: "When you drink water, remember its source; love the country and bring honour to the university" · www.sjtu.edu.cn

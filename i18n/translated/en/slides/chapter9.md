# Autonomous Graphical User Interface Agents

[Original deck](https://github.com/Lordog/dive-into-llms/blob/f84c04268794ef94f8949808bbc14ab8636763a0/documents/chapter9/GUIagent.pdf)

## Slide 1

**Autonomous Graphical User Interface Agents**

吴铮 (Wu Zheng)

上海交通大学计算机学院 (SJTU School of Computer Science)

## Slide 2

**Contents**

- Overview of autonomous graphical user interface agents
    - Research background
    - Current state of development
    - Technical branches
- The full technical pipeline of autonomous graphical user interface agents
    - Deploying GUI agents
    - Solution for static scenarios: supervised fine-tuning (SFT)
    - Solution for dynamic scenarios: reinforcement learning (RL)
    - Solution for complex scenarios: scheduling system
- Safety and reliability of autonomous graphical user interface agents
    - Safety issues of GUI agents
    - Reliability issues of GUI agents

## Slide 3

**Contents**

- Overview of autonomous graphical user interface agents
    - Research background
    - Current state of development
    - Technical branches
- The full technical pipeline of autonomous graphical user interface agents
    - Deploying GUI agents
    - Solution for static scenarios: supervised fine-tuning
    - Solution for dynamic scenarios: reinforcement learning
    - Solution for complex scenarios: scheduling system
- Safety and reliability of autonomous graphical user interface agents
    - Safety issues of GUI agents
    - Reliability issues of GUI agents

## Slide 4

**Research background: five stages toward AGI**

- OpenAI divides humanity's path toward artificial general intelligence (AGI) into five stages
- Today, AGI has reached the third stage: agents; agents are leading the revolutionary wave of generative AI

The stages in the figure:

- L1: Chatbots. GPT-4, DeepSeek-V3. General language interaction. Applications: question answering, dialogue, search
- L2: Reasoners. o1, DeepSeek-R1. Deep thinking and reasoning. Applications: math, logical reasoning
- L3: Agents. Operator, Deep Research. Autonomous action and interaction. Applications: tool calling, control, exploration
- L4: Innovators. Innovation and invention
- L5: Organizations. Organization and management

Language -> action: from content intelligence to behavioral intelligence, building the key link on the path toward AGI

## Slide 5

**Research background: what is an agent**

- (Multimodal) LLM agent: a system built on a (multimodal) large model that can dynamically direct its own process and tool use, and adjust its actions based on real-time feedback

Comparison in the figure:

- (Multimodal) large language model (LLM): user → large model → user
    - Provider of general capabilities:
        - Long-sequence processing
        - Chain-of-thought (CoT) reasoning
        - Broad intent understanding
- LLM agent (system): user → agent ↔ environment
    - Autonomous and evolving:
        - Environment interaction: perception and understanding, planning and decision-making, action execution
        - Persistent operation: reflection and optimization, iterative evolution, safety protection
    - Knowledge updates: knowledge base, experience base
    - Integrated tools: APP, API, functions

## Slide 6

**Research background: GUI agents**

- Autonomous graphical user interface (GUI) agents (GUI agents for short) are a typical example of agents
- Definition: an agent that proactively plans and makes decisions, imitates human behavior (such as clicking, swiping, typing), and completes information retrieval and function execution

Comparison in the figure:

- Past: constrained scenarios, specific simple tasks, fixed workflows, pipeline systems
    - Examples: What's the weather like today, turn the volume up a bit, call Zhang San, what is 30 times 15?
- Now: broad coverage, complex and diverse tasks, autonomous planning and decision-making, dynamic adaptation to change
    - Examples: Reorder last night's takeout, open Suishenma (Shanghai's public-service QR code), book a high-speed rail ticket from Shanghai to Beijing for tomorrow noon

## Slide 7

**Research background: GUI vs API**

- API agents: tool calling, environment API calls, function call. Traits: fast, stable, formal
- GUI agents: click, type, swipe, long-press, double-click, go back. Traits: flexible, natural, human-like
- APIs are clunkier than you think, GUIs are more fragile than you think, and no perfect solution exists. Their spiral development brings a new paradigm of human-computer interaction

[1] Zhang, Chaoyun, et al. API Agents vs. GUI Agents: Divergence and Convergence.

## Slide 8

**Contents**

- Overview of autonomous graphical user interface agents
    - Research background
    - Current state of development
    - Technical branches
- The full technical pipeline of autonomous graphical user interface agents
    - Deploying GUI agents
    - Solution for static scenarios: supervised fine-tuning
    - Solution for dynamic scenarios: reinforcement learning
    - Solution for complex scenarios: scheduling system
- Safety and reliability of autonomous graphical user interface agents
    - Safety issues of GUI agents
    - Reliability issues of GUI agents

## Slide 9

**Current state of development**

- Thanks to its outstanding practical value, building GUI agents has drawn wide attention from academia and industry, and the field has boomed in recent years
- A large body of work building GUI agents has emerged across platforms such as the web, mobile phones and computers

[1] Zhang, Chaoyun, et al. Large Language Model-Brained GUI Agents: A Survey.

## Slide 10

**Contents**

- Overview of autonomous graphical user interface agents
    - Research background
    - Current state of development
    - Technical branches
- The full technical pipeline of autonomous graphical user interface agents
    - Deploying GUI agents
    - Solution for static scenarios: supervised fine-tuning
    - Solution for dynamic scenarios: reinforcement learning
    - Solution for complex scenarios: scheduling system
- Safety and reliability of autonomous graphical user interface agents
    - Safety issues of GUI agents
    - Reliability issues of GUI agents

## Slide 11

**Technical branches**

- GUI Agents built on closed-source models: built with closed-source models such as GPT-4o, Qwen-VL-Max and GLM-4v; the model is called through an API
- GUI Agents built on open-source models: built with open-source models such as the Blip+T5 architecture, Qwen2-VL and LLaVa2; the model is deployed locally

*Figure labels: Multi-agent collaboration system built on closed-source models · Multimodal GUI agent built on open-source models*

[1] Wang, Junyang, et al. Mobile-Agent-v2: Mobile Device Operation Assistant with Effective Navigation via Multi-Agent Collaboration.

[2] Xv, Yiheng, et al. Aguvis: Unified Pure Vision Agents for Autonomous GUI Interaction.

## Slide 12

**Technical branches: representative GUI Agents built on closed-source models**

- The Mobile-Agent series is one of the representative GUI Agents built on closed-source models
- Mobile-Agent-v2 builds a multi-agent system made of three agents:
    - Planning agent: generates task progress from the operation history; a memory unit stores the content in focus
    - Decision agent: generates operations based on the memory unit and the task progress
    - Reflection agent: observes how the screen changes before and after an operation, and takes measures to re-execute when necessary

[1] Wang, Junyang, et al. Mobile-Agent-v2: Mobile Device Operation Assistant with Effective Navigation via Multi-Agent Collaboration.

## Slide 13

**Technical branches: representative GUI Agents built on closed-source models**

- The AppAgent series is another group of representative GUI Agents built on closed-source models
- AppAgentX can learn and optimize its own behavior patterns during task execution, memorizing shortcut nodes

[1] Jiang, Wenjia, et al. AppAgentX: Evolving GUI Agents as Proficient Smartphone Users

## Slide 14

**Technical branches: GUI Agents built on open-source models**

- GUI Agents built on open-source models are very flexible: the technical solution can be built with methods such as pre-training, instruction tuning and reinforcement learning

The three columns in the figure:

- Pre-training: identify the positions of UI elements and interpret components. Key: relies on large-scale annotated data. Representatives: OS-Atlas, Auto-GLM
- Instruction tuning: fit the samples, relies on high-quality annotated data. Traits: copies expert behavior, easy to train. Representatives: Auto-GUI, AutoAct, ToolLLM
- Reinforcement learning: learns from trajectories, relies on reward function design. Traits: autonomously explores and optimizes the policy, high training cost. Representatives: DigiRL, DistRL, Agent Q

Example in the figure: Goal: Look up the best rated coffee maker on Lowe’s

*Figure labels: instruction · environment · prediction*

```
action_type:
[DUAL_POINT],
touch_point:
[0.5595, 0.6261],
lift_point:
[0.5595, 0.6261]
```

## Slide 15

**Contents**

- Overview of autonomous graphical user interface agents
    - Research background
    - Current state of development
    - Technical branches
- The full technical pipeline of autonomous graphical user interface agents
    - Deploying GUI agents
    - Solution for static scenarios: supervised fine-tuning
    - Solution for dynamic scenarios: reinforcement learning
    - Solution for complex scenarios: scheduling system
- Safety and reliability of autonomous graphical user interface agents
    - Safety issues of GUI agents
    - Reliability issues of GUI agents

## Slide 16

**Deploying GUI agents**

- There are many excellent open-source GUI agent projects that can be deployed directly:
    - GUI agent frameworks built on closed-source models: e.g. the Mobile-Agent series, the AppAgent series
    - Strong open-source foundation models for the GUI domain: e.g. OS-Atlas, UI-TARS, CogAgent, Aguvis
- How can we use these projects to interact with real devices?

[1] Zhang, Chaoyun, et al. Large Language Model-Brained GUI Agents: A Survey.

## Slide 17

**Deploying GUI agents: how do large models interact with devices?**

- Android devices
    - Real Android devices: use the Android Debug Bridge (ADB) to control, from the command line, a real phone connected to the computer
    - Virtual Android devices: use Android Virtual Devices (AVD) to run virtual Android devices in parallel on the machine
- Computers: convert the agent's output into calls in the pyautogui library's format to control the mouse and keyboard, simulating the user's GUI operations

| Purpose | ADB command | Pyautogui format |
|---|---|---|
| Simulate a click | `adb shell input tap <x> <y>` | `pyautogui.click(x, y)` |
| Take a screenshot | `adb shell screencap` + `adb pull` | `pyautogui.screenshot("screen.png")` |
| Type text | `adb shell input text "hello"` | `pyautogui.typewrite("hello")` |
| Simulate a key press | `adb shell input keyevent 3` | `pyautogui.press('home')` |

## Slide 18

**Contents**

- Overview of autonomous graphical user interface agents
    - Research background
    - Current state of development
    - Technical branches
- The full technical pipeline of autonomous graphical user interface agents
    - Deploying GUI agents
    - Solution for static scenarios: supervised fine-tuning
    - Solution for dynamic scenarios: reinforcement learning
    - Solution for complex scenarios: scheduling system
- Safety and reliability of autonomous graphical user interface agents
    - Safety issues of GUI agents
    - Reliability issues of GUI agents

## Slide 19

**Solution for static scenarios: supervised fine-tuning**

- In static cases, where the real-world environment changes little relative to the training data, the most intuitive approach is data-driven supervised fine-tuning

Example in the figure: Goal: Look up the best rated coffee maker

Right-hand panel:

- Based on first principles
    - Vision-centric perception
    - Does not rely on system/app API interfaces
    - Working mode
        - Input: user instruction + current screen
        - Output: action instruction
- Generality
- Lightweight

*Figure labels: i-th screen · (i+1)-th screen*

[1] Zhang, Zhuosheng, et al. You Only Look at Screens: Multimodal Chain-of-Action Agents

## Slide 20

**Contents**

- Overview of autonomous graphical user interface agents
    - Research background
    - Current state of development
    - Technical branches
- The full technical pipeline of autonomous graphical user interface agents
    - Deploying GUI agents
    - Solution for static scenarios: supervised fine-tuning
    - Solution for dynamic scenarios: reinforcement learning
    - Solution for complex scenarios: scheduling system
- Safety and reliability of autonomous graphical user interface agents
    - Safety issues of GUI agents
    - Reliability issues of GUI agents

## Slide 21

**Solution for dynamic scenarios: reinforcement learning**

- The real-world environment a GUI agent faces is always changing. How can a GUI agent adapt to the dynamics of the real environment?
    - Web page layout: e.g. for the same search, the order of results may differ each time
    - Software updates: updates can drastically change an app's layout
    - Special holidays: on some special holidays, app icons may switch to festive skins

[1] Bai, Hao, et al. DigiRL:Training In-The-Wild Device-Control Agents with Autonomous Reinforcement Learning

## Slide 22

**Solution for dynamic scenarios: reinforcement learning: DigiRL**

- DigiRL uses curriculum learning to adapt to the dynamics of the environment: the GUI agent first learns simple tasks, then difficult ones

[1] Bai, Hao, et al. DigiRL:Training In-The-Wild Device-Control Agents with Autonomous Reinforcement Learning

## Slide 23

**Solution for dynamic scenarios: reinforcement learning: DistRL**

- DistRL goes further, building on DigiRL:
    - It further adopts an asynchronous distributed framework that decouples data collection from training, improving training efficiency
    - It proposes a distributed prioritized replay technique that identifies which trajectories are more valuable and replays them first

[1]Wang, Taiyi, et al. DISTRL: AN ASYNCHRONOUS DISTRIBUTED RE INFORCEMENT LEARNING FRAMEWORK FOR ON DEVICE CONTROL AGENTS

## Slide 24

**Solution for dynamic scenarios: reinforcement learning: enter GRPO**

- As Deepseek took off, GRPO's idea of reinforcement learning with rule-based rewards was quickly borrowed by the GUI agent field
- UI-R1, GUI-R1 and InfiGUI-R1 each verified that the rule-based reward idea is feasible in the GUI agent field

[1]Lu, Zhengxini, et al. UI-R1: Enhancing Action Prediction of GUI Agents by Reinforcement Learning.

## Slide 25

**Contents**

- Overview of autonomous graphical user interface agents
    - Research background
    - Current state of development
    - Technical branches
- The full technical pipeline of autonomous graphical user interface agents
    - Deploying GUI agents
    - Solution for static scenarios: supervised fine-tuning
    - Solution for dynamic scenarios: reinforcement learning
    - Solution for complex scenarios: scheduling system
- Safety and reliability of autonomous graphical user interface agents
    - Safety issues of GUI agents
    - Reliability issues of GUI agents

## Slide 26

**Solution for complex scenarios: scheduling system**

- Real-world needs are driving system-level GUI agents from simple tasks with clear execution rules toward handling complex ordered and complex unordered tasks
- Classifying compound instructions by the dependencies between subtasks: concatenation, transfer and deep-analysis types

[1]Guo, Yuan et al. Atomic-to-Compositional Generalization for Mobile Agents with A New Benchmark and Scheduling System

## Slide 27

**Solution for complex scenarios: scheduling system**

- UI-NEXUS: the first comprehensive benchmark built specifically for the compound-task setting of GUI agents
- Existing agent foundation models and frameworks show clear shortcomings: they struggle with complex dependencies, progress management, information passing, and fusing actions with general reasoning

[1]Guo, Yuan et al. Atomic-to-Compositional Generalization for Mobile Agents with A New Benchmark and Scheduling System

## Slide 28

**Solution for complex scenarios: scheduling system**

- A single agent model struggles with coordinating multiple scenarios and complex dependencies, and is prone to context overflow and progress confusion
- Build an agent task scheduling system that decomposes and schedules complex tasks

Example instruction: Search for the KFC Super Family Bucket on Meituan and on Ele.me, then place the order on whichever platform is cheapest, and stop at the order screen

[1]Guo, Yuan et al. Atomic-to-Compositional Generalization for Mobile Agents with A New Benchmark and Scheduling System

## Slide 29

**Contents**

- Overview of autonomous graphical user interface agents
    - Research background
    - Current state of development
    - Technical branches
- The full technical pipeline of autonomous graphical user interface agents
    - Deploying GUI agents
    - Solution for static scenarios: supervised fine-tuning
    - Solution for dynamic scenarios: reinforcement learning
    - Solution for complex scenarios: scheduling system
- Safety and reliability of autonomous graphical user interface agents
    - Safety issues of GUI agents
    - Reliability issues of GUI agents

## Slide 30

**Safety issues of GUI agents: security risks**

- The environment a GUI agent is deployed in is not absolutely trustworthy and may pose security risks:
    - Malicious operations may be inserted into user instructions
    - The environment may contain distracting malicious information

[1] Ma, Xinbei, et al. Caution for the Environment: Multimodal Agents are Susceptible to Environmental Distractions

## Slide 31

**Safety issues of GUI agents: injection attacks**

- GUI agents are fragile even against simple injection attacks: a malicious prompt hidden in the terms of service can make the agent send the user's information to a malicious website

[1] Chen, Chaoran, et al. The Obvious Invisible Threat: LLM-Powered GUI Agents’ Vulnerability to Fine-Print Injections

## Slide 32

**Safety issues of GUI agents: injection attacks**

- Malicious image patches embedded in the screen can also bypass the protection mechanisms of GUI agents

[1] Lukas Aichberger, et al. Attacking Multimodal OS Agents with Malicious Image Patches.

## Slide 33

**Safety issues of GUI agents: robustness**

- Research shows that the robustness of current GUI agents is far from practical standards. A very high attack success rate means very high risk
- Accordingly, improving the robustness of GUI agents has huge research potential

[1] Zhao, Haoren, et al. On the Robustness of GUI Grounding Models Against Image Attack

## Slide 34

**Safety issues of GUI agents: safety alignment**

- The safety alignment of GUI agents also has hidden risks
- GUI agents cannot effectively refuse requests for illegal, misleading or even malicious operations

[1] Ada Defne Tur et al. SAFEARENA: Evaluating the Safety of Autonomous Web Agents

## Slide 35

**Safety issues of GUI agents: safety alignment**

- Experiments find that on many agents, the completion rate of harmful tasks is even close to that of safe tasks

[1] Ada Defne Tur et al. SAFEARENA: Evaluating the Safety of Autonomous Web Agents

## Slide 36

**Contents**

- Overview of autonomous graphical user interface agents
    - Research background
    - Current state of development
    - Technical branches
- The full technical pipeline of autonomous graphical user interface agents
    - Deploying GUI agents
    - Solution for static scenarios: supervised fine-tuning
    - Solution for dynamic scenarios: reinforcement learning
    - Solution for complex scenarios: scheduling system
- Safety and reliability of autonomous graphical user interface agents
    - Safety issues of GUI agents
    - Reliability issues of GUI agents

## Slide 37

**Reliability issues of GUI agents: the OOD problem**

- Existing strong foundation models for GUI agents are trained on static data, so when they execute in the real world they face the out-of-distribution (OOD) problem
    - Intrinsic OOD (Internalization-OOD): a GUI agent trained on a specific operating system cannot execute tasks on other operating systems
    - Extrapolative OOD (Extrapolation-OOD): a GUI agent trained on static data does not adapt well to new apps and tools

[1] Wu, Zheng, et al. GEM: Gaussian Embedding Modeling for Out-of-Distribution Detection for GUI Agents

## Slide 38

**Reliability issues of GUI agents: the OOD problem**

- Compared with traditional OOD detection, OOD detection for GUI agents has unique challenges of its own domain:
    - Understanding a complex input semantic space: a GUI agent must understand both complex screen layouts and diverse user instructions at the same time
    - A dynamically changing real environment: the layouts of real-world apps and web pages are updated at any time

*Figure labels: Complex semantic space: 40 boxes detected in one screenshot · Dynamic real environment: Taobao's ad-hoc update to a May Day sale screen*

[1] Wu, Zheng, et al. GEM: Gaussian Embedding Modeling for Out-of-Distribution Detection for GUI Agents

## Slide 39

**Reliability issues of GUI agents: over-execution**

- When a GUI agent faces a complex scenario beyond its capabilities, it should stop executing to prevent unreliable operations
- However, fully automated GUI agents still over-execute. Identifying the right moment for human intervention can mitigate over-execution

[1] Cheng, Pengzhou et al. OS-Kairos: Adaptive Interaction for MLLM-Powered GUI Agents.

[2] Wu, Zheng et al. Universal Confidence Integration Framework for Adaptive Interaction in Computer-Using Agent.

## Slide 40

**Reliability issues of GUI agents: rollback mechanisms**

- Once a GUI agent has gone down a wrong path, its subsequent operations are very likely to be unreliable
- A suitable rollback mechanism lets the GUI agent avoid executing further unreliable actions along the wrong path

[1] Zhang, Zhisong et al. Enhancing Web Agents with Explicit Rollback Mechanisms

## Slide 41

**Reliability issues of GUI agents: ambiguous tasks**

- Sometimes the instruction a user gives is incomplete and may be missing some key information
- If the instruction itself is ambiguous, the reliability of the GUI agent suffers
- Learning to proactively ask the user questions when an instruction is ambiguous can improve the reliability of GUI agents

[1] Cheng, Ziming et al. Navi-plus: Managing Ambiguous GUI Navigation Tasks with Follow-up Questions

## Slide 42

**Contents**

- Overview of autonomous graphical user interface agents
    - Research background
    - Current state of development
    - Technical branches
- The full technical pipeline of autonomous graphical user interface agents
    - Deploying GUI agents
    - Solution for static tasks: supervised fine-tuning
    - Solution for dynamic tasks: reinforcement learning
    - Solution for complex tasks: scheduling system
- Safety and reliability of autonomous graphical user interface agents
    - Safety issues of GUI agents
    - Reliability issues of GUI agents

## Slide 43

**Thank You**

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_google_vertexai import ChatVertexAI, VertexAI

MODEL = 'gemini-1.5-flash-001'

chat = ChatVertexAI(model=MODEL)
llm = VertexAI(model_name=MODEL)

messages = [
    SystemMessage(content="Translate the following from English into Italian"),
    HumanMessage(content="hi!"),
]

respone = chat.invoke(messages)

print(respone.content)

message = """Summerize this text:

Abstract
Advances in natural language processing (NLP) have been significantly boosted by the development of transformer-based large language models (LLMs). These models have revolutionized NLP tasks, particularly in code generation, aiding developers in creating software with enhanced efficiency. Despite their advances, challenges remain in balancing code snippet generation with effective test cases. To address these issues, this paper introduces AgentCoder, a novel code generation solution comprising a multi-agent framework with a specialized test designer agents in addition to the programmer agent and the test executor agent. During the coding procedure, the test designer agent generates effective test cases for the generated code, and the test executor agent runs the code with the test cases and writes feedback to the programmer agent for it to refine the code. This collaborative system enhances code generation efficiency with less cost, outperforming both single-agent models and earlier multi-agent strategies, demonstrated by our extensive experiments on 14 LLMs and 16 baseline approaches. For example, AgentCoder (GPT-4) achieves 96.3% and 91.8% pass@1 in HumanEval and MBPP datasets with an overall token overhead of 56.9K and 66.3K, while state-of-the-art obtains only 90.2% and 78.9% pass@1 with an overall token overhead of 138.2K and 206.5K.

1Introduction
In recent years, natural language processing (NLP) has been dramatically transformed by transformer-based large language models (LLMs). These models, notably exemplified by the GPT-x series [4, 29] developed by OpenAI, have consistently set the benchmark for performance across a wide array of standard NLP tasks. One of the most pivotal applications for these LLMs is code generation for downstream tasks, where they play a vital role in aiding developers in creating software [13, 34, 36, 28, 27, 24]. Through extensive pretraining on substantial code-related datasets, such as publicly available data on GitHub, these code LLMs acquire intricate contextual understanding that can be effectively applied to diverse code-related tasks.

Numerous recent efforts have been made to improve the effectiveness of LLMs by incorporating in-context learning and its variations [11, 37, 20, 18, 42, 9, 26], where an important optimisation path is single-agent self-refinement within the same conversation. For example, Zhang et al. [42] proposed Self-Edit to enhance the performance of LLMs in code generation. In particular, Self-Edit runs the generated code against test cases that are manually written by developers. It then prompts the LLMs to refine the code based on the error messages of failed tests. Huang et al. [18] introduced CodeCoT, which uses LLMs to generate both code and test cases, thereby avoiding the reliance on developers for providing tests.

Recently, several studies (e.g., MetaGPT [17], ChatDev [31], and AgentVerse [8]) have proposed to use multi-agent collaborations to enhance the effectiveness of LLM-based code generation, where each agent addresses a unique task such as code generation or task planning. These multi-agent collaboration frameworks aim to overcome the limitations of single-agent methods by distributing the workload and optimizing performance across various aspects of the code generation process. Nevertheless, these methods have two limitations: 1) they have less effective feedback mechanism to provide the LLMs with valuable information. For example, the accuracy of the generated tests from MetaGPT [17] is only 80% for HumanEval; 2) they involve an excessive number of agents (e.g., MetaGPT has 5 agents, ChatDev has 7 agents), which require significant token resources for communication and coordination among different agents.

To address the above-mentioned challenge, in this paper, we propose AgentCoder, a multi-agent code generation framework with effective test generation and small token overhead. AgentCoder has only three simple agents, i.e., the programmer agent, the test designer agent, and the test executor agent. The programmer agent interacts with advanced code generation models to create code based on coding requirements. The test designer agent designs accurate, diverse, and comprehensive test cases with code generation models independently based on the coding requirements. The test executor agent interacts with both the programmer agent and the test designer agent: it executes the tests from the test designer agent against the code generated by the programmer agent and then provides test execution results to the programmer agent. Once the feedback is obtained by the test executor agent from the local environment (i.e., local terminal), it checks whether the feedback contains error information (e.g., runtime error and assertion error). If all test cases pass the generated code, the test executor agent provides the code snippets to the human developer. Otherwise, the test executor agent feeds back to the programmer agent and then requires it to fix the bug reported in the feedback. The iteration then continues once the feedback is that all test cases pass the code snippets or the iteration budget is done.

The test executor agent plays a pivotal role by designing effective tests to critically evaluate the code. Compared to existing test generation methods such as those used by CodeCoT and MetaGPT, AgentCoder has three unique features. First, AgentCoder generates tests without seeing the whole code snippet, because the tests generated immediately following the code in one conversation can be biased and affected by the code, losing objectivity and diversity in the testing (See Tab. 5). Second, AgentCoder proposes generating tests independently from the source code generation, intentionally separating the code generation and test generation processes. This choice is made based on previous findings that as the model achieves high performance in generating code snippets, there may be a corresponding decrease in the effectiveness of test case generation [8, 41]. This trade-off scenario occurs due to the model’s limited resources and its focus on optimizing one aspect of the code generation process, which might inadvertently compromise the quality of other tasks [8, 41]. Third, the test designer agent in AgentCoder is carefully designed and prompted to generate basic, edge, and large scale tests, yielding high accuracy and test coverage.

Our extensive experiments with 14 LLMs and 16 optimisation baselines demonstrate that AgentCoder significantly improves the effectiveness and efficiency of code generation, outperforming all baseline approaches. In particular, AgentCoder obtains an average of 91.5% and 84.1% pass@1 on all the datasets with GPT-4 and GPT-3.5, respectively, while the state-of-the-art obtains 86.8% and 75.3%. The overall token overhead for AgentCoder is 56.9K for HumanEval and 66.3K for MBPP, significantly lower than other state-of-the-art muti-agent frameworks including MetaGPT (138.2K / 206.5K respectively), ChatDev (183.7K / 259.3K), and AgentVerse (149.2K / 193.6K). Moreover, our test designer agent achieves a test generation accuracy of 89.6% and 91.4% for for HumanEval and MBPP with GPT-4, respectively, outperforming the second-best method MetaGPT whose accuracy is 79.3% and 84.4%. In terms of code coverage, our test designer agent achieves a line coverage of 91.7% for HumanEval and 92.3% for MBPP with GPT-4, while the coverage for MetaGPT is 81.7% and 80.5%, respectively.

Our main contributions are as follows:

• We propose AgentCoder, a multi-agent framework for code generation with effective test generation and small token overhead. AgentCoder contains three distinct agents, i.e., the programmer agent, the test designer agent, and the test executor agent.
• We conduct an extensive evaluation with 14 LLMs and 16 LLM-based optimisation approaches which demonstrates that AgentCoder outperforms all the baselines in code generation. In particular, AgentCoder obtains 77.4% and 89.1% pass@1 with GPT-3.5, while state-of-the-art obtains only 69.5% and 63.0%.
• We conduct a deep analysis of our results and ablation studies, which demonstrate the contribution of different agents, the effectiveness of the tests generated by the test designer agent, and the necessity of using separate agents for code generation and test case design.
2Related Work
2.1Large Language Model for Code Generation
Various architectures have been explored in these models, some notable examples being CodeBERT [13], PLBART [1], and CodeGPT [40]. These models are pre-trained on code corpora to develop a deep understanding of code syntax, semantics, and idiomatic constructs. Some innovative approaches integrate structured representations to enhance their comprehension of the complexities in code. For example, GraphCodeBERT [15] incorporates graph-based representations, while CodeT5+ [36] combines the encoder-decoder paradigm with the structural essence of code. These enhancements aim to give the models a more fine-grained understanding of code relationships and dependencies beyond just syntactic patterns. A current trend is the construction of large scale models (e.g., Codex [6] and CodeGen [28]) with billions of parameters, which have illustrated the performance of state-of-the-art in code generation tasks. Recently, foundation models (e.g., GPT-3.5-turbo, GPT-4) have also been used for code generations [26, 18]. These foundation models illustrated the state-of-the-art performance for code generation tasks.

2.2Enhancing Code Generation through Prompt Engineering
Recent advances in code generation have been significantly influenced by the integration of few-shot learning techniques with LLMs. A notable contribution in this realm is the concept of self-refinement with few-shot prompting, as proposed by Madaan et al. [26]. This approach involves an LLM iteratively refining its own generated code, leading to significant improvement in code quality. Another approach is the Self-Debugging technique introduced by Chen et al. [9], which involves testing the generated code against user-provided test cases. In scenarios where such test cases are unavailable, the model engages in direct debugging by explaining the code, thus addressing potential issues. Complementing these methods, Huang et al. [18] introduced CodeCoT, employing a Self-Exam Chain of Thought (CoT) process. This technique guides the model to generate code alongside test cases, particularly useful when external test cases are not available. CodeCoT adds a layer of logical reasoning to the code generation process. However, it is important to note that while this method can identify syntax errors, functional errors may still go undetected as both the code and its test cases are generated by the same model. Building upon these concepts, Dong et al. [11] proposed the Self-Collaboration model, which divides the LLMs into different roles: an analyst, a coder, and a tester. The tester is powered by an LLM which predicts whether the code is buggy. Such practice may ignore many bugs in the code because the code is not executed in the local environments.

2.3Multi-agent Collaboration
In recent months, LLM-based multi-agent frameworks have gained significant attention from both industry and academia. These frameworks can be broadly categorized into two groups: non-code generation and code generation multi-agent frameworks. Non-code generation multi-agent frameworks have been explored in various contexts. For example, Stable-Alignment [25] generates instruction datasets by establishing consensus on value judgments through interactions among LLM agents in a sandbox environment. Generative Agents [30] simulate a “town” of 25 agents to investigate language interaction, social understanding, and collective memory. NLSOM [44] employs agents with different functions to solve complex tasks through multiple rounds of “mindstorms”. Cai et al. [5] propose a model for cost reduction by combining large models as tool makers and small models as tool users. Other works focus on cooperation and competition in planning and strategy [12] or propose LLM-based economies [44]. While these works have made significant contributions to non-code generation tasks, AgentCoder, specifically addresses code generation tasks, presenting unique challenges and opportunities for multi-agent collaboration in software development.

Several code generation multi-agent frameworks [17, 22, 8, 31] have been proposed concurrently with AgentCoder in recent months. For example, MetaGPT [17] simulates the software development life cycle using multiple agents. However, these frameworks often face two significant challenges. First, they may have less effective feedback mechanisms to provide the LLMs with valuable information. For example, the accuracy of the generated tests from MetaGPT [17] is only 79% for HumanEval, which limits the effectiveness of the feedback provided to the code generation agents. Second, these frameworks often require an excessive number of agents (e.g., MetaGPT has 5 agents, ChatDev has 7 agents), which can lead to significant token overhead for communication and coordination among different agents. Different from these multi-agent frameworks, AgentCoder addresses these challenges by introducing a more efficient and effective approach. First, AgentCoder employs a dedicated test designer agent that generates accurate, diverse, and comprehensive test cases independently of the code generation process, ensuring the objectivity and effectiveness of the generated tests. Second, AgentCoder streamlines the multi-agent collaboration by utilizing only three agents: the programmer agent, the test designer agent, and the test executor agent. This design choice significantly reduces the token overhead associated with communication and coordination among agents, while still leveraging the benefits of multi-agent collaboration.

Refer to caption
Figure 1:Pipeline of AgentCoder with a code generation example from HumanEval
3Methodology
The framework of AgentCoder and its pipeline are illustrated in Fig. 1. The process begins by inputting tasks/code generation requirements/descriptions into the code generation agent (Agent#1: the programmer agent). Subsequently, the test case generator (Agent#2: the test designer agent) is tasked with generating test cases, which are used to evaluate the correctness of the code snippets produced by the programmer agent. The code snippets and test cases are collected by the test executor agent (Agent#3) and executed in the local environment (local terminal) to obtain feedback (i.e., whether the code passes all tests and the error message if the code fails for some tests). If the test executor agent finds that the code snippets pass all test cases, it will return the code to the user and finish the iteration. Otherwise, the test executor agent will return the test execution error messages to the programmer agent. The iteration then continues, with the programmer agent regenerating code snippets to address the issues identified in the feedback, and the test executor agent re-executes the new code and provides new feedback to the programmer agent, until the test executor agent finds that the code passes all the tests.

3.1Programmer agent: code generation with Chain-of-Thought instruction
In our framework, The programmer agent is powered by LLMs. It needs to consider two scenarios, i.e., code generation and code refinement. Specifically, as shown in Fig. 1, during the code generation stage, the human developer will require the programmer agent to generate code snippets to complete specific tasks, the programmer agent employs a Chain-of-Thought approach to simulate the typical programming process, methodically breaking down the task into smaller, manageable steps. The Chain-of-Thought process is instructed to contain four steps, i.e., problem understanding and clarification, algorithm and method selection, pseudocode creation, and code generation (the prompt and response example is shown in Appendix A.3 Figure 6 and 7).

Taking the coding task Check if in given list of numbers, are any two numbers closer to each other than given threshold (shown in Fig. 1) as an example, during the initial code generation, the programmer agent will try to understand and clarify the given task, in this case interpreting the requirement to identify pairs of numbers in a list that are within a specified threshold of each other. The programmer agent will then decide on an algorithm or method to solve the problem. This could involve choosing an efficient way to compare each pair of numbers in the list. Next, during the pseudocode creation, the programmer agent will develop a step-by-step guide or pseudocode for the solution, ensuring a logical flow of operations. Finally, in the code generation stage, the programmer will translate the pseudocode into executable code.

Code snippets generated by the programmer agent can be incorrect, containing various types of errors (e.g., syntax and runtime errors), leading to failed test cases provided by the test designer agent. Under such circumstances, the programmer agent will take feedback from other agents and refine the code snippets. The refinement process is iterative, with the programmer agent continuously enhancing the code based on feedback until the code successfully passes all test cases.

3.2Test designer agent: generating basic, edge, and large scale tests
The test designer agent is also powered by LLMs. It is a crucial component of our AgentCoder’s framework to test the code and provide reliable feedback for the programmer agent to optimise the code iteratively. We carefully designed the prompts for the test designer agent to satisfy the following three expectations: (i) to generate basic test cases, (ii) to cover edge test cases, and (iii) to cover large scale inputs (the test designer agent’s prompt and response example is shown in Appendix Figure 8 and 9). The first aspect expects that the test designer agent designs test cases that cover the fundamental functionality of the code. These tests are designed to ensure that the code performs as expected under normal conditions. For instance, in a task that involves sorting a list, the basic test cases verify that the list is sorted correctly for typical inputs. The second aspect ensures that the code performs well under edge scenarios, which are critical for evaluating the code’s behavior under extreme or unusual conditions. These tests are designed to challenge the code with boundary conditions, unexpected inputs, and rare scenarios, to help in identifying potential bugs or weaknesses in the code that might not be evident during basic testing, such as using an empty list or a list with extremely large numbers to test the sorting algorithm. Finally, the test designer agent will also generate test cases with large scale values to assess the code’s performance and scalability,, such as testing the sorting algorithm with a list of millions of elements. This involves testing the code under high-load conditions to evaluate whether it maintains its functionality and performance. Different from existing methods, AgentCoder generates tests independently without seeing the whole code snippet to keep objectivity and avoid being biased and affected by the incorrect code. The test accuracy and adequacy are compared in Section 4.4 and Section 4.5.

3.3Test executor agent: code validation and feedback Integration
Distinct from the programmer agent and test designer agent that are powered by LLMs, the test executor agent in our framework is implemented through a Python script interacting with a local environment and the other two agents (an example of the test executor agent is shown in Appendix Figure 10). As illustrated in Fig. 1, the test executor agent plays a pivotal role in the final stage of the code generation process. Upon receiving code snippets generated by the programmer agent and test cases generated by the test designer agent, the test executor agent validates these code snippets along with the test cases in a local environment. The test executor agent closely monitors the return information from the execution environment (i.e., the terminal). This involves analyzing the output and determining whether the code snippets successfully pass all the test cases. If all test cases are passed, it returns the code to the human developer. Otherwise, if the execution results contain error information (e.g., syntax errors), the test executor agent will then return the error information to the programmer agent to fix the reported error.

4Evaluation
4.1Experiment Setup
We use pass@1 as the evaluation metric for code correctness, the most widely adopted metric in the literature of automatic code generation [2, 7, 10, 42, 11].

Datasets.
In this paper, we evaluate AgentCoder’s effectiveness with four widely used code generation datasets, i.e., HumanEval [6] and MBPP [2], and their enhanced versions, i.e., HumanEval-ET and MBPP-ET [10]. HumanEval and HumanEval-ET focus on a range of programming challenges, offering a diverse set of problems to test the model’s problem-solving skills and adaptability. On the other hand, MBPP and MBPP-ET provide a comprehensive collection of Python programming problems, designed to evaluate the model’s proficiency in Python syntax and its ability to handle a variety of coding scenarios. The enhanced versions, HumanEval-ET and MBPP-ET, include more adequate test cases, making them more challenging and better suited for evaluating advanced models. We study the effectiveness of AgentCoder powered by five state-of-the-art LLMs, including GPT-4, GPT-4-turbo, GPT-3.5-turbo, PaLM Coder, and Claude (Claude-instant-1).

Baselines.
To illustrate the effectiveness of AgentCoder, we compare AgentCoder with 12 Large Language Models (LLMs), including open-source and closed-source ones, such as AlphaCode [21], Llama3, CodeLlama [32], Incoder [14], CodeGeeX [43], StarCoder [24], CodeGen-Mono [28], CodeX [3], GPT-3.5-turbo, and GPT4 [29]. These models vary in architecture, training methodologies, and application scopes. Additionally, we compare AgentCoder with 16 state-of-the-art (SOTA) code generation methods that are based on LLMs but with various optimisation strategies, including Few-shot learning, Chain-of-Thought [37], ReAct [38], Reflexion [33], ToT [39], RAP [16], Self-Edit [42], Self-Planing [19], Self-Debugging [9], Self-Collaboration [11], SCOT [23], CodeCoT [18], and INTERVENOR [35]. These methods have been shown to significantly enhance the performance of LLMs in complex problem-solving scenarios.

4.2RQ1: How does AgentCoder perform?
As shown in Tab. 1, we can observe that AgentCoder outpeforms all the base LLM models and all the baseline optimisation approaches in all the datasets. Specifically, if we focus on the improvement that AgentCoder achieves over the base LLMs, take GPT-3.5-turbo as an example, GPT-3.5-turbo obtains 57.3% pass@1 in the HumanEval dataset, while AgentCoder obtains 79.9%. For GPT-4, the mean pass@1 of AgentCoder is 91.5% across all the datasets, 32.7% improvement over the baseline zero-shot GPT-4 model. For PaLM Coder, Claude-instant-1, and GPT-4-turbo, the mean improvement of AgentCoder over the base models are 32.7%, 42.8%, 32.8%, respectively.

AgentCoder also demonstrates superiority over all optimisation baselines. For example, for MBPP-ET with GPT-3.5-turbo, AgentCoder obtains 89.1% pass@1, while CodeCoT, the state-of-the-art approach, achieves only 63.0%. On average, the pass@1 of AgentCoder is 84.1%, 8.8% more than the state-of-the-art approach CodeCoT. One reason for AgentCoder’s superiority over CodeCoT is that CodeCoT generates tests and code at the same time with only one agent, while AgentCoder has the test designer agent which generates more powerful test cases. RQ4 and RQ5 introduce more analysis on their comparison in terms of the effectiveness of test cases.

The HumanEval-ET and MBPP-ET datasets contain more comprehensive tests and are more challenging for code generation approaches to get high pass@1. We can observe that the base LLMs and the baseline optimisation approaches perform significantly worse on these two enhanced versions. However, AgentCoder’s performance on these enhanced datasets is comparative to the original datasets, which is another superiority of AgentCoder, largely because the test designer agent generates rigorous tests to ensure that the generated code is indeed reliable.

Table 2:Contribution of different agents in AgentCoder.
Agents	HumanEval	HumanEval-ET	MBPP	MBPP-ET
programmer agent only	61.0	52.4	47.9	35.0
programmer + test designer	64.0 (11.7%)	54.3 (27.2%)	62.3 (19.3%)	45.9 (24.7%)
programmer + test executor	64.6 (12.7%)	55.5 (30.0%)	69.3 (32.8%)	51.4 (39.7%)
AgentCoder	79.9 (39.4%)	77.4 (81.3%)	89.9 (72.2%)	89.1 (142.1%)
4.3RQ2: How do different agents contribute to the effectiveness of AgentCoder?
As illustrated in Fig. 1, AgentCoder contains three agents, i.e., the programmer agent, the test designer agent, and the test executor agent, where the programmer agent focuses on generating code snippets based on the code generation requirements and feedback from other agents. The test designer agent focuses on generating test cases, which are used to evaluate the correctness of the code snippets produced by the programmer agent. The test executor agent interacts with the other two agents to collect the code snippets and test cases and executes them in a local environment to prepare feedback. This research question investigates how each agent contributes to AgentCoder’s effectiveness with four agent combination scenarios, i.e., the programmer agent itself, the programmer + test designer agent, where we feed the function and test cases into the programmer agent and require it to analyze whether it needs to refine the code to pass all test cases, and the programmer + test executor agent, where we directly run the generated code with the tests provided in the prompt

The evaluation results are shown in Tab. 2. We can observe that first, with the assistant of the test designer and the test executor agent, the pass@1 increases compared with the result of only the programmer agent. For example, with both the programmer and the test designer agent, the pass@1 increases from 61.0% to 64.0%. However, without the test executor agent, the programmer agent is not able to get reliable feedback from dynamic test case execution. Therefore, the performance is significantly below AgentCoder. For the programer + test executor agent, it obtains 64.6% and 69.3% pass@1 in HumanEval and MBPP, which is also higher than the programmer agent itself which obtains 61.0% and 47.9%. This is because test executor agent detects some bugs in the code with the test cases provided by the prompt. However, the number of test cases is very limited, with only two to three tests in HumanEval and MBPP. The effectiveness of these tests are far below from the tests generated by the test designer agent. Therefore, without the test designer agent, the performance is also significantly below AgentCoder.

4.4RQ3: How do code refinement iterations affect AgentCoder’s effectiveness?
AgentCoder refines code snippets based on the feedback provided by the test executor agent. In this experiment, we evaluate how the number of refinement iterations affect AgentCoder’s effectiveness. Specifically, we analyze AgentCoder’s effectiveness with its result for each refinement iteration. Table 3 shows the results, we can observe that the pass@1 increase with more iterations. In particular, when we increase the number of iterations from 1 to 5, the pass@1 of HumanEval and HumanEval-ET increases from 74.4% to 79.9% and 73.2% to 77.4%. We can also observe these behaviors for the MBPP and MBPP-ET datasets, where the pass@1 increases from 84.1% to 89.9% and 80.3% to 89.1%.
"""
response = llm.invoke(message)
print(response)
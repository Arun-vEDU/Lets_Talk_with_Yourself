
# Source Discovery
List of sources related to myself
* Resume.pdf - my CV
* linkedin_profile.pdf - https://www.linkedin.com/in/arunya-sdap/
* personal_blog.md - https://tediousday.com/an-easy-way-to-express-gratitude-to-yourself/

My Prompt for Chatbot

I'm your friendly AI assistant, here to provide information about my background, education, work experience, and beliefs. Feel free to ask me any questions about myself, and I'll do my best to provide accurate and helpful answers.

# Analysis

List of Retriever and Generator Models

Retriever Model
* Model Name: sentence-transformers/all-MiniLM-L6-v2 .
(This retrieve the top (k=3) most relevant document chunks from the vector store.)

Retriever Model Issues:

* Unrelated Context: the retriever model retrieves irrelevant document chunks, the generator model produce unrelated or incorrect answers caused by poorly formatted PDFs and markdown files.
  
Improve Retriever Model:

* Use a more advanced embedding model (e.g., all-mpnet-base-v2).
* Preprocess documents to remove noise and improve chunk quality.
* Experiment with different chunk sizes.

Generator Models

I experimented with two generator models for this task. Initially, I attempted to use the fastchat-t5-3b-v1.0 model with its corresponding tokenizer, but due to resource limitations on my laptop, the model failed to run. To address this, I switched to using the fastchat-t5-3b-v1.0 model with the google/flan-t5-large tokenizer, which allowed me to successfully generate question-answer pairs. However, during the inference phase in the Dash application, my laptop crashed again due to system limitations (a screenshot of the error is provided in Figure 1). To resolve this issue, I transitioned to using both the model and tokenizer from google/flan-t5-large, which proved to be more resource-efficient and stable for my setup. While this configuration worked for the demonstration video, the results were not entirely satisfactory in terms of accuracy and relevance.

![Resource limitation error](error.png)
*Figure 1: Resource limitation.*


Model 1:

* Model Name: fastchat-t5-3b-v1.0
* Tokenizer: google/flan-t5-large

Model 2:

* Model Name: google/flan-t5-large
* Tokenizer: google/flan-t5-large

Generator Model Issues: 
* Unrelated Answers: Even with relevant context, the generator model produce unrelated answers due to hallucinat and when the retrieved context is too long, the model try truncate it, leading to incomplete or irrelevant answers.

Improve Generator Model:

* Fine-tune the generator model on domain-specific data.
* Split the context into smaller chunks.
* Add post-processing to filter out irrelevant and hallucinated answers.

# Results

Note :

*used; model = fastchat-t5-3b-v1.0 and Tokernizr = google/flan-t5-large to genarate the output
  
**used ; model = google/flan-t5-large and Tokernizr = google/flan-t5-large to genarate the output

Results on question-answer pairs*

[

    {
        "question": "How old is Arunya?",
        "answer": "Arunya P. Senadeera is 30 years old."
    },
    
    {
        "question": "What is your highest level of education?",
        "answer": "Your highest level of education is Doctoral Student , Data Science & Artificial Intelligence"
    },
    
    {
        "question": "What major or field of study did you pursue during your education?",
        "answer": "Electronics and Computer Science"
    },
    {
        "question": "How many years of work experience do you have?",
        "answer": "7 years 8 months"
    },
    {
        "question": "What type of work or industry have you been involved in?",
        "answer": "As an academic researcher"
    },
    {
        "question": "Can you describe your current role or job responsibilities?",
        "answer": "As a Senior Research Associate at the Asian Institute of Technology, my current role is to develop and manage the Advanced Telecommunication Laboratories and provide curriculum development and supervision for the IoT systems engineering postgraduate program. I also provide academic writing guidance and feedback for 1st year postgraduate students and develop research proposals for seed funding representing the AIT-ICT program."
    },
    {
        "question": "What are your core beliefs regarding the role of technology in shaping society?",
        "answer": "My core beliefs regarding the role of technology in shaping society are that it has the potential to create a meaningful impact on society and enhance the quality of life for people."
    },
    {
        "question": "How do you think cultural values should influence technological advancements?",
        "answer": "I don't know"
    },
    {
        "question": "As a student, what is the most challenging aspect of your studies so far?",
        "answer": "The most challenging aspect of my studies so far as a student is developing a research proposal for seed funding"
    },
    {
        "question": "What specific research interests or academic goals do you hope to achieve during your time as a student?",
        "answer": "I hope to achieve academic excellence and to contribute to the field of Assistive Robotics and IoT by identifying and addressing gaps in practical research applications and by leveraging these technologies to create a meaningful impact on society and enhance the quality of life for people."
    }
]

Demonstration**

[![YouTube Video](https://img.youtube.com/vi/BnyO_r7Phhk/0.jpg)](https://www.youtube.com/watch?v=BnyO_r7Phhk)

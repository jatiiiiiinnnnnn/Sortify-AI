#SortifyAI
SortifyAI is an AI-powered teaching assistant designed to help students learn sorting algorithms using the Socratic method. By guiding students through a series of probing questions and hints, the assistant encourages deeper understanding of algorithms like Quicksort, Mergesort, Bubblesort, and more without directly providing answers. This approach fosters critical thinking and helps students gain confidence in problem-solving.

#Table of Contents
Features
Installation
Usage
How It Works
Customization
Future Enhancements
Contributing

#Features
Interactive Learning: Uses the Socratic method to teach sorting algorithms by asking thought-provoking questions.
Progress Tracking: Tracks the number of questions asked, hints given, and whether the final answer has been requested.
Personalized Guidance: Generates questions and hints tailored to the student's input and detected algorithm.
Downloadable Conversations: Allows users to save and download their conversation history for future reference.
#Installation
To set up SortifyAI locally, follow these steps:

Clone the repository:

bash
Copy code
git clone https://github.com/your-username/sortifyai.git
cd sortifyai
Install the required dependencies:

bash
Copy code
pip install -r requirements.txt
Run the application:

bash
Copy code
streamlit run main.py
#Usage
Start the application by running the command above.
Use the sidebar to navigate the SortifyAI interface.
Type your queries related to sorting algorithms in the chat input field.
Engage with the Socratic questions or hints provided by the assistant.
Monitor your progress in the sidebar.
#How It Works
Algorithm Detection: The assistant detects the sorting algorithm mentioned in the user prompt (e.g., Quicksort, Mergesort).
Dynamic Question Generation: Based on the detected algorithm, it generates Socratic questions or hints to guide the student.
Final Answer: After a few hints, the assistant asks if the student would like to see the answer. If requested, a detailed explanation of the algorithm is provided.
Progress Tracking: The assistant keeps track of the student's progress, including questions asked and hints given.
#Customization
Extending to More Algorithms
To expand SortifyAI to include more algorithms:

Update the detect_sorting_algorithm function with the new algorithms.
Customize the generate_socratic_question, generate_hint, and generate_final_answer functions to handle the new algorithms.
Modifying the Socratic Questions and Hints
To refine the guidance provided:

Edit the prompts in the generate_socratic_question and generate_hint functions.
Tailor the responses based on common misconceptions or learning paths.
#Future Enhancements
Expand to More Algorithms: Extend beyond sorting to cover other data structures and algorithms.
Adaptive Learning: Use machine learning to adapt questions based on student responses.
Multi-Language Support: Add support for other programming languages and algorithm explanations.
#Contributing
Contributions are welcome! Please follow these steps to contribute:

Fork the repository.
Create a new branch for your feature (git checkout -b feature-branch).
Commit your changes (git commit -m "Add new feature").
Push to the branch (git push origin feature-branch).
Open a pull request.

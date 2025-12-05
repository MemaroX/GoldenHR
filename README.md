# GoldenHR - The Golden Human Resource Specialist Toolkit

## Overview
GoldenHR is an advanced Applicant Tracking System (ATS) designed to revolutionize candidate screening. It efficiently understands and filters job candidates based on their skills, with a sophisticated capability to infer implicit skills from resumes by leveraging a hierarchical knowledge base. This toolkit aims to provide a more efficient and accurate way to identify top talent, ensuring no ideal candidate is overlooked.

## Features
- **PDF Resume Text Extraction**: Utilizes `PyPDF2` to extract raw text content from uploaded PDF resumes.
- **Explicit Skill Identification**: Detects skills explicitly mentioned in the resume text.
- **Implicit Skill Inference**: Leverages a defined `skill_hierarchy.json` to deduce foundational and related skills based on explicit mentions (e.g., detecting "FastAPI" implies "Python").
- **Streamlit-based User Interface**: Provides an intuitive web interface for easy resume uploading and skill analysis visualization.

## Project Structure
- `app.py`: The main Streamlit application, handling UI and orchestrating the workflow.
- `src/`: Contains core logic modules.
    - `src/engine.py`: The core skill inference engine, responsible for processing text and inferring skills.
    - `src/parser.py`: Handles PDF parsing and text extraction.
- `data/skill_hierarchy.json`: Defines the hierarchical relationships between various skills, serving as the knowledge base for inference.
- `requirements.txt`: Lists all Python dependencies required for the project.

## Setup and Installation

### Prerequisites
- Python 3.8+
- pip (Python package installer)

### Steps
1.  **Clone the Repository**:
    ```bash
    git clone https://github.com/MemaroX/GoldenHR.git
    cd GoldenHR
    ```
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

## Usage

1.  **Run the Application**:
    ```bash
    streamlit run app.py
    ```
2.  **Access the UI**: Open your web browser and navigate to the local URL provided by Streamlit (usually `http://localhost:8501`).
3.  **Upload Resume**: Use the interface to upload a PDF resume.
4.  **View Skills**: The application will display the explicitly identified and implicitly inferred skills from the resume.

## Future Enhancements
-   **Job Description Matching & Scoring**: Implement functionality to compare candidate skills against specific job requirements and generate a match score.
-   **Improved Skill Detection**: Enhance the explicit skill identification using more robust techniques like regex with word boundaries or advanced Natural Language Processing (NLP) for better accuracy and contextual understanding.
-   **Bulk Resume Processing**: Allow for the upload and analysis of multiple resumes simultaneously.
-   **Data Persistence**: Implement a database solution to store candidate profiles and skill analyses.

## Contribution
Contributions are welcome! Please feel free to open issues or submit pull requests.

## License
[Consider adding a license here, e.g., MIT, Apache 2.0]

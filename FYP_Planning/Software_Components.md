# Software Components & Libraries

This document lists all the major software components, libraries, and frameworks utilized across the Coral Health Assessment project.

## 1. Machine Learning & Data Processing
These libraries power the core AI functionality, from data fetching and preprocessing to model training and evaluation.

*   **TensorFlow & Keras**: The primary deep learning framework used for building, compiling, and training the underlying CNN architecture, specifically the `EfficientNetB0` model.
*   **Scikit-learn**: Used for calculating robust performance metrics, such as generation of the classification report and confusion matrix during the evaluation phase.
*   **OpenCV (`opencv-python`)**: Crucial for image preprocessing (reading, resizing, color conversions) and for applying the JET colormap for Grad-CAM heatmap overlays.
*   **Pandas**: Utilized for reading and managing structured data, particularly the robust audit results (CSV).
*   **NumPy (`numpy<2.0.0`)**: The foundational library for numerical operations, array manipulation (including multi-scale TTA crops), and array transformations.
*   **Matplotlib**: Used for generating static graphical plots such as training history charts and classification reports.
*   **Seaborn**: Utilized alongside Matplotlib to render aesthetically pleasing confusion matrix heatmaps.
*   **Pillow (PIL)**: Used for generic image handling and processing.
*   **Kaggle Datasets (BHD Coral Dataset)**: The project sources its main dataset (BHD Coral Dataset) directly from Kaggle for training the CNN model on high-quality real-world coral reef images.

## 2. Hardware Acceleration & Environment
Since the project utilizes an NVIDIA RTX 3070 GPU for deep learning workloads, specific hardware acceleration software is required to enable training and fast inference.

*   **NVIDIA GPU Drivers**: The fundamental drivers to interface the Operating System with the RTX 3070 GPU.
*   **CUDA Toolkit**: NVIDIA's parallel computing platform and programming model, allowing TensorFlow to leverage the GPU for accelerated computation.
*   **cuDNN (CUDA Deep Neural Network library)**: A GPU-accelerated library of primitives for deep neural networks, required by TensorFlow for optimized performance.

## 3. Backend Web Architecture
The backend is responsible for routing web traffic, serving HTML templates, and providing the RESTful API endpoint for real-time model inferences.

*   **Flask**: A lightweight Python WSGI web application framework that serves the frontend UI and orchestrates requests to the loaded AI models.
*   **Flask-CORS**: Extracts the complexities of Cross-Origin Resource Sharing, allowing the backend API to interface seamlessly with varied frontend deployments (like external mobile or web apps).

## 4. Frontend Web Interface
The user interface is designed to be modern, responsive, and provide high-fidelity visual feedback without the overhead of heavy JavaScript frameworks.

*   **HTML5 / CSS3 / Vanilla JavaScript**: The foundational web technologies driving the structure, layout, and client-side logic of the dashboard interface.
*   **TailwindCSS (via CDN)**: A utility-first CSS framework used extensively for rapidly building responsive, modern styling and sleek UI components.
*   **Lucide Icons (via CDN)**: A comprehensive family of clean, vector-based SVG icons used throughout the user interface for enhanced visual aesthetics.
*   **Chart.js (via CDN)**: A JavaScript charting library used to generate the interactive, dynamic "Training & Validation Loss" charts directly within the browser ecosystem.

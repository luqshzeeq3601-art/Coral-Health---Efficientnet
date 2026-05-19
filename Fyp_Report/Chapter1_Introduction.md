# Chapter 1: Introduction

## 1.1 Introduction

Coral reefs are among the most biologically diverse and economically valuable ecosystems on the planet. They support approximately 25% of all known marine species while covering less than 1% of the ocean floor (Burke et al., 2011). Coral reefs provide essential ecosystem services including coastal protection, fisheries habitat, tourism revenue, and pharmaceutical resources. However, these vital ecosystems are under severe threat from climate change, ocean acidification, pollution, and destructive human activities. The increasing frequency and severity of mass coral bleaching events, driven primarily by rising sea surface temperatures, has led to significant and widespread coral mortality across the globe (Hughes et al., 2018).

Coral bleaching occurs when environmental stressors cause the expulsion of symbiotic zooxanthellae algae from coral tissues, resulting in the characteristic white appearance. If stressors persist, bleached corals may eventually die, leading to the collapse of reef structures and the loss of biodiversity they support. The monitoring and assessment of coral reef health is therefore a critical task for marine conservation. Traditional assessment methods rely heavily on manual underwater surveys conducted by trained marine biologists, which are time-consuming, expensive, and limited in spatial and temporal coverage (Gonzalez-Rivero et al., 2016).

Recent advances in deep learning, particularly Convolutional Neural Networks (CNNs), have demonstrated exceptional capability in image classification tasks across diverse domains including medical imaging, remote sensing, and ecological monitoring. Transfer learning, whereby a model pretrained on a large-scale dataset such as ImageNet is fine-tuned for a domain-specific task, has proven especially effective when labelled data is limited (Tan & Le, 2019). These advances offer a promising pathway towards automating coral reef health assessment through image analysis, enabling faster, more consistent, and more scalable monitoring compared to manual methods.

This project presents the development of an automated coral reef health classification system utilising the EfficientNetB0 architecture with transfer learning. The system classifies coral reef images into three categories: Healthy, Bleached, and Dead. To improve classification robustness, the model employs Stochastic Weight Averaging (SWA) with a five-seed ensemble strategy, Multi-Scale Test-Time Augmentation (TTA), and Temperature Scaling for confidence calibration. Furthermore, Gradient-weighted Class Activation Mapping (Grad-CAM) is integrated to provide visual explanations of the model's classification decisions, thereby enhancing interpretability and trust in the system's outputs. A web-based application is also developed to enable practical deployment with real-time inference and explainability visualisation.

---

## 1.2 Problem Statement

The health of coral reef ecosystems worldwide is deteriorating at an alarming rate due to climate change, ocean warming, and anthropogenic pressures. Effective conservation and management efforts require accurate, timely, and scalable monitoring of coral reef conditions. However, current monitoring practices face several critical challenges:

1. **Manual survey limitations.** Traditional coral health assessment depends on manual underwater surveys by trained marine biologists. These surveys are labour-intensive, time-consuming, costly, and inherently limited in the spatial and temporal extent of coverage they can achieve.

2. **Subjectivity and inconsistency.** Visual assessment of coral health by human observers is subject to inter-observer variability, fatigue, and subjective judgement, which can lead to inconsistent classification outcomes across different surveys and personnel.

3. **Scalability constraints.** The vast spatial extent of coral reef ecosystems, spanning hundreds of thousands of square kilometres globally, makes comprehensive manual monitoring impractical with current resources and methods.

4. **Delayed response.** The time required to collect, process, and analyse survey data through manual methods often results in significant delays between data acquisition and the generation of actionable insights, hindering timely conservation interventions.

There is therefore a pressing need for an automated, accurate, and interpretable system capable of classifying coral reef health conditions from image data. Such a system would complement existing monitoring efforts by providing rapid, consistent, and scalable assessments that can support evidence-based conservation decision-making.

---

## 1.3 Project Objectives

The objectives of this project are as follows:

1. To develop a deep learning model based on a pretrained EfficientNetB0 architecture with Stochastic Weight Averaging (SWA) and multi-seed ensemble strategy for coral reef health classification.

2. To apply Gradient-weighted Class Activation Mapping (Grad-CAM) as a visual explanation method to support the interpretation and validation of the model's classification decisions.

3. To evaluate the model's performance using standard classification metrics, including accuracy, precision, recall, and F1-score, on a held-out test set.

4. To deploy the trained model as a web-based application with real-time inference and explainability visualisation capabilities.

---

## 1.4 Project Scope

The scope of this project is defined as follows:

1. **Dataset.** The project utilises the BHD Coral Dataset sourced from Kaggle, comprising 795 coral reef images categorised into three classes: Healthy, Bleached, and Dead. No private, proprietary, or self-collected datasets are used.

2. **Classification task.** The project addresses multi-class image classification using a pretrained EfficientNetB0 backbone with transfer learning. The classification is limited to the three defined classes and does not extend to species-level identification or disease diagnosis beyond the Healthy–Bleached–Dead taxonomy.

3. **Model architecture and training.** The final model employs EfficientNetB0 pretrained on ImageNet as the feature extraction backbone. Five independently seeded models (seeds 42, 43, 44, 45, and 46) are trained with Stochastic Weight Averaging (SWA) and their predictions are combined via averaging to form an ensemble. Input images are preprocessed to 224 × 224 × 3 RGB resolution with data augmentation including rotation, horizontal flip, brightness adjustment, and contrast variation. Hard-example oversampling (×20) is applied for the minority Bleached and Dead classes to address class imbalance.

4. **Inference enhancement.** Multi-Scale Test-Time Augmentation (TTA) is applied at two resolutions (224 × 224 and 256 × 256) with horizontal flip, and Temperature Scaling (T = 0.441) is used for post-hoc confidence calibration.

5. **Explainability.** Gradient-weighted Class Activation Mapping (Grad-CAM) is implemented to generate heatmap overlays on input images using the JET colourmap, highlighting the image regions most influential to the model's classification decisions.

6. **Deployment.** The trained ensemble model is deployed as a locally hosted web application built on the Flask framework. The application supports drag-and-drop image upload, real-time classification with calibrated confidence scores, and Grad-CAM overlay visualisation. A one-click launcher script (`run_coral_ai.bat`) is provided for ease of execution.

7. **Hardware environment.** Model training and inference are performed on a workstation equipped with an NVIDIA RTX 3070 GPU, utilising CUDA and cuDNN for hardware-accelerated computation.

8. **Exclusions.** The project does not involve real-time video analysis, live data collection or streaming, drone or autonomous underwater vehicle (AUV) integration, or cloud deployment.

---

## 1.5 Project Significance

This project contributes to the field of marine environmental monitoring by demonstrating the feasibility and effectiveness of deep learning-based coral reef health classification. The key contributions and significance of this work are outlined as follows:

1. **Automated classification.** The development of a CNN-based classification system reduces the dependence on manual surveys for coral health assessment, enabling faster and more consistent evaluations of reef conditions.

2. **Ensemble robustness.** The use of a five-seed SWA ensemble with TTA and temperature scaling establishes a robust inference pipeline that mitigates the effects of random initialisation and improves prediction reliability, achieving a test accuracy of 98.11% on a held-out dataset of 159 images.

3. **Interpretability through Grad-CAM.** The integration of Grad-CAM provides visual explanations for the model's classification decisions, allowing marine scientists and stakeholders to verify that the model attends to biologically relevant features rather than artefacts or noise. This enhances trust and transparency in the system's outputs.

4. **Practical deployment.** The development of a web-based application with an intuitive user interface bridges the gap between model development and practical usability, enabling non-technical users to perform coral health assessments with minimal setup.

5. **Reproducibility.** The use of deterministic dataset splits, fixed random seeds, and documented training procedures ensures that the results are fully reproducible, supporting academic rigour and future comparative studies.

---

## 1.6 Summary of Chapters

This report is organised into five chapters as follows:

**Chapter 1: Introduction** provides the background and motivation for the project, defines the problem statement, states the project objectives, delineates the project scope, and discusses the significance of the work.

**Chapter 2: Literature Review** presents a review of related works in coral reef monitoring, deep learning for image classification, transfer learning, ensemble methods, and explainable artificial intelligence (XAI) techniques relevant to this project.

**Chapter 3: Methodology** describes the research methodology, including the dataset preparation, model architecture selection, training strategy, evaluation protocol, explainability implementation, and deployment approach.

**Chapter 4: Results and Discussion** presents the experimental results, including training behaviour analysis, classification performance metrics, confusion matrix analysis, Grad-CAM visualisation results, baseline comparison, and inference time evaluation. Key findings are discussed in relation to the project objectives.

**Chapter 5: Conclusion and Future Work** summarises the key findings, discusses the limitations of the current work, and proposes directions for future research and improvement.

---

*Last Updated: 29 April 2026*

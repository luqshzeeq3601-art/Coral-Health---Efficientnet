# Chapter 3: Methodology

## 3.X Overview of Proposed System

This chapter presents the methodology adopted for the development of an automated coral reef health classification system using deep learning. The proposed system follows a structured pipeline consisting of ten sequential stages, as illustrated in Figure 3.X. Each stage is described in detail in the following subsections.

---

## 3.X.1 Data Acquisition

The first stage of the methodology involves the acquisition of the coral reef image dataset. The dataset used in this project is the BHD Coral Dataset, which comprises underwater images of coral reefs categorised into three health condition classes. Table 3.X summarises the dataset composition.

**Table 3.X: Dataset Composition**

| Class | Number of Images | Description |
|-------|:----------------:|-------------|
| Healthy | 712 | Coral reefs exhibiting vibrant coloration, intact polyp structures, and no visible signs of stress or degradation. |
| Bleached | 720 | Coral reefs displaying partial or complete loss of coloration due to the expulsion of symbiotic algae (zooxanthellae), commonly triggered by elevated sea surface temperatures. |
| Dead | 150 | Coral reefs that have lost all living tissue, frequently characterised by algae overgrowth and structural deterioration. |

The total dataset consists of 1,582 coral reef images stored in PNG and JPEG formats. A notable class imbalance is present, as the Dead class contains significantly fewer samples compared to the Healthy and Bleached classes. This imbalance is addressed in subsequent stages through oversampling and class weighting strategies, as discussed in Section 3.X.4.

---

## 3.X.2 Data Pre-processing

Data pre-processing transforms raw images into a standardised format suitable for input into the deep learning model. The following operations are applied to every image in the dataset:

i. **Colour Space Conversion** — Images are loaded using OpenCV, which reads images in BGR (Blue-Green-Red) format by default. Each image is then converted to RGB (Red-Green-Blue) colour space to match the expected input format of the EfficientNet-B0 architecture.

ii. **Image Resizing** — All images are resized to a uniform spatial resolution of 224 × 224 pixels using bilinear interpolation. This dimension corresponds to the standard input size of EfficientNet-B0, as specified in the original architecture design by Tan and Le (2019).

iii. **Data Type Normalisation** — Pixel values are cast to 32-bit floating-point representation (float32) to ensure sufficient numerical precision during gradient computation and weight updates throughout the training process.

These pre-processing steps ensure that all images possess a consistent shape, colour format, and numerical representation, regardless of their original resolution or aspect ratio. This consistency is essential for efficient batch processing during model training.

---

## 3.X.3 Data Splitting

The pre-processed dataset is partitioned into three mutually exclusive subsets using stratified random splitting. A fixed random seed (seed = 42) is employed to ensure full reproducibility of the data partition. Table 3.X presents the split ratios and the purpose of each subset.

**Table 3.X: Data Split Configuration**

| Subset | Proportion | Purpose |
|--------|:----------:|---------|
| Training Set | 80% | Used to optimise the model parameters through backpropagation and gradient descent. |
| Validation Set | 10% | Used to monitor training progress, detect overfitting, and guide hyperparameter tuning. The model does not learn from this subset. |
| Test Set | 10% (159 images) | Reserved for the final, unbiased evaluation of the trained model. This subset is never exposed to the model during training or validation. |

Stratified splitting is employed to preserve the proportional class distribution (Healthy, Bleached, Dead) within each subset. This is particularly critical given the imbalanced representation of the Dead class. The split indices are persisted to a JSON configuration file to guarantee that the identical partition is maintained across all training seeds and any subsequent experiments.

It is important to note that data splitting is performed prior to data augmentation. This ordering prevents data leakage, a methodological error that would arise if augmented copies of the same original image were to appear in both the training and test sets, thereby inflating evaluation metrics artificially.

---

## 3.X.4 Data Augmentation

Data augmentation is applied exclusively to the training set to artificially expand the effective dataset size and improve the model's ability to generalise to unseen images. The augmentation pipeline applies stochastic geometric and photometric transformations to training images on-the-fly during each epoch, ensuring that the model encounters different variations of every sample across training iterations.

Table 3.X summarises the augmentation techniques employed in this project.

**Table 3.X: Data Augmentation Techniques**

| Technique | Configuration | Purpose |
|-----------|:-------------:|---------|
| Rotation | ±20° | Simulates varying camera orientations during underwater image capture. |
| Width/Height Shift | ±15% | Accounts for positional variation of coral subjects within the image frame. |
| Horizontal Flip | Enabled | Produces valid training samples, as coral structures exhibit horizontal symmetry. |
| Zoom | ±15% | Simulates different capture distances between the camera and the coral reef. |
| Shear | ±5% | Introduces minor geometric distortion to improve geometric invariance. |
| Brightness Jitter | 0.8–1.2× | Simulates variations in underwater illumination and water clarity. |
| Colour Jitter | Hue ±5%, Saturation 0.8–1.2× | Accounts for variations in water colour across different marine environments. |
| Mixup (Zhang et al., 2018) | α = 0.1 | Linearly interpolates pairs of training images and their corresponding labels to produce synthetic training samples, encouraging smoother decision boundaries. |

In addition to the above transformations, a hard example mining strategy is implemented to address the class imbalance problem. Images that were identified as difficult to classify during preliminary experiments are oversampled at elevated rates during training. Specifically, hard examples from the Dead class are oversampled at a factor of 30×, while hard examples from other classes are oversampled at a factor of 20×. Furthermore, balanced class weights are computed using the inverse class frequency method and applied during loss calculation, with the Dead class receiving an additional 1.3× weight multiplier to impose a higher penalty for misclassifications of this underrepresented class.

---

## 3.X.5 Model Training

The classification model is constructed using EfficientNet-B0 (Tan & Le, 2019) as the backbone feature extractor through transfer learning. EfficientNet-B0 was selected for this project due to its favourable trade-off between classification accuracy and computational efficiency, achieved through compound scaling that uniformly adjusts network width, depth, and input resolution.

### 3.X.5.1 Model Architecture

Table 3.X describes the architecture of the classification model built upon the EfficientNet-B0 backbone.

**Table 3.X: Model Architecture**

| Layer | Configuration |
|-------|---------------|
| Base Model | EfficientNet-B0 pre-trained on ImageNet; last 100 layers fine-tuned, remaining layers frozen. |
| Global Average Pooling | Reduces 7 × 7 × 1280 feature maps to a 1280-dimensional feature vector. |
| Dropout | Rate = 0.4; randomly deactivates 40% of neurons during training to mitigate overfitting. |
| Dense Output Layer | 3 neurons with Softmax activation function, producing a probability distribution over the three coral health classes. |
| L2 Regularisation | λ = 0.0002; applies weight decay to the output layer to constrain model complexity. |

### 3.X.5.2 Training Configuration

Table 3.X presents the training hyperparameters and configurations used during model training.

**Table 3.X: Training Configuration**

| Parameter | Value |
|-----------|:-----:|
| Optimiser | Adam (Kingma & Ba, 2015) |
| Loss Function | Categorical Cross-Entropy with Label Smoothing (ε = 0.05) |
| Learning Rate Schedule | Cosine Decay (initial rate = 8 × 10⁻⁵) |
| Number of Epochs | 30 |
| Batch Size | 16 |
| Ensemble Size | 5 models (seeds: 42, 43, 44, 45, 46) |

### 3.X.5.3 Stochastic Weight Averaging (SWA)

To further improve generalisation performance, Stochastic Weight Averaging (SWA) (Izmailov et al., 2018) is applied during the final five epochs of training for each seed. SWA operates by maintaining a running average of model weights collected at the end of each epoch during this window. The resulting averaged weights correspond to a point in a wider, flatter region of the loss landscape, which has been shown to yield superior generalisation compared to the final single-epoch weights. The SWA-averaged weights are saved as the deployment checkpoint for each seed.

### 3.X.5.4 Ensemble Strategy

Five models are trained independently using different random seeds to form a 5-model ensemble. During inference, predictions from all five SWA-averaged models are aggregated by computing the arithmetic mean of their output probability vectors. The class with the highest averaged probability is selected as the final prediction. This ensemble strategy reduces prediction variance and has been demonstrated to improve classification robustness compared to reliance on any single model (Lakshminarayanan et al., 2017).

---

## 3.X.6 Hyperparameter Tuning

Hyperparameter tuning was conducted through systematic experimentation to identify the configuration that maximises classification performance while maintaining training stability. Table 3.X presents the key hyperparameters that were adjusted from their initial baseline values, along with the rationale for each modification.

**Table 3.X: Hyperparameter Tuning Summary**

| Parameter | Baseline Value | Optimised Value | Rationale |
|-----------|:--------------:|:---------------:|-----------|
| Dropout Rate | 0.7 | 0.4 | The high baseline dropout caused training accuracy to fall below validation accuracy (inverted curves), indicating excessive regularisation. |
| L2 Regularisation | 0.0005 | 0.0002 | Reduced weight penalty allows the model to learn finer discriminative features between visually similar classes. |
| Label Smoothing | 0.1 | 0.05 | A lower smoothing factor permits the model to develop higher confidence in its correct predictions. |
| Initial Learning Rate | 5 × 10⁻⁵ | 8 × 10⁻⁵ | A moderately higher learning rate accelerates convergence without compromising training stability. |
| Fine-Tuned Layers | Last 150 | Last 100 | Freezing additional pre-trained layers reduces the risk of overfitting on the relatively small coral dataset. |
| Rotation Range | 40° | 20° | Excessive rotation introduced artificial black border artifacts that degraded model performance. |
| Vertical Flip | Enabled | Disabled | Vertical flipping is not ecologically valid, as coral reefs do not appear inverted in underwater imagery. |
| Dead Class Oversampling | 20× | 30× | Increased exposure to minority class samples improves Dead class precision. |
| Dead Class Weight Multiplier | 1.0× | 1.3× | A higher loss penalty for Dead class misclassifications directs the model to prioritise this underrepresented class. |

These adjustments collectively resolved three critical issues observed during initial training: (i) inverted training curves caused by excessive regularisation, (ii) poor precision on the Dead class, and (iii) Grad-CAM misattribution on Dead coral samples.

---

## 3.X.7 Save Model

Upon completion of training, all model artifacts are serialised and stored to facilitate deployment and ensure reproducibility. Table 3.X lists the saved artifacts and their purposes.

**Table 3.X: Saved Model Artifacts**

| Artifact | File Format | Description |
|----------|:-----------:|-------------|
| SWA Checkpoints | .weights.h5 | SWA-averaged weights for each of the five seeds; these serve as the primary deployment models loaded by the web application during inference. |
| Best Epoch Weights | .weights.h5 | Weights from the training epoch that achieved the highest validation accuracy, saved automatically via the ModelCheckpoint callback. |
| Temperature Calibration File | .txt | A scalar temperature value used for post-hoc probability calibration, ensuring that the model's output confidence scores are well-calibrated to reflect true prediction reliability. |
| Training History | .json | Raw accuracy and loss values for each epoch across all seeds, enabling subsequent replotting and comparative analysis. |

All model files are stored within the designated model directory. The SWA checkpoint files are the primary artifacts loaded by the Flask-based web application for real-time coral health inference.

---

## 3.X.8 Model Interpretability (Grad-CAM)

To ensure transparency and trustworthiness of the model's predictions, Gradient-weighted Class Activation Mapping (Grad-CAM) (Selvaraju et al., 2017) is employed. Grad-CAM produces visual explanations in the form of heatmaps that highlight the spatial regions of an input image that contributed most significantly to the model's classification decision.

### 3.X.8.1 Grad-CAM Procedure

The Grad-CAM computation proceeds as follows:

i. A forward pass is performed through the model to obtain the predicted class probability distribution.

ii. The gradient of the predicted class score is computed with respect to the activations of the final convolutional layer (top_conv) in EfficientNet-B0 via backpropagation.

iii. These gradients are globally average-pooled across the spatial dimensions to produce a set of channel-wise importance weights.

iv. A weighted linear combination of the convolutional feature maps, using the computed importance weights, generates the class-discriminative localisation map.

v. A ReLU activation is applied to the resulting map to retain only features that have a positive influence on the predicted class.

vi. The heatmap is upsampled to the original image dimensions (224 × 224) using bilinear interpolation and overlaid onto the input image using the JET colour map for visualisation.

### 3.X.8.2 Smoothing Techniques

Two smoothing techniques are applied to produce higher-quality heatmaps suitable for academic reporting:

i. **Eigen Smooth** — Principal Component Analysis (PCA) is applied to the activation-gradient product tensor to extract the dominant spatial activation pattern. This removes noise contributed by minor activation channels with minimal computational overhead.

ii. **Augmentation Smooth** — Grad-CAM heatmaps are computed for six augmented variants of each input image (three brightness levels × two horizontal flip states) and subsequently averaged. This yields spatially stable attention maps that are less sensitive to minor input perturbations.

Grad-CAM visualisations enable domain experts, such as marine biologists, to verify that the model attends to ecologically meaningful coral features — for instance, polyp texture and coloration patterns for Healthy corals, whitened or discoloured patches for Bleached corals, and algae overgrowth or structural collapse for Dead corals — rather than irrelevant background elements.

---

## 3.X.9 Model Evaluation

The trained ensemble model is evaluated on the held-out test set, which was not exposed to the model during training or hyperparameter tuning, to obtain an unbiased assessment of classification performance. Table 3.X defines the evaluation metrics employed.

**Table 3.X: Evaluation Metrics**

| Metric | Definition |
|--------|------------|
| Accuracy | The proportion of test samples for which the predicted class matches the true class label. |
| Precision | For a given class, the ratio of true positive predictions to the total number of positive predictions made for that class. |
| Recall (Sensitivity) | For a given class, the ratio of true positive predictions to the total number of actual positive samples of that class in the test set. |
| F1-Score | The harmonic mean of precision and recall, providing a single balanced metric that accounts for both false positives and false negatives. |
| Confusion Matrix | A matrix representation showing the frequency of each combination of true and predicted class labels across all test samples. |

### 3.X.9.1 Multi-Scale Test-Time Augmentation (TTA)

To maximise prediction robustness during evaluation, Multi-Scale Test-Time Augmentation is applied:

i. Each test image is processed at two spatial scales: 224 × 224 pixels (the native resolution) and 256 × 256 pixels (subsequently centre-cropped to 224 × 224 pixels).

ii. At each scale, both the original image and its horizontally flipped counterpart are evaluated.

iii. The output probability vectors from all five ensemble models across all TTA views are averaged to produce the final class prediction.

This procedure yields 20 independent predictions per test image (5 models × 2 scales × 2 flip states), substantially reducing the influence of any individual noisy prediction and improving overall classification reliability.

---

## 3.X.10 Output Results

The final stage of the methodology consolidates all evaluation outputs and trained model artifacts into structured, reproducible formats for both academic documentation and system deployment. Table 3.X summarises the outputs produced.

**Table 3.X: System Outputs**

| Output | File Format | Description |
|--------|:-----------:|-------------|
| Classification Report | .txt and .png | Per-class precision, recall, F1-score, and overall accuracy in both text and tabular image formats. |
| Confusion Matrix | .png | A colour-coded heatmap visualisation illustrating the distribution of correct and incorrect predictions across all class combinations. |
| Grad-CAM Visualisations | .png | Representative heatmap overlays for each class, demonstrating the model's spatial attention during classification. |
| Training History Plots | .png | Line charts depicting the 5-seed average training and validation accuracy and loss curves over 30 epochs. |
| Trained Model Weights | .h5 | Deployable SWA-ensemble model checkpoints integrated into the Flask-based Coral Health AI web application. |

These outputs fulfil two objectives. First, they provide the quantitative and qualitative evidence necessary for academic evaluation within this FYP report. Second, they constitute the deployment artifacts required by the Coral Health AI web application, which enables end users to perform real-time coral reef health classification through a browser-based interface.

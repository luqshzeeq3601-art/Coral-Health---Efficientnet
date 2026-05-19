import sys
from PIL import Image

def combine_images():
    img1_path = r"c:\Users\ZeeqRyz\Desktop\BASEPROJECT\03_Model_Evaluation\Efficientnet base vs Ensemble\09_gradcam_wrong_prediction_bleached_492.png"
    img2_path = r"c:\Users\ZeeqRyz\Desktop\BASEPROJECT\03_Model_Evaluation\Efficientnet base vs Ensemble\11_gradcam_wrong_prediction_dead_14_current.png"
    out_path = r"c:\Users\ZeeqRyz\Desktop\BASEPROJECT\03_Model_Evaluation\Efficientnet base vs Ensemble\12_combined_wrong_predictions_492_and_14.png"

    img1 = Image.open(img1_path)
    img2 = Image.open(img2_path)
    
    # Resize img2 to match img1's width if necessary
    if img1.width != img2.width:
        new_height = int(img2.height * (img1.width / img2.width))
        img2 = img2.resize((img1.width, new_height), Image.Resampling.LANCZOS)
    
    # Crop the top 9% of img2 to remove the redundant title "Wrong Prediction Grad-CAM"
    crop_y = int(img2.height * 0.09)
    img2_cropped = img2.crop((0, crop_y, img2.width, img2.height))
    
    # Create new image
    combined = Image.new('RGB', (img1.width, img1.height + img2_cropped.height), (255, 255, 255))
    
    # Paste images
    combined.paste(img1, (0, 0))
    combined.paste(img2_cropped, (0, img1.height))
    
    combined.save(out_path)
    print(f"Successfully generated {out_path}")

if __name__ == '__main__':
    combine_images()

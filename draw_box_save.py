import cv2
import os

# Load image
def load_image(path):
    return cv2.imread(path)

def draw_colored_border(image, rect, color='orange', thickness=4):
    colors = {'red': (0, 0, 255),
              'orange': (0, 165, 255),
              'blue': (255, 0, 0)}
    
    chosen_color = colors.get(color.lower(), (0, 0, 255))  # default 'red'

    # Draw box
    x, y, w, h = rect
    cv2.rectangle(image, (x, y), (x + w, y + h), chosen_color, thickness, cv2.LINE_AA)
    return image, image[y:y+h, x:x+w]  # Also return the cropped part

# Processing single image
def process_image(image_path, rect):
    image = load_image(image_path)
    full_image, cropped_image = draw_colored_border(image, rect)
    return full_image, cropped_image

def main(directory, save_subdir="box", crop_subdir="crop"):
    # Create the directories for saving full images and crops
    full_dir = os.path.join(directory, save_subdir)
    crop_dir = os.path.join(directory, crop_subdir)
    os.makedirs(full_dir, exist_ok=True)
    os.makedirs(crop_dir, exist_ok=True)

    # List images in the directory
    images = [os.path.join(directory, f) for f in os.listdir(directory) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    if not images:
        print("Directory contains no image files.")
        return

    # Get ROI
    first_image = load_image(images[0])
    roi = cv2.selectROI("Image", first_image, False, False)
    cv2.destroyAllWindows()

    # Draw boxes and crop for every image
    for image_path in images:
        full_image, cropped_image = process_image(image_path, roi)

        # Generate filenames
        base_name = os.path.basename(image_path)
        name, ext = os.path.splitext(base_name)
        full_name = f"{name}_box{ext}"
        crop_name = f"{name}_crop{ext}"

        # Save the processed images
        full_path = os.path.join(full_dir, full_name)
        crop_path = os.path.join(crop_dir, crop_name)
        
        cv2.imwrite(full_path, full_image)
        cv2.imwrite(crop_path, cropped_image)

        print(f"Processed and saved full image: {full_path}")
        print(f"Processed and saved cropped image: {crop_path}")

if __name__ == "__main__":
    directory = 'C:\\Users\\wyh\\Desktop\\Project\\Paper_FusionCLIP\\fig\\ablation_clear_vivid_none\\ab3\\'
    main(directory)

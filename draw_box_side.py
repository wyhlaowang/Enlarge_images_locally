import os
import cv2
from PIL import Image, ImageDraw

class ImagePlotter:
    def __init__(self, image_path):
        self.image_path = image_path
        self.refPt = []
        self.cropping = False
        self.regions = []
        self.image = None
        self.clone = None

    def click_and_crop(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.refPt = [(x, y)]
            self.cropping = True
        elif event == cv2.EVENT_LBUTTONUP:
            self.refPt.append((x, y))
            self.cropping = False
            cv2.rectangle(self.image, self.refPt[0], self.refPt[1], (255, 165, 0), 2)
            cv2.imshow("Image", self.image)
            if len(self.refPt) == 2:
                self.regions.append((self.refPt[0][0], self.refPt[0][1], self.refPt[1][0], self.refPt[1][1]))

    def setup_image_selection(self):
        self.image = cv2.imread(self.image_path)
        self.clone = self.image.copy()
        cv2.namedWindow("Image")
        cv2.setMouseCallback("Image", self.click_and_crop)
        while True:
            cv2.imshow("Image", self.image)
            key = cv2.waitKey(1) & 0xFF
            if key == ord('r'):
                self.image = self.clone.copy()
                self.regions.clear()
            elif key == ord('q') or len(self.regions) == 1:
                break
        cv2.destroyAllWindows()

class ImageCropper:
    def __init__(self, dir_path, region, out_path, placement):
        self.dir_path = dir_path
        self.region = region
        self.out_path = out_path
        self.placement = placement  # 'right' or 'bottom'

    def process_image(self):
        file_ls = os.listdir(self.dir_path)
        file_ls = [i for i in file_ls if i.endswith(('.png', '.jpg'))]
        for i in file_ls:
            image = cv2.imread(self.dir_path+i, cv2.IMREAD_COLOR)
            pil_image = Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
            self.create_cropped_image(pil_image, file_name=i)

    def create_cropped_image(self, pil_image, file_name):
        region = self.region[0]
        original_width, original_height = pil_image.size
        region_width = region[2] - region[0]
        region_height = region[3] - region[1]

        if self.placement == 'right':
            magnification = original_height / region_height
            new_width = int(region_width * magnification)
            new_height = original_height
            new_image = Image.new("RGB", (original_width + new_width, original_height))
            x_offset = original_width
            y_offset = 0
        else:  # 'bottom'
            magnification = original_width / region_width
            new_width = original_width
            new_height = int(region_height * magnification)
            new_image = Image.new("RGB", (original_width, original_height + new_height))
            x_offset = 0
            y_offset = original_height

        crop_img = pil_image.crop(region).resize((new_width, new_height), Image.ANTIALIAS)
        new_image.paste(pil_image, (0, 0))
        new_image.paste(crop_img, (x_offset, y_offset))
        draw_new = ImageDraw.Draw(new_image)

        draw_new.rectangle([region[0], region[1], region[2], region[3]], outline=(255, 165, 0), width=5)
        draw_new.rectangle([(x_offset, y_offset), (x_offset + new_width, y_offset + new_height)], outline=(255, 165, 0), width=10)


        if not os.path.exists(self.out_path):
            os.makedirs(self.out_path)
        new_image.save(self.out_path + file_name)

def main(dir_path, roi_image, save_dir='box', placement='bottom'):
    plotter = ImagePlotter(dir_path+roi_image)
    plotter.setup_image_selection()
    cropper = ImageCropper(dir_path, plotter.regions, os.path.join(dir_path, save_dir), placement)
    cropper.process_image()



if __name__ == "__main__":
    main(dir_path='C:\\Users\\wyh\Desktop\\Project\\Paper_FusionCLIP\\fig\\ablation_clear_vivid_none\\ab9\\',
         roi_image="ld.png",
         save_dir='box/',
         placement='right')  # Use 'right' or 'bottom' for placement

# Note: line witdth

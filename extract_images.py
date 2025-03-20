import fitz
import os

def extract_images(pdf_path, output_dir):
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Open the PDF
    doc = fitz.open(pdf_path)
    images = []
    
    # Iterate through pages
    for page_num in range(len(doc)):
        page = doc[page_num]
        image_list = page.get_images()
        
        # Save each image
        for img_index, img in enumerate(image_list):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            image_ext = base_image["ext"]
            
            # Generate filename
            image_name = f'page{page_num + 1}_img{img_index + 1}.{image_ext}'
            image_path = os.path.join(output_dir, image_name)
            
            # Save image
            with open(image_path, 'wb') as img_file:
                img_file.write(image_bytes)
            images.append(image_path)
            print(f"Saved {image_path}")
    
    return images

if __name__ == '__main__':
    pdf_path = 'uploads/Your-Property-Has-Been-Selected-for-a-Renewable-Energy-Opportunity.pdf'
    output_dir = 'static/extracted_images'
    images = extract_images(pdf_path, output_dir)
    print(f"\nExtracted {len(images)} images")

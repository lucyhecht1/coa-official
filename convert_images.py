from PIL import Image
import os

# Define input and output directories
input_folder = "static/images/gallery2025/" 
output_folder = "static/images/gallery2025_compressed/"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Process all image files in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(("jpg", "jpeg", "png")):  # process these formats
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # Convert to WebP
        webp_filename = os.path.splitext(filename)[0] + ".webp"  # Change extension to .webp
        output_path = os.path.join(output_folder, webp_filename)

        # Resize images
        max_width = 1200
        if img.width > max_width:
            new_height = int((max_width / img.width) * img.height)
            img = img.resize((max_width, new_height), Image.LANCZOS)

        # Save as WebP with compression (adjust quality as needed)
        img.save(output_path, "WEBP", quality=70)  # Quality 50-80 is ideal for balance

        print(f"Converted & Compressed: {filename} → {webp_filename}")

print("✅ All images have been converted to WebP and compressed!")

from PIL import Image
import os

# Define input (JPGs) and output (compressed WebPs) directories
input_folder = "static/images/gallery2025/"
output_folder = "static/images/gallery2025_compressed/"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Process all image files in the input folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(("jpg", "jpeg", "png")):
        img_path = os.path.join(input_folder, filename)
        img = Image.open(img_path)

        # Convert to WebP
        webp_filename = os.path.splitext(filename)[0] + ".webp"
        output_path = os.path.join(output_folder, webp_filename)

        # Skip if WebP file already exists
        if os.path.exists(output_path):
            print(f"Skipping (already converted): {filename}")
            continue

        # Resize images (optional, max width 1200px)
        max_width = 1200
        if img.width > max_width:
            new_height = int((max_width / img.width) * img.height)
            img = img.resize((max_width, new_height), Image.LANCZOS)

        # Save as WebP with compression (quality 70 is a good balance)
        img.save(output_path, "WEBP", quality=70)

        print(f"Converted & Compressed: {filename} → {webp_filename}")

print("✅ All images have been converted to WebP and compressed!")

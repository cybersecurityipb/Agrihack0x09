from PIL import Image

# Open the uploaded QR code image
image_path = 'D:\soal ctf\PIL_1\qr.png'
image = Image.open(image_path)

# Create a new image with the same size
new_image = Image.new('RGBA', image.size)

# Shift odd rows by 5 pixels
for y in range(image.size[1]):
    for x in range(image.size[0]):
        # If the row is odd (y is odd)
        if y % 2 != 0:
            # Shift pixel by 5 positions (with wrap-around)
            new_x = (x + 10) % image.size[0]
            new_y = (y + 10) % image.size[1]
        else:
            new_x = (x - 10) % image.size[0]
            new_y = (y - 10) % image.size[1]
        # Place the pixel from original image to new image
        new_image.putpixel((x, y), image.getpixel((new_x, new_y)))

# Save the modified image

new_image.save('chall.png')


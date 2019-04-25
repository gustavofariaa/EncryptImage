from PIL import Image
import DES
import os

# Key for encrypt and decrypt
KEY = '1597538462268423571597419638522587414569517538462573918462739158'

# Open original image
IMAGE = Image.open("image.png")

def encrypt_image():

  # Convert image to RGB and generate a new encrypted image
  RGB = IMAGE.convert('RGB')
  IMAGE_ENCRYPT = Image.new('RGB', (IMAGE.size[0], IMAGE.size[1]), 0)
  pixels_encrypt = IMAGE_ENCRYPT.load()

  # Variables to print loading
  percentage = "0.0%"
  count = 0 
  percentage_increment = 0

  # Go trhough matrix to encrypt pixel by pixel
  for line in range(IMAGE.size[0]):
    for pixel in range(IMAGE.size[1]):

      # Get pixel RGB and padding with '0123456789ABCEEF'
      red, green, blue = RGB.getpixel((line, pixel))
      clean_text = str(red)+ str(green) + str(blue) + '0123456789ABCEEF' 

      # Run DES and generate obfuscated text
      encrypt = DES.DES_encrypt(clean_text, KEY, ROUNDS, ZERO_KEY)

      # Get RGB without padding from obfuscated text
      red_encrypt = int(encrypt[56:64], 2)
      green_encrypt = int(encrypt[47:55], 2)
      blue_encrypt = int(encrypt[38:46], 2)

      # Merge all encrypted pixels to generate encrypted image
      pixels_encrypt[line, pixel] = (red_encrypt, green_encrypt, blue_encrypt, 255)

      # Print loading
      print_percentage(count, percentage, 0)
      print_percentage(count, percentage, 175)
      print_percentage(count, percentage, 350)
      if (round((100 * count) / (512 * 512), 2) == round(percentage_increment, 2)):
        percentage = str(round((100 * count) / (512 * 512), 2)) + "%"
        percentage_increment += 0.2
      count += 1

  # Print complete when image is encrypted
  os.system("clear")
  print ("Complete    [100%]")

  # Save encrypted image whit distinct names
  if ZERO_KEY:
    IMAGE_ENCRYPT.save("image_DES_with_zero_key.png", "PNG")
  elif (ROUNDS == 16):
    IMAGE_ENCRYPT.save("image_DES.png", "PNG")
  elif (ROUNDS == 0):
    IMAGE_ENCRYPT.save("image_DES_without_iteration.png", "PNG")
  elif (ROUNDS == 1):
    IMAGE_ENCRYPT.save("image_DES_with_one_iteration.png", "PNG")
  else:
    IMAGE_ENCRYPT.save("encrypted_image.png", "PNG")

def print_percentage(count, percentage, mod):
  # Update loading print
  if(count % 500 == mod):
    os.system("clear")
    print ("Loading  \\  [" + str(percentage) + "]")
    print ("")

# Encrypt image   
ROUNDS = 16
ZERO_KEY = False
encrypt_image()


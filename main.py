from PIL import Image
import numpy as np
from typing import List, Any
import logging
from lsb_encoder_decoder.encoder import Encoder

def logging_config() -> None:  
  logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s    |   %(levelname)s [%(name)s - %(funcName)s]   |   %(message)s",
                        datefmt="%d-%m-%Y %H:%M:%S",
                        filename="LSB_Steganography.log")

def image_to_bits(image: List[List[List[Any]]]) -> List[List[List[str]]]:
  cont = 0
  for row in range(len(image)):
    for rgb_channel in range(len(image[row])):
      for idx,value in enumerate(image[row][rgb_channel]):
        #print(f"original value: {value}, bin: {bin(value)}, 8_bit_bin: {bin(value).split('b')[1].zfill(8)}, 8_bit_bin_to_int: {int(bin(value).split('b')[1].zfill(8),2)}")
        image[row][rgb_channel][idx] = "0b" + bin(value).split('b')[1].zfill(8)
        cont += 1
  logging.info(f"Evaluated {cont} RGB channel values")
  return image
  

if __name__ == "__main__":
  
  logging_config()
  
  #List[List[List[int]]] -> List[riga1[pixel1, pixel2,..., pixel344] dove pixel = [R,G,B]
  pixels = np.array(Image.open("test_image.jpg"))
  logging.info(f"Calling image_to_bits")
  bit_pixels = image_to_bits(pixels.tolist())
  logging.info(f"image_to_bits completed!")
  del pixels
  print(bit_pixels[0][0:6])
  
  encoder = Encoder()
  if encoder.set_image(bit_pixels):
    logging.info("Image correctly setted inside the Encoder")
    if encoder.set_secret_message(): 
      logging.info("Secret message correctly setted inside the Encoder")
      try:
        encoded_image = encoder.encode()
        logging.info("Secret message correctly encoded inside the image")
      except Exception:
        logging.error("An error occurred while encoding the secret message inside the given image")
        exit()
  
  print(encoded_image[0][0:6])
from PIL import Image
import numpy as np
from typing import List, Any
import logging
from lsb_encoder_decoder.encoder import Encoder
from lsb_encoder_decoder.decoder import Decoder

IMAGE_NAME = "test_image.jpg"

def logging_config() -> None:  
  logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s    |   %(levelname)s [%(name)s - %(funcName)s]   |   %(message)s",
                        datefmt="%d-%m-%Y %H:%M:%S",
                        filename="LSB_Steganography.log")

#conversion of the int value into 0b8 str format
def image_to_bits(image: List[List[List[Any]]]) -> List[List[List[str]]]:
  cont = 0
  for row in range(len(image)):
    for rgb_channel in range(len(image[row])):
      for idx,value in enumerate(image[row][rgb_channel]):
        #image[row][rgb_channel][idx] = "0b" + bin(value).split('b')[1].zfill(8)
        image[row][rgb_channel][idx] = bin(value).format("08b")
        cont += 1
  logging.info(f"Evaluated {cont} RGB channel values")
  return image


if __name__ == "__main__":
  
  logging_config()
  
  #List[List[List[int]]] -> List[riga1[pixel1, pixel2,..., pixel344] dove pixel = [R,G,B]
  pixels = np.array(Image.open(IMAGE_NAME))
  size = pixels.shape
  image_size = size[0]*size[1]*size[2]
  logging.info(f"\nImage size: ({size[0]} x {size[1]} x {size[2]}), for a total size of {image_size}.")
  logging.info("Calling image_to_bits")
  bit_pixels = image_to_bits(pixels.tolist())
  logging.info(f"image_to_bits completed!")
  del pixels
  
  encoder = Encoder()
  if encoder.set_image(bit_pixels, image_size):
    logging.info("Image correctly setted inside the Encoder")
    if encoder.set_secret_message(): 
      logging.info("Secret message correctly setted inside the Encoder")
      try:
        encoded_image = encoder.encode()
        logging.info("Secret message correctly encoded inside the image")
      except Exception:
        logging.error("An error occurred while encoding the secret message inside the given image")
        exit()
    else: exit()
  else: exit()
  
  del bit_pixels
  
  logging.info("Generating encoded image")
  if encoder.generate_encoded_image(encoded_image):
    logging.info("Encoded image generated!")
  else:
    logging.error("Error while generating the encoded image!")
    exit()
    
  decoder = Decoder()
  if decoder.set_image(image_to_bits(encoded_image)):
    logging.info("Image correctly setted inside the Decoder")
    try:
      decoded_image = decoder.decode()
      logging.info("Secret message correctly decoded from the image")
    except Exception:
      logging.error("An error occurred while decoding the secret message from the given image")
      exit()
  else: exit()
      
  logging.info("Extracting secret message")
  secret_message = decoder.message_from_image(decoded_image)
  #secret_message = message_from_image(decoded_image)
  if secret_message:
    logging.info(f"Secret message extracted:\n\n{secret_message}")
  else:
    logging.error("Error while extracting the secret message from the image!")
    exit()
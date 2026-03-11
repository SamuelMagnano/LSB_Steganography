from typing import List, Any
import logging
import numpy as np
from PIL import Image

class Encoder:
  image: List[List[List[str]]]
  image_size: int
  secret_message: str
  logging.basicConfig(level=logging.INFO,
                      format="%(asctime)s    |   %(levelname)s [%(name)s - %(funcName)s]   |   %(message)s",
                      datefmt="%d-%m-%Y %H:%M:%S",
                      filename="LSB_Steganography.log")
  
  def set_secret_message(self) -> bool:
    value = input("1. Define the message via terminal\n2. Define the message via file\n")
    if value.strip() == "1":
      self.secret_message = input("Insert secret message: ")
      if len(self.secret_message) > 0:
        logging.info("Secret messagge loaded correctly!")
        return True
      else:
        logging.warning("Secret message cannot be empty!")
        return False
    else: #read file and use the content as the secret_message
      value = input("Drag and drop the file.\n")
      try:
        with open(value) as f:
          self.secret_message = f.read()
        f.close()
        if len(self.secret_message) > 0:
          return True
        else:
          logging.warning("Secret message cannot be empty!")
          return False
      except:
        logging.warning("Error while retrieving the file containing the secret message!")
        return False
   
  def set_image(self, image: List[List[List[str]]], size:int) -> bool:
    if image != None and size>0:
      self.image = image
      self.image_size = size
      return True
    logging.warning("Image empty or size == 0!")
    return False
  
  #Message -> str -> Ascii -> 8 bit binary
  def message_to_bin(self, secret_message:str) -> str:
    bin_message: str = ""
    for char in secret_message:
      bin_message += bin(ord(char)).split("b")[1].zfill(8)
    logging.info(f"Binary message: {bin_message}")
    return bin_message
  
  #returns the encoded image as its binary representation where each pixel has, for each color channel, the lsb changed according to the binary conversion of the related character bit 
  def encode(self) -> List[List[List[str]]]:
    if self.secret_message == "": 
      logging.warning("Secret message empty!")
      raise Exception("Error while encoding: Secret message empty!")
    if len(self.secret_message)*8 > self.image_size: 
      logging.warning("Secret message bigger than the image capability!")
      choice = input("Secret message bigger than the image capability!\nContinuing will result in a truncated secret message once decoded [y/n]: ")
      if choice != "y":
        logging.warning(f"Choice: {choice}, therefore the secret message will not be encoded in the given image!")
        raise Exception("Error while encoding: Secret message too big!")
      else: logging.warning(f"Choice: {choice}, therefore the secret message will be encoded truncated in the given image!")
    logging.info("Converting the secret message to binary (UTF-8)")
    bin_message = self.message_to_bin(self.secret_message)
    logging.info("Conversion done!")
    cont = 0
    logging.info("Encoding the secret message inside the image")
    for row in range(len(self.image)):
      for rgb_channel in range(len(self.image[row])):
        for idx in range(len(self.image[row][rgb_channel])):
          if not bin_message: continue
          x = bin_message[0]
          bin_message = bin_message[1:]
          #result = "0b" + bin((int(self.image[row][rgb_channel][idx], 2) & 0b11111110) | int(x)).split("b")[1].zfill(8)
          result = bin((int(self.image[row][rgb_channel][idx], 2) & 0b11111110) | int(x)).format("08b")
          self.image[row][rgb_channel][idx] = result
          cont += 1
    logging.info(f"Evaluated {cont} RGB channel values")
    logging.info("Encoding completed!")
    if cont>=0:
      return self.image 
    else: 
      logging.error("Error while encoding")
      raise Exception("Error while encoding")
    
  def generate_encoded_image(self, encoded_image: List[List[List[Any]]]) -> bool:
    cont = 0
    for row in range(len(encoded_image)):
      for rgb_channel in range(len(encoded_image[row])):
        for idx in range(len(encoded_image[row][rgb_channel])):
          encoded_image[row][rgb_channel][idx] = int(encoded_image[row][rgb_channel][idx],2)
          cont += 1
    logging.info(f"Evaluated {cont} RGB channel values")
    if cont <= 0: 
      logging.warning("Error converting the bits back to integers!")
      raise Exception("Error while converting the bits back to integers!")
    else:
      pixels_array = np.array(encoded_image, dtype=np.uint8)
      new_image = Image.fromarray(pixels_array, 'RGB')
      new_image.save("encoded_image.png")
      return True
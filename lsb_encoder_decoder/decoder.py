from typing import List
import logging

class Decoder:
  image: List[List[List[str]]]
  mask = "0b00000001"
  logging.basicConfig(level=logging.INFO,
                      format="%(asctime)s    |   %(levelname)s [%(name)s - %(funcName)s]   |   %(message)s",
                      datefmt="%d-%m-%Y %H:%M:%S",
                      filename="LSB_Steganography.log")
   
  def set_image(self, image: List[List[List[str]]]) -> bool:
    if image != None:
      self.image = image
      return True
    return False
  
  #returns the decoded image as its binary representation (all 0 except the least significant bit)
  def decode(self) -> List[List[List[str]]]:
    cont = 0
    logging.info("Decoding the secret message inside the image")
    for row in range(len(self.image)):
      for rgb_channel in range(len(self.image[row])):
        for idx in range(len(self.image[row][rgb_channel])):
          result = bin(int(self.image[row][rgb_channel][idx],2) & int(self.mask,2)) # 0b followed by all 0 except last one that is x -> python compresses to just 0bx
          self.image[row][rgb_channel][idx] = result
          cont += 1
    logging.info(f"Evaluated {cont} RGB channel values")
    logging.info("Decoding completed!")
    if cont>=0:
      return self.image 
    else: 
      logging.error("Error while decoding")
      raise Exception("Error while decoding")
    
  #return the secret message as string
  def message_from_image(self) -> str:
    cont = 0
    secret_message = []
    buffer = "0b"
    for row in range(len(self.image)):
      for rgb_channel in range(len(self.image[row])):
        for idx in range(len(self.image[row][rgb_channel])):
          buffer += self.image[row][rgb_channel][idx].split("b")[1]
          if len(buffer)>=10:
            secret_message.append(buffer)
            buffer = "0b"
          cont += 1
    return "".join(chr(int(word,2)) for word in secret_message)
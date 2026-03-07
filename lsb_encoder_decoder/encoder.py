from typing import List
import logging

class Encoder:
  image: List[List[List[str]]]
  secret_message: str
  mask = 11111111 #7bit, need the least significant one (from our words)
  logging.basicConfig(level=logging.INFO,
                      format="%(asctime)s    |   %(levelname)s [%(name)s - %(funcName)s]   |   %(message)s",
                      datefmt="%d-%m-%Y %H:%M:%S",
                      filename="LSB_Steganography.log")
  
  def set_secret_message(self) -> bool:
    message = ""
    value = input("1. Define the message\nDrag and drop the file otherwise\n")
    if value.strip() == "1":
      self.secret_message = input()
      logging.info("Secret messagge loaded correctly!")
      return True
    else: #read file and use the content as the secret_message
      ...
    logging.warning("Error while loading the secret message!")
    return False
   
  def set_image(self, image: List[List[List[str]]]) -> bool:
    if image != None:
      self.image = image
      return True
    return False
  
  #Message -> str -> Ascii -> 8 bit binary
  def message_to_bin(self, secret_message:str) -> str:
    bin_message: str = ""
    for char in secret_message:
      bin_message += bin(ord(char)).split("b")[1].zfill(8)
    logging.info(f"Binary message: {bin_message}")
    return bin_message
  
  def encode(self) -> List[List[List[str]]]:
    if self.secret_message == "": 
      logging.warning("Secret message empty!")
      raise Exception("Error while encoding: Secret message empty!")
    logging.info("Converting the secret message to binary (UTF-8)")
    bin_message = self.message_to_bin(self.secret_message)
    logging.info("Conversion done!")
    cont = 0
    logging.info("Encoding the secret message inside the image")
    for row in range(len(self.image)):
      for rgb_channel in range(len(self.image[row])):
        for idx,value in enumerate(self.image[row][rgb_channel]):
          #print(f"original value: {value}, bin: {bin(value)}, 8_bit_bin: {bin(value).split('b')[1].zfill(8)}, 8_bit_bin_to_int: {int(bin(value).split('b')[1].zfill(8),2)}")
          if len(bin_message)<=0: continue
          x = bin_message[0]
          bin_message = bin_message[1:]
          result = "0b" + bin(int(self.image[row][rgb_channel][idx],2) & int(f"0b1111111{x}",2)).split("b")[1].zfill(8)
          self.image[row][rgb_channel][idx] = result
          cont += 1
    logging.info(f"Evaluated {cont} RGB channel values")
    logging.info("Encoding completed!")
    if cont>=0:
      return self.image 
    else: 
      logging.error("Error while encoding")
      raise Exception("Error while encoding")
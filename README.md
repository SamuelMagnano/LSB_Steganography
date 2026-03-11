Simple and naive approach to the LSB Steganography message encoding inside an image.

I decided to do this mini-project just because i saw an IG reel talking about this tecnique and thought it was cool and easy enough to replicate given my almost absent understanding of cybersecurity since i'm majoring in AI.

My approach to the problem always puts the secret message starting from the upper left corner of the image and is defined as follows:

![steganography](https://github.com/user-attachments/assets/6af96e4e-2750-460d-9a73-1dd00a873055)

Inside this folder you will need to:
- test image (test_image.jpg in the code), that has to be RGB coded
- file .txt containing the secret message (if you do not want to pass the message through terminal)

Once all the above is set you can then proceed as follows:

Access via terminal this folder and create the venv (virtual enviroment) inside of it
```
python -m venv venv
```
Activate the venv
```
venv\Scripts\activate
```
Install the required libraries
```
pip install numpy pillow
```

I know i could have done all of this in a much efficient and easier way but i wanted to manipulate the pixels using their 8-bit representation and not the python optimized ones.

**I DO NOT OWN ANY IMAGE THAT MIGHT BE INSIDE THIS REPOSITORY ONCE PUBLIC.**
**I SIMPLY USED THEM TO TEST THE CODE.**
**ALL RIGHTS ARE RESERVED TO THE OWNERS.**

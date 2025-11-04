import numpy as np
from PIL import Image
import os
from scipy import ndimage


# Funtion: Convert colored image to grayscale
def grayscale_conversion(image):
  """
  Convert colored image to grayscale using weighted average method
  Luminance formula = 0.299*R + 0.587*G + 0.114*B
  """

  image_matrix = np.array(image)

  print(f"Input image shape : {image_matrix.shape}")

  #Handle different image formats
  if len(image_matrix.shape) == 3:
    R = image_matrix[:, :, 0].astype(np.float32)
    G = image_matrix[:, :, 1].astype(np.float32)
    B = image_matrix[:, :, 2].astype(np.float32)

    grayscale = 0.299*R + 0.587*G + 0.114*B

    # Convert back to uint8 and ensure proper range
    grayscale = np.clip(grayscale, 0, 255)  # Ensure values are within 0-255
    grayscale_matrix = grayscale.astype(np.uint8)

  elif len(image_matrix.shape) == 2:    #already grayscale
    grayscale_matrix = image_matrix

  print(f"Output grayscale shape: {grayscale_matrix.shape}")
  print(f"Output value range: [{np.min(grayscale_matrix)}, {np.max(grayscale_matrix)}]")


  return Image.fromarray(grayscale_matrix)


#Function: load and process captured image
def load_and_process_image(image_path):
  """
  Load image, convert to grayscale, resize, and save as 2D matrix
  """
  try:
      # Load image
      img = Image.open(image_path)
      print(f"Original image size: {img.size}")
      print(f"Original image mode: {img.mode}")

      # Convert to grayscale'
      grayscale_img = grayscale_conversion(img)    #img.convert('L') built-in method

      # Resize to manageable dimensions (maintaining aspect ratio)
      max_dimension = 500  # Adjust2D numpy array (matrix based on your machine's capabilities)
      width, height = grayscale_img.size

      if width > height:
          new_width = max_dimension
          new_height = int(height * (new_width / width))
      else:
          new_height = max_dimension
          new_width = int(width * (new_height / height))

      resized_grayscale_img = grayscale_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
      print(f"Resized image size: {resized_grayscale_img.size}")

      # Convert to 2D numpy array (matrix)
      grayscale_matrix = np.array(resized_grayscale_img)

      print("Image successfully processed and converted to 2D matrix!")
      print(f"Matrix shape: {grayscale_matrix.shape}")

      return grayscale_matrix

  except Exception as e:
      print(f"Error loading image: {e}")
      return False


def rotate_image(img_matrix, angle):
  """
  Rotate image by specified angle (in degrees)
  """
  try:
      rotated_matrix = ndimage.rotate(img_matrix, angle, reshape=True, mode='constant', cval=255)
      return rotated_matrix
  except Exception as e:
      print(f"Error during rotation: {e}")
      return None


def scale_image(img_matrix, scale_factor):
    """
    Scale image by specified factor
    """
    try:
        if scale_factor <= 0:
            print("Scale factor must be positive!")
            return None

        # Calculate new dimensions
        height, width = img_matrix.shape
        new_height = int(height * scale_factor)
        new_width = int(width * scale_factor)

        # Resize using PIL for better quality
        img = Image.fromarray(img_matrix)
        scaled_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)

        return np.array(scaled_img)

    except Exception as e:
        print(f"Error during scaling: {e}")
        return None


def translate_image(img_matrix, dx, dy):
  """
  Translate image by dx (horizontal) and dy (vertical) pixels
  """
  try:
      # Use scipy for translation
      translated = ndimage.shift(img_matrix, (dy, dx), mode='constant', cval=255)
      return translated
  except Exception as e:
      print(f"Error during translation: {e}")
      return None
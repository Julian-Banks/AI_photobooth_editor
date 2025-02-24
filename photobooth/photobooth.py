import pygame
import numpy as np
from picamera2 import Picamera2
from openai import OpenAI
import time
import requests
from io import BytesIO
from PIL import Image

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((512, 560))
pygame.display.set_caption("Camera Feed")
clock = pygame.time.Clock()

# Initialize Camera
picam2 = Picamera2()
config = picam2.create_preview_configuration(main={'size': (512, 512)}, buffer_count=2)
picam2.configure(config)
picam2.start()

# Button
button_colour = (0,255,30)
button_rect = pygame.Rect(206, 520, 100,30)
font = pygame.font.SysFont(None,24)
button_text = font.render('Capture', True, (0,0,0)) 

#Current Time
current_time = time.strftime("%Y-%m-%d_%H-%M-%S:")

#Create  OpenAi client
client = OpenAI()

#Do API request for an image edit
def get_edited_photo():
    response = client.images.edit(
    model = "dall-e-2",
    image = open("image.png", "rb"),
    mask  = open("mask.png", "rb"),
    prompt= "A Superhero in a photobooth. They are strong and majestic, dressed in the coolest superhero outfit!", 
    n = 1,
    size = "512x512",
    )
    print(response.data[0].url)
    img_url = response.data[0].url
    return img_url

def download_edited_photo(img_url):
    response = requests.get(img_url)
    if response.status_code == 200:
        img_data = BytesIO(response.content)
        pilImage = Image.open(img_data).convert("RGB")
        img_data = pygame.image.fromstring(pilImage.tobytes(), pilImage.size, pilImage.mode)
        pygame.image.save(img_data, f'edited_image{current_time}.png')
        print('imaged saved')
        return img_data
    else:
        print("failed to fetch data")

# Main Loop
running = True
try:
    while running:    # Capture Frame
        frame = picam2.capture_array()
        frame = np.rot90(frame)  # Rotate if necessary
        frame = frame[:,:,:3]
        frame = pygame.surfarray.make_surface(frame)
        frame = pygame.transform.scale(frame, (512, 512))

        # Display Frame
        screen.blit(frame, (0, 0))

       # Draw Button
        pygame.draw.rect(screen, button_colour, button_rect)
        screen.blit(button_text, (button_rect.x +10, button_rect.y +5))

        pygame.display.flip()

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pygame.image.save(frame, 'image.png')
                print("Photo saved as image.png")
                current_time = time.strftime("%Y-%m-%d_%H-%M-%S")
                pygame.image.save(frame, f'image{current_time}.png')
                #Call OPENAI API
                response = get_edited_photo()
                #response = "https://oaidalleapiprodscus.blob.core.windows.net/private/org-VmNCpwHQnrUC7csIUR7eq7MR/user-DVzP1er1Aa9264fuK7aVSD2A/img-uD3zuQS9GMdWkmoM8IheDqgL.png?st=2025-02-21T13%3A41%3A19Z&se=2025-02-21T15%3A41%3A19Z&sp=r&sv=2024-08-04&sr=b&rscd=inline&rsct=image/png&skoid=d505667d-d6c1-4a0a-bac7-5c84a87759f8&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2025-02-21T00%3A23%3A28Z&ske=2025-02-22T00%3A23%3A28Z&sks=b&skv=2024-08-04&sig=O1ewLXje5OWVYfk%2BuSQhYM3M1YB2Vk5eaAJSBzHTx2Y%3D"
                edited_image = download_edited_photo(response)
                running = False

        clock.tick(30)  # Limit to 30 FPS
    print('Edited Image Being displayed')
    screen.blit(edited_image, (0,0))
    pygame.display.flip()
    time.sleep(10)
# Cleanup
    picam2.stop()
finally:
    picam2.stop()
    pygame.quit()



'''
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                print('Capturing photo...')
                ret, frame = camera.read()
                if ret:
                    frame = cv2.resize(frame, IMAGE_SIZE)
                    cv2.imwrite(CAPTURED_IMAGE, frame, [cv2.IMWRITE_PNG_COMPRESSION, 0])
                    print('Photo saved as', CAPTURED_IMAGE)
                    show_loading_overlay()

                    # Call the OpenAI Image Edit API
                    with open(CAPTURED_IMAGE, 'rb') as image_file, open(MASK_IMAGE, 'rb') as mask_file:
                       print('SEND OPENAI API')
                       ''' ''' response = client.images.edit(
                            model = "dall-e-2",
                            image=image_file,
                            mask=mask_file,
                            prompt='A super awesome superhero posing in a photobooth',
                            n=1,
                            size='512x512'
                        )''' '''

                    # Handle the response and save the edited image
                    if response and 'data' in response:
                        image_url = response['data'][0]['url']
                        img_data = requests.get(image_url).content
                        with open(EDITED_IMAGE, 'wb') as handler:
                            handler.write(img_data)

                        # Display the edited image
                        edited_image = pygame.image.load(EDITED_IMAGE)
                        screen.blit(pygame.transform.scale(edited_image, WINDOW_SIZE), (0, 0))
                        pygame.display.flip()
                        print('Edited image displayed')
                    else:
                        print('Failed to get a valid response from OpenAI')
            elif event.key == pygame.K_q:
                running = False

    ret, frame = camera.read()
    if ret:
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = np.rot90(frame)
        frame = pygame.surfarray.make_surface(frame)
        screen.blit(pygame.transform.scale(frame, WINDOW_SIZE), (0, 0))

    pygame.display.flip()
    clock.tick(30)

camera.release()
pygame.quit()
print('Camera and window closed.')

'''

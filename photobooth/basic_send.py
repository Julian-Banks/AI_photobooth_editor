from openai import OpenAI

client = OpenAI()


response = client.images.edit(
	model = "dall-e-2",
	image = open("image.png", "rb"),
	prompt = "A superhero posing for a photo",
	mask = open("mask.png","rb"),
	n=1,
	size = "512x512",
	)
	
print(response.data[0].url)

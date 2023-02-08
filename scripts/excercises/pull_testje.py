from PIL import Image

print("Hello Danny")
print("Nice commit")

with Image.open("chef.png") as img:
    img.load()

converted_img = img.transpose(Image.FLIP_LEFT_RIGHT)

converted_img.show()

converted_img.save("mirror_chef.png")
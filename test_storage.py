from storage import save_object, load_object

content = "Hello Git-Lite!"

object_id = save_object(content)

print("Object ID:", object_id)
print("Saved content:", load_object(object_id))
filenames = ['Entities.py', 'Global.py', 'Items.py', "Main_menu.py", "MapGen.py", "Mission_Manager.py",
             "Overworld_game.py", "Shaders.py", "UIElements.py", "Utils.py"]

with open('combined.txt', 'w') as outfile:
    for i, filename in enumerate(filenames):
        # Write the filename as a separator before each file's content
        outfile.write(f"==== {filename} ====\n\n")

        with open(filename, 'r') as infile:
            contents = infile.read()
            outfile.write(contents)

        # Add a newline after each file's content
        outfile.write('\n\n')
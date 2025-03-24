import os
import pygame as pg
import numpy as np
from math import pi, sin, cos
from PIL import Image, ImageTk

# Initialize pygame for the Earth visualization
pg.init()
# Disable sound to prevent audio conflicts
pg.mixer.quit()

class SpinningEarth:
    def __init__(self, width=150, height=150):
        # Set dimensions for the Earth visualization
        self.width = width
        self.height = height
        
        # Create a surface for rendering the Earth
        self.surface = pg.Surface((width, height))
        
        # Set constants
        self.FPS = 30
        self.R = width // 4  # Radius scaled to the surface size
        self.MAP_WIDTH = 139
        self.MAP_HEIGHT = 34
        
        # Initialize font
        self.my_font = pg.font.SysFont('arial', 6)  # Smaller font for the corner display
        
        # Load the Earth ASCII art
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, 'earth_W140_H35.txt')
        
        try:
            with open(file_path, 'r') as file:
                data = [file.read().replace('\n', '')]
                
            # Process ASCII characters
            self.ascii_chars = []
            for line in data:
                for char in line:
                    self.ascii_chars.append(char)
            
            self.inverted_ascii_chars = self.ascii_chars[::-1]
            
            # Create 3D coordinates
            self.xyz = []
            for i in range(self.MAP_HEIGHT + 1):
                lat = (pi / self.MAP_HEIGHT) * i
                for j in range(self.MAP_WIDTH + 1):
                    lon = (2 * pi / self.MAP_WIDTH) * j
                    x = round(self.R * sin(lat) * cos(lon), 2)
                    y = round(self.R * sin(lat) * sin(lon), 2)
                    z = round(self.R * cos(lat), 2)
                    self.xyz.append((x, y, z))
            
            # Initialize spin angle
            self.spin = 0
            self.loaded = True
            
        except FileNotFoundError:
            print(f"Earth file not found at: {file_path}")
            # Create a simple placeholder file
            self.create_placeholder_earth_file(file_path)
            self.loaded = False
    
    def create_placeholder_earth_file(self, file_path):
        """Create a simple placeholder Earth ASCII art file"""
        try:
            with open(file_path, 'w') as file:
                # Basic ASCII Earth
                earth_art = []
                width, height = 139, 34
                
                for y in range(height):
                    line = ""
                    for x in range(width):
                        dx, dy = x - width // 2, y - height // 2
                        distance = (dx**2 + dy**2)**0.5
                        
                        if distance < width // 4:
                            if (x + y) % 7 == 0:
                                line += "#"  # Continents
                            else:
                                line += "~"  # Oceans
                        else:
                            line += " "
                    earth_art.append(line)
                
                file.write('\n'.join(earth_art))
            print(f"Created placeholder {file_path} file.")
            
            # Now that we created the file, load it
            with open(file_path, 'r') as file:
                data = [file.read().replace('\n', '')]
                
            # Process ASCII characters
            self.ascii_chars = []
            for line in data:
                for char in line:
                    self.ascii_chars.append(char)
            
            self.inverted_ascii_chars = self.ascii_chars[::-1]
            
            # Create 3D coordinates
            self.xyz = []
            for i in range(self.MAP_HEIGHT + 1):
                lat = (pi / self.MAP_HEIGHT) * i
                for j in range(self.MAP_WIDTH + 1):
                    lon = (2 * pi / self.MAP_WIDTH) * j
                    x = round(self.R * sin(lat) * cos(lon), 2)
                    y = round(self.R * sin(lat) * sin(lon), 2)
                    z = round(self.R * cos(lat), 2)
                    self.xyz.append((x, y, z))
                    
            self.loaded = True
            
        except Exception as e:
            print(f"Error creating placeholder Earth file: {e}")
    
    def update(self):
        # Increment the spin angle
        self.spin += 0.05
    
    def render(self):
        if not self.loaded:
            # If the Earth file couldn't be loaded, draw a placeholder
            self.surface.fill((10, 10, 60))
            text = self.my_font.render("Earth file not found", True, (255, 255, 255))
            self.surface.blit(text, (10, self.height // 2))
            return self.surface
        
        # Clear the surface
        self.surface.fill((0, 0, 50))
        
        # Create projection
        pv = self.Projection(self.width, self.height, self.surface)
        
        # Create and render the globe
        globe = self.Object()
        globe_nodes = [i for i in self.xyz]
        globe.addNodes(np.array(globe_nodes))
        pv.addSurface('globe', globe)
        pv.rotateAll(self.spin)
        pv.display(self.inverted_ascii_chars, self.my_font, self.MAP_WIDTH, self.MAP_HEIGHT)
        
        return self.surface
    
    def get_tk_image(self):
        """Convert pygame surface to a tkinter-compatible image"""
        # Render the Earth to a pygame surface
        earth_surface = self.render()
        
        # Get the raw pixel data
        raw_str = pg.image.tostring(earth_surface, 'RGB')
        
        # Create a PIL Image from the raw pixel data
        image = Image.frombytes('RGB', (self.width, self.height), raw_str)
        
        # Convert PIL Image to Tkinter PhotoImage
        tk_image = ImageTk.PhotoImage(image)
        
        return tk_image
    
    class Projection:
        def __init__(self, width, height, surface):
            self.width = width
            self.height = height
            self.surface = surface
            self.background = (10, 10, 60)
            self.surfaces = {}

        def addSurface(self, name, surface):
            self.surfaces[name] = surface

        def display(self, inverted_ascii_chars, font, MAP_WIDTH, MAP_HEIGHT):
            i = 0
            for surface in self.surfaces.values():
                for node in surface.nodes:
                    text = inverted_ascii_chars[i]
                    text_surface = font.render(text, False, (0, 255, 0))
                    if i > MAP_WIDTH - 1 and i < (MAP_WIDTH * MAP_HEIGHT - MAP_WIDTH) and node[1] > 0:
                        self.surface.blit(text_surface, (self.width / 2 + int(node[0]), self.height / 2 + int(node[2])))
                    i += 1

        def rotateAll(self, theta):
            for surface in self.surfaces.values():
                center = surface.findCentre()

                c = np.cos(theta)
                s = np.sin(theta)

                # Rotating about Z - axis
                matrix = np.array([[c, -s, 0, 0],
                                  [s, c, 0, 0],
                                  [0, 0, 1, 0],
                                  [0, 0, 0, 1]])

                surface.rotate(center, matrix)
    
    class Object:
        def __init__(self):
            self.nodes = np.zeros((0, 4))

        def addNodes(self, node_array):
            ones_column = np.ones((len(node_array), 1))
            ones_added = np.hstack((node_array, ones_column))
            self.nodes = np.vstack((self.nodes, ones_added))

        def findCentre(self):
            mean = self.nodes.mean(axis=0)
            return mean

        def rotate(self, center, matrix):
            for i, node in enumerate(self.nodes):
                self.nodes[i] = center + np.matmul(matrix, node - center)
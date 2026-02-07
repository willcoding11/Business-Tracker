#imports
import pygame
from tkinter import filedialog
import pandas as pd

pygame.init()

window = pygame.display.set_mode((800, 500))

pygame.display.set_caption("AI Business Tracker")

HEADER_FONT = pygame.font.SysFont("bold", 50)
HEADER_TEXT = HEADER_FONT.render("AI Business Tracker", True, (255, 255, 255))
HEADER_TEXT_RECT = HEADER_TEXT.get_rect(center=(400, 37.5))

HEADER_COLOR = (59, 190, 255)
BG = (255, 255, 255) # Light blue

class ScrollBar:
    def __init__(self, x, y, width, height, bg_color, bar_color, scroll_bar_height, scroll_bar_y):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.bar_color = bar_color
        self.scroll_bar_height = scroll_bar_height
        self.scroll_bar_y = scroll_bar_y
        
        self.scroll_bar_rect = pygame.Rect(x, scroll_bar_y, width, scroll_bar_height)
        self.rect = pygame.Rect(x, y, width, height)

    def draw(self, window):
        pygame.draw.rect(window, self.bg_color, self.rect, border_radius=5)
        pygame.draw.rect(window, self.bar_color, self.scroll_bar_rect, border_radius=5)

class CSVFileDisplay:
    def __init__(self, name, path, x, y, width, height, bg_color, border_color, radius):
        self.name = name
        self.path = path
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.bg_color = bg_color
        self.border_color = border_color
        self.radius = radius

        self.df = pd.DataFrame()

        self.rect = pygame.Rect(x, y, width, height)

        self.scroll_bar = ScrollBar(x + width - 20, y + 10, 10, height - 20, (200, 200, 200), (100 , 100, 100), 30, 10 + self.y)

    def draw_header(self, window):
        text_surface = pygame.font.SysFont("bold", 50).render(self.name, True, (0, 0, 0 ))
        text_rect = text_surface.get_rect(center=(self.x + self.width/2, self.y + 30))
        window.blit(text_surface, text_rect)

    def draw_data(self, window):
        if self.df is not None:
            for index, row in self.df.iterrows():
                text_surface = pygame.font.SysFont("bold", 20).render(row[0], True, (0, 0, 0))
                text_rect = text_surface.get_rect(center=(self.x + self.width/2, (self.y + 60 + index*30) - (self.scroll_bar.scroll_bar_rect.y - self.y)))
                window.blit(text_surface, text_rect)

        self.draw_background_except_self(window)

    def draw_background_except_self(self, window):
        # Draw the background color everywhere except over the CSVFileDisplay area
        window_width, window_height = window.get_size()
        # Top area
        if self.y > 0:
            pygame.draw.rect(window, BG, (0, 0, window_width, self.y))
        # Bottom area
        if self.y + self.height < window_height:
            pygame.draw.rect(window, BG, (0, self.y + self.height, window_width, window_height - (self.y + self.height)))
        # Left area
        if self.x > 0:
            pygame.draw.rect(window, BG, (0, self.y, self.x, self.height))
        # Right area
        if self.x + self.width < window_width:
            pygame.draw.rect(window, BG, (self.x + self.width, self.y, window_width - (self.x + self.width), self.height))

    def draw(self, window):
        pygame.draw.rect(window, self.bg_color, self.rect, 5, border_radius=self.radius)

        self.scroll_bar.draw(window)

        self.draw_header(window)

    def get_total_business_names_height(self):
        if self.df is None or self.df.empty:
            return 0
        font = pygame.font.SysFont("bold", 20)
        name_height = font.get_height()
        # each name is drawn at y + 60 + index*30, so vertical spacing is 30 even if glyph height is smaller
        spacing = 30
        num_names = len(self.df)
        if num_names == 0:
            return 0
        return spacing * num_names

    def update(self):
        name_heights = self.get_total_business_names_height()
        if name_heights != 0:
            percentage = self.height / name_heights
            if percentage < 0: percentage = 0
            if percentage > 1: percentage = 1
        else:
            percentage = 0

        self.scroll_bar.scroll_bar_height = percentage * self.scroll_bar.height
        self.scroll_bar.scroll_bar_rect.height = self.scroll_bar.scroll_bar_height

class Button:
    def __init__(self, text, text_size, x, y, width, height, color, hover_color, radius, function):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.hover_color = hover_color
        self.is_hovering = False
        self.rect = pygame.Rect(x, y, width, height)
        self.radius = radius
        self.function = function
        
        self.text = text
        self.text_font = pygame.font.SysFont("bold", text_size)
        self.text_surface = self.text_font.render(text, True, (255, 255, 255))
        self.text_rect = self.text_surface.get_rect(center=(x + width/2, y + height/2))

    def draw(self, window):
        if self.is_hovering:
            pygame.draw.rect(window, self.hover_color, self.rect, border_radius=self.radius)
        else:
            pygame.draw.rect(window, self.color, self.rect, border_radius=self.radius)
        window.blit(self.text_surface, self.text_rect)

    def update(self):
        mouse_pos = pygame.mouse.get_pos()
        self.check_hover(mouse_pos)

        if self.is_hovering and pygame.mouse.get_pressed()[0]:
            if self.function is not None:
                self.function()

    def check_hover(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos):
            self.is_hovering = True
        else:
            self.is_hovering = False

def upload_csv():
    filename = filedialog.askopenfilename(initialdir = "/",
                                          title = "Select a File",
                                          filetypes = (("Text files",
                                                        "*.csv*"),
                                                       ("all files",
                                                        "*.*")))

    try:
        # Change label contents
        csv_file_display.path = filename
        csv_file_display.name = filename.split("/")[-1]
        csv_file_display.df = pd.read_csv(filename)
    except Exception as e:
        print(e)
        print("Error reading CSV file")

def remove_file():
    csv_file_display.path = "csv_file.csv"
    csv_file_display.name = "Businesses"
    csv_file_display.df = None

def draw_header():
    pygame.draw.rect(window, HEADER_COLOR, (0, 0, 800, 75))
    window.blit(HEADER_TEXT, HEADER_TEXT_RECT)

upload_button = Button("Upload CSV", 30, 20, 100, 150, 75, (59, 190, 255), (89, 210, 255), 10, upload_csv)
research_button = Button("Research", 30, 200, 100, 150, 75, (59, 190, 255), (89, 210, 255), 10, None)
delete_button = Button("Delete", 30, 380, 100, 150, 75, (235, 64, 52), (255, 94, 82), 10, remove_file)

csv_file_display = CSVFileDisplay("Businesses", "csv_file.csv", 20, 200, 510, 280, (59, 190, 255), (255, 255, 255), 10)

run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    upload_button.update()
    research_button.update()
    delete_button.update()

    csv_file_display.update()

    window.fill(BG)

    csv_file_display.draw_data(window)

    draw_header()

    upload_button.draw(window)
    research_button.draw(window)
    delete_button.draw(window)

    csv_file_display.draw(window)

    pygame.display.flip()

pygame.quit()
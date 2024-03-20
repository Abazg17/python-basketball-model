import pygame

class ImageButton:
    """A class representing an image button in pygame.

    Attributes:
        x (int): The x-coordinate of the top-left corner of the button.
        y (int): The y-coordinate of the top-left corner of the button.
        width (int): The width of the button.
        height (int): The height of the button.
        text (str): The text to display on the button.
        image_path (str): The file path of the image for the button.
        hover_image_path (str, optional): The file path of the image for the button when hovered.
    """

    def __init__(self, x, y, width, height, text, image_path, hover_image_path=None):
        """Initialize the image button with given parameters."""
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (width, height))
        self.hover_image = self.image
        if hover_image_path:
            self.hover_image = pygame.image.load(hover_image_path)
            self.hover_image = pygame.transform.scale(self.hover_image, (width, height)) 
        self.rect = self.image.get_rect(topleft=(x, y))
        self.is_hovered = False

    def draw(self, screen):
        """Draw the button on the given screen."""
        current_image = self.hover_image if self.is_hovered else self.image
        screen.blit(current_image, self.rect.topleft)

        font = pygame.font.Font(None, 34)
        text_surface = font.render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)

    def check_hover(self, mouse_pos):
        """Check if the mouse is hovering over the button."""
        self.is_hovered = self.rect.collidepoint(mouse_pos)

    def handle_event(self, event):
        """Handle events for the button."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.is_hovered:
            pygame.event.post(pygame.event.Event(pygame.USEREVENT, button=self))

    def rename(self, new_name):
        self.text = new_name
    
    def get_text(self):
        return self.text
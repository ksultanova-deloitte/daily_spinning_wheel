import pygame
import random
import math
import sys
from questions import all_questions


# Set up the screen
pygame.init()
WIDTH, HEIGHT = int(800 * 1.2), int(600 * 1.3)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Icebreaker Question Spinner")

# Colors and font
WHITE = (224, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
FONT = pygame.font.Font(None, 24)

# Wheel configuration
NUM_SEGMENTS = 8
RADIUS = int(250 * 1.2)
CENTER = (WIDTH // 2, HEIGHT // 2)
ANGLE = 360 / NUM_SEGMENTS

# Predefined colors for each segment
COLORS = [
    (255, 102, 102),  # Red
    (255, 178, 102),  # Orange
    (255, 255, 102),  # Yellow
    (178, 255, 102),  # Light Green
    (102, 255, 102),  # Green
    (102, 255, 178),  # Light Blue
    (102, 178, 255),  # Blue
    (178, 102, 255),  # Purple
]

# Randomly select 8 questions from the full list
questions = random.sample(all_questions, NUM_SEGMENTS)

# Ensure the number of segments matches the number of questions
if len(questions) != NUM_SEGMENTS:
    raise ValueError("The number of questions must match the number of segments")

# Function to draw the arrow pointing to the center of the top segment
def draw_arrow():
    arrow_points = [
        (CENTER[0], CENTER[1] - RADIUS - 10),  # Tip closer to the center
        (CENTER[0] - 30, CENTER[1] - RADIUS - 40),  # Left base
        (CENTER[0] + 30, CENTER[1] - RADIUS - 40),  # Right base
    ]
    pygame.draw.polygon(screen, BLUE, arrow_points)

# Function to draw the spinning wheel
def draw_wheel(current_angle):
    screen.fill(WHITE)

    for i in range(NUM_SEGMENTS):
        # Calculate start and end angles for this segment
        start_angle = math.radians(ANGLE * i + current_angle)
        end_angle = math.radians(ANGLE * (i + 1) + current_angle)

        # Calculate the polygon points for each segment
        points = [
            CENTER,
            (
                CENTER[0] + RADIUS * math.cos(start_angle),
                CENTER[1] + RADIUS * math.sin(start_angle)
            ),
            (
                CENTER[0] + RADIUS * math.cos(end_angle),
                CENTER[1] + RADIUS * math.sin(end_angle)
            )
        ]

        pygame.draw.polygon(screen, COLORS[i % len(COLORS)], points)

        # Calculate the angle for the text
        text_angle = (ANGLE * i + ANGLE / 2 + current_angle)
        text_x = CENTER[0] + RADIUS // 2 * math.cos(math.radians(text_angle))
        text_y = CENTER[1] + RADIUS // 2 * math.sin(math.radians(text_angle))

        # Render the text with adjusted parameters
        text_surface = FONT.render(questions[i], True, BLACK)
        rotated_text_surface = pygame.transform.rotate(text_surface, -text_angle)
        text_rect = rotated_text_surface.get_rect(center=(text_x, text_y))
        screen.blit(rotated_text_surface, text_rect)

    draw_arrow()  # Draw the arrow on top of the wheel
    pygame.display.update()

# Function to simulate spinning the wheel
def spin_wheel():
    spin_speed = random.randint(5, 10)
    current_angle = 0
    for i in range(300):
        draw_wheel(current_angle)
        pygame.time.wait(10)
        current_angle += spin_speed
        spin_speed = max(spin_speed * 0.98, 0.5)

    # Correct the current_angle to be within the range of 0 to 360
    current_angle = current_angle % 360

    # Calculate the selected segment's index based on the current angle
    selected_index = int((current_angle + (ANGLE / 2)) // ANGLE) % NUM_SEGMENTS

    # Calculate the final angle needed to align the selected segment with the arrow
    final_angle = selected_index * ANGLE

    # Adjust the angle so that the selected segment aligns perfectly with the arrow
    adjusted_final_angle = -(final_angle - current_angle) % 360

    # Correcting the wheel to stop at the exact position
    draw_wheel(adjusted_final_angle)

    return questions[selected_index]

# Main loop
running = True
result = None
drawing_wheel = True  # Flag to control when to draw the wheel

while running:
    if drawing_wheel:
        draw_wheel(0)

    if result:
        # Draw the result on top of the wheel without clearing the screen
        result_surface = FONT.render("Selected Question: " + result, True, BLACK)
        result_rect = result_surface.get_rect(center=(WIDTH // 2, HEIGHT - 30))
        screen.blit(result_surface, result_rect)
        pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if not result:
                result = spin_wheel()
                drawing_wheel = False  # Stop drawing the wheel after the result is shown
            else:
                result = None
                drawing_wheel = True  # Enable wheel drawing for a new spin

pygame.quit()

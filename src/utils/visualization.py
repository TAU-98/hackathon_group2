import pygame

def show_instruction_screen(screen, text, font, color, background):
    """
    Display an instruction screen with centered text.
    Args:
        screen: pygame display surface
        text: string to display
        font: pygame font object
        color: text color
        background: background color
    """
    screen.fill(background)
    lines = text.split('\n')
    y_offset = screen.get_height() // 2 - (len(lines) * font.get_height()) // 2
    for i, line in enumerate(lines):
        rendered = font.render(line, True, color)
        rect = rendered.get_rect(center=(screen.get_width() // 2, y_offset + i * font.get_height()))
        screen.blit(rendered, rect)
    pygame.display.flip()

def show_candidate_table(screen, attributes, weights, values_a, values_b, font, color, background):
    """
    Display a table comparing two candidates (A and B) with attribute names, weights, and values.
    Args:
        screen: pygame display surface
        attributes: list of attribute names
        weights: list of weights
        values_a: list of values for candidate A
        values_b: list of values for candidate B
        font: pygame font object
        color: text color
        background: background color
    """
    screen.fill(background)
    # Table header
    header = ['Attribute', 'Weight', 'A', 'B']
    col_widths = [200, 100, 100, 100]
    start_x = (screen.get_width() - sum(col_widths)) // 2
    start_y = screen.get_height() // 2 - (len(attributes) + 1) * font.get_height() // 2
    # Draw header
    for j, h in enumerate(header):
        rendered = font.render(str(h), True, color)
        rect = rendered.get_rect()
        rect.topleft = (start_x + sum(col_widths[:j]), start_y)
        screen.blit(rendered, rect)
    # Draw rows
    for i, attr in enumerate(attributes):
        row = [attr, str(weights[i]), str(values_a[i]), str(values_b[i])]
        for j, val in enumerate(row):
            rendered = font.render(val, True, color)
            rect = rendered.get_rect()
            rect.topleft = (start_x + sum(col_widths[:j]), start_y + (i + 1) * font.get_height())
            screen.blit(rendered, rect)
    pygame.display.flip()

def show_feedback(screen, message, font, color, background):
    """
    Display a feedback message (e.g., 'Correct', 'Incorrect', 'Too slow!').
    Args:
        screen: pygame display surface
        message: feedback string
        font: pygame font object
        color: text color
        background: background color
    """
    screen.fill(background)
    rendered = font.render(message, True, color)
    rect = rendered.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(rendered, rect)
    pygame.display.flip()

def show_score(screen, score, font, color, background):
    """
    Display the current score on the screen.
    Args:
        screen: pygame display surface
        score: integer score
        font: pygame font object
        color: text color
        background: background color
    """
    text = f"Your score is: {score}"
    rendered = font.render(text, True, color)
    rect = rendered.get_rect(center=(screen.get_width() // 2, screen.get_height() - 100))
    screen.blit(rendered, rect)
    pygame.display.flip() 
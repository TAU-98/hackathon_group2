import pygame
import pygame.freetype
from src.experiment.Enums import Consts

class Visualization:

    def __init__(self, screen, font, bg_color, accent_color, text_color):
        self.screen = screen
        self.font = font
        self.bg_color = bg_color
        self.accent_color = accent_color
        self.text_color = text_color

    def show_demographics_form(self) -> dict:
        """
        Display a demographics input form and return a dict with 'name', 'age', 'gender'.
        """
        responses = [''] * len(Consts.FIELDS)
        current = 0
        running = True
        clock = pygame.time.Clock()

        while running:
            self.screen.fill(self.bg_color)
            self._add_title(title_name="Demographics")
            for i, field in enumerate(Consts.FIELDS):
                self._add_field(field=field, i=i, current=current,
                                responses=responses)
            self._add_instruction(title='Press Enter to continue')
            pygame.display.flip()
            for event in pygame.event.get():
                current, running = self._deal_event(event=event, current=current, responses=responses)
            clock.tick(30)

        return dict(zip(['name', 'age', 'gender'], responses))

    @staticmethod
    def _deal_event(event, current, responses):
        """handles a single Pygame event for a simple text input form."""
        running = True
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if current < 2:
                    current += 1
                else:
                    running = False
            elif event.key == pygame.K_BACKSPACE:
                responses[current] = responses[current][:-1]
            elif event.key == pygame.K_TAB:
                current = (current + 1) % 3
            else:
                if len(responses[current]) < 20 and event.unicode.isprintable():
                    responses[current] += event.unicode
        return current, running

    def _add_instruction(self, title):
        """add instruction to the screen."""
        instr = self.font.render(title, True, self.accent_color)
        self.screen.blit(instr, (self.screen.get_width() // 2 - instr.get_width() // 2, 450))

    def _add_title(self, title_name):
        """add title to the screen."""
        title_font = pygame.font.SysFont('Arial Rounded MT Bold', 44)
        title = title_font.render(title_name, True, self.accent_color)
        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 60))

    def _add_field(self, field, i, current, responses):
        """add a field to the demographics table in the demographics form."""
        label = self.font.render(field + ':', True, self.accent_color)
        self.screen.blit(label, (self.screen.get_width() // 2 - 200, 180 + i * 80))
        # Draw input box
        box_rect = pygame.Rect(self.screen.get_width() // 2 - 50, 175 + i * 80, 300, 50)
        pygame.draw.rect(self.screen, self.accent_color if i == current else (180, 180, 180), box_rect, 2, border_radius=10)
        input_text = self.font.render(responses[i], True, self.accent_color)
        self.screen.blit(input_text, (box_rect.x + 10, box_rect.y + 10))

    def draw_gradient(self, top_color, bottom_color):
        """
        Draw a vertical gradient background from top_color to bottom_color.
        """
        height = self.screen.get_height()
        for y in range(height):
            ratio = y / height
            color = [int(top_color[i] * (1 - ratio) + bottom_color[i] * ratio) for i in range(3)]
            pygame.draw.line(self.screen, color, (0, y), (self.screen.get_width(), y))

    def show_instruction_screen(self, text, title=None):
        """show text and title in instruction screen."""
        self.draw_gradient(top_color=self.bg_color, bottom_color=(30,30,30))
        if title:
            self._add_title(title_name=title)
        lines = text.split('\n')
        y_offset = self.screen.get_height() // 2 - (len(lines) * self.font.get_height()) // 2
        for i, line in enumerate(lines):
            rendered = self.font.render(line, True, self.text_color)
            rect = rendered.get_rect(center=(self.screen.get_width() // 2, y_offset + i * self.font.get_height()))
            self.screen.blit(rendered, rect)
        pygame.display.flip()

    def show_candidate_table(self, attributes, weights, values_a, values_b, title=None):
        """
        Display a large, visually clear candidate table with columns: Weight | Attribute | A | B, with weights listed vertically.
        The 'Weight' header cell is shifted slightly left for better spacing.
        """
        self.draw_gradient(self.bg_color, (30,30,30))
        if title:
            title_font = pygame.font.SysFont('Arial Rounded MT Bold', 64)
            title_surf = title_font.render(title, True, self.accent_color)
            self.screen.blit(title_surf, (self.screen.get_width()//2 - title_surf.get_width()//2, 40))
        # Table header
        header_font = pygame.font.SysFont('Arial Rounded MT Bold', 48)
        cell_font = pygame.font.SysFont('Arial Rounded MT Bold', 44)
        header = ['Weight', 'Attribute', 'A', 'B']
        col_widths = [140, 320, 120, 120]
        n_rows = len(attributes) + 1  # header + attribute rows
        n_cols = 4
        table_width = sum(col_widths)
        table_height = (n_rows + 1) * 70 + 40
        start_x = (self.screen.get_width() - table_width) // 2
        start_y = self.screen.get_height() // 2 - table_height // 2 + 40
        # Draw rounded rectangle background for table
        table_rect = pygame.Rect(start_x-30, start_y-30, table_width+60, table_height+60)
        pygame.draw.rect(self.screen, (40,40,60), table_rect, border_radius=28)
        # Draw header row (centered, but shift 'Weight' left)
        y = start_y
        for j, h in enumerate(header):
            cell_x = start_x + sum(col_widths[:j])
            cell_w = col_widths[j]
            rendered = header_font.render(h, True, self.accent_color)
            if j == 0:
                # Shift 'Weight' header left by 18 pixels
                rect = rendered.get_rect(center=(cell_x + cell_w//2 - 18, y + 35))
            else:
                rect = rendered.get_rect(center=(cell_x + cell_w//2, y + 35))
            self.screen.blit(rendered, rect)
        # Draw horizontal line under header
        pygame.draw.line(self.screen, self.accent_color, (start_x, y+70), (start_x+table_width, y+70), 5)
        # Draw vertical borders for columns
        for j in range(1, n_cols):
            x = start_x + sum(col_widths[:j])
            pygame.draw.line(self.screen, self.accent_color, (x, start_y), (x, start_y + n_rows*70), 4)
        # Draw attribute rows (centered)
        for i, attr in enumerate(attributes):
            y = start_y + (i+1)*70
            attr_label = ' '.join([w.capitalize() for w in attr.split()])
            row = [str(weights[i]), attr_label, str(values_a[i]), str(values_b[i])]
            for j, val in enumerate(row):
                cell_x = start_x + sum(col_widths[:j])
                cell_w = col_widths[j]
                rendered = cell_font.render(val, True, self.text_color)
                rect = rendered.get_rect(center=(cell_x + cell_w//2, y + 35))
                self.screen.blit(rendered, rect)
            # Draw horizontal line under each row
            pygame.draw.line(self.screen, (100,100,120), (start_x, y+70), (start_x+table_width, y+70), 3)
        pygame.display.flip()

    def show_feedback(self, message, color, title=None):
        """show feedback message on trial (right or wrong)"""
        self.draw_gradient(top_color=self.bg_color, bottom_color=(30,30,30))
        if title:
            self._add_title(title_name=title)
        rendered = self.font.render(message, True, color)
        rect = rendered.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
        self.screen.blit(rendered, rect)
        pygame.display.flip()

    def show_score(self, score, title=None):
        """the function show score on experiment on the screen"""
        self.draw_gradient(self.bg_color, (30,30,30))
        if title:
            self._add_title(title_name=title)
        text = f"Your score is: {score}"
        rendered = self.font.render(text, True, self.text_color)
        rect = rendered.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() - 100))
        self.screen.blit(rendered, rect)
        pygame.display.flip()

    def set_font(self, new_font):
        self.font = new_font

    def set_bg_color(self, bg_color):
        self.bg_color = bg_color

    def set_accent_color(self, accent_color):
        self.accent_color = accent_color

    def set_text_color(self, text_color):
        self.text_color = text_color


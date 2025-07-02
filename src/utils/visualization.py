import pygame
import pygame.freetype
from src.experiment.Enums import Consts

class Visualization:
    def show_demographics_form(self, screen, font, bg_color, accent_color):
        """
        Display a demographics input form and return a dict with 'name', 'age', 'gender'.
        """
        responses = [''] * len(Consts.FIELDS)
        current = 0
        running = True
        clock = pygame.time.Clock()

        while running:
            screen.fill(bg_color)
            self._add_title(screen=screen, accent_color=accent_color, title_name="Demographics")
            for i, field in enumerate(Consts.FIELDS):
                self._add_field(screen=screen, font=font, accent_color=accent_color, field=field, i=i, current=current,
                                responses=responses)
            self._add_instruction(screen=screen, font=font, accent_color=accent_color)
            pygame.display.flip()
            for event in pygame.event.get():
                current, running = self._deal_event(event=event, current=current, responses=responses)
            clock.tick(30)

        return dict(zip(['name', 'age', 'gender'], responses))

    @staticmethod
    def _deal_event(event, current, responses):
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

    @staticmethod
    def _add_instruction(screen, font, accent_color):
        instr = font.render('Press Enter to continue', True, accent_color)
        screen.blit(instr, (screen.get_width() // 2 - instr.get_width() // 2, 450))

    @staticmethod
    def _add_title(screen, accent_color, title_name):
        title_font = pygame.font.SysFont('Arial Rounded MT Bold', 44)
        title = title_font.render(title_name, True, accent_color)
        screen.blit(title, (screen.get_width() // 2 - title.get_width() // 2, 60))

    @staticmethod
    def _add_field(screen, font, accent_color, field, i, current, responses):
        label = font.render(field + ':', True, accent_color)
        screen.blit(label, (screen.get_width() // 2 - 200, 180 + i * 80))
        # Draw input box
        box_rect = pygame.Rect(screen.get_width() // 2 - 50, 175 + i * 80, 300, 50)
        pygame.draw.rect(screen, accent_color if i == current else (180, 180, 180), box_rect, 2, border_radius=10)
        input_text = font.render(responses[i], True, accent_color)
        screen.blit(input_text, (box_rect.x + 10, box_rect.y + 10))

    @staticmethod
    def draw_gradient(screen, top_color, bottom_color):
        """
        Draw a vertical gradient background from top_color to bottom_color.
        """
        height = screen.get_height()
        for y in range(height):
            ratio = y / height
            color = [int(top_color[i] * (1 - ratio) + bottom_color[i] * ratio) for i in range(3)]
            pygame.draw.line(screen, color, (0, y), (screen.get_width(), y))

    def show_instruction_screen(self, screen, text, font, color, background, title=None, accent_color=(255,255,0)):
        self.draw_gradient(screen, background, (30,30,30))
        if title:
            self._add_title(screen=screen, accent_color=accent_color, title_name=title)
        lines = text.split('\n')
        y_offset = screen.get_height() // 2 - (len(lines) * font.get_height()) // 2
        for i, line in enumerate(lines):
            rendered = font.render(line, True, color)
            rect = rendered.get_rect(center=(screen.get_width() // 2, y_offset + i * font.get_height()))
            screen.blit(rendered, rect)
        pygame.display.flip()

    def show_candidate_table(self, screen, attributes, weights, values_a, values_b, font, color, background, title=None, accent_color=(0,200,255)):
        """
        Display a large, visually clear candidate table with columns: Weight | Attribute | A | B, with weights listed vertically.
        The 'Weight' header cell is shifted slightly left for better spacing.
        """
        self.draw_gradient(screen, background, (30,30,30))
        if title:
            title_font = pygame.font.SysFont('Arial Rounded MT Bold', 64)
            title_surf = title_font.render(title, True, accent_color)
            screen.blit(title_surf, (screen.get_width()//2 - title_surf.get_width()//2, 40))
        # Table header
        header_font = pygame.font.SysFont('Arial Rounded MT Bold', 48)
        cell_font = pygame.font.SysFont('Arial Rounded MT Bold', 44)
        header = ['Weight', 'Attribute', 'A', 'B']
        col_widths = [140, 320, 120, 120]
        n_rows = len(attributes) + 1  # header + attribute rows
        n_cols = 4
        table_width = sum(col_widths)
        table_height = (n_rows + 1) * 70 + 40
        start_x = (screen.get_width() - table_width) // 2
        start_y = screen.get_height() // 2 - table_height // 2 + 40
        # Draw rounded rectangle background for table
        table_rect = pygame.Rect(start_x-30, start_y-30, table_width+60, table_height+60)
        pygame.draw.rect(screen, (40,40,60), table_rect, border_radius=28)
        # Draw header row (centered, but shift 'Weight' left)
        y = start_y
        for j, h in enumerate(header):
            cell_x = start_x + sum(col_widths[:j])
            cell_w = col_widths[j]
            rendered = header_font.render(h, True, accent_color)
            if j == 0:
                # Shift 'Weight' header left by 18 pixels
                rect = rendered.get_rect(center=(cell_x + cell_w//2 - 18, y + 35))
            else:
                rect = rendered.get_rect(center=(cell_x + cell_w//2, y + 35))
            screen.blit(rendered, rect)
        # Draw horizontal line under header
        pygame.draw.line(screen, accent_color, (start_x, y+70), (start_x+table_width, y+70), 5)
        # Draw vertical borders for columns
        for j in range(1, n_cols):
            x = start_x + sum(col_widths[:j])
            pygame.draw.line(screen, accent_color, (x, start_y), (x, start_y + (n_rows)*70), 4)
        # Draw attribute rows (centered)
        for i, attr in enumerate(attributes):
            y = start_y + (i+1)*70
            attr_label = ' '.join([w.capitalize() for w in attr.split()])
            row = [str(weights[i]), attr_label, str(values_a[i]), str(values_b[i])]
            for j, val in enumerate(row):
                cell_x = start_x + sum(col_widths[:j])
                cell_w = col_widths[j]
                rendered = cell_font.render(val, True, color)
                rect = rendered.get_rect(center=(cell_x + cell_w//2, y + 35))
                screen.blit(rendered, rect)
            # Draw horizontal line under each row
            pygame.draw.line(screen, (100,100,120), (start_x, y+70), (start_x+table_width, y+70), 3)
        pygame.display.flip()

    def show_feedback(self, screen, message, font, color, background, title=None, accent_color=(255,255,0)):
        self.draw_gradient(screen, background, (30,30,30))
        if title:
            title_font = pygame.font.SysFont('Arial Rounded MT Bold', 44)
            title_surf = title_font.render(title, True, accent_color)
            screen.blit(title_surf, (screen.get_width()//2 - title_surf.get_width()//2, 60))
        rendered = font.render(message, True, color)
        rect = rendered.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
        screen.blit(rendered, rect)
        pygame.display.flip()

    def show_score(self, screen, score, font, color, background, title=None, accent_color=(255,255,0)):
        self.draw_gradient(screen, background, (30,30,30))
        if title:
            title_font = pygame.font.SysFont('Arial Rounded MT Bold', 44)
            title_surf = title_font.render(title, True, accent_color)
            screen.blit(title_surf, (screen.get_width()//2 - title_surf.get_width()//2, 60))
        text = f"Your score is: {score}"
        rendered = font.render(text, True, color)
        rect = rendered.get_rect(center=(screen.get_width() // 2, screen.get_height() - 100))
        screen.blit(rendered, rect)
        pygame.display.flip()
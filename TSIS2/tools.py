"""
tools.py — Drawing tool implementations for the Paint application.
Each tool class exposes: on_mouse_down, on_mouse_move, on_mouse_up, draw_preview.
"""

import pygame
import math
from collections import deque


# ---------------------------------------------------------------------------
# Utility helpers
# ---------------------------------------------------------------------------

def draw_dashed_rect(surface, color, rect, dash=6):
    """Draw a dashed rectangle (used for selection previews)."""
    x, y, w, h = rect
    for i in range(0, w, dash * 2):
        pygame.draw.line(surface, color, (x + i, y), (min(x + i + dash, x + w), y))
        pygame.draw.line(surface, color, (x + i, y + h), (min(x + i + dash, x + w), y + h))
    for i in range(0, h, dash * 2):
        pygame.draw.line(surface, color, (x, y + i), (x, min(y + i + dash, y + h)))
        pygame.draw.line(surface, color, (x + w, y + i), (x + w, min(y + i + dash, y + h)))


# ---------------------------------------------------------------------------
# Pencil (freehand)
# ---------------------------------------------------------------------------

class PencilTool:
    name = "pencil"

    def __init__(self):
        self.drawing = False
        self.last_pos = None

    def on_mouse_down(self, canvas, pos, color, size):
        self.drawing = True
        self.last_pos = pos
        pygame.draw.circle(canvas, color, pos, max(1, size // 2))

    def on_mouse_move(self, canvas, pos, color, size):
        if self.drawing and self.last_pos:
            pygame.draw.line(canvas, color, self.last_pos, pos, size)
            self.last_pos = pos

    def on_mouse_up(self, canvas, pos, color, size):
        self.drawing = False
        self.last_pos = None

    def draw_preview(self, surface, pos, color, size):
        pygame.draw.circle(surface, color, pos, max(1, size // 2), 1)


# ---------------------------------------------------------------------------
# Straight Line
# ---------------------------------------------------------------------------

class LineTool:
    name = "line"

    def __init__(self):
        self.drawing = False
        self.start = None

    def on_mouse_down(self, canvas, pos, color, size):
        self.drawing = True
        self.start = pos

    def on_mouse_move(self, canvas, pos, color, size):
        pass  # Preview is drawn in draw_preview

    def on_mouse_up(self, canvas, pos, color, size):
        if self.drawing and self.start:
            pygame.draw.line(canvas, color, self.start, pos, size)
        self.drawing = False
        self.start = None

    def draw_preview(self, surface, pos, color, size):
        if self.drawing and self.start:
            pygame.draw.line(surface, color, self.start, pos, size)


# ---------------------------------------------------------------------------
# Rectangle
# ---------------------------------------------------------------------------

class RectangleTool:
    name = "rectangle"

    def __init__(self):
        self.drawing = False
        self.start = None

    def _make_rect(self, start, end):
        x = min(start[0], end[0])
        y = min(start[1], end[1])
        w = abs(end[0] - start[0])
        h = abs(end[1] - start[1])
        return pygame.Rect(x, y, w, h)

    def on_mouse_down(self, canvas, pos, color, size):
        self.drawing = True
        self.start = pos

    def on_mouse_move(self, canvas, pos, color, size):
        pass

    def on_mouse_up(self, canvas, pos, color, size):
        if self.drawing and self.start:
            rect = self._make_rect(self.start, pos)
            if rect.width > 0 and rect.height > 0:
                pygame.draw.rect(canvas, color, rect, size)
        self.drawing = False
        self.start = None

    def draw_preview(self, surface, pos, color, size):
        if self.drawing and self.start:
            rect = self._make_rect(self.start, pos)
            if rect.width > 0 and rect.height > 0:
                pygame.draw.rect(surface, color, rect, size)


# ---------------------------------------------------------------------------
# Square (constrained rectangle)
# ---------------------------------------------------------------------------

class SquareTool:
    name = "square"

    def __init__(self):
        self.drawing = False
        self.start = None

    def _make_rect(self, start, end):
        dx = end[0] - start[0]
        dy = end[1] - start[1]
        side = min(abs(dx), abs(dy))
        x = start[0] if dx >= 0 else start[0] - side
        y = start[1] if dy >= 0 else start[1] - side
        return pygame.Rect(x, y, side, side)

    def on_mouse_down(self, canvas, pos, color, size):
        self.drawing = True
        self.start = pos

    def on_mouse_move(self, canvas, pos, color, size):
        pass

    def on_mouse_up(self, canvas, pos, color, size):
        if self.drawing and self.start:
            rect = self._make_rect(self.start, pos)
            if rect.width > 0:
                pygame.draw.rect(canvas, color, rect, size)
        self.drawing = False
        self.start = None

    def draw_preview(self, surface, pos, color, size):
        if self.drawing and self.start:
            rect = self._make_rect(self.start, pos)
            if rect.width > 0:
                pygame.draw.rect(surface, color, rect, size)


# ---------------------------------------------------------------------------
# Circle / Ellipse
# ---------------------------------------------------------------------------

class CircleTool:
    name = "circle"

    def __init__(self):
        self.drawing = False
        self.start = None

    def _make_rect(self, start, end):
        x = min(start[0], end[0])
        y = min(start[1], end[1])
        w = abs(end[0] - start[0])
        h = abs(end[1] - start[1])
        return pygame.Rect(x, y, w, h)

    def on_mouse_down(self, canvas, pos, color, size):
        self.drawing = True
        self.start = pos

    def on_mouse_move(self, canvas, pos, color, size):
        pass

    def on_mouse_up(self, canvas, pos, color, size):
        if self.drawing and self.start:
            rect = self._make_rect(self.start, pos)
            if rect.width > 0 and rect.height > 0:
                pygame.draw.ellipse(canvas, color, rect, size)
        self.drawing = False
        self.start = None

    def draw_preview(self, surface, pos, color, size):
        if self.drawing and self.start:
            rect = self._make_rect(self.start, pos)
            if rect.width > 0 and rect.height > 0:
                pygame.draw.ellipse(surface, color, rect, size)


# ---------------------------------------------------------------------------
# Right Triangle
# ---------------------------------------------------------------------------

class RightTriangleTool:
    name = "right_triangle"

    def __init__(self):
        self.drawing = False
        self.start = None

    def _points(self, start, end):
        return [start, (start[0], end[1]), end]

    def on_mouse_down(self, canvas, pos, color, size):
        self.drawing = True
        self.start = pos

    def on_mouse_move(self, canvas, pos, color, size):
        pass

    def on_mouse_up(self, canvas, pos, color, size):
        if self.drawing and self.start:
            pts = self._points(self.start, pos)
            pygame.draw.polygon(canvas, color, pts, size)
        self.drawing = False
        self.start = None

    def draw_preview(self, surface, pos, color, size):
        if self.drawing and self.start:
            pts = self._points(self.start, pos)
            pygame.draw.polygon(surface, color, pts, size)


# ---------------------------------------------------------------------------
# Equilateral Triangle
# ---------------------------------------------------------------------------

class EquilateralTriangleTool:
    name = "equilateral_triangle"

    def __init__(self):
        self.drawing = False
        self.start = None

    def _points(self, start, end):
        cx = (start[0] + end[0]) / 2
        base = abs(end[0] - start[0])
        h = base * math.sqrt(3) / 2
        top_y = min(start[1], end[1])
        p1 = (start[0], top_y + h)
        p2 = (end[0], top_y + h)
        p3 = (cx, top_y)
        return [p1, p2, p3]

    def on_mouse_down(self, canvas, pos, color, size):
        self.drawing = True
        self.start = pos

    def on_mouse_move(self, canvas, pos, color, size):
        pass

    def on_mouse_up(self, canvas, pos, color, size):
        if self.drawing and self.start:
            pts = self._points(self.start, pos)
            pygame.draw.polygon(canvas, color, pts, size)
        self.drawing = False
        self.start = None

    def draw_preview(self, surface, pos, color, size):
        if self.drawing and self.start:
            pts = self._points(self.start, pos)
            pygame.draw.polygon(surface, color, pts, size)


# ---------------------------------------------------------------------------
# Rhombus
# ---------------------------------------------------------------------------

class RhombusTool:
    name = "rhombus"

    def __init__(self):
        self.drawing = False
        self.start = None

    def _points(self, start, end):
        cx = (start[0] + end[0]) / 2
        cy = (start[1] + end[1]) / 2
        return [
            (cx, start[1]),
            (end[0], cy),
            (cx, end[1]),
            (start[0], cy),
        ]

    def on_mouse_down(self, canvas, pos, color, size):
        self.drawing = True
        self.start = pos

    def on_mouse_move(self, canvas, pos, color, size):
        pass

    def on_mouse_up(self, canvas, pos, color, size):
        if self.drawing and self.start:
            pts = self._points(self.start, pos)
            pygame.draw.polygon(canvas, color, pts, size)
        self.drawing = False
        self.start = None

    def draw_preview(self, surface, pos, color, size):
        if self.drawing and self.start:
            pts = self._points(self.start, pos)
            pygame.draw.polygon(surface, color, pts, size)


# ---------------------------------------------------------------------------
# Eraser
# ---------------------------------------------------------------------------

class EraserTool:
    name = "eraser"

    def __init__(self):
        self.drawing = False
        self.last_pos = None

    def on_mouse_down(self, canvas, pos, color, size):
        self.drawing = True
        self.last_pos = pos
        pygame.draw.circle(canvas, (255, 255, 255), pos, size * 2)

    def on_mouse_move(self, canvas, pos, color, size):
        if self.drawing and self.last_pos:
            pygame.draw.line(canvas, (255, 255, 255), self.last_pos, pos, size * 4)
            self.last_pos = pos

    def on_mouse_up(self, canvas, pos, color, size):
        self.drawing = False
        self.last_pos = None

    def draw_preview(self, surface, pos, color, size):
        r = size * 2
        pygame.draw.rect(surface, (180, 180, 180),
                         (pos[0] - r, pos[1] - r, r * 2, r * 2), 1)


# ---------------------------------------------------------------------------
# Flood Fill
# ---------------------------------------------------------------------------

class FillTool:
    name = "fill"

    def on_mouse_down(self, canvas, pos, color, size):
        self._flood_fill(canvas, pos, color)

    def on_mouse_move(self, canvas, pos, color, size):
        pass

    def on_mouse_up(self, canvas, pos, color, size):
        pass

    def draw_preview(self, surface, pos, color, size):
        # Draw a small bucket cursor indicator
        pygame.draw.circle(surface, color, pos, 6)
        pygame.draw.circle(surface, (0, 0, 0), pos, 6, 1)

    def _flood_fill(self, canvas, start, fill_color):
        """BFS flood fill using get_at / set_at."""
        w, h = canvas.get_size()
        sx, sy = int(start[0]), int(start[1])
        if not (0 <= sx < w and 0 <= sy < h):
            return

        target_color = canvas.get_at((sx, sy))[:3]
        fill_rgb = fill_color[:3] if len(fill_color) > 3 else fill_color

        if target_color == fill_rgb:
            return  # Already the same color, nothing to do

        visited = set()
        queue = deque()
        queue.append((sx, sy))
        visited.add((sx, sy))

        # Lock for faster pixel access
        canvas.lock()
        try:
            while queue:
                x, y = queue.popleft()
                if canvas.get_at((x, y))[:3] != target_color:
                    continue
                canvas.set_at((x, y), fill_rgb)
                for nx, ny in ((x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)):
                    if 0 <= nx < w and 0 <= ny < h and (nx, ny) not in visited:
                        visited.add((nx, ny))
                        queue.append((nx, ny))
        finally:
            canvas.unlock()


# ---------------------------------------------------------------------------
# Text Tool
# ---------------------------------------------------------------------------

class TextTool:
    name = "text"

    def __init__(self):
        self.active = False
        self.pos = None
        self.text = ""
        self.font = None
        self._init_font()
        self._cursor_visible = True
        self._cursor_timer = 0

    def _init_font(self):
        try:
            self.font = pygame.font.SysFont("Arial", 22)
        except Exception:
            self.font = pygame.font.Font(None, 28)

    def on_mouse_down(self, canvas, pos, color, size):
        # Clicking while active → confirm current text, start new
        if self.active and self.text:
            self._commit(canvas, color)
        self.active = True
        self.pos = pos
        self.text = ""

    def on_mouse_move(self, canvas, pos, color, size):
        pass

    def on_mouse_up(self, canvas, pos, color, size):
        pass

    def handle_key(self, event, canvas, color):
        """Return True if event was consumed."""
        if not self.active:
            return False
        if event.key == pygame.K_RETURN:
            self._commit(canvas, color)
            return True
        elif event.key == pygame.K_ESCAPE:
            self.active = False
            self.text = ""
            return True
        elif event.key == pygame.K_BACKSPACE:
            self.text = self.text[:-1]
            return True
        else:
            ch = event.unicode
            if ch and ch.isprintable():
                self.text += ch
            return True

    def _commit(self, canvas, color):
        if self.text and self.pos:
            surf = self.font.render(self.text, True, color)
            canvas.blit(surf, self.pos)
        self.active = False
        self.text = ""
        self.pos = None

    def draw_preview(self, surface, pos, color, size):
        if not self.active or not self.pos:
            return
        # Render current text
        display = self.text
        surf = self.font.render(display, True, color)
        surface.blit(surf, self.pos)
        # Blinking cursor
        tw = surf.get_width()
        cx = self.pos[0] + tw + 1
        cy = self.pos[1]
        ch = surf.get_height()
        pygame.draw.line(surface, color, (cx, cy), (cx, cy + ch), 2)

    def update(self, dt):
        self._cursor_timer += dt
        if self._cursor_timer > 500:
            self._cursor_visible = not self._cursor_visible
            self._cursor_timer = 0


# ---------------------------------------------------------------------------
# Color Picker (eyedropper) — samples from the canvas
# ---------------------------------------------------------------------------

class ColorPickerTool:
    name = "color_picker"
    picked_color = None

    def on_mouse_down(self, canvas, pos, color, size):
        x, y = int(pos[0]), int(pos[1])
        w, h = canvas.get_size()
        if 0 <= x < w and 0 <= y < h:
            ColorPickerTool.picked_color = canvas.get_at((x, y))[:3]

    def on_mouse_move(self, canvas, pos, color, size):
        pass

    def on_mouse_up(self, canvas, pos, color, size):
        pass

    def draw_preview(self, surface, pos, color, size):
        pygame.draw.circle(surface, (0, 0, 0), pos, 8, 2)
        pygame.draw.circle(surface, (255, 255, 255), pos, 6, 1)

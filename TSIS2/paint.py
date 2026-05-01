"""
paint.py — Extended Paint Application (TSIS 2)
Extends Practice 10–11 with: pencil, line, flood-fill, text, brush sizes, Ctrl+S save.

Controls
--------
Tools (toolbar buttons or keyboard):
  P  — Pencil          L  — Line
  R  — Rectangle       C  — Circle
  S  — Square          T  — Right Triangle
  E  — Equilateral Tri H  — Rhombus
  F  — Fill (bucket)   X  — Text
  K  — Color Picker    D  — Eraser

Brush size:
  1  — Small (2 px)    2  — Medium (5 px)    3  — Large (10 px)

Other:
  Ctrl+S — Save canvas as timestamped PNG
  Escape — Cancel text input
"""

import sys
import pygame
from datetime import datetime
pygame.init()
pygame.font.init()
from tools import (
    PencilTool, LineTool, RectangleTool, SquareTool,
    CircleTool, RightTriangleTool, EquilateralTriangleTool,
    RhombusTool, EraserTool, FillTool, TextTool, ColorPickerTool,
)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------

WINDOW_W, WINDOW_H = 1200, 750
TOOLBAR_W = 200          # left panel width
CANVAS_X = TOOLBAR_W
CANVAS_W = WINDOW_W - TOOLBAR_W
CANVAS_H = WINDOW_H

BRUSH_SIZES = {1: 2, 2: 5, 3: 10}

BG_COLOR       = (245, 245, 247)
PANEL_COLOR    = (30,  30,  35)
PANEL_ACCENT   = (55,  55,  62)
BUTTON_COLOR   = (60,  60,  68)
BUTTON_ACTIVE  = (99,  132, 227)
BUTTON_HOVER   = (80,  80,  90)
TEXT_COLOR     = (230, 230, 235)
TEXT_DIM       = (140, 140, 150)
SWATCH_BORDER  = (200, 200, 200)
CANVAS_COLOR   = (255, 255, 255)

PALETTE = [
    (0,   0,   0),   (255, 255, 255), (192, 192, 192), (128, 128, 128),
    (255, 0,   0),   (180, 0,   0),   (255, 128, 0),   (255, 200, 0),
    (0,   200, 0),   (0,  100,  0),   (0,   200, 200), (0,   0,   200),
    (100, 0,   200), (200, 0,   200), (255, 150, 200), (139, 90,  43),
]

TOOLS = [
    ("Pencil",    "P", PencilTool()),
    ("Line",      "L", LineTool()),
    ("Rectangle", "R", RectangleTool()),
    ("Circle",    "C", CircleTool()),
    ("Square",    "S", SquareTool()),
    ("R-Tri",     "T", RightTriangleTool()),
    ("Eq-Tri",    "E", EquilateralTriangleTool()),
    ("Rhombus",   "H", RhombusTool()),
    ("Fill",      "F", FillTool()),
    ("Text",      "X", TextTool()),
    ("Eyedrop",   "K", ColorPickerTool()),
    ("Eraser",    "D", EraserTool()),
]

KEY_MAP = {
    pygame.K_p: "Pencil",    pygame.K_l: "Line",
    pygame.K_r: "Rectangle", pygame.K_c: "Circle",
    pygame.K_s: "Square",    pygame.K_t: "R-Tri",
    pygame.K_e: "Eq-Tri",    pygame.K_h: "Rhombus",
    pygame.K_f: "Fill",      pygame.K_x: "Text",
    pygame.K_k: "Eyedrop",   pygame.K_d: "Eraser",
}


# ---------------------------------------------------------------------------
# Toolbar renderer
# ---------------------------------------------------------------------------

class Toolbar:
    BTN_H   = 36
    BTN_GAP = 4
    MARGIN  = 10

    def __init__(self, font_sm, font_xs):
        self.font_sm = font_sm
        self.font_xs = font_xs
        # Build button rects for tools (2-column grid)
        self.tool_rects = {}   # label → Rect
        self.size_rects = {}   # size_key → Rect
        self.swatch_rects = [] # (color, Rect)
        self._build(TOOLS)

    def _build(self, tools):
        m = self.MARGIN
        col_w = (TOOLBAR_W - m * 2 - self.BTN_GAP) // 2
        y = 52  # below title
        for i, (label, key, _tool) in enumerate(tools):
            col = i % 2
            x = m + col * (col_w + self.BTN_GAP)
            if col == 0 and i > 0:
                y += self.BTN_H + self.BTN_GAP
            rect = pygame.Rect(x, y, col_w, self.BTN_H)
            self.tool_rects[label] = rect
        if len(tools) % 2 == 1:
            y += self.BTN_H + self.BTN_GAP
        else:
            y += self.BTN_H + self.BTN_GAP

        # Brush size buttons
        y += 14
        size_labels = {1: "S  1", 2: "M  2", 3: "L  3"}
        sw = (TOOLBAR_W - m * 2 - self.BTN_GAP * 2) // 3
        for i, (k, lbl) in enumerate(size_labels.items()):
            rect = pygame.Rect(m + i * (sw + self.BTN_GAP), y, sw, self.BTN_H)
            self.size_rects[k] = rect
        y += self.BTN_H + 18

        # Color swatches (4×4 grid)
        sw_size = (TOOLBAR_W - m * 2 - 3 * 4) // 4
        self.palette_y = y
        for row in range(4):
            for col in range(4):
                idx = row * 4 + col
                if idx >= len(PALETTE):
                    break
                rx = m + col * (sw_size + 4)
                ry = y + row * (sw_size + 4)
                self.swatch_rects.append((PALETTE[idx], pygame.Rect(rx, ry, sw_size, sw_size)))
        self.bottom_y = y + 4 * (sw_size + 4) + 14

    def draw(self, surface, active_tool_label, active_size, active_color, mouse_pos):
        # Panel background
        pygame.draw.rect(surface, PANEL_COLOR, (0, 0, TOOLBAR_W, WINDOW_H))
        pygame.draw.line(surface, PANEL_ACCENT, (TOOLBAR_W - 1, 0), (TOOLBAR_W - 1, WINDOW_H), 2)

        # Title
        title = self.font_sm.render("🎨 Paint", True, TEXT_COLOR)
        surface.blit(title, (self.MARGIN, 14))

        # Tool buttons
        for label, key, _tool in TOOLS:
            rect = self.tool_rects[label]
            hovered = rect.collidepoint(mouse_pos)
            active  = (label == active_tool_label)
            color = BUTTON_ACTIVE if active else (BUTTON_HOVER if hovered else BUTTON_COLOR)
            pygame.draw.rect(surface, color, rect, border_radius=6)
            txt = self.font_xs.render(f"{label} [{key}]", True, TEXT_COLOR)
            tw, th = txt.get_size()
            surface.blit(txt, (rect.x + (rect.w - tw) // 2, rect.y + (rect.h - th) // 2))

        # Brush size section
        size_label_surf = self.font_xs.render("BRUSH SIZE", True, TEXT_DIM)
        size_y = list(self.size_rects.values())[0].y - 14
        surface.blit(size_label_surf, (self.MARGIN, size_y - 2))
        size_names = {1: "S  1", 2: "M  2", 3: "L  3"}
        for k, rect in self.size_rects.items():
            hovered = rect.collidepoint(mouse_pos)
            active  = (k == active_size)
            color = BUTTON_ACTIVE if active else (BUTTON_HOVER if hovered else BUTTON_COLOR)
            pygame.draw.rect(surface, color, rect, border_radius=6)
            txt = self.font_xs.render(size_names[k], True, TEXT_COLOR)
            tw, th = txt.get_size()
            surface.blit(txt, (rect.x + (rect.w - tw) // 2, rect.y + (rect.h - th) // 2))

        # Color palette label
        pal_label = self.font_xs.render("PALETTE", True, TEXT_DIM)
        surface.blit(pal_label, (self.MARGIN, self.palette_y - 14))

        # Swatches
        for color, rect in self.swatch_rects:
            pygame.draw.rect(surface, color, rect, border_radius=3)
            if color == active_color:
                pygame.draw.rect(surface, (255, 255, 255), rect, 2, border_radius=3)
            elif rect.collidepoint(mouse_pos):
                pygame.draw.rect(surface, SWATCH_BORDER, rect, 1, border_radius=3)

        # Active color preview
        preview_y = self.bottom_y
        pygame.draw.rect(surface, TEXT_DIM,
                         (self.MARGIN - 1, preview_y - 1, TOOLBAR_W - self.MARGIN * 2 + 2, 30),
                         border_radius=6)
        pygame.draw.rect(surface, active_color,
                         (self.MARGIN, preview_y, TOOLBAR_W - self.MARGIN * 2, 28),
                         border_radius=5)

        # Ctrl+S hint
        hint = self.font_xs.render("Ctrl+S  →  Save PNG", True, TEXT_DIM)
        surface.blit(hint, (self.MARGIN, WINDOW_H - 30))

    def get_tool_at(self, pos):
        for label, _key, tool in TOOLS:
            if self.tool_rects[label].collidepoint(pos):
                return label, tool
        return None, None

    def get_size_at(self, pos):
        for k, rect in self.size_rects.items():
            if rect.collidepoint(pos):
                return k
        return None

    def get_color_at(self, pos):
        for color, rect in self.swatch_rects:
            if rect.collidepoint(pos):
                return color
        return None


# ---------------------------------------------------------------------------
# Save helper
# ---------------------------------------------------------------------------

def save_canvas(canvas):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"canvas_{ts}.png"
    pygame.image.save(canvas, filename)
    return filename


# ---------------------------------------------------------------------------
# Status bar
# ---------------------------------------------------------------------------

def draw_status(surface, font, tool_label, size_key, color, message, mouse_pos):
    bar_h = 24
    y = WINDOW_H - bar_h
    pygame.draw.rect(surface, (20, 20, 24), (CANVAS_X, y, CANVAS_W, bar_h))
    cx, cy = mouse_pos
    cx_canvas = cx - CANVAS_X
    parts = [
        f"Tool: {tool_label}",
        f"Size: {BRUSH_SIZES[size_key]}px",
        f"Pos: ({cx_canvas}, {cy})",
    ]
    if message:
        parts.append(f"✓ {message}")
    txt = "   |   ".join(parts)
    surf = font.render(txt, True, (160, 160, 170))
    surface.blit(surf, (CANVAS_X + 8, y + 4))

    # small color dot in status
    pygame.draw.circle(surface, color, (WINDOW_W - 20, y + bar_h // 2), 7)
    pygame.draw.circle(surface, (200, 200, 200), (WINDOW_W - 20, y + bar_h // 2), 7, 1)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_W, WINDOW_H))
    pygame.display.set_caption("Paint — TSIS 2  |  Ctrl+S to save")

    clock = pygame.time.Clock()

    # Fonts
    font_sm = pygame.font.SysFont("Segoe UI", 16, bold=True)
    font_xs = pygame.font.SysFont("Segoe UI", 12)
    font_status = pygame.font.SysFont("Consolas", 11)

    # Canvas surface (no status bar baked in)
    STATUS_H = 24
    canvas = pygame.Surface((CANVAS_W, CANVAS_H - STATUS_H))
    canvas.fill(CANVAS_COLOR)

    toolbar = Toolbar(font_sm, font_xs)

    # State
    active_tool_label = "Pencil"
    active_tool = TOOLS[0][2]  # PencilTool instance
    active_size_key = 2        # medium by default
    active_color = (0, 0, 0)
    save_message = ""
    save_timer = 0

    # Text tool reference for key handling
    text_tool = next(t for _, _, t in TOOLS if isinstance(t, TextTool))

    running = True
    while running:
        dt = clock.tick(60)
        mouse_pos = pygame.mouse.get_pos()

        # Canvas-relative mouse pos (clipped to canvas area, above status bar)
        canvas_mouse = (
            max(0, min(mouse_pos[0] - CANVAS_X, CANVAS_W - 1)),
            max(0, min(mouse_pos[1], CANVAS_H - STATUS_H - 1)),
        )
        on_canvas = mouse_pos[0] >= CANVAS_X and mouse_pos[1] < CANVAS_H - STATUS_H
        brush_size = BRUSH_SIZES[active_size_key]

        # Save message timer
        if save_message:
            save_timer += dt
            if save_timer > 3000:
                save_message = ""
                save_timer = 0

        # Text tool cursor blink
        text_tool.update(dt)

        # ── Events ──────────────────────────────────────────────────────────
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # ── Key Down ────────────────────────────────────────────────────
            elif event.type == pygame.KEYDOWN:
                # Let text tool eat keys first when active
                if text_tool.active:
                    consumed = text_tool.handle_key(event, canvas, active_color)
                    if consumed:
                        continue

                mods = pygame.key.get_mods()

                # Ctrl+S → save
                if event.key == pygame.K_s and (mods & pygame.KMOD_CTRL):
                    fname = save_canvas(canvas)
                    save_message = f"Saved {fname}"
                    save_timer = 0
                    continue

                # Tool shortcuts
                if event.key in KEY_MAP:
                    label = KEY_MAP[event.key]
                    active_tool_label = label
                    active_tool = next(t for lbl, _, t in TOOLS if lbl == label)

                # Brush size shortcuts
                if event.key == pygame.K_1:
                    active_size_key = 1
                elif event.key == pygame.K_2:
                    active_size_key = 2
                elif event.key == pygame.K_3:
                    active_size_key = 3

            # ── Mouse Down ──────────────────────────────────────────────────
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = mouse_pos

                if pos[0] < TOOLBAR_W:
                    # Toolbar click
                    label, tool = toolbar.get_tool_at(pos)
                    if tool:
                        active_tool_label = label
                        active_tool = tool
                        # Confirm any text in progress if switching away
                        if active_tool_label != "Text" and text_tool.active:
                            text_tool.handle_key(
                                type("E", (), {"key": pygame.K_RETURN, "unicode": ""})(),
                                canvas, active_color,
                            )
                    sk = toolbar.get_size_at(pos)
                    if sk:
                        active_size_key = sk
                    col = toolbar.get_color_at(pos)
                    if col:
                        active_color = col
                else:
                    if on_canvas:
                        active_tool.on_mouse_down(canvas, canvas_mouse, active_color, brush_size)
                        # Check if eyedropper picked a color
                        if isinstance(active_tool, ColorPickerTool) and ColorPickerTool.picked_color:
                            active_color = ColorPickerTool.picked_color
                            ColorPickerTool.picked_color = None

            # ── Mouse Up ────────────────────────────────────────────────────
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if on_canvas:
                    active_tool.on_mouse_up(canvas, canvas_mouse, active_color, brush_size)

            # ── Mouse Move ──────────────────────────────────────────────────
            elif event.type == pygame.MOUSEMOTION:
                if on_canvas and pygame.mouse.get_pressed()[0]:
                    active_tool.on_mouse_move(canvas, canvas_mouse, active_color, brush_size)

        # ── Draw ─────────────────────────────────────────────────────────────
        screen.fill(BG_COLOR)

        # Blit canvas
        screen.blit(canvas, (CANVAS_X, 0))

        # Preview layer (live shape ghost / cursor indicator)
        preview = canvas.copy()
        if on_canvas:
            active_tool.draw_preview(preview, canvas_mouse, active_color, brush_size)
        screen.blit(preview, (CANVAS_X, 0))

        # Toolbar
        toolbar.draw(screen, active_tool_label, active_size_key, active_color, mouse_pos)

        # Status bar
        draw_status(screen, font_status, active_tool_label, active_size_key,
                    active_color, save_message, mouse_pos)

        # Custom cursor — hide on canvas for some tools
        if on_canvas and active_tool_label in ("Pencil", "Eraser", "Fill", "Text", "Eyedrop"):
            pygame.mouse.set_visible(False)
        else:
            pygame.mouse.set_visible(True)

        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

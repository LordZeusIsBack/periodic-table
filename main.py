import pygame as pg
from ast import literal_eval
import sys
import math
import chemistry_constants
from ai_model import AIModel, ChatSession

pg.init()

BACKGROUND = (44, 44, 47)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 100, 100)
ELEMENT_FONT_COLOR = (82, 87, 93)
HEIGHT, WIDTH = 720, 1280
screen = pg.display.set_mode((WIDTH, HEIGHT))
CELL_SIZE = 53
GRID_PADDING = 4
TABLE_OFFSET_X = 80

gen_font = pg.font.Font(None, 29)
large_font = pg.font.Font(None, 36)
bold_font = pg.font.Font(None, 33)
bold_font.set_bold(True)

element_font = pg.font.Font("font/Brownist.otf", 28)

popup_font = pg.font.Font(None, 46)

response = None


def draw_element(element, x, y, angle=0):
    if angle == 0:
        if element and element in chemistry_constants.ELEMENTS:
            rect = pg.Rect(x, y, CELL_SIZE, CELL_SIZE)
            pg.draw.rect(screen, chemistry_constants.ELEMENTS[element]["color"], rect)
            pg.draw.rect(screen, BLACK, rect, 1)
            symbol = element_font.render(element, True, ELEMENT_FONT_COLOR)
            symbol_rect = symbol.get_rect(
                center=(x + CELL_SIZE // 2, y + CELL_SIZE // 2)
            )
            screen.blit(symbol, symbol_rect)


def draw_periodic_table():
    for row, elements in enumerate(chemistry_constants.PERIODIC_TABLE_LAYOUT):
        for column, element in enumerate(elements):
            x = column * (CELL_SIZE + GRID_PADDING) + GRID_PADDING + TABLE_OFFSET_X
            y = row * (CELL_SIZE + GRID_PADDING) + GRID_PADDING
            draw_element(element, x, y)


def draw_electron_shells(element, x, y, width, height):
    configuration = chemistry_constants.ELEMENTS[element]["shells"]
    center_x, center_y = x + width // 2, y + height // 2
    for i, electrons in enumerate(configuration):
        radius = (i + 1) * (min(width, height) // (2 * len(configuration)))
        pg.draw.circle(screen, WHITE, (center_x, center_y), radius, 1)
        angle_step = 360 / electrons
        for j in range(electrons):
            angle = math.radians(j * angle_step)
            ex, ey = (
                center_x + int(radius * math.cos(angle)),
                center_y + int(radius * math.sin(angle)),
            )
            pg.draw.circle(screen, WHITE, (ex, ey), 2)


def create_tooltip(element):
    info = chemistry_constants.ELEMENTS[element]
    tooltip_text = f'{info["name"]}'
    tooltip = gen_font.render(tooltip_text, True, (44, 44, 47), (229, 229, 229))
    return tooltip


def draw_tooltip(tooltip, pos):
    screen.blit(tooltip, (pos[0] + 15, pos[1] + 15))


def show_element_info(element):
    info = chemistry_constants.ELEMENTS[element]
    lines = [
        f'Name: {info["name"]}',
        f'Atomic Number: {info["atomic_number"]}',
        f'Mass: {info["mass"]}',
        f'Electronic Configuration: {info["electron_config"]}',
    ]
    return lines


def show_compound_info():
    global response
    try:
        lines = [
            f'Name: {response["Formula"]["name"]}',
            f'Formula: {response["Formula"]["elements"]}',
            f'Uses: {str(response["Formula"]["uses"])[1:-1]}',
            f"Properties: {(response['Formula']['properties'])}",
        ]
    except TypeError:
        return response
    else:
        return lines


def get_compound_info(lst_of_elements):
    global response
    ai_model = AIModel()
    chat_session = ChatSession(ai_model)
    try:
        response = chat_session.send_prompt(lst_of_elements)  # Directly pass the list, no string conversion
        print("Raw response received:", response)  # Debug print
    except (SyntaxError, TypeError) as e:
        print(f"Error parsing response: {str(e)}")
        pg.quit()
        sys.exit("Parsing Error - Exiting")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
        quit()
    else:
        return response


def show_popup(message, color):
    popup = popup_font.render(message, True, color)
    popup_rect = popup.get_rect(center=(WIDTH // 2, HEIGHT - 260))
    screen.blit(popup, popup_rect)
    pg.display.flip()
    pg.time.wait(1500)


def get_element_at_pos(pos):
    x, y = pos
    column, row = (
        (x - TABLE_OFFSET_X) // (CELL_SIZE + GRID_PADDING),
        y // (CELL_SIZE + GRID_PADDING),
    )
    if 0 <= column < len(
        chemistry_constants.PERIODIC_TABLE_LAYOUT[0]
    ) and 0 <= row < len(chemistry_constants.PERIODIC_TABLE_LAYOUT):
        return chemistry_constants.PERIODIC_TABLE_LAYOUT[row][column]
    return None


def main():
    global response

    pg.display.set_caption("Elemental combinator - Periodic Table")

    clock = pg.time.Clock()
    dragging, dragged_element, merge_area, info_area = False, None, [], []

    merge_area_rect = pg.Rect(WIDTH - 200, HEIGHT - 150, 180, 100)
    electron_shell_rect = pg.Rect(WIDTH - 200, HEIGHT - 260, 180, 100)
    merge_button = pg.Rect(WIDTH - 200, HEIGHT - 40, 180, 30)
    hover_element = None
    tooltip = None

    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
                sys.exit("Exit button clicked")
            elif event.type == pg.MOUSEBUTTONDOWN:
                if merge_button.collidepoint(event.pos):
                    get_compound_info(merge_area)
                    print(response)
                    if isinstance(response, dict):
                        show_popup(f"Created {response['Formula']['name']} "
                                   f"({response['Formula']['elements']})", WHITE)
                        info_area = show_compound_info()
                    else:
                        show_popup(response, RED)
                    merge_area.clear()
                else:
                    element = get_element_at_pos(event.pos)
                    if element in chemistry_constants.ELEMENTS:
                        dragging, dragged_element = True, element
                        info_area = show_element_info(element)
            elif event.type == pg.MOUSEBUTTONUP:
                if dragging:
                    dragging = False
                    if merge_area_rect.collidepoint(event.pos) and dragged_element:
                        merge_area.append(dragged_element)
                    else:
                        show_popup(
                            f"{chemistry_constants.ELEMENTS[dragged_element]['name']}",
                            WHITE,
                        )
                dragged_element = None
        screen.fill(BACKGROUND)
        draw_periodic_table()
        pg.draw.rect(screen, WHITE, merge_area_rect, 2)
        for i, element in enumerate(merge_area):
            draw_element(
                element, merge_area_rect.x + 10 + i * 40, merge_area_rect.y + 10
            )
        pg.draw.rect(screen, WHITE, electron_shell_rect, 2)
        if merge_area:
            draw_electron_shells(
                merge_area[-1],
                electron_shell_rect.x,
                electron_shell_rect.y,
                electron_shell_rect.width,
                electron_shell_rect.height,
            )
        pg.draw.rect(screen, WHITE, merge_button)
        merge_text = gen_font.render("Merge", True, BLACK)
        screen.blit(merge_text, (merge_button.x + 70, merge_button.y + 8))
        info_rect = pg.Rect(10, HEIGHT - 150, 300, 140)
        for i, line in enumerate(info_area):
            info_text = gen_font.render(line, True, WHITE)
            screen.blit(info_text, (info_rect.x, info_rect.y + i * 30))
        mouse_pos = pg.mouse.get_pos()
        hover_element = get_element_at_pos(mouse_pos)
        if hover_element and hover_element in chemistry_constants.ELEMENTS:
            tooltip = create_tooltip(hover_element)
        else:
            tooltip = None
        if tooltip:
            draw_tooltip(tooltip, mouse_pos)
        if dragging and dragged_element:
            x, y = pg.mouse.get_pos()
            draw_element(dragged_element, x - CELL_SIZE // 2, y - CELL_SIZE // 2)
        pg.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()

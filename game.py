import copsandrobbers
import fluidsynth
import time
import pyglet
from pyglet.window import key
from pyglet import clock

window_size = 500
window = pyglet.window.Window(window_size, window_size)
margin = 50
grid_size = 20
grid_spacing = (window_size-margin*2)/grid_size
cop_delay = 0.25

cop_stream = open("./Resources/CopBlue.png","rb")
cop_png = pyglet.image.load("./Resources/CopBlue.png",file = cop_stream)
cop0_sprite = pyglet.sprite.Sprite(cop_png)
cop1_sprite = pyglet.sprite.Sprite(cop_png)

robber_stream = open("./Resources/RobberRed.png","rb")
rob_png = pyglet.image.load("./Resources/RobberRed.png",file = robber_stream)
rob_sprite = pyglet.sprite.Sprite(rob_png)

cop0_sprite.x = margin - cop0_sprite.width / 2
cop0_sprite.y = margin - cop0_sprite.height / 2

cop1_sprite.x = margin + grid_spacing - cop1_sprite.width / 2
cop1_sprite.y = margin - cop1_sprite.width / 2

rob_sprite.x = window_size-margin - rob_sprite.width*1.5
rob_sprite.y = window_size-margin - rob_sprite.height*1.5

valid_keys = [key.LEFT, key.RIGHT, key.UP, key.DOWN, key.SPACE]

game_over = pyglet.text.Label(
    "Game Over",
    font_name="Comic Sans",
    font_size=36,
    x=window.width//2,
    y = window.height//2,
    anchor_x="center",
    anchor_y ="center"
    )

fs = fluidsynth.Synth()
fs.start()
sfid = fs.sfload("./synthgms.sf2")

horizontal = copsandrobbers.make_path(grid_size)
vertical = copsandrobbers.make_path(grid_size)

grid = copsandrobbers.product(horizontal,vertical)
game_state = copsandrobbers.GameState(grid_size, grid_size)
game_state.print_locations()

# drawing

def draw_grid():
    for edge in grid.get_edges():
        u = edge[0]
        v = edge[1]
        x1 = u[0] * grid_spacing + margin
        y1 = u[1] * grid_spacing + margin
        x2 = v[0] * grid_spacing + margin
        y2 = v[1] * grid_spacing + margin
        pyglet.graphics.draw(2, pyglet.gl.GL_LINES, ("v2i", (x1, y1, x2, y2)))

def set_sprite(sprite, x, y):
    sprite.x = x - sprite.width / 2
    sprite.y = y - sprite.height / 2

# moving players

def move_robber(symbol):
    if game_state.is_game_over():
        return False

    if symbol == key.LEFT:
        di = -1
        dj =  0
    elif symbol == key.RIGHT:
        di = 1
        dj = 0
    elif symbol == key.UP:
        di = 0
        dj = 1
    elif symbol == key.DOWN:
        di = 0
        dj = -1
    elif symbol == key.SPACE:
        di = 0
        dj = 0

    if not game_state.move_robber(di, dj):
        return False

    i = game_state.robber.i
    j = game_state.robber.j
    loc_i = i * grid_size + margin
    loc_j = j * grid_size + margin
    set_sprite(rob_sprite, loc_i, loc_j)
    midi_note = i + j + 60
    play_midi_note(0, 0, midi_note, 127)
    return True

def move_cop0(dt):
    game_state.move_cop0()
    cop0_i = game_state.cop0.i * grid_size + margin
    cop0_j = game_state.cop0.j * grid_size + margin
    set_sprite(cop0_sprite, cop0_i, cop0_j)
    midi_note1 = game_state.cop0.i + game_state.cop0.j + 60
    play_midi_note(11, 0, midi_note1, 127)

def move_cop1(dt):
    game_state.move_cop1()
    cop1_i = game_state.cop1.i * grid_size + margin
    cop1_j = game_state.cop1.j * grid_size + margin
    set_sprite(cop1_sprite, cop1_i, cop1_j)
    midi_note2 = game_state.cop1.i + game_state.cop1.j + 60
    play_midi_note(12, 0, midi_note2, 127)

# MIDI

def play_midi_note(instrument,channel,pitch,velocity):
    fs.program_select(0, sfid, 0, instrument)
    fs.noteon(channel, pitch, velocity)
    clock.schedule_once(note_off, 0.1, channel, pitch)


def note_off(dt, channel, pitch):
    fs.noteoff(channel, pitch)

# pyglet event handlers

@window.event
def on_key_press(symbol,modifiers):
    if symbol == key.Q:
        pyglet.app.exit()
    if symbol in valid_keys:
        if move_robber(symbol):
            clock.schedule_once(move_cop0, cop_delay)
            clock.schedule_once(move_cop1, cop_delay * 2)
            game_state.print_locations()

@window.event
def on_draw():
    window.clear()
    draw_grid()
    cop0_sprite.draw()
    cop1_sprite.draw()
    rob_sprite.draw()
    if game_state.is_game_over():
        game_over.draw()

pyglet.app.run()

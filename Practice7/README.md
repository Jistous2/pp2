# Practice 7 — Pygame Games

## Setup
```
pip install -r requirements.txt
```

## Projects

### Mickey's Clock
Displays current time using rotating hand graphics.
```
cd mickeys_clock
python main.py
```
Place a `mickey_hand.png` image in `mickeys_clock/images/` to use custom hands.

### Music Player
Keyboard-controlled music player.
```
cd music_player
python main.py
```
Add `.mp3` / `.wav` / `.ogg` files to `music_player/music/`.

| Key | Action |
|-----|--------|
| P | Play |
| S | Stop |
| N | Next track |
| B | Previous track |
| Q / Esc | Quit |

### Moving Ball
Arrow-key controlled red ball on white background.
```
cd moving_ball
python main.py
```
Ball moves 20 px per key press and cannot leave the screen.

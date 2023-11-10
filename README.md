# mystic-square
This project is a multi-agent mystic-square game solver. Each tile is autonomous and try to reach its final destination. Agents can:
- Move if the destination cell is empty (white)
- Request other tiles to move if they block them

<img src="assets/screenshot.png" alt="Project screenshot"/>

## Installation
This project uses [Nix](https://nixos.org/) with [flakes enabled](https://nixos.wiki/wiki/Flakes) as environment manager.

## Usage
Assuming you are at `mystic-square` root.

```bash
python src/main.py
```

## This project is part of my engineering school curriculum
[<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f8/CY_Tech.svg/320px-CY_Tech.svg.png" alt="CYTech logo"/>](https://cytech.cyu.fr/)
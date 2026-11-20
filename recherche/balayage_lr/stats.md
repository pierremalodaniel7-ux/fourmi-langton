# Statistiques du balayage LR (grille carrée, 1 fourmi, départ blanc)

Règles = mots primitifs, avec L et R, un représentant par paire L↔R (commence par L).

| q | règles | B | V (certifiées) | V? (non certifiées) | C | S | X | E |
|---|---|---|---|---|---|---|---|---|
| 2 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 |
| 3 | 3 | 0 | 1 | 0 | 2 | 0 | 0 | 0 |
| 4 | 6 | 0 | 2 | 0 | 2 | 2 | 0 | 0 |
| 5 | 15 | 0 | 1 | 0 | 4 | 0 | 10 | 0 |
| 6 | 27 | 0 | 3 | 0 | 6 | 6 | 12 | 0 |
| 7 | 63 | 0 | 11 | 0 | 16 | 0 | 36 | 0 |
| 8 | 120 | 0 | 16 | 3 | 24 | 12 | 65 | 0 |
| 9 | 252 | 0 | 31 | 3 | 52 | 0 | 166 | 0 |
| 10 | 495 | 0 | 58 | 0 | 67 | 30 | 340 | 0 |
| 11 | 1023 | 0 | 115 | 0 | 130 | 0 | 778 | 0 |
| 12 | 2010 | 0 | 216 | 0 | 240 | 54 | 1500 | 0 |
| 13 | 4095 | 0 | 436 | 0 | 465 | 0 | 3194 | 0 |
| 14 | 8127 | 0 | 847 | 1 | 752 | 126 | 6401 | 0 |
| 15 | 16365 | 0 | 1720 | 1 | 1538 | 0 | 13106 | 0 |
| 16 | 32640 | 0 | 3327 | 1 | 2869 | 240 | 26203 | 0 |
| total | 65242 | 0 | 6785 | 9 | 6167 | 470 | 51811 | 0 |

## Périodes d'autoroute (histogramme, classes log2)

- [16, 32) : 2038 ████████████████████████████████████████████████████████████
- [32, 64) : 1058 ███████████████████████████████
- [64, 128) : 1217 ███████████████████████████████████
- [128, 256) : 1453 ██████████████████████████████████████████
- [256, 512) : 593 █████████████████
- [512, 1024) : 263 ███████
- [1024, 2048) : 90 ██
- [2048, 4096) : 40 █
- [4096, 8192) : 22 █
- [8192, 16384) : 5 █
- [16384, 32768) : 5 █
- [32768, 65536) : 1 █

Périodes les plus fréquentes : 18 (2038), 52 (509), 88 (284), 38 (180), 42 (146), 168 (132), 104 (131), 46 (130), 68 (126), 100 (125), 108 (123), 152 (88), 196 (88), 116 (70), 128 (59)

## Records

- Plus longue période : LLLLLLLRRLLRLLL P=54280 D=(-32,32) début=253714 cert=1
- Plus longue période : LLLLLRRRRRRRLL P=28224 D=(-60,-60) début=1174492 cert=1
- Plus longue période : LRLRLRLRRRRRRRLR P=27528 D=(24,-78) début=1098998 cert=1
- Plus longue période : LLRLRLLLLRLRLRRL P=24444 D=(-66,-66) début=1506323 cert=1
- Plus longue période : LRLRLRLRRRRRRLLR P=19680 D=(-24,78) début=645516 cert=1
- Plus longue période : LLLLLLRRLRRRRRLL P=18996 D=(42,42) début=712769 cert=1
- Plus longue période : LLLLLLLRRRRRRRL P=12144 D=(-30,30) début=529259 cert=1
- Plus longue période : LLLRLRRLRLRRLLL P=11288 D=(28,-4) début=67079 cert=1
- Plus longue période : LLLRLRRLRLRRLLLL P=11020 D=(28,-4) début=225850 cert=1
- Plus longue période : LLRLRLRRRLLRRLRR P=8852 D=(36,-12) début=108718 cert=1
- Plus long transitoire (début) : LLRRLLR P=204 D=(-2,-2) début=80669024 cert=1
- Plus long transitoire (début) : LLRRRL P=896 D=(-4,4) début=64416367 cert=1
- Plus long transitoire (début) : LLRLRRLR P=1000 D=(6,6) début=57230891 cert=1
- Plus long transitoire (début) : LRLRLRRLR P=512 D=(-2,6) début=45835335 cert=1
- Plus long transitoire (début) : LLLRRLLR P=118 D=(-1,1) début=34895126 cert=1
- Plus long transitoire (début) : LRRLRLLLR P=578 D=(-5,5) début=14973490 cert=1
- Plus long transitoire (début) : LLLLLRRRL P=664 D=(-2,2) début=8744718 cert=1
- Plus long transitoire (début) : LRLRLRLRRRRRRLL P=3284 D=(0,-24) début=7152649 cert=1
- Plus long transitoire (début) : LLLRRRLLL P=488 D=(-2,2) début=6772882 cert=1
- Plus long transitoire (début) : LLRLRRL P=296 D=(2,-2) début=5024551 cert=1

Directions (pente réduite, à symétries près) : 1/1:6534, 1/3:121, 0/1:77, 3/5:12, 1/2:7, 2/3:6, 3/11:5, 5/7:4, 1/5:4, 7/11:3, 1/7:3, 3/7:2, 4/13:2, 9/11:2, 3/13:1, 7/9:1, 7/17:1

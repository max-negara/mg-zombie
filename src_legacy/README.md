# Zombie Pixel Shooter (Python)

Simplu demo în Python folosind Pygame. Jocul folosește o suprafață mică scalată pentru efect pixelat.

Cum rulezi:

1. Instalează Pygame:

```bash
python -m pip install -r requirements.txt
```

2. Rulează jocul:

```bash
python main.py
```

Controles:
- Click stânga: tragi
- S: aplecare (ține)
- U: cumpără armă nouă (cost 100 bani)
- C: schimbă skin (cost 1000 bani)

Reguli:
- Fiecare zombi omorât oferă 1 ban.
- Când ai 100 bani, se deblochează o armă mai puternică (SMG).
- Starea (bani, skin, armă) se salvează în `save.json`.
 - Poți cumpăra arma cu `U` (taie 100 bani din cont).
 - Poți schimba skinul cu `C` (costă 1000 bani și se deduc la cumpărare).

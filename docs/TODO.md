# Plan de Migrare: Zombie Pixel Shooter (Phaser 3)

Acest document detaliază pașii necesari pentru migrarea jocului din Python (Pygame) în tehnologii Web (Phaser 3 + ES6), conform specificațiilor din `project.md`.

## Faza 1: Configurare și Structură Proiect
- [x] **Configurare Mediu de Lucru**
    - [x] Creare structură foldere: `css/`, `assets/`, `js/` (cu subfoldere: `scenes/`, `entities/`, `utils/`).
    - [x] Creare `index.html` (container Canvas, import scripturi tip `module`).
    - [x] Creare `style.css` pentru centrarea canvas-ului și stil retro (fonturi pixel).
    - [x] Descărcare/Linkare bibliotecă Phaser 3 (CDN sau local).

- [x] **Arhitectură Modulară (ES6)**
    - [x] Configurare `main.js` (Configurarea jocului Phaser: dimensiuni, fizică Arcade, listă scene).
    - [x] Creare clasă de bază pentru scene.

## Faza 2: Sistemul de Scene
- [x] **BootScene (`js/scenes/BootScene.js`)**
    - [x] Inițializare setări globale.
- [x] **PreloaderScene (`js/scenes/PreloaderScene.js`)**
    - [x] Încărcare asset-uri (dacă există) sau pregătire resurse grafice generate.
    - [x] Implementare bară de încărcare (opțional).
- [x] **MainMenuScene (`js/scenes/MainMenuScene.js`)**
    - [x] Titlu joc.
    - [x] Buton "Start Game".
    - [x] Buton "Shop" / "Skins".
- [x] **GameScene (`js/scenes/GameScene.js`)**
    - [x] Setup buclă principală de joc.
    - [x] Inițializare sisteme (Input, Fizică, Manager Entități).

## Faza 3: Portare Grafică Procedurală (Renderer)
*Nota: Grafica este stil pixel-art procedural, nu sprite-uri statice.*
- [x] **Sistem de Randare (`js/utils/PixelRenderer.js`)**
    - [x] Implementare funcții helper pentru desenare dreptunghiuri "pixelate" folosind `Phaser.GameObjects.Graphics`.
    - [x] Portare logică scalare (pixel size).
- [x] **Definiții Skin-uri (`js/data/Skins.js`)**
    - [x] Extragere date culori și structură din codul Python vechi.
    - [x] Creare structură de date JSON/Object pentru toate skin-urile (Naruto, Mario, etc.).
- [x] **Vizualizare Jucător**
    - [x] Implementare metodă de desenare a caracterului în funcție de skin-ul curent și starea (idle, crouch, shoot).

## Faza 4: Gameplay Core - Jucător
- [x] **Clasa Player (`js/entities/Player.js`)**
    - [x] Extindere `Phaser.Physics.Arcade.Sprite` sau Container.
    - [x] Implementare mișcare (stânga/dreapta - Velocity) - suport WASD și Săgeți.
    - [x] Implementare salt (Jump) și gravitație.
    - [x] Implementare stare "Crouch" (S).
- [x] **Sistem de Arme (`js/entities/Weapon.js`)**
    - [x] Logică tragere (Mouse Click).
    - [x] Generare proiectile (`Bullet.js`).
    - [x] Mecanică Cooldown și Reload.

## Faza 5: Gameplay Core - Inamici
- [x] **Clasa Enemy (`js/entities/Enemy.js`)**
    - [x] Configurare fizică și coliziuni.
    - [x] Logică AI simplă (urmărire jucător).
    - [x] Sistem de viață și damage visual feedback.
- [x] **Enemy Spawner (`js/systems/WaveManager.js`)**
    - [x] Logică generare valuri de zombi.
    - [x] Creștere progresivă a dificultății.
    - [ ] Spawn Boss la 1000 zombi eliminați. (To be done in later refinement or optimization)

## Faza 6: Fizică și Coliziuni
- [ ] Configurare grupuri de coliziune Phaser (Player, Enemies, Bullets, Ground).
- [ ] Implementare `Collider`: Gloanțe vs Inamici (Kill logic).
- [ ] Implementare `Collider`: Inamici vs Player (Damage logic).
- [ ] Implementare limite hartă (World Bounds).

## Faza 7: UI și Economie
- [ ] **HUD (Heads-Up Display) (`js/ui/HUD.js`)**
    - [ ] Afișare viață (Health Bar).
    - [ ] Afișare bani (Coins counter).
    - [ ] Afișare muniție.
- [ ] **Sistem de Magazin (`js/ui/Shop.js`)**
    - [ ] Interfață cumpărare arme (Upgrade la SMG).
    - [ ] Interfață selector skin-uri.
    - [ ] Logică deblocare "Turn" (Tower) la 25000 bani.

## Faza 8: Persistența Datelor (Migrare save.json)
- [ ] **Storage Manager (`js/systems/Storage.js`)**
    - [ ] Implementare wrapper peste `window.localStorage`.
    - [ ] Funcție `saveGame(data)`: serializează starea (bani, skin-uri, arme).
    - [ ] Funcție `loadGame()`: deserializează și aplică starea la start.
    - [ ] Mapare câmpuri din vechiul `save.json` la noua structură.

## Faza 9: Optimizare și Polish
- [ ] Adăugare efecte de particule (sânge, explozii).
- [ ] Adăugare sunete (dacă există resurse).
- [ ] Testare performanță și ajustare Garbage Collection.

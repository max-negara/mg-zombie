# Documentație Proiect: Zombie Pixel Shooter

## 1. Descriere Platformă Actuală (Legacy)

Proiectul curent, situat în folderul `src_legacy`, este un joc de acțiune 2D implementat în **Python**, utilizând biblioteca **Pygame**.

### Caracteristici Principale:
*   **Gameplay**: Un "wave shooter" simplu în care jucătorul trebuie să supraviețuiască atacurilor zombilor.
*   **Grafică**: Stil pixel-art realizat prin randare la rezoluție mică și scalare.
*   **Controale**:
    *   `Mouse Stânga`: Trage.
    *   `S`: Aplecare (crouch).
    *   `U`: Cumpără armă nouă (SMG - 100 bani).
    *   `C`: Schimbă skin-ul (Cost 1000 bani).
*   **Economie**: Fiecare zombi eliminat oferă bani (coins), care pot fi folosiți în magazin.
*   **Sistem de Salvare**: Datele jucătorului (bani, skin curent, skin-uri deținute, arme deblocat, statistici) sunt persistate într-un fișier local `save.json`.
*   **Varietate**: Jocul include o logică extinsă de desenare a caracterului, suportând numeroase skin-uri inspirate din Anime, Jocuri și Filme (ex: Naruto, Mario, Spiderman).

### Structura Fișierelor (Python):
*   `main.py` / `main_fixed.py`: Punctul de intrare și logica principală a jocului (game loop, randare, logică entități).
*   `save.json`: Stocarea datelor persistente.

---

## 2. Obiectivul Migrării (Web)

Scopul acestui proiect este rescrierea completă a jocului folosind tehnologii web standard (**HTML5**, **CSS**, **JavaScript**), pentru a permite rularea sa direct într-un browser web.

### Specificații Noi:
*   **Tehnologie**:
    *   **Phaser 3 Framework**: Pentru gestionarea randării, fizică și logică (înlocuiește Pygame).
    *   **JavaScript (ES6+)**: Pentru logica jocului.
    *   **CSS**: Pentru stilizarea containerului jocului.
*   **Stocare**: Înlocuirea fișierului `save.json` cu **localStorage** din browser.
*   **Avantaje**:
    *   Nu necesită instalarea Python sau a dependențelor.
    *   Poate fi jucat pe orice dispozitiv cu un browser modern.
    *   Ușor de distribuit (ex: GitHub Pages).
    *   Dezvoltare accelerată datorită funcțiilor integrate în Phaser (Sprite-uri, Fizică Arcade, Scene).

### Plan de Acțiune:
1.  Configurarea proiectului Phaser (`index.html` și includerea librăriei).
2.  Structurarea jocului folosind **Scene** Phaser (Boot, Preloader, MainMenu, Game).
3.  Implementarea logicii de randare folosind `Phaser.GameObjects.Graphics` pentru stilul procedural pixel-art.
4.  Implementarea sistemului de input și fizică folosind Arcade Physics.
5.  Implementarea logicii de joc (spawning inamici, coliziuni, magazin).
6.  Migrarea sistemului de salvare pe `localStorage`.

---

## 3. Standarde de Dezvoltare și Best Practices

Pentru a asigura un cod mentenabil, scalabil și robust, noul proiect va respecta următoarele principii:

*   **Arhitectură Modulară (ES6 Modules)**:
    *   Codul nu va fi scris într-un singur fișier monolitic (ca în versiunea `legacy`).
    *   Se va folosi `import`/`export` pentru separarea responsabilităților (ex: `Player.js`, `Enemy.js`, `Renderer.js`, `GameLoop.js`).
*   **Separation of Concerns (SoC)**:
    *   Logica jocului (state, fizică) va fi decuplată de logica de randare (desenare pe Canvas).
    *   Input handling-ul va fi gestionat separat.
*   **Clean Code**:
    *   Nume de variabile și funcții descriptive (în Engleză).
    *   Funcții mici care fac un singur lucru.
    *   Evitarea "numerelor magice" prin folosirea de constante.
*   **Performance Optimization**:
    *   Utilizarea eficientă a `requestAnimationFrame`.
    *   Minimizarea alocărilor de memorie în bucla principală (Garbage Collection optimization).
*   **Code Style**:
    *   Indentare consistentă și comentarii explicative unde logica este complexă.

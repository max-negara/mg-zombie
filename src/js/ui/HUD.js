export class HUD {
    constructor(scene, maxHealth) {
        this.scene = scene;
        this.maxHealth = maxHealth;
        this.maxHearts = 5;
        this.scale = 3; // Scaling for pixel art

        // Container HUD - poziționat sus-stânga, dar cu o margine
        this.container = this.scene.add.container(20, 20);

        this.hearts = [];
        this.createHearts();
        this.createCoinDisplay();
    }

    createHearts() {
        for (let i = 0; i < this.maxHearts; i++) {
            const heart = this.scene.add.graphics();
            this.container.add(heart);
            this.hearts.push(heart);
            // Poziționăm fiecare inimioară
            heart.x = i * (9 * this.scale); // Spacing 
            this.drawHeart(heart, true); // Inițial pline
        }
    }

    drawHeart(graphics, filled) {
        graphics.clear();
        const color = filled ? 0xff0000 : 0x330000; // Roșu aprins vs Roșu închis (gol)
        graphics.fillStyle(color, 1);

        // Pixel Art Heart (7x6 matrix)
        const pixels = [
            '0110110',
            '1111111',
            '1111111',
            '0111110',
            '0011100',
            '0001000'
        ];

        for (let y = 0; y < pixels.length; y++) {
            for (let x = 0; x < pixels[y].length; x++) {
                if (pixels[y][x] === '1') {
                    graphics.fillRect(x * this.scale, y * this.scale, this.scale, this.scale);
                }
            }
        }
    }

    createCoinDisplay() {
        // Punem monedele la dreapta inimilor
        // Inimile ocupa aprox 135px (5 * 9 * 3). Lăsăm un spațiu și începem de la x=150
        const xOffset = 150; 
        const yOffset = 0; 
        
        // -- Coin Icon --
        const coin = this.scene.add.graphics();
        coin.fillStyle(0xffd700, 1);
        coin.lineStyle(2, 0xccaa00, 1);
        
        // Cerc simplu pentru monedă
        const radius = 8;
        // Desenam cercul centrat pe verticala inimilor (aprox 9px + padding)
        const centerY = (6 * this.scale) / 2; // = 9
        
        coin.fillCircle(xOffset + radius, centerY, radius);
        coin.strokeCircle(xOffset + radius, centerY, radius);
        
        // Simbol '$' sau doar luciu pe monedă
        coin.fillStyle(0xfff7cc, 1);
        coin.fillRect(xOffset + radius - 2, centerY - 4, 4, 8); // dungă verticală
        
        this.container.add(coin);

        // -- Coin Text --
        this.coinText = this.scene.add.text(xOffset + 25, yOffset - 4, '0', {
            fontFamily: '"Courier New", Courier, monospace',
            fontSize: '24px',
            fill: '#ffd700',
            stroke: '#000',
            strokeThickness: 2
        });
        
        this.container.add(this.coinText);
    }

    updateHealth(currentHealth) {
        // Calculăm câte inimi sunt pline
        // 100 health / 5 hearts = 20 health per heart
        const percentage = Math.max(0, currentHealth) / this.maxHealth;
        const heartsFilled = Math.ceil(percentage * this.maxHearts);

        for (let i = 0; i < this.maxHearts; i++) {
            // Dacă indexul curent e mai mic decât numărul de inimi pline, desenăm plin
            const isFull = i < heartsFilled;
            this.drawHeart(this.hearts[i], isFull);
        }
    }

    updateCoins(amount) {
        this.coinText.setText(amount.toString());
    }
}

import { PixelRenderer } from '../utils/PixelRenderer.js';
import { Weapon } from './Weapon.js';

export class Player extends Phaser.GameObjects.Container {
    constructor(scene, x, y, skin = 'default') {
        super(scene, x, y);
        this.scene = scene;
        this.skin = skin;

        // --- Physics Setup ---
        this.scene.physics.world.enable(this);
        this.body.setGravityY(600);
        this.body.setCollideWorldBounds(true);
        // Dimensiunile fizice ajustate (mai mici decat grafica pentru a evita blocaje)
        this.body.setSize(12, 16); 
        this.body.setOffset(-6, -8); // Centrare body pe container (0,0 e centrul containerului)

        // --- Graphics ---
        // Player-ul este desenat procedural
        this.graphics = this.scene.add.graphics();
        this.add(this.graphics);
        
        // --- Properties ---
        this.speed = 160;
        this.jumpForce = -350;
        this.facing = 1; // 1 = right, -1 = left
        this.isCrouching = false;
        this.isInvulnerable = false;
        
        // --- Systems ---
        this.weapon = new Weapon(this.scene, this);
        
        // --- Input Keys ---
        this.cursors = this.scene.input.keyboard.createCursorKeys();
        this.keyW = this.scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.W);
        this.keyA = this.scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.A);
        this.keyS = this.scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.S);
        this.keyD = this.scene.input.keyboard.addKey(Phaser.Input.Keyboard.KeyCodes.D);

        this.scene.add.existing(this);
    }

    takeHit() {
        if (this.isInvulnerable) return false;

        this.isInvulnerable = true;
        this.alpha = 0.5;
        
        // Invulnerability timer (1 second)
        this.scene.time.delayedCall(1000, () => {
            if (this.active) {
                this.isInvulnerable = false;
                this.alpha = 1;
            }
        });
        
        return true;
    }

    update() {
        const body = this.body;
        
        // --- Movement ---
        if (this.cursors.left.isDown || this.keyA.isDown) {
            body.setVelocityX(-this.speed);
            this.facing = -1;
        } else if (this.cursors.right.isDown || this.keyD.isDown) {
            body.setVelocityX(this.speed);
            this.facing = 1;
        } else {
            body.setVelocityX(0);
        }

        // --- Jump ---
        if ((this.cursors.up.isDown || this.keyW.isDown) && body.touching.down) {
            body.setVelocityY(this.jumpForce);
        }

        // --- Crouch ---
        // Simplu: doar schimbăm bounding box-ul sau viteza dacă vrem
        // Momentan doar flag vizual
        this.isCrouching = (this.cursors.down.isDown || this.keyS.isDown) && body.touching.down;

        // --- Shooting ---
        if (this.scene.input.activePointer.isDown) {
            this.weapon.fire();
        }

        // --- Redraw ---
        // Redesenăm în fiecare frame pentru a răspunde la facing și skin
        this.draw();
        
        // --- Boundary Check ---
        if (this.y > this.scene.physics.world.bounds.height) {
            this.setPosition(100, 100);
            body.setVelocity(0,0);
        }
    }

    draw() {
        this.graphics.clear();
        
        // Ajustare înălțime vizuală pentru crouch
        let yOffset = -8; // Desenăm relativ la centrul containerului (care e la picioare +/-)
        // În logică: Container (x,y) este poziția fizică. 
        // Vrem ca desenul să fie centrat pe body. 
        // Body size 12x16. 
        // Desenăm de la x-6, y-8 relative to center?
        // PixelRenderer.drawPlayer desenează un dreptunghi w,h la x,y.
        
        // Dacă pixel renderer desenează de la colț stânga-sus:
        // x = -6 (jumătate din w=12)
        // y = -8 (jumătate din h=16)
        
        let drawY = -8;
        let drawH = 16;
        
        if (this.isCrouching) {
            drawY = -4;
            drawH = 12; // Arată mai scund
            // Aici ar trebui o logică de desenare crouch specifică, dar folosim scalare simplă
        }

        PixelRenderer.drawPlayer(
            this.graphics, 
            -6,     // x (local)
            drawY,  // y (local)
            12,     // w
            drawH,  // h
            this.facing, 
            this.skin
        );

        // Draw Weapon
        PixelRenderer.drawWeapon(
            this.graphics,
            -6,
            drawY,
            12,
            drawH,
            this.facing
        );
    }
}

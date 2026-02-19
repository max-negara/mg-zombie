import { PixelRenderer } from '../utils/PixelRenderer.js';

export class Enemy extends Phaser.GameObjects.Container {
    constructor(scene, x, y, player) {
        super(scene, x, y);
        this.scene = scene;
        this.player = player;

        // --- Physics Setup ---
        this.scene.physics.world.enable(this);
        this.body.setGravityY(600);
        this.body.setCollideWorldBounds(true);
        this.body.setSize(12, 16);
        this.body.setOffset(-6, -8);

        // --- Graphics ---
        this.graphics = this.scene.add.graphics();
        this.add(this.graphics);

        // --- Properties ---
        this.speed = 40 + Math.random() * 40; // Random speed
        this.health = 50;
        this.damage = 10;
        this.skin = 'zombie';
        this.facing = 1;

        this.scene.add.existing(this);
    }

    update(time, delta) {
        if (!this.active) return;
        
        // --- AI: Follow Player ---
        if (this.player && this.player.active) {
            if (this.x < this.player.x - 10) {
                this.body.setVelocityX(this.speed);
                this.facing = 1;
            } else if (this.x > this.player.x + 10) {
                this.body.setVelocityX(-this.speed);
                this.facing = -1;
            } else {
                this.body.setVelocityX(0);
            }
        }

        // --- Simple Jump over obstacles (optional, simple logic) ---
        // If blocked, jump
        if (this.body.blocked.left || this.body.blocked.right) {
             if (this.body.touching.down) {
                 this.body.setVelocityY(-250);
             }
        }
        
        this.draw();
        
        // Fall off world check
        if (this.y > this.scene.physics.world.bounds.height + 100) {
            this.destroy();
        }
    }

    takeDamage(amount) {
        this.health -= amount;
        
        // Visual feedback (flash red)
        this.graphics.alpha = 0.5;
        this.scene.time.delayedCall(100, () => {
             if (this.active) this.graphics.alpha = 1;
        });

        if (this.health <= 0) {
            this.die();
        }
    }

    die() {
        // Maybe spawn particles or loot here
        this.destroy();
    }

    draw() {
        this.graphics.clear();
        PixelRenderer.drawPlayer(
            this.graphics, 
            -6, -8, 
            12, 16, 
            this.facing, 
            this.skin
        );
    }
}

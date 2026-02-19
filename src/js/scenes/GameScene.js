import { BaseScene } from './BaseScene.js';
import { HUD } from '../ui/HUD.js';
import { Player } from '../entities/Player.js';
import { WaveManager } from '../systems/WaveManager.js';

export class GameScene extends BaseScene {
    constructor() {
        super('GameScene');
        this.playerHealth = 100;
        this.playerCoins = 0;
    }

    create() {
        console.log('GameScene: Created');
        
        // --- World Bounds ---
        this.physics.world.setBounds(0, 0, 1280, 720);
        
        // Setup background
        this.cameras.main.setBackgroundColor('#4488aa'); 
        this.cameras.main.setBounds(0, 0, 1280, 720);

        // --- Ground ---
        const mapW = 1280;
        const groundH = 40;
        const groundY = 360 - groundH; // 360 este înălțimea logică a jocului (640x360 config)

        const ground = this.add.rectangle(0, groundY, mapW, groundH, 0x333333).setOrigin(0, 0);
        this.physics.add.existing(ground, true); // true = static body
        this.ground = ground;

        // --- Player ---
        this.player = new Player(this, 100, groundY - 50, 'goku'); // Testăm cu skin Goku
        
        // Camera Follow
        this.cameras.main.startFollow(this.player, true, 0.1, 0.1);

        // Colliders
        this.physics.add.collider(this.player, this.ground);

        // --- Waves & Enemies ---
        this.waveManager = new WaveManager(this, this.player, this.ground);

        // --- Collisions ---
        // 1. Bullets vs Enemies
        this.physics.add.overlap(this.player.weapon.bullets, this.waveManager.enemies, (bullet, enemy) => {
            if (bullet.active && enemy.active) {
                bullet.destroy();
                // Verificăm dacă inamicul poate primi damage
                if (typeof enemy.takeDamage === 'function') {
                    enemy.takeDamage(this.player.weapon.damage);
                    if (!enemy.active) {
                        this.addCoins(10);
                    }
                }
            }
        });

        // 2. Enemies vs Player
        this.physics.add.overlap(this.player, this.waveManager.enemies, (player, enemy) => {
            if (enemy.active && player.active) {
                // Încercăm să aplicăm lovitura (verifică invulnerabilitatea)
                if (player.takeHit()) {
                    this.damagePlayer(10);
                    
                    // Knockback logic
                    const force = 300;
                    if (player.x < enemy.x) {
                        player.body.setVelocityX(-force);
                    } else {
                        player.body.setVelocityX(force);
                    }
                }
            }
        });

        // --- UI / HUD ---
        this.hud = new HUD(this, 100);
        this.hud.updateHealth(this.playerHealth);
        this.hud.updateCoins(this.playerCoins);
        this.hud.container.setScrollFactor(0);

        // Wave Info Text
        this.waveText = this.add.text(this.cameras.main.width/2, 20, 'Wave 1', {
            fontSize: '20px',
            fill: '#fff',
            fontFamily: '"Courier New", Courier, monospace',
            stroke: '#000',
            strokeThickness: 3
        }).setOrigin(0.5).setScrollFactor(0);
        
        const info = this.add.text(this.cameras.main.width/2, 50, 'WASD/Arrows to Move. CLICK to Shoot.\nPhase 5: Gameplay Enemies', {
            fontSize: '16px',
            fill: '#000',
            align: 'center'
        }).setOrigin(0.5).setScrollFactor(0);

        // Input ESC
        this.input.keyboard.on('keydown-ESC', () => {
             this.scene.start('MainMenuScene');
        });

        // Start waves
        this.waveManager.start();
    }

    update(time, delta) {
        if (this.player) {
            this.player.update(time, delta);
        }
        if (this.waveManager) {
            this.waveManager.update(time, delta);
        }
    }

    updateWaveText(waveNum) {
        if (this.waveText) this.waveText.setText('Wave ' + waveNum);
    }

    addCoins(amount) {
        this.playerCoins += amount;
        this.hud.updateCoins(this.playerCoins);
    }

    damagePlayer(amount) {
        this.playerHealth -= amount;
        this.hud.updateHealth(this.playerHealth);
        this.cameras.main.flash(100, 255, 0, 0);

        if (this.playerHealth <= 0) {
            this.scene.restart();
        }
    }
}

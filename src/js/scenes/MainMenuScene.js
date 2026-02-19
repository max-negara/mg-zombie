import { BaseScene } from './BaseScene.js';

export class MainMenuScene extends BaseScene {
    constructor() {
        super('MainMenuScene');
    }

    create() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;

        // --- Title ---
        const titleText = this.add.text(0, 0, 'ZOMBIE\nPIXEL SHOOTER', {
            fontFamily: '"Courier New", Courier, monospace',
            fontSize: '48px',
            fill: '#ff0000',
            align: 'center',
            stroke: '#000000',
            strokeThickness: 6
        }).setOrigin(0.5);
        this.centerObject(titleText, 0, -60);

        // --- Start Button ---
        const startBtn = this.createButton(0, 20, 'START GAME', () => {
            this.scene.start('GameScene');
        });

        // --- Shop Button ---
        const shopBtn = this.createButton(0, 80, 'SHOP (coming soon)', () => {
            console.log('Open Shop');
        });
        
        // Instructions
        const footerText = this.add.text(width/2, height - 20, 'v1.0.0 Web Edition', {
            fontSize: '18px',
            fill: '#666'
        }).setOrigin(0.5);
    }

    createButton(xOffset, yOffset, text, callback) {
        const btn = this.add.text(0, 0, text, {
            fontFamily: '"Courier New", Courier, monospace',
            fontSize: '32px',
            fill: '#ffffff'
        }).setOrigin(0.5).setInteractive();

        this.centerObject(btn, xOffset, yOffset);

        btn.on('pointerover', () => btn.setStyle({ fill: '#ff0' }));
        btn.on('pointerout', () => btn.setStyle({ fill: '#fff' }));
        btn.on('pointerdown', callback);
        
        return btn;
    }
}

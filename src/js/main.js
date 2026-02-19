import { BootScene } from './scenes/BootScene.js';
import { PreloaderScene } from './scenes/PreloaderScene.js';
import { MainMenuScene } from './scenes/MainMenuScene.js';
import { GameScene } from './scenes/GameScene.js';

const config = {
    type: Phaser.AUTO,
    width: 640,
    height: 360,
    zoom: 2, // 640x2 = 1280px width
    parent: 'game-container',
    pixelArt: true, // Critic pentru stilul retro
    roundPixels: true, // Ajută la prevenirea textului neclar
    physics: {
        default: 'arcade',
        arcade: {
            gravity: { y: 600 },
            debug: false
        }
    },
    scene: [
        BootScene,
        PreloaderScene,
        MainMenuScene,
        GameScene
    ]
};

const game = new Phaser.Game(config);

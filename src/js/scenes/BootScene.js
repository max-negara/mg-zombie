import { BaseScene } from './BaseScene.js';

export class BootScene extends BaseScene {
    constructor() {
        super('BootScene');
    }

    preload() {
        console.log('BootScene: Preload');
        // Aici se vor încărca asset-urile in Faza 2
    }

    create() {
        console.log('BootScene: Created');
        // Immediately start the Preloader
        this.scene.start('PreloaderScene');
    }
}

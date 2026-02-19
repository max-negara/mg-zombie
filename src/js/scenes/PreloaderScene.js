import { BaseScene } from './BaseScene.js';

export class PreloaderScene extends BaseScene {
    constructor() {
        super('PreloaderScene');
    }

    preload() {
        // Setup loading bar
        this.createLoadingBar();

        // Simulate loading assets (since we use procedural generation mostly)
        // Folosim un timer pentru a simula încărcarea și a vedea bara de progres
        
        let progress = 0;
        const totalSteps = 100;
        
        // Simulam incarcarea cu un timer repetitiv
        this.time.addEvent({
            delay: 20, // 20ms * 100 = 2 secunde total
            repeat: totalSteps,
            callback: () => {
                progress++;
                // Actualizam manual bara (sau emitem evenimentul de 'progress' daca foloseam fisiere reale)
                // Aici apelam logica de desenare direct sau putem emite un event fals
                
                // Pentru simplitate, redesenam bara direct aici folosind logica din createLoadingBar?
                // Nu, createLoadingBar asculta la `this.load`.
                // Hai sa incarcam niste imagini placeholder dummy online sau sa fortam eventul.
                
                // Varianta simpla: fortam update-ul grafic
                this.updateBarPercent(progress / totalSteps);
                
                if (progress >= totalSteps) {
                     this.scene.start('MainMenuScene');
                }
            }
        });
    }

    createLoadingBar() {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        
        this.progressBar = this.add.graphics();
        this.progressBox = this.add.graphics();
        this.progressBox.fillStyle(0x222222, 0.8);
        
        this.barW = 400; // Marim bara
        this.barH = 40;
        this.barX = (width - this.barW) / 2;
        this.barY = (height - this.barH) / 2;

        this.progressBox.fillRect(this.barX, this.barY, this.barW, this.barH);
    }
    
    updateBarPercent(value) {
        this.progressBar.clear();
        this.progressBar.fillStyle(0xffffff, 1);
        this.progressBar.fillRect(this.barX + 2, this.barY + 2, (this.barW - 4) * value, this.barH - 4);
    }
}

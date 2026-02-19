export class BaseScene extends Phaser.Scene {
    constructor(key) {
        super(key);
    }

    // Metode utilitare comune pentru toate scenele pot fi adăugate aici
    
    // Exemplu: Centrare element
    centerObject(gameObject, offsetX = 0, offsetY = 0) {
        const width = this.cameras.main.width;
        const height = this.cameras.main.height;
        gameObject.setX(width / 2 + offsetX);
        gameObject.setY(height / 2 + offsetY);
    }
}

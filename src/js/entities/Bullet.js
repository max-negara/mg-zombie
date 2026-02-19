export class Bullet extends Phaser.Physics.Arcade.Sprite {
    constructor(scene, x, y, direction) {
        // Create a 4x4 yellow texture on the fly if it doesn't exist
        if (!scene.textures.exists('bullet')) {
            const graphics = scene.make.graphics({ x: 0, y: 0, add: false });
            graphics.fillStyle(0xffff00);
            graphics.fillRect(0, 0, 4, 4);
            graphics.generateTexture('bullet', 4, 4);
        }

        super(scene, x, y, 'bullet');
        scene.add.existing(this);
        scene.physics.add.existing(this);

        this.speed = 400;
        this.direction = direction; // 1 or -1
        this.born = 0;
        this.lifespan = 2000; // ms

        this.setVelocityX(this.speed * this.direction);
        this.body.allowGravity = false; // Bullets fly straight
    }

    update(time, delta) {
        this.born += delta;
        if (this.born > this.lifespan) {
            this.destroy();
        }
    }
}

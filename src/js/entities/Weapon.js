import { Bullet } from './Bullet.js';

export class Weapon {
    constructor(scene, player) {
        this.scene = scene;
        this.player = player;
        
        // Physics group for bullets
        this.bullets = this.scene.physics.add.group({
            classType: Bullet,
            runChildUpdate: true,
            allowGravity: false 
        });

        this.nextFire = 0;
        this.fireRate = 200; // ms
        this.damage = 25;
    }

    fire() {
        if (this.scene.time.now < this.nextFire) {
            return;
        }

        const x = this.player.x + (this.player.facing === 1 ? 20 : -20);
        const y = this.player.y;

        // Create bullet
        const bullet = new Bullet(this.scene, x, y, this.player.facing);
        this.bullets.add(bullet);
        
        // CRITICAL FIX: Re-apply velocity and physics settings AFTER adding to group
        // Group.add() can sometimes reset the body or velocity depending on config
        if (bullet.body) {
            bullet.body.setAllowGravity(false);
            bullet.body.setVelocityX(bullet.speed * bullet.direction);
        }

        this.nextFire = this.scene.time.now + this.fireRate;
    }
}

import { Enemy } from '../entities/Enemy.js';

export class WaveManager {
    constructor(scene, player, ground) {
        this.scene = scene;
        this.player = player;
        this.ground = ground;

        this.enemies = this.scene.add.group({
            runChildUpdate: true
        });

        // Wave settings
        this.waveNumber = 1;
        this.enemiesInWave = 5;
        this.enemiesSpawned = 0;
        this.enemiesKilled = 0;
        
        this.spawnTimer = 0;
        this.spawnInterval = 2000; // ms

        this.active = false;
    }

    start() {
        this.active = true;
        this.startNextWave();
    }

    startNextWave() {
        this.enemiesInWave = 5 + Math.floor(this.waveNumber * 1.5);
        this.enemiesSpawned = 0;
        this.enemiesKilled = 0; // Reset for wave tracking if needed
        console.log(`Starting Wave ${this.waveNumber} with ${this.enemiesInWave} enemies`);
        
        // Notify UI if possible
        if (this.scene.updateWaveText) {
            this.scene.updateWaveText(this.waveNumber);
        }
    }

    update(time, delta) {
        if (!this.active) return;

        // Spawning logic
        if (this.enemiesSpawned < this.enemiesInWave) {
            this.spawnTimer += delta;
            if (this.spawnTimer > this.spawnInterval) {
                this.spawnEnemy();
                this.spawnTimer = 0;
                // Decrease interval slightly as waves progress
                this.spawnInterval = Math.max(500, 2000 - (this.waveNumber * 50));
            }
        } else {
            // Check if wave is cleared
            if (this.enemies.countActive(true) === 0) {
                this.waveNumber++;
                this.startNextWave();
            }
        }
    }

    spawnEnemy() {
        // Spawn from left or right side of screen, randomly
        const spawnRight = Math.random() > 0.5;
        const cam = this.scene.cameras.main;
        
        // Spawn outside camera view
        const x = spawnRight ? cam.worldView.right + 50 : cam.worldView.left - 50;
        // Adjust x to be within world bounds if possible, or just let them walk in
        // Ideally we want them to spawn on the ground.
        // We know groundY from GameScene but we can pass it or calculate it.
        // Assuming ground is at a known Y, typically `ground.y` is the top of the ground rect if origin is (0,0)
        
        // We need to inject the ground collision
        const y = this.ground.y - 40; // slightly above ground

        const enemy = new Enemy(this.scene, x, y, this.player);
        this.enemies.add(enemy);
        this.enemiesSpawned++;

        // Add collider with ground
        this.scene.physics.add.collider(enemy, this.ground);
    }
}

import { getSkinData } from '../data/Skins.js';

export class PixelRenderer {
    
    static adjustColor(hex, amount) {
        let r = (hex >> 16) & 0xFF;
        let g = (hex >> 8) & 0xFF;
        let b = hex & 0xFF;
        
        r = Math.max(0, Math.min(255, r + amount));
        g = Math.max(0, Math.min(255, g + amount));
        b = Math.max(0, Math.min(255, b + amount));
        
        return (r << 16) | (g << 8) | b;
    }

    static drawPlayer(graphics, x, y, w, h, facing, skinName) {
        const data = getSkinData(skinName);
        
        // Handle special custom drawing routines
        if (data.custom === 'goku') {
            this.drawGoku(graphics, x, y, w, h, facing);
            return;
        }

        const c_shirt = data.shirt;
        const c_pants = data.pants;
        const c_skin = data.skin;
        const c_hair = data.hair || 0x323232;
        const c_shoes = data.shoes || 0x323232;
        const has_hair = data.hasHair !== false;
        const hair_style = data.hairStyle || 'flat';

        // 1. Legs/Pants
        graphics.fillStyle(c_pants);
        graphics.fillRect(x, y + 10, w, h - 10);
        
        // Shading on pants
        const shade_x = (facing === 1) ? x : x + w - 2;
        const c_pants_shade = this.adjustColor(c_pants, -30);
        graphics.fillStyle(c_pants_shade);
        graphics.fillRect(shade_x, y + 10, 2, h - 10);
        
        // Center seam
        const c_pants_seam = this.adjustColor(c_pants, -20);
        graphics.fillStyle(c_pants_seam);
        graphics.fillRect(x + w / 2 - 1, y + 12, 2, h - 12);

        // 2. Shirt/Body
        graphics.fillStyle(c_shirt);
        graphics.fillRect(x, y + 4, w, 6);
        
        // Shading on shirt
        const c_shirt_shade = this.adjustColor(c_shirt, -30);
        graphics.fillStyle(c_shirt_shade);
        graphics.fillRect(shade_x, y + 4, 2, 6);

        // 3. Arms
        let arm_color = c_shirt;
        let arm_shade = this.adjustColor(arm_color, -20);

        if (facing === 1) {
            // Right arm (front)
            graphics.fillStyle(arm_color);
            graphics.fillRect(x + 4, y + 5, 3, 4);
            // Left arm (back)
            graphics.fillStyle(arm_shade);
            graphics.fillRect(x - 2, y + 5, 2, 4);
        } else {
            // Left arm (front)
            graphics.fillStyle(arm_color);
            graphics.fillRect(x + 5, y + 5, 3, 4);
            // Right arm (back)
            graphics.fillStyle(arm_shade);
            graphics.fillRect(x + w, y + 5, 2, 4);
        }

        // 4. Head
        graphics.fillStyle(c_skin);
        graphics.fillRect(x + 2, y - 6, w - 4, 8);
        
        // Shading on face
        const face_shade_x = (facing === 1) ? x + 2 : x + w - 4;
        const c_skin_shade = this.adjustColor(c_skin, -20);
        graphics.fillStyle(c_skin_shade);
        graphics.fillRect(face_shade_x, y - 6, 2, 8);

        // 5. Belt (if shirt != pants)
        if (c_shirt !== c_pants) {
            graphics.fillStyle(0x1E1E1E); // (30,30,30)
            graphics.fillRect(x, y + 9, w, 1);
            graphics.fillStyle(0xB4B4B4); // (180,180,180)
            graphics.fillRect(x + w / 2 - 1, y + 9, 2, 1); // Buckle
        }

        // Hair / Hat
        if (has_hair) {
            graphics.fillStyle(c_hair);
            if (hair_style === 'flat') {
                graphics.fillRect(x + 2, y - 8, w - 4, 2);
                graphics.fillRect(x + 1, y - 7, w - 2, 2);
            } else if (hair_style === 'spiky') {
                const centerX = x + w / 2;
                graphics.fillPoints([{x: x, y: y-6}, {x: x+2, y: y-9}, {x: x+4, y: y-6}]); // Left spike
                graphics.fillPoints([{x: x+w, y: y-6}, {x: x+w-2, y: y-9}, {x: x+w-4, y: y-6}]); // Right spike
                graphics.fillPoints([{x: centerX-2, y: y-6}, {x: centerX, y: y-10}, {x: centerX+2, y: y-6}]); // Middle spike
            } else if (hair_style === 'hat_red') { // Mario
                graphics.fillStyle(0xFF0000);
                graphics.fillRect(x + 1, y - 8, w - 2, 3);
                const brimX = (facing === 1) ? x + w : x - 2;
                graphics.fillRect(brimX, y - 7, 4, 2);
            } else if (hair_style === 'hat_green') { // Luigi
                graphics.fillStyle(0x00C800);
                graphics.fillRect(x + 1, y - 8, w - 2, 3);
                const brimX = (facing === 1) ? x + w : x - 2;
                graphics.fillRect(brimX, y - 7, 4, 2);
            } else if (hair_style === 'cowl_black') { // Batman
                graphics.fillStyle(0x141414);
                graphics.fillRect(x + 1, y - 9, w - 2, 5);
                graphics.fillPoints([{x: x+1, y: y-9}, {x: x+1, y: y-12}, {x: x+3, y: y-9}]); // Left ear
                graphics.fillPoints([{x: x+w-1, y: y-9}, {x: x+w-1, y: y-12}, {x: x+w-3, y: y-9}]); // Right ear
            }
        }

        // Eyes
        // ex = x + (w - 6 if facing == 1 else 2)
        const ex = x + ((facing === 1) ? w - 6 : 2);
        
        if (skinName === 'batman') {
            graphics.fillStyle(0xFFFFFF);
            graphics.fillRect(ex, y - 4, 3, 2);
        } else {
            // Standard eyes
            graphics.fillStyle(0xFFFFFF);
            graphics.fillRect(ex, y - 4, 3, 3);
            const pupilX = ex + ((facing === 1) ? 1 : 0);
            graphics.fillStyle(0x141414);
            graphics.fillRect(pupilX, y - 3, 2, 2);
        }

        // Shoes
        graphics.fillStyle(c_shoes);
        graphics.fillRect(x + 2, y + h - 2, 4, 4);
        graphics.fillRect(x + w - 6, y + h - 2, 4, 4);
        
        // Laces
        graphics.fillStyle(0xC8C8C8);
        graphics.fillRect(x + 3, y + h - 2, 2, 1);
        graphics.fillRect(x + w - 5, y + h - 2, 2, 1);
    }

    static drawWeapon(graphics, x, y, w, h, facing) {
        // Simple Gun (Pistol)
        // Coords relative to player top-left (x,y)
        
        // Hand position approximation based on drawPlayer arm logic
        // Arm is at y+5, h=4. Hand is at the bottom of arm? or end?
        // Let's place gun at y+6 (mid-arm height) usually extended.
        
        graphics.fillStyle(0x222222); // Gun Dark Gray
        
        const gunY = y + 6;
        let gunX;
        
        if (facing === 1) {
            // Facing Right
            gunX = x + w - 2; // extended from body
            // Barrel
            graphics.fillRect(gunX, gunY, 8, 3);
            // Handle
            graphics.fillRect(gunX, gunY + 2, 3, 4);
        } else {
            // Facing Left
            gunX = x - 6; // extended left
            // Barrel
            graphics.fillRect(gunX, gunY, 8, 3);
            // Handle
            graphics.fillRect(gunX + 5, gunY + 2, 3, 4);
        }
    }
    
    // Custom Goku Drawer - ported from Python
    static drawGoku(graphics, x, y, w, h, facing) {
        // Body (Gi)
        graphics.fillStyle(0xFF8C00); // Orange
        graphics.fillRect(x, y + 4, w, h - 4);
        
        // Undershirt
        graphics.fillStyle(0x0000C8); // Blue
        graphics.fillRect(x + 2, y + 4, w - 4, 4);
        
        // Sash
        graphics.fillRect(x, y + 10, w, 2);
        
        // Head
        graphics.fillStyle(0xFFDCAA); // Skin
        graphics.fillRect(x + 2, y - 6, w - 4, 8);
        
        // Hair (Anime Style - Defined "Palm tree" shape)
        graphics.fillStyle(0x000000);
        
        const cx = x + w / 2;
        const hy = y - 6; // Head Top Y level

        // 1. Base Density (covers the scalp)
        graphics.fillRect(x, hy - 4, w, 5);

        // 2. Right Side Spikes (3 distinct tiers)
        // Lower
        graphics.fillPoints([{x: cx+3, y: hy+1}, {x: cx+12, y: hy+2}, {x: cx+4, y: hy-3}]);
        // Middle
        graphics.fillPoints([{x: cx+2, y: hy-2}, {x: cx+13, y: hy-5}, {x: cx+3, y: hy-6}]);
        // Upper
        graphics.fillPoints([{x: cx+1, y: hy-5}, {x: cx+10, y: hy-12}, {x: cx, y: hy-7}]);

        // 3. Left Side Spikes (3 distinct tiers)
        // Lower
        graphics.fillPoints([{x: cx-3, y: hy+1}, {x: cx-12, y: hy+2}, {x: cx-4, y: hy-3}]);
        // Middle
        graphics.fillPoints([{x: cx-2, y: hy-2}, {x: cx-13, y: hy-5}, {x: cx-3, y: hy-6}]);
        // Upper
        graphics.fillPoints([{x: cx-1, y: hy-5}, {x: cx-10, y: hy-12}, {x: cx, y: hy-7}]);

        // 4. Top/Crown Spikes
        // Main top spike leaning slightly
        graphics.fillPoints([{x: cx-3, y: hy-5}, {x: cx-5, y: hy-14}, {x: cx+3, y: hy-5}]);
        
        // 5. Bangs (Forehead)
        // Left Bang
        graphics.fillPoints([{x: cx-1, y: hy-3}, {x: cx-4, y: hy+3}, {x: cx-2, y: hy-4}]);
        // Right Bang
        graphics.fillPoints([{x: cx+1, y: hy-3}, {x: cx+4, y: hy+3}, {x: cx+2, y: hy-4}]);
        
        // Eyes
        const ex = x + ((facing === 1) ? w - 5 : 1);
        graphics.fillStyle(0x000000);
        graphics.fillRect(ex, y - 4, 2, 2);
        
        // Boots
        graphics.fillStyle(0x000096);
        graphics.fillRect(x + 2, y + h - 2, 4, 4);
        graphics.fillRect(x + w - 6, y + h - 2, 4, 4);
    }
}

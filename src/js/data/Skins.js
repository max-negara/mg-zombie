export const SKINS = {
    'default': {
        shirt: 0xFFDC96, // (255, 220, 150)
        pants: 0xC8A06E, // (200, 160, 110)
        skin: 0xFFDCAA,  // (255, 220, 170)
        hair: 0x323232,  // (50, 50, 50)
        shoes: 0x323232,
        hairStyle: 'flat',
        hasHair: true
    },
    'blue': {
        shirt: 0x64B4FF, // (100, 180, 255)
        pants: 0x4678B4, // (70, 120, 180)
        skin: 0xFFDCAA,
        hair: 0x323232,
        shoes: 0x323232,
        hairStyle: 'flat',
        hasHair: true
    },
    'green': {
        shirt: 0x8CFF8C, // (140, 255, 140)
        pants: 0x5AB45A, // (90, 180, 90)
        skin: 0xFFDCAA,
        hair: 0x323232,
        shoes: 0x323232,
        hairStyle: 'flat',
        hasHair: true
    },
    'naruto': {
        shirt: 0xFF8C00, // (255, 140, 0)
        pants: 0xFF8C00,
        skin: 0xFFDCAA,
        hair: 0xFFFF00, // (255, 255, 0)
        shoes: 0x000096, // (0, 0, 150)
        hairStyle: 'spiky',
        hasHair: true
    },
    'sasuke': {
        shirt: 0xC8C8FF, // (200, 200, 255)
        pants: 0xF0F0F0,
        skin: 0xFFDCAA,
        hair: 0x141428,
        shoes: 0x323232,
        hairStyle: 'spiky',
        hasHair: true
    },
    'mario': {
        shirt: 0xFF0000,
        pants: 0x0000C8,
        skin: 0xFFDCAA,
        hair: 0x502800,
        shoes: 0x323232,
        hairStyle: 'hat_red',
        hasHair: true
    },
    'luigi': {
        shirt: 0x00C800,
        pants: 0x0000C8,
        skin: 0xFFDCAA,
        hair: 0x502800,
        shoes: 0x323232,
        hairStyle: 'hat_green',
        hasHair: true
    },
    'saitama': {
        shirt: 0xFFFF00,
        pants: 0xFFFF00,
        skin: 0xFFDCAA,
        shoes: 0xC83232,
        hasHair: false
    },
    'homer': {
        shirt: 0xFFFFFF,
        pants: 0x6496FF,
        skin: 0xFFFF00,
        shoes: 0x323232,
        hasHair: false
    },
    'batman': {
        shirt: 0x323232,
        pants: 0x323232,
        skin: 0xC8B496,
        shoes: 0x323232,
        hairStyle: 'cowl_black',
        hasHair: true
    },
    'goku': {
        // Special marker for custom renderer logic
        custom: 'goku' 
    },
    'zombie': {
        shirt: 0x009696,
        pants: 0x000096,
        skin: 0x329632, // Greenish
        hair: 0x1E501E,
        shoes: 0x1E1E1E,
        hairStyle: 'flat',
        hasHair: true
    }
};

export function getSkinData(name) {
    return SKINS[name] || SKINS['default'];
}

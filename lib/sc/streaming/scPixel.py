from enum import IntEnum

class ScPixel(IntEnum):
    # ETC2 / EAC
    EAC_R11 = 170
    EAC_SIGNED_R11 = 172
    EAC_RG11 = 174
    EAC_SIGNED_RG11 = 176
    ETC2_EAC_RGBA8 = 178
    ETC2_EAC_SRGBA8 = 179
    ETC2_RGB8 = 180
    ETC2_SRGB8 = 181
    ETC2_RGB8_PUNCHTHROUGH_ALPHA1 = 182
    ETC2_SRGB8_PUNCHTHROUGH_ALPHA1 = 183
    
    
    # ASTC SRGBA8
    ASTC_SRGBA8_4x4 = 186
    ASTC_SRGBA8_5x4 = 187
    ASTC_SRGBA8_5x5 = 188
    ASTC_SRGBA8_6x5 = 189
    ASTC_SRGBA8_6x6 = 190
    ASTC_SRGBA8_8x5 = 192
    ASTC_SRGBA8_8x6 = 193
    ASTC_SRGBA8_8x8 = 194
    ASTC_SRGBA8_10x5 = 195
    ASTC_SRGBA8_10x6 = 196
    ASTC_SRGBA8_10x8 = 197
    ASTC_SRGBA8_10x10 = 198
    ASTC_SRGBA8_12x10 = 199
    ASTC_SRGBA8_12x12 = 200
    
    # ASTC RGBA8
    ASTC_RGBA8_4x4 = 204
    ASTC_RGBA8_5x4 = 205
    ASTC_RGBA8_5x5 = 206
    ASTC_RGBA8_6x5 = 207
    ASTC_RGBA8_6x6 = 208
    ASTC_RGBA8_8x5 = 210
    ASTC_RGBA8_8x6 = 211
    ASTC_RGBA8_8x8 = 212
    ASTC_RGBA8_10x5 = 213
    ASTC_RGBA8_10x6 = 214
    ASTC_RGBA8_10x8 = 215
    ASTC_RGBA8_10x10 = 216
    ASTC_RGBA8_12x10 = 217
    ASTC_RGBA8_12x12 = 218
    
    # ETC1
    ETC1_RGB8 = 263
    
    @staticmethod
    def glInternalFormat(pixel_type):
        # Dictionary-basiertes Lookup (kompatibel mit Python < 3.10)
        format_map = {
            ScPixel.ETC1_RGB8: 0x648d,
            
            # ETC2 / EAC
            ScPixel.EAC_R11: 0x9270,
            ScPixel.EAC_SIGNED_R11: 0x9273,
            ScPixel.EAC_RG11: 0x9272,
            ScPixel.EAC_SIGNED_RG11: 0x9273,
            ScPixel.ETC2_EAC_RGBA8: 0x9278,
            ScPixel.ETC2_EAC_SRGBA8: 0x9279,
            ScPixel.ETC2_RGB8: 0x9274,
            ScPixel.ETC2_SRGB8: 0x9275,
            ScPixel.ETC2_RGB8_PUNCHTHROUGH_ALPHA1: 0x9276,
            ScPixel.ETC2_SRGB8_PUNCHTHROUGH_ALPHA1: 0x9277,
            
            # ASTC SRGBA8
            ScPixel.ASTC_SRGBA8_4x4: 0x93D0,
            ScPixel.ASTC_SRGBA8_5x4: 0x93D1,
            ScPixel.ASTC_SRGBA8_5x5: 0x93D2,
            ScPixel.ASTC_SRGBA8_6x5: 0x93D3,
            ScPixel.ASTC_SRGBA8_6x6: 0x93D4,
            ScPixel.ASTC_SRGBA8_8x5: 0x93D5,
            ScPixel.ASTC_SRGBA8_8x6: 0x93D6,
            ScPixel.ASTC_SRGBA8_8x8: 0x93D7,
            ScPixel.ASTC_SRGBA8_10x5: 0x93D8,
            ScPixel.ASTC_SRGBA8_10x6: 0x93D9,
            ScPixel.ASTC_SRGBA8_10x8: 0x93DA,
            ScPixel.ASTC_SRGBA8_10x10: 0x93DB,
            ScPixel.ASTC_SRGBA8_12x10: 0x93DC,
            ScPixel.ASTC_SRGBA8_12x12: 0x93DD,
            
            # ASTC RGBA8
            ScPixel.ASTC_RGBA8_4x4: 0x93B0,
            ScPixel.ASTC_RGBA8_5x4: 0x93B1,
            ScPixel.ASTC_RGBA8_5x5: 0x93B2,
            ScPixel.ASTC_RGBA8_6x5: 0x93B3,
            ScPixel.ASTC_RGBA8_6x6: 0x93B4,
            ScPixel.ASTC_RGBA8_8x5: 0x93B5,
            ScPixel.ASTC_RGBA8_8x6: 0x93B6,
            ScPixel.ASTC_RGBA8_8x8: 0x93B7,
            ScPixel.ASTC_RGBA8_10x5: 0x93B8,
            ScPixel.ASTC_RGBA8_10x6: 0x93B9,
            ScPixel.ASTC_RGBA8_10x8: 0x93BA,
            ScPixel.ASTC_RGBA8_10x10: 0x93BB,
            ScPixel.ASTC_RGBA8_12x10: 0x93BC,
            ScPixel.ASTC_RGBA8_12x12: 0x93BD,
        }
        
        return format_map.get(pixel_type, 0xFFFF)

class Base62Generator:
    """Generator for unique base62 encoded strings"""
    
    CHARS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    @classmethod
    def encode(cls, num: int) -> str:
        """
        Encode a number into base62 string.
        
        Args:
            num: The number to encode
            
        Returns:
            str: The base62 encoded string
        """
        if num == 0:
            return "0"
        
        result = ""
        while num > 0:
            result = cls.CHARS[num % 62] + result
            num //= 62
            
        return result
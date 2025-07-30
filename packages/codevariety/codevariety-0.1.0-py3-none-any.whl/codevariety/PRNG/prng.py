import time

class PRNG:
    def __init__(self, seed:int=None) -> None:
        """
        A collection of functions to generate random values.
        :param seed: Enter a custom seed for hash function. Must be an integer. Defaulted to None. Disclaimer: Changing seed can have a negative effect on randomness of output!
        """
        if seed:
            if type(seed) != int:
                raise ValueError(f'Invalid type. Seed must be an integer! Seed entered: {seed}')
            self.seed = seed
        else:
            self.seed = int(time.time()*1000)
        self.max_value = 999993089
    
    def random_integer(self, min_value:int=None, max_value:int=None):
        """Returns a random integer

        :param min_value: Minimum value returned. Defaulted to None.
        :param max_value: Maximum value returned. Defaulted to None.
        """
        if min_value is not None and max_value is not None and min_value > max_value:
            raise ValueError(f'min_value ({min_value}) is greater than max_value ({max_value})')
        value = str(time.time() * 1000)
        log = []
        for x in range(501):
            if x == 0:
                hashed_value = self._poly_hash(value=value)
                log.append(hashed_value)
            else:
                self.seed = hashed_value
                hashed_value = self._poly_hash(value=value)
                log.append(hashed_value)
        if min_value is None and max_value is None:
            return log[500]
        elif min_value is not None and max_value is None:
            return log[500] + min_value
        elif min_value is None and max_value is not None:
            return log[500] % max_value
        elif min_value is not None and max_value is not None:
            range_size = max_value - min_value + 1
            scaled_value = log[500] % range_size
            final_value = scaled_value + min_value
            return final_value

    def random_letter(self, min_letter:str=None, max_letter:str=None, lower:bool=False) -> str:
        """Returns a random letter.
        :param min_letter: Minimum letter returned ('A' being the lowest value). Defaulted to None.
        :param max_letter: Maximum letter returned ('Z' being the largest value). Defaulted to None.
        :param lower: If True, value returned is lowercase. Defaulted to False.
        """
        # Determine the ASCII bounds
        min_ascii = ord(min_letter) if min_letter else 65 # Default to 'A'
        max_ascii = ord(max_letter) if max_letter else 90 # Default to 'Z'

        if min_ascii > max_ascii:
            raise ValueError(f'min_letter ({min_letter}) cannot be greater than max_letter ({max_letter})')
        
        # Generate a random letter within range
        range_size = max_ascii - min_ascii + 1
        random_ascii = min_ascii + (self.random_integer() % range_size)
        if lower:
            return chr(random_ascii).lower()
        else:
            return chr(random_ascii)
        
    def random_float(self, min_value:int=None, max_value:int=None, decimal_range:int=2) -> float:
        """Returns a random float
        :param min_value: Minimum value returned. Default is None.
        :param max_value: Maximum value returned. Default is None.
        :param decimal_range: Number of decimal places on float. Default is 2.
        """
        if min_value is not None and max_value is not None and min_value >= max_value:
            raise ValueError(f'Invalid min/max combination. Min: {min_value}, Max: {max_value}')
        value = str(time.time() * 1000)
        log = []
        for x in range(501):
            if x == 0:
                hashed_value = self._poly_hash(value=value)
                log.append(hashed_value)
            else:
                self.seed = hashed_value
                hashed_value = self._poly_hash(value=value)
                log.append(hashed_value)
        random_value = float(f'{log[500]}.{log[499]}')
        if min_value is None and max_value is None:
            return round(random_value, decimal_range)
        elif min_value is not None and max_value is None:
            random_value += min_value
            return round(random_value, decimal_range)
        elif min_value is None and max_value is not None:
            random_value = random_value % max_value
            return round(random_value, decimal_range)
        elif min_value is not None and max_value is not None:
            range_size = max_value - min_value
            scaled_value = random_value % range_size
            final_value = scaled_value + min_value
            return round(final_value, decimal_range)

    def random_choice(self, array:list):
        """Returns a random item from a list.
        :param array: List that random item is returned from.
        """
        return array[self.random_integer(0, len(array) - 1)]
    
    def random_shuffle(self, array:list):
        """Returns a list with all items randomly shuffled.
        :param array: List that will be returned with items shuffled.
        """
        shuffled = array[:]
        for i in range(len(shuffled)):
            j = self.random_integer(0, i)
            shuffled[i], shuffled[j] = shuffled[j], shuffled[i]
        return shuffled

    def _poly_hash(self, value, base=7177, mod=1000000007):
        hash_value = self.seed
        for char in value:
            hash_value = (hash_value * base + ord(char)) % mod
        return hash_value
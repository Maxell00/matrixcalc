# Monomial contains a series of variables and degrees, but not a coefficient
# Monomial is a dictionary, with keys representing variables, and values representing degrees
class Monomial:
    def __init__(self, exponents):
        # Should data be in form of dict?
        if not data:
            # Arch decision -- allow empty monomial? -- leaning yes
        # Internal structure with dictionary
        # {}

    # Returns a variable's degree
    def __getitem__(self, key):
        return self._exponents[key]

    # Sets a variable's degree
    def __setitem__(self, key, value):
        # Should this shallow copy value?
        self._exponents[key] = value

    def __repr__(self):
        return f"Monomial({self._exponents!r})"

    def __str__(self):
        # Have to decide how to make exponents look nice in terminal-friendly way

    def __eq__(self, other):
        if not isinstance(other, Monomial):
            return False
        return self._variables == other._variables

    def __add__(self, other):
        if not isinstance(other, Monomial):
            raise TypeError("Monomial must be added to a monomial")
        # Perhaps ban adding? Should only be added via polynomial implementation

    def __sub__(self, other):
        if not isinstance(other, Monomial):
            raise TypeError("Monomial must be subtracted from a monomial")
        # See note above

    def __mul__(self, other):
        if not isinstance(other, Monomial):
            raise TypeError("Monomial must be multiplied with a monomial")

        result_data = {}
        for key in self.keys() & other.keys():
            result_data[key] = self.get(key, 0) + other.get(key, 0)
        return Monomial(result_data).clean()

    def __rmul__(self, other):
        return self * other
            
    # Needed?
    def __truediv__(self, scalar):
        # Placeholder

    def __neg__(self):
        return -1 * self

    # Methods

    # Remove zero entries
    def clean(self):
        for key, value in self.items():
            if value == 0:
                self.pop(key)

# A Polynomial stores only nonzero coefficients, with integer exponents ≥ 0
# Its internal mapping is normalized so that each exponent occurs exactly once.

class Polynomial:
    def __init__(self, data):
        # Placeholder

    # Returns a coefficient
    def __getitem__(self, index):
        # Placeholder
    
    # Sets a coefficient
    def __setitem__(self, index, value):
        # Placeholder

    def __repr__(self):
        # Placeholder

    def __str__(self):
        # Placeholder

    def __eq__(self, other):
        # Placeholder

    def __add__(self, other):
        # Placeholder

    def __sub__(self, other):
        # Placeholder

    def __mul__(self, other):
        # Placeholder

    def __rmul__(self, other):
        # Placeholder
            
    # Needed?
    def __truediv__(self, scalar):
        # Placeholder

    def __neg__(self):
        return -1 * self


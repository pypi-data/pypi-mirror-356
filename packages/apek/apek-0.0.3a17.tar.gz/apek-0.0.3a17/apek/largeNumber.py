# -*- coding: utf-8 -*-
"""
The main module of the package.

Handle large numbers through the LargeNumber class.

Classes:
    LargeNumber:
        The main class.
"""



import math as _math
import re as _re
from ._base import _showArgsError, _checkAndShowParamTypeError



class LargeNumber():
    """
    Handle large numbers through the class.
    
    Attributes:
        base (float): The base part of the number.
        exp (int): The exponent part of the number.
        isNegative (bool): Set whether the base is negative.
        cfg (dict): The dictionary that stores dispPrec, realPrec, reprUnits_en, and reprUnits_zh.
    
    Methods:
        parseToString:
            Convert the LargeNumber instance to a string based on the provided or default formatting parameters.
    """
    
    @staticmethod
    def _parseLargeNumberOrShowError(n):
        _checkAndShowParamTypeError("n", n, (LargeNumber, int, float))
        if not isinstance(n, (LargeNumber)):
            return LargeNumber(n, 0)
        return n
    
    def __init__(
        self,
        base = 0,
        exp = 0,
        *args,
        dispPrec = 4,
        realPrec = 8,
        reprUnits_en = "KMBTPEZY",
        reprUnits_zh = "万亿兆京垓秭穰"
    ):
        """
        Provide parameters "base" and "exp" to create an instance of LargeNumber.
        
        The specific value of LargeNumber is set through "base" and "exp",
        and it also supports setting precision and display unit table.
        
        Args:
            base (int or float, optional):
                "base" is used to control the base part of LargeNumber, that is the "X" in "XeY",
                and its range will be automatically calibrated to [1, 10).
                The corresponding "exp" will be modified.
                The default is 0.
            exp (int, optional):
                "exp" is used to control the exponent part of LargeNumber, that is the "Y" in "XeY".
                The default is 0.
            *args:
                When the constructor's argument list provides more (greater than or equal to three) non-keyword arguments,
                a TypeError will be thrown.
            dispPrec (int, optional):
                Keyword argument.
                Controls the decimal precision when displaying.
                Parts below the precision will be automatically rounded.
                It cannot be greater than "realPrec" and cannot be negative.
                The default is 4.
            realPrec (int, optional):
                Keyword argument.
                Controls the decimal precision during actual calculations.
                Parts below the precision will be discarded.
                It cannot be less than "dispPrec" and cannot be negative.
                The default is 8.
            reprUnits_en (str or list or tuple, optional):
                Keyword argument.
                Controls the English units used for the exponent part when converting a LargeNumber instance with a large "exp" to a string.
                When accepting a str, each character is treated as a unit.
                When accepting a list or tuple, each item is treated as a unit.
                The units are ordered from smallest to largest from the beginning to the end.
                The iterable object must not be empty.
            reprUnits_zh (str or list or tuple, optional):
                Keyword argument.
                Controls the Chinese units used for the exponent part when converting a LargeNumber instance with a large "exp" to a string.
                When accepting a str, each character is treated as a unit.
                When accepting a list or tuple, each item is treated as a unit.
                The units are ordered from smallest to largest from the beginning to the end. The iterable object must not be empty.
        
        Returns:
            None
        
        Raises:
            TypeError: A TypeError will be thrown when the number or type of the accepted arguments is incorrect.
            ValueError: A ValueError will be thrown when the value of the accepted arguments is incorrect.
        """
        
        _checkAndShowParamTypeError("base", base, (int, float))
        _checkAndShowParamTypeError("exp", exp, int)
        if args:
            _showArgsError(args)
        
        if base < 0:
            self.isNegative = True
            base = -base
        else:
            self.isNegative = False
        self.base, self.exp = base, exp
        
        cfg = {}
        
        if dispPrec:
            _checkAndShowParamTypeError("dispPrec", dispPrec, int)
            if dispPrec < 0:
                raise ValueError("The parameter 'dispPrec' cannot be less than 0.")
            cfg["dispPrec"] = dispPrec
        else:
            cfg["dispPrec"] = 4
        
        if realPrec:
            _checkAndShowParamTypeError("realPrec", realPrec, int)
            if realPrec < 0:
                raise ValueError("The parameter 'realPrec' cannot be less than 0.")
            if realPrec < dispPrec:
                raise ValueError("The parameter 'realPrec' cannot be less than parameter 'dispPrec'.")
            cfg["realPrec"] = realPrec
        else:
            cfg["realPrec"] = 8
        
        if reprUnits_en:
            _checkAndShowParamTypeError("reprUnits_en", reprUnits_en, (str, list, tuple))
            if not reprUnits_en:
                raise ValueError(f"The paramter 'reprUnits_en' cannot be empty {type(reprUnits_en).__name__}.")
            cfg["reprUnits_en"] = reprUnits_en
        else:
            cfg["reprUnits_en"] = "KMBTPEZY"
        
        if reprUnits_zh:
            _checkAndShowParamTypeError("reprUnits_zh", reprUnits_zh, (str, list, tuple))
            if not reprUnits_zh:
                raise ValueError(f"The paramter 'reprUnits_zh' cannot be empty {type(reprUnits_en).__name__}.")
            cfg["reprUnits_zh"] = reprUnits_zh
        else:
            cfg["reprUnits_zh"] = "万亿兆京垓秭穰"
        
        self.config = cfg
        
        self._calibrate()
    
    def _calibrate(self):
        base, exp = self.getBase(), self.getExp()
        
        k = _math.floor(_math.log10(base)) if base != 0 else 0
        exp += k
        base /= 10 ** k
        
        t = 10 ** self.getConfig("realPrec")
        s1 = base * t
        s2 = _math.floor(s1)
        base = s2 / t
        
        self.base, self.exp = base, exp
    
    def getBase(self):
        """
        Get the base.
        
        Returns:
            float: The base.
        """
        
        if self.isNegative:
            return -self.base
        return self.base
    
    def getExp(self):
        """
        Get the exponent.
        
        Returns:
            int: The exponent.
        """
        
        return self.exp
    
    def getConfig(self, key):
        """
        Get the configs.
        
        Returns:
            dict: The configs.
        """
        
        if not key:
            return self.cofig
        return self.config.get(key)
    
    def _insertUnit(self, number, mul, units):
        if number < mul:
            return str(number)
        
        for unit in units:
            number = round(number / mul, self.getConfig("realPrec"))
            if number < mul:
                return f"{number}{unit}"
    
    def parseString(self, *args, prec="default", expReprMode="comma", template="{0}e{1}", alwayUseTemplate=False):
        if args:
            _showArgsError(args)
        if prec == "default":
            prec = self.getConfig("dispPrec")
        _checkAndShowParamTypeError("prec", prec, int)
        _checkAndShowParamTypeError("expReprMode", expReprMode, str)
        _checkAndShowParamTypeError("alwayUseTemplate", alwayUseTemplate, bool)
        
        base, exp = self.getBase(), self.getExp()
        if -4 <= exp <= self.getConfig("realPrec") and not alwayUseTemplate:
            r = str(base * 10 ** exp)
            return r
        
        dispBase = str(round(base * 10 ** prec) / 10 ** prec)
        dispExp = None
        
        if exp >= 1_000_000_000_000_000 or exp <= -10:
            expReprMode = "power"
        
        if expReprMode ==  "comma":
            dispExp = f"{exp:,}"
        elif expReprMode ==  "byUnit_en":
            dispExp = self._insertUnit(exp, 1000, self.getConfig("reprUnits_en"))
        elif expReprMode ==  "byUnit_zh":
            dispExp = self._insertUnit(exp, 10000, self.getConfig("reprUnits_zh"))
        elif expReprMode ==  "power":
            dispExp = str(LargeNumber(exp, 0))
        else:
            raise ValueError(f"Invalid expReprMode: {repr(expReprMode)}")
        
        return template.format(dispBase, dispExp)
    
    def parseInt(self, *args, mode="default"):
        """
        Convert the string to an integer.
        
        Args:
            mode (str):
                Keyword argument.
                Controls the behavior when converting to an integer.
                In "default" mode, it will be directly converted to an integer.
                In "power N" mode, when the exponent is greater than N, an error will be thrown, using only "power" defaults to "power 128".
        
        Returns:
            int:
                The converted integer.
        
        Raises:
            OverflowError:
                This error is raised when the exponent exceeds the specified range of power,
                or the limits of Python.
            ValueError:
                This error will be thrown when an unknown conversion mode is accepted.
        """
        
        if args:
            _showArgsError(args)
        _checkAndShowParamTypeError("mode", mode, str)
        
        if mode == "default":
            if self.getBase() == 0:
                return 0
            if self.getConfig("realPrec") >= self.getExp():
                return int(self.getBase() * 10 ** self.getExp())
            expSub = self.getExp() - self.getConfig("realPrec")
            base = str(self.getBase()).replace(".", "")
            expSub -= len(base) - 1
            return int(base + "0" * expSub)
        
        if mode == "power" or _re.search("^power\\s+\\d{1,6}$", mode):
            if mode == "power":
                mode = "power 128"
            power = int(_re.split("\\s+", mode)[1])
            if self.getExp() > power:
                raise OverflowError(f"The exponent exceeds the allowed upper limit: {power}")
            return self.parseInt(mode="default")
        
        raise ValueError(f"Invalid mode: {repr(mode)}")
    
    def parseFloat(self, *args, prec=None, rounding="floor"):
        """
        Convert the string to an floating-point number.
        
        Args:
            prec (int):
                Keyword argument.
                Controls the precision of the floating-point number during conversion.
                Defaults to the realPrec in config.
            rounding ("floor" or "round" or "ceil"):
                Keyword argument.
                Controls the rounding mode
                The defaults to "floor".
        
        Returns:
            float:
                The converted floating-point number.
        
        Raises:
            ValueError:
                This error will be raised when an unknown rounding mode is accepted.
        """
        
        if args:
            _showArgsError(args)
        _checkAndShowParamTypeError("prec", prec, (None, int))
        
        if prec is None:
            prec = self.getConfig("realPrec")
        
        if not -256 < self.getExp() < 256:
            return 0.0 if self.getExp() < -256 else _math.inf
        f = float(self.getBase() * 10 ** self.getExp())
        
        if rounding == "floor":
            return _math.floor(f * 10 ** prec) / 10 ** prec
        if rounding == "ceil":
            return _math.ceil(f * 10 ** prec) / 10 ** prec
        if rounding == "round":
            return round(f, prec)
        raise ValueError(f"Invalid rounding mode: {repr(rounding)}")
    
    def __str__(self):
        return self.parseString()
    
    def __bool__(self):
        if self.getBase() == 0 and self.getExp() == 0:
            return False
        return True
    
    def __int__(self):
        return self.parseInt()
    
    def __float__(self):
        return self.parseFloat()
    
    def __complex__(self):
        return complex(float(self))
    
    def __repr__(self):
        return self.parseString(template="LargeNumber({0}, {1})", alwayUseTemplate=True)
    
    def __neg__(self):
        return LargeNumber(-self.getBase(), self.getExp())
    
    def __pos__(self):
        return self
    
    def __abs__(self):
        return LargeNumber(self.getBase(), self.getExp())
    
    def __eq__(self, other):
        other = self._parseLargeNumberOrShowError(other)
        if (self.getBase() == other.base) and (self.getExp() == other.exp):
            return True
        return False
    
    def __ne__(self, other):
        return not self == other
    
    def __lt__(self, other):
        other = self._parseLargeNumberOrShowError(other)
        if self.getExp() != other.exp:
            return self.getExp() < other.exp
        return self.getBase() < other.base
    
    def __le__(self, other):
        return self < other or self == other
    
    def __gt__(self, other):
        return not self <= other
    
    def __ge__(self, other):
        return not self < other
    
    def __add__(self, other):
        other = self._parseLargeNumberOrShowError(other)
        
        if self == other:
            return (self.getBase() + other.base, self.getExp())
        
        big, small = 0, 0
        if self < other:
            big, small = other, self
        else:
            big, small = self, other
        
        if big.getExp() - small.getExp() > big.getConfig("realPrec"):
            return big
        
        expSub = big.getExp() - small.getExp()
        bigBase = big.getBase * 10 ** expSub()
        smallBase = small.getBase()
        
        return LargeNumber(bigBase + smallBase, small.getExp())
    
    def __radd__(self, other):
        return self + other
    
    def __iadd__(self, other):
        return self + other
    
    def __sub__(self, other):
        return self + -other
    
    def __rsub__(self, other):
        return other + -self
    
    def __isub__(self, other):
        return self - other
    
    def __mul__(self, other):
        other = self._parseLargeNumberOrShowError(other)
        return LargeNumber(
            self.getBase() * other.getBase(),
            self.getExp() + other.getExp()
        )
    
    def __rmul__(self, other):
        return self * other
    
    def __imul__(self, other):
        return self * other
    
    def __truediv__(self, other):
        other = self._parseLargeNumberOrShowError(other)
        if other == 0:
            raise ZeroDivisionError(f"{repr(self)} cannot be divided by 0.")
        return LargeNumber(self.getBase() / other.base, self.getExp() - other.exp)
    
    def __rtruediv__(self, other):
        return other / self
    
    def __itruediv__(self, other):
        return self / other

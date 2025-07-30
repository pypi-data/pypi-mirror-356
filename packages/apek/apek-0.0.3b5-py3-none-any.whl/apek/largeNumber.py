# -*- coding: utf-8 -*-
"""
The main module of the package.

Handle large numbers through the LargeNumber class.

Classes:
    LargeNumber:
        The main class.
"""



# 导入math模块，标记为内部使用，即重命名以下划线开头。
import math as _math
# 导入re模块，标记为内部使用，即重命名以下划线开头。
import re as _re
# 从base导入基础函数，后续使用。
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
        # 检测n是不是LargeNumber int float的其中一种。
        _checkAndShowParamTypeError("n", n, (LargeNumber, int, float))
        # 如果n不是LargeNumber类型。
        if not isinstance(n, LargeNumber):
            # 把n转换为LargeNumber类型，并返回。
            return LargeNumber(n, 0)
        # 否则原路返回。
        return n
    
    def __init__(
        self,
        base = 0,  # 基数默认为0。
        exp = 0,  # 指数默认为0。
        *args,  # 无效参数。
        dispPrec = 4,  # 表示时的精度，默认4。
        realPrec = 8,  # 实际计算时的精度，默认8。
        reprUnits_en = "KMBTPEZY",  # 英文单位表。
        reprUnits_zh = "万亿兆京垓秭穰"  # 中文单位表。
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
        
        # 检测base是不是int或float类型，已经exp是不是int类型。
        _checkAndShowParamTypeError("base", base, (int, float))
        _checkAndShowParamTypeError("exp", exp, int)
        # 如果有无效参数，抛出错误。
        if args:
            _showArgsError(args)
        
        # 如果base是负数，设置“负数”标记。
        self.isNegative = base < 0
        # 存储base的绝对值和exp。
        self.base, self.exp = abs(base), exp
        
        # 初始化配置字典。
        cfg = {}
        _checkAndShowParamTypeError("dispPrec", dispPrec, int)
        # 如果精度小于0，抛出错误，因为不支持小于0的精度。
        if dispPrec < 0:
            raise ValueError("The parameter 'dispPrec' cannot be less than 0.")
        # 否则存储配置。
        cfg["dispPrec"] = dispPrec
        
        # 如果精度小于0，抛出错误，因为不支持小于0的精度。
        _checkAndShowParamTypeError("realPrec", realPrec, int)
        if realPrec < 0:
            raise ValueError("The parameter 'realPrec' cannot be less than 0.")
        if realPrec < dispPrec:
            raise ValueError("The parameter 'realPrec' cannot be less than parameter 'dispPrec'.")
        cfg["realPrec"] = realPrec
        
        # 检查英文单位表是不是可迭代元素。
        _checkAndShowParamTypeError("reprUnits_en", reprUnits_en, (str, list, tuple))
        # 如果不可迭代，抛出错误。
        if not reprUnits_en:
            raise ValueError(f"The paramter 'reprUnits_en' cannot be empty {type(reprUnits_en).__name__}.")
        # 否则存储配置。
        cfg["reprUnits_en"] = reprUnits_en
        
        # 检查中文单位表是不是可迭代元素。
        _checkAndShowParamTypeError("reprUnits_zh", reprUnits_zh, (str, list, tuple))
        # 如果不可迭代，抛出错误。
        if not reprUnits_zh:
            raise ValueError(f"The paramter 'reprUnits_zh' cannot be empty {type(reprUnits_zh).__name__}.")
        # 否则存储配置。
        cfg["reprUnits_zh"] = reprUnits_zh
        
        # 存储所有配置。
        self.config = cfg
        # 进行数值校准。
        self._calibrate()
    
    def _calibrate(self):
        # 获取base和exp的值。
        base, exp = self.getBase(), self.getExp()
        
        # 获取基数的对数的整数部分，如果基数是0则设置为0
        k = _math.floor(_math.log10(base)) if base != 0 else 0
        # 把k添加到指数里
        exp += k
        # 把基数通过乘除10移动到1<=x<10
        base /= 10 ** k
        
        # 获取精度。
        prec = self.getConfig("realPrec")
        # 把基数的最后一个精度位的下一位向下取整。
        base = _math.floor(base * 10 ** prec) / 10 ** prec
        
        # 把base和exp存储回去。
        self.base, self.exp = base, exp
    
    def getBase(self):
        """
        Get the base.
        
        Returns:
            float: The base.
        """
        
        # 如果存在“负数”标记，就返回基数的负数形式。
        if self.isNegative:
            return -self.base
        # 否则返回基数。
        return self.base
    
    def getExp(self):
        """
        Get the exponent.
        
        Returns:
            int: The exponent.
        """
        
        # 返回指数。
        return self.exp
    
    def getConfig(self, key):
        """
        Get the configs.
        
        Returns:
            dict: The configs.
        """
        
        # 如果没有指定键名，则返回整个配置字典。
        if not key:
            return self.config
        # 有指定键名，就返回那个键的值。
        return self.config.get(key)
    
    def _insertUnit(self, number, mul, units):
        # 如果数字小于单位进率的话，就直接返回。
        if number < mul:
            return str(number)
        # 不然，就遍历单位表。
        for unit in units:
            # 然后把数字除以进率。
            number = round(number / mul, self.getConfig("realPrec"))
            # 如果数字小于进率，即不需要继续除了，就返回数字和单位。
            if number < mul:
                return f"{number}{unit}"
        return f"{number}{units[-1]}"
    
    def parseString(self, *args, prec="default", expReprMode="comma", template="{0}e{1}", alwayUseTemplate=False):
        """
        Convert LargeNumber to a string
        
        Args:
            *args:
                When the constructor's argument list provides more (greater than or equal to three) non-keyword arguments,
                a TypeError will be thrown.
            prec (int or "default"):
                Keyword argument.
                The precision of the converted string.
                Defaults to the value of dispPrec.
            expReprMode ("comma" or "byUnit_en" or "byUnit_zh" or "power"):
                Keyword argument.
                Controls the display mode of the exponent.
                Defaults to "comma".
            template (str):
                Keyword argument.
                Controls the template for inserting the base and exponent when converting to a string.
                Defaults to "{0}e{1}".
            alwayUseTemplate (bool):
                Keyword argument.
                Controls whether to always use the template.
                Defaults to False.
        
        Returns:
            str: The converted string.
        
        Raises:
            TypeError:
                This error is raised when the number or position of the arguments is incorrect,
                or the argument type is wrong.
        """
        
        # 如果有无效参数，抛出错误。
        if args:
            _showArgsError(args)
        # 如果精度是"deafult"，就默认设置为配置字典里的显示精度。
        if prec == "default":
            prec = self.getConfig("dispPrec")
        # 检查类型。
        _checkAndShowParamTypeError("prec", prec, int)
        _checkAndShowParamTypeError("expReprMode", expReprMode, str)
        _checkAndShowParamTypeError("alwayUseTemplate", alwayUseTemplate, bool)
        
        # 取出base和exp。
        base, exp = self.getBase(), self.getExp()
        # 如果指数在-4到7之间，并且没有强制使用模板，则直接返回字符串形式。
        if -4 <= exp <= 7 and not alwayUseTemplate:
            return str(base * 10 ** exp)
        
        # 调整基数的精度。
        dispBase = str(round(base * 10 ** prec) / 10 ** prec)
        # 创建dispExp。
        dispExp = None
        
        # 如果指数大于等于1000万亿或者小于10，就强制使用power模式。
        if exp >= 1_000_000_000_000_000 or exp <= -10:
            expReprMode = "power"
        
        # 如果模式是comma，就直接用f-string设置显示的指数为逗号分割。
        if expReprMode ==  "comma":
            dispExp = f"{exp:,}"
        # 如果模式是byUnit_en，就把指数用英文单位表示。
        elif expReprMode ==  "byUnit_en":
            dispExp = self._insertUnit(exp, 1000, self.getConfig("reprUnits_en"))
        # 如果模式是byUnit_zh，就把指数用中文单位表示。
        elif expReprMode ==  "byUnit_zh":
            dispExp = self._insertUnit(exp, 10000, self.getConfig("reprUnits_zh"))
                # 如果模式是power，就把指数用指数表示。
        elif expReprMode ==  "power":
            dispExp = str(LargeNumber(exp, 0))
        # 否则抛出错误。
        else:
            raise ValueError(f"Invalid expReprMode: {repr(expReprMode)}")
        
        # 最后，把显示的基数和指数用特定模板插入。
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
        
        # 如果有无效参数，抛出错误。
        if args:
            _showArgsError(args)
        # 类型检查。
        _checkAndShowParamTypeError("mode", mode, str)
        
        # 使用默认模式。
        if mode == "default":
            # 如果基数为0，就直接返回0。
            if self.getBase() == 0:
                return 0
            # 如果指数在-4到7之间，就直接返回计算结果。
            if -4 <= self.getExp() <= 7:
                return int(self.getBase() * 10 ** self.getExp())
            # 如果指数超出常规范围，直接计算可能会导致浮点数精度误差累积，所以使用字符串拼接的方法来处理。
            # 计算指数与精度的差。
            expSub = self.getExp() - self.getConfig("realPrec")
            # 储存基数去掉小数点之后的字符串
            base = str(self.getBase()).replace(".", "")
            # 计算原来的基数有多少位小数，然后让expSub自减它。
            expSub -= len(base) - 1
            # 然后返回结果。
            return int(base + "0" * expSub)
        # 使用power模式。
        if mode == "power" or _re.search("^power\\s+\\d{1,6}$", mode):
            # 如果未指定指数，默认为128。
            if mode == "power":
                mode = "power 128"
            # 提取指定的指数。
            power = int(_re.split("\\s+", mode)[1])
            # 如果实际指数大于限制的指数，抛出错误。
            if self.getExp() > power:
                raise OverflowError(f"The exponent exceeds the allowed upper limit: {power}")
            # 否则，按原来转换。
            return self.parseInt(mode="default")
        
        # 如果模式类型未知，抛出错误。
        raise ValueError(f"Invalid mode: {repr(mode)}")
    
    def __str__(self):
        # 直接调用默认的转换行为。
        return self.parseString()
    
    def __bool__(self):
        # 如果是0，就返回False，不然返回True。
        if self.getBase() == 0 and self.getExp() == 0:
            return False
        return True
    
    def __int__(self):
        # 调用默认的转换行为。
        return self.parseInt()
    
    def __repr__(self):
        # 用模板来调用字符串转换。
        return self.parseString(template="LargeNumber({0}, {1})", alwayUseTemplate=True)
    
    def __neg__(self):
        # 对基数取反在返回。
        return LargeNumber(-self.getBase(), self.getExp())
    
    def __pos__(self):
        # 返回自己
        return self
    
    def __abs__(self):
        # 返回基数的绝对值。
        return LargeNumber(abs(self.getBase()), self.getExp())
    
    def __eq__(self, other):
        # 类型检查。
        other = self._parseLargeNumberOrShowError(other)
        # 如果基数和指数都相等，就相等，否则不相等。
        if (self.getBase() == other.base) and (self.getExp() == other.exp):
            return True
        return False
    
    def __ne__(self, other):
        # 对相等检查的结果取反。
        return not self == other
    
    def __lt__(self, other):
        # 类型检查。
        other = self._parseLargeNumberOrShowError(other)
        # 指数不相等，指数小的就小。
        if self.getExp() != other.exp:
            return self.getExp() < other.exp
        # 指数不相等，基数小的就小。
        return self.getBase() < other.base
    
    def __le__(self, other):
        # 检查是否较小或相等。
        return self < other or self == other
    
    def __gt__(self, other):
        # 对小于等于的检查取反。
        return not self <= other
    
    def __ge__(self, other):
        # 对小于的检查取反。
        return not self < other
    
    def __add__(self, other):
        # 类型检查。
        other = self._parseLargeNumberOrShowError(other)
        
        # 如果相等，就直接基数相加。
        if self == other:
            return self.getBase() + other.base, self.getExp()
        
        # 初始化big和small。
        big, small = 0, 0
        # 把较大的存储在big里，较小的存储在small里。
        if self < other:
            big, small = other, self
        else:
            big, small = self, other
        
        # 如果在大的数上增加小的数时，精度太低，无影响，就直接返回大的就好。
        if big.getExp() - small.getExp() > big.getConfig("realPrec"):
            return big
        
        # 以小的数的指数为基准，获取两个数的基数。
        expSub = big.getExp() - small.getExp()
        bigBase = big.getBase * 10 ** expSub()
        smallBase = small.getBase()
        
        # 返回两个基数相加，同一个指数。
        return LargeNumber(bigBase + smallBase, small.getExp())
    
    def __radd__(self, other):
        # 调用加法行为。
        return self + other
    
    def __iadd__(self, other):
        # 调用加法行为。
        return self + other
    
    def __sub__(self, other):
        # 用self加other的取反。
        return self + -other
    
    def __rsub__(self, other):
        # 调用减法行为。
        return other + -self
    
    def __isub__(self, other):
        # 调用减法行为。
        return self - other
    
    def __mul__(self, other):
        # 类型检查。
        other = self._parseLargeNumberOrShowError(other)
        # 返回基数相乘，指数相加。
        return LargeNumber(
            self.getBase() * other.getBase(),
            self.getExp() + other.getExp()
        )
    
    def __rmul__(self, other):
        # 调用乘法行为。
        return self * other
    
    def __imul__(self, other):
        # 调用乘法行为。
        return self * other
    
    def __truediv__(self, other):
        # 类型检查。
        other = self._parseLargeNumberOrShowError(other)
        # 如果除数是0，抛出错误。
        if other == 0:
            raise ZeroDivisionError(f"{repr(self)} cannot be divided by 0.")
        # 返回基数相除，指数相减。
        return LargeNumber(self.getBase() / other.base, self.getExp() - other.exp)
    
    def __rtruediv__(self, other):
        # 调用除法行为。
        return other / self
    
    def __itruediv__(self, other):
        # 调用除法行为。
        return self / other

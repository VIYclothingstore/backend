from enum import Enum


class Gender(Enum):
    MALE = "Чоловіки"
    FEMALE = "Жінки"

    @classmethod
    def choices(cls):
        return [
            (cls.MALE.value, "Чоловіки"),
            (cls.FEMALE.value, "Жінки"),
        ]


class Category(Enum):
    SHOES = "Кросівки"
    TSHIRTS = "Футболки"
    SHORTS = "Шорти"
    TROUSERS = "Штани"
    SWEATSHIRTS = "Світшоти"

    @classmethod
    def choices(cls):
        return [
            (cls.SHOES.value, "Кросівки"),
            (cls.TSHIRTS.value, "Футболки"),
            (cls.SHORTS.value, "Шорти"),
            (cls.TROUSERS.value, "Штани"),
            (cls.SWEATSHIRTS.value, "Світшоти"),
        ]


class Color(Enum):
    BLACK = "Чорний"
    WHITE = "Білий"
    BLUE = "Синій"
    COLORFUL = "Різнокольорові"

    @classmethod
    def choices(cls):
        return [
            (cls.BLACK.value, "Чорний"),
            (cls.WHITE.value, "Білий"),
            (cls.BLUE.value, "Синій"),
            (cls.COLORFUL.value, "Різнокольорові"),
        ]


class Size(Enum):
    # Shoe sizes
    SIZE_36 = "36"
    SIZE_37 = "37"
    SIZE_38 = "38"
    SIZE_39 = "39"
    SIZE_40 = "40"
    SIZE_41 = "41"
    SIZE_42 = "42"
    SIZE_43 = "43"
    SIZE_44 = "44"
    SIZE_45 = "45"

    # Clothing sizes
    SMALL = "S"
    MEDIUM = "M"
    LARGE = "L"
    XLARGE = "XL"
    XXLARGE = "XXL"

    @classmethod
    def choices(cls):
        return [
            (cls.SIZE_36.value, "36"),
            (cls.SIZE_37.value, "37"),
            (cls.SIZE_38.value, "38"),
            (cls.SIZE_39.value, "39"),
            (cls.SIZE_40.value, "40"),
            (cls.SIZE_41.value, "41"),
            (cls.SIZE_42.value, "42"),
            (cls.SIZE_43.value, "43"),
            (cls.SIZE_44.value, "44"),
            (cls.SIZE_45.value, "45"),
            (cls.SMALL.value, "S"),
            (cls.MEDIUM.value, "M"),
            (cls.LARGE.value, "L"),
            (cls.XLARGE.value, "XL"),
            (cls.XXLARGE.value, "XXL"),
        ]

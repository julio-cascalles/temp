from modelos.util.sinalizador import Sinalizador


class Midia(Sinalizador):
    WHATSAPP    =   1
    FACEBOOK    =   2
    INSTAGRAM   =   4
    TIKTOK      =   8
    X_TWITTER   =  16
    LINKEDIN    =  32

    @classmethod
    def item_enum(cls, name: str):
        if name in ('X', "TWITTER"):
            return Midia.X_TWITTER
        return super().item_enum(name)

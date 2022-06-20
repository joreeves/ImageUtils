
class NORMALIZATION():
    """
    Colorspace base class
    """
    def __init__(self):
        self.reverse = reverse
        self.__color__(**kwargs) # INIT COLOR SPECIFIC SETTINGS

    def __color__(self):
        return

    def color_in(self,img):
        if self.reverse:
            return self.__backward__(img)
        else:
            return self.__forward__(img)

    def color_out(self,img):
        if self.reverse:
            return self.__forward__(img)
        else:
            return self.__backward__(img)

    def __forward__(self,img):
        # OVERLOAD THIS
        return img

    def __backward__(self, img):
        # OVERLOAD THIS
        return img

class Sounds(object):
    def __init__(self, volume, ilosc_stopni_glosnosci):
        self.volume = volume
        self.ilosc_stopni_glosnosci = ilosc_stopni_glosnosci
        self.sounds = []
    def add_sound(self, sound):
        self.sounds.append(sound)
        self.actualize()
    def set_volume(self, volume):
        self.volume = volume
        self.actualize()
    def get_volume(self):
        return self.volume
    def set_down_volume(self):
        if self.volume > 0:
            self.volume -= 1
            self.actualize()
    def set_up_volume(self):
        if self.volume < self.ilosc_stopni_glosnosci:
            self.volume += 1
            self.actualize()
    def actualize(self):
        for s in self.sounds:
            s.set_volume(self.volume / float(self.ilosc_stopni_glosnosci))
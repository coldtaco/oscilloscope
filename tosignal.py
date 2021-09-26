from scipy.io import wavfile
class toSignal:
    def __init__(self, source, dest, image = True ):
        self.dest = dest
        if image:
            pass
        else:
            if source.isdigit():
                self.source = int(source)

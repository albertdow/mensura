from mensura import Converter

if __name__ == "__main__":
    converter = Converter()
    print(converter.convert(1, "kilometre", "metre"))
    print(converter.convert(1, "kilometre", "foot"))
    print(converter.convert(2, "metre", "inch"))

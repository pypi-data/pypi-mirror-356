import os
import json

class PhonemeConverter:
    def __init__(self, default_stress="1"):
        self.default_stress = default_stress

        # 完整版 IPA -> ARPAbet 映射
        self.ipa2arpa = {
            # 元音（单元音）
            "i": "iy",  "ɪ": "ih",  "e": "ey",   "ɛ": "eh",
            "æ": "ae",  "ɑ": "aa",  "ɔ": "ao",   "o": "ow",
            "ʊ": "uh",  "u": "uw",  "ʌ": "ah",   "ə": "ax",
            "ɝ": "er",  "ɚ": "er",

            # 双元音
            "aɪ": "ay", "aʊ": "aw", "ɔɪ": "oy", "eɪ": "ey", "oʊ": "ow",

            # 辅音
            "p": "p",  "b": "b",   "t": "t",   "d": "d",   "k": "k",
            "g": "g",  "tʃ": "ch", "dʒ": "jh", "f": "f",   "v": "v",
            "θ": "th", "ð": "dh",  "s": "s",   "z": "z",   "ʃ": "sh",
            "ʒ": "zh", "h": "hh",  "m": "m",   "n": "n",   "ŋ": "ng",
            "l": "l",  "r": "r",   "j": "y",   "w": "w",

            # 符号（重读、次重读）
            "ˈ": "",   # 重读符号
            "ˌ": "",   # 次重读符号
            " ": " ",
        }

        # 反向映射：ARPAbet -> IPA，只保留第一个对应
        self.arpa2ipa = {}
        for k, v in self.ipa2arpa.items():
            if v and v not in self.arpa2ipa:
                self.arpa2ipa[v] = k

        # ARPAbet元音集合，用于加压力数字
        self.vowels = {
            "iy", "ih", "ey", "eh", "ae", "aa", "ao", "ow", "uh", "uw",
            "ah", "ax", "er", "ay", "aw", "oy"
        }

    def ipa_to_arpa(self, ipa: str) -> str:
        result = []
        i = 0
        apply_stress = False

        while i < len(ipa):
            if ipa[i] == 'ˈ':
                apply_stress = True
                i += 1
                continue
            if ipa[i] == 'ˌ':
                i += 1
                continue

            # 先匹配双字符音素
            if i + 1 < len(ipa):
                pair = ipa[i:i+2]
                if pair in self.ipa2arpa:
                    arpa = self.ipa2arpa[pair]
                    i += 2
                else:
                    arpa = self.ipa2arpa.get(ipa[i], ipa[i])
                    i += 1
            else:
                arpa = self.ipa2arpa.get(ipa[i], ipa[i])
                i += 1

            if not arpa:
                continue

            if arpa in self.vowels:
                stress = self.default_stress if apply_stress else "0"
                result.append(f"{arpa}{stress}")
            else:
                result.append(arpa)

            apply_stress = False

        return " ".join(result).upper()

    def arpa_to_ipa(self, arpa: str) -> str:
        tokens = arpa.strip().split()
        result = []

        for token in tokens:
            base = ''.join(filter(str.isalpha, token)).lower()
            ipa = self.arpa2ipa.get(base, base)
            result.append(ipa)

        return ' '.join(result)

    def convert(self, text: str, mode: str = "ipa2arpa") -> str:
        if mode == "ipa2arpa":
            return self.ipa_to_arpa(text)
        elif mode == "arpa2ipa":
            return self.arpa_to_ipa(text)
        else:
            raise ValueError("mode must be 'ipa2arpa' or 'arpa2ipa'")

    def from_file(self, filepath: str, mode="ipa2arpa") -> dict:
        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        results = {line.strip(): self.convert(line.strip(), mode) for line in lines}
        return results

    def to_file(self, input_path: str, output_path: str, mode="ipa2arpa"):
        results = self.from_file(input_path, mode)
        with open(output_path, 'w', encoding='utf-8') as f:
            for original, converted in results.items():
                f.write(f"{original} => {converted}\n")



if __name__ == "__main__":
    conv = PhonemeConverter()
    print(conv.ipa_to_arpa("ˈkæt"))          # k ae1 t
    print(conv.ipa_to_arpa("mɪsˈɑki"))       # m ih0 s aa1 k iy0
    print(conv.arpa_to_ipa("k ae1 t"))       # kæt
    print(conv.arpa_to_ipa("m ih0 s aa1 k iy0")) # misaki
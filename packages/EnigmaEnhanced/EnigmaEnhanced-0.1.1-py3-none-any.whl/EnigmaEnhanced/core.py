import os
import json
import base64
import hashlib
import secrets
from typing import List

class EnigmaEnhanced:
    def __init__(self):
        self.key = None
        self.print_help()

    def print_help(self):
        print("""
        === 增强版恩尼格玛密码机 ===
        所有命令以斜杠 (/) 开头，以避免与普通文本冲突
        
        命令:
          /genkey [filename] - 生成并导出密钥到文件（默认: enigma_key.json）
          /loadkey <filename> - 从文件加载密钥
          /delkey - 删除当前密钥
          /help - 显示帮助
          /exit - 退出程序
        
        加密: 输入任何非命令文本
        解密: 输入以"ENC:"开头的文本

        密钥增强: 使用SHA-256哈希增强转子配置
        Unicode支持: 所有字符均可加密
        密钥检测: 当密钥不匹配时会明确提示


        === Enhanced Enigma Cipher Machine ===
        All commands start with a slash (/) to avoid conflicts with regular text

        Commands:
        /genkey [filename] - Generate and export key to file (default: enigma_key.json)
        /loadkey <filename> - Load key from file
        /delkey - Delete current key
        /help - Show help
        /exit - Exit program

        Encryption: Enter any non-command text
        Decryption: Enter text starting with "ENC:"

        Key Enhancement: Rotor configuration strengthened using SHA-256 hash
        Unicode Support: All characters can be encrypted
        Key Detection: Explicit prompt when key mismatch occurs
        """)

    def _derive_key(self, seed: bytes, length: int) -> bytes:
        """使用HKDF-like方法派生密钥 Derive keys using an HKDF-like method"""
        key = b''
        salt = b'enigma_salt'
        counter = 0
        while len(key) < length:
            key += hashlib.sha256(salt + seed + counter.to_bytes(4, 'big')).digest()
            counter += 1
        return key[:length]

    def generate_key(self, filename="enigma_key.json"):
        # 生成随机种子 Generate a random seed
        seed = secrets.token_bytes(32)
        
        # 派生密钥 Derive keys
        key_material = self._derive_key(seed, 768)  # 256 * 3个转子 256 * 3 rotors
        
        # 构建转子配置 Build rotor configuration
        rotors = []
        for i in range(3):
            rotor = list(range(256))
            # 使用派生密钥打乱转子 Scramble rotors using derived keys
            for j in range(256):
                # 确保索引在0-255范围内 Ensure the index is within the 0-255 range
                swap_index = key_material[i*256 + j] % 256
                rotor[j], rotor[swap_index] = rotor[swap_index], rotor[j]
            rotors.append(rotor)
        
        # 构建反射器 Build reflector
        reflector = list(range(256))
        for i in range(128):
            j = 255 - i
            reflector[i], reflector[j] = reflector[j], reflector[i]
        
        # 保存密钥 Save key
        key_data = {
            "seed": base64.b64encode(seed).decode(),
            "rotors": rotors,
            "reflector": reflector
        }
        
        with open(filename, 'w') as f:
            json.dump(key_data, f)
        
        self.key = key_data
        print(f"密钥已生成并保存到 {filename} The key has been generated and saved to {filename}")
        return key_data

    def load_key(self, filename):
        try:
            with open(filename, 'r') as f:
                self.key = json.load(f)
            print(f"密钥已从 {filename} 加载 Key has been loaded from {filename}")
            return True
        except Exception as e:
            print(f"错误 ERROR: {e}")
            return False

    def delete_key(self):
        self.key = None
        print("密钥已删除 Key has been deleted")

    def _process_byte(self, byte_val: int, rotors: List[List[int]], reflector: List[int]) -> int:
        """处理单个字节的加密/解密 Process byte-wise encryption/decryption"""
        # 转子处理Rotor processing
        for rotor in rotors:
            byte_val = rotor[byte_val]
        byte_val = reflector[byte_val]
        for rotor in reversed(rotors):
            # 查找反向映射 Find reverse mapping
            byte_val = rotor.index(byte_val)
        return byte_val

    def encrypt(self, text: str) -> str:
        if not self.key:
            print("错误: 没有可用密钥 ERROR: No key available")
            return None
        
        # 获取转子配置 Retrieve rotor configuration
        rotors = self.key["rotors"]
        reflector = self.key["reflector"]
        
        # 将文本编码为UTF-8字节序列 Encode text to UTF-8 byte sequence
        text_bytes = text.encode('utf-8')
        
        # 处理每个字节 Process each byte
        processed_bytes = []
        for byte_val in text_bytes:
            processed_byte = self._process_byte(byte_val, rotors, reflector)
            processed_bytes.append(processed_byte)
        
        # 添加增强：使用派生密钥混淆结果 Enhancement: Obfuscate with derived keys
        seed = base64.b64decode(self.key["seed"])
        key_material = self._derive_key(seed, len(processed_bytes))
        
        # 混淆处理 Obfuscation processing
        encrypted = []
        for i, byte_val in enumerate(processed_bytes):
            encrypted.append(byte_val ^ key_material[i])
        
        # Base64编码 Base64 encoding
        encrypted_bytes = bytes(encrypted)
        return "ENC:" + base64.b64encode(encrypted_bytes).decode()

    def decrypt(self, text: str) -> str:
        if not text.startswith("ENC:"):
            print("错误: 无效的密文格式 ERROR: Invalid ciphertext format")
            return None
        
        if not self.key:
            print("错误: 没有可用密钥 ERROR: No key available")
            return None
            
        try:
            # Base64解码 Base64 decoding
            encrypted_bytes = base64.b64decode(text[4:])
            
            # 获取密钥材料 Retrieve key material
            seed = base64.b64decode(self.key["seed"])
            key_material = self._derive_key(seed, len(encrypted_bytes))
            
            # 去混淆处理 De-obfuscation processing
            decrypted = []
            for i, byte_val in enumerate(encrypted_bytes):
                decrypted.append(byte_val ^ key_material[i])
            
            # 获取转子配置 Retrieve rotor configuration
            rotors = self.key["rotors"]
            reflector = self.key["reflector"]
            
            # 恩尼格玛解密 Enigma decryption
            result_bytes = []
            for byte_val in decrypted:
                try:
                    result_byte = self._process_byte(byte_val, rotors, reflector)
                    result_bytes.append(result_byte)
                except ValueError:
                    # 转子处理失败，可能是密钥不匹配 Rotor processing failed, possible key mismatch
                    return "解密失败：密钥不匹配 Decryption failed: Key mismatch"
            
            # 尝试将字节解码为字符串 Attempt byte-to-string decoding
            try:
                return bytes(result_bytes).decode('utf-8')
            except UnicodeDecodeError:
                # 解码失败，可能是密钥不匹配 Decoding failed, possible key mismatch
                return "解密失败：密钥不匹配或密文损坏 Decryption failed: Key mismatch OR ciphertext corruption"
                
        except Exception as e:
            return f"解密失败 Decryption failed：{str(e)}"
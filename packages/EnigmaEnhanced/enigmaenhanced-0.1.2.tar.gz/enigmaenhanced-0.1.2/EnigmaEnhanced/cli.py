from . import __version__
from .core import EnigmaEnhanced
import argparse
import sys

def interactive_mode():
    """交互式命令行界面 Interactive command line interface"""
    enigma = EnigmaEnhanced()
    
    while True:
        try:
            user_input = input("\n> ").strip()
        except EOFError:
            print("\n退出程序 Exit program")
            break
        except KeyboardInterrupt:
            print("\n退出程序 Exit program")
            break
            
        if not user_input:
            continue
        
        # 命令处理 - 所有命令以斜杠 (/) 开头
        if user_input.startswith("/"):
            # 移除斜杠并分割命令
            command_parts = user_input[1:].split(maxsplit=1)
            command = command_parts[0]
            args = command_parts[1] if len(command_parts) > 1 else ""
            
            if command == "genkey":
                filename = args if args else "enigma_key.json"
                enigma.generate_key(filename)
            
            elif command == "loadkey":
                if not args:
                    print("请指定文件名 Please specify filename")
                    continue
                enigma.load_key(args)
            
            elif command == "delkey":
                enigma.delete_key()
            
            elif command == "help":
                enigma.print_help()
                
            elif command == "exit":
                print("退出程序 Exit program")
                break
                
            else:
                print(f"未知命令 Unknown command: /{command}")
        
        # 解密处理
        elif user_input.startswith("ENC:"):
            if enigma.key is None:
                print("错误: 没有可用密钥 ERROR: No key available")
                continue
            result = enigma.decrypt(user_input)
            if result:
                if result.startswith("解密失败 Decryption failed："):
                    print(result)
                else:
                    print(f"解密结果 Decryption result: {result}")
        
        # 加密处理
        else:
            if enigma.key is None:
                print("错误: 没有可用密钥 ERROR: No key available")
                continue
            result = enigma.encrypt(user_input)
            if result:
                print(f"加密结果 Encryption result: {result}")

def batch_mode(args):
    """批处理模式 Batch processing mode"""
    enigma = EnigmaEnhanced()
    
    if not enigma.load_key(args.keyfile):
        print(f"无法加载密钥文件: {args.keyfile}")
        return
    
    if args.encrypt:
        result = enigma.encrypt(args.encrypt)
        if result:
            print(f"加密结果: {result}")
    
    elif args.decrypt:
        if not args.decrypt.startswith("ENC:"):
            print("错误: 密文必须以 'ENC:' 开头")
            return
        result = enigma.decrypt(args.decrypt)
        if result:
            if result.startswith("解密失败"):
                print(f"错误: {result}")
            else:
                print(f"解密结果: {result}")

def main():
    parser = argparse.ArgumentParser(
        description="增强版恩尼格玛密码机 | Enhanced Enigma Cipher Machine",
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=False  # 禁用默认的help选项，我们将自定义处理
    )
    
    # 添加版本参数
    parser.add_argument(
        '-v', '--version',
        action='version',
        version=f'EnigmaEnhanced {__version__}',
        help="显示程序版本号 | Show program version"
    )
    
    # 添加帮助参数
    parser.add_argument(
        '-h', '--help',
        action='help',
        default=argparse.SUPPRESS,
        help='显示帮助信息 | Show this help message and exit'
    )
    
    # 批处理模式参数
    parser.add_argument(
        '--encrypt', 
        metavar="TEXT",
        help="要加密的文本 | Text to encrypt"
    )
    parser.add_argument(
        '--decrypt', 
        metavar="CIPHERTEXT",
        help="要解密的文本（必须以 'ENC:' 开头） | Text to decrypt (must start with 'ENC:')"
    )
    parser.add_argument(
        '--keyfile', 
        default="enigma_key.json",
        help="密钥文件路径（默认: enigma_key.json） | Key file path (default: enigma_key.json)"
    )
    
    # 解析参数
    args = parser.parse_args()
    
    # 如果有批处理参数，则进入批处理模式
    if args.encrypt or args.decrypt:
        batch_mode(args)
    # 否则进入交互模式
    else:
        interactive_mode()

if __name__ == "__main__":
    main()
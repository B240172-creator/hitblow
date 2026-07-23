"""ゲームの進行（入力・表示・ループ）。"""

import os
from .core import judge


def input_secret(digits):
    """プレイヤーが秘密の数字を入力する。"""
    while True:
        secret = input(f"{digits}桁の重複のない数字を入力 > ").strip()

        if (
            len(secret) == digits
            and secret.isdigit()
            and len(set(secret)) == digits
        ):
            return secret

        print(f"{digits}桁の重複のない数字を入力してください。")


def clear_screen():
    """画面をクリアする"""
    os.system("cls")  # Windows
    # Mac/Linuxの場合は os.system("clear")


def play():
    while True:
        digits = input("桁数(3~6)を選んでね > ").strip()

        if digits.isdigit():
            digits = int(digits)
            if 3 <= digits <= 6:
                break

        print("3～6の数字を入力してね")

    # プレイヤー1の秘密
    print("=== プレイヤー1 ===")
    secret1 = input_secret(digits)
    clear_screen()

    # プレイヤー2の秘密
    print("=== プレイヤー2 ===")
    secret2 = input_secret(digits)
    clear_screen()

    print(f"Hit & Blow（{digits}桁・重複なし）")

    tries1 = 0
    tries2 = 0
    player = 1

    while True:
        print(f"\n===== プレイヤー{player}の番 =====")

        guess = input("予想 > ").strip()

        # 入力チェック
        if (
            len(guess) != digits
            or not guess.isdigit()
            or len(set(guess)) != digits
        ):
            print(f"{digits}桁の重複のない数字を入力してください。")
            continue

        # 判定
        if player == 1:
            tries1 += 1
            hit, blow = judge(secret2, guess)
        else:
            tries2 += 1
            hit, blow = judge(secret1, guess)

        print(f"Hit = {hit}  Blow = {blow}")

        # 勝利判定
        if hit == digits:
            print("\n====================")
            if player == 1:
                print(f"🎉 プレイヤー1の勝ち！")
                print(f"試行回数：{tries1}回")
                print(f"プレイヤー2の秘密の数字：{secret2}")
            else:
                print(f"🎉 プレイヤー2の勝ち！")
                print(f"試行回数：{tries2}回")
                print(f"プレイヤー1の秘密の数字：{secret1}")
            print("====================")
            break

        # プレイヤー交代
        player = 2 if player == 1 else 1



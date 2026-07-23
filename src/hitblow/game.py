"""ゲームの進行（入力・表示・ループ）。"""

import os
from getpass import getpass

from .core import judge
from .item import reveal, change_secret


def input_secret(digits):
    """プレイヤーが秘密の数字を入力する。"""
    while True:
        secret = getpass(
            f"{digits}桁の重複のない数字を入力 ※数字は非表示にしてます > "
        ).strip()

        if (
            len(secret) == digits
            and secret.isdigit()
            and len(set(secret)) == digits
        ):
            return secret

        print(f"{digits}桁の重複のない数字を入力してください。※数字は非表示にしてます")


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
    print("アイテム：")
    print(" reveal : 相手の数字を1つ開示（1回のみ）")
    print(" change : 自分の数字を1つ変更（1回のみ）")

    tries1 = 0
    tries2 = 0
    player = 1

    # アイテム使用フラグ
    p1_reveal = False
    p2_reveal = False
    p1_change = False
    p2_change = False

    while True:
        print(f"\n===== プレイヤー{player}の番 =====")

        guess = input("予想（reveal / change も使用可能）> ").strip()

        # ==========================
        # reveal アイテム
        # ==========================
        if guess.lower() == "reveal":

            if player == 1:
                if p1_reveal:
                    print("このアイテムはもう使っています。")
                else:
                    idx, num = reveal(secret2)
                    print(f"相手の{idx+1}桁目は「{num}」です。")
                    p1_reveal = True
            else:
                if p2_reveal:
                    print("このアイテムはもう使っています。")
                else:
                    idx, num = reveal(secret1)
                    print(f"相手の{idx+1}桁目は「{num}」です。")
                    p2_reveal = True

            continue

        # ==========================
        # change アイテム
        # ==========================
        if guess.lower() == "change":

            if player == 1:
                if p1_change:
                    print("このアイテムはもう使っています。")
                else:
                    secret1 = change_secret(secret1)
                    print("自分の秘密の数字を変更しました。")
                    p1_change = True
            else:
                if p2_change:
                    print("このアイテムはもう使っています。")
                else:
                    secret2 = change_secret(secret2)
                    print("自分の秘密の数字を変更しました。")
                    p2_change = True

            continue

        # ==========================
        # 入力チェック
        # ==========================
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
                print("🎉 プレイヤー1の勝ち！")
                print(f"試行回数：{tries1}回")
            else:
                print("🎉 プレイヤー2の勝ち！")
                print(f"試行回数：{tries2}回")

            print(f"プレイヤー1の秘密の数字：{secret1}")
            print(f"プレイヤー2の秘密の数字：{secret2}")
            print("====================")
            break

        input("Enterキーを押して交代してください...")

        # プレイヤー交代
        player = 2 if player == 1 else 1
import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk


class CardCountingApp:
    def setup_language(self):
        self.languages = {
            'en': {
                'title': "Leroy's BlackJack Counter",
                'running_count': "Running Count:",
                'cards_played': "Cards Played:",
                'reset': "Reset",
                'exit': "Exit",
                'select_language': "Select Language",
                'decks': "Decks",
                'base_bet': "Base Bet",
                'true_count': "True Count",
                'cards_left': "Cards Left:",
                'suggested_bet': "Suggested Bet:",
                'entered_cards': "Entered Cards:",
                'delete': "Delete",
                'language': "Language"
            },
            'zh': {
                'title': "Leroy 21點計數器",
                'running_count': "目前計數：",
                'cards_played': "已玩牌數：",
                'reset': "重置",
                'exit': "退出",
                'select_language': "選擇語言",
                'decks': "副牌數",
                'base_bet': "基礎注碼",
                'true_count': "真實計數",
                'cards_left': "剩餘牌數:",
                'suggested_bet': "建議下注:",
                'entered_cards': "輸入的牌:",
                'delete': "刪除",
                'language': "語言"
            }
        }
        self.current_language = 'en'
        self.language_strings = self.languages[self.current_language]

    def update_language(self, event=None):
        lang = self.language_var.get()
        # 轉換顯示文字為語言代碼
        lang_map = {"English": "en", "中文": "zh"}
        if lang in lang_map:
            lang = lang_map[lang]
        
        self.current_language = lang
        self.language_strings = self.languages[lang]
        self.master.title(self.language_strings['title'])
        self.update_labels()

    def update_labels(self):
        try:
            # 更新所有標籤文字
            self.cards_left_label.config(text=f"{self.language_strings['cards_left']} {self.total_cards - self.cards_played}")
            self.bet_suggest_label.config(text=f"{self.language_strings['suggested_bet']} {self.bet_unit}")
            self.cards_display.config(text=f"{self.language_strings['entered_cards']} {self.format_displayed_cards()}")
            self.deck_label.config(text=self.language_strings['decks'])
            self.bet_label.config(text=self.language_strings['base_bet'])
            self.language_label.config(text=self.language_strings['language'])
            self.count_title_label.config(text=self.language_strings['running_count'])
            self.true_count_title_label.config(text=self.language_strings['true_count'])
            self.delete_button.config(text=self.language_strings['delete'])
            self.reset_button.config(text=self.language_strings['reset'])
        except AttributeError:
            pass  # Labels might not be initialized yet
    
    def __init__(self, master):
        self.master = master
        
        self.setup_language()
        self.master.title(self.language_strings['title'])

        self.master.geometry("700x600")
        
        # 設定主題色
        self.BG_DARK = "#000000"      # 純黑背景
        self.BG_LIGHT = "#1a1a1a"     # 深灰背景
        self.TEXT_COLOR = "#ffffff"    # 白色文字
        self.ACCENT_COLOR = "#ffffff"  # 白色強調
        self.INFO_COLOR = "#ffffff"    # 資訊顯示顏色
        self.HIGHLIGHT_COLOR = "#ffffff" # 高亮顏色
        self.POSITIVE_COLOR = "#00ff00" # 綠色 (正數)
        self.NEGATIVE_COLOR = "#ff0000" # 紅色 (負數)
        
        self.master.configure(bg=self.BG_DARK)
        
        # 設定樣式
        self.setup_styles()
        
        self.running_count = 0
        self.cards_played = 0
        self.bet_unit = 100
        self.num_decks = 8
        self.total_cards = self.num_decks * 52
        self.entered_cards = []

        # 創建並放置Logo
        self.create_logo()
        
        # 創建其他元件
        self.create_widgets()

    def setup_styles(self):
        style = ttk.Style()
        
        # 設定按鈕樣式 - 白色按鈕，黑色文字
        style.configure('Card.TButton',
                       padding=(5, 2),
                       background='white',
                       foreground='black',  
                       font=('Arial', 12, 'bold'))
        
        # 設定控制按鈕樣式
        style.configure('Control.TButton',
                       padding=(10, 5),
                       background='white',
                       foreground='black',  
                       font=('Arial', 11, 'bold'))
                       
        # 設定下拉選單樣式
        style.configure('TCombobox',
                       background=self.BG_LIGHT,
                       foreground='black',  
                       fieldbackground='white')  

    def create_logo(self):
        # Logo區域
        logo_frame = tk.Frame(self.master, bg=self.BG_DARK)
        logo_frame.pack(pady=10)
        
        try:
            # 載入logo圖片
            logo_img = Image.open("logo.png")
            # 調整大小
            logo_img = logo_img.resize((150, 100), Image.Resampling.LANCZOS)
            self.logo_photo = ImageTk.PhotoImage(logo_img)
            
            # 創建並放置logo標籤
            logo_label = tk.Label(logo_frame, image=self.logo_photo, bg=self.BG_DARK)
            logo_label.pack()
        except Exception as e:
            print(f"Logo載入失敗: {e}")

    def create_widgets(self):
        # 上方設置區域
        settings_frame = tk.Frame(self.master, bg=self.BG_DARK)
        settings_frame.pack(pady=5, padx=10, fill='x')
        
        # 副牌數選擇
        deck_frame = tk.Frame(settings_frame, bg=self.BG_DARK)
        deck_frame.pack(side=tk.LEFT, padx=5)
        self.deck_label = tk.Label(deck_frame, text=self.language_strings['decks'], font=('Arial', 10, 'bold'),
                fg=self.TEXT_COLOR, bg=self.BG_DARK)
        self.deck_label.pack()
        self.deck_var = tk.StringVar(value="8")
        self.deck_dropdown = ttk.Combobox(deck_frame, textvariable=self.deck_var,
                                        values=[str(i) for i in range(1, 9)],
                                        state="readonly", width=3)
        self.deck_dropdown.pack()
        self.deck_dropdown.bind("<<ComboboxSelected>>", self.update_decks)

        # 語言選擇
        language_frame = tk.Frame(settings_frame, bg=self.BG_DARK)
        language_frame.pack(side=tk.LEFT, padx=5)
        self.language_label = tk.Label(language_frame, text=self.language_strings['language'], font=('Arial', 10, 'bold'),
                fg=self.TEXT_COLOR, bg=self.BG_DARK)
        self.language_label.pack()
        self.language_var = tk.StringVar(value="English")
        self.language_dropdown = ttk.Combobox(language_frame, textvariable=self.language_var,
                                        values=["English", "中文"],
                                        state="readonly", width=7)
        self.language_dropdown.pack()
        self.language_dropdown.bind("<<ComboboxSelected>>", self.update_language)

        # 下注單位
        bet_frame = tk.Frame(settings_frame, bg=self.BG_DARK)
        bet_frame.pack(side=tk.RIGHT, padx=5)
        self.bet_label = tk.Label(bet_frame, text=self.language_strings['base_bet'], font=('Arial', 10, 'bold'),
                fg=self.TEXT_COLOR, bg=self.BG_DARK)
        self.bet_label.pack()
        self.bet_entry = ttk.Entry(bet_frame, width=6)
        self.bet_entry.insert(0, "100")
        self.bet_entry.pack()

        # Count顯示區
        count_frame = tk.Frame(self.master, bg=self.BG_LIGHT, pady=10,
                             highlightbackground=self.TEXT_COLOR,
                             highlightthickness=1)
        count_frame.pack(fill='x', pady=5, padx=10)
        
        # Running Count
        self.count_title_label = tk.Label(count_frame, text=self.language_strings['running_count'], font=('Arial', 12, 'bold'),
                fg=self.TEXT_COLOR, bg=self.BG_LIGHT)
        self.count_title_label.pack()
        self.count_label = tk.Label(count_frame, text="0", font=('Arial', 24, 'bold'),
                                  fg=self.ACCENT_COLOR, bg=self.BG_LIGHT)
        self.count_label.pack()
        
        # True Count
        self.true_count_title_label = tk.Label(count_frame, text=self.language_strings['true_count'], font=('Arial', 12, 'bold'),
                fg=self.TEXT_COLOR, bg=self.BG_LIGHT)
        self.true_count_title_label.pack()
        self.true_count_label = tk.Label(count_frame, text="0.00", font=('Arial', 24, 'bold'),
                                       fg=self.ACCENT_COLOR, bg=self.BG_LIGHT)
        self.true_count_label.pack()

        # 資訊顯示
        info_frame = tk.Frame(self.master, bg=self.BG_DARK)
        info_frame.pack(fill='x', pady=5)
        
        # 剩餘牌數
        self.cards_left_label = tk.Label(
            info_frame, 
            text=f"{self.language_strings['cards_left']} {self.total_cards}",
            font=('Arial', 12, 'bold'), 
            fg=self.HIGHLIGHT_COLOR,
            bg=self.BG_DARK
        )
        self.cards_left_label.pack(side=tk.LEFT, padx=10)
        
        # 建議下注
        self.bet_suggest_label = tk.Label(
            info_frame, 
            text=f"{self.language_strings['suggested_bet']} {self.bet_unit}",
            font=('Arial', 12, 'bold'), 
            fg=self.INFO_COLOR,
            bg=self.BG_DARK
        )
        self.bet_suggest_label.pack(side=tk.RIGHT, padx=10)

        # 輸入的牌
        self.cards_display = tk.Label(
            self.master, 
            text=f"{self.language_strings['entered_cards']} ",
            font=('Arial', 11, 'bold'), 
            fg=self.ACCENT_COLOR,
            bg=self.BG_DARK,
            wraplength=280
        )
        self.cards_display.pack(pady=5)

        # 牌值按鈕 - 使用新的佈局
        cards_frame = tk.Frame(self.master, bg=self.BG_DARK)
        cards_frame.pack(pady=5)
        
        # 第一行按鈕
        row1_frame = tk.Frame(cards_frame, bg=self.BG_DARK)
        row1_frame.pack()
        for card in ["A", "2", "3", "4", "5", "6", "7"]:
            btn = ttk.Button(row1_frame, text=card, style='Card.TButton',
                           width=3, command=lambda c=card: self.process_card(c))
            btn.pack(side=tk.LEFT, padx=3, pady=3)

        # 第二行按鈕
        row2_frame = tk.Frame(cards_frame, bg=self.BG_DARK)
        row2_frame.pack()
        for card in ["8", "9", "10", "J", "Q", "K"]:
            btn = ttk.Button(row2_frame, text=card, style='Card.TButton',
                           width=3, command=lambda c=card: self.process_card(c))
            btn.pack(side=tk.LEFT, padx=3, pady=3)

        # 控制按鈕
        control_frame = tk.Frame(self.master, bg=self.BG_DARK)
        control_frame.pack(pady=10)
        self.delete_button = ttk.Button(control_frame, text=self.language_strings['delete'], style='Control.TButton',
                  command=self.delete_last_card)
        self.delete_button.pack(side=tk.LEFT, padx=10)
        self.reset_button = ttk.Button(control_frame, text=self.language_strings['reset'], style='Control.TButton',
                  command=self.reset_counter)
        self.reset_button.pack(side=tk.LEFT, padx=10)

    def update_decks(self, event):
        self.num_decks = int(self.deck_var.get())
        self.total_cards = self.num_decks * 52
        self.reset_counter()

    def process_card(self, card):
        try:
            self.update_count(card)
            self.entered_cards.append(card)
            self.update_display()
        except Exception as e:
            messagebox.showerror("錯誤", f"處理錯誤: {e}")

    def delete_last_card(self):
        if self.entered_cards:
            last_card = self.entered_cards.pop()
            self.undo_count(last_card)
            self.update_display()

    def format_displayed_cards(self):
        if len(self.entered_cards) <= 10:
            return " ".join(self.entered_cards)
        else:
            return "..." + " ".join(self.entered_cards[-10:])

    def update_display(self):
        remaining_cards = self.total_cards - self.cards_played
        remaining_decks = remaining_cards / 52
        true_count = self.running_count / remaining_decks if remaining_decks > 0 else 0
        
        try:
            self.bet_unit = int(self.bet_entry.get())
        except ValueError:
            self.bet_unit = 100

        bet_multiplier = max(1, true_count - 1)
        bet_suggestion = max(self.bet_unit, int(bet_multiplier * self.bet_unit))

        # 設定 running count 顏色
        count_color = self.POSITIVE_COLOR if self.running_count > 0 else (
            self.NEGATIVE_COLOR if self.running_count < 0 else self.ACCENT_COLOR)
        
        # 設定 true count 顏色
        true_count_color = self.POSITIVE_COLOR if true_count > 0 else (
            self.NEGATIVE_COLOR if true_count < 0 else self.ACCENT_COLOR)
        
        # 更新所有顯示
        self.count_label.config(
            text=str(self.running_count),
            fg=count_color
        )
        
        self.true_count_label.config(
            text=f"{true_count:.2f}",
            fg=true_count_color
        )
        
        self.cards_left_label.config(
            text=f"{self.language_strings['cards_left']} {remaining_cards}",
            fg=self.HIGHLIGHT_COLOR
        )
        
        self.bet_suggest_label.config(
            text=f"{self.language_strings['suggested_bet']} {bet_suggestion}",
            fg=self.INFO_COLOR
        )
        
        self.cards_display.config(
            text=f"{self.language_strings['entered_cards']} {self.format_displayed_cards()}",
            fg=self.ACCENT_COLOR
        )

    def update_count(self, card):
        high_cards = ["10", "J", "Q", "K", "A"]
        low_cards = ["2", "3", "4", "5", "6"]
        if card in high_cards:
            self.running_count -= 1
        elif card in low_cards:
            self.running_count += 1
        self.cards_played += 1

    def undo_count(self, card):
        high_cards = ["10", "J", "Q", "K", "A"]
        low_cards = ["2", "3", "4", "5", "6"]
        if card in high_cards:
            self.running_count += 1
        elif card in low_cards:
            self.running_count -= 1
        self.cards_played -= 1

    def reset_counter(self):
        self.running_count = 0
        self.cards_played = 0
        self.entered_cards = []
        self.update_display()

if __name__ == "__main__":
    root = tk.Tk()
    app = CardCountingApp(root)
    root.mainloop()
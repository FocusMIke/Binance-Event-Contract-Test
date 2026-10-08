import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import uiautomator2 as u2
import time
import threading
import configparser
import os
import requests
import sys
import ctypes
import queue

# ==========================================
# 1. System & Console Setup
# ==========================================
def disable_quickedit():
    """Disable Windows QuickEdit Mode to prevent script suspension"""
    try:
        kernel32 = ctypes.windll.kernel32
        handle = kernel32.GetStdHandle(-10)
        mode = ctypes.c_uint32()
        kernel32.GetConsoleMode(handle, ctypes.byref(mode))
        mode.value &= ~0x0040
        kernel32.SetConsoleMode(handle, mode)
    except Exception:
        pass

if getattr(sys, 'frozen', False):
    APP_PATH = os.path.dirname(sys.executable)
else:
    APP_PATH = os.path.dirname(os.path.abspath(__file__))

CONFIG_FILE = os.path.join(APP_PATH, 'config.ini')

# ==========================================
# 2. Multi-Language EULA & UI Texts
# ==========================================
EULA_CONTENT = {
    "English": {
        "text": """END USER LICENSE AGREEMENT (EULA)

This software is an OPEN-SOURCE and 100% FREE project developed strictly for scientific research, UI automation testing, and educational purposes ONLY. 

1. NOT A COMMERCIAL PRODUCT: This is NOT a commercial financial product. It is NOT designed to provide financial advice or guarantee profits.
2. VOLUNTARY USE: By choosing to use this software, you acknowledge that you are doing so entirely voluntarily. 
3. ASSUMPTION OF RISK: You assume full responsibility for any and all financial losses, account suspensions, or risks incurred by using this automation tool.
4. ZERO LIABILITY: The developer assumes ZERO legal or financial liability for your actions. 

By checking the box below, you legally agree to these terms.""",
        "checkbox": "I have read and agree to the terms of the EULA.",
        "btn_decline": "✖ Decline & Exit",
        "btn_accept": "✔ Accept & Continue"
    },
    "繁體中文": {
        "text": """最終用戶許可協議 (EULA)

本軟體為開源且 100% 免費的專案，嚴格用於科學研究、UI 自動化測試與教育目的。

1. 非商業金融產品：本軟體絕非商業產品。它並非設計用來提供財務建議或保證任何獲利。
2. 自願使用：當您選擇使用本軟體時，即表示您完全出於自願。
3. 承擔風險：您願意自行承擔因使用本自動化工具而產生的所有潛在財務損失、帳號封禁或其他風險。
4. 零責任：開發者對您的操作與結果不承擔任何法律與財務責任。

勾選下方核取方塊，即表示您在法律上同意上述條款。""",
        "checkbox": "我已閱讀並同意上述 EULA 條款。",
        "btn_decline": "✖ 拒絕並退出",
        "btn_accept": "✔ 同意並繼續"
    },
    "Español": {
        "text": """ACUERDO DE LICENCIA DE USUARIO FINAL (EULA)

Este software es un proyecto de CÓDIGO ABIERTO y 100% GRATUITO desarrollado estrictamente para investigación científica, pruebas de automatización de UI y fines educativos.

1. NO ES UN PRODUCTO COMERCIAL: NO es un producto financiero comercial ni garantiza ganancias.
2. USO VOLUNTARIO: Al utilizar este software, lo hace voluntariamente.
3. ASUNCIÓN DE RIESGOS: Usted asume toda la responsabilidad por cualquier pérdida financiera, suspensión de cuenta o riesgos incurridos.
4. CERO RESPONSABILIDAD: El desarrollador no asume NINGUNA responsabilidad legal o financiera.

Al marcar la casilla a continuación, acepta legalmente estos términos.""",
        "checkbox": "He leído y acepto los términos del EULA.",
        "btn_decline": "✖ Rechazar y Salir",
        "btn_accept": "✔ Aceptar y Continuar"
    },
    "한국어": {
        "text": """최종 사용자 사용권 계약 (EULA)

본 소프트웨어는 엄격하게 과학적 연구, UI 자동화 테스트 및 교육 목적으로만 개발된 오픈 소스 및 100% 무료 프로젝트입니다.

1. 상업용 제품 아님: 본 소프트웨어는 상업용 금융 상품이 아니며 재정적 조언을 제공하거나 이익을 보장하지 않습니다.
2. 자발적 사용: 본 소프트웨어를 사용하기로 선택함으로써 귀하는 전적으로 자발적으로 사용하는 것임을 인정합니다.
3. 위험 감수: 발생하는 모든 재정적 손실, 계정 정지 또는 위험에 대한 모든 책임은 귀하에게 있습니다.
4. 책임 면제: 개발자는 귀하의 행동에 대해 어떠한 법적 또는 재정적 책임도 지지 않습니다.

아래 확인란을 선택하면 본 약관에 법적으로 동의하는 것입니다.""",
        "checkbox": "본인은 EULA 약관을 읽고 이에 동의합니다.",
        "btn_decline": "✖ 거절 및 종료",
        "btn_accept": "✔ 동의 및 계속"
    },
    "日本語": {
        "text": """エンドユーザー使用許諾契約（EULA）

本ソフトウェアは、科学的研究、UI自動化テスト、および教育目的でのみ開発された、オープンソースで100％無料のプロジェクトです。

1. 非商業製品：これは商業的な金融商品ではありません。財務的なアドバイスを提供したり、利益を保証したりするものではありません。
2. 自発的な使用：このソフトウェアを使用することにより、あなたは完全に自発的に使用していることを認めるものとします。
3. リスクの引き受け：経済的損失、アカウントの凍結、または発生したリスクに対するすべての責任はあなたにあります。
4. 責任の免除：開発者はあなたの行動に対して一切の法的または財政的責任を負いません。

下のチェックボックスをオンにすると、法的にこれらの条件に同意したことになります。""",
        "checkbox": "私はEULAの条件を読み、これに同意します。",
        "btn_decline": "✖ 拒否して終了",
        "btn_accept": "✔ 同意して続行"
    }
}

TUTORIALS = {
    "English": """[DISCLAIMER - PLEASE READ]
This software is an OPEN-SOURCE and 100% FREE project developed strictly for scientific research and educational purposes. It is NOT a commercial product. By using this software, you acknowledge that you do so entirely voluntarily and assume full responsibility for any financial losses. The developer assumes ZERO liability.

[STEP-BY-STEP GUIDE]
1. License Key: Enter the VIP key provided by your administrator.
2. Server IP: Enter the cloud server IP address.
3. Device SN (Hardware Serial Number): 
   - SINGLE PHONE: Leave this field completely BLANK. The system will auto-detect your connected phone.
   - MULTIPLE PHONES: To control multiple phones on one PC, you CANNOT run them from the same folder. You must create a NEW FOLDER for each phone (e.g., 'Phone_A', 'Phone_B'). Copy this EXE file into each new folder. Run each EXE separately, and enter the specific SN code of each phone into its respective window to avoid data conflicts!
4. Trade Amount (USDT): Set your desired order size per trade. (Default: 5)
5. Screen Coordinates (X , Y): Input the exact X and Y coordinates for the buttons on your specific phone screen. Decimals (e.g., 500.5) are fully supported.
6. Start Running: Click 'Save Settings', then click '▶ START BOT'. Do NOT touch the mobile device screen while the bot is running!""",

    "繁體中文": """[免責聲明 - 請務必閱讀]
本軟體為開源且 100% 免費的專案，嚴格用於科學研究與教育目的。本軟體絕非商業產品。當您選擇使用本軟體時，即表示您完全出於自願，並願意自行承擔所有潛在的財務損失與風險。開發者對此不承擔任何責任。

[傻瓜式使用教學]
1. License Key (授權碼): 請填寫管理員提供的 VIP 密鑰。
2. Server IP (伺服器 IP): 填寫雲端伺服器 IP。
3. Device SN (設備序號): 
   - 單台手機: 請將此欄位「完全留空」，系統會自動偵測連線的手機。
   - 多台手機: 若要在一台電腦控制多台手機，請務必「新建多個資料夾」（例如：手機A、手機B）。將本 EXE 軟體分別複製到每個資料夾中。獨立打開它們，並在各自的視窗中填寫對應的手機 SN 碼，絕對不可共用同一個資料夾，以免數據衝突！
4. Trade Amount (交易金額): 設定您期望的單次下單金額。(預設: 5)
5. Screen Coordinates (螢幕座標): 填寫適用於您手機解析度的 X 與 Y 座標，支援小數點格式。
6. 開始運行: 先點擊「Save Settings (儲存設定)」，再點擊「▶ START BOT」。運行期間切勿用手觸碰手機螢幕！"""
}
# Redirect other languages to English for tutorial brevity
for lang in ["Español", "한국어", "日本語"]:
    TUTORIALS[lang] = TUTORIALS["English"]

# ==========================================
# 3. Startup EULA Blocking Window (防溢出版)
# ==========================================
class EULAWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("End User License Agreement")
        self.geometry("620x550")
        self.configure(bg="#1e1e1e")
        self.resizable(False, False)
        
        # Intercept close button (X) to kill app entirely
        self.protocol("WM_DELETE_WINDOW", self.on_decline)
        
        self.setup_ui()
        self.change_language()

    def setup_ui(self):

        top_frame = tk.Frame(self, bg="#1e1e1e")
        top_frame.pack(side=tk.TOP, fill=tk.X, pady=15, padx=20)
        
        tk.Label(top_frame, text="🌐 Language / 語言:", bg="#1e1e1e", fg="#ffffff", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(value="English")
        self.lang_combo = ttk.Combobox(top_frame, textvariable=self.lang_var, values=list(EULA_CONTENT.keys()), state="readonly", width=15)
        self.lang_combo.pack(side=tk.LEFT, padx=10)
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)
        

        btn_frame = tk.Frame(self, bg="#1e1e1e")
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=(5, 20))
        
        self.btn_decline = tk.Button(btn_frame, text="", bg="#d13b3b", fg="white", font=("Segoe UI", 10, "bold"), borderwidth=0, padx=15, pady=8, cursor="hand2", command=self.on_decline)
        self.btn_decline.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))
        
        self.btn_accept = tk.Button(btn_frame, text="", bg="#444444", fg="gray", font=("Segoe UI", 10, "bold"), borderwidth=0, padx=15, pady=8, state=tk.DISABLED, command=self.on_accept)
        self.btn_accept.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        self.agree_var = tk.BooleanVar(value=False)
        self.chk_agree = tk.Checkbutton(self, text="", variable=self.agree_var, command=self.toggle_accept, 
                                        bg="#1e1e1e", fg="#00fa9a", selectcolor="#2d2d2d", font=("Segoe UI", 10, "bold"), activebackground="#1e1e1e", activeforeground="#00fa9a")
        self.chk_agree.pack(side=tk.BOTTOM, anchor=tk.W, padx=20, pady=(5, 10))
        

        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, bg="#2d2d2d", fg="#d4d4d4", font=("Segoe UI", 10), borderwidth=0, padx=15, pady=15, height=10)
        self.text_area.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

    def change_language(self, event=None):
        lang = self.lang_var.get()
        content = EULA_CONTENT[lang]
        
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, content["text"])
        self.text_area.config(state=tk.DISABLED)
        
        self.chk_agree.config(text=content["checkbox"])
        self.btn_decline.config(text=content["btn_decline"])
        self.btn_accept.config(text=content["btn_accept"])

    def toggle_accept(self):
        if self.agree_var.get():
            self.btn_accept.config(state=tk.NORMAL, bg="#00a67d", fg="white", cursor="hand2")
        else:
            self.btn_accept.config(state=tk.DISABLED, bg="#444444", fg="gray", cursor="arrow")

    def on_accept(self):
        self.destroy()
        self.master.deiconify() 
        app_main = TradingGatewayApp(self.master)

    def on_decline(self):
        self.master.destroy()
        sys.exit()

# ==========================================
# 4. Main GUI Components (Tutorial & Logs)
# ==========================================
class TutorialWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Tutorial & Disclaimer")
        self.geometry("700x600")
        self.configure(bg="#1e1e1e")
        self.resizable(False, False)
        
        top_frame = tk.Frame(self, bg="#1e1e1e")
        top_frame.pack(fill=tk.X, pady=15, padx=15)
        
        tk.Label(top_frame, text="Select Language:", bg="#1e1e1e", fg="#ffffff", font=("Segoe UI", 10, "bold")).pack(side=tk.LEFT)
        self.lang_var = tk.StringVar(value="English")
        self.lang_combo = ttk.Combobox(top_frame, textvariable=self.lang_var, values=list(TUTORIALS.keys()), state="readonly", width=15)
        self.lang_combo.pack(side=tk.LEFT, padx=10)
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)
        
        self.copy_btn = ttk.Button(top_frame, text="📋 Copy Text", command=self.copy_text)
        self.copy_btn.pack(side=tk.RIGHT)
        
        self.text_area = scrolledtext.ScrolledText(self, wrap=tk.WORD, bg="#2d2d2d", fg="#d4d4d4", font=("Segoe UI", 10), borderwidth=0, padx=15, pady=15)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        self.change_language()

    def change_language(self, event=None):
        lang = self.lang_var.get()
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, TUTORIALS.get(lang, ""))
        self.text_area.config(state=tk.DISABLED)

    def copy_text(self):
        self.clipboard_clear()
        self.clipboard_append(self.text_area.get(1.0, tk.END))
        messagebox.showinfo("Copied", "Text copied to clipboard successfully!", parent=self)

class StdoutRedirector:
    def __init__(self, text_widget):
        self.text_widget = text_widget
    def write(self, string):
        self.text_widget.configure(state='normal')
        self.text_widget.insert(tk.END, string)
        self.text_widget.see(tk.END)
        self.text_widget.configure(state='disabled')
    def flush(self): pass

# ==========================================
# 5. Main App Logic
# ==========================================
class TradingGatewayApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Trading Gateway Client - Pro Edition")
        self.root.geometry("680x760")
        self.root.resizable(False, False)
        self.root.configure(bg="#1e1e1e")
        
        self.setup_theme()
        
        self.config = configparser.ConfigParser()
        self.is_running = False
        self.bot_thread = None
        self.d = None 
        self.signal_queue = None
        
        self.init_default_config()
        self.build_ui()
        self.load_config_to_ui()

    def setup_theme(self):
        style = ttk.Style()
        if 'clam' in style.theme_names():
            style.theme_use('clam')
        style.configure("TFrame", background="#1e1e1e")
        style.configure("TLabel", background="#1e1e1e", foreground="#ffffff", font=("Segoe UI", 10))
        style.configure("TLabelframe", background="#1e1e1e", bordercolor="#444444")
        style.configure("TLabelframe.Label", background="#1e1e1e", foreground="#00fa9a", font=("Segoe UI", 10, "bold"))
        style.configure("TButton", background="#333333", foreground="#ffffff", font=("Segoe UI", 10, "bold"), padding=5)
        style.map("TButton", background=[("active", "#555555")])
        style.configure("Accent.TButton", background="#007acc", foreground="#ffffff")
        style.map("Accent.TButton", background=[("active", "#0098ff")])
        style.configure("Start.TButton", background="#00a67d", foreground="#ffffff")
        style.map("Start.TButton", background=[("active", "#00d19e")])
        style.configure("Stop.TButton", background="#d13b3b", foreground="#ffffff")
        style.map("Stop.TButton", background=[("active", "#ff4d4d")])

    def init_default_config(self):
        if not os.path.exists(CONFIG_FILE):
            self.config['Authorization'] = {'LICENSE_KEY': 'TEST_001', 'TARGET_DEVICE_SN': ''}
            self.config['Network'] = {'SERVER_IP': '0.0.0.0'}
            self.config['Trading'] = {'LOCAL_TRADE_AMOUNT': '5'}
            self.config['Coordinates'] = {
                'INPUT_AMOUNT_X': '500', 'INPUT_AMOUNT_Y': '600', 'YES_BTN_X': '300', 'YES_BTN_Y': '800',
                'NO_BTN_X': '700', 'NO_BTN_Y': '800', 'CONFIRM_BTN_X': '500', 'CONFIRM_BTN_Y': '900'
            }
            with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
                self.config.write(configfile)
        else:
            self.config.read(CONFIG_FILE, encoding='utf-8')

    def build_ui(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(header_frame, text="Automated Trading Client", font=("Segoe UI", 16, "bold"), foreground="#00fa9a").pack(side=tk.LEFT)
        ttk.Button(header_frame, text="📖 Tutorial & Guide", style="Accent.TButton", command=lambda: TutorialWindow(self.root)).pack(side=tk.RIGHT)

        frame_auth = ttk.LabelFrame(main_frame, text=" 1. Authorization & Network ", padding="15")
        frame_auth.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame_auth, text="License Key:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ent_key = tk.Entry(frame_auth, width=28, bg="#2d2d2d", fg="#ffffff", insertbackground="#ffffff", borderwidth=1, relief="solid", font=("Consolas", 10))
        self.ent_key.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 20))

        ttk.Label(frame_auth, text="Server IP:").grid(row=0, column=2, sticky=tk.E, pady=5)
        self.ent_ip = tk.Entry(frame_auth, width=18, bg="#2d2d2d", fg="#ffffff", insertbackground="#ffffff", borderwidth=1, relief="solid", font=("Consolas", 10))
        self.ent_ip.grid(row=0, column=3, sticky=tk.W, pady=5, padx=(10, 0))

        ttk.Label(frame_auth, text="Device SN:").grid(row=1, column=0, sticky=tk.W, pady=10)
        self.ent_sn = tk.Entry(frame_auth, width=28, bg="#2d2d2d", fg="#ffffff", insertbackground="#ffffff", borderwidth=1, relief="solid", font=("Consolas", 10))
        self.ent_sn.grid(row=1, column=1, sticky=tk.W, pady=10, padx=(10, 20))
        
        sn_hint = "ℹ️ Single Phone: Leave Blank | Multiple Phones: Enter specific SN"
        ttk.Label(frame_auth, text=sn_hint, font=("Segoe UI", 8, "italic"), foreground="#aaaaaa").grid(row=2, column=1, columnspan=3, sticky=tk.W, padx=10, pady=(0, 5))

        frame_trade = ttk.LabelFrame(main_frame, text=" 2. Trading Settings ", padding="15")
        frame_trade.pack(fill=tk.X, pady=5)

        ttk.Label(frame_trade, text="Trade Amount (USDT):").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.ent_amount = tk.Entry(frame_trade, width=15, bg="#2d2d2d", fg="#00fa9a", insertbackground="#ffffff", borderwidth=1, relief="solid", font=("Consolas", 12, "bold"))
        self.ent_amount.grid(row=0, column=1, sticky=tk.W, pady=5, padx=10)

        frame_coord = ttk.LabelFrame(main_frame, text=" 3. Screen Coordinates (X , Y) - Decimals Auto-Rounded ", padding="15")
        frame_coord.pack(fill=tk.X, pady=5)

        labels = ["Input Field:", "YES Button:", "NO Button:", "Confirm Btn:"]
        self.coord_entries = []
        for i, text in enumerate(labels):
            ttk.Label(frame_coord, text=text).grid(row=i//2, column=(i%2)*4, sticky=tk.E, pady=8, padx=5)
            ent_x = tk.Entry(frame_coord, width=7, bg="#2d2d2d", fg="#ffffff", insertbackground="#ffffff", borderwidth=1, justify="center")
            ent_x.grid(row=i//2, column=(i%2)*4+1, pady=8)
            ttk.Label(frame_coord, text=",").grid(row=i//2, column=(i%2)*4+2)
            ent_y = tk.Entry(frame_coord, width=7, bg="#2d2d2d", fg="#ffffff", insertbackground="#ffffff", borderwidth=1, justify="center")
            ent_y.grid(row=i//2, column=(i%2)*4+3, pady=8, padx=(0,15))
            self.coord_entries.append((ent_x, ent_y))

        frame_btns = ttk.Frame(main_frame, padding="10")
        frame_btns.pack(fill=tk.X, pady=5)

        self.btn_save = ttk.Button(frame_btns, text="💾 Save Settings", command=self.save_config)
        self.btn_save.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.btn_start = ttk.Button(frame_btns, text="▶ START BOT", style="Start.TButton", command=self.start_bot)
        self.btn_start.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)
        self.btn_stop = ttk.Button(frame_btns, text="■ STOP BOT", style="Stop.TButton", command=self.stop_bot, state=tk.DISABLED)
        self.btn_stop.pack(side=tk.LEFT, padx=5, expand=True, fill=tk.X)

        ttk.Label(main_frame, text="Console Logs:").pack(anchor=tk.W, pady=(5, 0))
        self.log_area = scrolledtext.ScrolledText(main_frame, height=12, state='disabled', bg="#0c0c0c", fg="#00ff00", font=("Consolas", 9), borderwidth=1, relief="solid")
        self.log_area.pack(fill=tk.BOTH, expand=True)

        sys.stdout = StdoutRedirector(self.log_area)
        sys.stderr = StdoutRedirector(self.log_area)
        print("[SYSTEM] Terms Accepted. Pro UI initialized successfully.")

    def load_config_to_ui(self):
        try:
            self.ent_key.insert(0, self.config.get('Authorization', 'LICENSE_KEY', fallback=''))
            self.ent_sn.insert(0, self.config.get('Authorization', 'TARGET_DEVICE_SN', fallback=''))
            self.ent_ip.insert(0, self.config.get('Network', 'SERVER_IP', fallback=''))
            self.ent_amount.insert(0, self.config.get('Trading', 'LOCAL_TRADE_AMOUNT', fallback=''))

            keys = [('INPUT_AMOUNT_X', 'INPUT_AMOUNT_Y'), ('YES_BTN_X', 'YES_BTN_Y'),
                    ('NO_BTN_X', 'NO_BTN_Y'), ('CONFIRM_BTN_X', 'CONFIRM_BTN_Y')]
            for i, (k_x, k_y) in enumerate(keys):
                self.coord_entries[i][0].insert(0, self.config.get('Coordinates', k_x, fallback='0'))
                self.coord_entries[i][1].insert(0, self.config.get('Coordinates', k_y, fallback='0'))
        except: pass

    def save_config(self):
        if self.is_running:
            messagebox.showwarning("Warning", "Cannot save settings while bot is running!")
            return
        self.config['Authorization']['LICENSE_KEY'] = self.ent_key.get().strip()
        self.config['Authorization']['TARGET_DEVICE_SN'] = self.ent_sn.get().strip()
        self.config['Network']['SERVER_IP'] = self.ent_ip.get().strip()
        self.config['Trading']['LOCAL_TRADE_AMOUNT'] = self.ent_amount.get().strip()

        keys = [('INPUT_AMOUNT_X', 'INPUT_AMOUNT_Y'), ('YES_BTN_X', 'YES_BTN_Y'),
                ('NO_BTN_X', 'NO_BTN_Y'), ('CONFIRM_BTN_X', 'CONFIRM_BTN_Y')]
        for i, (k_x, k_y) in enumerate(keys):
            self.config['Coordinates'][k_x] = self.coord_entries[i][0].get().strip()
            self.config['Coordinates'][k_y] = self.coord_entries[i][1].get().strip()

        with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
        print("[SYSTEM] Settings saved successfully.")
        messagebox.showinfo("Success", "Configuration saved successfully!")

    def start_bot(self):
        self.save_config()
        self.is_running = True
        self.signal_queue = queue.Queue() 
        
        self.btn_start.config(state=tk.DISABLED)
        self.btn_save.config(state=tk.DISABLED)
        self.btn_stop.config(state=tk.NORMAL)
        
        self.log_area.configure(state='normal')
        self.log_area.delete(1.0, tk.END)
        self.log_area.configure(state='disabled')
        
        print("==================================================")
        print(">>> INITIALIZING TRADING ENGINE...")
        print("==================================================")
        self.bot_thread = threading.Thread(target=self.bot_core_process, daemon=True)
        self.bot_thread.start()

    def stop_bot(self):
        self.is_running = False
        print("[SYSTEM] Stop signal sent. Terminating active connections...")
        self.btn_start.config(state=tk.NORMAL)
        self.btn_save.config(state=tk.NORMAL)
        self.btn_stop.config(state=tk.DISABLED)

    def get_parsed_coord(self, key_x, key_y):
        try:
            return (int(round(float(self.config.get('Coordinates', key_x, fallback='0')))), 
                    int(round(float(self.config.get('Coordinates', key_y, fallback='0')))))
        except: return (0, 0)

    def bot_core_process(self):
        try:
            target_sn = self.config.get('Authorization', 'TARGET_DEVICE_SN').strip()
            server_ip = self.config.get('Network', 'SERVER_IP').strip()
            self.server_url = f"http://{server_ip}"
            
            self.license_key = self.config.get('Authorization', 'LICENSE_KEY').strip()
            self.trade_amount = self.config.get('Trading', 'LOCAL_TRADE_AMOUNT').strip()
            self.coord_input = self.get_parsed_coord('INPUT_AMOUNT_X', 'INPUT_AMOUNT_Y')
            self.coord_yes = self.get_parsed_coord('YES_BTN_X', 'YES_BTN_Y')
            self.coord_no = self.get_parsed_coord('NO_BTN_X', 'NO_BTN_Y')
            self.coord_confirm = self.get_parsed_coord('CONFIRM_BTN_X', 'CONFIRM_BTN_Y')
        except Exception as e:
            print(f"[ERROR] Configuration parsing failed: {e}")
            self.stop_bot()
            return

        print("[SYSTEM] Verifying License Key with Cloud Server...")
        try:
            payload = {"key": self.license_key, "sn": target_sn if target_sn else "startup_check", "amount": self.trade_amount}
            res = requests.post(f"{self.server_url}/api/verify", json=payload, timeout=5)
            if res.json().get("authorized") == False:
                print("\n❌ [SECURITY ALERT] Start aborted! License Key is INVALID or BLOCKED by Admin.")
                self.stop_bot()
                return
            print("✅ [SUCCESS] License Key Verified!")
        except Exception as e:
            print(f"\n❌ [NETWORK ERROR] Cannot connect to server {self.server_url}.")
            print("Make sure the Server IP is correct and the server is running.")
            self.stop_bot()
            return

        print("[SYSTEM] Connecting to physical device...")
        try:
            self.d = u2.connect(target_sn) if target_sn else u2.connect()
            self.device_sn = self.d.serial
            print(f"[SUCCESS] Device Connected. SN: {self.device_sn}")
            if not target_sn:
                self.ent_sn.delete(0, tk.END)
                self.ent_sn.insert(0, self.device_sn)
                self.config['Authorization']['TARGET_DEVICE_SN'] = self.device_sn
                with open(CONFIG_FILE, 'w', encoding='utf-8') as configfile:
                    self.config.write(configfile)
        except Exception as e:
            print(f"[FATAL] Device connection failed: {e}")
            self.stop_bot()
            return
            
        threading.Thread(target=self.signal_consumer, daemon=True).start()
        self.poll_signals_from_cloud()

    def signal_consumer(self):
        while self.is_running:
            try:
                side, quantity = self.signal_queue.get(timeout=1)
                self.execute_trade_action(side, quantity)
                self.signal_queue.task_done()
            except queue.Empty:
                pass 
            except Exception as e:
                pass

    def execute_trade_action(self, side, quantity):
        print(f"\n[EXECUTION START] Target: {side} | Loop Count: {quantity}")
        pkg_name = "com.binance.dev"
        for i in range(quantity):
            if not self.is_running: break
            print(f"> Sequence {i + 1}/{quantity} initiated...")
            try:
                self.d.screen_on()
                self.d.app_start(pkg_name)
                time.sleep(0.3) 
                self.d.click(*self.coord_input) 
                time.sleep(0.2)
                input_node = self.d(className="android.widget.EditText")
                input_node.clear_text()
                input_node.set_text(self.trade_amount)
                time.sleep(0.5) 
                
                if side.upper() == "YES": self.d.click(*self.coord_yes)
                elif side.upper() == "NO": self.d.click(*self.coord_no)
                else: return
                
                time.sleep(0.8)
                self.d.click(*self.coord_confirm)
                time.sleep(1.0)
                self.d.click(*self.coord_confirm)
                
                print(f"[SUCCESS] Sequence {i + 1} completed.")
                if i < quantity - 1: time.sleep(2.0)
            except Exception as e:
                print(f"[ERROR] Exception during execution: {e}")
                break 

    def poll_signals_from_cloud(self):
        last_executed_id = 0
        print("[NETWORK] Listening for cloud signals...")
        
        while self.is_running:
            try:
                res = requests.get(f"{self.server_url}/api/get_signal?key={self.license_key}", timeout=3)
                data = res.json()
                
                if not data.get("authorized"):
                    print("\n❌ [SECURITY ALERT] License invalidated during runtime! Connection closed.")
                    self.stop_bot()
                    break 
                    
                current_id = data.get("signal_id", 0)
                if current_id > last_executed_id:
                    if last_executed_id == 0:
                        last_executed_id = current_id
                        print("[STATUS] Sync complete. Ready for new trades.")
                    else:
                        last_executed_id = current_id
                        side = data.get("side")
                        quantity = data.get("quantity")
                        
                        pending_count = self.signal_queue.qsize() + 1
                        print(f"\n[SIGNAL DETECTED] Direction: {side} | Quantity: {quantity}")
                        print(f"➜ Added to execution queue. Pending orders: {pending_count}")
                        self.signal_queue.put((side, quantity))
                        
            except Exception:
                pass 
            time.sleep(1)
        print("[SYSTEM] Engine stopped gracefully.")

if __name__ == "__main__":
    disable_quickedit()
    
    root = tk.Tk()
    root.withdraw() 
    
    eula_window = EULAWindow(root)
    
    root.mainloop()
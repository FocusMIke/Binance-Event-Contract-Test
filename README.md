# ☯️ Trading Gateway Client - Pro Edition

![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey)

---

## ⚠️ STRICT LEGAL DISCLAIMER (PLEASE READ FIRST)

**This software is purely a SCIENTIFIC RESEARCH PROJECT and is absolutely NOT a commercial software or financial product.** 
- It is developed strictly for **academic study, UI automation testing, and educational purposes ONLY**. 
- It is **NOT** designed to provide financial advice, solicit investments, or guarantee any profits.
- By downloading or using this software, you acknowledge that you are doing so entirely voluntarily. You assume **full and sole responsibility** for any and all financial losses, account suspensions, or risks incurred. 
- **The developer assumes ZERO legal or financial liability for your actions.**

---

> **Eastern Metaphysics Meets Algorithmic Trading.**
> Featuring a unique UI inspired by the "Purple Gold Taiji Bagua" and "Yi Wood" (vitality and trend-following flow), this client is designed for supreme aesthetic appeal and robust execution.

**Trading Gateway Client** is a powerful, open-source UI automation bridge. It connects cloud-based trading signals (like TradingView Webhooks) directly to physical or emulated Android devices via `uiautomator2`, enabling automated execution on mobile trading apps.

---

## 📥 Download & Installation

**[👉 Click here to download the latest Release (Pro Edition)](https://github.com/FocusMIke/Binance-Event-Contract-Test/tags)**

*(Note: Download the `.zip` file from the latest tag, extract it into a new folder, and run the `.exe` directly. No Python environment required!)*

---

## 📖 The Ultimate Step-by-Step Setup Guide (READ CAREFULLY)

To ensure the bot runs perfectly, please follow these exact steps. Do not skip any!

### Step 1: Client Configuration (UI Settings)

1. **License Key:** 
   - The default text is `TEST_001`. Your administrator will provide you with a VIP key (e.g., `VIP_999`). 
   - 🚨 **CRITICAL WARNING:** You must replace the **ENTIRE** string! Do not just change the numbers. If you enter `TEST_999`, it will **FAIL**. It must be exactly exactly what the admin gave you (e.g., `VIP_999`).
2. **Server IP:** 
   - Leave this exactly as it is (default is usually `104.156.254.63`). 
   - 🚨 **CRITICAL WARNING:** **DO NOT TOUCH THIS!** If you change this, your client will completely disconnect from the cloud signals.
3. **Trade Amount (USDT):** 
   - Enter your base order size per trade (e.g., `10` or `50`).

### Step 2: Prepare Your Android Phone (Developer Mode)

To allow the PC to control your phone, you must enable a few hidden Android settings.

1. **Enable Developer Options:** 
   - Go to your phone's `Settings` -> `About Phone`.
   - Find `Build Number` and **tap it 7 times quickly**. You will see a message saying "You are now a developer!"
2. **Enable USB Debugging:** 
   - Go back to `Settings` -> find `Developer Options` (usually under System).
   - Turn ON **USB Debugging**.
   - Plug your phone into the PC. If a popup appears on your phone asking "Allow USB Debugging?", check "Always allow" and click **OK**.

> 💡 **PRO TIP (Ask AI):** Android menus look different on Samsung, Xiaomi, Motorola, etc. If you can't find "Build Number" or "USB Debugging", please ask an AI assistant like **ChatGPT, Claude, or Doubao**. 
> *Just copy and paste this into AI:* **"How do I turn on Developer Options and USB Debugging on my [Insert Your Phone Model Here]?"**

### Step 3: Device SN (Serial Number) Routing

- **If you only use ONE phone:** Leave the "Device SN" box completely **BLANK**. The software will auto-detect your phone.
- **If you use MULTIPLE phones on one PC:** 
  1. You must create a **NEW FOLDER** for each device (e.g., Folder `Phone_A`, Folder `Phone_B`). Put the `.exe` inside each folder and run them separately!
  2. You cannot leave the SN box blank. You must input the exact SN code of each phone. 
  3. *How to find SN?* Go to `Settings` -> `About Phone` -> `Status` -> `Serial Number`. Alternatively, open your computer terminal (CMD) and type `adb devices`.

### Step 4: Calibrating Screen Coordinates (X , Y)

Since every phone screen has a different size, you must tell the bot exactly where to tap.

1. Go back to your phone's **Developer Options**.
2. Scroll down and turn ON **Pointer Location** (sometimes called "Show taps and pointer location").
3. Now, open your trading app. Tap on the exact spot where the "Amount Input" box is. Look at the very top of your phone screen: you will see a bar showing **X:** and **Y:** coordinates (e.g., `X: 540.5  Y: 1200.0`).
4. Type those exact X and Y numbers into the corresponding boxes in the client software. Decimals are fully supported.
5. Repeat this for the YES button, NO button, and Confirm button.
6. Once you are done, you can turn **Pointer Location** OFF in your phone settings.

### Step 5: Start the Bot

- Click **💾 Save Settings** first.
- Click **▶ START BOT**. 
- ⚠️ **DO NOT touch the mobile device screen** while the bot is running, or you might interrupt the automation!

---

## 📡 TradingView Webhook Configuration

Set up an alert on TradingView and point the Webhook URL to your cloud server:
`http://<YOUR_SERVER_IP>/api/tv_signal`

In the **Message** box, strictly use the following JSON format:

```json
{"side": "YES", "quantity": 1}
```

*(Tip: Set `quantity` to 2 or higher if you want the bot to auto-split and loop the order for heavier positions!)*

---

## ☕ Support & Donation

If you find this project helpful for your quantitative research or trading automation, consider buying the developer a coffee! Your support is highly appreciated and keeps this project 100% free, open-source, and actively maintained.

**USDT (Tether)**
* **Network:** BSC / BNB Smart Chain (BEP20)
* **Address:** `0x8a086cf46675ab76e4cf4f4e06f5d91bac77831f`

<img src="USDT_QR.png" width="200" alt="USDT BSC QR Code">

*(⚠️ Note: Please ensure you select the strictly correct **BSC / BEP20** network when transferring, otherwise your funds may be permanently lost.)*

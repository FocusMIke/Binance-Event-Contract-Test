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

## ✨ Core Features

- **🚀 Lightning-Fast UI Automation:** Built on `uiautomator2` for millisecond-level screen interaction.
- **🛡️ Enterprise-Grade Concurrency (Queue System):** Never worry about overlapping signals. The built-in FIFO queue ensures that if multiple signals arrive within seconds, they are executed in a strictly orderly sequence, preventing UI conflict.
- **📱 Multi-Device Support:** Run multiple emulators or physical phones from a single PC. (See Multi-Device Setup below).
- **🎛️ Dynamic Position Sizing (Scaling):** Supports dynamic `quantity` payload in JSON. If the cloud sends `quantity: 3`, the bot will automatically loop the execution 3 times, perfectly bypassing strict single-order limits on specific exchanges.
- **🔒 Cloud-Based Auth System:** Real-time license verification and heartbeat monitoring to ensure secure access.

---

## 📖 Step-by-Step Guide

### 1. Initial Setup
1. Enter your **License Key** (Provided by your server admin).
2. Enter the **Server IP** of your cloud backend (e.g., `104.156.xxx.xxx`).
3. Set your base **Trade Amount (USDT)** per execution loop.
4. Calibrate the **Screen Coordinates (X, Y)** to match your specific Android device resolution. Decimals are auto-rounded.

### 2. Multi-Device Routing (Crucial)
If you want to control **multiple phones** on a single PC, you **CANNOT** run multiple instances from the same folder.
- Create a NEW folder for each device (e.g., `Device_A`, `Device_B`).
- Copy the `.exe` file into each folder.
- Run them separately, and enter the specific **Hardware SN (Serial Number)** of each phone in its respective client window. (Leave blank if you are only using one phone).

### 3. TradingView Webhook Configuration
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

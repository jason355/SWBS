# 校園無聲廣播系統 SWBS (School Wrieless Broadcasting System)

- [校園無聲廣播系統 SWBS (School Wrieless Broadcasting System)](#校園無聲廣播系統-swbs-school-wrieless-broadcasting-system)
  - [Full map](#full-map)
    - [Overall](#overall)
  - [Server](#server)
    - [1. Method](#1-method)
  - [Android App (Yun'an)](#android-app-yunan)
    - [1. Method](#1-method-1)
    - [2. Flow chart](#2-flow-chart)
    - [3. 命名由來](#3-命名由來)
  - [Line Bot](#line-bot)
    - [1. Method](#1-method-2)

## Full map
![DFD](Flow%20Charts/DFD.png)

### Overall
- 此無聲廣播系統採用文字方式顯示在班級電子螢幕上，藉此達到無聲。我們最基本的架構為"Linebot"、"Server"、"Android App"。以此三個架構作為基礎，建立起此無聲廣播系統。



## Server
### 1. Method
- 此無聲廣播系統相較於傳統廣播系統採用文字方式顯示，傳輸方式由Websocket 傳輸協定達到雙向資料傳輸。 


## Android App (Yun'an)
### 1. Method
- 主要由"timer"、"websocket"兩個背景執行程式完成，timer 用來偵測是否為下課，而websocket則是用來建立與伺服器的連線。
### 2. Flow chart
![Yun'an Flow chart](Flow%20Charts/Yun'an1.png)
![Yun'an Flow chart](Flow%20Charts/Yun'an2.png)
![Yun'an Flow chart](Flow%20Charts/Yun'an3.png)
![Yun'an Flow chart](Flow%20Charts/Yun'an4.png)
### 3. 命名由來
- 我們始終覺得Android app 需要一個名字讓整個系統更親民，因此我們就開始腦力激盪思考此系統與他人的差別，最後的決定是，因為是無聲廣播，所以取"安靜"的"安"字，而與他牌的差異在於我們使用伺服器，伺服器令人聯想到"雲端"，故取"雲字"，而"雲安"較"安雲"好聽，所以取"雲安"，但我們團隊看久了覺得"雲"字太普遍，所以翻了字典找到了"昀"字覺得撞名機率不高，最後就決定為"昀安"，而英文則是直翻"Yun'an"
## Line Bot
### 1. Method






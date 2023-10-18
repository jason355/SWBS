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
    - [2. How to use?](#2-how-to-use)
      - [首次登入](#首次登入)
      - [發送廣播訊息](#發送廣播訊息)

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
- 我們始終覺得Android app 需要一個名字讓整個系統更親民，因此我們就開始腦力激盪思考此系統與他人的差別，最後的決定是，因為是無聲廣播，所以取"安靜"的"安"字，而與他牌的差異在於我們使用伺服器，伺服器令人聯想到"雲端"，故取"雲字"，而"雲安"較"安雲"好聽，所以取"雲安"，但我們團隊看久了覺得"雲"字太普遍，所以翻了字典找到了"昀"字覺得撞名機率不高，最後就決定為"昀安"，而英文則是直翻"Yun'an"。
## Line Bot
### 1. Method
- 我們一直在尋找一個低建置成本又高覆蓋率的介面讓傳輸端使用上較方便，而 LineBot 就是一個相當符合的介面。現在人基本上手機內都會有 Line 應用程式，這就達到我們要的高覆蓋率，且Linebot 的建置成本也不高，可使用 python 達成。原本我們考慮建置網頁，但 Linebot 感覺較符合行動裝置上的使用。至於寫一個軟體因作業系統不同而須開發兩種軟體，不管是在開發上或是建置上成本都較高。
  
  不過因為 Linebot 與使用者互動的限制相較網頁多，所以在開發時我們一直把對於使用者輸入最友善的方法擺在第一考量，活許沒有開發一個軟體或網頁來的漂亮，但是在使用上至少是方便且快速的。
### 2. How to use?
#### 首次登入
- 當使用者首次登入，會需要輸入身分，包含名稱、所在處室，而輸入後須等管理員驗證後才可啟用。

#### 發送廣播訊息
- 傳送"!"，可叫出快速選單，選擇"發送廣播訊息"，後輸入發送文字，等到機器人回傳確認，再選擇"單一班級"或是"群發"
  - 單一班級:
    
     輸入傳送班級數字即可
  - 群發:

    輸入 "0 ~ 3"或"7 ~ 9"或是 特定班級數字(ex 101)，使用空格或是逗號隔開即可。
- 以上都完成後，機器人會傳送確認訊息，如有需要更改，可選擇"no 訊息有誤"，重新輸入，如沒有問題，則選擇"yes 確認"





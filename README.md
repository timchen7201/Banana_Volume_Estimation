## 一、系統 / 程式目的
透過香蕉園中的Speed Dome攝影機拍攝，搭配電腦影像處理技術，追蹤香蕉生長情形變化。

## 二、輸入 / 輸出規格
### 輸入
此系統為初代版本，需要的輸入為
<b>同一鏡頭定點、旋轉角度、放大倍率。多張不同日期、時間的Speed Dome香蕉園高清影像。
</b>
<p>檔名格式：image_日-月-年_時-分-秒_AM(PM).jpg(png)</p>

#### 範例

![圖一](data/day/image_23-06-2020_01-00-52_PM.jpg)

![圖二](data/night/image_23-06-2020_01-00-38_AM.jpg)


### 輸出
香蕉體積變化的趨勢。如下圖：
![](scatter.png)

## 三、系統 / 程式操作說明

### 步驟一
將預進行邊緣偵測的圖片
![](data/night/image_23-06-2020_01-00-38_AM.jpg)
放入images/original/：
![](document_img/pic1.png)

### 步驟二
打開command line並執行
> python3 main

![](document_img/pic3.png)

按下enter後，可以看到系統正在處理圖片運算

![](document_img/pic4.png)

大約5分鐘後會電腦就會自動跑出香蕉體積趨勢圖

![](document_img/pic5.png)

並且會將趨勢圖存在當下目錄，並命名為scatter.png

![](document_img/pic2.png)

## 四、系統 / 程式流程

![](document_img/banana_volume_estimate-3.png)

## 五、演算法的使用
### 1.邊緣偵測(一) -- DexiNed：

DexiNed (Dense Extreme Inception Network for Edge Detection)
![](document_img/DexiNed.png)

香蕉結果圖像，產出於 image/edged_img/ 資料夾中。如下圖：
![](images/edged_img/image_14-06-2020_01-00-39_AM.png)

### 2.邊緣偵測(二) -- OpenCV Canny Filter：
The successive steps of the Canny filter

![](document_img/pic6.png)

香蕉結果圖像，如下圖：

![](document_img/pic7.png)


### 3.輪廓尋找 -- OpenCV findContours()：
參數選擇 cv2.RETR_EXTERNAL，只留下外圍的輪廓。
<b>圖例說明：</b>

![](document_img/pic8.png)

香蕉結果圖像，如下圖：
![](document_img/pic9.png)

### 4.篩選香蕉輪廓：
篩選條件：
* 輪廓圍起來的面積 > 前25%位數
* 輪廓圍起來的面積 < 平均+0.25倍的標準差
* 輪廓周長 < 600 pixels

香蕉結果圖像，產出於 image/result_pics/ 資料夾中。如下圖：
![](images/result_pics/res_image_24-06-2020_01-00-33_AM.png)

### 5.計算單根香蕉的平均體積：
#### 5.1
我們由 cv2.contourArea() 得到封閉曲線面積。
#### 5.2
由於面積 Area (A) 正比於邊長的平方，體積 Volume (V) 正比於邊長的三次方。
故我們將面積 Area (A) 開根號，再乘上三次方，求得體積 Volume (V) 的相對數值。

#### 5.3
將所有體積加總後，平均。

### 6.將單根香蕉的平均體積相對日期時間作圖，並計算回歸線
![](scatter.png)

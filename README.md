# Hopfield-network
## 程式簡介
### 使用說明
> 透過視覺化界面展示「離散型Hopfield Network」的使用方法

*  右方可以選擇訓練資料：「Basic_Training」、「Bonus_Training

*  所有資料皆以3張圖為一組，且「Bonus_Training」可以再細選子訓練集：「Bonus-x」

* 「訓練」後即產生所選資料的訓練結果

* 訓練後，可透過滑鼠點擊左側的圖片來選擇「測試資料」，並可「加入雜訊」

* 「驗證」後下方會產生Hopfield Network的 ( 聯想 ) 結果

### 範例圖
![](https://i.imgur.com/TbLk2fK.png)

## Hopfield Network 演算法
### 演算法簡介
> 應用於各方面的一種「聯想式學習」演算法
* 模擬人類記憶中聯想的神經網路，又分為「自聯想」、「異聯想」，Hopfield又屬自聯想

  * 自聯想： 看到模糊不清的照片，依然能辨別出原來的風貌
  
  * 異聯想： 聽到相對論，想到愛因斯坦的名字

* 離散Hopfield網路有記憶上限，假設神經元數目p，在記憶提取99%正確率的情況下，可儲存的資料筆數不超過

     <img src="https://render.githubusercontent.com/render/math?math={Memory \quad capacity \quad \le \quad p \over {4lnp}}">

* 聯想記憶的表達方式為 <img src="https://render.githubusercontent.com/render/math?math=Y = W X">，目標就是找到適合的 W，讓 X 聯想( 回想 )起 Y
  * X - 輸入，為n x 1的矩陣 
  
  * Y - 聯想結果，為n x 1的矩陣 
  
  * W - 網路鍵結值，為n x n的「對稱」矩陣
  
* W 的學習有很多種方法：**Hebbian rule**、Projection rule...。
* 聯想( 回想 )又分兩種方法：「同步」、「異步」，同步即一般的矩陣相乘，若採同步會有兩種可能：
  * 收斂至穩定狀態即定值：正確
  
  * 長度為2的有限循環：錯誤
  
* 呈上，異步回想則一定會收斂到穩定狀態。雖然此程式採用同步，但幸運地此程式所用的資料集都可以收斂到穩定狀態。
 
* 輸入、輸出向量都必須是雙極值 ( -1、1 ) 或 二元值 ( 0、1 )，但在Hebbian rule的學習法則下，兩者的學習公式會有些微差別：
  > w 表示第 j 到第 i 個神經元的鍵結值，x 表示輸入資料的第 i 維或第 j 維

  * 輸入輸出為雙極值 ( -1、1 )，W更新公式 ：
  
     <img src="https://render.githubusercontent.com/render/math?math=\Delta w_{ij} = x_{i} * x_{j}">
     
  * 輸入輸出為二元值 ( 0、1 )時，W更新公式 ( 4用於取整數，可有可無 )： 
  
     <img src="https://render.githubusercontent.com/render/math?math=\Delta w_{ij} = 4 (x_{i}-{1 \over 2}) * (x_{j}-{1 \over 2})">
     

     
* **神經網路架構圖：**  
  <img src="https://i.imgur.com/AtccqVU.png">  

### 演算法步驟
> 下述的「學習階段」、「回想階段」之相關數學證明請參考原始Paper
#### 1. 學習階段
此程式採用Hebbian rule學習法中的雙極值 ( -1、1 )輸入輸出，參數簡介：
* N筆輸入向量，每一筆有P個維度，表示成 x

* W為P x P的矩陣，預設為0矩陣：避免正回授

* I為單位矩陣：除以P是為了簡化參數，可有可無 

<img src="https://render.githubusercontent.com/render/math?math=x_i=[x_{i1},...,x_{ip}]"> , <img src="https://render.githubusercontent.com/render/math?math=i=1, 2,...,N">

W 即透過下式來學習：

<img src="https://render.githubusercontent.com/render/math?math=W = \begin{bmatrix}w_{11} \quad \dots \quad w_{1p} \\ \vdots \quad \ddots \quad \vdots \\ w_{p1} \quad \dots \quad w_{pp} \end{bmatrix} ={1 \over p} \sum_{k=1}^{N}x_k*{x_k}^T-{N \over p}I">

W訓練一次就完成了!! 。另外此處與簡介倒數第二點所提的公式是一樣的，倒數第二點表達的是單個鍵結值的單次更新，可以透過矩陣與sigma來表示全部資料的更新。此處很不好理解，必須用一點想像力，如果有疑問可以來信詢問。

> 為什麼要減去單位矩陣？為了讓W的對角為0，Hopfield在原始Paper中，神經元並不會連到自己

至於每個神經元的閥值有兩種設定方法( θ表示閥值；j表示第j個神經元 )：
* 全部神經元皆設定為0

  <img src="https://render.githubusercontent.com/render/math?math=\theta_j=0, j=1,...,P">
  
* j 神經元的閥值設為其他神經元連接到 j 神經元的鍵結值總和

  <img src="https://render.githubusercontent.com/render/math?math=\theta_j=\sum_{i=1}^{p}w_{ji}, j=1,...,P">
  
#### 2. 回想( 聯想 )階段
當網路訓練好後就要進入回想階段，假設一個新的輸入X(0)，0表示時間點。運算 X(1) = W * X(0)，產生X(1)，而W * X(0)內的每個值需要經過激勵函數在輸出成X(1)，激勵函數如下( j表示第j個神經元的值 )：

<img src="https://render.githubusercontent.com/render/math?math=x_j(n%2B1) =  sgn(\sum_{i=1}^{p}w_{ji}*x_i(n)-\theta_j) = sgn(u_j(n)-\theta_j) = \left\{\begin{array}{r}1 \quad if \quad u_j(n)-\theta_j > 0 \\x_j(n) \quad if \quad u_j(n)-\theta_j = 0\\-1 \quad if \quad u_j(n)-\theta_j < 0 \end{array} \right.">

整個聯想過程可以寫成： <img src="https://render.githubusercontent.com/render/math?math=x(0) \to \dots \to x(n) \to x(n%2B1)">
而當 <img src="https://render.githubusercontent.com/render/math?math=x(n) = x(n%2B1)">則聯想過程停止。

> 有興趣可參考國立聯合大學-陳士杰老師的講義，附件中的「Hopfield intro」pdf

# 8 ROOKS

## BÁO CÁO CÁ NHÂN

**Môn: Trí Tuệ Nhân Tạo**

**GVHD: TS. Phan Thị Huyền Trang**

| Sinh viên thực hiện | MSSV |
|---------------------|------|
| **Lương Quang Lâm** | 23110121 |


---

## GIỚI THIỆU

**8 Rooks AI** là một trò chơi mô phỏng trực quan các **thuật toán tìm kiếm trong Trí Tuệ Nhân Tạo**, được xây dựng trên bài toán **8 quân xe (8 Rooks Problem)**.

Mục tiêu của trò chơi:
- Giúp người học **hiểu và quan sát trực quan** cách hoạt động của các nhóm thuật toán tìm kiếm khác nhau.
- So sánh **hiệu năng (thời gian, số trạng thái được duyệt, số trạng thái được sinh ra)** giữa các thuật toán.

---

## PHÂN TÍCH PEAS

| Thành phần | Mô tả |
|-------------|-------|
| **Performance (Hiệu năng)** | Thời gian chạy, số node mở rộng, visited, frontier, và khả năng tìm lời giải nhanh nhất |
| **Environment (Môi trường)** | Bàn cờ n×n (3 ≤ n ≤ 8) – trạng thái được biểu diễn bằng hoán vị vị trí các quân xe; tĩnh, rời rạc, xác định, quan sát đầy đủ |
| **Actuators (Bộ truyền động)** | Đặt quân xe vào các vị trí hợp lệ trên bàn cờ |
| **Sensors (Bộ cảm biến)** | Phát hiện trạng thái hiện tại, goal, và các vị trí hợp lệ không bị tấn công |

---

## CÁC NHÓM THUẬT TOÁN

**Lưu ý**: Do vấn đề về bộ nhớ nên lúc sinh trạng thái trong tất cả các thuật toán được sử dụng hầu như đều sử dụng sinh theo hàng.

Dự án chia thành **5 nhóm thuật toán chính**.

### **Tìm Kiếm Không Có Thông Tin**

**1. Breadth-First Search (BFS)** – tìm theo chiều rộng  
- Tìm kiếm theo chiều rộng (Breadth First Search) sử dụng cấu trúc hàng đợi queue (FIFO) để chứa các trạng thái được sinh ra.

- Hướng dẫn

      Đầu vào: Bài toán 8 quân xe, trạng thái ban đầu, queue.
      Đầu ra: Giải pháp tìm thấy trạng thái mục tiêu.
      Đưa vào queue trạng thái ban đầu.
      Loop:
          1. Lấy một trạng thái ra khỏi đầu hàng đợi.
          2. Nếu là trạng thái mục tiêu thì trả về kết quả.
          3. Ngược lại, sinh ra tất cả các trạng thái kế tiếp hợp lệ bằng cách đặt quân xe vào các cột chưa bị chiếm.
          4. Thêm các trạng thái mới sinh vào cuối hàng đợi.
          5. Quay lại vòng lặp Loop.
  
- Minh họa áp dụng thuật toán
![BFS Demo](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/gif_sample/bfs.gif)
  
**2. Depth-First Search (DFS)** – tìm theo chiều sâu
- Tìm kiếm theo chiều sâu (Depth First Search) sử dụng cấu trúc ngăn xếp stack (LIFO) để chứa các trạng thái sinh ra.
  
- Hướng dẫn

      Đầu vào: Bài toán 8 quân xe, trạng thái ban đầu, stack.
      Đầu ra: Giải pháp tìm thấy trạng thái mục tiêu.
      Đưa vào stack trạng thái ban đầu.
      Loop:
          1. Lấy một trạng thái ra khỏi đỉnh ngăn xếp.
          2. Nếu trạng thái này là trạng thái mục tiêu → trả về kết quả.
          3. Ngược lại, sinh ra các trạng thái con hợp lệ bằng cách đặt quân xe vào các cột chưa bị chiếm.
          4. Thêm các trạng thái mới vào đỉnh ngăn xếp.
          5. Quay lại vòng lặp Loop.
  
- Minh họa áp dụng thuật toán
![DFS Demo](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/gif_sample/dfs.gif)
  
**3. Depth-Limited Search (DLS)** – DFS giới hạn độ sâu
- Thuật toán tìm kiếm theo chiều sâu giới hạn (Depth Limited Search) là phiên mở rộng của thuật toán DFS.
- Khi gặp cây có độ sâu vô hạn mà mục tiêu chỉ nằm ở giữa thân, trong khi đó DFS sẽ duyệt đến độ sâu cuối cùng cho theo cơ chế LIFO. Nên để để tối ưu với trường hợp trên thuật toán DLS được sử dụng duyệt với độ sâu với hạn cho đến khi tìm được mục tiêu. <br>

  Ưu điểm: có thể trách khỏi tình trạng duyệt vô hạn và tránh được việc ngốn bộ nhớ. <br>
  
  Nhược điểm: Thuật toán duyệt với độ sâu cố định sẽ gặp phải tình trạng không tìm được mục tiêu vì chỉ duyệt đến độ sâu   định sẵn nhưng mục tiêu có thể nằm ở sâu hơn. Thuật toán này cũng khá tốn bộ nhở vì thực hiện gọi đệ quy nhiều lần. 

- Hướng dẫn
  
      Đầu vào: Bài toán 8 quân xe, trạng thái ban đầu, độ sâu.
      Đầu ra: giải pháp từ trạng thái ban đầu đến trạng thái mục tiêu.
      Thực hiện gọi hàm đệ quy và truyền vào vấn đề của bài toán, trạng thái ban đầu và độ sâu.
      Hàm đệ quy:
          1. Nếu đạt đến trạng thái mục tiêu → trả về kết quả.
          2. Nếu đạt đến giới hạn độ sâu (depth == 0) → cắt nhánh (“cutoff”)..
          3. Ngược lại:
                3.1. Sinh các trạng thái con bằng cách đặt quân xe vào các cột chưa bị chiếm.
                3.2. Gọi đệ quy để tiếp tục tìm kiếm ở mức sâu hơn.
                3.3. Nếu tất cả nhánh đều bị cắt → trả về “cutoff”; nếu tìm thấy lời giải → trả về trạng thái mục tiêu.
 
- Minh họa áp dụng thuật toán
![DLS Demo](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/gif_sample/dls.gif)

**4. Iterative Deepening (IDS)** – tìm lặp tăng dần độ sâu
- Thuật toán tìm kiếm theo chiều sâu lặp sâu dần (Iterative Deepening Search) là sự kết hợp của thuật toán BFS và DFS. Sử dụng với độ sâu lặp đi lặp lại đến khi nào tìm được trạng thái mục tiêu thì dừng lại.

- Hướng dẫn IDS với DLS

      Đầu vào: Bài toán 8 quân xe, trạng thái ban đầu, thuật toán DLS.
      Đầu ra: Giải pháp từ trạng thái ban đầu đến trạng thái mục tiêu.
      Loop độ sâu tăng từ 1 đến n:
          1. Gọi thuật toán tìm kiếm giới hạn độ sâu (DLS) với giới hạn hiện tại.
          2. Nếu DLS trả về lời giải thực sự (không phải None hay "cutoff") → dừng vòng lặp và lưu kết quả.
 
- Minh họa áp dụng thuật toán
![IDS Demo](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/gif_sample/ids.gif)

**5. Uniform Cost Search (UCS)** – chi phí đồng đều
- Thuật toán tìm kiếm chi phí đồng đều (Uniform Cost Search) để lưu trữ các trạng thái được sinh ra. Tìm kiếm các chi phí trên đường đi có chi phí nhỏ nhất đến trạng thái mục tiêu.
  
  Chi phí mà UCS sử dụng là Path Cost (chi phí từ trạng thái ban đầu đến trạng thái hiện tại).
  
- Hướng dẫn UCS

      Đầu vào: Bài toán 8 quân xe, trạng thái ban đầu, priority queue.
      Đầu ra: Giải giáp từ trạng thái ban đầu đến trạng thái mục tiêu với chi phí tốt nhất.
      Đưa trạng thái ban đầu vào Priority Queue.
      Loop:
          1. Lấy từ Priority Queue trạng thái có chi phí tốt nhất (Chí phí nhỏ nhất).
          2. Nếu trạng thái đó là trạng thái mục tiêu thì dừng.
          3. Sinh các trạng thái đồng thời tính chi phí Path Cost cho từng trạng thái đó.
          4. Sau khi sinh xong đưa vào Priority Queue và quay lại Loop.

- Minh họa áp dụng thuật toán
![UCS Demo](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/gif_sample/ucs.gif)

**6. Nhận xét, đánh giá**
![Uninform Statistic](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/statistic_sample/uninformed.png)
- Về hiệu quả không gian (Số node đã mở rộng)

  Xét về không gian tìm kiếm, **Uniform Cost Search (UCS)** tỏ ra vượt trội nhất. Nguyên nhân chính là do hàm chi phí đã biến nó thành một thuật toán tìm kiếm có thông tin (informed search), giúp nó đi thẳng đến lời giải mục tiêu mà không cần duyệt qua các nhánh không cần thiết.
  
  Ngược lại, **Iterative Deepening Search (IDS)** là thuật toán kém hiệu quả nhất do phải liên tục duyệt lại các node ở những tầng nông. Các thuật toán còn lại như **BFS, DFS, và DLS** đều là tìm kiếm "mù", phải duyệt qua một không gian lớn hơn rất nhiều so với **UCS** để tìm ra lời giải.

- Về hiệu quả thời gian (Thời gian thực thi)

  Về mặt thời gian, kết quả cũng phản ánh tương tự. **UCS** hoàn thành nhanh nhất, việc thu hẹp không gian tìm kiếm đã giúp giảm thiểu đáng kể thời gian xử lý. Trong khi đó, **IDS** là thuật toán chậm nhất, trực tiếp là hệ quả của việc phải mở rộng số lượng node lớn nhất. **DFS và DLS** nhanh hơn **BFS** vì chúng nhanh chóng đi sâu xuống một nhánh để tìm lời giải, thay vì phải duyệt toàn bộ các node ở mỗi tầng như **BFS**.

### **Tìm Kiếm Có Thông Tin**

**1. Greedy Best-First Search** – tìm theo hướng ước lượng tốt nhất
- Thuật toán Greedy Search sử dụng cấu trúc Priority Queue để lưu các trạng thái sinh ra từ bàn cờ. Mỗi lần lấy trạng thái ra Greedy chọn trạng thái có chi phí tốt nhất (chi phí thấp nhất).
  
  Thuật toán này sử dụng hàm ước lượng chi phí (Herurictics) để tính chi phí cho các trạng thái sinh ra.
   
  Ước lượng chi phí từ trạng thái ban đầu đến trạng thái mục tiêu.
  
  Thuật tóa Greedy muốn tối ưu đòi hỏi ta phải xây dựng hàm ước lượng chi phí gần đúng nhất so với trạng thái mục tiêu.
  
- Hướng dẫn

      Đầu vào: Bài toán 8 quân xe, trạng thái ban đầu, thuật toán GS, hàm Herurictics.
      Đầu ra: Giải pháp từ trạng thái ban đầu đến trạng thái mục tiêu.
      Đưa vào priorityQueue trạng thái ban đầu kèm chi phí.
      Loop:
          1. Lấy từ priorityQueue trạng thái tốt nhất (có chi phí thấp nhất).
          2. Nếu trạng thái lấy ra là trạng thái mục tiêu thì dừng và trả về kết quả.
          3. Sinh các trạng thái tiếp theo và tính ước lượng chi phí cho các trạng thái sinh ra.
          4. Đưa các trạng thái sinh ra đó vào priorityQueue.
          5. Quay lại vòng lặp Loop.

- Minh họa áp dụng thuật toán
![GBF Demo](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/gif_sample/greedy.gif)

**2. A\* Search** – kết hợp chi phí thực tế và heuristic  
- Thuật toán A* (A Star Search) sử dụng cấu trúc lưu trữ và ý tưởng gần giống với thuật toán Greedy. Chỉ khác ở bên Greedy chỉ sử dụng hàm Herurictics để tính chi phí còn A* sử dụng hai hàm Herurictics và Path Cost để tính chi phí.
  
  Thuật toán A* muốn tối ưu phải xây dụng 2 hàm tính chi phí có tính chính xác cao.
    
  Nếu xây dụng hàm Path Cost và Herurictics chưa chính xác thì thuật toán A* có thể chạy lâu hơn hàm Greedy.
    
  Hàm tính chi phí: f(x) = g(x) + h(x)
  
        Trong đó: 1. f(x) là tổng các chi phí.
                  2. g(x) là chi phí từ trạng thái ban đầu đến hiện tại (Path Cost).
                  3. h(x) là chi phí từ trạng thái hiện tại đến mục tiêu (Herurictics).

- Hướng dẫn

      Đầu vào: Bài toán 8 quân xe, trạng thái ban đầu, thuật toán AS, các hàm tính chi phí.
      Đầu ra: Giải pháp từ trạng thái ban đầu đến trạng thái mục tiêu.
      Đưa trạng thái ban đầu kèm chi phí vào priorityQueue.
      Loop:
          1. Lấy từ priorityQueue trạng thái tốt nhất (có tổng chi phí nhỏ nhất).
          2. Nếu trạng thái lấy ra đó là trạng thái mục tiêu thì return.
          3. Sinh các trạng thái kế tiếp và tính chi phí f(x) cho trạng thái đó.
          4. Đưa trạng các trạng thái sinh ra vào priorityQueue.
          5. Quay lại vòng lặp Loop.

- Minh họa áp dụng thuật toán
![ASTAR Demo](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/gif_sample/astar.gif)

**3. Nhận xét, đánh giá**
![Inform Statistic](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/statistic_sample/informed.png)
- Về hiệu quả không gian (Số node đã mở rộng)

  Trong nhóm này, **Greedy Best-First Search** tỏ ra hiệu quả hơn hẳn so với **A Star**. Điều này xảy ra vì **Greedy Search** hoạt động theo nguyên tắc "tham lam": nó chỉ quan tâm đến giá trị *heuristic* (ước tính khoảng cách tới đích) và luôn chọn đường đi có vẻ tốt nhất ở thời điểm hiện tại. Ngược lại, thuật toán **A Star** cân bằng giữa chi phí thực tế từ điểm bắt đầu (g(n)) và giá trị *heuristic* (h(n)). Việc phải tính toán và cân nhắc cả hai yếu tố này khiến A* phải khám phá nhiều node hơn để đảm bảo tìm được đường đi tối ưu.

- Về hiệu quả thời gian (Thời gian thực thi)

  Hiệu quả về thời gian cũng phản ánh trực tiếp số lượng node đã mở rộng. **Greedy Best-First Search** hoàn thành rất nhanh nhờ vào chiến lược đơn giản và tập trung của nó. Trong khi đó, **A Star** thì lâu hơn rất nhiều do chi phí tính toán phức tạp hơn và không gian tìm kiếm lớn hơn mà nó phải duyệt qua. Mặc dù chậm hơn, sự đánh đổi của A* là nó đảm bảo tìm ra lời giải tối ưu nhất (chi phí thấp nhất), điều mà Greedy Search không thể đảm bảo.

### **Tìm Kiếm Cục Bộ**

**1. Hill Climbing** – leo đồi theo giá trị heuristic
- Thuật toán leo đồi (Hill Climbing) sử dụng cấu trúc Priority Queue để lưu trữ các trạng thái sinh ra. Nhưng thuật toán này khác với các thuật toán khác trong nhóm thuật toán tìm kiếm có thông tin là mỗi lần sinh trạng thái đưa vào queue và sau khi chọn được trạng thái tốt nhất thì các trạng thái còn lại trong queue không được sử dụng tiếp mà bị xóa đi.

  Thuật toán này rất dễ bị vướng ở cục bộ bởi vị nó chỉ chọn trạng thái tốt nhất từ các trạng thái sinh ra từ trạng thái hiện tại, nếu như trạng thái tốt nhất chọn ra không tốt hơn trạng thái hiện tại thì chương trình bị mắc ở cục bộ.
  
  Trong thuật toán này có sử dụng hàm Herurictics để tính chi phí.

- Hướng dẫn

      Đầu vào: Bài toán 8 quân xe, trạng thái ban đầu, hàm Herurictics, thuật toán Hill Climbing.
      Đầu ra: Giải pháp từ trạng thái ban đầu đến trạng thái mục tiêu.
      Lưu trạng thái ban đầu vào H
      Loop:
          1. Kiểm trạn trạng thái H có phải trạng thái mục tiêu không, nếu là mục tiêu thì trả về kết quả.
          2. Khởi tạo priorityQueue rỗng.
          3. Sinh các trạng thái lân cận từ H, tính chi phí cho các trạng thái lân cận đó và đưa vào priorityQueue.
          4. Nếu priorityQueue là rỗng thì dừng.
          5. Chọn M từ priorityQueue là trạng thái có chi phí thấp nhất.
          6. Nếu chi phí của M > chi phí của H thì dừng.
          7. Gán H = M và tiếp lục lặp Loop.

- Minh họa áp dụng thuật toán
![HILL CLIMBING Demo](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/gif_sample/hill.gif)
  
**2. Simulated Annealing** – mô phỏng quá trình tôi kim loại
- Thuật toán mô phỏng quá trình tôi kim loại (Simulated Annealling) còn được gọi là thuật toán mô phỏng luyện kim. Đây là phiên bản cải tiến hơn của Hill Climbing để tránh việc tìm kiếm trong cục bộ mà đưa dần tiếp kiếm ra toàn  cục với một xác xuất nào đó.

  Thuật toán này được tối ưu khi ta xây dụng hàm tính nhiệt độ một cách chính xác và hàm tính chi phí phải tối ưu. Làm tăng khả năng tìm kiếm ra toàn cục hơn.

- Hướng dẫn

      Đầu vào: Bài toán 8 quân xe, trạng thái ban đầu, thuật toán Simulated Annealling, hàm tính chi phí.
      Đầu ra: Giải pháp từ trạng thái ban đầu đến mục tiêu.
      Lưu trạng thái ban đầu là H.
      Loop t = 1:
          1. Kiểm trạn trạng thái H có phải trạng thái mục tiêu không, là mục tiêu thì trả về kết quả.
          2. Xây dựng hàm tính tính độ T dựa trên t.
          3. Nếu T giảm về 0 thì return "Không tìm thấy mục tiêu".
          4. Khởi tạo priorityQueue rỗng.
          5. Sinh các trạng thái lân cận từ H, tính chi phí cho các trạng thái lân cận đó và đưa vào priorityQueue.
          6. Nếu priorityQueue là rỗng thì return "Không thể sinh tiếp trạng thái".
          7. Chọn M từ priorityQueue là trạng thái có chi phí thấp nhất.
          8. Nếu chi phí của M > chi phí của H:
              8.1. Tính xác xuất theo công thức exp(−Δ(chi phí M, chi phí H)/T).
              8.2. Chọn một xác xuất random.
              8.3. Nếu xác suất tính theo công thức > xác xuất random thì chấp nhận trạng thái xấu: H = M.
              8.4. Quay lại vòng lặp Loop.
          9. Gán H = M và tiếp tục lặp Loop.

- Minh họa áp dụng thuật toán
![SA Demo](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/gif_sample/sa.gif)

**3. Genetic Algorithm (GA)** – tiến hóa tự nhiên
- Thuật toán tiến hóa tự nhiên (Genetic ALgorithms) được thiết lập theo các cơ chế sau: Khởi tạo quần thểm, chọn lọc quần thể, lại ghép và độ biến gen các cá thể trong quần thể.
  
  Thuật toán này  khó tìm ra mục tiêu nếu các các thể trong quần  thể thiếu tính đa dạng và quần thể ít cá thể.
  
  Do vậy để thuật toán này tối ưu hơn ta cần tăng số lượng cá thể trong quần thể, tăng tính  đa dạng của quần thể.
  
- Hướng dẫn
  
      Đầu vào: Bài toán 8 quân xe, tập quần thể ban đầu, thuật toán GA.
      Đầu ra: Giải pháp từ trạng thái ban đầu đến trạng thái mục tiêu.
      Lưu ý: các quần thể là một tập các trạng thái của bàn cờ.
      Khởi tạo quần thể chưa 6 trạng thái bàn cờ ngẫu nhiên.
      Loop với số lượng mã Gen cố định:
          1. Chọn lọc 2 trạng thái tốt và random ngẫu nhiên một trạng thái xấu trong quần thể ban đầu.
          2. Đem các trạng thái chọn lọc đi lai (lai từng cặp trạng thái khác nhau).
              2.1. khởi tạo tỉ lệ lai.
              2.2. Với mỗi cột trong trạng thái có một xác xuất random.
              2.3. Nếu xác xuất random < tỉ lệ lai thì ta sẽ hoán đổi các cột giữa 2 trạng thái với nhau.
          3. Đem các trạng thái vừa lai xong đi đột biến.
              3.1. Khởi tạo tỉ lệ đột biến.
              3.2. Với mỗi cột trong trạng thái có một giá trị đột biến random.
              3.3. Nếu giá trị đó < tỉ lệ  đột biến thì đưa tất cả giá trị trong vột về 0 và random ngẫu nhiên một vị trí đặt 1.
          4. Đưa các trạng thái trên vào quần thể mới.
          5. Nếu quần thể mới chưa đủ 6 trạng thái thì tiếp tục quá trình trên.
          6. Nếu quần thể mới đủ 6 trạng thái thì kiểm tra trong quần thể mới có mục tiêu không nếu có thì return.

- Minh họa áp dụng thuật toán
![GENETIC Demo](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/gif_sample/genetic.gif)

**4. Beam Search** – giữ k trạng thái tốt nhất ở mỗi bước
- Thuật toán Beam Search dựa trên thuật toán tìm kiếm theo chiều rộng nhưng thay vì lấy hết trạng thái sinh ra thì ở đây Beam chỉ lấy k trạng thái tốt nhất. Beam sử dụng hàm Herurictics để tính chi phí và dùng  queue giống như BFS để lưu trạng thái sinh ra.

  Do đó thuật toán này có thể được coi là phiên bản tối ưu của BFS.
  
  Nhưng để thuật  toán này tối ưu được ta cũng phải xây dựng hàm tính chi phí phải tối ưu.

- Hướng dẫn

      Đầu vào: Bài toán 8 quân xe, trạng thái ban đầu, thuật toán BS, hàm herurictics.
      Đầu ra: giải pháp từ trạng thái ban đầu đến mục tiêu.
      đưa vào queue trạng thái ban đầu.
      Loop:
          1. Lấy ra khỏi queue một trạng thái theo cơ  chế (FIFO).
          2. Nếu trạng thái lấy ra là mục tiêu thì return.
          3. Tạo một priorityQueue rỗng.
          4. sinh các trạng thái từ trạng thái lấy ra và tính chi phí cho các trạng thái đó.
          5. Đưa vào priorityQueue các trạng thái sinh ra đó.
          6. Lấy ra khỏi priorityQueue k trạng thái có chi phí thấp nhất.
          7. Đưa k trạng thái tốt nhất đó vào queue và quay lại Loop.

- Minh họa áp dụng thuật toán
![BEAM Demo](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/gif_sample/beam.gif)

**5. Nhận xét, đánh giá**
![Local Statistic](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/statistic_sample/local.png)
- Về hiệu quả không gian (Số node đã mở rộng)

  Đối với nhóm tìm kiếm cục bộ, **Hill Climbing** và **Simulated Annealing** là hai thuật toán tiết kiệm không gian nhất. Cả hai đều hoạt động bằng cách chỉ xem xét các "hàng xóm" trực tiếp của trạng thái hiện tại, giúp không gian tìm kiếm được giữ ở mức tối thiểu. Ngược lại, **Genetic Algorithm** và **Beam Search** mở rộng nhiều node hơn đáng kể. Lý do là chúng duy trì và làm việc với một tập hợp nhiều trạng thái cùng lúc — một "quần thể" trong **Genetic Algorithm** và một "chùm" (beam) trong **Beam Search** — thay vì chỉ một trạng thái duy nhất.

- Về hiệu quả thời gian (Thời gian thực thi)

  Về thời gian, **Hill Climbing** và **Simulated Annealing** tiếp tục dẫn đầu nhờ sự đơn giản của chúng. **Simulated Annealing** chậm hơn một chút do phải thực hiện thêm các phép tính xác suất để quyết định có nên chấp nhận một bước đi tệ hơn hay không. **Genetic Algorithm** là thuật toán chậm nhất với. Chi phí thời gian cao này đến từ việc phải quản lý cả một quần thể, thực hiện các thao tác phức tạp như lựa chọn, lai ghép và đột biến qua nhiều thế hệ. **Beam Search** nằm ở giữa, nhanh hơn Genetic Algorithm vì nó chỉ giữ lại một số lượng trạng thái tốt nhất cố định ở mỗi bước, giảm bớt gánh nặng tính toán.

### **Môi Trường Phức Tạp**

**1. Nondeterministic / AND-OR Search** – hành động không chắc chắn 
- Thuật toán And-Or Tree Search có thể được sử dụng chung với các nhóm thuật toán có thông tin và không có thông tin. Trong bài toán này thuật toán này được sử dụng chung với thuật toán DFS. Ban đầu thuật toán sẽ gọi hàm Or sẽ xác định việc sinh ra các hành động và đảm bảo bột trong các hành động là mục tiêu thì trả về. Sau khi quyết định được hành động gọi hàm And và truyền vào một tập các trạng thái sinh ra từ hành động đặt và phải thõa mãn các trạng thái sinh ra từ hành động Or phải tìm thấy mục tiêu.

  Thuật toán là sử dụng ý tưởng giống các phép toán tử logic trong toán học. And trả về đúng nếu cả hai cùng đúng còn Or chỉ đúng khi một trong hai đúng.

- Hướng dẫn

      Đầu vào: Bài toán 8 quân xe, trạng thái ban đầu, thuật toán And-Or.
      Đầu ra: Giải pháp tìm ra tập mục tiêu hợp lệ.
          1. Gọi hàm Or truyền vào trạng thái ban đầu và đường đi
          2. Hàm Or:
              2.1. kiểm tra xem trạng thái truyền vào là mục tiêu thì trả về trạng thái đó
              2.2. Kiểm tra xem có chu trình hay không
              2.3. Nếu không có chu trình thì thêm trạng thái vào path.
              2.4. Gọi hàm And và truyền vào tập trạng thái sinh ra từ hành động được chọn.
              2.5. Nếu giá trị mà hàm And trả về không phải False thì xóa trạng thái đó ra khỏi path và return trạng thái đó.
              2.6. Reuturn False nếu không thể gọi tiếp hàm And.
          3. Hàm And:
              3.1. Loop mỗi trạng thái trong tập trạng thái được nhận:
                  - Gọi hàm Or truyền vào trạng thái đang xét.
                  - nếu hàm Or trả về False thì return False
              3.2. Return tập trạng thái đều là mục tiêu.

- Minh họa áp dụng thuật toán
![ANDOR Demo](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/gif_sample/andor.gif)

**2. Unobservable Search** – môi trường không quan sát được
- Giải thuật tìm kiếm trong môi trường không nhìn thấy ban đầu sẽ không xác định được vị trí hay có thông tin rằng mình đang ở đâu mà phải xây dựng một tập niềm tin ban đầu và muốn biết được kết quả thì cũng xây dựng nên tập niềm tin mục tiêu.

  Ở thuật toán nào khó tìm thấy mục tiêu đối với bài toán 8 quân xe khi mà tập niềm tin mục tiêu đưa vào quá ít, và có thể là không tìm ra được.
  
  Đối với thuật toán này muốn tối ưu thuật toán thif ta phải xây dựng niềm tin ban đầu có nhiều trạng thái mục tiêu nhất và niềm tin ban đầu phải có kích thước nhỏ. Để giảm dung lượng bộ nhớ giúp chương trình chạy nhanh hơn.
  
  khi xây tập niềm tin ban đầu và niềm tin mục tiêu phải bảo đảm các tập có số trạng thái > 2.
  
  Ở trong chương trình này được xây dựng dựa trên thuật toán DFS.

- Hướng dẫn

      Đầu vào: bài toán 8 quân xe, niềm tin ban đầu, niềm tin kết thúc.
      Đầu ra: Tập các trạng thái đặt quân xe hợp lệ.
        1. Xây dựng niềm tin ban đầu.
        2. Xây dựng niềm tin kết thúc.
        3. Đưa niềm tin ban đầu vào stack.
        4. Xây dưng tập hành động: di chuyển và đặt
        5. Loop:
            5.1. Lấy 1 phần tử đầu tiên ra khỏi stack (LIFO).
            5.2. Kiểm tra các trạng thái trong phần tử: nếu tất cả các trạng thái đều nằm trong niềm tin ban đầu thì dừng.
            5.3. thực hiện các hành động lên phần tử lấy ra đó.
            5.4. mội lần thực hiện 1 hành động sinh ra một tập các trạng thái của bàn cờ và đưa vào stack.

- Minh họa áp dụng thuật toán
![UNOB Demo](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/gif_sample/unobservable.gif)

**3. Partial Observable Search** – quan sát một phần
- Giải thuật tìm kiếm trong môi trường nhìn thấy một phần có thể coi là phiên bản tối ưu của phiên bản tìm kiếm trong môi trường không nhìn thấy. Thay vì không nhìn thấy mà đi tìm kiếm mục tiêu mù quáng thì ở đây sẽ nhìn thấy được một hoặc 2 vị trí hoặc có thể hơn trong niềm tin ban đầu.

  Nhưng ở thuật toán này không sử dụng với thuật toán DFS mà xây dựng dựa trên thuật toán Greedy Search.
  
  Tương tự như Greedy thì để thuật toán tối ưu phải xây dựng hàm ước lượng chi phí một cách tối ưu nhất và ngoài ra ta còn cần xây dựng thêm niềm tin mục tiêu đa dạng hơn.

- Hướng dẫn

      Đầu vào: Bài toán 8 quân xe, niềm tin ban đầu, niềm tin kết thúc, nhìn thấy được một quân xe trên bàn cờ.
      Đầu ra: tập các trạng thái đặt 8 quân xe hợp lệ.
          1. Xây dựng niềm tin ban đầu và các trạng thái phải chứa quân xe đã biết trước.
          2. Xây dựng niềm tin mục tiêu.
          3. Xây dựng tập hành động: di chuyển và đặt.
          4. đưa niềm tin ban đầu vao priorityQueue.
          5. Loop:
              5.1. Lấy phần tử có chi phí thấp nhất ra khởi priorityQueue.
              5.2. Kiểm tra các trạng thái trong phần tử thuộc trong niềm tin mục tiêu không: nếu tất cả đều thuộc thì dừng.
              5.3. Từ các hành động sinh các tập trạng thái và ước lượng chi phí cho các tập đó.
              5.4. Đưa các tập trạng thái sinh ra vào priorityQueue.

- Minh họa áp dụng thuật toán
![PARTOB Demo](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/gif_sample/partialobs.gif)

**4. Nhận xét, đánh giá**
![Complex Statistic](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/statistic_sample/complex.png)
- Về hiệu quả không gian (Số node đã mở rộng)

  Trong các môi trường phức tạp, **Partial Observable** (Quan sát được một phần) là hiệu quả nhất. Điều này là do thuật toán có một phần thông tin về trạng thái (ví dụ: biết trước vị trí của vài con xe đầu tiên), giúp thu hẹp không gian tìm kiếm một cách đáng kể. Ngược lại, môi trường **Nondeterministic** (Không xác định) là tốn kém nhất. Nguyên nhân là vì mỗi hành động có thể dẫn đến nhiều kết quả không thể đoán trước, và thuật toán AND-OR phải tìm ra một kế hoạch dự phòng hoạt động được với tất cả các khả năng, dẫn đến một cây tìm kiếm khổng lồ. Môi trường **Unobservable** (Không quan sát được) mở rộng rất ít nhưng lại không tìm thấy lời giải, cho thấy thuật toán đã nhanh chóng thất bại do không có thông tin cảm biến để định hướng.

- Về hiệu quả thời gian (Thời gian thực thi)

  Hiệu quả về thời gian cũng cho thấy kết quả tương tự. **Partial Observable** là nhanh nhất , khẳng định lợi ích của việc có thông tin, dù chỉ là một phần. Môi trường **Nondeterministic** chậm nhất. Thuật toán **Unobservable** kết thúc nhanh (0.11 ms) nhưng đó là thời gian của một lần chạy thất bại, không phải là một chỉ số hiệu suất thành công. Tóm lại, lượng thông tin mà agent có về môi trường ảnh hưởng trực tiếp và mạnh mẽ đến hiệu quả tìm kiếm.

### **Tìm Kiếm Thỏa Mãn Ràng Buộc (CSP)**

**1. Backtracking** – thử-sai và quay lui
- CSP ban đầu cần tạo các tập biến, tập giá trị và tập ràng buộc sau mới gọi hàm bactracking.

  Để giảm bớt thời gian chạy và bộ nhớ cũng như tăng khả năng tìm thấy thì thuật toán này không tìm ra một mục tiêu cụ thể nào đó mà chỉ tìm ra một trạng thái đặt 8 quân xe hợp lệ.
  
- Hướng dẫn

      Đầu vào: Bài toán 8 quân xe, tập biến, tập giá trị, tập ràng buộc.
      Đầu ra: Trạng thái đặt xe phù hợp.
          1. Xây dựng tập biến chứa 8 quân xe.
          2. Xây dựng tập giá trị là các vị trí có thể đặt của quân xe.
          3. Xây dựng tập ràng buộc: không đặt cùng hàng và cùng cột.
          4. Gọi hàm Backtracking và truyền vào tập biến, tập giá trị và tập ràng buộc.
          5. Hàm Backtracking:
              5.1. Kiểm tra xem bàn cờ có hợp lệ không nếu hợp lệ thì dừng.
              5.2. Chọn ngẫu nhiên một quân xe.
              5.3. Chọn ngẫu nhiên một giá trị từ tập giá trị của quân xe.
              5.4. Đặt quân xe được chọn ngẫu nhiên lên vị trí có giá trị được chọn ngẫu nhiên.
              5.5. Gọi Backtracking
              5.6. Nếu giá trị trả về của hàm Backtracking là một trạng thái hợp lệ thì return
              5.7. Return None

- Minh họa áp dụng thuật toán
![BACKTRACK Demo](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/gif_sample/backtrack.gif)

**2. Forward Checking** – cắt tỉa miền giá trị sau mỗi gán
- Thông qua quá trình quan sát thì thuật toán CSP Backtracking sẽ thử hết tất các các giá trị nằm trong miền điều này dễ dẫn tới việc bộ nhớ quá lớn và tốn thời gian. Để giảm thiểu việc này mỗi lần ta đặt quân xe ra sẽ giới hạn lại tập giá trị, khi đặt quân xe lên sẽ giảm các vị trí mà quân xe đã đặt đó tấn công được. Đây được gọi là thuật toán Forward Checking.

  Thuật toán này có thể xem là phiên bản tối ưu hơn của Backtracking.

- Hướng dẫn

      Đầu vào: Bài toán 8 quân xe, tập biến, tập giá trị, tập ràng buộc.
      Đầu ra: Trạng thái đặt xe phù hợp.
          1. Xây dựng tập biến chứa 8 quân xe.
          2. Xây dựng tập giá trị là các vị trí có thể đặt của quân xe.
          3. Xây dựng tập ràng buộc: không đặt cùng hàng và cùng cột.
          4. Gọi hàm ForwardChecking và truyền vào tập biến, tập giá trị và tập ràng buộc.
          5. Hàm ForwardChecking:
              5.1. Kiểm tra xem bàn cờ có hợp lệ không nếu hợp lệ thì dừng.
              5.2. Chọn ngẫu nhiên một quân xe.
              5.3. Chọn ngẫu nhiên một giá trị từ tập giá trị của quân xe và đặt quân xe lên vị trí có giá trị được chọn.
              5.4. Gọi hàm F để loại bỏ bớt tập giá trị mà chứa các vị trị bị quân xe đã đặt có thể tấn công được.
              5.5. Gọi ForwardChecking.
              5.6. Nếu giá trị trả về của hàm ForwardChecking là một trạng thái hợp lệ thì return.
              5.7. Return None
  
- Minh họa áp dụng thuật toán
![FORWARD Demo](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/gif_sample/forward.gif)

**3. Arc Consistency (AC-3)** – duy trì tính nhất quán cung
- Thuật toán AC-3 được xây dựng dựa trên việc tinh giảm miền giá trị trước khi đưa vào quá trình Backtracking. Mỗi quân xe sẽ có một miền giá trị riêng cho mình, thay vì mỗi lần gọi backtracking sau khi đặt thì mới cắt giảm miền giá trị giống Forward Checking thì AC-3 sẽ chọn lọc ra mỗi miền giá trị riêng thuộc về mỗi quân xe bằng việc thõa mãn ràng buộc nào đó.

- Hướng dẫn

      Đầu vào: Bài toán 8 quân xe, tập biến, tập giá trị và các ràng buộc.
      Đầu ra: Trạng thái đặt 8 quân xe hợp lý.
          1. Xây dựng tập biến.
          2. Xây dựng tập giá trị cho mỗi biến.
          3. Gọi hàm AC3:
              3.1. Tạo các cặp quân xe và đưa vào queue.
              3.2. Gọi hàm revise để kiểm tra: 
                  - Nếu thõa mãn ràng buộc một quân xe sẽ di chuyển trên cùng hàng vùng cột, không có quân xe nào di chuyển trên vị trí con kia. nếu thõa mãn thì return True.
                  - Nếu không thì đưa bớt các giá trị trong miền giá trị không phù hợp vào danh sách để xóa.
              3.3. Nếu hàn revise là True thì kiểm tra:
                  1. Nếu miền giá trị của x đã bị xóa hết thì return False
                  2. Đưa các biến hàng xóm không phải y ghép thành cặp với x và đưa vào queue. 
          4. Sau khi miền giá trị của các quân xe đã bị cắt giảm thì bắt đầu gọi hàm Backtracking để tìm ra mục tiêu.

- Minh họa áp dụng thuật toán
![AC3 Demo](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/gif_sample/ac3.gif)

**4. Nhận xét, đánh giá**
![CSP Statistic](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/statistic_sample/csp.png)
- Về hiệu quả không gian (Số node đã mở rộng)

  Một điểm đáng chú ý là cả ba thuật toán — **Backtracking, Forward Checking, và Arc Consistency (AC-3)** — đều mở rộng cùng một số lượng node. Điều này có thể được giải thích: đối với bài toán 8 con xe, ràng buộc "các con xe không được nằm trên cùng một cột" khá đơn giản. Phép kiểm tra if col not in state cơ bản trong thuật toán **Backtracking** đã đủ mạnh để cắt tỉa các nhánh không hợp lệ một cách hiệu quả. Các kỹ thuật phức tạp hơn như **Forward Checking và AC-3**, mặc dù mạnh mẽ hơn trong các bài toán phức tạp, nhưng trong trường hợp này lại không mang lại lợi ích cắt tỉa nào thêm, dẫn đến việc chúng duyệt qua cùng một không gian tìm kiếm.

- Về hiệu quả thời gian (Thời gian thực thi)

  Sự khác biệt lớn nằm ở thời gian thực thi. **Backtracking** là nhanh nhất vì nó có chi phí xử lý ở mỗi node là thấp nhất. **Forward Checking** chậm hơn vì sau mỗi lần đặt xe, nó phải thực hiện thêm công việc là cập nhật "miền giá trị" (các cột hợp lệ) cho các hàng còn lại. **Arc Consistency (AC-3)** là chậm nhất. Lý do là ở mỗi bước, nó phải chạy một thuật toán tốn kém để kiểm tra và thực thi tính nhất quán trên tất cả các cặp biến, một sự đầu tư quá mức cần thiết cho bài toán này. Kết quả cho thấy, đối với các bài toán có ràng buộc đơn giản, một thuật toán cơ bản như **Backtracking** có thể hiệu quả hơn các phương pháp phức tạp do chi phí tính toán thấp hơn.

### **Tổng quát**
![Group](https://github.com/QuangLam0208/8-rooks-ai/blob/main/assets/pics/statistic_sample/bestgroup.png)
- Về hiệu quả không gian (Số node đã mở rộng)

  Khi so sánh các thuật toán hiệu quả nhất từ mỗi nhóm, sự khác biệt về chiến lược tìm kiếm trở nên cực kỳ rõ rệt. **Partial Observable** (Quan sát được một phần) là thuật toán vượt trội nhất, mở rộng rất ít nhờ vào việc có sẵn thông tin ban đầu để định hướng tìm kiếm. Các thuật toán dựa trên heuristic như Greedy **Best-First và Hill Climbing** cũng cực kỳ hiệu quả, luôn đi theo hướng hứa hẹn nhất để đến mục tiêu. Ngược lại, **Backtracking**, đại diện cho phương pháp duyệt vét cạn có hệ thống, phải khám phá một không gian tìm kiếm khổng lồ. Ngay cả **Uniform Cost**, vốn được hưởng lợi từ một hàm chi phí "thông minh", cũng phải mở rộng rất nhiều, cho thấy rằng việc chỉ dựa vào heuristic (Greedy/Hill Climbing) hoặc có thông tin cảm biến (Partial Observable) là chiến lược tối ưu hơn về mặt không gian.

- Về hiệu quả thời gian (Thời gian thực thi)

  Về mặt thời gian, kết quả cũng phản ánh chính xác hiệu quả về không gian. **Partial Observable** là nhanh nhất, chứng tỏ rằng càng có nhiều thông tin về môi trường thì việc tìm kiếm càng nhanh. **Greedy Best-First và Hill Climbing** theo sát phía sau, cho thấy các thuật toán "tham lam" có chi phí tính toán ở mỗi bước rất thấp, giúp chúng đạt được tốc độ ấn tượng. **Backtracking** là thuật toán chậm nhất do phải xử lý số lượng node rất rất lớn. **Uniform Cost**  tuy nhanh hơn **Backtracking** nhưng vẫn chậm hơn đáng kể so với các thuật toán dựa trên heuristic, vì nó phải duy trì một hàng đợi ưu tiên và tính toán chi phí phức tạp hơn ở mỗi bước.

- Kết luận chung: Biểu đồ tổng hợp này là một minh chứng xuất sắc cho thấy sức mạnh của thông tin và heuristic. Các thuật toán được trang bị "kiến thức" về bài toán, dù là thông qua cảm biến hay hàm đánh giá heuristic, đều vượt trội hoàn toàn so với các phương pháp duyệt có hệ thống nhưng "mù quáng" như Backtracking, cả về không gian lẫn thời gian.

---

## THỐNG KÊ SO SÁNH

Bảng thống kê tự động cập nhật sau mỗi lần chạy thuật toán:

| Chỉ số | Ý nghĩa |
|--------|----------|
| **Expanded** | Số trạng thái sinh ra |
| **Visited** | Số trạng thái đã duyệt |
| **Frontier** | Số trạng thái còn trong hàng đợi |
| **Time (ms)** | Thời gian thực thi |
| **Status** | Kết quả (Done / Not Found) |

Người dùng có thể xem lại lịch sử chạy **8 thuật toán gần nhất** ở khung bên phải.

---

## HƯỚNG DẪN SỬ DỤNG

1. **Khởi chạy chương trình**
   ```bash
   python main.py
   ```
2. **Chọn nhóm thuật toán** ở cột bên trái (ví dụ: *Uninformed Search*).  
3. **Chọn thuật toán cụ thể** (BFS, DFS, v.v.) để chạy.  
4. **Bấm “Run”** để thực thi hoặc **“Visual”** để xem từng bước tìm kiếm.  
5. **Random** sinh bàn cờ mới, **Reset** để xóa trạng thái hiện tại.  
6. **Resize** để thay đổi kích thước bàn cờ (3×3 đến 8×8).  

> Ghi chú: Visualization chỉ khả dụng với bàn cờ **≤ 6×6** (để đảm bảo tốc độ hiển thị).

---

## CẤU TRÚC DỰ ÁN

```
8-rooks-ai/
├── src/
│   ├── main.py                     # File chạy chính
│   ├── algorithms/                 # Chứa các thuật toán tìm kiếm
│   ├── core/                       # Xử lý logic chính của ứng dụng
│   │   └── app.py
│   └── ui/                         # Giao diện người dùng (Pygame)
│       ├── __init__.py
│       ├── board.py                # Xử lý bàn cờ và hiển thị quân xe
│       ├── buttons.py              # Tạo và quản lý các nhóm nút thuật toán
│       ├── layout.py               # Bố cục giao diện
│       ├── properties.py           # Cấu hình màu sắc, kích thước
│       └── stats_history.py        # Thống kê và lịch sử chạy thuật toán
│
└── assets/
    ├── fonts/                      # Font chữ (ví dụ: JosefinSans)
    └── pics/                       # Hình ảnh, biểu tượng minh họa
```

---

## MÔI TRƯỜNG

### Yêu cầu
- Python 3.8 trở lên  
- Thư viện:
  ```bash
  pip install pygame matplotlib pillow
  ```

---


## KẾT LUẬN

Dự án **8 Rooks AI** cung cấp một công cụ học tập trực quan giúp người học:
- Hiểu bản chất hoạt động của từng loại thuật toán tìm kiếm.
- So sánh được hiệu suất giữa các nhóm thuật toán.
- Ứng dụng vào các bài toán mở rộng như **N-Queens**, **Robot Pathfinding**, hay **Game AI**.

> Đây là một nền tảng học tập – mô phỏng AI sinh động, dễ hiểu, và có thể mở rộng thêm nhiều thuật toán khác trong tương lai.

---

## ĐÓNG GÓP

Dự án được phát triển bởi:
- **Lương Quang Lâm** – 23110121   

Dưới sự hướng dẫn của:  
**TS. Phan Thị Huyền Trang**

---

**© 2025 - 8 Rooks AI Project**

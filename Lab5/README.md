# Các bước giải: 

Dùng lỗi format string để leak địa chỉ của canary (%19), và return address của hàm vuln(%21)

Tính toán địa chỉ hàm win từ return address của hàm vuln

Dùng lỗi integer overflow để thay đổi tham số len trong hàm read() gây lõi buffer overflow

Bypass canary và đè địa chỉ hàm win lên return address, trong đó setup payload chuỗi "Nghi Hoang Khoa dep trai" để thỏa điều kiện hàm win, vì stack của hàm win và stack của hàm main nằm gần tương tự vị trí nhau.

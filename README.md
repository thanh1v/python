# TikTok Scrapping project - 1 dự án nhỏ để thu thập dữ liệu và tải video TikTok

## Giới thiệu
`TikTokScrapper` là 1 script Python dùng để lấy 1 vài thông tin cơ bản từ 1 video TikTok như là tác giả, id, lượt xem, lượt thích,.v.v...
Sử dụng các thư viện đơn giản như `requests`, `BeautifulSoup`, `re`, đây là 1 script rất dễ hiểu và sử dụng.

## Yêu cầu
- python phiên bản 3. trở lên.
- Cài đặt các thư viện python như `requests` và `beautifulsoup4` với lệnh:
  
```bash
pip install requests
pip install beautifulsoup4
```

## Chi tiết script
Script có 1 lớp `TikTokScrapper` với các function sau:
- `__init__(self,url)`: Dùng để khởi tạo các giá trị ban đầu và đưa vào URL của 1 video TikTok.
- `check_url(self)`: Dùng để kiểm tra URL hợp lệ của TikTok.
- `get_data(self)`: Thu thập các thông tin cơ bản của 1 video, cụ thể là ID, tác giả, lượt xem, lượt thích, bình luận, số lần lưu, mô tả và hashtag.
- `Downloading(self)`: Tải video TikTok từ URL về theo chunk.
- `Saving(self)`: Lưu dữ liệu thu thập được vào file.json và video vào file.mp4.

## Cách dùng
1. Chuẩn bị 1 URL TikTok hợp lệ để sử dụng.
2. Điền URL bạn đã chuẩn bị vào biến url ở phần `if __name__ == '__main__' :` với dạng string.

Ví dụ:
```python
if __name__ == '__main__' :
    url = 'https://www.tiktok.com/@duyyy.real.channel/video/7504660594465770770'
    scrap = TikTokScrapper(url)
    scrap.check_url()
    scrap.get_data()
    scrap.Downloading()
    scrap.Saving()
```

3. Kiểm tra kết quả:
   File JSON `TikTok_<id>.json` chứa thông tin cơ bản của video.
   File `TikTok_<video_id>.mp4` là video bạn đã chọn.

## Lỗi có thể xảy ra
- Lỗi `Phòng này k chơi CÁI ẤY, chỉ Tiktok thôi` tức là URL được nhập vào không hợp lệ, hãy đảm bảo nó bắt đầu bằng `https://www.tiktok.com` hoặc `https://vt.tiktok.com`, `https://vm.tiktok.com`.
- Lỗi `Lỗi khi lấy thông tin từ JSON` kiểm tra lại và chắc chắn code không bị sửa đổi, nếu không có thể là script đã quá cũ so với TikTok.
- Lôi `Lỗi khi tải video` đảm bảo đường truyền mạng hoặc cập nhật cookie/user-agent.
- Lỗi khi lưu dữ liệu hoặc video: đảm bảo script có quyền ghi thư mục đầu ra.

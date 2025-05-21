import requests
from bs4 import BeautifulSoup
import json
import re
from datetime import datetime

class TikTokScrapper:
    def __init__(self,url):
        self.url = url
        self.id = None
        self.dwn_video = None
        self.data = {
            "id": None,
            "author_name":  None,
            "views": None,
            "likes": None,
            "comments": None,
            "saves": None,
            "dates": None,
            "description": None,
            "hashtag": []
        }

    # Đầu tiên chắc chắn phải kiểm tra url để chắc chắn bạn k gửi cornhub lấy video ('')>
    def check_url(self):
        # Chỉ chấp nhận các link đầy đủ và rút gọn của TikTok
        if not self.url.startswith(("https://vt.tiktok.com","https://vm.tiktok.com","https://www.tiktok.com")):
            raise ValueError('Phòng này k chơi CÁI ẤY, chỉ Tiktok thôi')
        

    # Sau khi xác nhạn đúng link TikTok thì mới lấy các thông tin như id và name .....
    def get_data(self):
        
        # Ở đây e dùng cookie để login vào tiktok, pass qua mọi capcha =))/
        headers = {
            "accept": "*/*",
            "accept-language": "vi,en;q=0.9,en-GB;q=0.8,en-US;q=0.7",
            "cookie": "uid_tt=0717909e84cc36b2d71d9bec90212042e25c88aa1f7c440ac38316eba0e0c0ec; sid_tt=f5684549b99ba21776650a599210f624; sessionid=f5684549b99ba21776650a599210f624; sessionid_ss=f5684549b99ba21776650a599210f624",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/136.0.0.0 Safari/537.36 Edg/136.0.0.0"
        }
        
        response = requests.get(self.url, headers=headers)
        soup = BeautifulSoup(response.text,'html.parser')

        # Chúng ta sẽ "đánh cắp" các dữ liệu trên TikTok được lưu ở dạng JSON trong id: "__UNIVERSAL_DATA_FOR_REHYDRATION__"
        script_tag = soup.find("script", id="__UNIVERSAL_DATA_FOR_REHYDRATION__")
        if script_tag:
            try:
                raw_json = script_tag.string
                data = json.loads(raw_json)
                itemm_struct = data['__DEFAULT_SCOPE__']['webapp.video-detail']['itemInfo']['itemStruct']
                # Ta sẽ phải dẫn vị trí đến chính xác của thông tin cần tìm

                stats = itemm_struct.get('stats',{})                    # còn cái này tiếp tục dẫn vào để lấy like,comment,view và saved 
                self.data["likes"] = stats.get('diggCount', '')
                self.data["comments"] = stats.get('commentCount', '')
                self.data["views"] = stats.get('playCount', '')
                self.data["saves"] = stats.get('shareCount', '')
                
                # Đoạn lấy desc và hashtag này e đi copy nhưng cóp về thì hiểu đc rồi :)
                self.data["description"] = re.sub(r'#\w+', '', itemm_struct.get('desc', '')).strip()        #Cái này lấy cả desc và hashtag về xong rồi sẽ xóa đi những thứ sau dấu # và cả nó

                text_tags = itemm_struct.get('textExtra', [])
                self.data["hashtag"] = ['#'+tag.get('hashtagName', '') for tag in text_tags if tag.get('hashtagName')] # Còn đây sẽ trực tiếp lấy các hashtag luôn


                # Đoạn này là để lấy link dài phục vụ cho việc download video kiểu để đồng nhất ấy (format: https://www.tiktok.com/@<author>/video/<id>)
                link = data['__DEFAULT_SCOPE__']['seo.abtest']
                riel_url = link.get('canonical', '')
                self.url = riel_url.replace('\u002F','/')

                # Lấy id và author    
                self.id= re.search(r'/video/(\d+)', self.url).group(1)
                self.data['id'] = self.id
                author= re.search(r'tiktok\.com/@([^/]+)/video', self.url).group(1)
                self.data['author_name'] = author


                # Làm xong thấy thiếu date nên thêm vô
                time = int(itemm_struct.get('createTime'))                          #time này là số giây tính từ 1/1/1970
                self.data['dates'] = datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')

            except Exception as e:
                print(f"Lỗi khi lấy thông tin từ JSON: {e}")
    
        
    # Bước cuối là tải video nè :((
    def Downloading(self):

        # Hết cách, bất lực nên phải gọi 1 cái session để giả dạng browser
        session = requests.Session()
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Referer": "https://www.tiktok.com/",
            "Accept-Language": "en-US,en;q=0.9"
        }
        session.headers.update(headers)

        try:
            response = session.get(self.url)
            response.raise_for_status()
        
            # Đoạn này tính làm cả html lẫn json nhưng cái đầu đc r thì bỏ cái 2 cho gọn :/
            html_content = response.text
        
            # Cách 1 tìm ở downloadAddr
            pattern = r'"downloadAddr":"([^"]+)"'
            video_match = re.search(pattern, html_content)
            print("Đang tìm downloadAddr.....")
        
            if not video_match:
                # Cách 2: tìm ở play Addr
                pattern = r'"playAddr":"([^"]+)"'
                video_match = re.search(pattern, html_content)
                print('Đang tìm playAddr.....')
        
            # url sau khi lấy ở đây sẽ không dùng trực tiếp được mà phải thay đổi 1 số chỗ cho giống 1 cái link thực sự
            video_url = video_match.group(1).replace('\\u0026', '&').replace('\\u002F', '/').replace('\\/', '/')


            # Đoạn này để tải video nè
            self.dwn_video = session.get(video_url, stream=True)        # Cái này để tải từng phần nhỏ về để lưu theo chunk và có thể đọc lại
            self.dwn_video.raise_for_status()                           # Còn đây để tránh lỗi ví dụ như 404,..
            print(type(self.dwn_video))
            
        except requests.RequestException as e:
            print(f"Lỗi khi tải video: {e}")
            return None
        

    def Saving(self):
        # Cái này thì dễ hiểu rồi, nó là lưu thông tin vào file.json
        file_name = f"TikTok_{self.id}.json"
        try:
            with open(file_name, 'w', encoding='utf-8') as f:
                json.dump(self.data, f, indent=4, ensure_ascii=False)
                # Việc encoding và ascii=False để ta có thể lưu tiếng Việt và file.json

            print(f'Lưu thành công vào {file_name}')


        except Exception as e:
            print('Lưu dữ liệu thất bại')

        # Đây là lưu video vào file.mp4
        video_name = f"TikTok_{self.id}.mp4"
        try:
            with open(video_name, 'wb') as f:
                for chunk in self.dwn_video.iter_content(chunk_size=8192):     # Bước này là đọc lại dữ liệu theo chunk và tối đa mỗi chunk dc phép là 8KB
                    if chunk:
                        f.write(chunk)
                        print(f'Lưu thành công vào {video_name}')

        except requests.RequestException as e:
            print('Lỗi khi lưu video:', e)



if __name__ == '__main__' :
    url = " "
    # Ví dụ: url = "https://www.tiktok.com/@duyyy.real.channel/video/7504660594465770770"
    scrap = TikTokScrapper(url)
    scrap.check_url()
    scrap.get_data()
    scrap.Downloading()
    scrap.Saving()


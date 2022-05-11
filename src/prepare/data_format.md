### data format

- Muc format

```
Biển rác sau lễ hội ở <ENAMEX TYPE="LOCATION-GPE">Anh</ENAMEX>
```

- conll2003 

```
# định dạng ConLL 2003 gồm:
# cột 0     cột 1       cột 2           cột 3       cột 4->>>
# word      POS(k có)   Phrase(k có)    NER_main    Ner_extension
```

```
Biển	_	_	O	O
rác	_	_	O	O
sau	_	_	O	O
lễ	_	_	O	O
hội	_	_	O	O
ở	_	_	O	O
Anh	_	_	B-LOCATION-GPE	O
```

### entity 

- 

```
Person   
PersonType   
Location   
    - LOCATION-GPE (các thành phố, quốc gia, vùng lãnh thổ, các bang)   
    - LOCATION-STRUC (Những công trình do người xây dựng)   
    - LOCATION-GEO (Các thực thể tự nhiên :Sông, hồ, ao, suối, đại dương, ...)   
Organization   
    - ORGANIZATION-MED: (Các công ty, bệnh viện liên quan đến y tế, dược phẩm, ...)    
    - ORGANIZATION-STOCK (Các chợ, sàn trao đổi, giao dịch hàng hoá, chứng khoán)    
    - ORGANIZATION-SPORTS (Các tổ chức liên quan đến thể thao)    
Event  
    - EVENT-CUL (Các sự kiện văn hoá, các ngày lễ tết, ...)
    - EVENT-NATURAL (Các sự kiện tự nhiên xảy ra)
    - EVENT-SPORT (Các sự kiện thể thao)
    - EVENT-GAMESHOW (Các chương trình ti vi, gameshow, ...)  
Product    
    - PRODUCT-COM (Các sản phẩm liên quan đến máy móc tính toán)
    - PRODUCT-LEGAL (Legal products - Các sản phẩm liên quan đến pháp luật: Các hiệp định, hiệp ước, luật, ....)
    - PRODUCT-AWARD: Prizes at competitions
Skill    
Address    
Phone number    
Email    
URL     
IP    
DateTime 
    - DATETIME-DATE (Một ngày cụ thể)
    - DATETIME-TIME (Thời gian trong một ngày)
    - DATETIME-DATERANGE (KHoảng ngày tháng)
    - DATETIME-TIMERANGE (Khoảng thời gian)
    - DATETIME-DURATION (Khoảng, thời lượng)
    - DATETIME-SET (Tập hợp thời gian riêng rẽ)   
Quantity  
    - QUANTITY-NUM (Số)
    - QUANTITY-PER (Phần trăm)
    - QUANTITY-ORD (Số thứ tự)
    - QUANTITY-AGE (Tuổi)
    - QUANTITY-CUR (Tiền tệ)
    - QUANTITY-DIM (Số chiều)
    - QUANTITY-TEM (Nhiệt độ)
```

### Sửa lỗi 

- fix mis 

```
<ENAMEX TYPE="*">sĩ</ENAMEX> <ENAMEX TYPE="*"><ENAMEX TYPE="PERSONTYPE">Tiến</ENAMEX> Stephen Goldbart</ENAMEX>
```

```
<ENAMEX TYPE="PERSON"><ENAMEX TYPE="PERSONTYPE">Tiến sĩ</ENAMEX> Stephen Goldbart</ENAMEX>
```

- đánh lại nhãn
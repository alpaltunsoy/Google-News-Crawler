# Veri Çekme Sanatı: Google News'i Ayağınıza Getirin


Günümüz dünyasında haberler, bilgiye erişmemiz için en önemli kaynaklardan birisi konumundadır. Bu bilgiler gerek hayatımız için gerek de iş hayatımız için kilit taşıdır. Hava durumu  ile giyimimiz, Faiz kararlarına göre portföyümüz şekil alıyor. Peki bu haberlerin hepsini okuyup analiz etmek isteseydik ne olurdu?

Büyük ihtimalle bu kadar veriyi manuel bir şekilde inceleyemeyecektik ve analiz edemeyecektik. İşte burada devreye **Web Kazıma** girecek. Web Kazıma (Web Scraping), otomatik veri çekme işlemidir ve sitelerden veri kazımanın efektif yollarından birisidir.

İşte bugün benimle bu yazımda, Google News'ten veri kazımı yapmanın detaylarına bakacağız. O zaman başlıyoruz.

## Google News Crawler Nedir?
Hayatımızda tüm kayda değer haberlere göz gezdirmek isteseydik, bir analiz yapmak isteseydik, ya da istatikçilerin tek tek bunları kayda almak isteseydi ne olurdu? Büyük ihtimalle bu kadar haberle uğraşmak için vaktimiz olmayacaktı. İşte bu sorunu python ile çok basit bir şekilde çözebiliyoruz.

Google News Crawler, temelde açık kaynaklı kütüphaneleri kullanan bir Python scriptidir. Açık kaynaklı kütüphanelerden bahsetmişken bunların ne olduğuna da değinelim. Açık kaynaklı kütüphaneler, telif hakkı sahibi tarafından kaynak kodları değiştirilebilen incelenebilen kod blokları diyebiliriz. Bu sayede kapalı kaynak kütüphanelere kıyasla daha güvenli bir program çıkartmamıza olanak sağlıyor. Evet açık kaynaklı kütüphaneleri kullanıyoruz evet, ama bir kullanıcı olarak ne işime yaradı diye sorabilirsiniz? Bir kullanıcı olarak bu yazılımı aklınızda soru işareti kalmadan kullanmanıza olanak sağlıyor.

Google News Crawler, [Ana Sayfa](https://news.google.com/home?hl=tr&gl=TR&ceid=TR:tr)'dan başlayarak tüm kategorileri tespit ediyor ve bu kategorileri hafızaya alıyor. Hafızaya aldıktan sonra her bir kategorinin olduğu sayfaya gidiyor ve tüm haberleri size bir csv veya json dosyası olarak sunuyor. Haberlerin hepsini size tek bir csv veya json dosyası haline getirmesinin yanı sıra bu haberleri size kategori olarak da ayrı ayrı veriyor. Bunun yanı sıra istemediğiniz kategorileri kaynak kodu içerisine yazarak, o kategoriden haber kazımasının önüne geçebiliyorsunuz. Haberlerinin başlığının yanı sıra, URL, Kategori, Kaçıncı sırada olduğu gibi verileri de kaydediyoruz. Tabii ki, bunların yanı sıra bu programı sürekli çalıştırmanıza gerek yok, bu program sizin yerinize her saat başı bu işlemi otomatik yapıyor ve tarih-saat şeklinde klasörlüyor. Evet belki tüm haberleri okuyamayız ama tüm haberleri bilgisayarımızda bu şekilde tutabiliriz.

### Neden CSV ve JSON dosyası

> JSON, JavaScript nesne gösterini anlamına gelir ve hafif metin tabanlı veri formatıdır. İnsanlar tarafından anlaşılabilir olması yanı sıra, bilgisayarlar arası veri alışverişinde yaygın olarak kullanılmaktadır.

> CSV, virgülle ayrılmış değerler anlamına gelir ve basit, düz metin tabanlı bir dosya formatıdır. Genellikle tablo şeklinde veri saklamak için kullanılır.

Anlayacağınız üzere ikisi de veri ile alakalı dosya tipleridir ve bu sayede büyük veri kümelerini saklama, verileri aktarma ve raporlama gibi alanlarda kullanılmaktadır. Google News Crawler'da da verilerimizi saklamak için ve ileride analiz etmek isterseniz diye bu dosya formatlarını tercih ettik.


## Python ile Web Kazıma
Bu bölümümüzde önce temel Web Kazıma özelliklerinden bahsedeceğiz ve sizlerin de içiniz rahat bir şekilde Google News Crawler'ı kullanabilmesi için biraz programın koduna da değineceğiz.

### Temel Web Kazıma Teknikleri
Öncelikle web kazıma yapabilmemiz için [BeautifulSoup](https://pypi.org/project/beautifulsoup4/) ve [requests](https://pypi.org/project/requests/) kütüphanelerini Python'a kurmanız gerekmektedir. Bu yazımızın konusu olmadığı için **import** işlemlerini bu yazımda anlatmayacağım.

`import requests`

`from bs4 import BeautifulSoup`

Bu iki kütüphaneyi kodumuza eklediğimize göre bazı kütüphane içerisindeki bazı fonksiyonlardan bahsedelim.


#### Get()
`X = requests.get(url, params)`
Tarayıcımızdan bir internet sitesine gitmek istediğimiz de aslında bir get işlemi yaparız ve bize HTML Dökümünü geri döndürür. o zaman geri bir şey döndürüyorsa bunu sonra kullanmak üzere bir değişkene tanımlayabiliriz. Yukarıdaki X bu değişkeni temsil etmektedir.

**url:** Sayfanın linkini temsil etmektedir.<br>**params:** Get fonksiyonu için tuple şeklinde veri alır bazı sitelerin özel parametreleri için bu kısmı kullanırız.

#### `status_code`
`X.status_code` HTTP isteği yapıldığında karşıdan sunucudan dönen bir durum kodunu ifade eder. En çok aşina olduğunuz *404* kodu dönerse eğer internet sitesi bulunamamıştır. *200* kodu ise başarılı istek anlamına gelir.

#### BeautifulSoup 
`Y = BeautifulSoup(HTML_FILE, parser_type)` BeautifulSoup ile HTML dosyalarını ayrıştırabiliriz ve bu ayrıştırdığımız verileri manipüle edebiliriz. *HTML_FILE* yazan kısım HTML dosyasınını talep eder biz buraya request ile aldığımız X değişkenini koyabiliriz. *parser_type* kısmına ise çözümleme yöntemlerinden birisini yerleştirmemiz gerekmektedir. Ben Google News Crawler'ı yazarken **lxml** tipini kullandım. Her bir parser tipinin dezavantajları ve avantajları bulunmaktadır. 

#### `find_all()`
`etiketler = Y.find_all("a" class_="XXXXX" )` Bu metodun birden fazla kullanım yöntemi olduğundan dolayı burada sadece Google News Crawler'da kullandığım şekilde kullanımından bahsedeceğim. Bu bahsedişten sonra genel hatlarıyla kullanımını anlamış olacaksınız. Daha fazla bilgi için [Dökümanlarını](https://beautiful-soup-4.readthedocs.io/en/latest/#making-the-soup) inceleyebilirsiniz.

find_all methodu ile `XXXXX` sınıfına dahil tüm `<a>` etiketlerini bulur. Buradaki `class_` ve `<a>` kısımları html içerisinde aramak istediğiniz özelliğe etikete göre değiştirebilirsiniz.

#### `get()` ve `.contents[].strip()` methodları
`etiketler.get("href")` get() fonksiyonu ile bulmuş olduğum özelliklerdeki HTML parçalarının, istediğimiz etiket değerlerini direkt çekebiliriz. Buradaki **href** sadece bir örnek olup istediğmiiz etiketi yazabiliriz. 
*HTML kodunda eğer `<a href = "xxx">` gibi bi özellik varsa bize get fonksiyonu xxx' döndürecektir.

`etiketler.contents[].strip()` Etiketlerin *children* sınıflarına ulaşmak için kullanılır ve strip methodu ile tüm boşluklar kaldırılır.


Google News Crawler'da kullandığım bazı Web Kazıma Fonksiyonları hakkında bilgi vermiş olduğumu düşünmekteyim. Daha fazla bilgi için kütüphanelerin dökümanlarını inceleyebilirsiniz.

## Kodun Genel Çalışma Mantığı ve Tanımlanan methodlar

Bu kısımda Google News Crawler'ı yazarken oluşturmuş olduğum bazı methodlardan ve çalışırken ne yaptıklarından bahsedeceğim. Bu kısımda methodların detaylı açıklamasını değil sadece neyin ne zaman ve nasıl çalıştığına dair basit açıklamalar yer alacak.

### `main()`
Script'i çalıştırdığımızda ilk olarak `main()` çalışır. Main içerisinde sadece saat başı kodumuzu tetikletecek kodlar ve scripin açık olduğuna dair uyarı bilgisi yer almaktadır. Her saat başı bu kod bloğu `start()` methodunu tetikler.

### `start()`
`start()` methodu diğer methodları sırasıyla çağırmak için kullandığımız methodtur. Bu method içerisinde akışa uygun bir şekilde diğer kodlar çağırılmaktadır. Bu methodlar arasında haberlerimizin kaydedildiği dosyaların oluşturulduğu method, Google News sitesinde yer alan kategorileri bulan method ve kategorileri bulduktan sonra haberleri bulan method yer almaktadır. Bu methodların adı sırasıyla 
`create_folder()`, `finding_categories()` ve `finding_news()` methodlarıdır.
Methodların yanı sıra burada tarih saat bilgisini barındıran, kategorileri depolayan değişkenlerin tanımlaması da burada yapılmaktadır.
### `create_folder()`
Bu method sayesinde çalışma dizininde *docs* adlı bir dosyanın olup olmadığının kontrolü gerçekleştirilir ve eğer yoksa çalışma dizinine ekler. Bu dosyanın kontrolünü yaptıktan sonra ise mevcut tarih saate göre yeni klasörlerin *docs* içerisine eklenmesi gerçekleştirilir. Tüm işlemler bittikten sonra Google News'ten kategorileri bulmak için yazmış olduğum `finding_categories()` methodu çalışır.

### `finding_categories()` 
Sıra bu methoda geldiğinde Google News'e request atılır ve HTML dosyasını bir değişkene kaydederiz. Eğer url bozuksa uygulama *except* bloğuna girer ve `exit()` modülü ile direkt scripti kapatır. 

Eğer bağlantı başarılı olursa yukarıda bahsedilen `status_code` kontrol edilir. Eğer sunucudan alınan yanıt 200 değilse uyarı mesajı gelir ve `finding_news()` methoduna geçer burada'da kategori bulunamadığından dolayı request başarısız olur ve program `exit()` methoduna gider. 

Evet artık sunucunun 200 kodunu döndürdüğünü varsayabiliriz. Artık methodumuz BeautifulSoup objesi oluşturur ve elimizdeki HTML kodunu ayrıştırmaya başlar. Bu kod bloğunun içerisinde bulunan *categories_exclude* değişkenin içerisinde bulunan içerikler istemediğimiz kategoriler veya kısımlardır. Burası varsayılan olarak **Sizin için**, **Ana Sayfa** vs gibi içerikleri bulundurur. Bunun sebebi HTML'i ayrıştırdığımızda kategori kısmında bu tarz istemediğimiz içerikler bulundurmasıdır. Başarılı bir şekilde kategorileri bulduktan sonra artık `finding_news()` methoduna sıra gelir.


### `finding_news()` 

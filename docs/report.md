# Veri Çekme Sanatı: Google News'i Ayağınıza Getirin


Günümüz dünyasında haberler, bilgiye erişmemiz için en önemli kaynaklardan birisi konumundadır. Bu bilgiler gerek hayatımız için gerek de iş hayatımız için kilit taşıdır. Hava durumu  ile giyimimiz, Faiz kararlarına göre portföyümüz şekil alıyor. Peki bu haberlerin hepsini okuyup analiz etmek isteseydik ne olurdu?

Büyük ihtimalle bu kadar veriyi manuel bir şekilde inceleyemeyecektik ve analiz edemeyecektik. İşte burada devreye **Web Kazıma** girecek. Web Kazıma (Web Scraping), otomatik veri çekme işlemidir ve sitelerden veri kazımanın efektif yollarından birisidir.

İşte bugün benimle bu yazımda, Google News'ten veri kazımı yapmanın detaylarına bakacağız. O zaman başlıyoruz.

## Google News Crawler Nedir?
Hayatımızda tüm kayda değer haberlere göz gezdirmek isteseydik, bir analiz yapmak isteseydik, ya da istatikçiler tek tek bunları kayda almak isteseydi ne olurdu? Büyük ihtimalle bu kadar haberle uğraşmak için vaktileri olmayacaktı. İşte bu sorunu python ile çok basit bir şekilde çözebiliyoruz.

Google News Crawler, temelde açık kaynaklı kütüphaneleri kullanan bir Python scriptidir. Açık kaynaklı kütüphanelerden bahsetmişken bunların ne olduğuna da değinelim. Açık kaynaklı kütüphaneler, telif hakkı sahibi tarafından, kaynak kodları değiştirilmeye, incelenmeye izin verilen kod bloklarıdır diyebiliriz. Bu sayede kapalı kaynak kütüphanelere kıyasla daha güvenli bir program çıkartmamıza olanak sağlıyor. Evet açık kaynaklı kütüphaneleri kullanıyoruz, ama bir kullanıcı olarak ne işime yaradı diye sorabilirsiniz? Bir kullanıcı olarak bu yazılımı aklınızda soru işareti kalmadan kullanmanıza olanak sağlıyor.

Google News Crawler, [Ana Sayfa](https://news.google.com/home?hl=tr&gl=TR&ceid=TR:tr)'dan başlayarak tüm kategorileri tespit ediyor ve bu kategorileri hafızaya alıyor. Hafızaya aldıktan sonra her bir kategorinin olduğu sayfaya gidiyor ve tüm haberleri size bir csv veya json dosyası olarak sunuyor. Haberlerin hepsini size tek bir csv veya json dosyası haline getirmesinin yanı sıra, bu haberleri size kategori olarak da ayrı ayrı veriyor. Bunun yanı sıra istemediğiniz kategorileri kaynak kodu içerisine yazarak, o kategoriden haber kazımasının önüne geçebiliyorsunuz. Haberlerinin başlığının yanı sıra, URL, Kategori, Kaçıncı sırada olduğu gibi verileri de kaydediyoruz. Tabii ki, bunların yanı sıra bu programı sürekli çalıştırmanıza gerek yok, bu program sizin yerinize her saat başı bu işlemi otomatik yapıyor ve tarih-saat şeklinde klasörlüyor. Evet belki tüm haberleri okuyamayız ama tüm haberleri bilgisayarımızda bu şekilde tutabiliriz.

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
`X.status_code` HTTP isteği yapıldığında karşıdan sunucudan dönen bir durum kodunu ifade eder. En çok aşina olduğunuz *404* kodu dönerse eğer, internet sitesi bulunamamıştır. *200* kodu ise başarılı istek anlamına gelir.

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
Bu methodta bir **for** döngüsü ile tüm kategorilerdeki haberler csv dosyasına kaydedilir ve oluşturulan csv dosyası json formatına dönüştürülür. Her bir kategorinin url'si belli bir formattadır ve bulununan kategoriler mevcutta olan url ile birleştirilir. Birleştirme yapıldıktan sonra tekrar request atılır ve bunun sonucunda yukarıda bahsedilen sunucudan gelen yanıt ve request'in başarısı kontrol edilir. Bu kontroller sonucunda bir sorun yoksa kategoriye göre haber bulma işlemi başlar.

Haberleri bulurken **Başlık**, **Kaçıncı sırada olduğu**, **Habere ait bağlantı**, **Kategorisi**, **Yayımcısı** kayıt altına alınır. Her bir kategorideki haberleri bulduktan sonra bunlar bir csv dosyası haline getirilir. Csv dosyasını oluşturmak için `csv_creator_category()` methodu kullanılır adından da belli olacağı şekilde bu sadece kategorileri ayrı ayrı csv dosyası yapmaya yarar. Csv yapıldıktan sonra
`csv_to_json()` metodu ile oluşturulmuş csv dosyası json'a dönüştürülür. For döngüsü bittikten sonra ise tüm haberleri depoladığımız değişkenimiz  `csv_creator()` metodu tüm haberleri kategorisiz bir şekilde hepsini tek bir csv'ye yazar ve ardından `csv_to_json()` methodu ile tekrar jsona dönüştürülür.

#### `csv_creator_category()`  ve `csv_creator()`  
Bu methodlar adından anlaşılacağı şekilde bulmuş olduğumuz haberleri csv dosyasına yazmak için verileri hazırlar ve csv dosyasına yazar. İki method arasındaki tek fark birisinin her kategorideki haberleri ayrı ayrı csv dosyasına kaydetmesidir.Diğer method ise tüm haberleri kategorilerine ayırmadan tek bir csv dosyasına yazıyor.

#### `csv_to_json()` 
Oluşturduğumuz csv dosyalarını bulunduğu dizinden çekerek json dosyasına dönüştürür ve tekrar dizine kaydeder. Bu işlemi açık kaynak kodlu **panda** kütüphanesinin içinde bulunan `to_json()` methodu ile yapmaktadır. Yukarıda bu kütüphaneden bahsetmeme sebebim ana temamızın Web Kazıma olmasından dolayıdır. 
 

Tüm methodlarımızı açıkladığımıza göre artık temel olarak Google News Crawler'ın nasıl çalıştığına dair ön fikrimiz var. Bundan sonraki kısımda karşılaştığım sorunlar, zorluklar ve çözüm yolları hakkında konuşacağız.

## Karşılaşılan Zorluklar ve Sorunlar

Bu kısımda yazacağım sorun ve problemler tamamen kendime aittir. Bu zorluklar sizin karşınıza çıkmayabilir ya da bu sorunları biliyor olabilirsiniz.

### Farklı etikete sahip haberler
Google News Sitesinde haberler bazen dörtlü bazen de tekli bulunmakta. Bundan kaynaklı ilk yaptığım versiyonda bunu farkedemedim ve kendimin gördüğü sayı ile kaç tane haber, link, başlık bulduğuma dair sayaç koymuştum bu sayaçlar birbirinden farklı olunca bu sorunu çözmeye koyuldum. Bahsettiğim durum aşağıdadır. ![Örnek Yerleşke](dizilim.jpg)


Bu sorununun çözümü oldukça basit çünkü Google News bu haberlerin dizilimini değiştirdiği zaman HTML etiketlerini de değiştiriyor. Fakat benim tek kontrol mekanizmam olduğu için sadece dörtlü haberleri almıştım. Bu sorunu çözebilmek için tek kontrol mekanizması ile iki tane HTML sınıfını kontrol etmem gerekiyordu. Ya o ya bu tarzı ve bunu `lambda` ile çözdüm. Kod bloğu aşağıdadır.

`newsSoup.find_all("a", class_=lambda x: x and (x.startswith("gPFEn") or x.startswith("JtKRv")))` 

Lambda'ları anonim bir fonksiyon olarak düşünebiliriz. Bir fonksiyon içerisinde kullanmak için uygundur. Burada birden fazla argümanı kontrol ediyoruz. Sorunuz şu olacaktır neden **x and** kulanılmıştır olabilir. Eğer boş ise *false* döndürmektedir. Bu sorunun Çözümü için [StackOverFlow](https://stackoverflow.com/questions/44872063/beautiful-soup-find-all-encompassing-multiple-class-names)'a başvurdum.

Bu sorun dışında başka bir sorun veya problemle karşılaşmadım.

## Programın Geliştirilmesi için Yapılabilecekler

Program çok kısa bir sürede yapıldığı için bazı geliştirilmesi gereken yerlerinin olduğunu ben de düşünüyorum. Bunlardan bazılarını aşağıya ekliyorum.

* Tüm değişkenlerin ve methodların aynı formatta yazılması. Örnek: WebParsing'in Web_Parsing yapılması gibi
* `csv_creator()` methodunun teke düşürülmesi hem kategori, hem de genel csv oluşturucusuna ayrı ayrı gerek yok.
* Yeni kazımanın ne zaman başlayacağına dair bir sayaç eklenmesi.
* **temp** değişkenlerini kullanmadan var olan değişkenlerle programın sürdürülmesi.

Evet programın geliştirilmesi için bu tarz küçük şeyler yapılabilir. Bu tarz geliştirmeler kodun okunulabilirliğini ve biraz da olsa hızını arttıracaktır.

## Sonuç
Çok kısa bir sürede Google News'i kazıyarak tüm haberleri ayağımıza getirdik ve bunu yaparken bu işleri nasıl yaptığımıza dair kısa kısa açıklamalardan bahsettik. Siz de burada olan kodları güncelleyerek ya da buradaki kodları kullanarak kendinize göre kişiselleştirebilirsiniz.
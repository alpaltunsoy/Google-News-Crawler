# Veri Çekme Sanatı: Google News'i Ayağınıza Getirin

## Python ile Web Kazıma

Günümüz dünyasında haberler, bilgiye erişmemiz için en önemli kaynaklardan birisi konumundadır. Bu bilgiler gerek hayatımız için gerek de iş hayatımız için kilit taşıdır. Hava durumu  ile giyimimiz, Faiz kararlarına göre portföyümüz şekil alıyor. Peki bu haberlerin hepsini okuyup analiz etmek isteseydik ne olurdu?

Büyük ihtimalle bu kadar veriyi manuel bir şekilde inceleyemeyecektik ve analiz edemeyecektik. İşte burada devreye **Web Kazıma** girecek. Web Kazıma (Web Scraping), otomatik veri çekme işlemidir ve sitelerden veri kazımanın efektif yollarından birisidir.

İşte bugün benimle bu yazımda, Google News'ten veri kazımı yapmanın detaylarına bakacağız. O zaman başlıyoruz.

### Google News Crawler Nedir?
Hayatımızda tüm kayda değer haberlere göz gezdirmek isteseydik, bir analiz yapmak isteseydik, ya da istatikçilerin tek tek bunları kayda almak isteseydi ne olurdu? Büyük ihtimalle bu kadar haberle uğraşmak için vaktimiz olmayacaktı. İşte bu sorunu python ile çok basit bir şekilde çözebiliyoruz.

Google News Crawler, temelde açık kaynaklı kütüphaneleri kullanan bir Python scriptidir. Açık kaynaklı kütüphanelerden bahsetmişken bunların ne olduğuna da değinelim. Açık kaynaklı kütüphaneler, telif hakkı sahibi tarafından kaynak kodları değiştirilebilen incelenebilen kod blokları diyebiliriz. Bu sayede kapalı kaynak kütüphanelere kıyasla daha güvenli bir program çıkartmamıza olanak sağlıyor. Evet açık kaynaklı kütüphaneleri kullanıyoruz evet, ama bir kullanıcı olarak ne işime yaradı diye sorabilirsiniz? Bir kullanıcı olarak bu yazılımı aklınızda soru işareti kalmadan kullanmanıza olanak sağlıyor.

Google News Crawler, [Ana Sayfa](https://news.google.com/home?hl=tr&gl=TR&ceid=TR:tr)'dan başlayarak tüm kategorileri tespit ediyor ve bu kategorileri hafızaya alıyor. Hafızaya aldıktan sonra her bir kategorinin olduğu sayfaya gidiyor ve tüm haberleri size bir csv veya json dosyası olarak sunuyor. Haberlerin hepsini size tek bir csv veya json dosyası haline getirmesinin yanı sıra bu haberleri size kategori olarak da ayrı ayrı veriyor. Bunun yanı sıra istemediğiniz kategorileri kaynak kodu içerisine yazarak, o kategoriden haber kazımasının önüne geçebiliyorsunuz. Haberlerinin başlığının yanı sıra, URL, Kategori, Kaçıncı sırada olduğu gibi verileri de kaydediyoruz. Tabii ki, bunların yanı sıra bu programı sürekli çalıştırmanıza gerek yok, bu program sizin yerinize her saat başı bu işlemi otomatik yapıyor ve tarih-saat şeklinde klasörlüyor. Evet belki tüm haberleri okuyamayız ama tüm haberleri bilgisayarımızda bu şekilde tutabiliriz.

#### Neden CSV ve JSON dosyası

JSON, JavaScript nesne gösterini anlamına gelir ve hafif metin tabanlı veri formatıdır. İnsanlar tarafından anlaşılabilir olması yanı sıra, bilgisayarlar arası veri alışverişinde yaygın olarak kullanılmaktadır.

CSV, virgülle ayrılmış değerler anlamına gelir ve basit, düz metin tabanlı bir dosya formatıdır. Genellikle tablo şeklinde veri saklamak için kullanılır.

Anlayacağınız üzere ikisi de veri ile alakalı dosya tipleridir ve bu sayede büyük veri kümelerini saklama, verileri aktarma ve raporlama gibi alanlarda kullanılmaktadır. Google News Crawler'da da verilerimizi saklamak için ve ileride analiz etmek isterseniz diye bu dosya formatlarını tercih ettik.





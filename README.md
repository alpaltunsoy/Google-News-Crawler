# Google News Scraper

Bu proje, Google News'den haber başlıklarını, kaynaklarını, kategorilerini, zamanlarını ve URL'lerini toplayan bir web kazıma (web scraping) aracıdır. Toplanan veriler CSV ve JSON formatlarında saklanır.

## İçindekiler

- [Kurulum](#kurulum)
- [Fonksiyonlar](#fonksiyonlar)
- [Örnek Çıktılar](#örnek-çıktılar)

## Kurulum

Proje için gerekli bağımlılıkları yüklemek için aşağıdaki adımları izleyin:


1. Gerekli Python kütüphanelerini yükleyin:

    ```bash
    pip install requests beautifulsoup4 pandas schedule
    ```


## Fonksiyonlar

- `csv_creator_category(headers, kaynak, category, time, url)`: Belirli bir kategori için haberleri CSV dosyasına yazar.
- `csv_creator(headers, kaynak, category, time, url)`: Tüm haberleri tek bir CSV dosyasına yazar.
- `finding_categories(categories_dictionary)`: Google News ana sayfasındaki kategorileri bulur ve sözlüğe ekler.
- `finding_news(categories_dictionary)`: Belirtilen kategorilerdeki haberleri bulur ve verileri toplar.
- `csv_to_json(category)`: Belirtilen kategorideki CSV dosyasını JSON formatına dönüştürür.
- `create_folder()`: Gerekli klasörleri oluşturur.
- `start()`: Kazıma işlemini başlatır.
- `main()`: Programın ana döngüsünü başlatır ve planlama işlemlerini yönetir.

## Örnek Çıktılar

Kazıma işlemi sonucunda, belirli bir klasörde şu dosyalar oluşturulur:

- `All_news_list_{category}.csv`: Belirli bir kategori için tüm haberler.
- `All_news_list_{category}.json`: Belirli bir kategori için tüm haberler JSON formatında.
- `All_news_list_.csv`: Tüm kategorilerdeki tüm haberler.
- `All_news_list_.json`: Tüm kategorilerdeki tüm haberler JSON formatında.


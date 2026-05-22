import json
from .database import SessionLocal
from .models import Origin

ORIGINS = [
    {
        "country": "Ethiopia", "country_ja": "エチオピア", "region": "Yirgacheffe",
        "latitude": 6.15, "longitude": 38.20, "altitude_min": 1700, "altitude_max": 2200,
        "climate": "Tropical Highland", "slug": "ethiopia",
        "varieties": ["Heirloom"], "process_methods": ["Natural", "Washed"],
        "flavor_notes": ["Blueberry", "Jasmine", "Citrus", "Floral"],
        "acidity": 5, "bitterness": 2, "sweetness": 4, "body": 3,
        "description": "Ethiopia is the birthplace of coffee. The Yirgacheffe region produces some of the world's most prized beans, known for their vibrant floral aromas and fruity complexity. Heirloom varieties grown at high altitude create a uniquely bright and wine-like cup.",
        "description_ja": "エチオピアはコーヒーの発祥地。イルガチェフェは華やかなフローラルと果実味が際立つ世界屈指の産地。",
        "data_source": "SCA / ICO"
    },
    {
        "country": "Colombia", "country_ja": "コロンビア", "region": "Huila / Nariño",
        "latitude": 2.50, "longitude": -75.50, "altitude_min": 1500, "altitude_max": 2000,
        "climate": "Tropical Highland", "slug": "colombia",
        "varieties": ["Castillo", "Caturra", "Colombia"],
        "process_methods": ["Washed"],
        "flavor_notes": ["Caramel", "Red Apple", "Chocolate", "Nutty"],
        "acidity": 4, "bitterness": 2, "sweetness": 4, "body": 3,
        "description": "Colombia's diverse microclimates and mountain ranges produce a consistently well-balanced coffee. The Huila and Nariño regions are particularly celebrated for their bright acidity and rich sweetness, making Colombian coffee a global benchmark.",
        "description_ja": "コロンビアは安定した品質で知られる。フイラ・ナリーニョはキャラメルの甘みと明るい酸味が魅力。",
        "data_source": "FNC Colombia"
    },
    {
        "country": "Brazil", "country_ja": "ブラジル", "region": "Minas Gerais",
        "latitude": -19.50, "longitude": -46.50, "altitude_min": 800, "altitude_max": 1300,
        "climate": "Tropical", "slug": "brazil",
        "varieties": ["Bourbon", "Mundo Novo", "Catuai"],
        "process_methods": ["Natural", "Pulped Natural"],
        "flavor_notes": ["Chocolate", "Nuts", "Caramel", "Low Acidity"],
        "acidity": 2, "bitterness": 3, "sweetness": 4, "body": 5,
        "description": "Brazil is the world's largest coffee producer. Its flat terrain and consistent climate produce smooth, low-acid coffees with deep chocolate and nutty notes. Natural processing amplifies the sweetness, making Brazilian coffee perfect for espresso blends.",
        "description_ja": "世界最大の生産国。ナチュラル精製によるチョコレートとナッツの風味が特徴。エスプレッソブレンドに最適。",
        "data_source": "ABIC / ICO"
    },
    {
        "country": "Guatemala", "country_ja": "グアテマラ", "region": "Antigua / Huehuetenango",
        "latitude": 14.60, "longitude": -90.70, "altitude_min": 1300, "altitude_max": 2000,
        "climate": "Subtropical Highland", "slug": "guatemala",
        "varieties": ["Bourbon", "Caturra", "Typica"],
        "process_methods": ["Washed"],
        "flavor_notes": ["Dark Chocolate", "Spice", "Brown Sugar", "Berry"],
        "acidity": 4, "bitterness": 3, "sweetness": 3, "body": 4,
        "description": "Guatemala's volcanic soil and diverse microclimates produce complex, full-bodied coffees. Antigua is famous for its smoky richness from volcanic ash, while Huehuetenango delivers bright fruit-driven profiles at extreme altitudes.",
        "description_ja": "火山性土壌がもたらす複雑なフレーバー。アンティグアはスモーキーさ、ウエウエテナンゴはフルーティな酸味が特徴。",
        "data_source": "ANACAFE"
    },
    {
        "country": "Costa Rica", "country_ja": "コスタリカ", "region": "Tarrazú",
        "latitude": 9.60, "longitude": -84.00, "altitude_min": 1200, "altitude_max": 1900,
        "climate": "Tropical Highland", "slug": "costa-rica",
        "varieties": ["Caturra", "Catuai"],
        "process_methods": ["Washed", "Honey"],
        "flavor_notes": ["Honey", "Citrus", "Apricot", "Brown Sugar"],
        "acidity": 4, "bitterness": 2, "sweetness": 5, "body": 3,
        "description": "Costa Rica pioneered the honey process, creating coffees with exceptional sweetness and fruit character. The Tarrazú region is the crown jewel, producing clean, bright, and complex cups that showcase the country's commitment to quality.",
        "description_ja": "ハニープロセスの発祥地。タラスは甘みと明るい酸味の調和が絶妙な高品質コーヒーで知られる。",
        "data_source": "ICAFE"
    },
    {
        "country": "Kenya", "country_ja": "ケニア", "region": "Nyeri / Kirinyaga",
        "latitude": -0.50, "longitude": 37.10, "altitude_min": 1400, "altitude_max": 2100,
        "climate": "Tropical Highland", "slug": "kenya",
        "varieties": ["SL28", "SL34", "Ruiru 11"],
        "process_methods": ["Washed (Double Fermentation)"],
        "flavor_notes": ["Blackcurrant", "Tomato", "Grapefruit", "Wine-like"],
        "acidity": 5, "bitterness": 2, "sweetness": 3, "body": 4,
        "description": "Kenyan coffee is celebrated for its bold, wine-like complexity and striking blackcurrant notes. The unique double-fermentation washing process and high-altitude growing conditions create an intensely aromatic and juicy cup unlike any other origin.",
        "description_ja": "ブラックカラントとワインのような複雑さが際立つ。二重発酵ウォッシュドによる強烈な個性が世界で珍重される。",
        "data_source": "Kenya Coffee Board"
    },
    {
        "country": "Yemen", "country_ja": "イエメン", "region": "Haraz / Bani Matar",
        "latitude": 15.30, "longitude": 43.80, "altitude_min": 1500, "altitude_max": 2500,
        "climate": "Arid Highland", "slug": "yemen",
        "varieties": ["Dawairi", "Ismaili", "Tufahi"],
        "process_methods": ["Natural (Dry)"],
        "flavor_notes": ["Wild Berry", "Spice", "Dried Fruit", "Earthy"],
        "acidity": 4, "bitterness": 3, "sweetness": 3, "body": 4,
        "description": "Yemen is one of the oldest coffee-producing countries, with cultivation methods unchanged for centuries. Beans are sun-dried in their cherry on stone rooftops, creating wild, complex flavors with deep dried-fruit sweetness and mysterious earthiness.",
        "description_ja": "数百年変わらない伝統農法。天日乾燥のナチュラルが生み出すワイルドでスパイシーな風味は世界唯一無二。",
        "data_source": "Yemen Coffee Association"
    },
    {
        "country": "Indonesia", "country_ja": "インドネシア", "region": "Sumatra / Sulawesi",
        "latitude": -2.00, "longitude": 113.00, "altitude_min": 1000, "altitude_max": 1500,
        "climate": "Tropical", "slug": "indonesia",
        "varieties": ["Typica", "Tim Tim", "Ateng"],
        "process_methods": ["Wet-Hulled (Giling Basah)"],
        "flavor_notes": ["Earthy", "Cedar", "Dark Chocolate", "Tobacco"],
        "acidity": 2, "bitterness": 4, "sweetness": 2, "body": 5,
        "description": "Indonesia's unique wet-hulling process (Giling Basah) produces exceptionally full-bodied, low-acid coffees with distinctive earthy and woody notes. Sumatra Mandheling and Sulawesi Toraja are iconic expressions of this rich, complex profile.",
        "description_ja": "ギリン・バサ（湿式脱穀）が生み出す独特のアーシーさと重厚なボディ。スマトラマンデリングが有名。",
        "data_source": "AEKI Indonesia"
    },
    {
        "country": "Vietnam", "country_ja": "ベトナム", "region": "Central Highlands",
        "latitude": 14.00, "longitude": 108.00, "altitude_min": 500, "altitude_max": 1500,
        "climate": "Tropical", "slug": "vietnam",
        "varieties": ["Robusta", "Arabica"],
        "process_methods": ["Natural", "Washed"],
        "flavor_notes": ["Chocolate", "Rubbery", "Woody", "Strong Bitter"],
        "acidity": 1, "bitterness": 5, "sweetness": 2, "body": 5,
        "description": "Vietnam is the world's second-largest coffee producer, dominated by Robusta. Vietnamese coffee is known for its intense strength and low acidity, traditionally served with condensed milk. Arabica is grown in cooler highland areas.",
        "description_ja": "世界第2位の生産国。ロブスタ主体の強烈な苦みと低い酸味。コンデンスミルクとの相性が抜群。",
        "data_source": "VICOFA"
    },
    {
        "country": "Honduras", "country_ja": "ホンジュラス", "region": "Copán / Marcala",
        "latitude": 14.80, "longitude": -86.80, "altitude_min": 1000, "altitude_max": 1800,
        "climate": "Subtropical", "slug": "honduras",
        "varieties": ["Bourbon", "Catuai", "Lempira"],
        "process_methods": ["Washed"],
        "flavor_notes": ["Peach", "Milk Chocolate", "Citrus", "Caramel"],
        "acidity": 3, "bitterness": 2, "sweetness": 4, "body": 3,
        "description": "Honduras has quietly risen to become one of Central America's top coffee producers. High-altitude farms in the Copán and Marcala regions produce sweet, well-balanced coffees with stone fruit and milk chocolate character.",
        "description_ja": "中米トップクラスの生産国に急成長。コパン・マルカラのピーチとミルクチョコレートのバランスが魅力。",
        "data_source": "IHCAFE"
    },
    {
        "country": "Mexico", "country_ja": "メキシコ", "region": "Chiapas / Oaxaca",
        "latitude": 16.70, "longitude": -92.60, "altitude_min": 900, "altitude_max": 1700,
        "climate": "Subtropical", "slug": "mexico",
        "varieties": ["Typica", "Bourbon", "Maragogipe"],
        "process_methods": ["Washed"],
        "flavor_notes": ["Nutty", "Chocolate", "Mild Citrus", "Caramel"],
        "acidity": 3, "bitterness": 3, "sweetness": 3, "body": 3,
        "description": "Mexico produces clean, mild coffees ideal for everyday drinking. Chiapas and Oaxaca lead production, offering balanced cups with gentle nutty and chocolatey notes. Mexican coffee is often organic, grown by smallholder farmers.",
        "description_ja": "マイルドで飲みやすい日常使いのコーヒー。チアパス・オアハカが主産地。有機栽培が多い。",
        "data_source": "AMECAFE"
    },
    {
        "country": "Tanzania", "country_ja": "タンザニア", "region": "Kilimanjaro / Mbeya",
        "latitude": -6.80, "longitude": 35.70, "altitude_min": 1400, "altitude_max": 2000,
        "climate": "Tropical Highland", "slug": "tanzania",
        "varieties": ["Bourbon", "Kent", "Arusha"],
        "process_methods": ["Washed"],
        "flavor_notes": ["Black Tea", "Plum", "Citrus", "Floral"],
        "acidity": 4, "bitterness": 2, "sweetness": 3, "body": 3,
        "description": "Tanzania produces elegant East African coffees with a distinctive tea-like quality. Farms on the slopes of Mount Kilimanjaro and in the Mbeya highlands create bright, complex cups with plum and citrus notes that linger on the palate.",
        "description_ja": "キリマンジャロ山麓とムベヤ高原が産地。紅茶を思わせる上品な酸味とプラムの余韻が特徴。",
        "data_source": "TCB Tanzania"
    },
    {
        "country": "Rwanda", "country_ja": "ルワンダ", "region": "Western Province",
        "latitude": -2.00, "longitude": 29.50, "altitude_min": 1500, "altitude_max": 2000,
        "climate": "Tropical Highland", "slug": "rwanda",
        "varieties": ["Bourbon"],
        "process_methods": ["Washed", "Natural"],
        "flavor_notes": ["Raspberry", "Hibiscus", "Caramel", "Floral"],
        "acidity": 5, "bitterness": 1, "sweetness": 4, "body": 3,
        "description": "Rwanda has transformed its coffee industry since the early 2000s into a showcase of African specialty coffee. Bourbon cultivars grown at high altitude produce cups bursting with raspberry and hibiscus notes — some of the most elegant and delicate coffees in the world.",
        "description_ja": "高品質化に成功した東アフリカの新星。ラズベリーとハイビスカスの繊細なフレーバーで世界から注目される。",
        "data_source": "NAEB Rwanda"
    },
    {
        "country": "Peru", "country_ja": "ペルー", "region": "Cajamarca / Junín",
        "latitude": -7.00, "longitude": -78.50, "altitude_min": 1200, "altitude_max": 2000,
        "climate": "Tropical Highland", "slug": "peru",
        "varieties": ["Typica", "Bourbon", "Caturra"],
        "process_methods": ["Washed"],
        "flavor_notes": ["Milk Chocolate", "Toffee", "Green Apple", "Mild"],
        "acidity": 3, "bitterness": 2, "sweetness": 4, "body": 3,
        "description": "Peru has emerged as a significant organic coffee producer. The high-altitude farms of Cajamarca and Junín produce clean, sweet coffees with gentle chocolate and toffee notes. Peru is one of the world's largest certified organic coffee exporters.",
        "description_ja": "有機コーヒーの主要生産国。カハマルカ・フニンの高地でマイルドなチョコレートとトフィーの風味を育む。",
        "data_source": "JNC Peru"
    },
    {
        "country": "El Salvador", "country_ja": "エルサルバドル", "region": "Apaneca-Ilamatepec",
        "latitude": 13.80, "longitude": -89.70, "altitude_min": 1000, "altitude_max": 1800,
        "climate": "Subtropical", "slug": "el-salvador",
        "varieties": ["Bourbon", "Pacamara"],
        "process_methods": ["Washed", "Natural", "Honey"],
        "flavor_notes": ["Brown Sugar", "Stone Fruit", "Chocolate", "Mild Acidity"],
        "acidity": 3, "bitterness": 2, "sweetness": 5, "body": 4,
        "description": "El Salvador is famous for the Pacamara variety — a large-bean hybrid with exceptional sweetness and complexity. The volcanic highlands of Apaneca-Ilamatepec provide ideal conditions for producing sweet, full-bodied coffees.",
        "description_ja": "パカマラ品種の故郷。火山高地が育むブラウンシュガーとストーンフルーツの甘みが魅力。",
        "data_source": "CSC El Salvador"
    },
    {
        "country": "Papua New Guinea", "country_ja": "パプアニューギニア", "region": "Western Highlands",
        "latitude": -5.80, "longitude": 144.30, "altitude_min": 1500, "altitude_max": 2100,
        "climate": "Tropical Highland", "slug": "papua-new-guinea",
        "varieties": ["Typica", "Arusha"],
        "process_methods": ["Washed"],
        "flavor_notes": ["Fruity", "Earthy", "Tropical", "Wild"],
        "acidity": 4, "bitterness": 2, "sweetness": 3, "body": 4,
        "description": "Papua New Guinea produces wild, complex coffees from smallholder gardens in the Western Highlands. Grown with minimal chemical inputs, these coffees reflect the rich biodiversity of the island, offering tropical and earthy character.",
        "description_ja": "西高地の小規模農園産。熱帯の複雑なフレーバーと野生味あるアーシーさが魅力の個性派コーヒー。",
        "data_source": "CIC Papua New Guinea"
    },
    {
        "country": "India", "country_ja": "インド", "region": "Coorg / Chikmagalur",
        "latitude": 12.50, "longitude": 75.80, "altitude_min": 900, "altitude_max": 1500,
        "climate": "Tropical", "slug": "india",
        "varieties": ["Arabica", "Robusta"],
        "process_methods": ["Washed", "Monsooned"],
        "flavor_notes": ["Spice", "Earthy", "Dark Chocolate", "Low Acidity"],
        "acidity": 2, "bitterness": 4, "sweetness": 2, "body": 5,
        "description": "India's coffee is unique for its Monsooning process — beans are exposed to monsoon winds for weeks, creating a distinctive mellow, low-acid coffee with earthy spice. Coorg and Chikmagalur produce most of India's fine Arabica under spice-tree shade.",
        "description_ja": "モンスーン精製が生む独特の低酸・アーシースパイスが特徴。クールグ・チクマガルールのシェードアラビカが有名。",
        "data_source": "Coffee Board of India"
    },
    {
        "country": "Burundi", "country_ja": "ブルンジ", "region": "Ngozi / Kayanza",
        "latitude": -3.30, "longitude": 29.90, "altitude_min": 1400, "altitude_max": 2000,
        "climate": "Tropical Highland", "slug": "burundi",
        "varieties": ["Bourbon"],
        "process_methods": ["Washed"],
        "flavor_notes": ["Peach", "Apricot", "Floral", "Black Tea"],
        "acidity": 5, "bitterness": 1, "sweetness": 4, "body": 3,
        "description": "Burundi produces some of Africa's most elegant coffees, often compared to Rwanda in their floral delicacy. Bourbon cultivars in the Ngozi and Kayanza regions develop complex stone fruit and tea-like characteristics under the Great Rift Valley climate.",
        "description_ja": "アフリカ屈指の繊細さ。ルワンダと並ぶフローラルな香りとピーチ・アプリコットの上品なフレーバー。",
        "data_source": "ARFIC Burundi"
    },
    {
        "country": "Bolivia", "country_ja": "ボリビア", "region": "Caranavi",
        "latitude": -15.80, "longitude": -67.60, "altitude_min": 1000, "altitude_max": 2300,
        "climate": "Tropical Highland", "slug": "bolivia",
        "varieties": ["Typica", "Caturra"],
        "process_methods": ["Washed"],
        "flavor_notes": ["Peach", "Vanilla", "Milk Chocolate", "Floral"],
        "acidity": 4, "bitterness": 2, "sweetness": 4, "body": 3,
        "description": "Bolivia is a hidden gem of South American specialty coffee. The Caranavi region's extreme altitude (up to 2,300m) and cool temperatures create slow-ripening beans with exceptional sweetness and delicate floral and stone fruit character.",
        "description_ja": "南米の隠れた逸品。カラナビの極高地（最大2300m）が生む繊細なバニラとピーチの甘みが際立つ。",
        "data_source": "FECAFEB Bolivia"
    },
    {
        "country": "Jamaica", "country_ja": "ジャマイカ", "region": "Blue Mountain",
        "latitude": 18.10, "longitude": -76.70, "altitude_min": 900, "altitude_max": 1700,
        "climate": "Tropical", "slug": "jamaica",
        "varieties": ["Typica"],
        "process_methods": ["Washed"],
        "flavor_notes": ["Mild", "Creamy", "Nutty", "No Bitterness"],
        "acidity": 3, "bitterness": 1, "sweetness": 4, "body": 4,
        "description": "Jamaica Blue Mountain is one of the most exclusive coffees in the world. Grown in the misty Blue Mountains, it is prized for its impossibly smooth, well-balanced cup with no bitterness — a rare quality achieved by cool temperatures and high humidity.",
        "description_ja": "世界最高峰のコーヒーの一つ。ブルーマウンテンの霧の中で育つ苦みのないクリーミーなカップは唯一無二。",
        "data_source": "CIB Jamaica"
    },
    {
        "country": "Panama", "country_ja": "パナマ", "region": "Boquete / Volcán",
        "latitude": 8.78, "longitude": -82.44, "altitude_min": 1200, "altitude_max": 1800,
        "climate": "Tropical Highland", "slug": "panama",
        "varieties": ["Gesha", "Typica", "Caturra"],
        "process_methods": ["Washed", "Natural"],
        "flavor_notes": ["Jasmine", "Bergamot", "Peach", "Tropical Fruit"],
        "acidity": 5, "bitterness": 1, "sweetness": 4, "body": 2,
        "description": "Panama is home to the legendary Gesha variety, which revolutionized the specialty coffee world in 2004. Boquete and Volcán produce strikingly aromatic coffees with jasmine, bergamot, and tropical fruit — often fetching record auction prices.",
        "description_ja": "ゲシャ品種の聖地。2004年に世界を驚かせた伝説の産地。ジャスミンとベルガモットの圧倒的な香りは競売で最高値を記録する。",
        "data_source": "SCAP Panama / World Coffee Research"
    },
    {
        "country": "Nicaragua", "country_ja": "ニカラグア", "region": "Jinotega / Matagalpa",
        "latitude": 13.09, "longitude": -85.71, "altitude_min": 1000, "altitude_max": 1700,
        "climate": "Subtropical", "slug": "nicaragua",
        "varieties": ["Bourbon", "Caturra", "Maragogipe"],
        "process_methods": ["Washed"],
        "flavor_notes": ["Chocolate", "Citrus", "Caramel", "Nuts"],
        "acidity": 3, "bitterness": 2, "sweetness": 4, "body": 3,
        "description": "Nicaragua produces balanced, approachable specialty coffees from the highlands of Jinotega and Matagalpa. The Maragogipe variety — known for its unusually large beans — produces complex cups with caramel sweetness and bright citrus notes.",
        "description_ja": "ヒノテガ・マタガルパ高地が産地。大粒で有名なマラゴジッペ品種はキャラメルと柑橘の複雑な風味を持つ。",
        "data_source": "CONACAFE Nicaragua"
    },
    {
        "country": "Ecuador", "country_ja": "エクアドル", "region": "Loja / Pichincha",
        "latitude": -4.00, "longitude": -79.20, "altitude_min": 1200, "altitude_max": 2000,
        "climate": "Tropical Highland", "slug": "ecuador",
        "varieties": ["Typica", "Bourbon", "Sidra"],
        "process_methods": ["Washed", "Natural"],
        "flavor_notes": ["Floral", "Citrus", "Caramel", "Stone Fruit"],
        "acidity": 4, "bitterness": 2, "sweetness": 4, "body": 3,
        "description": "Ecuador is an emerging specialty origin with remarkable potential. The Sidra variety — exclusive to Ecuador — produces strikingly floral and fruity cups. Loja and Pichincha benefit from the equatorial climate and high altitude to develop exceptional sweetness.",
        "description_ja": "新興スペシャルティ産地。エクアドル固有のシドラ品種はフローラルで果実味豊か。赤道直下の高地気候が卓越した甘みを生む。",
        "data_source": "COFENAC Ecuador / World Coffee Research"
    },
    {
        "country": "Uganda", "country_ja": "ウガンダ", "region": "Mt. Elgon / Rwenzori",
        "latitude": 1.30, "longitude": 34.20, "altitude_min": 1500, "altitude_max": 2300,
        "climate": "Tropical Highland", "slug": "uganda",
        "varieties": ["SL14", "SL28", "Robusta"],
        "process_methods": ["Washed", "Natural"],
        "flavor_notes": ["Berry", "Cocoa", "Black Tea", "Full-bodied"],
        "acidity": 3, "bitterness": 3, "sweetness": 3, "body": 4,
        "description": "Uganda is one of Africa's largest coffee producers, growing both Arabica on the slopes of Mt. Elgon and Rwenzori, and Robusta in lower elevations. The high-altitude Arabica produces vibrant berry and cocoa notes with a satisfying full body.",
        "description_ja": "エルゴン山・ルウェンゾリ山麓のアラビカはベリーとカカオが際立つ。アフリカ有数の生産量を誇る実力派産地。",
        "data_source": "UCDA Uganda"
    },
    {
        "country": "Malawi", "country_ja": "マラウイ", "region": "Misuku Hills / Thyolo",
        "latitude": -9.50, "longitude": 34.00, "altitude_min": 900, "altitude_max": 1800,
        "climate": "Tropical Highland", "slug": "malawi",
        "varieties": ["Gesha", "Typica", "Catimor"],
        "process_methods": ["Washed"],
        "flavor_notes": ["Stone Fruit", "Chocolate", "Floral", "Mild Acidity"],
        "acidity": 3, "bitterness": 2, "sweetness": 4, "body": 3,
        "description": "Malawi is one of Africa's lesser-known yet quality-focused origins. The Misuku Hills in the north produce clean, sweet coffees with stone fruit and floral notes. The presence of Gesha cultivars at high altitude is drawing growing attention from the specialty world.",
        "description_ja": "知る人ぞ知るアフリカの実力派。ミスク丘陵のゲシャ種はストーンフルーツとフローラルが際立つ高品質コーヒーを生む。",
        "data_source": "Malawi Coffee Association"
    },
    {
        "country": "Dominican Republic", "country_ja": "ドミニカ共和国", "region": "Barahona / Cibao",
        "latitude": 18.70, "longitude": -71.00, "altitude_min": 600, "altitude_max": 1600,
        "climate": "Tropical", "slug": "dominican-republic",
        "varieties": ["Typica", "Caturra", "Bourbon"],
        "process_methods": ["Washed"],
        "flavor_notes": ["Mild", "Nutty", "Chocolate", "Sweet"],
        "acidity": 3, "bitterness": 2, "sweetness": 4, "body": 3,
        "description": "The Dominican Republic produces mild, sweet coffees from the mountainous regions of Barahona and the Cibao Valley. Once a significant Caribbean exporter, the country is reviving its specialty sector with clean, chocolatey profiles that suit everyday drinking.",
        "description_ja": "バラオナとシバオ渓谷が産地。マイルドで甘いチョコレート系フレーバーのカリブ海コーヒー。スペシャルティ復活に向けた取り組みが進む。",
        "data_source": "CODOCAFE Dominican Republic"
    },
    {
        "country": "Cuba", "country_ja": "キューバ", "region": "Sierra Maestra / Escambray",
        "latitude": 20.00, "longitude": -76.00, "altitude_min": 500, "altitude_max": 1500,
        "climate": "Tropical", "slug": "cuba",
        "varieties": ["Typica (Crystal Mountain)", "Bourbon"],
        "process_methods": ["Washed"],
        "flavor_notes": ["Sweet", "Mild", "Chocolate", "Low Acidity"],
        "acidity": 2, "bitterness": 2, "sweetness": 4, "body": 3,
        "description": "Cuban coffee carries historical mystique and a gentle, low-acid character. Crystal Mountain — grown on the slopes of the Sierra Maestra — is the island's most prized variety, producing smooth, sweet cups with mild chocolate notes that reflect Cuba's colonial coffee heritage.",
        "description_ja": "歴史的な神秘を纏うキューバコーヒー。シエラマエストラ産クリスタルマウンテンはマイルドでチョコレートの甘みが上品。",
        "data_source": "Grupo Empresarial del Tabaco y Café Cuba"
    },
    {
        "country": "Thailand", "country_ja": "タイ", "region": "Chiang Rai / Doi Chang",
        "latitude": 19.80, "longitude": 99.60, "altitude_min": 1200, "altitude_max": 1800,
        "climate": "Subtropical Highland", "slug": "thailand",
        "varieties": ["Arabica", "Catimor"],
        "process_methods": ["Washed", "Natural", "Honey"],
        "flavor_notes": ["Honey", "Peach", "Mild Chocolate", "Light Floral"],
        "acidity": 3, "bitterness": 2, "sweetness": 4, "body": 2,
        "description": "Thailand's northern highlands around Chiang Rai and Doi Chang have developed a thriving specialty coffee culture. Arabica grown at high altitude produces clean, honey-like sweetness with peach and light floral notes, supported by government and royal projects promoting quality.",
        "description_ja": "チェンライ・ドイチャン高地が産地。王室プロジェクトが品質を後押し。ハニーとピーチの甘みを持つ洗練されたスペシャルティ。",
        "data_source": "Thai Coffee Association / Royal Project Foundation"
    },
    {
        "country": "China", "country_ja": "中国（雲南）", "region": "Yunnan / Pu'er",
        "latitude": 23.00, "longitude": 100.00, "altitude_min": 1000, "altitude_max": 2000,
        "climate": "Subtropical", "slug": "china-yunnan",
        "varieties": ["Catimor", "Bourbon", "Typica"],
        "process_methods": ["Washed", "Natural"],
        "flavor_notes": ["Mild", "Nuts", "Chocolate", "Earthy"],
        "acidity": 2, "bitterness": 3, "sweetness": 3, "body": 3,
        "description": "China's Yunnan province is a rapidly growing coffee origin, centered around the city of Pu'er. The subtropical highland climate produces mild, chocolatey coffees that are gaining recognition in the specialty world as processing and farming techniques rapidly improve.",
        "description_ja": "急成長する雲南省プーアル周辺が主産地。マイルドなチョコレート系フレーバーで、農業技術・精製技術の向上とともに国際評価が急上昇。",
        "data_source": "Yunnan Coffee Exchange / ICO"
    },
    {
        "country": "Philippines", "country_ja": "フィリピン", "region": "Sagada / Benguet",
        "latitude": 17.00, "longitude": 121.00, "altitude_min": 1200, "altitude_max": 1800,
        "climate": "Tropical Highland", "slug": "philippines",
        "varieties": ["Typica", "Benguet", "Excelsa"],
        "process_methods": ["Washed"],
        "flavor_notes": ["Mild", "Chocolate", "Nutty", "Herbal"],
        "acidity": 2, "bitterness": 3, "sweetness": 3, "body": 3,
        "description": "The Philippines grows all four commercially cultivated coffee species: Arabica, Robusta, Liberica, and Excelsa. The Cordillera highlands of Sagada and Benguet produce mild Arabica with herbal and chocolatey notes, while Barako (Liberica) is a cultural icon.",
        "description_ja": "アラビカ・ロブスタ・リベリカ・エクセルサの4種を栽培する世界屈指の多様性。コルディリェラ高地産のアラビカはハーバルで穏やかな風味。",
        "data_source": "Philippine Coffee Board"
    },
    {
        "country": "Zambia", "country_ja": "ザンビア", "region": "Muchinga / Northern Province",
        "latitude": -11.00, "longitude": 31.00, "altitude_min": 1300, "altitude_max": 1800,
        "climate": "Tropical Highland", "slug": "zambia",
        "varieties": ["Bourbon", "Caturra"],
        "process_methods": ["Washed"],
        "flavor_notes": ["Citrus", "Peach", "Mild Chocolate", "Floral"],
        "acidity": 4, "bitterness": 2, "sweetness": 4, "body": 3,
        "description": "Zambia is one of Africa's most underrated specialty origins. The Muchinga escarpment and Northern Province produce elegant, citrusy coffees with peach and floral notes. Large estate farms maintain consistent quality, making Zambia a rising star in the specialty market.",
        "description_ja": "アフリカで最も過小評価された産地の一つ。ムチンガ高地の大農園が安定した品質を供給。柑橘とピーチの上品なフレーバーが特徴。",
        "data_source": "Coffee Association of Zambia"
    },
    {
        "country": "DR Congo", "country_ja": "コンゴ民主共和国", "region": "North Kivu / South Kivu",
        "latitude": -1.50, "longitude": 29.00, "altitude_min": 1400, "altitude_max": 2000,
        "climate": "Tropical Highland", "slug": "dr-congo",
        "varieties": ["Bourbon", "Typica"],
        "process_methods": ["Washed"],
        "flavor_notes": ["Dark Chocolate", "Fruity", "Earthy", "Full-bodied"],
        "acidity": 3, "bitterness": 3, "sweetness": 3, "body": 4,
        "description": "The Democratic Republic of Congo is home to some of Africa's most extraordinary natural coffee potential. The volcanic soils of North and South Kivu around Lake Kivu produce rich, full-bodied coffees with dark chocolate and tropical fruit notes at high altitudes.",
        "description_ja": "キブ湖周辺の火山性土壌が育む豊潤なコーヒー。ダークチョコレートとフルーツの複雑なフレーバーはアフリカ屈指のポテンシャルを持つ。",
        "data_source": "ONAPAC Congo / ICO"
    },
]


def run():
    db = SessionLocal()
    try:
        if db.query(Origin).count() > 0:
            return
        for data in ORIGINS:
            origin = Origin(
                country=data["country"],
                country_ja=data["country_ja"],
                region=data["region"],
                latitude=data["latitude"],
                longitude=data["longitude"],
                altitude_min=data["altitude_min"],
                altitude_max=data["altitude_max"],
                climate=data["climate"],
                slug=data["slug"],
                varieties=json.dumps(data["varieties"]),
                process_methods=json.dumps(data["process_methods"]),
                flavor_notes=json.dumps(data["flavor_notes"]),
                acidity=data["acidity"],
                bitterness=data["bitterness"],
                sweetness=data["sweetness"],
                body=data["body"],
                description=data["description"],
                description_ja=data["description_ja"],
                data_source=data["data_source"],
            )
            db.add(origin)
        db.commit()
    finally:
        db.close()



import { ref } from 'vue'

export type Locale = 'en' | 'ja'

const locale = ref<Locale>('ja')

const messages = {
  en: {
    nav: { map: 'Map', origins: 'Origins' },
    footer: 'Coffee Origin Atlas',
    origins: {
      title: 'Coffee Origins',
      loading: 'Loading...',
      error: 'Failed to load origins',
    },
    detail: {
      loading: 'Loading...',
      notFound: 'Origin not found',
      flavorProfile: 'Flavor Profile',
      flavorNotes: 'Flavor Notes',
      varieties: 'Varieties',
      processMethods: 'Process Methods',
      roastLevel: 'Roast Level',
      subRegion: 'Sub-region',
      farm: 'Farm',
      back: '← Back to Origins',
    },
    flavor: {
      acidity: 'Acidity',
      bitterness: 'Bitterness',
      sweetness: 'Sweetness',
      body: 'Body',
    },
    panel: {
      flavorNotes: 'Flavor Notes',
      flavorProfile: 'Flavor Profile',
      varieties: 'Varieties',
      process: 'Process',
      viewFull: 'View Full Profile →',
    },
    filter: {
      searchPlaceholder: 'Search by country, region, variety...',
      region: 'Region',
      flavor: 'Flavor',
      process: 'Process',
      roast: 'Roast',
      sort: 'Sort',
      sortDefault: 'Default',
      altitude: 'Altitude',
      all: 'All',
      reset: 'Reset filters',
      resultsSuffix: ' origins',
      noResults: 'No origins match these filters.',
    },
  },
  ja: {
    nav: { map: 'マップ', origins: '産地一覧' },
    footer: 'コーヒー産地アトラス',
    origins: {
      title: 'コーヒー産地一覧',
      loading: '読み込み中...',
      error: 'データの取得に失敗しました',
    },
    detail: {
      loading: '読み込み中...',
      notFound: '産地が見つかりません',
      flavorProfile: 'フレーバープロファイル',
      flavorNotes: 'フレーバーノート',
      varieties: '品種',
      processMethods: '精製方法',
      roastLevel: '焙煎度',
      subRegion: 'サブリージョン',
      farm: '農園',
      back: '← 産地一覧に戻る',
    },
    flavor: {
      acidity: '酸味',
      bitterness: '苦味',
      sweetness: '甘味',
      body: 'コク',
    },
    panel: {
      flavorNotes: 'フレーバーノート',
      flavorProfile: 'フレーバープロファイル',
      varieties: '品種',
      process: '精製方法',
      viewFull: '詳細を見る →',
    },
    filter: {
      searchPlaceholder: '国名・地域・品種で検索...',
      region: '地域',
      flavor: 'フレーバー',
      process: '精製方法',
      roast: '焙煎度',
      sort: '並び替え',
      sortDefault: 'おすすめ順',
      altitude: '標高',
      all: 'すべて',
      reset: '絞り込みを解除',
      resultsSuffix: '件の産地',
      noResults: '条件に合う産地が見つかりませんでした。',
    },
  },
}

const termMap: Record<string, string> = {
  // 品種
  'Heirloom': 'エアルーム',
  'Castillo': 'カスティジョ',
  'Caturra': 'カトゥーラ',
  'Colombia': 'コロンビア',
  'Bourbon': 'ブルボン',
  'Mundo Novo': 'ムンドノーボ',
  'Catuai': 'カトゥアイ',
  'Typica': 'ティピカ',
  'SL28': 'SL28',
  'SL34': 'SL34',
  'Ruiru 11': 'ルイル11',
  'Dawairi': 'ダワイリ',
  'Ismaili': 'イスマイリ',
  'Tufahi': 'トゥファヒ',
  'Tim Tim': 'ティム・ティム',
  'Ateng': 'アテン',
  'Robusta': 'ロブスタ',
  'Arabica': 'アラビカ',
  'Lempira': 'レンピーラ',
  'Maragogipe': 'マラゴジペ',
  'Kent': 'ケント',
  'Arusha': 'アルーシャ',
  'Pacamara': 'パカマラ',
  // 精製方法
  'Natural': 'ナチュラル',
  'Washed': 'ウォッシュド',
  'Pulped Natural': 'パルプドナチュラル',
  'Honey': 'ハニー',
  'Washed (Double Fermentation)': 'ウォッシュド（ダブル発酵）',
  'Natural (Dry)': 'ナチュラル（乾燥）',
  'Wet-Hulled (Giling Basah)': 'ウェットハルド（ギリン・バサー）',
  'Monsooned': 'モンスーン',
  // フレーバーノート
  'Blueberry': 'ブルーベリー',
  'Citrus': 'シトラス',
  'Red Apple': '赤リンゴ',
  'Berry': 'ベリー',
  'Apricot': 'アプリコット',
  'Blackcurrant': 'ブラックカラント',
  'Grapefruit': 'グレープフルーツ',
  'Wild Berry': 'ワイルドベリー',
  'Dried Fruit': 'ドライフルーツ',
  'Peach': '桃',
  'Mild Citrus': 'マイルドシトラス',
  'Plum': 'プラム',
  'Raspberry': 'ラズベリー',
  'Green Apple': '青リンゴ',
  'Stone Fruit': 'ストーンフルーツ',
  'Fruity': 'フルーティ',
  'Tropical': 'トロピカル',
  'Caramel': 'キャラメル',
  'Chocolate': 'チョコレート',
  'Dark Chocolate': 'ダークチョコレート',
  'Milk Chocolate': 'ミルクチョコレート',
  'Brown Sugar': 'ブラウンシュガー',
  'Toffee': 'トフィー',
  'Vanilla': 'バニラ',
  'Creamy': 'クリーミー',
  'Jasmine': 'ジャスミン',
  'Floral': 'フローラル',
  'Hibiscus': 'ハイビスカス',
  'Spice': 'スパイス',
  'Earthy': 'アーシー',
  'Cedar': 'シダー',
  'Tobacco': 'タバコ',
  'Wild': 'ワイルド',
  'Rubbery': 'ゴム感',
  'Woody': 'ウッディ',
  'Black Tea': '紅茶',
  'Wine-like': 'ワイン',
  'Nutty': 'ナッティ',
  'Nuts': 'ナッツ',
  'Low Acidity': '低酸味',
  'Tomato': 'トマト',
  'Strong Bitter': '強い苦味',
  'Mild': 'マイルド',
  'Mild Acidity': 'マイルドな酸味',
  'No Bitterness': '苦味なし',
  // 焙煎度
  'Light': '浅煎り',
  'Medium-Light': 'ミディアムライト',
  'Medium': '中煎り',
  'Medium-Dark': 'ミディアムダーク',
  'Dark': '深煎り',
  // 地域
  'Africa': 'アフリカ',
  'Americas': '南北アメリカ',
  'Asia & Pacific': 'アジア・太平洋',
}

type Messages = typeof messages.en
type DotPaths<T, Prefix extends string = ''> =
  T extends string
    ? Prefix
    : { [K in keyof T & string]: DotPaths<T[K], Prefix extends '' ? K : `${Prefix}.${K}`> }[keyof T & string]

export function useLocale() {
  function t(path: DotPaths<Messages>): string {
    const keys = path.split('.')
    let val: any = messages[locale.value]
    for (const k of keys) val = val?.[k]
    return val ?? path
  }

  function toggle() {
    locale.value = locale.value === 'en' ? 'ja' : 'en'
  }

  function translateTerm(term: string): string {
    if (locale.value === 'ja') return termMap[term] ?? term
    return term
  }

  return { locale, t, toggle, translateTerm }
}

import { watchEffect, toValue, type MaybeRefOrGetter } from 'vue'

export interface PageMetaOptions {
  /** Page title without the site name suffix. */
  title: string
  description: string
  /** Absolute image URL for social sharing. */
  image?: string
  /** Path (e.g. "/origins/kenya") used to build the canonical/og:url. */
  path: string
}

const SITE_NAME = 'BeanAtlas'
const SITE_URL = 'https://beanatlas.net'
const DEFAULT_IMAGE = `${SITE_URL}/beanatlas-logo.png`

function setMetaTag(attr: 'name' | 'property', key: string, content: string) {
  let el = document.head.querySelector(`meta[${attr}="${key}"]`)
  if (!el) {
    el = document.createElement('meta')
    el.setAttribute(attr, key)
    document.head.appendChild(el)
  }
  el.setAttribute('content', content)
}

function setLinkTag(rel: string, href: string) {
  let el = document.head.querySelector(`link[rel="${rel}"]`)
  if (!el) {
    el = document.createElement('link')
    el.setAttribute('rel', rel)
    document.head.appendChild(el)
  }
  el.setAttribute('href', href)
}

/**
 * Applies a per-page <title>, meta description, canonical link, and
 * Open Graph / Twitter Card tags. Re-runs whenever the reactive source
 * changes (e.g. once async origin data finishes loading).
 */
export function usePageMeta(source: MaybeRefOrGetter<PageMetaOptions>) {
  watchEffect(() => {
    const { title, description, image = DEFAULT_IMAGE, path } = toValue(source)
    const fullTitle = `${title} | ${SITE_NAME}`
    const url = `${SITE_URL}${path}`

    document.title = fullTitle
    setMetaTag('name', 'description', description)
    setLinkTag('canonical', url)

    setMetaTag('property', 'og:type', 'website')
    setMetaTag('property', 'og:site_name', SITE_NAME)
    setMetaTag('property', 'og:locale', 'ja_JP')
    setMetaTag('property', 'og:title', fullTitle)
    setMetaTag('property', 'og:description', description)
    setMetaTag('property', 'og:url', url)
    setMetaTag('property', 'og:image', image)

    setMetaTag('name', 'twitter:card', 'summary_large_image')
    setMetaTag('name', 'twitter:title', fullTitle)
    setMetaTag('name', 'twitter:description', description)
    setMetaTag('name', 'twitter:image', image)
  })
}

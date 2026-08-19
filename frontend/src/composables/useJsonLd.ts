import { watchEffect, toValue, type MaybeRefOrGetter } from 'vue'

const SCRIPT_ID = 'ld-json'

/**
 * Injects a single <script type="application/ld+json"> tag into <head>,
 * replacing its contents whenever the source changes. Pass null/undefined
 * to remove the tag (e.g. while data is still loading).
 */
export function useJsonLd(source: MaybeRefOrGetter<object | null | undefined>) {
  watchEffect(() => {
    const data = toValue(source)
    let el = document.head.querySelector<HTMLScriptElement>(`script#${SCRIPT_ID}`)

    if (!data) {
      el?.remove()
      return
    }

    if (!el) {
      el = document.createElement('script')
      el.id = SCRIPT_ID
      el.type = 'application/ld+json'
      document.head.appendChild(el)
    }
    el.textContent = JSON.stringify(data)
  })
}

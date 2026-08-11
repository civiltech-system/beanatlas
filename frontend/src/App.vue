<template>
  <header class="sticky top-0 z-50 bg-coffee-50/80 backdrop-blur border-b border-coffee-200">
    <div class="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between">
      <RouterLink to="/" class="flex items-center h-full py-1.5">
        <picture class="h-full block">
          <source srcset="/beanatlas-header.webp" type="image/webp" />
          <img src="/beanatlas-header.png" alt="BeanAtlas" class="h-full w-auto" width="1458" height="270" />
        </picture>
      </RouterLink>

      <!-- PC ナビ -->
      <nav class="hidden sm:flex items-center gap-6 text-sm text-coffee-500">
        <RouterLink to="/" class="hover:text-coffee-600 transition-colors">{{ t('nav.map') }}</RouterLink>
        <RouterLink to="/origins" class="hover:text-coffee-600 transition-colors">{{ t('nav.origins') }}</RouterLink>
        <a
          href="https://github.com/civiltech-system/BeanAtlas"
          target="_blank"
          rel="noopener"
          class="hover:text-coffee-600 transition-colors"
        >GitHub</a>
        <button
          @click="toggle"
          class="text-xs border border-coffee-300 rounded px-2 py-0.5 hover:border-coffee-500 hover:text-coffee-600 transition-colors"
        >{{ locale === 'en' ? 'JA' : 'EN' }}</button>
      </nav>

      <!-- ハンバーガーボタン（モバイルのみ） -->
      <button
        class="sm:hidden flex flex-col justify-center items-center w-8 h-8 gap-1.5"
        @click="menuOpen = !menuOpen"
        :aria-expanded="menuOpen"
        aria-label="メニュー"
      >
        <span
          class="block w-5 h-0.5 bg-coffee-500 transition-all duration-200"
          :class="menuOpen ? 'rotate-45 translate-y-2' : ''"
        />
        <span
          class="block w-5 h-0.5 bg-coffee-500 transition-all duration-200"
          :class="menuOpen ? 'opacity-0' : ''"
        />
        <span
          class="block w-5 h-0.5 bg-coffee-500 transition-all duration-200"
          :class="menuOpen ? '-rotate-45 -translate-y-2' : ''"
        />
      </button>
    </div>

    <!-- モバイルメニュー -->
    <Transition
      enter-active-class="transition-all duration-200 ease-out"
      enter-from-class="opacity-0 -translate-y-2"
      enter-to-class="opacity-100 translate-y-0"
      leave-active-class="transition-all duration-150 ease-in"
      leave-from-class="opacity-100 translate-y-0"
      leave-to-class="opacity-0 -translate-y-2"
    >
      <nav
        v-if="menuOpen"
        class="sm:hidden border-t border-coffee-200 bg-coffee-50 px-6 py-4 flex flex-col gap-4 text-sm text-coffee-500"
      >
        <RouterLink to="/" class="hover:text-coffee-600 transition-colors" @click="menuOpen = false">{{ t('nav.map') }}</RouterLink>
        <RouterLink to="/origins" class="hover:text-coffee-600 transition-colors" @click="menuOpen = false">{{ t('nav.origins') }}</RouterLink>
        <a
          href="https://github.com/civiltech-system/BeanAtlas"
          target="_blank"
          rel="noopener"
          class="hover:text-coffee-600 transition-colors"
        >GitHub</a>
        <button
          @click="toggle"
          class="self-start text-xs border border-coffee-300 rounded px-2 py-0.5 hover:border-coffee-500 hover:text-coffee-600 transition-colors"
        >{{ locale === 'en' ? 'JA' : 'EN' }}</button>
      </nav>
    </Transition>
  </header>

  <main>
    <RouterView />
  </main>

  <footer class="border-t border-coffee-200 mt-16 py-8 text-center text-sm text-coffee-400">
    <p>© 2026 BeanAtlas — {{ t('footer') }}</p>
    <p class="mt-1">
      Map data ©
      <a href="https://www.openstreetmap.org/copyright" target="_blank" class="underline hover:text-coffee-600">OpenStreetMap</a>
      contributors
    </p>
  </footer>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useLocale } from '@/composables/useLocale'

const { locale, t, toggle } = useLocale()
const menuOpen = ref(false)
</script>

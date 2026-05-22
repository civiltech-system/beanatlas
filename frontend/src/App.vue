<template>
  <header class="sticky top-0 z-50 bg-coffee-50/80 backdrop-blur border-b border-coffee-200">
    <div class="max-w-7xl mx-auto px-6 h-14 flex items-center justify-between">
      <RouterLink to="/" class="flex items-center h-full py-1.5">
        <img src="/beanatlas-header.png" alt="BeanAtlas" class="h-full w-auto" />
      </RouterLink>
      <nav class="flex items-center gap-6 text-sm text-coffee-500">
        <RouterLink to="/" class="hover:text-coffee-600 transition-colors">Map</RouterLink>
        <RouterLink to="/origins" class="hover:text-coffee-600 transition-colors">Origins</RouterLink>
        <a
          href="https://github.com/civiltech-system/BeanAtlas"
          target="_blank"
          rel="noopener"
          class="hover:text-coffee-600 transition-colors"
        >GitHub</a>
      </nav>
    </div>
  </header>

  <main>
    <RouterView />
  </main>

  <footer class="border-t border-coffee-200 mt-16 py-8 text-center text-sm text-coffee-400">
    <p>© 2026 BeanAtlas — Coffee Origin Atlas</p>
    <p class="mt-1">
      Map data ©
      <a href="https://www.openstreetmap.org/copyright" target="_blank" class="underline hover:text-coffee-600">OpenStreetMap</a>
      contributors
    </p>
  </footer>
</template>

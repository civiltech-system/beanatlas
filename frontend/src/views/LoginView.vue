<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { FirebaseError } from 'firebase/app'
import { applyActionCode } from 'firebase/auth'
import { EmailVerificationRequiredError, useAuthStore } from '@/stores/auth'
import { firebaseAuth } from '@/lib/firebase'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()
const mode = ref<'login' | 'register'>('login')
const email = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')
const notice = ref('')
const verificationState = ref<'idle' | 'verifying' | 'success' | 'error'>('idle')

onMounted(async () => {
  if (route.query.mode !== 'verifyEmail' || typeof route.query.oobCode !== 'string') return

  verificationState.value = 'verifying'
  try {
    await applyActionCode(firebaseAuth, route.query.oobCode)
    verificationState.value = 'success'
  } catch {
    verificationState.value = 'error'
  }
})

async function proceedToLogin() {
  verificationState.value = 'idle'
  await router.replace('/login')
}

function authenticationErrorMessage(cause: unknown) {
  if (cause instanceof EmailVerificationRequiredError) {
    return 'メールアドレスの確認が完了していません。確認メールを再送しました。メール内のリンクを開いてからログインしてください。'
  }
  if (!(cause instanceof FirebaseError)) {
    return 'ログイン処理に失敗しました。時間をおいてもう一度お試しください。'
  }

  const messages: Record<string, string> = {
    'auth/invalid-credential': 'メールアドレスまたはパスワードが正しくありません。',
    'auth/invalid-email': 'メールアドレスの形式を確認してください。',
    'auth/email-already-in-use': 'このメールアドレスはすでに登録されています。',
    'auth/weak-password': 'パスワードは6文字以上で入力してください。',
    'auth/too-many-requests': '試行回数が多いため一時的に制限されています。時間をおいて再度お試しください。',
    'auth/network-request-failed': '通信に失敗しました。Wi-Fiやモバイル通信、広告ブロック設定を確認してください。',
    'auth/web-storage-unsupported': 'このブラウザではログイン情報を保存できません。プライベートブラウズを解除してお試しください。',
    'auth/operation-not-supported-in-this-environment': 'このブラウザ環境ではログインできません。SafariまたはChromeで開いてください。',
    'auth/unauthorized-domain': 'このサイトのドメインがFirebaseで許可されていません。管理者へお問い合わせください。',
  }
  return messages[cause.code] ?? `ログイン処理に失敗しました。（${cause.code}）`
}

async function submit() {
  loading.value = true
  error.value = ''
  notice.value = ''
  try {
    if (mode.value === 'register') {
      await auth.register(email.value, password.value)
      mode.value = 'login'
      password.value = ''
      notice.value = '確認メールを送信しました。メール内のリンクを開いてからログインしてください。'
      return
    }
    await auth.login(email.value, password.value)
    const redirect = typeof route.query.redirect === 'string' ? route.query.redirect : '/records'
    await router.replace(redirect)
  } catch (cause) {
    error.value = authenticationErrorMessage(cause)
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="max-w-md mx-auto px-6 py-12">
    <div v-if="verificationState !== 'idle'" class="bg-white rounded-2xl p-6 sm:p-8 shadow-sm text-center">
      <template v-if="verificationState === 'verifying'">
        <h1 class="text-2xl font-serif font-bold text-coffee-600 mb-3">メールアドレスを確認しています</h1>
        <p class="text-sm text-coffee-400">しばらくお待ちください。</p>
      </template>
      <template v-else-if="verificationState === 'success'">
        <h1 class="text-2xl font-serif font-bold text-coffee-600 mb-3">Your email has been verified</h1>
        <p class="text-sm text-coffee-400 mb-6">メールアドレスの確認が完了しました。ログインして飲んだコーヒーを記録できます。</p>
        <button class="rounded-lg bg-coffee-600 px-5 py-2.5 text-white hover:bg-coffee-500" @click="proceedToLogin">ログインへ進む</button>
      </template>
      <template v-else>
        <h1 class="text-2xl font-serif font-bold text-coffee-600 mb-3">メールアドレスを確認できませんでした</h1>
        <p class="text-sm text-coffee-400 mb-6">確認リンクが無効か、期限切れの可能性があります。ログイン画面から確認メールを再送してください。</p>
        <RouterLink to="/" class="inline-block rounded-lg bg-coffee-600 px-5 py-2.5 text-white hover:bg-coffee-500">トップに戻る</RouterLink>
      </template>
    </div>

    <div v-else class="bg-white rounded-2xl p-6 sm:p-8 shadow-sm">
      <h1 class="text-2xl font-serif font-bold text-coffee-600 mb-2">
        {{ mode === 'login' ? 'ログイン' : 'アカウント登録' }}
      </h1>
      <p class="text-sm text-coffee-400 mb-6">飲んだコーヒーを自分だけの記録として残せます。</p>

      <p v-if="notice" class="mb-4 rounded-lg bg-green-50 px-3 py-2 text-sm text-green-700" role="status">{{ notice }}</p>

      <form class="space-y-4" @submit.prevent="submit">
        <label class="block text-sm text-coffee-600">
          メールアドレス
          <input v-model.trim="email" type="email" inputmode="email" autocomplete="email" autocapitalize="none" :spellcheck="false" required class="mt-1 w-full rounded-lg border border-coffee-200 bg-coffee-50 px-3 py-2 outline-none focus:border-coffee-400" />
        </label>
        <label class="block text-sm text-coffee-600">
          パスワード
          <input v-model="password" type="password" :autocomplete="mode === 'login' ? 'current-password' : 'new-password'" minlength="6" required class="mt-1 w-full rounded-lg border border-coffee-200 bg-coffee-50 px-3 py-2 outline-none focus:border-coffee-400" />
        </label>
        <p v-if="error" class="text-sm text-red-600" role="alert">{{ error }}</p>
        <button :disabled="loading" class="w-full rounded-lg bg-coffee-600 px-4 py-2.5 text-white hover:bg-coffee-500 disabled:opacity-50">
          {{ loading ? '処理中…' : mode === 'login' ? 'ログイン' : '登録する' }}
        </button>
      </form>

      <button class="mt-5 w-full text-sm text-coffee-500 hover:text-coffee-600" @click="mode = mode === 'login' ? 'register' : 'login'; error = ''; notice = ''">
        {{ mode === 'login' ? '初めての方はこちら（無料登録）' : 'アカウントをお持ちの方はこちら' }}
      </button>
    </div>
  </div>
</template>

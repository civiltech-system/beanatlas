import { ref } from 'vue'
import { defineStore } from 'pinia'
import {
  createUserWithEmailAndPassword,
  onAuthStateChanged,
  sendEmailVerification,
  signInWithEmailAndPassword,
  signOut,
  type User,
} from 'firebase/auth'
import { firebaseAuth } from '@/lib/firebase'

function verificationActionCodeSettings() {
  return {
    url: `${window.location.origin}/login`,
    handleCodeInApp: true,
  }
}

export class EmailVerificationRequiredError extends Error {
  constructor() {
    super('Email verification is required')
    this.name = 'EmailVerificationRequiredError'
  }
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const ready = ref(false)
  let initialization: Promise<void> | null = null

  function initialize() {
    if (initialization) return initialization
    initialization = new Promise((resolve) => {
      onAuthStateChanged(firebaseAuth, (firebaseUser) => {
        user.value = firebaseUser
        if (!ready.value) {
          ready.value = true
          resolve()
        }
      })
    })
    return initialization
  }

  async function login(email: string, password: string) {
    const credential = await signInWithEmailAndPassword(firebaseAuth, email.trim(), password)
    if (!credential.user.emailVerified) {
      await sendEmailVerification(credential.user, verificationActionCodeSettings())
      await signOut(firebaseAuth)
      throw new EmailVerificationRequiredError()
    }
  }

  async function register(email: string, password: string) {
    const credential = await createUserWithEmailAndPassword(firebaseAuth, email.trim(), password)
    await sendEmailVerification(credential.user, verificationActionCodeSettings())
    await signOut(firebaseAuth)
  }

  async function logout() {
    await signOut(firebaseAuth)
  }

  async function getIdToken() {
    if (!user.value) throw new Error('ログインが必要です')
    return user.value.getIdToken()
  }

  return { user, ready, initialize, login, register, logout, getIdToken }
})

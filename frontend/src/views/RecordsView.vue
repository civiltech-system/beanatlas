<script setup lang="ts">
import { computed, onMounted, reactive, ref } from 'vue'
import { createRecord, deleteRecord, fetchRecords, updateRecord } from '@/api/records'
import { fetchOrigins } from '@/api/origins'
import type { Origin } from '@/types/origin'
import type { CoffeeRecord, CoffeeRecordInput } from '@/types/record'

const records = ref<CoffeeRecord[]>([])
const origins = ref<Origin[]>([])
const loading = ref(true)
const saving = ref(false)
const error = ref('')
const editingId = ref<number | null>(null)

function localDateTime() {
  const now = new Date(Date.now() - new Date().getTimezoneOffset() * 60_000)
  return now.toISOString().slice(0, 16)
}

function emptyForm(): CoffeeRecordInput {
  return {
    origin_id: null,
    coffee_name: '',
    roaster: '',
    drank_at: localDateTime(),
    brew_method: '',
    roast_level: '',
    rating: 3,
    notes: '',
  }
}

const form = reactive<CoffeeRecordInput>(emptyForm())
const originNames = computed(() => new Map(origins.value.map((origin) => [origin.id, origin.country_ja || origin.country])))

onMounted(async () => {
  try {
    const [recordData, originData] = await Promise.all([fetchRecords(), fetchOrigins()])
    records.value = recordData
    origins.value = originData
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : '読み込みに失敗しました'
  } finally {
    loading.value = false
  }
})

function resetForm() {
  Object.assign(form, emptyForm())
  editingId.value = null
  error.value = ''
}

function edit(record: CoffeeRecord) {
  editingId.value = record.id
  Object.assign(form, {
    origin_id: record.origin_id,
    coffee_name: record.coffee_name,
    roaster: record.roaster,
    drank_at: record.drank_at.slice(0, 16),
    brew_method: record.brew_method,
    roast_level: record.roast_level,
    rating: record.rating,
    notes: record.notes,
  })
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

async function save() {
  saving.value = true
  error.value = ''
  try {
    if (editingId.value) {
      const updated = await updateRecord(editingId.value, { ...form })
      const index = records.value.findIndex((record) => record.id === updated.id)
      records.value.splice(index, 1, updated)
    } else {
      records.value.unshift(await createRecord({ ...form }))
    }
    resetForm()
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : '保存に失敗しました'
  } finally {
    saving.value = false
  }
}

async function remove(record: CoffeeRecord) {
  if (!window.confirm(`「${record.coffee_name}」の記録を削除しますか？`)) return
  try {
    await deleteRecord(record.id)
    records.value = records.value.filter((item) => item.id !== record.id)
    if (editingId.value === record.id) resetForm()
  } catch (cause) {
    error.value = cause instanceof Error ? cause.message : '削除に失敗しました'
  }
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-6 py-10">
    <h1 class="text-3xl font-serif font-bold text-coffee-600 mb-2">飲んだ記録</h1>
    <p class="text-coffee-400 mb-8">豆や淹れ方、その日の味わいを残しましょう。</p>

    <form class="bg-white rounded-2xl p-6 shadow-sm mb-10" @submit.prevent="save">
      <h2 class="text-lg font-semibold text-coffee-600 mb-5">{{ editingId ? '記録を編集' : '新しい記録' }}</h2>
      <div class="grid sm:grid-cols-2 gap-4">
        <label class="text-sm text-coffee-600">コーヒー名<span class="text-red-500"> *</span>
          <input v-model="form.coffee_name" required maxlength="200" placeholder="例：エチオピア イルガチェフェ" class="form-input" />
        </label>
        <label class="text-sm text-coffee-600">飲んだ日時
          <input v-model="form.drank_at" type="datetime-local" required class="form-input" />
        </label>
        <label class="text-sm text-coffee-600">産地
          <select v-model="form.origin_id" class="form-input">
            <option :value="null">選択しない</option>
            <option v-for="origin in origins" :key="origin.id" :value="origin.id">{{ origin.country_ja || origin.country }}</option>
          </select>
        </label>
        <label class="text-sm text-coffee-600">ロースター・店名
          <input v-model="form.roaster" maxlength="200" placeholder="例：BeanAtlas Coffee" class="form-input" />
        </label>
        <label class="text-sm text-coffee-600">抽出方法
          <select v-model="form.brew_method" class="form-input">
            <option value="">選択しない</option><option>ハンドドリップ</option><option>エスプレッソ</option><option>フレンチプレス</option><option>エアロプレス</option><option>水出し</option><option>その他</option>
          </select>
        </label>
        <label class="text-sm text-coffee-600">焙煎度
          <select v-model="form.roast_level" class="form-input">
            <option value="">選択しない</option><option>浅煎り</option><option>中浅煎り</option><option>中煎り</option><option>中深煎り</option><option>深煎り</option>
          </select>
        </label>
        <label class="text-sm text-coffee-600 sm:col-span-2">評価
          <select v-model.number="form.rating" class="form-input"><option v-for="rating in 5" :key="rating" :value="rating">{{ '★'.repeat(rating) }}{{ '☆'.repeat(5 - rating) }}</option></select>
        </label>
        <label class="text-sm text-coffee-600 sm:col-span-2">メモ
          <textarea v-model="form.notes" rows="3" maxlength="2000" placeholder="香り、酸味、甘さ、次回試したいレシピなど" class="form-input resize-y" />
        </label>
      </div>
      <p v-if="error" class="mt-4 text-sm text-red-600" role="alert">{{ error }}</p>
      <div class="flex gap-3 mt-5">
        <button :disabled="saving" class="rounded-lg bg-coffee-600 px-5 py-2.5 text-white hover:bg-coffee-500 disabled:opacity-50">{{ saving ? '保存中…' : editingId ? '更新する' : '記録する' }}</button>
        <button v-if="editingId" type="button" class="rounded-lg border border-coffee-200 px-5 py-2.5 text-coffee-500" @click="resetForm">キャンセル</button>
      </div>
    </form>

    <div v-if="loading" class="text-center text-coffee-400 py-10">読み込み中…</div>
    <div v-else-if="!records.length" class="rounded-2xl border border-dashed border-coffee-300 p-10 text-center text-coffee-400">まだ記録がありません。最初の一杯を記録してみましょう。</div>
    <div v-else class="space-y-4">
      <article v-for="record in records" :key="record.id" class="bg-white rounded-2xl p-5 shadow-sm">
        <div class="flex justify-between gap-4">
          <div><p class="text-xs text-coffee-400">{{ new Date(record.drank_at).toLocaleString('ja-JP') }}</p><h2 class="text-lg font-semibold text-coffee-600">{{ record.coffee_name }}</h2><p v-if="record.roaster" class="text-sm text-coffee-400">{{ record.roaster }}</p></div>
          <div class="text-amber-500 whitespace-nowrap">{{ '★'.repeat(record.rating) }}<span class="text-coffee-200">{{ '★'.repeat(5 - record.rating) }}</span></div>
        </div>
        <div class="flex flex-wrap gap-2 mt-3 text-xs text-coffee-500"><span v-if="record.origin_id" class="rounded-full bg-coffee-100 px-3 py-1">{{ originNames.get(record.origin_id) }}</span><span v-if="record.brew_method" class="rounded-full bg-coffee-100 px-3 py-1">{{ record.brew_method }}</span><span v-if="record.roast_level" class="rounded-full bg-coffee-100 px-3 py-1">{{ record.roast_level }}</span></div>
        <p v-if="record.notes" class="mt-4 whitespace-pre-wrap text-sm leading-relaxed text-coffee-600">{{ record.notes }}</p>
        <div class="flex gap-4 mt-4 text-sm"><button class="text-origin-blue hover:underline" @click="edit(record)">編集</button><button class="text-red-500 hover:underline" @click="remove(record)">削除</button></div>
      </article>
    </div>
  </div>
</template>

<style scoped>
.form-input {
  display: block;
  width: 100%;
  margin-top: 0.25rem;
  padding: 0.5rem 0.75rem;
  border: 1px solid #e0d0c0;
  border-radius: 0.5rem;
  background: #faf7f4;
  outline: none;
}
.form-input:focus { border-color: #c8813a; }
</style>

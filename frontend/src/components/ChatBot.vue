<script setup lang="ts">
import { ref, onMounted } from "vue";
import { marked } from "marked";

interface Conversation {
  user_input: string;
  bot_response: string;
}

const userInput = ref<string>("");
const model = ref<string>("gemini-2.0-flash");
const temperature = ref<number>(0.5);
const conversations = ref<Conversation[]>([]);
const botResponse = ref<string>("");
const loading = ref<boolean>(false);

const fetchChatResponse = async () => {
  if (!userInput.value) return;

  loading.value = true;
  try {
    const response = await fetch("http://localhost:5050/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        input: userInput.value,
        model: model.value,
        temperature: temperature.value,
      }),
    });

    if (!response.ok) {
      throw new Error("API request failed");
    }

    const data = await response.json();
    console.log("Response from backend:", data);
    //botResponse.value = marked.parse(data.response);
    botResponse.value = marked(data.response);

    // 新しい会話を追加
    conversations.value.unshift({
      user_input: userInput.value,
      bot_response: data.response,
    });

    // 入力フィールドをリセット
    userInput.value = "";
  } catch (error) {
    console.error("Error:", error);
  } finally {
    loading.value = false;
  }
};

const adjustHeight = (event: Event) => {
  const element = event.target as HTMLTextAreaElement;
  element.style.height = "auto";
  element.style.height = `${element.scrollHeight}px`;
};

// 初回ロード時に会話ログを取得
onMounted(async () => {
  try {
    const response = await fetch("/");
    const data = await response.json();
    conversations.value = data.conversations || [];
  } catch (error) {
    console.error("Error loading conversation log:", error);
  }
});
</script>

<template>
  <div>
    <h1>Chatbot <span id="smallfont">powered by GeminiAI</span></h1>
    <div>
      keisuke.Oが練習用に作成したアプリケーションです（vue+TypeScript
      ver）。Dockerで起動成功
    </div>

    <label for="model-select">モデルを選択：</label>
    <select id="model-select" v-model="model">
      <option value="gemini-2.0-flash">Gemini 2.0 Flash</option>
      <option value="gemini-1.5-flash">Gemini 1.5 Flash</option>
      <option value="gemini-2.0-pro">Gemini 2.0 Pro</option>
    </select>

    <label for="temperature-slider">temperature（創造性）:</label>
    <input
      type="range"
      id="temperature-slider"
      min="0.0"
      max="1.0"
      step="0.1"
      v-model="temperature"
    />
    <span>{{ temperature }}</span>

    <div class="container">
      <textarea
        id="user-input"
        v-model="userInput"
        placeholder="こんにちは！私はGeminiのチャットボットです。 どんなご用件でしょうか？"
        @input="adjustHeight"
      ></textarea>
      <button :disabled="loading" @click="fetchChatResponse">
        {{ loading ? "送信中..." : "送信" }}
      </button>
    </div>

    <div v-if="loading" id="loading-icon">読み込み中...</div>

    <div v-html="botResponse"></div>

    <h2>会話ログ</h2>
    <div v-for="(conversation, index) in conversations" :key="index">
      <div><strong>過去の質問:</strong> {{ conversation.user_input }}</div>
      <div><strong>Geminiの返答:</strong> {{ conversation.bot_response }}</div>
      <hr />
    </div>

    <footer>
      <p>&copy; 2024 Kei.O. All rights reserved.</p>
    </footer>
  </div>
</template>

<style scoped>
h1 {
  font-size: 24px;
}
.container {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
textarea {
  width: 100%;
  min-height: 50px;
}
button {
  cursor: pointer;
}
</style>

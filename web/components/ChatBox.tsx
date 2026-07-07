"use client";

import { FormEvent, useState } from "react";

import { ChatResponse } from "../lib/api";

type Message = {
  role: "user" | "assistant";
  text: string;
  refused?: boolean;
};

export function ChatBox({
  disabled,
  onAsk
}: {
  disabled: boolean;
  onAsk: (question: string) => Promise<ChatResponse>;
}) {
  const [question, setQuestion] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const trimmed = question.trim();
    if (!trimmed || disabled || loading) {
      return;
    }

    setQuestion("");
    setLoading(true);
    setMessages((current) => [...current, { role: "user", text: trimmed }]);
    const response = await onAsk(trimmed);
    setMessages((current) => [
      ...current,
      { role: "assistant", text: response.answer, refused: response.refused }
    ]);
    setLoading(false);
  }

  return (
    <section style={panelStyle}>
      <h2 style={{ margin: "0 0 12px", fontSize: 18 }}>Scoped Chat</h2>
      <div style={{ display: "grid", gap: 10, minHeight: 140 }}>
        {messages.length ? (
          messages.map((message, index) => (
            <div
              key={`${message.role}-${index}`}
              style={{
                justifySelf: message.role === "user" ? "end" : "start",
                maxWidth: "92%",
                background: message.role === "user" ? "#e9f2ff" : "#f7f7f8",
                border: message.refused ? "1px solid #f2b8b5" : "1px solid #e4e7ec",
                borderRadius: 8,
                padding: "10px 12px",
                whiteSpace: "pre-wrap",
                fontSize: 14
              }}
            >
              {message.text}
            </div>
          ))
        ) : (
          <p style={{ margin: 0, color: "#667085", fontSize: 14 }}>
            Ask about summary, top risks, salary, termination, probation, non-compete, or penalties.
          </p>
        )}
      </div>

      <form onSubmit={handleSubmit} style={{ display: "flex", gap: 8, marginTop: 14 }}>
        <input
          value={question}
          disabled={disabled || loading}
          onChange={(event) => setQuestion(event.target.value)}
          placeholder="List the top risks"
          style={{
            flex: 1,
            border: "1px solid #cfd6df",
            borderRadius: 8,
            padding: "10px 12px",
            fontSize: 14
          }}
        />
        <button type="submit" disabled={disabled || loading} style={buttonStyle}>
          {loading ? "..." : "Send"}
        </button>
      </form>
    </section>
  );
}

const panelStyle = {
  background: "#ffffff",
  border: "1px solid #d7dde5",
  borderRadius: 8,
  padding: 16
};

const buttonStyle = {
  border: "1px solid #1f5fbf",
  background: "#1f5fbf",
  color: "#ffffff",
  borderRadius: 8,
  padding: "10px 14px",
  fontWeight: 700,
  cursor: "pointer"
};

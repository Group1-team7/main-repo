"use client";

export function ContractInput({
  value,
  loading,
  onChange,
  onAnalyze
}: {
  value: string;
  loading: boolean;
  onChange: (value: string) => void;
  onAnalyze: () => void;
}) {
  return (
    <section style={panelStyle}>
      <label htmlFor="contract-text" style={{ display: "block", fontWeight: 700, marginBottom: 10 }}>
        Contract Text
      </label>
      <textarea
        id="contract-text"
        value={value}
        dir="rtl"
        onChange={(event) => onChange(event.target.value)}
        style={{
          width: "100%",
          minHeight: 360,
          boxSizing: "border-box",
          resize: "vertical",
          border: "1px solid #cfd6df",
          borderRadius: 8,
          padding: 14,
          fontSize: 16,
          lineHeight: 1.7,
          background: "#fcfcfd"
        }}
      />
      <button
        type="button"
        disabled={loading || !value.trim()}
        onClick={onAnalyze}
        style={{
          marginTop: 12,
          border: "1px solid #0b6b58",
          background: loading ? "#8ab8ad" : "#0b6b58",
          color: "#ffffff",
          borderRadius: 8,
          padding: "11px 18px",
          fontWeight: 800,
          cursor: loading ? "default" : "pointer"
        }}
      >
        {loading ? "Analyzing..." : "Analyze"}
      </button>
    </section>
  );
}

const panelStyle = {
  background: "#ffffff",
  border: "1px solid #d7dde5",
  borderRadius: 8,
  padding: 16
};

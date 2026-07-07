import { DetectedRisk } from "../lib/api";

export function RiskCard({ risk }: { risk: DetectedRisk }) {
  return (
    <article
      style={{
        background: "#ffffff",
        border: "1px solid #d7dde5",
        borderRadius: 8,
        padding: 16,
        minHeight: 210
      }}
    >
      <div style={{ display: "flex", justifyContent: "space-between", gap: 12 }}>
        <h3 style={{ margin: 0, fontSize: 17 }}>{risk.risk_type}</h3>
        <span
          style={{
            alignSelf: "start",
            borderRadius: 999,
            padding: "4px 9px",
            background: levelBackground(risk.risk_level),
            color: "#20242c",
            fontSize: 12,
            fontWeight: 800
          }}
        >
          {risk.risk_level}
        </span>
      </div>

      <p style={{ color: "#475467", lineHeight: 1.55 }}>{risk.reason}</p>
      <p dir="rtl" style={{ background: "#f7f7f8", borderRadius: 8, padding: 10, lineHeight: 1.6 }}>
        {risk.clause_text}
      </p>
      <p style={{ marginBottom: 0, color: "#344054", lineHeight: 1.5 }}>
        {risk.safe_recommendation}
      </p>
    </article>
  );
}

function levelBackground(level: DetectedRisk["risk_level"]) {
  if (level === "high") {
    return "#ffd6d6";
  }
  if (level === "medium") {
    return "#ffe8b3";
  }
  return "#d8f5df";
}

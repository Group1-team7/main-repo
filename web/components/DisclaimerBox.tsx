const DEFAULT_DISCLAIMER =
  "Educational capstone MVP only. This output is not legal advice, does not decide whether a clause is legal or illegal, and should not be used as a sign/do-not-sign recommendation. Review any potential risk with a qualified lawyer in Jordan.";

export function DisclaimerBox({ text }: { text?: string }) {
  return (
    <aside
      style={{
        background: "#fff8e6",
        border: "1px solid #f0d99c",
        borderRadius: 8,
        padding: 16,
        color: "#5c4600"
      }}
    >
      <strong style={{ display: "block", marginBottom: 6 }}>Disclaimer</strong>
      <p style={{ margin: 0, lineHeight: 1.55 }}>{text || DEFAULT_DISCLAIMER}</p>
    </aside>
  );
}

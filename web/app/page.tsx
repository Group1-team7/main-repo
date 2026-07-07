"use client";

import { useMemo, useState } from "react";

import { ChatBox } from "../components/ChatBox";
import { ContractInput } from "../components/ContractInput";
import { DisclaimerBox } from "../components/DisclaimerBox";
import { RiskCard } from "../components/RiskCard";
import {
  analyzeContract,
  ChatResponse,
  LegalSnippet,
  ReportResponse,
  sendChat
} from "../lib/api";
import { mockAnalyzeContract, mockChat } from "../lib/mock";

const INITIAL_TEXT = `البند 1: يعمل الموظف لدى الشركة بوظيفة مساعد إداري.

البند 2: يحدد الراتب لاحقاً حسب تقدير الشركة.

البند 3: يجوز لصاحب العمل إنهاء العقد في أي وقت دون إشعار.

البند 4: يلتزم الموظف بعد انتهاء العقد بعدم منافسة الشركة في أي مكان لمدة سنتين.`;

export default function Page() {
  const [contractText, setContractText] = useState(INITIAL_TEXT);
  const [report, setReport] = useState<ReportResponse | null>(null);
  const [status, setStatus] = useState("");
  const [loading, setLoading] = useState(false);

  const citations = useMemo(() => collectCitations(report), [report]);

  async function handleAnalyze() {
    setLoading(true);
    setStatus("");
    try {
      setReport(await analyzeContract(contractText));
    } catch {
      setReport(mockAnalyzeContract(contractText));
      setStatus("Backend unavailable. Showing mock fallback.");
    } finally {
      setLoading(false);
    }
  }

  async function handleAsk(question: string): Promise<ChatResponse> {
    try {
      return await sendChat(question, contractText);
    } catch {
      return mockChat(question);
    }
  }

  return (
    <main style={{ maxWidth: 1120, margin: "0 auto", padding: "32px 20px 48px" }}>
      <header style={{ marginBottom: 24 }}>
        <p style={{ margin: "0 0 6px", color: "#667085", fontSize: 14 }}>
          AI.SPIRE Module 12 Capstone
        </p>
        <h1 style={{ margin: 0, fontSize: 34, lineHeight: 1.15 }}>
          Lawz AI JO Ultra-MVP
        </h1>
      </header>

      <section
        style={{
          display: "grid",
          gridTemplateColumns: "minmax(0, 1.1fr) minmax(320px, 0.9fr)",
          gap: 20,
          alignItems: "start"
        }}
      >
        <div>
          <ContractInput
            value={contractText}
            loading={loading}
            onChange={setContractText}
            onAnalyze={handleAnalyze}
          />
          {status ? (
            <p style={{ margin: "10px 0 0", color: "#8a4b00", fontSize: 14 }}>{status}</p>
          ) : null}
        </div>

        <div style={{ display: "grid", gap: 14 }}>
          <DisclaimerBox text={report?.disclaimer} />
          <ChatBox disabled={!contractText.trim()} onAsk={handleAsk} />
        </div>
      </section>

      <section style={{ marginTop: 28 }}>
        <div
          style={{
            display: "flex",
            alignItems: "baseline",
            justifyContent: "space-between",
            gap: 16,
            flexWrap: "wrap"
          }}
        >
          <h2 style={{ margin: 0, fontSize: 22 }}>Detected Risks</h2>
          {report ? (
            <span style={{ color: "#667085", fontSize: 14 }}>
              {report.clause_count} clauses · overall {report.overall_risk_level}
            </span>
          ) : null}
        </div>

        <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fit, minmax(260px, 1fr))", gap: 14, marginTop: 14 }}>
          {report?.detected_risks.length ? (
            report.detected_risks.map((risk) => <RiskCard key={risk.risk_id} risk={risk} />)
          ) : (
            <div style={emptyStateStyle}>
              {report ? "No predefined potential risks were detected." : "Run analysis to view results."}
            </div>
          )}
        </div>
      </section>

      <section style={{ marginTop: 28 }}>
        <h2 style={{ margin: "0 0 14px", fontSize: 22 }}>Citations</h2>
        <div style={panelStyle}>
          {citations.length ? (
            citations.map((citation) => (
              <div key={`${citation.risk_type}-${citation.source_id}`} style={{ padding: "12px 0", borderBottom: "1px solid #eceff3" }}>
                <strong>{citation.source_id}</strong>
                <p style={{ margin: "6px 0", color: "#475467" }}>{citation.snippet}</p>
                <small style={{ color: "#667085" }}>
                  {citation.source_url} · {citation.last_verified} · {citation.trust_level}
                </small>
              </div>
            ))
          ) : (
            <p style={{ margin: 0, color: "#667085" }}>No citations loaded yet.</p>
          )}
        </div>
      </section>
    </main>
  );
}

function collectCitations(report: ReportResponse | null): LegalSnippet[] {
  if (!report) {
    return [];
  }
  const seen = new Set<string>();
  const citations: LegalSnippet[] = [];
  for (const risk of report.detected_risks) {
    for (const source of risk.sources) {
      const key = `${source.risk_type}:${source.source_id}`;
      if (!seen.has(key)) {
        citations.push(source);
        seen.add(key);
      }
    }
  }
  return citations;
}

const panelStyle = {
  background: "#ffffff",
  border: "1px solid #d7dde5",
  borderRadius: 8,
  padding: 16
};

const emptyStateStyle = {
  ...panelStyle,
  color: "#667085",
  minHeight: 92,
  display: "grid",
  placeItems: "center"
};

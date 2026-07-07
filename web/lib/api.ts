export type RiskType =
  | "termination_without_notice"
  | "salary_unclear"
  | "probation_unclear_or_long"
  | "non_compete_overreach"
  | "penalty_or_deduction_clause";

export type RiskLevel = "low" | "medium" | "high";

export type LegalSnippet = {
  risk_type: RiskType;
  source_id: string;
  source_title: string;
  source_url: string;
  snippet: string;
  last_verified: string;
  trust_level: string;
  notes?: string | null;
};

export type DetectedRisk = {
  risk_id: string;
  risk_type: RiskType;
  risk_level: RiskLevel;
  clause_id: number;
  clause_text: string;
  reason: string;
  sources: LegalSnippet[];
  safe_recommendation: string;
};

export type ReportResponse = {
  contract_summary: string;
  clause_count: number;
  detected_risks: DetectedRisk[];
  overall_risk_level: RiskLevel;
  safe_recommendation: string;
  disclaimer: string;
};

export type ChatResponse = {
  answer: string;
  refused: boolean;
  citations: LegalSnippet[];
  disclaimer: string;
};

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

export async function analyzeContract(contractText: string): Promise<ReportResponse> {
  return postJson<ReportResponse>("/analyze-contract", { contract_text: contractText });
}

export async function sendChat(question: string, contractText: string): Promise<ChatResponse> {
  return postJson<ChatResponse>("/chat", { question, contract_text: contractText });
}

async function postJson<T>(path: string, body: unknown): Promise<T> {
  const response = await fetch(`${API_BASE}${path}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(body)
  });

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json() as Promise<T>;
}

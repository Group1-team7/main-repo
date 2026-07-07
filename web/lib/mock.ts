import { ChatResponse, ReportResponse } from "./api";

const disclaimer =
  "Educational capstone MVP only. This output is not legal advice, does not decide whether a clause is legal or illegal, and should not be used as a sign/do-not-sign recommendation. Review any potential risk with a qualified lawyer in Jordan.";

export function mockAnalyzeContract(contractText: string): ReportResponse {
  // TODO[PERSON-4]: Keep mock output aligned with backend response shape during UI changes.
  return {
    contract_summary:
      "تم تحليل النص كعقد عمل لأغراض تعليمية أولية. تم استخدام بيانات mock بسبب عدم توفر backend.",
    clause_count: contractText.split(/\n+/).filter(Boolean).length,
    overall_risk_level: "high",
    safe_recommendation:
      "Treat the flagged items as a first-pass review checklist only and review with a qualified lawyer.",
    disclaimer,
    detected_risks: [
      {
        risk_id: "termination_without_notice-mock",
        risk_type: "termination_without_notice",
        risk_level: "high",
        clause_id: 3,
        clause_text: "يجوز لصاحب العمل إنهاء العقد في أي وقت دون إشعار.",
        reason:
          "The clause mentions ending employment with wording that may remove or weaken notice.",
        safe_recommendation:
          "Review notice-period wording with a qualified lawyer before relying on it.",
        sources: [
          {
            risk_type: "termination_without_notice",
            source_id: "MANUAL_VERIFY_JO_LABOR_LAW_TERMINATION_NOTICE",
            source_title:
              "MANUAL_FILL_FROM_OFFICIAL_SOURCE - Jordanian labor law notice/termination provision",
            source_url: "MANUAL_FILL_FROM_OFFICIAL_SOURCE",
            snippet:
              "MANUAL_FILL_FROM_OFFICIAL_SOURCE: Insert a manually verified official Jordanian snippet.",
            last_verified: "MANUAL_VERIFY",
            trust_level: "placeholder_unverified"
          }
        ]
      }
    ]
  };
}

export function mockChat(question: string): ChatResponse {
  const refused = /sign|illegal|lawsuit|sue|غير قانوني|دعوى|أوقع|اوقع/i.test(question);
  return {
    refused,
    answer: refused
      ? "I cannot provide final legal advice, decide legality, recommend signing, draft a lawsuit, or advise whether to sue."
      : "Potential risks found in the pasted contract:\n- termination_without_notice (high): The clause may be related to notice-period review.\nUse these points as a review checklist with a qualified lawyer.",
    citations: [],
    disclaimer
  };
}

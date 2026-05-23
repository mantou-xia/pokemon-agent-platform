/**
 * Dify Chat API 客户端
 */

export interface DifyAppParams {
  opening_statement: string;
  suggested_questions: string[];
  user_input_form: UserInputField[];
}

export interface UserInputField {
  type: "text-input" | "select" | "paragraph" | "number";
  label: string;
  variable: string;
  required: boolean;
  default?: string;
  options?: { label: string; value: string }[];
}

export interface DifyMessage {
  role: "user" | "assistant" | "tool";
  content: string;
  toolCalls?: ToolCallInfo[];
}

export interface ToolCallInfo {
  tool: string;
  input: string;
  observation?: string;
}

export interface DifyStreamEvent {
  event: string;
  conversation_id?: string;
  message_id?: string;
  answer?: string;
  tool?: string;
  tool_input?: string;
  observation?: string;
}

const API_BASE = process.env.NEXT_PUBLIC_DIFY_API_URL || "http://localhost/v1";
const API_KEY = process.env.NEXT_PUBLIC_DIFY_API_KEY || "app-MxbH9j4SG861NENYrNf1hRsJ";

export class DifyClient {
  private conversationId: string | null = null;
  private abortController: AbortController | null = null;

  getConversationId(): string | null {
    return this.conversationId;
  }

  cancel() {
    this.abortController?.abort();
  }

  /** 获取应用参数（开场白、建议问题、变量配置） */
  async getAppParams(): Promise<DifyAppParams> {
    const resp = await fetch(`${API_BASE}/parameters`, {
      headers: { Authorization: `Bearer ${API_KEY}` },
    });
    if (!resp.ok) throw new Error(`Failed to get params: ${resp.status}`);
    const data = await resp.json();
    return {
      opening_statement: data.opening_statement || "",
      suggested_questions: data.suggested_questions || [],
      user_input_form: parseUserInputForm(data.user_input_form || []),
    };
  }

  async *chat(
    query: string,
    inputs: Record<string, string> = {},
    user: string = "web-user"
  ): AsyncGenerator<DifyStreamEvent> {
    this.abortController = new AbortController();

    const body = JSON.stringify({
      inputs: { user_name: user, assistant_name: "宝可梦助手", ...inputs },
      query,
      response_mode: "streaming",
      user,
      conversation_id: this.conversationId || "",
    });

    const response = await fetch(`${API_BASE}/chat-messages`, {
      method: "POST",
      headers: {
        Authorization: `Bearer ${API_KEY}`,
        "Content-Type": "application/json",
      },
      body,
      signal: this.abortController.signal,
    });

    if (!response.ok) {
      const text = await response.text();
      throw new Error(`Dify API error (${response.status}): ${text}`);
    }

    const reader = response.body?.getReader();
    if (!reader) throw new Error("No response body");

    const decoder = new TextDecoder();
    let buffer = "";

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() || "";

      for (const line of lines) {
        const trimmed = line.trim();
        if (!trimmed || !trimmed.startsWith("data: ")) continue;
        try {
          const event: DifyStreamEvent = JSON.parse(trimmed.slice(6));
          if (event.conversation_id) {
            this.conversationId = event.conversation_id;
          }
          yield event;
        } catch {
          // skip malformed events
        }
      }
    }
  }
}

function parseUserInputForm(
  raw: Record<string, Record<string, unknown>>[]
): UserInputField[] {
  return raw.map((item) => {
    const [type, config] = Object.entries(item)[0];
    return {
      type: type as UserInputField["type"],
      label: (config.label as string) || "",
      variable: (config.variable as string) || "",
      required: (config.required as boolean) || false,
      default: (config.default as string) || "",
      options: (config.options as { label: string; value: string }[]) || undefined,
    };
  });
}
